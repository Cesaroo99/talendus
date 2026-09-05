"""Envoi d'e-mails : journalisation persistée, worker qui relit la file en base."""

from __future__ import annotations

import html
import logging
import queue
import re
import secrets
import smtplib
import threading
import time
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import EmailLog
from app.models.enums import EmailStatus, EmailType, utcnow

logger = logging.getLogger("talendus.email")
SMTP_DISABLED_ERROR = "SMTP désactivé — le courriel n’a pas quitté le serveur."
FAKE_SENT_ERROR = "Jamais remis au serveur SMTP (journalisé seulement)."
PIXEL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
    b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)
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
    host = (stored.get("smtp.host") or "").strip() or env.email_server
    username = normalize_smtp_username(stored.get("smtp.username")) or (env.email_username or "").strip()
    from_addr = (
        (stored.get("smtp.from") or "").strip()
        or (env.email_from or "").strip()
        or "Talendus <info@talendus.ca>"
    )
    ready = _smtp_ready(host, username, password)
    if ready:
        enabled = False if (enabled_ov is False and env.app_env == "test") else True
    elif enabled_ov is None:
        enabled = bool(env.email_enabled)
    else:
        enabled = enabled_ov
    return SmtpRuntime(
        enabled=enabled,
        host=host,
        port=port,
        username=username,
        password=password,
        from_addr=from_addr,
        use_tls=env.email_use_tls if tls_ov is None else tls_ov,
        reply_to=(env.public_email or "info@talendus.ca").strip(),
    )


def _smtp_ready(host: str, username: str, password: str) -> bool:
    target = (host or "").strip().lower()
    if not target or target in {"localhost", "127.0.0.1", "::1"}:
        return False
    return bool((username or "").strip() and (password or "").strip())


def email_actually_sent(log: EmailLog | None) -> bool:
    if log is None:
        return False
    return log.status == EmailStatus.SENT and (log.attempts or 0) >= 1


def mark_smtp_disabled(log: EmailLog) -> EmailLog:
    log.status = EmailStatus.FAILED
    log.error = SMTP_DISABLED_ERROR
    log.sent_at = None
    return log


def delivery_error(log: EmailLog | None) -> str:
    if log is None:
        return SMTP_DISABLED_ERROR
    return (log.error or SMTP_DISABLED_ERROR).strip() or SMTP_DISABLED_ERROR


def new_tracking_token() -> str:
    return secrets.token_urlsafe(24)


def public_base_url() -> str:
    env = get_settings()
    return (env.frontend_url or env.render_external_url or "https://talendus.ca").rstrip("/")


def tracking_pixel_url(token: str) -> str:
    return f"{public_base_url()}/api/mail/o/{token}.gif"


def delivery_snapshot(log: EmailLog | None) -> dict:
    if log is None:
        return {
            "delivery": "unknown",
            "delivery_label": "Statut inconnu",
            "delivered": False,
            "opened": False,
            "opened_at": None,
            "open_count": 0,
            "sent_at": None,
            "email_error": "",
            "email_log_id": None,
            "email_status": None,
        }
    delivered = email_actually_sent(log)
    opened = bool(getattr(log, "opened_at", None))
    if delivered and opened:
        key, label = "opened", "Ouvert"
    elif delivered:
        key, label = "accepted", "Parti — accepté par le serveur"
    elif log.status == EmailStatus.QUEUED:
        key, label = "queued", "En file"
    elif never_handed_to_smtp(log):
        key, label = "failed", "Non parti — jamais remis au serveur"
    else:
        key, label = "failed", "Non parti — refusé par SMTP"
    return {
        "delivery": key,
        "delivery_label": label,
        "delivered": delivered,
        "opened": opened,
        "opened_at": log.opened_at.isoformat() if getattr(log, "opened_at", None) else None,
        "open_count": int(getattr(log, "open_count", 0) or 0),
        "sent_at": log.sent_at.isoformat() if log.sent_at else None,
        "email_error": log.error or "",
        "email_log_id": log.id,
        "email_status": log.status.value if log.status else "QUEUED",
    }


