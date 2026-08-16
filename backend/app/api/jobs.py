from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import JobStatus, UserRole
from app.schemas import JobIn, JobPatchIn
from app.services import jobs as jobs_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def search_jobs(
    q: str | None = None,
    location: str | None = None,
    sector: str | None = None,
    contract_type: str | None = None,
    experience: str | None = None,
    company: str | None = None,
    salary_min: int | None = Query(default=None, ge=0),
    salary_max: int | None = Query(default=None, ge=0),
    lat: float | None = Query(default=None),
    lng: float | None = Query(default=None),
    radius_km: float | None = Query(default=None, ge=1, le=500),
    sort: str = "relevance",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    items, total = jobs_service.search_jobs(
        db,
        q=q,
        location=location,
        sector=sector,
        contract_type=contract_type,
        experience=experience,
        company=company,
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
    return ok(
        [jobs_service.serialize_job(item) for item in items],
        meta={"total": total, "page": page, "page_size": page_size, "pages": pages},
    )


@router.get("/board")
def job_board(db: Session = Depends(get_db)):
    return ok(jobs_service.export_board(db))


@router.get("/managed")
def managed_jobs(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN)),
):
    items = jobs_service.list_managed(db, user)
    return ok([jobs_service.serialize_job(item) for item in items])


@router.get("/{slug}")
def get_job(slug: str, db: Session = Depends(get_db)):
    job = jobs_service.get_public_job(db, slug)
    return ok(jobs_service.serialize_job(job))


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
