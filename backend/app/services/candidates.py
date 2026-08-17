from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import AppError
from app.models import (
    Candidate,
    CandidateCertification,
    CandidateEducation,
    CandidateExperience,
    Resume,
    User,
)
from app.models.enums import EmailType, NotificationType, UserRole
from app.rbac import is_admin
from app.schemas import AdminCandidatePatchIn, CandidateProfileIn, CertificationIn, EducationIn, ExperienceIn
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.notifications import notify
from app.services.resume_parse import parse_json_dump, parse_resume_bytes
from app.services.storage import delete_stored, save_resume


def create_staff_candidate(db: Session, actor: User, data) -> Candidate:
    from app.models import UserPreference
    from app.security import hash_password, random_password
    from app.services.email import send_email
    from app.services.notifications import notify

    existing = db.scalar(select(User).where(User.email == str(data.email).lower()))
    if existing:
        raise AppError(409, "Un compte existe déjà avec ce courriel.", "EMAIL_TAKEN")
    password = data.password or random_password()
    user = User(
        email=str(data.email).lower(),
        password_hash=hash_password(password),
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        phone=data.phone,
        role=UserRole.CANDIDATE,
    )
    db.add(user)
    db.flush()
    db.add(UserPreference(user_id=user.id))
    profile = Candidate(
        user_id=user.id,
        city=data.city,
        title=data.title,
        sector=data.sector,
        assigned_recruiter_id=actor.id,
    )
    db.add(profile)
    db.flush()
    send_email(db, user.email, EmailType.WELCOME, "welcome", name=user.first_name, link="espace.html")
    notify(db, user, NotificationType.ACCOUNT_CREATED, "Compte créé", "Votre dossier a été ouvert chez Talendus.")
    audit(db, "candidate.staff_create", actor, "candidate", profile.id)
    db.commit()
    db.refresh(profile)
    return profile


def list_for_staff(db: Session) -> list[Candidate]:
    return list(
        db.scalars(
            select(Candidate)
            .options(
                joinedload(Candidate.user),
                selectinload(Candidate.experiences),
                selectinload(Candidate.education),
                selectinload(Candidate.certifications),
                selectinload(Candidate.resumes),
            )
            .order_by(Candidate.updated_at.desc())
        ).unique().all()
    )


STAFF_PIPELINE = {
    "nouveau",
    "a-contacter",
    "qualifie",
    "entretien",
    "presente",
    "entretien-client",
    "offre",
    "place",
    "refuse",
    "inactif",
}


def get_staff_candidate(db: Session, candidate_id: str) -> Candidate:
    profile = db.scalar(
        select(Candidate)
        .options(
            joinedload(Candidate.user),
            selectinload(Candidate.experiences),
            selectinload(Candidate.education),
            selectinload(Candidate.certifications),
            selectinload(Candidate.resumes),
        )
        .where(Candidate.id == candidate_id)
    )
    if not profile:
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    return profile


def update_staff_candidate(db: Session, actor: User, candidate_id: str, data: AdminCandidatePatchIn) -> Candidate:
    profile = get_staff_candidate(db, candidate_id)
    payload = data.model_dump(exclude_unset=True)
    user_fields = {key: payload.pop(key) for key in ("first_name", "last_name", "phone") if key in payload}
    if profile.user and user_fields:
        for key, value in user_fields.items():
            setattr(profile.user, key, value)
    if "pipeline_status" in payload:
        status = (payload["pipeline_status"] or "").strip()
        if status and status not in STAFF_PIPELINE:
            raise AppError(400, "Statut de pipeline invalide.", "VALIDATION_ERROR")
        payload["pipeline_status"] = status or None
    for key, value in payload.items():
        setattr(profile, key, value)
    audit(db, "candidate.staff_update", actor, "candidate", profile.id)
    db.commit()
    return get_staff_candidate(db, profile.id)


def upload_cv_for_candidate(db: Session, actor: User, candidate_id: str, data: bytes, filename: str) -> Resume:
    profile = get_staff_candidate(db, candidate_id)
    original, stored, mime, size, url = save_resume(data, filename)
    parse_status = "failed"
    parse_json = None
    parsed: dict = {}
    try:
        parsed = parse_resume_bytes(data, mime, original)
        parse_status = parsed.get("status") or "done"
        parse_json = parse_json_dump(parsed)
    except Exception:
        parse_status = "failed"
        parsed = {}
    if not (profile.skills or "").strip() and parsed.get("skills"):
        profile.skills = ", ".join(parsed["skills"])
    for old in db.scalars(select(Resume).where(Resume.candidate_id == profile.id)):
        old.is_primary = False
    row = Resume(
        candidate_id=profile.id,
        original_name=original,
        stored_name=stored,
        storage_url=url,
        mime_type=mime,
        size_bytes=size,
        is_primary=True,
        parse_status=parse_status,
        parse_json=parse_json,
    )
    db.add(row)
    if profile.user:
        notify(db, profile.user, NotificationType.RESUME_UPDATED, "CV mis à jour", "Talendus a déposé un document dans votre dossier.")
    audit(db, "candidate.staff_resume_upload", actor, "candidate", profile.id)
    db.commit()
    db.refresh(row)
    return row


