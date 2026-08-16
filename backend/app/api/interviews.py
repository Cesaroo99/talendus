from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import InterviewIn, InterviewPatchIn, InterviewStatusIn
from app.services import interviews as interviews_service

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.get("")
def list_interviews(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok([interviews_service.serialize_interview(row) for row in interviews_service.list_interviews(db, user)])


@router.post("")
def create_interview(
    payload: InterviewIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    row = interviews_service.create_interview(db, user, payload, client_ip(request))
    return ok(interviews_service.serialize_interview(row), message="Entretien planifié.")


@router.post("/reminders")
def send_reminders(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
    hours: int = 24,
):
    return ok(interviews_service.dispatch_due_reminders(db, hours=hours), message="Rappels traités.")


@router.get("/{interview_id}")
def get_interview(interview_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(interviews_service.serialize_interview(interviews_service.get_interview(db, user, interview_id)))


@router.patch("/{interview_id}")
def patch_interview(
    interview_id: str,
    payload: InterviewPatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    row = interviews_service.patch_interview(db, user, interview_id, payload)
    return ok(interviews_service.serialize_interview(row))


@router.post("/{interview_id}/status")
def change_status(
    interview_id: str,
    payload: InterviewStatusIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = interviews_service.set_status(db, user, interview_id, payload.status)
    return ok(interviews_service.serialize_interview(row))
