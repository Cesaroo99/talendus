from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import ApplicationStatus, UserRole
from app.schemas import ApplicationCreateIn, PublicApplyIn, StatusChangeIn
from app.services import applications as applications_service

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("")
def apply(
    payload: ApplicationCreateIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    application = applications_service.apply(db, user, payload, client_ip(request))
    return ok(applications_service.serialize_application(application, user))


@router.post("/public")
def apply_public(payload: PublicApplyIn, request: Request, db: Session = Depends(get_db)):
    application = applications_service.apply_public(db, payload, client_ip(request))
    return ok(applications_service.serialize_application(application, None), message="Candidature envoyée.")


@router.get("/me")
def my_applications(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok([applications_service.serialize_application(item, user) for item in applications_service.list_own(db, user)])


@router.get("")
def list_applications(
    job_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(
        [applications_service.serialize_application(item, user) for item in applications_service.list_inbox(db, user, job_id)]
    )


@router.get("/{application_id}")
def get_application(
    application_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = applications_service.get_application(db, user, application_id)
    return ok(applications_service.serialize_application(application, user))


@router.post("/{application_id}/status")
def change_status(
    application_id: str,
    payload: StatusChangeIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    application = applications_service.change_status(db, user, application_id, payload.status, payload.comment)
    return ok(applications_service.serialize_application(application, user))


@router.post("/{application_id}/withdraw")
def withdraw(
    application_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    application = applications_service.change_status(
        db, user, application_id, ApplicationStatus.WITHDRAWN, "Retrait par le candidat"
    )
    return ok(applications_service.serialize_application(application, user))
