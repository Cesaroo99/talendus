from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company, CompanyMembership, User
from app.models.enums import UserRole
from app.rbac import ADMINS, is_admin


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
