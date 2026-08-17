from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import ApplicationStatus, UserRole
from app.schemas import ApplicationCreateIn, PublicApplyIn, StatusChangeIn
from app.services import applications as applications_service


def _form_text(form, key: str) -> str:
    value = form.get(key)
    if value is None or hasattr(value, "read"):
        return ""
    return str(value).strip()


def _public_payload(raw: dict) -> PublicApplyIn:
    try:
        return PublicApplyIn.model_validate(raw)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc

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
async def apply_public(request: Request, db: Session = Depends(get_db)):
    content_type = (request.headers.get("content-type") or "").lower()
    cv_file = None
    cv_filename = None
    if "multipart/form-data" in content_type:
        form = await request.form()
        payload = _public_payload(
            {
                "job_slug": _form_text(form, "job_slug"),
                "first_name": _form_text(form, "first_name"),
                "last_name": _form_text(form, "last_name"),
                "email": _form_text(form, "email"),
                "phone": _form_text(form, "phone") or None,
                "cover_note": _form_text(form, "cover_note") or None,
                "cv_url": _form_text(form, "cv_url") or None,
                "password": _form_text(form, "password") or None,
            }
        )
        upload = form.get("file") or form.get("cv") or form.get("cvfile")
        filename = getattr(upload, "filename", "") or ""
        if upload is not None and hasattr(upload, "read") and filename:
            data = await upload.read()
            if data:
                cv_file = data
                cv_filename = filename
    else:
        payload = _public_payload(await request.json())
    application = applications_service.apply_public(
        db, payload, client_ip(request), cv_file=cv_file, cv_filename=cv_filename
    )
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