def serialize_email_log(log: EmailLog) -> dict:
    snap = delivery_snapshot(log)
    return {
        "id": log.id,
        "to_email": log.to_email,
        "type": log.type.value if log.type else None,
        "subject": log.subject,
        "body": log.body,
        "status": log.status.value if log.status else "QUEUED",
        "error": log.error,
        "attempts": log.attempts,
        "message_id": getattr(log, "message_id", None),
        "tracking_token": getattr(log, "tracking_token", None),
        "created_at": log.created_at.isoformat() if log.created_at else None,
        **snap,
    }


def record_email_open(db: Session, token: str) -> EmailLog | None:
    value = (token or "").strip().removesuffix(".gif")
    if len(value) < 8:
        return None
    log = db.scalar(select(EmailLog).where(EmailLog.tracking_token == value))
    if log is None:
        return None
    log.open_count = (log.open_count or 0) + 1
    if not log.opened_at:
        log.opened_at = utcnow()
    return log


def ensure_smtp_ready(db: Session) -> dict:
    """En production, active l’envoi dès que le serveur SMTP est renseigné."""
    from app.models import SystemSetting

    cfg = runtime_email_config(db)
    ready = _smtp_ready(cfg.host, cfg.username, cfg.password)
    env = get_settings()
    if ready and env.app_env != "test":
        row = db.scalar(select(SystemSetting).where(SystemSetting.key == "smtp.enabled"))
        if row is None:
            db.add(
                SystemSetting(
                    key="smtp.enabled",
                    value="oui",
                    label="Activer l’envoi SMTP (oui / non ; vide = oui si le serveur SMTP est configuré)",
                )
            )
        elif (row.value or "").strip().lower() != "oui":
            row.value = "oui"
        db.flush()
        cfg = runtime_email_config(db)
    elif not ready:
        logger.warning(
            "SMTP incomplet host=%s user=%s password=%s — les courriels ne partiront pas",
            cfg.host or "(vide)",
            cfg.username or "(vide)",
            "oui" if cfg.password else "non",
        )
    return {
        "enabled": cfg.enabled,
        "ready": ready,
        "host": cfg.host,
        "username": cfg.username,
        "has_password": bool(cfg.password),
    }


def never_handed_to_smtp(log: EmailLog | None) -> bool:
    if log is None or email_actually_sent(log):
        return False
    if (log.attempts or 0) == 0:
        return True
    err = log.error or ""
    return SMTP_DISABLED_ERROR in err or FAKE_SENT_ERROR in err or "journalisé seulement" in err


def is_hard_smtp_reject(error: str | None) -> bool:
    raw = (error or "").lower()
    return any(
        token in raw
        for token in (
            "5.1.1",
            "user unknown",
            "does not exist",
            "recipient address rejected",
            "mailbox unavailable",
            "550-5.1.1",
        )
    )


def retryable_undelivered_logs(db: Session, limit: int = 400) -> list[EmailLog]:
    rows = list(
        db.scalars(
            select(EmailLog)
            .where(EmailLog.type == EmailType.ADMIN, EmailLog.status != EmailStatus.SENT)
            .order_by(EmailLog.created_at.desc())
        ).all()
    )
    delivered_keys = {
        ((log.to_email or "").lower(), (log.subject or "")[:180])
        for log in db.scalars(select(EmailLog).where(EmailLog.status == EmailStatus.SENT)).all()
        if email_actually_sent(log)
    }
    picked: list[EmailLog] = []
    seen: set[tuple[str, str]] = set()
    for log in rows:
        if not never_handed_to_smtp(log):
            continue
        if is_hard_smtp_reject(log.error):
            continue
        key = ((log.to_email or "").lower(), (log.subject or "")[:180])
        if key in delivered_keys or key in seen:
            continue
        seen.add(key)
        picked.append(log)
        if len(picked) >= limit:
            break
    return picked


def touch_prospects_after_delivery(db: Session, log: EmailLog) -> int:
    if not email_actually_sent(log):
        return 0
    from app.models.prospect import Prospect

    rows = list(db.scalars(select(Prospect).where(Prospect.email == (log.to_email or "").lower())).all())
    changed = 0
    for row in rows:
        row.last_contacted_at = log.sent_at or utcnow()
        if row.stage in {"nouveau", "a-contacter"}:
            row.stage = "contacte"
            changed += 1
    return changed


