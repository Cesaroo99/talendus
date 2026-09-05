from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Company, CompanyMembership, InternalNote, Recruiter, RecruitmentMission, User
from app.models.enums import CompanyMemberRole, UserRole
from app.rbac import ADMINS, is_admin
from app.schemas import CompanyIn, NoteIn
from app.services.access import (
    company_ids_for_employer,
    first_employer_company,
    recruiter_can_access_company,
    user_belongs_to_company,
)
from app.services.audit import audit


def create_company(db: Session, user: User, data: CompanyIn) -> Company:
    if user.role == UserRole.EMPLOYER:
        existing = first_employer_company(db, user)
        if existing:
            return update_company(db, user, existing.id, data)
        from app.services.employer_claim import find_unclaimed_employer_company, claim_employer_company

        claimed = find_unclaimed_employer_company(
            db,
            email=user.email,
            company_name=data.name or "",
        )
        if claimed:
            claim_employer_company(db, user, claimed)
            return update_company(db, user, claimed.id, data)
    payload = data.model_dump()
    company = Company(
        name=payload["name"],
        legal_name=payload.get("legal_name"),
        trade_name=payload.get("trade_name"),
        description=payload.get("description"),
        sector=payload.get("sector"),
        city=payload.get("city"),
        address=payload.get("address"),
        province=payload.get("province") or "Québec",
        country=payload.get("country") or "Canada",
        contact_name=payload.get("contact_name") or user.full_name,
        email=str(payload["email"]) if payload.get("email") else user.email,
        phone=payload.get("phone"),
        website=payload.get("website"),
        linkedin_url=payload.get("linkedin_url"),
        facebook_url=payload.get("facebook_url"),
        employees=payload.get("employees"),
        size_label=payload.get("size_label"),
        owner_user_id=user.id if user.role == UserRole.EMPLOYER else None,
    )
    db.add(company)
    db.flush()
    if user.role == UserRole.EMPLOYER:
        db.add(CompanyMembership(company_id=company.id, user_id=user.id, member_role=CompanyMemberRole.OWNER))
    audit(db, "company.create", user, "company", company.id)
    from app.integrations.hooks import apply_coordinates, company_address, maybe_geocode

    apply_coordinates(
        company,
        maybe_geocode(company_address(company.address, company.city, company.province, company.country)),
    )
    db.commit()
    db.refresh(company)
    return company


def list_companies(db: Session, user: User) -> list[Company]:
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        return list(db.scalars(select(Company).where(Company.id.in_(ids)).order_by(Company.name.asc())).all())
    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Permission insuffisante.", "FORBIDDEN")
    rows = list(db.scalars(select(Company).order_by(Company.name.asc())).all())
    if user.role == UserRole.RECRUITER:
        return [row for row in rows if recruiter_can_access_company(db, user, row)]
    return rows


def invite_recruiter(db: Session, user: User, data) -> Recruiter:
    from app.models import Recruiter, UserPreference
    from app.security import hash_password, random_password

    existing = db.scalar(select(User).where(User.email == data.email.lower()))
    if existing:
        raise AppError(409, "Un compte existe déjà avec ce courriel.", "EMAIL_TAKEN")
    password = data.password or random_password()
    recruiter_user = User(
        email=data.email.lower(),
        password_hash=hash_password(password),
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        role=UserRole.RECRUITER,
        title=data.title,
    )
    db.add(recruiter_user)
    db.flush()
    db.add(UserPreference(user_id=recruiter_user.id))
    recruiter = Recruiter(user_id=recruiter_user.id, specialty=data.specialty)
    db.add(recruiter)
    audit(db, "recruiter.invite", user, "user", recruiter_user.id)
    db.commit()
    db.refresh(recruiter)
    return recruiter


