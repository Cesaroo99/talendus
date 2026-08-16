"""Demandes de recrutement (entreprise) distinctes des offres publiées par Talendus."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import RecruitmentMission, User
from app.models.enums import MissionStatus, NotificationType, UserRole, utcnow
from app.rbac import ADMINS, INTERNAL
from app.schemas import HiringRequestIn, HiringRequestPatchIn, JobIn
from app.services.access import company_ids_for_employer, first_employer_company, user_belongs_to_company
from app.services.audit import audit
from app.services.jobs import create_job
from app.services.notifications import notify, portal_href

STAFF_ROLES = INTERNAL | ADMINS

STATUS_COPY = {
    MissionStatus.REQUEST_SUBMITTED: (
        "Besoin transmis",
        "Votre besoin de recrutement a bien été transmis à Talendus. Notre équipe va maintenant l'étudier et reviendra vers vous pour approfondir votre recherche.",
    ),
    MissionStatus.UNDER_REVIEW: (
        "Analyse en cours",
        "Notre équipe analyse actuellement votre besoin afin de définir le profil recherché.",
    ),
    MissionStatus.CLIENT_CONTACTED: (
        "Échange avec Talendus",
        "Un conseiller Talendus vous contacte pour approfondir le contexte, les responsabilités et le type de candidat recherché.",
    ),
    MissionStatus.NEEDS_CONFIRMED: (
        "Profil défini",
        "Les critères de recherche ont été précisés avec vous. Talendus prépare ensuite l'offre et le sourcing.",
    ),
    MissionStatus.JOB_BEING_PREPARED: (
        "Offre en préparation",
        "Talendus rédige l'offre d'emploi à partir du brief. Vous pourrez valider les éléments avant publication.",
    ),
    MissionStatus.CLIENT_VALIDATION: (
        "Validation demandée",
        "Votre équipe peut maintenant consulter le brief préparé et nous transmettre ses retours.",
    ),
    MissionStatus.JOB_PUBLISHED: (
        "Recherche lancée",
        "Talendus recherche actuellement les profils correspondant à votre besoin.",
    ),
    MissionStatus.SOURCING: (
        "Recherche en cours",
        "Talendus recherche actuellement les profils correspondant à votre besoin.",
    ),
    MissionStatus.SCREENING: (
        "Présélection en cours",
        "Nous analysons et qualifions actuellement les candidats identifiés.",
    ),
    MissionStatus.INTERVIEWS: (
        "Entretiens Talendus",
        "Nous échangeons avec les candidats identifiés pour valider le parcours, les motivations et la disponibilité.",
    ),
    MissionStatus.SHORTLIST: (
        "Shortlist disponible",
        "Une sélection de profils pertinents est maintenant disponible.",
    ),
    MissionStatus.CLIENT_REVIEW: (
        "Profils à consulter",
        "Votre équipe peut maintenant consulter les profils présélectionnés et nous transmettre ses retours.",
    ),
    MissionStatus.HIRING: (
        "Décision en cours",
        "Vous étudiez les profils présentés. La décision finale vous appartient.",
    ),
    MissionStatus.CLOSED: (
        "Recrutement terminé",
        "Ce recrutement est clos. Vous pouvez transmettre un nouveau besoin à tout moment.",
    ),
}

EMPLOYER_VISIBLE = set(MissionStatus)


def serialize_request(row: RecruitmentMission) -> dict:
    title, message = STATUS_COPY.get(row.status, (row.status.value, ""))
    return {
        "id": row.id,
        "title": row.title,
        "seats": row.seats,
        "status": row.status.value,
        "status_label": title,
        "status_message": message,
        "location": row.location,
        "sector": row.sector,
        "contract_type": row.contract_type,
        "experience_level": row.experience_level,
        "skills": row.skills,
        "qualifications": row.qualifications,
        "languages": row.languages,
        "salary_display": row.salary_display,
        "start_date": row.start_date,
        "notes": row.notes,
        "extra_criteria": row.extra_criteria,
        "contact_name": row.contact_name,
        "contact_role": row.contact_role,
        "contact_email": row.contact_email,
        "contact_phone": row.contact_phone,
        "company_size": row.company_size,
        "job_id": row.job_id,
        "company_id": row.company_id,
        "company_name": row.company.name if row.company else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


def _company_for(db: Session, user: User, company_id: str | None):
    if user.role == UserRole.EMPLOYER:
        if company_id:
            if not user_belongs_to_company(db, user, company_id):
                raise AppError(403, "Vous n'avez pas accès à cette entreprise.", "FORBIDDEN")
            from app.models import Company

            company = db.get(Company, company_id)
            if not company:
                raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
            return company
        company = first_employer_company(db, user)
        if not company:
            raise AppError(400, "Aucune entreprise associée à ce compte.", "NO_COMPANY")
        return company
    if not company_id:
        raise AppError(400, "company_id est requis.", "VALIDATION_ERROR")
    from app.models import Company

    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    return company


def _assert_can_read(db: Session, user: User, row: RecruitmentMission) -> None:
    if user.role in STAFF_ROLES:
        return
    if user.role == UserRole.EMPLOYER and user_belongs_to_company(db, user, row.company_id):
        return
    raise AppError(403, "Vous n'avez pas accès à cette demande.", "FORBIDDEN")


def _notify_employer(db: Session, row: RecruitmentMission) -> None:
    from app.models import Company

    company = row.company or db.get(Company, row.company_id)
    if not company or not company.owner_user_id:
        return
    owner = db.get(User, company.owner_user_id)
    title, message = STATUS_COPY.get(row.status, ("Mise à jour", "Votre recrutement avance avec Talendus."))
    notify(db, owner, NotificationType.HIRING_REQUEST, title, message, portal_href(owner, "jobs", row.id))


def _notify_staff(db: Session, row: RecruitmentMission, title: str, message: str) -> None:
    staff = db.scalars(select(User).where(User.role.in_(STAFF_ROLES), User.is_active.is_(True))).all()
    for user in staff:
        notify(db, user, NotificationType.HIRING_REQUEST, title, message, portal_href(user, "jobs", row.id))


def create_request(db: Session, user: User, data: HiringRequestIn, ip: str | None = None) -> RecruitmentMission:
    company = _company_for(db, user, data.company_id)
    row = RecruitmentMission(
        company_id=company.id,
        recruiter_id=user.id if user.role in STAFF_ROLES else None,
        title=data.title.strip(),
        seats=data.seats or 1,
        status=MissionStatus.REQUEST_SUBMITTED,
        location=data.location,
        sector=data.sector,
        contract_type=data.contract_type,
        experience_level=data.experience_level,
        skills=data.skills,
        qualifications=data.qualifications,
        languages=data.languages,
        salary_display=data.salary_display,
        start_date=data.start_date,
        notes=data.notes,
        extra_criteria=data.extra_criteria,
        contact_name=data.contact_name or f"{user.first_name} {user.last_name}".strip(),
        contact_role=data.contact_role,
        contact_email=str(data.contact_email) if data.contact_email else user.email,
        contact_phone=data.contact_phone or user.phone,
        company_size=data.company_size,
    )
    db.add(row)
    db.flush()
    audit(db, "hiring_request.create", user, "mission", row.id, ip)
    _notify_employer(db, row)
    _notify_staff(
        db,
        row,
        "Nouveau besoin de recrutement",
        f"{company.name} a transmis un besoin : {row.title}.",
    )
    db.commit()
    db.refresh(row)
    return row


def list_requests(db: Session, user: User) -> list[RecruitmentMission]:
    stmt = select(RecruitmentMission).options(joinedload(RecruitmentMission.company))
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(RecruitmentMission.company_id.in_(ids))
    return list(db.scalars(stmt.order_by(RecruitmentMission.updated_at.desc())).unique().all())


def get_request(db: Session, user: User, request_id: str) -> RecruitmentMission:
    row = db.scalar(
        select(RecruitmentMission).options(joinedload(RecruitmentMission.company)).where(RecruitmentMission.id == request_id)
    )
    if not row:
        raise AppError(404, "Demande introuvable.", "HIRING_REQUEST_NOT_FOUND")
    _assert_can_read(db, user, row)
    return row


def update_request(db: Session, user: User, request_id: str, data: HiringRequestPatchIn) -> RecruitmentMission:
    row = get_request(db, user, request_id)
    if user.role == UserRole.EMPLOYER and row.status not in {
        MissionStatus.REQUEST_SUBMITTED,
        MissionStatus.UNDER_REVIEW,
        MissionStatus.CLIENT_CONTACTED,
        MissionStatus.CLIENT_VALIDATION,
    }:
        raise AppError(403, "Cette demande n'est plus modifiable de votre côté.", "FORBIDDEN")
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(row, key, value)
    row.updated_at = utcnow()
    audit(db, "hiring_request.update", user, "mission", row.id)
    db.commit()
    db.refresh(row)
    return row


def set_status(db: Session, user: User, request_id: str, status_raw: str) -> RecruitmentMission:
    if user.role not in STAFF_ROLES:
        raise AppError(403, "Seul Talendus met à jour le statut d'un recrutement.", "FORBIDDEN")
    try:
        status = MissionStatus(status_raw)
    except ValueError as exc:
        raise AppError(400, "Statut invalide.", "VALIDATION_ERROR") from exc
    row = get_request(db, user, request_id)
    row.status = status
    row.updated_at = utcnow()
    audit(db, f"hiring_request.{status.value.lower()}", user, "mission", row.id)
    _notify_employer(db, row)
    db.commit()
    db.refresh(row)
    return row


def employer_feedback(db: Session, user: User, request_id: str, action: str, comment: str | None) -> RecruitmentMission:
    row = get_request(db, user, request_id)
    if user.role != UserRole.EMPLOYER:
        raise AppError(403, "Ce retour est réservé à l'entreprise.", "FORBIDDEN")
    action = (action or "").strip().lower()
    note = (comment or "").strip()
    if action in {"validate", "valider", "confirm"}:
        row.status = MissionStatus.NEEDS_CONFIRMED if row.status == MissionStatus.CLIENT_VALIDATION else row.status
        if note:
            row.notes = ((row.notes or "") + "\n\nValidation client : " + note).strip()
    elif action in {"changes", "modification", "request_changes"}:
        if note:
            row.notes = ((row.notes or "") + "\n\nAjustement demandé : " + note).strip()
        row.status = MissionStatus.CLIENT_CONTACTED
    elif note:
        row.notes = ((row.notes or "") + "\n\nRetour client : " + note).strip()
    else:
        raise AppError(400, "Indiquez une action (valider, modification) ou un commentaire.", "VALIDATION_ERROR")
    row.updated_at = utcnow()
    audit(db, "hiring_request.feedback", user, "mission", row.id)
    _notify_staff(db, row, "Retour entreprise", note or action)
    db.commit()
    db.refresh(row)
    return row


def convert_to_job(db: Session, user: User, request_id: str) -> RecruitmentMission:
    if user.role not in STAFF_ROLES:
        raise AppError(403, "Seul Talendus crée et publie l'offre d'emploi.", "FORBIDDEN")
    row = get_request(db, user, request_id)
    description = "\n\n".join(
        part
        for part in [
            row.notes or "",
            f"Compétences : {row.skills}" if row.skills else "",
            f"Qualifications : {row.qualifications}" if row.qualifications else "",
            f"Critères : {row.extra_criteria}" if row.extra_criteria else "",
        ]
        if part
    )
    job = create_job(
        db,
        user,
        JobIn(
            title=row.title,
            description=description,
            company_id=row.company_id,
            location=row.location,
            sector=row.sector,
            contract_type=row.contract_type,
            skills=row.skills,
            experience_level=row.experience_level,
            qualifications=row.qualifications,
            salary_display=row.salary_display,
            openings=row.seats or 1,
            start_date=row.start_date,
        ),
    )
    row = db.get(RecruitmentMission, request_id) or row
    row.job_id = job.id
    row.status = MissionStatus.JOB_BEING_PREPARED
    row.updated_at = utcnow()
    audit(db, "hiring_request.convert_job", user, "mission", row.id)
    _notify_employer(db, row)
    db.commit()
    db.refresh(row)
    return row
