from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import CompanyIn, RecruiterInviteIn
from app.services import companies as companies_service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("")
def create_company(
    payload: CompanyIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.ADMIN)),
):
    company = companies_service.create_company(db, user, payload)
    return ok(companies_service.serialize_company(company))


@router.get("")
def list_companies(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok([companies_service.serialize_company(c) for c in companies_service.list_companies(db, user)])


@router.get("/me")
def my_company(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    company = companies_service.company_for_employer(db, user)
    return ok(companies_service.serialize_company(company))


@router.get("/{company_id}")
def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.errors import AppError
    from app.models import Company

    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and company.owner_user_id != user.id:
        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    if user.role not in {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN}:
        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    return ok(companies_service.serialize_company(company))


@router.patch("/{company_id}")
def update_company(
    company_id: str,
    payload: CompanyIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = companies_service.update_company(db, user, company_id, payload)
    return ok(companies_service.serialize_company(company))


@router.post("/{company_id}/recruiters")
def invite_recruiter(
    company_id: str,
    payload: RecruiterInviteIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.ADMIN)),
):
    from app.errors import AppError
    from app.models import Company

    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and company.owner_user_id != user.id:
        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    recruiter = companies_service.invite_recruiter(db, user, payload)
    return ok({"id": recruiter.id, "user_id": recruiter.user_id})
