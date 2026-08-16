import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Notification, User
from app.models.enums import NotificationType, utcnow

logger = logging.getLogger("talendus.notify")


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
    row = Notification(user_id=user.id, type=ntype, title=title, message=message, href=href)
    db.add(row)
    logger.info("notify user=%s type=%s", user.id, ntype)
    return row


def serialize_notification(row: Notification) -> dict:
    return {
        "id": row.id,
        "type": row.type.value,
        "title": row.title,
        "message": row.message,
        "href": row.href,
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
