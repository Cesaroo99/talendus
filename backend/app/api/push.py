from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.services import push as push_service

router = APIRouter(prefix="/push", tags=["push"])


class PushKeysIn(BaseModel):
    p256dh: str = Field(min_length=8, max_length=255)
    auth: str = Field(min_length=8, max_length=255)


class PushSubscribeIn(BaseModel):
    endpoint: str = Field(min_length=12, max_length=2000)
    keys: PushKeysIn


class PushUnsubscribeIn(BaseModel):
    endpoint: str = Field(min_length=12, max_length=2000)


@router.get("/vapid-public-key")
def vapid_public_key(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok({"public_key": push_service.public_key(db), "user_id": user.id})


@router.post("/subscribe")
def subscribe(
    payload: PushSubscribeIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = push_service.subscribe(
        db,
        user,
        payload.endpoint,
        payload.keys.p256dh,
        payload.keys.auth,
        request.headers.get("user-agent"),
    )
    return ok({"id": row.id, "endpoint": row.endpoint})


@router.delete("/subscribe")
def unsubscribe(
    payload: PushUnsubscribeIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    count = push_service.unsubscribe(db, user, payload.endpoint)
    return ok({"removed": count})
