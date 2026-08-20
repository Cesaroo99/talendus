from datetime import datetime, timezone
from urllib.parse import quote

from sqlalchemy import Select, case, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.config import get_settings
from app.deps import slugify
from app.errors import AppError
from app.models import Company, JobOffer, User
from app.models.enums import JobStatus, OPEN_JOB_STATUSES, PUBLIC_JOB_STATUSES, UserRole, utcnow
from app.rbac import ADMINS
from app.schemas import JobIn, JobPatchIn
from app.services.access import company_ids_for_employer, first_employer_company, user_belongs_to_company
from app.services.audit import audit


def _parse_expires(value: str | None):
    if not value:
        return None
    raw = value.strip().replace("Z", "+00:00")
    if "T" not in raw and len(raw) == 10:
        raw = raw + "T23:59:59+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise AppError(400, "Date limite invalide.", "INVALID_DATETIME") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _unique_slug(db: Session, base: str, ignore_id: str | None = None) -> str:
    from app.site_jobs import is_site_job_slug

    slug = slugify(base)
    i = 2
    while True:
        q = select(JobOffer).where(JobOffer.slug == slug)
        if ignore_id:
            q = q.where(JobOffer.id != ignore_id)
        taken = bool(db.scalar(q))
        if not taken and is_site_job_slug(slug):
            current = db.get(JobOffer, ignore_id) if ignore_id else None
            if not current or current.slug != slug:
                taken = True
        if not taken:
            return slug
        slug = f"{slugify(base)}-{i}"
        i += 1


def public_job_url(job: JobOffer, lang: str = "fr") -> str:
    base = get_settings().frontend_url.rstrip("/")
    if lang == "en":
        return f"{base}/en/job-{job.slug}.html"
    return f"{base}/emploi-{job.slug}.html"


def linkedin_share_url(url: str) -> str:
    return "https://www.linkedin.com/sharing/share-offsite/?url=" + quote(url, safe="")


def serialize_job(job: JobOffer) -> dict:
    url_fr = public_job_url(job, "fr")
    url_en = public_job_url(job, "en")
    return {
        "id": job.id,
        "slug": job.slug,
        "title": job.title,
        "description": job.description,
        "responsibilities": job.responsibilities,
        "qualifications": job.qualifications,
        "location": job.location,
        "lat": job.lat,
        "lng": job.lng,
        "place_id": job.place_id,
        "sector": job.sector,
        "contract_type": job.contract_type,
        "salary_display": job.salary_display,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "currency": job.currency,
        "openings": job.openings,
        "skills": job.skills,
        "experience_level": job.experience_level,
        "education_required": job.education_required,
        "certifications": job.certifications,
        "shift": job.shift,
        "schedule": job.schedule,
        "work_mode": job.work_mode,
        "languages": job.languages,
        "overtime": job.overtime,
        "driver_license": job.driver_license,
        "unionized": job.unionized,
        "travel": job.travel,
        "work_authorization": job.work_authorization,
        "can_sponsor": bool(job.can_sponsor),
        "benefits": job.benefits,
        "start_date": job.start_date,
        "status": job.status.value,
        "published_at": job.published_at.isoformat() if job.published_at else None,
        "expires_at": job.expires_at.isoformat() if job.expires_at else None,
        "company_id": job.company_id,
        "company_name": job.company.name if job.company else None,
        "url": f"emploi-{job.slug}.html",
        "public_url": url_fr,
        "share": {
            "linkedin": linkedin_share_url(url_fr),
            "linkedin_en": linkedin_share_url(url_en),
        },
    }


def export_board(db: Session) -> dict:
    items, _total = search_jobs(db, public_only=True, page=1, page_size=50, sort="published_at")
    return {
        "source": "Talendus",
        "url": get_settings().frontend_url,
        "updated_at": utcnow().isoformat(),
        "jobs": [
            {
                "id": job.id,
                "slug": job.slug,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "sector": job.sector,
                "employment_type": job.contract_type,
                "salary": job.salary_display,
                "skills": job.skills,
                "date_posted": job.published_at.isoformat() if job.published_at else None,
                "valid_through": job.expires_at.isoformat() if job.expires_at else None,
                "url": public_job_url(job),
                "company": job.company.name if job.company else "Talendus",
            }
            for job in items
            if job.status.value == "PUBLISHED"
        ],
    }


