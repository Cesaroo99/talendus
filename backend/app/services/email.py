"""Envoi d'e-mails : journalisation persistée, worker qui relit la file en base."""

from __future__ import annotations

import logging
import queue
import re
import smtplib
import threading
import time
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import EmailLog
from app.models.enums import EmailStatus, EmailType, utcnow

logger = logging.getLogger("talendus.email")
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "emails" / "templates"

_queue: queue.Queue[str] = queue.Queue()
_worker_lock = threading.Lock()
_worker_started = False


@dataclass(frozen=True)
class SmtpRuntime:
    enabled: bool
    host: str
    port: int
    username: str
    password: str
    from_addr: str
    use_tls: bool
    reply_to: str


def _truthy(value: str | None) -> bool | None:
    raw = (value or "").strip().lower()
    if raw in {"1", "true", "oui", "on", "yes"}:
        return True
    if raw in {"0", "false", "non", "off", "no"}:
        return False
    return None


def load_smtp_overrides(db: Session | None) -> dict[str, str]:
    if db is None:
        return {}
    try:
        from app.models import SystemSetting

        rows = db.scalars(select(SystemSetting).where(SystemSetting.key.like("smtp.%"))).all()
        return {row.key: (row.value or "") for row in rows}
    except Exception:  # noqa: BLE001
        return {}


def normalize_smtp_username(raw: str | None) -> str:
    value = (raw or "").strip()
    angled = re.search(r"<([^>]+)>", value)
    if angled:
        value = angled.group(1).strip()
    return value.lower()


def normalize_smtp_password(raw: str | None) -> str:
    return "".join((raw or "").split())


def is_smtp_bad_credentials(error: str | None) -> bool:
    raw = error or ""
    return (
        "5.7.8" in raw
        or "BadCredentials" in raw
        or "Username and Password not accepted" in raw
        or "535" in raw and "not accepted" in raw.lower()
    )


def runtime_email_config(db: Session | None = None) -> SmtpRuntime:
    env = get_settings()
    stored = load_smtp_overrides(db)
    enabled_ov = _truthy(stored.get("smtp.enabled"))
    tls_ov = _truthy(stored.get("smtp.use_tls"))
    port_raw = (stored.get("smtp.port") or "").strip()
    try:
        port = int(port_raw) if port_raw else int(env.email_port)
    except ValueError:
        port = int(env.email_port)
    password = normalize_smtp_password(stored.get("smtp.password")) or normalize_smtp_password(env.email_password)
    from_addr = (
        (stored.get("smtp.from") or "").strip()
        or (env.email_from or "").strip()
        or "Talendus <info@talendus.ca>"
    )
    return SmtpRuntime(
        enabled=env.email_enabled if enabled_ov is None else enabled_ov,
        host=(stored.get("smtp.host") or "").strip() or env.email_server,
        port=port,
        username=normalize_smtp_username(stored.get("smtp.username")) or (env.email_username or "").strip(),
        password=password,
        from_addr=from_addr,
        use_tls=env.email_use_tls if tls_ov is None else tls_ov,
        reply_to=(env.public_email or "info@talendus.ca").strip(),
    )


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


def _smtp_send(cfg: SmtpRuntime, to_email: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = cfg.from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    if cfg.reply_to:
        msg["Reply-To"] = cfg.reply_to
    msg.set_content(body)
    with smtplib.SMTP(cfg.host, cfg.port, timeout=15) as smtp:
        if cfg.use_tls:
            smtp.starttls()
        if cfg.username:
            smtp.login(cfg.username, cfg.password)
        smtp.send_message(msg)


def _record_smtp_result(log: EmailLog, cfg: SmtpRuntime, *, fail_fast: bool = False) -> None:
    try:
        _smtp_send(cfg, log.to_email, log.subject, log.body or "")
        log.status = EmailStatus.SENT
        log.error = None
        log.sent_at = utcnow()
        log.attempts = (log.attempts or 0) + 1
    except Exception as exc:  # noqa: BLE001
        log.attempts = (log.attempts or 0) + 1
        log.error = str(exc)[:2000]
        log.status = EmailStatus.FAILED if fail_fast or log.attempts >= 5 else EmailStatus.QUEUED
        logger.warning("email failed to=%s attempt=%s: %s", log.to_email, log.attempts, exc)


def send_email(
    db: Session,
    to_email: str,
    email_type: EmailType,
    template: str,
    *,
    sync: bool = False,
    **ctx: str,
) -> EmailLog:
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
    cfg = runtime_email_config(db)
    if not cfg.enabled:
        log.status = EmailStatus.SENT
        log.sent_at = utcnow()
        logger.info("email[dev] to=%s type=%s subject=%s", to_email, email_type, subject)
        return log
    if sync:
        _record_smtp_result(log, cfg, fail_fast=True)
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
            cfg = runtime_email_config(db)
            _record_smtp_result(log, cfg, fail_fast=False)
            db.commit()
            return
        finally:
            db.close()
    logger.warning("email log %s introuvable après retries", log_id)
