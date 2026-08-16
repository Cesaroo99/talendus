"""Envoi d'e-mails : journalisation persistée, worker qui relit la file en base."""

from __future__ import annotations

import logging
import queue
import smtplib
import threading
import time
from email.message import EmailMessage
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import EmailLog
from app.models.enums import EmailStatus, EmailType, utcnow

logger = logging.getLogger("talendus.email")
settings = get_settings()
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "emails" / "templates"

_queue: queue.Queue[str] = queue.Queue()
_worker_lock = threading.Lock()
_worker_started = False


def _render(template_name: str, **ctx: str) -> tuple[str, str]:
    path = TEMPLATE_DIR / f"{template_name}.txt"
    if not path.exists():
        body = "\n".join(f"{k}: {v}" for k, v in ctx.items())
        return ctx.get("subject", "Talendus"), body
    raw = path.read_text(encoding="utf-8")
    for key, value in ctx.items():
        raw = raw.replace("{{" + key + "}}", str(value))
    lines = raw.splitlines()
    subject = lines[0].replace("Subject:", "").strip() if lines else "Talendus"
    body = "\n".join(lines[2:] if len(lines) > 2 else lines)
    return subject, body


def send_email(db: Session, to_email: str, email_type: EmailType, template: str, **ctx: str) -> EmailLog:
    subject, body = _render(template, **ctx)
    log = EmailLog(
        to_email=to_email,
        type=email_type,
        subject=subject,
        body=body,
        status=EmailStatus.QUEUED,
        attempts=0,
    )
    db.add(log)
    db.flush()
    if not settings.email_enabled:
        log.status = EmailStatus.SENT
        log.sent_at = utcnow()
        logger.info("email[dev] to=%s type=%s subject=%s", to_email, email_type, subject)
        return log
    _queue.put(log.id)
    start_worker()
    return log


def start_worker() -> None:
    global _worker_started
    with _worker_lock:
        if _worker_started:
            return
        thread = threading.Thread(target=_loop, name="talendus-email", daemon=True)
        thread.start()
        _worker_started = True
        logger.info("email worker started (file persistée)")


def _loop() -> None:
    from app.database import SessionLocal

    while True:
        log_id = None
        try:
            log_id = _queue.get(timeout=8)
        except queue.Empty:
            pass
        try:
            if log_id:
                _deliver(SessionLocal, log_id)
            else:
                _reap(SessionLocal)
        except Exception as exc:  # noqa: BLE001
            logger.warning("email worker error: %s", exc)
        finally:
            if log_id:
                _queue.task_done()


def _reap(session_factory) -> None:
    db = session_factory()
    try:
        ids = list(
            db.scalars(
                select(EmailLog.id).where(EmailLog.status == EmailStatus.QUEUED).order_by(EmailLog.created_at.asc()).limit(20)
            ).all()
        )
    finally:
        db.close()
    for log_id in ids:
        _deliver(session_factory, log_id)


def _deliver(session_factory, log_id: str) -> None:
    for attempt in range(5):
        db = session_factory()
        try:
            log = db.get(EmailLog, log_id)
            if log is None:
                time.sleep(0.1 * (attempt + 1))
                continue
            if log.status == EmailStatus.SENT:
                return
            to_email = log.to_email
            subject = log.subject
            body = log.body or ""
            try:
                msg = EmailMessage()
                msg["From"] = settings.email_from
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.set_content(body)
                with smtplib.SMTP(settings.email_server, settings.email_port, timeout=10) as smtp:
                    if settings.email_use_tls:
                        smtp.starttls()
                    if settings.email_username:
                        smtp.login(settings.email_username, settings.email_password)
                    smtp.send_message(msg)
                log.status = EmailStatus.SENT
                log.error = None
                log.sent_at = utcnow()
                log.attempts = (log.attempts or 0) + 1
            except Exception as exc:  # noqa: BLE001
                log.attempts = (log.attempts or 0) + 1
                log.error = str(exc)[:2000]
                if log.attempts >= 5:
                    log.status = EmailStatus.FAILED
                else:
                    log.status = EmailStatus.QUEUED
                logger.warning("email failed to=%s attempt=%s: %s", to_email, log.attempts, exc)
            db.commit()
            return
        finally:
            db.close()
    logger.warning("email log %s introuvable après retries", log_id)
