from __future__ import annotations

import json
from datetime import timedelta

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Interview, User
from app.models.calls import CallPeer, CallSignal
from app.models.enums import InterviewStatus, InterviewType, NotificationType, utcnow
from app.services.interviews import (
    get_interview,
    is_staff,
    serialize_interview,
    viewer_can_join_call,
    viewer_can_start_call,
)
from app.services.notifications import notify, portal_href

CALL_TYPES = {
    InterviewType.TALENDUS,
    InterviewType.CLIENT,
    InterviewType.PHONE,
    InterviewType.VIDEO,
}
LIVE_STATUSES = {InterviewStatus.SCHEDULED, InterviewStatus.CONFIRMED}
PEER_TTL = timedelta(seconds=25)
KINDS = {"offer", "answer", "ice", "hangup"}
ICE_SERVERS = [
    {"urls": "stun:stun.l.google.com:19302"},
    {"urls": "stun:stun.cloudflare.com:3478"},
]


def can_join_call(row: Interview) -> bool:
    return row.type in CALL_TYPES and row.status in LIVE_STATUSES


def default_video(row: Interview) -> bool:
    return row.type != InterviewType.PHONE


def _prune_stale(db: Session, interview_id: str) -> None:
    cutoff = utcnow() - PEER_TTL
    stale = list(
        db.scalars(
            select(CallPeer).where(CallPeer.interview_id == interview_id, CallPeer.last_seen < cutoff)
        ).all()
    )
    for row in stale:
        db.delete(row)


def _delete_signals(db: Session, interview_id: str) -> None:
    for row in list(db.scalars(select(CallSignal).where(CallSignal.interview_id == interview_id)).all()):
        db.delete(row)


def _latest_signal(db: Session, interview_id: str) -> CallSignal | None:
    return db.scalar(
        select(CallSignal)
        .where(CallSignal.interview_id == interview_id)
        .order_by(CallSignal.created_at.desc(), CallSignal.id.desc())
    )


def _live_peers(db: Session, interview_id: str, *, exclude_user_id: str | None = None) -> list[CallPeer]:
    _prune_stale(db, interview_id)
    cutoff = utcnow() - PEER_TTL
    stmt = select(CallPeer).where(CallPeer.interview_id == interview_id, CallPeer.last_seen >= cutoff)
    if exclude_user_id:
        stmt = stmt.where(CallPeer.user_id != exclude_user_id)
    return list(db.scalars(stmt).all())


def _reset_idle_room(db: Session, interview_id: str) -> bool:
    """Vide offer/answer/ice/hangup dès qu’il n’y a plus personne dans la salle."""
    if _live_peers(db, interview_id):
        return False
    leftover = list(db.scalars(select(CallPeer).where(CallPeer.interview_id == interview_id)).all())
    for row in leftover:
        db.delete(row)
    _delete_signals(db, interview_id)
    return True


def _prepare_join_session(db: Session, interview_id: str, user_id: str, peer: CallPeer | None) -> None:
    """Nouveau participant : on jette la négociation précédente, pas celle en cours."""
    cutoff = utcnow() - PEER_TTL
    arriving = peer is None or peer.last_seen < cutoff
    if not arriving:
        return
    others = _live_peers(db, interview_id, exclude_user_id=user_id)
    if not others:
        _delete_signals(db, interview_id)
        return
    last = _latest_signal(db, interview_id)
    if last is None or last.kind == "hangup":
        _delete_signals(db, interview_id)
        return
    hangups = list(
        db.scalars(
            select(CallSignal).where(CallSignal.interview_id == interview_id, CallSignal.kind == "hangup")
        ).all()
    )
    for row in hangups:
        db.delete(row)


def _peers(db: Session, interview: Interview, viewer: User) -> list[dict]:
    _prune_stale(db, interview.id)
    cutoff = utcnow() - PEER_TTL
    rows = list(
        db.scalars(
            select(CallPeer).where(CallPeer.interview_id == interview.id, CallPeer.last_seen >= cutoff)
        ).all()
    )
    out = []
    for row in rows:
        user = db.get(User, row.user_id)
        if not user:
            continue
        out.append(
            {
                "user_id": row.user_id,
                "name": user.full_name,
                "video": row.video,
                "self": row.user_id == viewer.id,
            }
        )
    return out


