from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user
from app.errors import ok
from app.models import User
from app.schemas import MessageIn
from app.services import messages as messages_service

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("")
def threads(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(messages_service.list_threads(db, user))


@router.get("/directory")
def directory(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(messages_service.directory(db, user))


@router.get("/{user_id}")
def conversation(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = messages_service.list_conversation(db, user, user_id)
    return ok([messages_service.serialize_message(row) for row in rows])


@router.post("")
def send(payload: MessageIn, request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = messages_service.send_message(db, user, payload.recipient_id, payload.body, payload.application_id, client_ip(request))
    return ok(messages_service.serialize_message(row), message="Message envoyé.")
