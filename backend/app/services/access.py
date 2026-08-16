from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company, CompanyMembership, User
from app.models.enums import CompanyMemberRole, UserRole
from app.rbac import ADMINS, company_can, is_admin


RECRUITER_STAFF = {UserRole.RECRUITER} | ADMINS
FINANCE_STAFF = {UserRole.FINANCE} | ADMINS
CONTRACT_STAFF = {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS
MESSAGE_STAFF = {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS


def company_ids_for_employer(db: Session, user: User) -> list[str]:
    owned = list(db.scalars(select(Company.id).where(Company.owner_user_id == user.id)).all())
    member = list(db.scalars(select(CompanyMembership.company_id).where(CompanyMembership.user_id == user.id)).all())
    return list({*owned, *member})


def first_employer_company(db: Session, user: User) -> Company | None:
    owned = db.scalar(select(Company).where(Company.owner_user_id == user.id))
    if owned:
        return owned
    membership = db.scalar(
        select(CompanyMembership).where(CompanyMembership.user_id == user.id).order_by(CompanyMembership.created_at.asc())
    )
    if not membership:
        return None
    return db.get(Company, membership.company_id)


def user_belongs_to_company(db: Session, user: User, company_id: str) -> bool:
    if is_admin(user) or user.role == UserRole.RECRUITER:
        return True
    return company_id in company_ids_for_employer(db, user)


def membership_for(db: Session, user: User, company_id: str) -> CompanyMembership | None:
    return db.scalar(
        select(CompanyMembership).where(
            CompanyMembership.user_id == user.id,
            CompanyMembership.company_id == company_id,
        )
    )


def member_role_for(db: Session, user: User, company_id: str) -> CompanyMemberRole | None:
    if is_admin(user):
        return CompanyMemberRole.OWNER
    company = db.get(Company, company_id)
    if company and company.owner_user_id == user.id:
        return CompanyMemberRole.OWNER
    membership = membership_for(db, user, company_id)
    return membership.member_role if membership else None


def require_company_perm(db: Session, user: User, company_id: str, permission: str) -> Company:
    if is_admin(user) or user.role == UserRole.RECRUITER:
        company = db.get(Company, company_id)
        if not company:
            from app.errors import AppError

            raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
        return company
    if user.role != UserRole.EMPLOYER:
        from app.errors import AppError

        raise AppError(403, "Accès refusé à cette entreprise.", "FORBIDDEN")
    role = member_role_for(db, user, company_id)
    if not company_can(role, permission):
        from app.errors import AppError

        raise AppError(403, "Permission insuffisante pour cette action.", "FORBIDDEN")
    company = db.get(Company, company_id)
    if not company:
        from app.errors import AppError

        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    return company
