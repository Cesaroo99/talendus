from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.services import calls as calls_service

router = APIRouter(prefix="/calls", tags=["calls"])


class CallJoinIn(BaseModel):
    video: bool | None = None


class CallSignalIn(BaseModel):
    kind: str = Field(min_length=2, max_length=16)
    payload: dict = Field(default_factory=dict)


@router.get("/{interview_id}/lobby")
def call_lobby(
    interview_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(calls_service.lobby(db, user, interview_id))


@router.post("/{interview_id}/open")
def open_call(
    interview_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(calls_service.open_room(db, user, interview_id), message="Salle d’appel ouverte.")


@router.post("/{interview_id}/join")
def join_call(
    interview_id: str,
    payload: CallJoinIn | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    video = payload.video if payload else None
    return ok(calls_service.join(db, user, interview_id, video))


@router.get("/{interview_id}/signals")
def list_signals(
    interview_id: str,
    after: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(calls_service.list_signals(db, user, interview_id, after))


@router.post("/{interview_id}/signal")
def post_signal(
    interview_id: str,
    payload: CallSignalIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(calls_service.post_signal(db, user, interview_id, payload.kind, payload.payload))


@router.post("/{interview_id}/hangup")
def hangup_call(
    interview_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(calls_service.hangup(db, user, interview_id))
