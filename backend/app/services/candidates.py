from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import (
    Candidate,
    CandidateCertification,
    CandidateEducation,
    CandidateExperience,
    Resume,
    User,
)
from app.models.enums import NotificationType
from app.schemas import CandidateProfileIn, CertificationIn, EducationIn, ExperienceIn
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.notifications import notify
from app.services.storage import save_resume


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
    original, stored, mime, size = save_resume(data, filename)
    for old in db.scalars(select(Resume).where(Resume.candidate_id == profile.id)):
        old.is_primary = False
    row = Resume(
        candidate_id=profile.id,
        original_name=original,
        stored_name=stored,
        mime_type=mime,
        size_bytes=size,
        is_primary=True,
    )
    db.add(row)
    notify(db, user, NotificationType.RESUME_UPDATED, "CV mis à jour", "Votre CV a été enregistré.")
    audit(db, "candidate.resume_upload", user, "candidate", profile.id)
    db.commit()
    db.refresh(row)
    return row


def serialize_candidate(profile: Candidate, include_private: bool = True) -> dict:
    user = profile.user
    public = {
        "id": profile.id,
        "first_name": user.first_name,
        "title": profile.title,
        "city": profile.city,
        "sector": profile.sector,
        "years_experience": profile.years_experience,
        "skills": profile.skills,
        "languages": profile.languages,
        "experience_level": profile.experience_level,
    }
    if not include_private:
        return public
    public.update(
        {
            "email": user.email,
            "phone": user.phone,
            "last_name": user.last_name,
            "availability": profile.availability,
            "desired_salary_min": profile.desired_salary_min,
            "desired_salary_max": profile.desired_salary_max,
            "mobility": profile.mobility,
            "contract_type": profile.contract_type,
            "shift_preference": profile.shift_preference,
            "bio": profile.bio,
            "experiences": [
                {"id": e.id, "company": e.company, "role": e.role, "years": e.years, "description": e.description}
                for e in profile.experiences
            ],
            "education": [
                {"id": e.id, "school": e.school, "diploma": e.diploma, "year": e.year}
                for e in profile.education
            ],
            "certifications": [
                {"id": c.id, "name": c.name, "issuer": c.issuer, "year": c.year}
                for c in profile.certifications
            ],
            "resumes": [
                {"id": r.id, "original_name": r.original_name, "is_primary": r.is_primary, "size_bytes": r.size_bytes}
                for r in profile.resumes
            ],
        }
    )
    return public


def get_resume_for_user(db: Session, user: User, resume_id: str) -> Resume:
    resume = db.get(Resume, resume_id)
    if not resume:
        raise AppError(404, "CV introuvable.", "RESUME_NOT_FOUND")
    if user.role.value in {"RECRUITER", "ADMIN"}:
        return resume
    if user.role.value == "EMPLOYER":
        from app.models import Application, Company, JobOffer

        company = db.scalar(select(Company).where(Company.owner_user_id == user.id))
        if company:
            linked = db.scalar(
                select(Application)
                .join(JobOffer, Application.job_id == JobOffer.id)
                .where(Application.resume_id == resume.id, JobOffer.company_id == company.id)
            )
            if linked:
                return resume
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    if user.role.value == "CANDIDATE":
        profile = ensure_candidate(db, user)
        if resume.candidate_id != profile.id:
            raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
        return resume
    raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
