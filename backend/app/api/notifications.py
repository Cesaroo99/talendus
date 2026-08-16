from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.services import notifications as notif_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(
    unread: bool = Query(default=False),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = notif_service.list_for_user(db, user, unread_only=unread)
    return ok(
        [notif_service.serialize_notification(row) for row in rows],
        meta={"unread": len(notif_service.list_for_user(db, user, unread_only=True))},
    )


@router.get("/unread")
def unread_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = notif_service.list_for_user(db, user, unread_only=True)
    return ok([notif_service.serialize_notification(row) for row in rows], meta={"count": len(rows)})


@router.post("/{notification_id}/read")
def mark_read(
    notification_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = notif_service.mark_read(db, user, notification_id)
    return ok(notif_service.serialize_notification(row))


@router.post("/read-all")
def mark_all_read(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count = notif_service.mark_all_read(db, user)
    return ok({"updated": count})
