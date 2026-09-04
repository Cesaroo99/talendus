"""Envoi d'e-mails : journalisation persistée, worker qui relit la file en base."""

from __future__ import annotations

import html
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
EMAIL_DIR = Path(__file__).resolve().parents[1] / "emails"
TEMPLATE_DIR = EMAIL_DIR / "templates"
SIGNATURE_IMAGE = EMAIL_DIR / "assets" / "signature.jpg"
SIGNATURE_CID = "talendus-signature@talendus.ca"
SIGNATURE_TEXT = (
    "\n\n—\n"
    "Talendus\n"
    "Votre partenaire stratégique en recrutement au Québec.\n"
    "info@talendus.ca · 263 558 5225 · talendus.ca\n"
)
_LEGACY_FOOTER = re.compile(
    r"(?:\r?\n)+Talendus\s*·\s*info@talendus\.ca(?:\s*·\s*[^\n]+)?\s*$",
    re.IGNORECASE,
)
_URL_RE = re.compile(r"(https?://[^\s<]+)")

_queue: queue.Queue[str] = queue.Queue()
_worker_lock = threading.Lock()
_worker_started = False


@dataclass(frozen=True)
class EmailAttachment:
    filename: str
    data: bytes
    mime: str = "application/octet-stream"
    kind: str = ""
    label: str = ""


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


def strip_legacy_footer(body: str) -> str:
    text = _LEGACY_FOOTER.sub("", body or "")
    marker = "\n—\nTalendus\n"
    if marker in text:
        text = text[: text.rfind(marker)]
    return text.rstrip()


def signed_plain(body: str) -> str:
    core = strip_legacy_footer(body)
    if not core:
        return SIGNATURE_TEXT.lstrip()
    return f"{core}{SIGNATURE_TEXT}"


_LINK_BTN = (
    '<a href="{href}" style="display:inline-block;margin:6px 0 2px;padding:11px 18px;'
    "background:#ff6b00;color:#ffffff;text-decoration:none;font-weight:700;"
    'font-size:14px;border-radius:6px;">{label}</a>'
)
_LINK_INLINE = '<a href="{href}" style="color:#0b1f3a;font-weight:700;">{href}</a>'


