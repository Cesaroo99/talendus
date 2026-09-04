from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import AppError, ok
from app.models import Application, Candidate, JobOffer, User
from app.models.enums import UserRole
from app.rbac import is_admin
from app.integrations.schemas import AiPurposeIn
from app.schemas import CandidateProfileIn, CertificationIn, EducationIn, ExperienceIn
from app.services import candidates as cand_svc
from app.services.access import company_ids_for_employer, is_presented_to_employer
from app.services.auth import ensure_candidate
from app.services.portal import candidate_dashboard
from app.services.storage import open_resume

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


@router.get("/me/dashboard")
def my_dashboard(user: User = Depends(require_roles(UserRole.CANDIDATE)), db: Session = Depends(get_db)):
    return ok(candidate_dashboard(db, user))


@router.patch("/me")
def update_profile(payload: CandidateProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = cand_svc.update_profile(db, user, payload)
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


@router.post("/me/experiences")
def add_exp(payload: ExperienceIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_experience(db, user, payload)
    return ok({"id": row.id})


@router.patch("/me/experiences/{row_id}")
def patch_exp(row_id: str, payload: ExperienceIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.patch_experience(db, user, row_id, payload)
    return ok({"id": row.id})


@router.delete("/me/experiences/{row_id}")
def del_exp(row_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cand_svc.delete_experience(db, user, row_id)
    return ok(message="Expérience supprimée.")


@router.post("/me/education")
def add_edu(payload: EducationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_education(db, user, payload)
    return ok({"id": row.id})


@router.patch("/me/education/{row_id}")
def patch_edu(row_id: str, payload: EducationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.patch_education(db, user, row_id, payload)
    return ok({"id": row.id})


@router.delete("/me/education/{row_id}")
def del_edu(row_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cand_svc.delete_education(db, user, row_id)
    return ok(message="Formation supprimée.")


@router.post("/me/certifications")
def add_cert(payload: CertificationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.add_certification(db, user, payload)
    return ok({"id": row.id})


@router.patch("/me/certifications/{row_id}")
def patch_cert(row_id: str, payload: CertificationIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = cand_svc.patch_certification(db, user, row_id, payload)
    return ok({"id": row.id})


@router.delete("/me/certifications/{row_id}")
def del_cert(row_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cand_svc.delete_certification(db, user, row_id)
    return ok(message="Certification supprimée.")


@router.post("/me/resume")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await file.read()
    row = cand_svc.upload_cv(db, user, data, file.filename or "cv")
    return ok({"id": row.id, "original_name": row.original_name, "parse_status": row.parse_status})


@router.delete("/me/resume/{resume_id}")
def delete_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cand_svc.delete_resume(db, user, resume_id)
    return ok(message="CV supprimé.")


@router.get("")
def list_candidates(
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    private = is_admin(user) or user.role == UserRole.RECRUITER
    return ok([cand_svc.serialize_candidate(c, include_private=private) for c in cand_svc.list_for_staff(db)])


@router.get("/resumes/{resume_id}/file")
def download_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = cand_svc.get_resume_for_user(db, user, resume_id)
    url, path = open_resume(resume.stored_name, resume.storage_url)
    if url:
        return RedirectResponse(url)
    return FileResponse(path, media_type=resume.mime_type, filename=resume.original_name)


@router.get("/resumes/{resume_id}/preview")
def preview_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.services.resume_parse import preview_html
    from app.services.storage import read_stored_bytes

    resume = cand_svc.get_resume_for_user(db, user, resume_id)
    data = read_stored_bytes(resume.stored_name, resume.storage_url, "resumes")
    return HTMLResponse(preview_html(data, resume.mime_type, resume.original_name))


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
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    private = is_admin(user) or user.role == UserRole.RECRUITER
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            raise AppError(403, "Vous n'avez pas accès à ce candidat.", "FORBIDDEN")
        linked = list(
            db.scalars(
                select(Application)
                .options(joinedload(Application.history))
                .join(JobOffer, Application.job_id == JobOffer.id)
                .where(Application.candidate_id == profile.id, JobOffer.company_id.in_(ids))
            )
            .unique()
            .all()
        )
        if not any(is_presented_to_employer(row) for row in linked):
            raise AppError(403, "Ce dossier n'a pas encore été transmis par Talendus.", "FORBIDDEN")
        private = False
    payload = cand_svc.serialize_candidate(profile, include_private=private)
    if user.role == UserRole.EMPLOYER and profile.user:
        payload["last_name"] = profile.user.last_name
    return ok(payload)


@router.post("/{candidate_id}/ai")
def analyze_candidate_ai(
    candidate_id: str,
    payload: AiPurposeIn,
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return ok(cand_svc.analyze_with_ai(db, user, candidate_id, payload.purpose))
