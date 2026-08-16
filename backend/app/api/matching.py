from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.services import matching as matching_service

router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("/jobs")
def my_matches(
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok(matching_service.my_job_matches(db, user, limit))


@router.get("/jobs/{job_id}/candidates")
def job_candidates(
    job_id: str,
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(matching_service.staff_job_candidates(db, user, job_id, limit))


@router.get("/candidates/{candidate_id}")
def candidate_jobs(
    candidate_id: str,
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    return ok(matching_service.staff_candidate_jobs(db, user, candidate_id, limit))