def _serialize_signal(row: CallSignal) -> dict:
    try:
        payload = json.loads(row.payload or "{}")
    except json.JSONDecodeError:
        payload = {}
    return {
        "id": row.id,
        "kind": row.kind,
        "payload": payload,
        "sender_id": row.sender_id,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def _open_room(db: Session, interview: Interview, user: User, *, notify_candidate: bool) -> bool:
    if interview.call_opened_at:
        return False
    interview.call_opened_at = utcnow()
    if not notify_candidate:
        return True
    cand_user = interview.candidate.user if interview.candidate else None
    if cand_user and cand_user.id != user.id:
        notify(
            db,
            cand_user,
            NotificationType.INTERVIEW_INVITE,
            "L’appel est ouvert",
            "Le conseiller a ouvert la salle. Vous pouvez rejoindre l’entretien maintenant.",
            href=portal_href(cand_user, "interviews"),
        )
    return True


def lobby(db: Session, user: User, interview_id: str) -> dict:
    interview = get_interview(db, user, interview_id)
    return {
        "interview": serialize_interview(interview, user),
        "peers": _peers(db, interview, user),
        "self_id": user.id,
        "call_open": bool(interview.call_opened_at),
        "can_start": viewer_can_start_call(interview, user),
        "can_join": viewer_can_join_call(interview, user),
    }


def open_room(db: Session, user: User, interview_id: str) -> dict:
    interview = get_interview(db, user, interview_id)
    if not can_join_call(interview):
        raise AppError(409, "Cet entretien ne peut pas se faire en appel dans l'appli.", "CALL_NOT_AVAILABLE")
    if not is_staff(user) and not viewer_can_start_call(interview, user):
        raise AppError(403, "Vous ne pouvez pas ouvrir cet appel.", "CALL_CANNOT_START")
    _reset_idle_room(db, interview.id)
    _open_room(db, interview, user, notify_candidate=True)
    db.commit()
    return lobby(db, user, interview_id)


def join(db: Session, user: User, interview_id: str, video: bool | None = None) -> dict:
    interview = get_interview(db, user, interview_id)
    if not can_join_call(interview):
        raise AppError(409, "Cet entretien ne peut pas se faire en appel dans l'appli.", "CALL_NOT_AVAILABLE")
    if not viewer_can_join_call(interview, user) and not viewer_can_start_call(interview, user):
        raise AppError(
            409,
            "Le conseiller n’a pas encore ouvert l’appel. Vous pourrez rejoindre dès qu’il sera lancé.",
            "CALL_WAITING_FOR_HOST",
        )
    if is_staff(user) or viewer_can_start_call(interview, user):
        _open_room(db, interview, user, notify_candidate=is_staff(user))
    want_video = default_video(interview) if video is None else bool(video)
    peer = db.scalar(
        select(CallPeer).where(CallPeer.interview_id == interview.id, CallPeer.user_id == user.id)
    )
    _prepare_join_session(db, interview.id, user.id, peer)
    now = utcnow()
    if peer:
        peer.video = want_video
        peer.last_seen = now
    else:
        db.add(CallPeer(interview_id=interview.id, user_id=user.id, video=want_video, last_seen=now))
    db.commit()
    return {
        "interview": serialize_interview(interview, user),
        "video": want_video,
        "ice_servers": ICE_SERVERS,
        "self_id": user.id,
        "peers": _peers(db, interview, user),
        "in_app_call": True,
        "call_open": True,
        "can_start": viewer_can_start_call(interview, user),
        "can_join": True,
    }


def list_signals(db: Session, user: User, interview_id: str, after: str | None = None) -> dict:
    interview = get_interview(db, user, interview_id)
    peer = db.scalar(
        select(CallPeer).where(CallPeer.interview_id == interview.id, CallPeer.user_id == user.id)
    )
    if peer:
        peer.last_seen = utcnow()
        db.commit()
    stmt = select(CallSignal).where(
        CallSignal.interview_id == interview.id,
        CallSignal.sender_id != user.id,
    )
    if after:
        ref = db.get(CallSignal, after)
        if ref and ref.interview_id == interview.id:
            stmt = stmt.where(
                or_(
                    CallSignal.created_at > ref.created_at,
                    and_(CallSignal.created_at == ref.created_at, CallSignal.id > ref.id),
                )
            )
    rows = list(db.scalars(stmt.order_by(CallSignal.created_at.asc(), CallSignal.id.asc())).all())
    return {
        "signals": [_serialize_signal(row) for row in rows],
        "peers": _peers(db, interview, user),
        "self_id": user.id,
    }


def post_signal(db: Session, user: User, interview_id: str, kind: str, payload: dict | None) -> dict:
    interview = get_interview(db, user, interview_id)
    key = (kind or "").strip().lower()
    if key not in KINDS:
        raise AppError(400, "Type de signal d'appel invalide.", "INVALID_CALL_SIGNAL")
    body = payload if isinstance(payload, dict) else {}
    raw = json.dumps(body, ensure_ascii=False)
    if len(raw) > 20000:
        raise AppError(400, "Signal d'appel trop volumineux.", "CALL_SIGNAL_TOO_LARGE")
    row = CallSignal(interview_id=interview.id, sender_id=user.id, kind=key, payload=raw)
    db.add(row)
    db.flush()
    peer = db.scalar(
        select(CallPeer).where(CallPeer.interview_id == interview.id, CallPeer.user_id == user.id)
    )
    if peer:
        peer.last_seen = utcnow()
    if key == "hangup":
        if peer:
            db.delete(peer)
            db.flush()
        if not _live_peers(db, interview.id, exclude_user_id=user.id):
            _delete_signals(db, interview.id)
            leftover = list(db.scalars(select(CallPeer).where(CallPeer.interview_id == interview.id)).all())
            for leftover_peer in leftover:
                db.delete(leftover_peer)
            db.commit()
            return {"id": row.id, "kind": "hangup", "payload": {}, "sender_id": user.id, "created_at": None, "cleared": True}
    db.commit()
    db.refresh(row)
    return _serialize_signal(row)


def hangup(db: Session, user: User, interview_id: str) -> dict:
    return post_signal(db, user, interview_id, "hangup", {})