def search_jobs(
    db: Session,
    *,
    q: str | None = None,
    sector: str | None = None,
    location: str | None = None,
    contract_type: str | None = None,
    experience: str | None = None,
    salary_min: int | None = None,
    salary_max: int | None = None,
    company: str | None = None,
    shift: str | None = None,
    schedule: str | None = None,
    work_mode: str | None = None,
    work_authorization: str | None = None,
    work_status: str | None = None,
    can_sponsor: bool | None = None,
    title: str | None = None,
    status: JobStatus | None = None,
    public_only: bool = True,
    page: int = 1,
    page_size: int = 12,
    sort: str = "published_at",
    lat: float | None = None,
    lng: float | None = None,
    radius_km: float | None = None,
) -> tuple[list[JobOffer], int]:
    stmt: Select = select(JobOffer).options(joinedload(JobOffer.company))
    if public_only:
        stmt = stmt.where(JobOffer.status.in_(PUBLIC_JOB_STATUSES))
        stmt = stmt.where(or_(JobOffer.expires_at.is_(None), JobOffer.expires_at > utcnow()))
    elif status:
        stmt = stmt.where(JobOffer.status == status)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                JobOffer.title.ilike(like),
                JobOffer.description.ilike(like),
                JobOffer.skills.ilike(like),
                JobOffer.location.ilike(like),
                JobOffer.sector.ilike(like),
            )
        )
    if sector:
        stmt = stmt.where(JobOffer.sector.ilike(f"%{sector}%"))
    if location:
        from app.integrations.hooks import maybe_geocode
        from app.integrations.registry import is_active

        if radius_km and lat is None and lng is None and is_active("google_maps"):
            geo = maybe_geocode(location)
            if geo and geo.get("lat") is not None and geo.get("lng") is not None:
                lat = float(geo["lat"])
                lng = float(geo["lng"])
        if lat is None:
            stmt = stmt.where(JobOffer.location.ilike(f"%{location}%"))
    if lat is not None and lng is not None and radius_km:
        delta = max(float(radius_km), 1.0) / 111.0
        stmt = stmt.where(
            JobOffer.lat.is_not(None),
            JobOffer.lng.is_not(None),
            JobOffer.lat.between(lat - delta, lat + delta),
            JobOffer.lng.between(lng - delta, lng + delta),
        )
    if contract_type:
        stmt = stmt.where(JobOffer.contract_type.ilike(f"%{contract_type}%"))
    if experience:
        stmt = stmt.where(JobOffer.experience_level.ilike(f"%{experience}%"))
    if shift:
        stmt = stmt.where(JobOffer.shift.ilike(f"%{shift}%"))
    if schedule:
        stmt = stmt.where(JobOffer.schedule.ilike(f"%{schedule}%"))
    if work_mode:
        stmt = stmt.where(JobOffer.work_mode.ilike(f"%{work_mode}%"))
    if title:
        stmt = stmt.where(JobOffer.title.ilike(f"%{title.strip()}%"))
    if work_authorization:
        stmt = stmt.where(JobOffer.work_authorization == work_authorization.strip())
    if can_sponsor is True:
        stmt = stmt.where(JobOffer.can_sponsor.is_(True))
    if work_status:
        from app.services.job_catalog import allowed_authorizations_for_status

        allowed = allowed_authorizations_for_status(work_status)
        if allowed is not None:
            stmt = stmt.where(
                or_(
                    JobOffer.work_authorization.is_(None),
                    JobOffer.work_authorization.in_(allowed),
                    JobOffer.can_sponsor.is_(True),
                )
            )
    if salary_min:
        stmt = stmt.where(or_(JobOffer.salary_min >= salary_min, JobOffer.salary_max >= salary_min))
    if salary_max:
        stmt = stmt.where(or_(JobOffer.salary_max <= salary_max, JobOffer.salary_min <= salary_max))
    if company:
        stmt = stmt.join(Company).where(Company.name.ilike(f"%{company}%"))
    order_clauses: list = []
    if sort in {"relevance", "published_at"} and q:
        like = f"%{q.strip()}%"
        order_clauses.append(case((JobOffer.title.ilike(like), 0), else_=1))
    order_map = {
        "title": JobOffer.title.asc(),
        "salary": JobOffer.salary_max.desc(),
        "published_at": JobOffer.published_at.desc(),
        "relevance": JobOffer.published_at.desc(),
    }
    order_clauses.append(order_map.get(sort, JobOffer.published_at.desc()))
    total = db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
    rows = db.scalars(stmt.order_by(*order_clauses).offset((page - 1) * page_size).limit(page_size)).unique().all()
    return list(rows), int(total)


