from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import AppError, ok
from app.models import Recruiter, User
from app.models.enums import UserRole
from app.schemas import MissionIn, NoteIn
from app.services import companies as companies_service

router = APIRouter(prefix="/recruiters", tags=["recruiters"])


@router.get("/me")
def my_recruiter_profile(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    recruiter = db.scalar(select(Recruiter).where(Recruiter.user_id == user.id))
    if recruiter is None and user.role != UserRole.ADMIN:
        raise AppError(404, "Profil recruteur introuvable.", "RECRUITER_NOT_FOUND")
    return ok(
        {
            "id": recruiter.id if recruiter else None,
            "specialty": recruiter.specialty if recruiter else None,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "title": user.title,
        }
    )


@router.get("/missions")
def list_missions(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.EMPLOYER)),
):
    return ok([companies_service.serialize_mission(m) for m in companies_service.list_missions(db, user)])


@router.post("/missions")
def create_mission(
    payload: MissionIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.EMPLOYER)),
):
    mission = companies_service.create_mission(db, user, payload)
    return ok(companies_service.serialize_mission(mission))


@router.post("/notes")
def add_note(
    payload: NoteIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    note = companies_service.add_note(db, user, payload)
    return ok(
        {
            "id": note.id,
            "entity_type": note.entity_type,
            "entity_id": note.entity_id,
            "text": note.text,
            "created_at": note.created_at.isoformat() if note.created_at else None,
        }
    )