def _linkify(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        href = match.group(1).rstrip(").,;")
        label = "Ouvrir mon espace"
        if "employeur" in href:
            label = "Déposer le besoin"
        if match.group(0) == match.string.strip() or text.strip() == match.group(0):
            return _LINK_BTN.format(href=href, label=label)
        return _LINK_INLINE.format(href=href)

    return _URL_RE.sub(repl, text)


def _html_list(lines: list[str]) -> str:
    items = []
    for line in lines:
        item = re.sub(r"^(?:[-•]|\d+[.)])\s+", "", line).strip()
        if not item:
            continue
        items.append(f'<li style="margin:0 0 8px;">{_linkify(item)}</li>')
    if not items:
        return ""
    return (
        '<ul style="margin:0 0 16px;padding:0 0 0 20px;font-family:Arial,Helvetica,sans-serif;">'
        + "".join(items)
        + "</ul>"
    )


def _text_to_html_blocks(core: str) -> str:
    escaped = html.escape(core or "")
    blocks = []
    for raw in re.split(r"\n\s*\n", escaped):
        block = raw.strip()
        if not block:
            continue
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        is_list = len(lines) > 1 and all(re.match(r"^(?:[-•]|\d+[.)])\s+", ln) for ln in lines)
        is_attach = block.lower().startswith("pièce jointe")
        if is_list:
            html_block = _html_list(lines)
        else:
            rendered = "<br>\n".join(_linkify(ln) for ln in lines)
            html_block = f'<p style="margin:0 0 16px;">{rendered}</p>'
        if is_attach:
            html_block = (
                '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
                'style="margin:8px 0 20px;border:1px solid #f3d2b8;border-left:4px solid #ff6b00;'
                'background:#fff8f1;border-radius:8px;">'
                f'<tr><td style="padding:14px 16px;font-family:Arial,Helvetica,sans-serif;'
                f'font-size:15px;line-height:1.55;color:#1a2332;">{html_block}</td></tr></table>'
            )
        blocks.append(html_block)
    return "".join(blocks) or '<p style="margin:0;"></p>'


def signed_html(body: str) -> str:
    core = strip_legacy_footer(body)
    inner = _text_to_html_blocks(core)
    return (
        "<!DOCTYPE html><html lang=\"fr-CA\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        '<body style="margin:0;padding:0;background:#e8edf4;">'
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#e8edf4;">'
        '<tr><td align="center" style="padding:28px 12px;">'
        '<table role="presentation" width="600" cellspacing="0" cellpadding="0" '
        'style="max-width:600px;width:100%;background:#ffffff;border:1px solid #d5dce6;border-radius:12px;">'
        '<tr><td style="height:5px;background:#ff6b00;font-size:0;line-height:0;border-radius:12px 12px 0 0;">&nbsp;</td></tr>'
        '<tr><td style="padding:18px 28px 14px;background:#0b1f3a;">'
        '<div style="font-family:Arial,Helvetica,sans-serif;color:#ffffff;font-size:20px;font-weight:800;letter-spacing:0.02em;">Talendus</div>'
        '<div style="font-family:Arial,Helvetica,sans-serif;color:#c5d0de;font-size:12px;padding-top:4px;">Cabinet de recrutement au Québec</div>'
        "</td></tr>"
        f'<tr><td style="padding:28px 28px 10px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#1a2332;">{inner}</td></tr>'
        '<tr><td style="padding:4px 16px 22px;">'
        f'<img src="cid:{SIGNATURE_CID}" width="600" alt="Talendus — Votre partenaire stratégique en recrutement au Québec. info@talendus.ca · 263 558 5225 · talendus.ca" style="display:block;width:100%;max-width:600px;height:auto;border:0;">'
        "</td></tr></table></td></tr></table></body></html>"
    )


def _attach_files(msg: EmailMessage, attachments: list[EmailAttachment] | None) -> None:
    for att in attachments or []:
        raw = att.mime or "application/octet-stream"
        main, _, sub = raw.partition("/")
        msg.add_attachment(
            att.data,
            maintype=main or "application",
            subtype=sub or "octet-stream",
            filename=att.filename,
        )


def build_email_message(
    cfg: SmtpRuntime,
    to_email: str,
    subject: str,
    body: str,
    attachments: list[EmailAttachment] | None = None,
) -> EmailMessage:
    plain = signed_plain(body)
    msg = EmailMessage()
    msg["From"] = cfg.from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    if cfg.reply_to:
        msg["Reply-To"] = cfg.reply_to
    msg.set_content(plain, charset="utf-8")
    msg.add_alternative(signed_html(body), subtype="html", charset="utf-8")
    image = SIGNATURE_IMAGE.read_bytes() if SIGNATURE_IMAGE.is_file() else b""
    if image:
        for part in msg.iter_parts():
            if part.get_content_type() == "text/html":
                part.add_related(
                    image,
                    maintype="image",
                    subtype="jpeg",
                    cid=SIGNATURE_CID,
                    filename="talendus-signature.jpg",
                )
                for child in part.iter_parts():
                    if child.get_content_type() != "image/jpeg":
                        continue
                    child.replace_header("Content-ID", f"<{SIGNATURE_CID}>")
                    child.replace_header(
                        "Content-Disposition",
                        'inline; filename="talendus-signature.jpg"',
                    )
                break
    _attach_files(msg, attachments)
    return msg


def _smtp_send(
    cfg: SmtpRuntime,
    to_email: str,
    subject: str,
    body: str,
    attachments: list[EmailAttachment] | None = None,
) -> None:
    msg = build_email_message(cfg, to_email, subject, body, attachments)
    with smtplib.SMTP(cfg.host, cfg.port, timeout=15) as smtp:
        if cfg.use_tls:
            smtp.starttls()
        if cfg.username:
            smtp.login(cfg.username, cfg.password)
        smtp.send_message(msg)


def _record_smtp_result(
    log: EmailLog,
    cfg: SmtpRuntime,
    *,
    fail_fast: bool = False,
    attachments: list[EmailAttachment] | None = None,
) -> None:
    try:
        _smtp_send(cfg, log.to_email, log.subject, log.body or "", attachments)
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
    body = signed_plain(body)
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


def send_composed_email(
    db: Session,
    to_email: str,
    subject: str,
    body: str,
    *,
    email_type: EmailType = EmailType.ADMIN,
    sync: bool = True,
    attachments: list[EmailAttachment] | None = None,
) -> EmailLog:
    body = signed_plain(body)
    log = EmailLog(
        to_email=to_email,
        type=email_type,
        subject=(subject or "Talendus")[:180],
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
        logger.info("email[composed] to=%s subject=%s", to_email, subject)
        return log
    if attachments and not sync:
        sync = True
    if sync:
        _record_smtp_result(log, cfg, fail_fast=True, attachments=attachments)
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