def lookup_job(db: Session, slug_or_id: str) -> JobOffer | None:
    if not slug_or_id:
        return None
    return db.scalar(
        select(JobOffer).options(joinedload(JobOffer.company)).where(
            or_(JobOffer.slug == slug_or_id, JobOffer.id == slug_or_id)
        )
    )


def get_public_job(db: Session, slug_or_id: str) -> JobOffer:
    job = lookup_job(db, slug_or_id)
    if not job:
        from app.site_jobs import ensure_catalog_job, is_site_job_slug

        if is_site_job_slug(slug_or_id):
            created = ensure_catalog_job(db, slug_or_id)
            if created:
                db.commit()
                job = lookup_job(db, slug_or_id)
    if not job or job.status not in PUBLIC_JOB_STATUSES:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    return job


def assert_job_open(job: JobOffer) -> None:
    if job.status not in OPEN_JOB_STATUSES:
        raise AppError(409, "Cette offre n'accepte plus de candidatures.", "JOB_CLOSED")
    if job.expires_at and job.expires_at < utcnow():
        raise AppError(409, "Cette offre est expirée.", "JOB_EXPIRED")


def _company_for_user(db: Session, user: User, company_id: str | None) -> Company:
    if user.role == UserRole.EMPLOYER:
        if company_id:
            if not user_belongs_to_company(db, user, company_id):
                raise AppError(403, "Vous n'avez pas accès à cette entreprise.", "FORBIDDEN")
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
    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    return company


def create_job(db: Session, user: User, data: JobIn, ip: str | None = None) -> JobOffer:
    if user.role == UserRole.EMPLOYER:
        raise AppError(
            403,
            "Vous transmettez un besoin de recrutement ; Talendus crée et publie l'offre.",
            "JOB_STAFF_ONLY",
        )
    company = _company_for_user(db, user, data.company_id)
    job = JobOffer(
        company_id=company.id,
        recruiter_id=user.id if user.role in {UserRole.RECRUITER} | ADMINS else None,
        slug=_unique_slug(db, data.slug or data.title),
        title=data.title,
        description=data.description,
        responsibilities=data.responsibilities,
        qualifications=data.qualifications,
        location=data.location,
        sector=data.sector,
        contract_type=data.contract_type,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        salary_display=data.salary_display,
        skills=data.skills,
        experience_level=data.experience_level,
        education_required=data.education_required,
        certifications=data.certifications,
        shift=data.shift,
        schedule=data.schedule,
        work_mode=data.work_mode,
        languages=data.languages,
        overtime=data.overtime,
        driver_license=data.driver_license,
        unionized=data.unionized,
        travel=data.travel,
        work_authorization=data.work_authorization or "ouvert",
        can_sponsor=bool(data.can_sponsor),
        benefits=data.benefits,
        currency=getattr(data, "currency", None) or "CAD",
        openings=getattr(data, "openings", None) or 1,
        start_date=getattr(data, "start_date", None),
        expires_at=_parse_expires(getattr(data, "expires_at", None)),
        status=JobStatus.DRAFT,
    )
    db.add(job)
    db.flush()
    from app.integrations.hooks import apply_coordinates, maybe_geocode

    apply_coordinates(job, maybe_geocode(job.location))
    audit(db, "job.create", user, "job", job.id, ip)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, user: User, job_id: str, data: JobIn | JobPatchIn) -> JobOffer:
    job = db.get(JobOffer, job_id)
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    _assert_can_write(db, user, job)
    payload = data.model_dump(exclude_unset=True, exclude={"company_id", "slug"})
    if "expires_at" in payload:
        payload["expires_at"] = _parse_expires(payload.get("expires_at"))
    for key, value in payload.items():
        setattr(job, key, value)
    if data.slug:
        job.slug = _unique_slug(db, data.slug, job.id)
    from app.integrations.hooks import apply_coordinates, maybe_geocode

    if "location" in payload:
        apply_coordinates(job, maybe_geocode(job.location))
    audit(db, "job.update", user, "job", job.id)
    db.commit()
    db.refresh(job)
    return job


