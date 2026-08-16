from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import ok
from app.models import Candidate, User
from app.models.enums import UserRole
from app.schemas import CandidateProfileIn, CertificationIn, EducationIn, ExperienceIn
from app.services import candidates as cand_svc
from app.services.auth import ensure_candidate
from app.services.storage import resume_path

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/me")
def my_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = ensure_candidate(db, user)
    profile = db.scalar(
        select(Candidate)
        .options(
            joinedload(Candidate.user),
            joinedload(Candidate.experiences),
            joinedload(Candidate.education),
            joinedload(Candidate.certifications),
            joinedload(Candidate.resumes),
        )
        .where(Candidate.id == profile.id)
    )
    return ok(cand_svc.serialize_candidate(profile, include_private=True))


@router.patch("/me")
def update_profile(payload: CandidateProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = cand_svc.update_profile(db, user, payload)
    return ok({"id": profile.id})


@router.post("/me/experiences")
def add_exp(payload: ExperienceIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_experience(db, user, payload)
    return ok({"id": row.id})


@router.post("/me/education")
def add_edu(payload: EducationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_education(db, user, payload)
    return ok({"id": row.id})


@router.post("/me/certifications")
def add_cert(payload: CertificationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_certification(db, user, payload)
    return ok({"id": row.id})


@router.post("/me/resume")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await file.read()
    row = cand_svc.upload_cv(db, user, data, file.filename or "cv.pdf")
    return ok({"id": row.id, "original_name": row.original_name})


@router.get("/resumes/{resume_id}/file")
def download_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = cand_svc.get_resume_for_user(db, user, resume_id)
    path = resume_path(resume.stored_name)
    return FileResponse(path, media_type=resume.mime_type, filename=resume.original_name)


@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: str,
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.EMPLOYER)),
    db: Session = Depends(get_db),
):
    profile = db.scalar(
        select(Candidate)
        .options(
            joinedload(Candidate.user),
            joinedload(Candidate.experiences),
            joinedload(Candidate.education),
            joinedload(Candidate.certifications),
            joinedload(Candidate.resumes),
        )
        .where(Candidate.id == candidate_id)
    )
    if not profile:
        from app.errors import AppError
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    private = user.role in {UserRole.RECRUITER, UserRole.ADMIN}
    return ok(cand_svc.serialize_candidate(profile, include_private=private))
