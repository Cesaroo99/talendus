from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import AppError, ok
from app.models import Company, User
from app.models.enums import UserRole
from app.schemas import CompanyIn, CompanyMemberIn, CompanyMemberPatchIn, RecruiterInviteIn
from app.services import companies as companies_service
from app.services.access import user_belongs_to_company
from app.services.portal import (
    employer_dashboard,
    invite_member,
    list_members,
    patch_member,
    remove_member,
    set_company_logo,
)
from app.services.storage import open_stored

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("")
def create_company(
    payload: CompanyIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
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


@router.get("/me/dashboard")
def my_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    return ok(employer_dashboard(db, user))


@router.get("/me/members")
def my_members(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    return ok(list_members(db, user))


@router.post("/me/members")
def add_member(
    payload: CompanyMemberIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    return ok(invite_member(db, user, payload), message="Membre ajouté.")


@router.patch("/me/members/{membership_id}")
def update_member(
    membership_id: str,
    payload: CompanyMemberPatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    return ok(patch_member(db, user, membership_id, payload))


@router.delete("/me/members/{membership_id}")
def delete_member(
    membership_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    remove_member(db, user, membership_id)
    return ok(message="Membre retiré.")


@router.get("/{company_id}")
def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, company.id):
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
    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, company.id):
        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    recruiter = companies_service.invite_recruiter(db, user, payload)
    return ok({"id": recruiter.id, "user_id": recruiter.user_id})


@router.post("/{company_id}/logo")
async def upload_logo(
    company_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await file.read()
    company = set_company_logo(db, user, company_id, data, file.filename or "logo.png")
    return ok(companies_service.serialize_company(company), message="Logo enregistré.")


@router.get("/{company_id}/logo")
def company_logo(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = db.get(Company, company_id)
    if not company or not company.logo_path:
        raise AppError(404, "Logo introuvable.", "NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, company.id):
        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    url, path = open_stored(company.logo_path, None, "logos")
    if url:
        return RedirectResponse(url)
    return FileResponse(path, media_type="image/png")
