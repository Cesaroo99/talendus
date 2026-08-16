"""Envoi d'e-mails : journalisation immédiate, SMTP asynchrone (file en mémoire)."""

from __future__ import annotations

import logging
import queue
import smtplib
import threading
import time
from email.message import EmailMessage
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import EmailLog
from app.models.enums import EmailStatus, EmailType

logger = logging.getLogger("talendus.email")
settings = get_settings()
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "emails" / "templates"

_queue: queue.Queue[tuple[str, str, str, str]] = queue.Queue()
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
    log = EmailLog(to_email=to_email, type=email_type, subject=subject, status=EmailStatus.QUEUED)
    db.add(log)
    db.flush()
    if not settings.email_enabled:
        log.status = EmailStatus.SENT
        logger.info("email[dev] to=%s type=%s subject=%s", to_email, email_type, subject)
        return log
    _queue.put((log.id, to_email, subject, body))
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
        logger.info("email worker started")


def _loop() -> None:
    from app.database import SessionLocal

    while True:
        log_id, to_email, subject, body = _queue.get()
        try:
            _deliver(SessionLocal, log_id, to_email, subject, body)
        except Exception as exc:  # noqa: BLE001
            logger.warning("email worker error: %s", exc)
        finally:
            _queue.task_done()


def _deliver(session_factory, log_id: str, to_email: str, subject: str, body: str) -> None:
    last_error = ""
    for attempt in range(5):
        db = session_factory()
        try:
            log = db.get(EmailLog, log_id)
            if log is None:
                time.sleep(0.1 * (attempt + 1))
                continue
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
            except Exception as exc:  # noqa: BLE001
                log.status = EmailStatus.FAILED
                log.error = str(exc)[:2000]
                logger.warning("email failed to=%s: %s", to_email, exc)
            db.commit()
            return
        finally:
            db.close()
    logger.warning("email log %s introuvable après retries (%s)", log_id, last_error)