def retry_undelivered_emails(db: Session, *, sync: bool = False, limit: int = 400) -> dict:
    mark_fake_sent_logs(db)
    smtp = ensure_smtp_ready(db)
    cfg = runtime_email_config(db)
    if not cfg.enabled:
        return {"retried": 0, "queued": 0, "sent": 0, "reason": "smtp_off", "smtp": smtp}
    logs = retryable_undelivered_logs(db, limit=limit)
    for log in logs:
        log.status = EmailStatus.QUEUED
        log.error = None
        if sync:
            _record_smtp_result(log, cfg, fail_fast=True)
            touch_prospects_after_delivery(db, log)
    if logs and not sync:
        start_worker()
    sent_now = sum(1 for log in logs if email_actually_sent(log))
    return {
        "retried": len(logs),
        "queued": 0 if sync else len(logs),
        "sent": sent_now,
        "reason": "ok" if logs else "none",
        "smtp": smtp,
    }


def email_delivery_summary(db: Session, limit: int = 200) -> dict:
    smtp = ensure_smtp_ready(db)
    rows = list(
        db.scalars(
            select(EmailLog).where(EmailLog.type == EmailType.ADMIN).order_by(EmailLog.created_at.desc()).limit(limit)
        ).all()
    )
    counts = {"accepted": 0, "opened": 0, "failed": 0, "queued": 0, "total": len(rows), "retryable": 0, "hard_failed": 0}
    for log in rows:
        key = delivery_snapshot(log)["delivery"]
        if key in counts:
            counts[key] += 1
        if never_handed_to_smtp(log):
            counts["retryable"] += 1
        elif key == "failed":
            counts["hard_failed"] += 1
    retryable_all = len(retryable_undelivered_logs(db))
    counts["retryable"] = retryable_all
    if not smtp.get("ready"):
        reason = "smtp_off"
        explanation = (
            "Ce n’est pas une limite Gmail ni un problème d’adresses. "
            "Ces courriels n’ont jamais été remis au serveur SMTP (envoi journalisé seulement)."
        )
    elif retryable_all:
        reason = "never_sent"
        explanation = (
            f"{retryable_all} courriels n’ont jamais quitté Talendus. "
            "Ce n’est pas une limitation obligatoire : ils vont être relancés maintenant que le SMTP est prêt."
        )
    else:
        reason = "ok"
        explanation = "Les courriels prospects ont quitté le serveur, ou aucun n’est en attente de relance."
    return {**counts, "reason": reason, "explanation": explanation, "smtp": smtp}


def enrich_audits_with_delivery(db: Session, rows: list[dict]) -> list[dict]:
    log_ids = []
    lookups: list[tuple[str, str]] = []
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        if meta.get("email_log_id"):
            log_ids.append(meta["email_log_id"])
        elif meta.get("to") and meta.get("subject"):
            lookups.append((str(meta["to"]).lower(), str(meta["subject"])[:180]))
    logs: dict[str, EmailLog] = {}
    if log_ids:
        for log in db.scalars(select(EmailLog).where(EmailLog.id.in_(log_ids))).all():
            logs[log.id] = log
    by_pair: dict[tuple[str, str], EmailLog] = {}
    if lookups:
        emails = {to for to, _ in lookups}
        for log in db.scalars(select(EmailLog).where(EmailLog.to_email.in_(emails)).order_by(EmailLog.created_at.desc())).all():
            pair = ((log.to_email or "").lower(), (log.subject or "")[:180])
            by_pair.setdefault(pair, log)
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        log = logs.get(meta.get("email_log_id")) if meta.get("email_log_id") else None
        if log is None and meta.get("to") and meta.get("subject"):
            log = by_pair.get((str(meta["to"]).lower(), str(meta["subject"])[:180]))
        if log is None and row.get("action") != "prospect.send":
            continue
        snap = delivery_snapshot(log)
        row["delivery"] = snap
        if isinstance(row.get("metadata"), dict):
            row["metadata"] = {**row["metadata"], **snap}
    return rows


