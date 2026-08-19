from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, get_current_user_optional, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import JobStatus, UserRole
from app.schemas import JobIn, JobPatchIn
from app.services import jobs as jobs_service
from app.services.portal import list_saved_jobs, save_job, saved_job_ids, unsave_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def search_jobs(
    q: str | None = None,
    location: str | None = None,
    sector: str | None = None,
    contract_type: str | None = None,
    experience: str | None = None,
    company: str | None = None,
    shift: str | None = None,
    schedule: str | None = None,
    work_mode: str | None = None,
    salary_min: int | None = Query(default=None, ge=0),
    salary_max: int | None = Query(default=None, ge=0),
    lat: float | None = Query(default=None),
    lng: float | None = Query(default=None),
    radius_km: float | None = Query(default=None, ge=1, le=500),
    sort: str = "relevance",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    items, total = jobs_service.search_jobs(
        db,
        q=q,
        location=location,
        sector=sector,
        contract_type=contract_type,
        experience=experience,
        company=company,
        shift=shift,
        schedule=schedule,
        work_mode=work_mode,
        salary_min=salary_min,
        salary_max=salary_max,
        sort=sort,
        page=page,
        page_size=page_size,
        public_only=True,
        lat=lat,
        lng=lng,
        radius_km=radius_km,
    )
    pages = max(1, (total + page_size - 1) // page_size) if total else 0
    payload = [jobs_service.serialize_job(item) for item in items]
    if user and user.role == UserRole.CANDIDATE:
        saved = saved_job_ids(db, user, [item["id"] for item in payload])
        for item in payload:
            item["saved"] = item["id"] in saved
    return ok(
        payload,
        meta={"total": total, "page": page, "page_size": page_size, "pages": pages},
    )


@router.get("/board")
def job_board(db: Session = Depends(get_db)):
    return ok(jobs_service.export_board(db))


@router.get("/options")
def job_options(db: Session = Depends(get_db)):
    from app.services.job_catalog import catalog

    return ok(catalog(db))


@router.get("/managed")
def managed_jobs(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    items = jobs_service.list_managed(db, user)
    return ok([jobs_service.serialize_job(item) for item in items])


@router.get("/saved")
def saved_jobs(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.CANDIDATE))):
    return ok(list_saved_jobs(db, user))


@router.get("/managed/{job_id}")
def get_managed_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(jobs_service.serialize_job(jobs_service.get_managed_job(db, user, job_id)))


@router.post("/{job_id}/save")
def bookmark_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok(save_job(db, user, job_id))


@router.delete("/{job_id}/save")
def remove_bookmark(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok(unsave_job(db, user, job_id))


@router.get("/{slug}")
def get_job(slug: str, db: Session = Depends(get_db), user: User | None = Depends(get_current_user_optional)):
    job = jobs_service.get_public_job(db, slug)
    payload = jobs_service.serialize_job(job)
    if user and user.role == UserRole.CANDIDATE:
        payload["saved"] = job.id in saved_job_ids(db, user, [job.id])
    return ok(payload)


@router.post("")
def create_job(
    payload: JobIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    job = jobs_service.create_job(db, user, payload, client_ip(request))
    return ok(jobs_service.serialize_job(job))


@router.patch("/{job_id}")
def update_job(
    job_id: str,
    payload: JobPatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = jobs_service.update_job(db, user, job_id, payload)
    return ok(jobs_service.serialize_job(job))


@router.post("/{job_id}/publish")
def publish_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = jobs_service.set_job_status(db, user, job_id, JobStatus.PUBLISHED)
    return ok(jobs_service.serialize_job(job))


@router.post("/{job_id}/pause")
def pause_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = jobs_service.set_job_status(db, user, job_id, JobStatus.PAUSED)
    return ok(jobs_service.serialize_job(job))


@router.post("/{job_id}/close")
def close_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = jobs_service.set_job_status(db, user, job_id, JobStatus.CLOSED)
    return ok(jobs_service.serialize_job(job))


@router.post("/{job_id}/archive")
def archive_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = jobs_service.set_job_status(db, user, job_id, JobStatus.ARCHIVED)
    return ok(jobs_service.serialize_job(job))


@router.post("/{job_id}/duplicate")
def duplicate_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    job = jobs_service.duplicate_job(db, user, job_id)
    return ok(jobs_service.serialize_job(job))


@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    jobs_service.delete_job(db, user, job_id)
    return ok(message="Offre supprimée.")
