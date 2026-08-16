import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import EmailLog
from app.models.enums import EmailStatus, EmailType

logger = logging.getLogger("talendus.email")
settings = get_settings()
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "emails" / "templates"


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
    try:
        if not settings.email_enabled:
            log.status = EmailStatus.SENT
            logger.info("email[dev] to=%s type=%s subject=%s", to_email, email_type, subject)
            return log
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
    except Exception as exc:  # noqa: BLE001
        log.status = EmailStatus.FAILED
        log.error = str(exc)[:2000]
        logger.warning("email failed to=%s: %s", to_email, exc)
    return log