def update_profile(db: Session, user: User, data: CandidateProfileIn) -> Candidate:
    profile = ensure_candidate(db, user)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    audit(db, "candidate.profile_update", user, "candidate", profile.id)
    db.commit()
    db.refresh(profile)
    return profile


def add_experience(db: Session, user: User, data: ExperienceIn) -> CandidateExperience:
    profile = ensure_candidate(db, user)
    row = CandidateExperience(candidate_id=profile.id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def add_education(db: Session, user: User, data: EducationIn) -> CandidateEducation:
    profile = ensure_candidate(db, user)
    row = CandidateEducation(candidate_id=profile.id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def add_certification(db: Session, user: User, data: CertificationIn) -> CandidateCertification:
    profile = ensure_candidate(db, user)
    row = CandidateCertification(candidate_id=profile.id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def upload_cv(db: Session, user: User, data: bytes, filename: str) -> Resume:
    profile = ensure_candidate(db, user)
    original, stored, mime, size, url = save_resume(data, filename)
    parse_status = "failed"
    parse_json = None
    parsed: dict = {}
    try:
        parsed = parse_resume_bytes(data, mime, original)
        parse_status = parsed.get("status") or "done"
        parse_json = parse_json_dump(parsed)
    except Exception:
        parse_status = "failed"
        parsed = {}
    if not (profile.skills or "").strip() and parsed.get("skills"):
        profile.skills = ", ".join(parsed["skills"])
    for old in db.scalars(select(Resume).where(Resume.candidate_id == profile.id)):
        old.is_primary = False
    row = Resume(
        candidate_id=profile.id,
        original_name=original,
        stored_name=stored,
        storage_url=url,
        mime_type=mime,
        size_bytes=size,
        is_primary=True,
        parse_status=parse_status,
        parse_json=parse_json,
    )
    db.add(row)
    notify(db, user, NotificationType.RESUME_UPDATED, "CV mis à jour", "Votre CV a été enregistré.")
    audit(db, "candidate.resume_upload", user, "candidate", profile.id)
    db.commit()
    db.refresh(row)
    return row


def serialize_candidate(profile: Candidate, include_private: bool = True) -> dict:
    from app.services.portal import profile_completeness

    user = profile.user
    public = {
        "id": profile.id,
        "first_name": user.first_name if user else "",
        "title": profile.title,
        "city": profile.city,
        "sector": profile.sector,
        "years_experience": profile.years_experience,
        "skills": profile.skills,
        "languages": profile.languages,
        "experience_level": profile.experience_level,
        "bio": profile.bio,
        "experiences": [
            {"id": e.id, "company": e.company, "role": e.role, "years": e.years, "description": e.description}
            for e in (profile.experiences or [])
        ],
        "education": [
            {"id": e.id, "school": e.school, "diploma": e.diploma, "year": e.year}
            for e in (profile.education or [])
        ],
        "certifications": [
            {"id": c.id, "name": c.name, "issuer": c.issuer, "year": c.year}
            for c in (profile.certifications or [])
        ],
        "resumes": [
            {
                "id": r.id,
                "original_name": r.original_name,
                "is_primary": r.is_primary,
                "size_bytes": r.size_bytes,
                "parse_status": r.parse_status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "download_path": f"/api/candidates/resumes/{r.id}/file",
            }
            for r in (profile.resumes or [])
        ],
    }
    if not include_private:
        return public
    public.update(
        {
            "email": user.email if user else None,
            "phone": user.phone if user else None,
            "last_name": user.last_name if user else "",
            "address": profile.address,
            "province": profile.province,
            "country": profile.country,
            "birth_date": profile.birth_date,
            "availability": profile.availability,
            "desired_salary_min": profile.desired_salary_min,
            "desired_salary_max": profile.desired_salary_max,
            "mobility": profile.mobility,
            "contract_type": profile.contract_type,
            "shift_preference": profile.shift_preference,
            "education_level": profile.education_level,
            "job_search_status": profile.job_search_status.value if profile.job_search_status else None,
            "work_preferences": profile.work_preferences,
            "completeness": profile_completeness(profile) if user else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
            "avatar_path": user.avatar_path if user else None,
        }
    )
    return public


def get_resume_for_user(db: Session, user: User, resume_id: str) -> Resume:
    resume = db.get(Resume, resume_id)
    if not resume:
        raise AppError(404, "CV introuvable.", "RESUME_NOT_FOUND")
    if is_admin(user) or user.role.value == "RECRUITER":
        return resume
    if user.role.value == "EMPLOYER":
        from app.models import Application, JobOffer
        from app.services.access import company_ids_for_employer, is_presented_to_employer

        ids = company_ids_for_employer(db, user)
        if ids:
            apps = list(
                db.scalars(
                    select(Application)
                    .options(joinedload(Application.history))
                    .join(JobOffer, Application.job_id == JobOffer.id)
                    .where(Application.candidate_id == resume.candidate_id, JobOffer.company_id.in_(ids))
                )
                .unique()
                .all()
            )
            if any(is_presented_to_employer(row) for row in apps):
                return resume
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    if user.role.value == "CANDIDATE":
        profile = ensure_candidate(db, user)
        if resume.candidate_id != profile.id:
            raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
        return resume
    raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")


def delete_resume(db: Session, user: User, resume_id: str) -> None:
    resume = get_resume_for_user(db, user, resume_id)
    profile = ensure_candidate(db, user)
    if resume.candidate_id != profile.id:
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    was_primary = resume.is_primary
    delete_stored(resume.stored_name, resume.storage_url, "resumes")
    db.delete(resume)
    db.flush()
    if was_primary:
        nxt = db.scalar(select(Resume).where(Resume.candidate_id == profile.id).order_by(Resume.created_at.desc()))
        if nxt:
            nxt.is_primary = True
    audit(db, "candidate.resume_delete", user, "candidate", profile.id)
    db.commit()


def _owned_row(db: Session, user: User, model, row_id: str):
    profile = ensure_candidate(db, user)
    row = db.get(model, row_id)
    if not row or row.candidate_id != profile.id:
        raise AppError(404, "Élément introuvable.", "NOT_FOUND")
    return row


def patch_experience(db: Session, user: User, row_id: str, data: ExperienceIn) -> CandidateExperience:
    row = _owned_row(db, user, CandidateExperience, row_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_experience(db: Session, user: User, row_id: str) -> None:
    row = _owned_row(db, user, CandidateExperience, row_id)
    db.delete(row)
    db.commit()


def patch_education(db: Session, user: User, row_id: str, data: EducationIn) -> CandidateEducation:
    row = _owned_row(db, user, CandidateEducation, row_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_education(db: Session, user: User, row_id: str) -> None:
    row = _owned_row(db, user, CandidateEducation, row_id)
    db.delete(row)
    db.commit()


def patch_certification(db: Session, user: User, row_id: str, data: CertificationIn) -> CandidateCertification:
    row = _owned_row(db, user, CandidateCertification, row_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_certification(db: Session, user: User, row_id: str) -> None:
    row = _owned_row(db, user, CandidateCertification, row_id)
    db.delete(row)
    db.commit()


def analyze_with_ai(db: Session, user: User, candidate_id: str, purpose: str) -> dict:
    from app.integrations.ai.openai import ALLOWED_PURPOSES, OpenAIService
    from app.rbac import ADMINS

    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Analyse IA réservée à l'équipe Talendus.", "FORBIDDEN")
    if purpose not in ALLOWED_PURPOSES:
        raise AppError(400, "Usage OpenAI non autorisé.", "INTEGRATION_INVALID_REQUEST")
    profile = db.scalar(
        select(Candidate)
        .options(joinedload(Candidate.user), joinedload(Candidate.resumes))
        .where(Candidate.id == candidate_id)
    )
    if not profile:
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    resume_text = ""
    for resume in profile.resumes or []:
        if resume.parse_json:
            resume_text = resume.parse_json
            break
    blob = " ".join(
        part
        for part in [
            profile.user.full_name if profile.user else "",
            profile.title or "",
            profile.skills or "",
            profile.bio or "",
            resume_text,
        ]
        if part
    ).strip()
    if not blob:
        raise AppError(400, "Pas assez de contenu pour une analyse IA.", "VALIDATION_ERROR")
    service = OpenAIService()
    if purpose == "skill_extraction":
        return service.extract_skills(blob)
    if purpose == "profile_classification":
        return service.classify_profile(blob)
    if purpose == "matching_suggestion":
        return service.suggest_match(blob, profile.title or "")
    if purpose == "job_description":
        return service.improve_job_description(blob)
    return service.analyze_resume(blob)
