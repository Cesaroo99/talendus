import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Notification, User, UserPreference
from app.models.enums import NotificationType, UserRole, utcnow

logger = logging.getLogger("talendus.notify")

_APPLICATION_TYPES = {
    NotificationType.APPLICATION_NEW,
    NotificationType.APPLICATION_STATUS,
    NotificationType.APPLICATION_ACCEPTED,
    NotificationType.APPLICATION_REJECTED,
}

_CANDIDATE_ROUTES = {
    "applications": "apps",
    "apps": "apps",
    "application": "application",
    "interviews": "interviews",
    "messages": "messages",
    "jobs": "jobs",
    "dashboard": "dashboard",
    "documents": "documents",
    "notifs": "notifs",
}
_EMPLOYER_ROUTES = {
    "applications": "inbox",
    "inbox": "inbox",
    "interviews": "interviews",
    "messages": "messages",
    "invoices": "invoices",
    "pipeline": "pipeline",
    "jobs": "jobs",
    "dashboard": "dashboard",
    "documents": "documents",
    "notifs": "notifs",
    "contracts": "contracts",
}


def portal_href(user: User | None, section: str, item_id: str | None = None) -> str:
    """Lien de notification vers le bon portail (candidat, employeur ou admin)."""
    role = user.role if user else UserRole.CANDIDATE
    item = f"/{item_id}" if item_id else ""
    if role == UserRole.CANDIDATE:
        name = _CANDIDATE_ROUTES.get(section, section)
        if section in {"applications", "apps", "application"} and item_id:
            name = "application"
        return f"/espace.html#/{name}{item}"
    if role == UserRole.EMPLOYER:
        name = _EMPLOYER_ROUTES.get(section, section)
        return f"/espace-employeur.html#/{name}{item}"
    if section in {"jobs", "job"}:
        return f"/admin/#/jobs{item}"
    return f"/admin/#/{section}{item}"


def _pref_allows(db: Session, user: User, ntype: NotificationType) -> bool:
    pref = user.preferences
    if pref is None:
        pref = db.scalar(select(UserPreference).where(UserPreference.user_id == user.id))
    if pref is None:
        return True
    if not pref.notify_in_app:
        return False
    if ntype is NotificationType.JOB_MATCH and not pref.notify_match:
        return False
    if ntype in _APPLICATION_TYPES and not pref.notify_application:
        return False
    if ntype is NotificationType.MESSAGE and not pref.notify_message:
        return False
    if ntype is NotificationType.INTERVIEW_INVITE and not pref.notify_interview:
        return False
    return True


def notify(
    db: Session,
    user: User | None,
    ntype: NotificationType,
    title: str,
    message: str,
    href: str | None = None,
) -> Notification | None:
    if not user:
        return None
    if not _pref_allows(db, user, ntype):
        logger.info("notify skipped prefs user=%s type=%s", user.id, ntype)
        return None
    row = Notification(user_id=user.id, type=ntype, title=title, message=message, href=href)
    db.add(row)
    logger.info("notify user=%s type=%s", user.id, ntype)
    _queue_external_channels(db, user, ntype, title, message, href)
    return row


def _queue_external_channels(
    db: Session,
    user: User,
    ntype: NotificationType,
    title: str,
    message: str,
    href: str | None = None,
) -> None:
    """E-mail (déjà envoyé ailleurs), SMS/WhatsApp (journalisés) et Web Push."""
    pref = user.preferences
    if pref is not None:
        if pref.notify_sms:
            logger.info("notify channel=sms queued user=%s type=%s", user.id, ntype)
        if pref.notify_whatsapp:
            logger.info("notify channel=whatsapp queued user=%s type=%s", user.id, ntype)
    try:
        from app.services import push as push_service

        sent = push_service.send_to_user(db, user, title, message, href)
        if sent:
            logger.info("notify channel=push sent=%s user=%s type=%s", sent, user.id, ntype)
    except Exception as exc:
        logger.info("notify channel=push failed user=%s type=%s err=%s", user.id, ntype, exc)


def serialize_notification(row: Notification) -> dict:
    return {
        "id": row.id,
        "type": row.type.value,
        "title": row.title,
        "message": row.message,
        "href": row.href,
        "channel": row.channel.value if getattr(row, "channel", None) else "in_app",
        "is_read": row.is_read,
        "read_at": row.read_at.isoformat() if row.read_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def list_for_user(db: Session, user: User, unread_only: bool = False) -> list[Notification]:
    stmt = select(Notification).where(Notification.user_id == user.id)
    if unread_only:
        stmt = stmt.where(Notification.is_read.is_(False))
    return list(db.scalars(stmt.order_by(Notification.created_at.desc())).all())


def mark_read(db: Session, user: User, notification_id: str) -> Notification:
    from app.errors import AppError

    row = db.get(Notification, notification_id)
    if not row or row.user_id != user.id:
        raise AppError(404, "Notification introuvable.", "NOTIFICATION_NOT_FOUND")
    row.is_read = True
    row.read_at = utcnow()
    db.commit()
    db.refresh(row)
    return row


def mark_all_read(db: Session, user: User) -> int:
    rows = list_for_user(db, user, unread_only=True)
    for row in rows:
        row.is_read = True
        row.read_at = utcnow()
    db.commit()
    return len(rows)