def create_mission(db: Session, user: User, data) -> RecruitmentMission:
    if user.role not in {UserRole.RECRUITER, UserRole.EMPLOYER} | ADMINS:
        raise AppError(403, "Permission insuffisante.", "FORBIDDEN")
    company = db.get(Company, data.company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, company.id):
        raise AppError(403, "Vous n'avez pas accès à cette entreprise.", "FORBIDDEN")
    if user.role == UserRole.RECRUITER and not recruiter_can_access_company(db, user, company):
        raise AppError(403, "Cette fiche est assignée à un autre recruteur.", "FORBIDDEN")
    mission = RecruitmentMission(
        company_id=data.company_id,
        job_id=data.job_id,
        recruiter_id=data.recruiter_id,
        title=data.title,
        seats=data.seats,
        value=data.value,
        commission=data.commission,
        start_date=data.start_date,
        due_date=data.due_date,
    )
    db.add(mission)
    db.flush()
    audit(db, "mission.create", user, "mission", mission.id)
    db.commit()
    db.refresh(mission)
    return mission


def list_missions(db: Session, user: User) -> list[RecruitmentMission]:
    stmt = select(RecruitmentMission)
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(RecruitmentMission.company_id.in_(ids))
    elif user.role == UserRole.RECRUITER:
        stmt = stmt.where(RecruitmentMission.recruiter_id == user.id)
    elif not is_admin(user):
        raise AppError(403, "Permission insuffisante.", "FORBIDDEN")
    return list(db.scalars(stmt.order_by(RecruitmentMission.created_at.desc())).all())


def company_for_employer(db: Session, user: User) -> Company:
    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    return company


def update_company(db: Session, user: User, company_id: str, data: CompanyIn) -> Company:
    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, company.id):
        raise AppError(403, "Vous n'avez pas accès à cette entreprise.", "FORBIDDEN")
    if user.role not in {UserRole.EMPLOYER, UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Permission insuffisante.", "FORBIDDEN")
    if user.role == UserRole.RECRUITER and not recruiter_can_access_company(db, user, company):
        raise AppError(403, "Cette fiche est assignée à un autre recruteur.", "FORBIDDEN")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)
    from app.integrations.hooks import apply_coordinates, company_address, maybe_geocode

    apply_coordinates(
        company,
        maybe_geocode(company_address(company.address, company.city, company.province, company.country)),
    )
    audit(db, "company.update", user, "company", company.id)
    db.commit()
    db.refresh(company)
    return company


def add_note(db: Session, user: User, data: NoteIn) -> InternalNote:
    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Seuls les recruteurs peuvent ajouter une note interne.", "FORBIDDEN")
    note = InternalNote(
        entity_type=data.entity_type,
        entity_id=data.entity_id,
        author_id=user.id,
        text=data.text,
    )
    db.add(note)
    audit(db, "note.create", user, data.entity_type, data.entity_id)
    db.commit()
    db.refresh(note)
    return note


def serialize_company(c: Company) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "legal_name": c.legal_name,
        "trade_name": c.trade_name,
        "description": c.description,
        "sector": c.sector,
        "city": c.city,
        "address": c.address,
        "province": c.province,
        "country": c.country,
        "lat": c.lat,
        "lng": c.lng,
        "place_id": c.place_id,
        "contact_name": c.contact_name,
        "email": c.email,
        "phone": c.phone,
        "website": c.website,
        "linkedin_url": c.linkedin_url,
        "facebook_url": c.facebook_url,
        "employees": c.employees,
        "size_label": c.size_label,
        "status": c.status.value if c.status else None,
        "logo_path": c.logo_path,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


def serialize_mission(m: RecruitmentMission) -> dict:
    linked = m.linked_jobs
    if not linked:
        job_ids: list[str] = []
    elif hasattr(linked, "id") and not isinstance(linked, (list, tuple)):
        job_ids = [linked.id]
    else:
        try:
            job_ids = [j.id for j in linked]
        except TypeError:
            job_ids = []
    return {
        "id": m.id,
        "title": m.title,
        "company_id": m.company_id,
        "job_id": m.job_id,
        "recruiter_id": m.recruiter_id,
        "seats": m.seats,
        "status": m.status.value,
        "progress": m.progress,
        "value": m.value,
        "commission": m.commission,
        "start_date": m.start_date,
        "due_date": m.due_date,
        "notes": m.notes,
        "job_ids": job_ids,
    }