def mark_fake_sent_logs(db: Session) -> int:
    rows = list(db.scalars(select(EmailLog).where(EmailLog.status == EmailStatus.SENT)).all())
    changed = 0
    for log in rows:
        if (log.attempts or 0) >= 1:
            continue
        log.status = EmailStatus.FAILED
        log.error = (log.error or FAKE_SENT_ERROR)[:2000]
        log.sent_at = None
        changed += 1
    return changed


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
        low = block.lower()
        is_attach = low.startswith("pièce jointe") or "trouverez ceci en pièce jointe" in low
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


def signed_html(body: str, tracking_url: str | None = None) -> str:
    core = strip_legacy_footer(body)
    inner = _text_to_html_blocks(core)
    pixel = ""
    if tracking_url:
        pixel = (
            f'<img src="{html.escape(tracking_url)}" width="1" height="1" alt="" '
            'style="display:block;width:1px;height:1px;border:0;opacity:0;">'
        )
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
        f"{pixel}</td></tr></table></td></tr></table></body></html>"
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
    tracking_url: str | None = None,
    message_id: str | None = None,
) -> EmailMessage:
    plain = signed_plain(body)
    msg = EmailMessage()
    msg["From"] = cfg.from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    if message_id:
        msg["Message-ID"] = message_id
    if cfg.reply_to:
        msg["Reply-To"] = cfg.reply_to
    msg.set_content(plain, charset="utf-8")
    msg.add_alternative(signed_html(body, tracking_url=tracking_url), subtype="html", charset="utf-8")
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
    tracking_url: str | None = None,
    message_id: str | None = None,
) -> str:
    msg = build_email_message(
        cfg,
        to_email,
        subject,
        body,
        attachments,
        tracking_url=tracking_url,
        message_id=message_id,
    )
    with smtplib.SMTP(cfg.host, cfg.port, timeout=20) as smtp:
        if cfg.use_tls:
            smtp.starttls()
        if cfg.username:
            smtp.login(cfg.username, cfg.password)
        refused = smtp.send_message(msg)
        if refused:
            raise RuntimeError(f"SMTP a refusé le destinataire : {refused}")
    return str(msg["Message-ID"] or message_id or "")


def _record_smtp_result(
    log: EmailLog,
    cfg: SmtpRuntime,
    *,
    fail_fast: bool = False,
    attachments: list[EmailAttachment] | None = None,
) -> None:
    try:
        token = getattr(log, "tracking_token", None) or ""
        mid = _smtp_send(
            cfg,
            log.to_email,
            log.subject,
            log.body or "",
            attachments,
            tracking_url=tracking_pixel_url(token) if token else None,
            message_id=getattr(log, "message_id", None),
        )
        log.status = EmailStatus.SENT
        log.error = None
        log.sent_at = utcnow()
        log.attempts = (log.attempts or 0) + 1
        if mid:
            log.message_id = mid
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
        tracking_token=new_tracking_token(),
        message_id=make_msgid(domain="talendus.ca"),
    )
    db.add(log)
    db.flush()
    cfg = runtime_email_config(db)
    if not cfg.enabled:
        mark_smtp_disabled(log)
        logger.warning("email[disabled] to=%s type=%s subject=%s", to_email, email_type, subject)
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
        tracking_token=new_tracking_token(),
        message_id=make_msgid(domain="talendus.ca"),
    )
    db.add(log)
    db.flush()
    cfg = runtime_email_config(db)
    if not cfg.enabled:
        mark_smtp_disabled(log)
        logger.warning("email[composed-disabled] to=%s subject=%s", to_email, subject)
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
    if get_settings().app_env == "test":
        return
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
            if email_actually_sent(log):
                return
            cfg = runtime_email_config(db)
            if not cfg.enabled:
                mark_smtp_disabled(log)
                db.commit()
                return
            _record_smtp_result(log, cfg, fail_fast=False)
            if email_actually_sent(log):
                touch_prospects_after_delivery(db, log)
            db.commit()
            time.sleep(0.35)
            return
        finally:
            db.close()
    logger.warning("email log %s introuvable après retries", log_id)
