from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import HiringRequestFeedbackIn, HiringRequestIn, HiringRequestPatchIn, HiringRequestStatusIn
from app.services import hiring_requests as svc

router = APIRouter(prefix="/hiring-requests", tags=["hiring-requests"])


@router.get("")
def list_hiring_requests(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok([svc.serialize_request(row) for row in svc.list_requests(db, user)])


@router.post("")
def create_hiring_request(
    payload: HiringRequestIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    row = svc.create_request(db, user, payload, client_ip(request))
    return ok(svc.serialize_request(row), message="Votre besoin a bien été transmis à Talendus.")


@router.get("/{request_id}")
def get_hiring_request(
    request_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(svc.serialize_request(svc.get_request(db, user, request_id)))


@router.patch("/{request_id}")
def patch_hiring_request(
    request_id: str,
    payload: HiringRequestPatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(svc.serialize_request(svc.update_request(db, user, request_id, payload)))


@router.post("/{request_id}/status")
def set_hiring_request_status(
    request_id: str,
    payload: HiringRequestStatusIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(svc.serialize_request(svc.set_status(db, user, request_id, payload.status)))


@router.post("/{request_id}/feedback")
def hiring_request_feedback(
    request_id: str,
    payload: HiringRequestFeedbackIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    return ok(svc.serialize_request(svc.employer_feedback(db, user, request_id, payload.action, payload.comment)))


@router.post("/{request_id}/convert-to-job")
def convert_hiring_request(
    request_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(svc.serialize_request(svc.convert_to_job(db, user, request_id)))