def set_job_status(db: Session, user: User, job_id: str, status: JobStatus) -> JobOffer:
    job = db.get(JobOffer, job_id)
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    _assert_can_write(db, user, job)
    job.status = status
    if status == JobStatus.PUBLISHED:
        job.published_at = job.published_at or utcnow()
        from app.services.matching import notify_job_matches

        notify_job_matches(db, job)
    audit(db, f"job.{status.value.lower()}", user, "job", job.id)
    db.commit()
    db.refresh(job)
    return job


def list_managed(db: Session, user: User) -> list[JobOffer]:
    stmt = select(JobOffer).options(joinedload(JobOffer.company))
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(JobOffer.company_id.in_(ids))
    return list(db.scalars(stmt.order_by(JobOffer.updated_at.desc())).unique().all())


def get_managed_job(db: Session, user: User, job_id: str) -> JobOffer:
    job = db.scalar(select(JobOffer).options(joinedload(JobOffer.company)).where(JobOffer.id == job_id))
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    _assert_can_manage(db, user, job)
    return job


def duplicate_job(db: Session, user: User, job_id: str) -> JobOffer:
    source = get_managed_job(db, user, job_id)
    _assert_can_write(db, user, source)
    copy = JobOffer(
        company_id=source.company_id,
        recruiter_id=source.recruiter_id,
        slug=_unique_slug(db, f"{source.slug}-copie"),
        title=f"{source.title} (copie)",
        description=source.description,
        responsibilities=source.responsibilities,
        qualifications=source.qualifications,
        location=source.location,
        lat=source.lat,
        lng=source.lng,
        place_id=source.place_id,
        sector=source.sector,
        contract_type=source.contract_type,
        salary_min=source.salary_min,
        salary_max=source.salary_max,
        salary_display=source.salary_display,
        currency=source.currency,
        openings=source.openings,
        skills=source.skills,
        experience_level=source.experience_level,
        education_required=source.education_required,
        certifications=source.certifications,
        shift=source.shift,
        schedule=source.schedule,
        work_mode=source.work_mode,
        languages=source.languages,
        overtime=source.overtime,
        driver_license=source.driver_license,
        unionized=source.unionized,
        travel=source.travel,
        work_authorization=source.work_authorization,
        can_sponsor=bool(source.can_sponsor),
        benefits=source.benefits,
        status=JobStatus.DRAFT,
        start_date=source.start_date,
    )
    db.add(copy)
    db.flush()
    audit(db, "job.duplicate", user, "job", copy.id)
    db.commit()
    db.refresh(copy)
    return copy


def delete_job(db: Session, user: User, job_id: str) -> None:
    job = get_managed_job(db, user, job_id)
    _assert_can_write(db, user, job)
    if job.status == JobStatus.PUBLISHED:
        raise AppError(400, "Archivez l'offre publiée avant de la supprimer.", "JOB_PUBLISHED")
    db.delete(job)
    audit(db, "job.delete", user, "job", job_id)
    db.commit()


def _assert_can_manage(db: Session, user: User, job: JobOffer) -> None:
    if user.role in {UserRole.RECRUITER} | ADMINS:
        return
    if user.role == UserRole.EMPLOYER:
        if user_belongs_to_company(db, user, job.company_id):
            return
    raise AppError(403, "Vous ne pouvez pas consulter cette offre.", "FORBIDDEN")


def _assert_can_write(db: Session, user: User, job: JobOffer) -> None:
    if user.role in {UserRole.RECRUITER} | ADMINS:
        return
    raise AppError(
        403,
        "Talendus crée, publie et gère les offres. L'entreprise transmet un besoin de recrutement.",
        "JOB_STAFF_ONLY",
    )
