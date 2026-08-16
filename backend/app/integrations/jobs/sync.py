"""Import et déduplication d'offres externes (source + external_id)."""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.integrations.errors import IntegrationError
from app.integrations.jobs.base import ExternalJobPayload
from app.integrations.jobs.indeed import IndeedService
from app.integrations.jobs.linkedin import LinkedInService
from app.integrations.logging import persist_call
from app.models.enums import utcnow
from app.models.integrations import ExternalJob

PROVIDERS = {
    "linkedin": LinkedInService,
    "indeed": IndeedService,
}


def serialize_external_job(row: ExternalJob) -> dict:
    return {
        "id": row.id,
        "externalId": row.external_id,
        "source": row.source,
        "title": row.title,
        "company": row.company,
        "description": row.description,
        "location": row.location,
        "salary": row.salary,
        "employmentType": row.employment_type,
        "originalUrl": row.original_url,
        "publishedAt": row.published_at,
        "importedAt": row.imported_at.isoformat() if row.imported_at else None,
        "lastSyncedAt": row.last_synced_at.isoformat() if row.last_synced_at else None,
        "status": row.status,
    }


def _hash_payload(job: ExternalJobPayload) -> str:
    raw = json.dumps(
        {
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "url": job.original_url,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def upsert_jobs(db: Session, jobs: list[ExternalJobPayload]) -> dict:
    created = updated = skipped = 0
    now = utcnow()
    for job in jobs:
        if not job.external_id or not job.source or not job.title:
            skipped += 1
            continue
        fingerprint = _hash_payload(job)
        existing = db.scalar(
            select(ExternalJob).where(ExternalJob.source == job.source, ExternalJob.external_id == job.external_id)
        )
        if existing is None:
            db.add(
                ExternalJob(
                    external_id=job.external_id,
                    source=job.source,
                    title=job.title,
                    company=job.company,
                    description=job.description,
                    location=job.location,
                    salary=job.salary,
                    employment_type=job.employment_type,
                    original_url=job.original_url,
                    published_at=job.published_at,
                    imported_at=now,
                    last_synced_at=now,
                    status="imported",
                    raw_hash=fingerprint,
                )
            )
            created += 1
            continue
        if existing.raw_hash == fingerprint:
            existing.last_synced_at = now
            skipped += 1
            continue
        existing.title = job.title
        existing.company = job.company
        existing.description = job.description
        existing.location = job.location
        existing.salary = job.salary
        existing.employment_type = job.employment_type
        existing.original_url = job.original_url
        existing.published_at = job.published_at
        existing.last_synced_at = now
        existing.status = "updated"
        existing.raw_hash = fingerprint
        updated += 1
    db.commit()
    persist_call(
        provider="jobs",
        operation="upsert",
        success=True,
        status_code=200,
        error_code=None,
    )
    return {"created": created, "updated": updated, "skipped": skipped, "total": created + updated + skipped}


def sync_from_provider(db: Session, source: str, query: str | None = None) -> dict:
    cls = PROVIDERS.get(source)
    if cls is None:
        raise IntegrationError("Source d'offres inconnue.", "INTEGRATION_NOT_FOUND", provider=source)
    jobs = cls().fetch_jobs(query)
    result = upsert_jobs(db, jobs)
    result["source"] = source
    return result


def list_external_jobs(db: Session, source: str | None = None, limit: int = 50) -> list[ExternalJob]:
    stmt = select(ExternalJob).order_by(ExternalJob.imported_at.desc()).limit(limit)
    if source:
        stmt = stmt.where(ExternalJob.source == source)
    return list(db.scalars(stmt).all())
