from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import (
    Application,
    Candidate,
    Company,
    CompanyMembership,
    Interview,
    JobOffer,
    Notification,
    PortalDocument,
    SavedJob,
    User,
)
from app.models.enums import ApplicationStatus, InterviewStatus, JobStatus, NotificationType, PUBLIC_JOB_STATUSES, UserRole, utcnow
from app.rbac import is_admin
from app.schemas import CompanyMemberIn, CompanyMemberPatchIn
from app.services.access import (
    CLIENT_INTERVIEW_TYPES,
    PRESENTED_STATUSES,
    company_ids_for_employer,
    first_employer_company,
    is_presented_to_employer,
    member_role_for,
    require_company_perm,
)
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.jobs import lookup_job, serialize_job
from app.services.notifications import notify
from app.services.storage import delete_stored, save_bytes

IN_PROGRESS = {
    ApplicationStatus.SUBMITTED,
    ApplicationStatus.RECEIVED,
    ApplicationStatus.UNDER_REVIEW,
    ApplicationStatus.SHORTLISTED,
    ApplicationStatus.INTERVIEW,
    ApplicationStatus.SECOND_INTERVIEW,
    ApplicationStatus.OFFER_SENT,
}
DOC_KINDS = {"cover_letter", "certification", "other", "contract", "mission", "company"}


def profile_completeness(profile: Candidate) -> dict:
    user = profile.user
    checks = {
        "name": bool(user and user.first_name and user.last_name),
        "phone": bool(user and user.phone),
        "photo": bool(user and user.avatar_path),
        "city": bool(profile.city),
        "address": bool(profile.address),
        "title": bool(profile.title),
        "bio": bool((profile.bio or "").strip()),
        "skills": bool((profile.skills or "").strip()),
        "experience": bool(profile.experiences),
        "education": bool(profile.education),
        "resume": bool(profile.resumes),
        "availability": bool(profile.availability),
        "languages": bool((profile.languages or "").strip()),
        "contract": bool(profile.contract_type),
        "work_status": bool(profile.work_status),
    }
    filled = sum(1 for value in checks.values() if value)
    percent = round(100 * filled / len(checks)) if checks else 0
    return {
        "percent": percent,
        "checks": checks,
        "missing": [key for key, value in checks.items() if not value],
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


def candidate_dashboard(db: Session, user: User) -> dict:
    profile = ensure_candidate(db, user)
    profile = db.scalar(
        select(Candidate)
        .options(
            joinedload(Candidate.user),
            joinedload(Candidate.experiences),
            joinedload(Candidate.education),
            joinedload(Candidate.resumes),
        )
        .where(Candidate.id == profile.id)
    )
    completeness = profile_completeness(profile)
    apps = list(db.scalars(select(Application).where(Application.candidate_id == profile.id)).all())
    interviews = list(
        db.scalars(
            select(Interview).where(
                Interview.candidate_id == profile.id,
                Interview.status.in_([InterviewStatus.SCHEDULED, InterviewStatus.CONFIRMED]),
                Interview.scheduled_at >= utcnow(),
            )
        ).all()
    )
    unread = db.scalar(
        select(func.count()).select_from(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))
    ) or 0
    recent = list(
        db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(5)).all()
    )
    from app.services.matching import jobs_for_candidate
    from app.services.notifications import serialize_notification

    matches = jobs_for_candidate(db, profile, limit=4)
    return {
        "first_name": user.first_name,
        "completeness": completeness,
        "stats": {
            "applications": len(apps),
            "in_progress": sum(1 for a in apps if a.status in IN_PROGRESS),
            "interviews": len(interviews),
            "accepted": sum(1 for a in apps if a.status == ApplicationStatus.HIRED),
            "saved_jobs": db.scalar(select(func.count()).select_from(SavedJob).where(SavedJob.user_id == user.id)) or 0,
            "unread_notifications": int(unread),
        },
        "notifications": [serialize_notification(n) for n in recent],
        "matches": matches,
    }


def employer_dashboard(db: Session, user: User) -> dict:
    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    ids = company_ids_for_employer(db, user)
    jobs = list(db.scalars(select(JobOffer).where(JobOffer.company_id.in_(ids))).all()) if ids else []
    job_ids = [j.id for j in jobs]
    apps = []
    if job_ids:
        apps = list(db.scalars(select(Application).where(Application.job_id.in_(job_ids))).all())
        apps = [a for a in apps if a.status in PRESENTED_STATUSES]
    interviews = []
    if ids:
        interviews = list(
            db.scalars(
                select(Interview).where(
                    Interview.company_id.in_(ids),
                    Interview.type.in_(CLIENT_INTERVIEW_TYPES),
                    Interview.status.in_([InterviewStatus.SCHEDULED, InterviewStatus.CONFIRMED]),
                )
            ).all()
        )
    unread = db.scalar(
        select(func.count()).select_from(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))
    ) or 0
    from app.services.notifications import serialize_notification

    recent = list(
        db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(6)).all()
    )
    return {
        "company_name": company.name,
        "company_id": company.id,
        "member_role": member_role_for(db, user, company.id).value if member_role_for(db, user, company.id) else None,
        "stats": {
            "active_jobs": sum(1 for j in jobs if j.status == JobStatus.PUBLISHED),
            "applications": len(apps),
            "shortlisted": sum(1 for a in apps if a.status == ApplicationStatus.SHORTLISTED),
            "interviews": len(interviews),
            "hired": sum(1 for a in apps if a.status == ApplicationStatus.HIRED),
            "unread_notifications": int(unread),
        },
        "notifications": [serialize_notification(n) for n in recent],
        "recent_jobs": [
            {"id": j.id, "title": j.title, "status": j.status.value, "updated_at": j.updated_at.isoformat() if j.updated_at else None}
            for j in sorted(jobs, key=lambda x: x.updated_at or utcnow(), reverse=True)[:5]
        ],
    }


def list_saved_jobs(db: Session, user: User) -> list[dict]:
    rows = list(
        db.scalars(
            select(SavedJob)
            .options(joinedload(SavedJob.job).joinedload(JobOffer.company))
            .where(SavedJob.user_id == user.id)
            .order_by(SavedJob.created_at.desc())
        )
        .unique()
        .all()
    )
    out = []
    for row in rows:
        if not row.job:
            continue
        payload = serialize_job(row.job)
        payload["saved"] = True
        payload["saved_at"] = row.created_at.isoformat() if row.created_at else None
        payload["available"] = row.job.status in PUBLIC_JOB_STATUSES
        out.append(payload)
    return out


def _job_for_bookmark(db: Session, job_id: str) -> JobOffer | None:
    job = lookup_job(db, job_id)
    if job:
        return job
    from app.site_jobs import ensure_catalog_job, is_site_job_slug

    if is_site_job_slug(job_id):
        return ensure_catalog_job(db, job_id)
    return None


def save_job(db: Session, user: User, job_id: str) -> dict:
    if user.role != UserRole.CANDIDATE:
        raise AppError(403, "Seuls les candidats peuvent sauvegarder une offre.", "FORBIDDEN")
    job = _job_for_bookmark(db, job_id)
    if not job or job.status not in PUBLIC_JOB_STATUSES:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    existing = db.scalar(select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == job.id))
    if existing:
        return {"id": existing.id, "job_id": job.id, "saved": True}
    row = SavedJob(user_id=user.id, job_id=job.id)
    db.add(row)
    audit(db, "job.save", user, "job", job.id)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "job_id": job.id, "saved": True}


def unsave_job(db: Session, user: User, job_id: str) -> dict:
    job = _job_for_bookmark(db, job_id)
    real_id = job.id if job else job_id
    row = db.scalar(select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == real_id))
    if row:
        db.delete(row)
        audit(db, "job.unsave", user, "job", real_id)
        db.commit()
    return {"job_id": real_id, "saved": False}


def saved_job_ids(db: Session, user: User, job_ids: list[str]) -> set[str]:
    if not job_ids:
        return set()
    rows = db.scalars(select(SavedJob.job_id).where(SavedJob.user_id == user.id, SavedJob.job_id.in_(job_ids))).all()
    return set(rows)


def serialize_document(row: PortalDocument) -> dict:
    return {
        "id": row.id,
        "kind": row.kind,
        "original_name": row.original_name,
        "mime_type": row.mime_type,
        "size_bytes": row.size_bytes,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "download_path": f"/api/documents/{row.id}/file",
    }


def _owner_for_user(db: Session, user: User, owner_type: str | None = None) -> tuple[str, str]:
    if owner_type == "company" or user.role == UserRole.EMPLOYER:
        company = first_employer_company(db, user)
        if not company:
            raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
        return "company", company.id
    profile = ensure_candidate(db, user)
    return "candidate", profile.id


def list_documents(db: Session, user: User, owner_type: str | None = None) -> list[dict]:
    otype, oid = _owner_for_user(db, user, owner_type)
    rows = list(
        db.scalars(
            select(PortalDocument)
            .where(PortalDocument.owner_type == otype, PortalDocument.owner_id == oid)
            .order_by(PortalDocument.created_at.desc())
        ).all()
    )
    return [serialize_document(r) for r in rows]


def list_documents_for_owner(db: Session, owner_type: str, owner_id: str) -> list[PortalDocument]:
    return list(
        db.scalars(
            select(PortalDocument)
            .where(PortalDocument.owner_type == owner_type, PortalDocument.owner_id == owner_id)
            .order_by(PortalDocument.created_at.desc())
        ).all()
    )


def list_all_documents(db: Session) -> list[PortalDocument]:
    return list(db.scalars(select(PortalDocument).order_by(PortalDocument.created_at.desc())).all())


def staff_upload_document(
    db: Session,
    user: User,
    data: bytes,
    filename: str,
    kind: str,
    owner_type: str,
    owner_id: str,
) -> PortalDocument:
    if user.role not in {UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE}:
        raise AppError(403, "Téléversement réservé à l’équipe Talendus.", "FORBIDDEN")
    kind = (kind or "other").strip().lower()
    if kind not in DOC_KINDS:
        kind = "other"
    otype = (owner_type or "candidate").strip().lower()
    if otype not in {"candidate", "company"}:
        raise AppError(400, "Type de dossier invalide.", "VALIDATION_ERROR")
    if otype == "candidate":
        owner = db.get(Candidate, owner_id)
        if not owner:
            raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    else:
        owner = db.get(Company, owner_id)
        if not owner:
            raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    original, stored, mime, size, url = save_bytes(data, filename, category="documents")
    row = PortalDocument(
        owner_type=otype,
        owner_id=owner_id,
        kind=kind,
        original_name=original,
        stored_name=stored,
        storage_url=url,
        mime_type=mime,
        size_bytes=size,
        created_by=user.id,
    )
    db.add(row)
    audit(db, "document.staff_upload", user, "document", None, metadata={"kind": kind, "owner": otype})
    db.commit()
    db.refresh(row)
    return row


def upload_document(db: Session, user: User, data: bytes, filename: str, kind: str, owner_type: str | None = None) -> PortalDocument:
    kind = (kind or "other").strip().lower()
    if kind not in DOC_KINDS:
        kind = "other"
    otype, oid = _owner_for_user(db, user, owner_type)
    if otype == "company":
        require_company_perm(db, user, oid, "documents:write")
    original, stored, mime, size, url = save_bytes(data, filename, category="documents")
    row = PortalDocument(
        owner_type=otype,
        owner_id=oid,
        kind=kind,
        original_name=original,
        stored_name=stored,
        storage_url=url,
        mime_type=mime,
        size_bytes=size,
        created_by=user.id,
    )
    db.add(row)
    notify(db, user, NotificationType.DOCUMENT_ADDED, "Document ajouté", original)
    audit(db, "document.upload", user, "document", None, metadata={"kind": kind})
    db.commit()
    db.refresh(row)
    return row


def get_document_for_user(db: Session, user: User, document_id: str) -> PortalDocument:
    row = db.get(PortalDocument, document_id)
    if not row:
        raise AppError(404, "Document introuvable.", "DOCUMENT_NOT_FOUND")
    if is_admin(user) or user.role == UserRole.RECRUITER:
        return row
    if row.owner_type == "candidate":
        if user.role == UserRole.CANDIDATE:
            profile = ensure_candidate(db, user)
            if row.owner_id == profile.id:
                return row
        if user.role == UserRole.EMPLOYER:
            ids = company_ids_for_employer(db, user)
            if ids:
                linked = list(
                    db.scalars(
                        select(Application)
                        .options(joinedload(Application.history))
                        .join(Candidate, Application.candidate_id == Candidate.id)
                        .join(JobOffer, Application.job_id == JobOffer.id)
                        .where(Candidate.id == row.owner_id, JobOffer.company_id.in_(ids))
                    )
                    .unique()
                    .all()
                )
                if any(is_presented_to_employer(item) for item in linked):
                    return row
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    if row.owner_type == "company":
        if user.role == UserRole.EMPLOYER and row.owner_id in company_ids_for_employer(db, user):
            return row
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")


def delete_document(db: Session, user: User, document_id: str) -> None:
    row = get_document_for_user(db, user, document_id)
    if user.role == UserRole.EMPLOYER and row.owner_type == "company":
        require_company_perm(db, user, row.owner_id, "documents:write")
    elif user.role == UserRole.CANDIDATE:
        profile = ensure_candidate(db, user)
        if row.owner_id != profile.id:
            raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    elif not (is_admin(user) or user.role == UserRole.RECRUITER or user.role == UserRole.CANDIDATE):
        raise AppError(403, "Vous n'avez pas accès à ce fichier.", "FORBIDDEN")
    delete_stored(row.stored_name, row.storage_url, "documents")
    db.delete(row)
    audit(db, "document.delete", user, "document", document_id)
    db.commit()


def set_avatar(db: Session, user: User, data: bytes, filename: str) -> User:
    original, stored, mime, size, url = save_bytes(data, filename, category="avatars", kind="image", max_mb=2)
    if user.avatar_path:
        delete_stored(_basename(user.avatar_path), None, "avatars")
    user.avatar_path = stored
    audit(db, "user.avatar", user, "user", user.id)
    db.commit()
    db.refresh(user)
    return user


def _basename(path: str) -> str:
    return Path(path).name


def set_company_logo(db: Session, user: User, company_id: str, data: bytes, filename: str) -> Company:
    company = require_company_perm(db, user, company_id, "company:write")
    original, stored, mime, size, url = save_bytes(data, filename, category="logos", kind="image", max_mb=2)
    if company.logo_path:
        delete_stored(_basename(company.logo_path), None, "logos")
    company.logo_path = stored
    audit(db, "company.logo", user, "company", company.id)
    db.commit()
    db.refresh(company)
    return company


def list_members(db: Session, user: User) -> list[dict]:
    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    require_company_perm(db, user, company.id, "company:read")
    rows = list(
        db.scalars(
            select(CompanyMembership)
            .options(joinedload(CompanyMembership.user))
            .where(CompanyMembership.company_id == company.id)
            .order_by(CompanyMembership.created_at.asc())
        )
        .unique()
        .all()
    )
    return [
        {
            "id": row.id,
            "user_id": row.user_id,
            "member_role": row.member_role.value,
            "first_name": row.user.first_name if row.user else "",
            "last_name": row.user.last_name if row.user else "",
            "email": row.user.email if row.user else "",
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]


def invite_member(db: Session, user: User, data: CompanyMemberIn) -> dict:
    from app.models import UserPreference
    from app.security import hash_password, random_password

    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    require_company_perm(db, user, company.id, "members:manage")
    actor = member_role_for(db, user, company.id)
    if data.member_role.value == "OWNER" and (actor is None or actor.value != "OWNER"):
        raise AppError(403, "Seul le propriétaire peut nommer un autre propriétaire.", "FORBIDDEN")
    existing = db.scalar(select(User).where(User.email == str(data.email).lower()))
    password = data.password or random_password()
    if existing:
        if existing.role != UserRole.EMPLOYER:
            raise AppError(409, "Ce courriel appartient à un autre type de compte.", "EMAIL_TAKEN")
        if membership_exists(db, company.id, existing.id):
            raise AppError(409, "Cet utilisateur fait déjà partie de l'entreprise.", "MEMBER_EXISTS")
        member_user = existing
    else:
        member_user = User(
            email=str(data.email).lower(),
            password_hash=hash_password(password),
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            role=UserRole.EMPLOYER,
        )
        db.add(member_user)
        db.flush()
        db.add(UserPreference(user_id=member_user.id))
    row = CompanyMembership(company_id=company.id, user_id=member_user.id, member_role=data.member_role)
    db.add(row)
    audit(db, "company.member_invite", user, "company", company.id, metadata={"user_id": member_user.id})
    db.commit()
    db.refresh(row)
    return {"id": row.id, "user_id": member_user.id, "member_role": row.member_role.value}


def membership_exists(db: Session, company_id: str, user_id: str) -> bool:
    return db.scalar(
        select(CompanyMembership.id).where(CompanyMembership.company_id == company_id, CompanyMembership.user_id == user_id)
    ) is not None


def patch_member(db: Session, user: User, membership_id: str, data: CompanyMemberPatchIn) -> dict:
    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    require_company_perm(db, user, company.id, "members:manage")
    row = db.get(CompanyMembership, membership_id)
    if not row or row.company_id != company.id:
        raise AppError(404, "Membre introuvable.", "MEMBER_NOT_FOUND")
    if row.member_role.value == "OWNER" and data.member_role.value != "OWNER":
        owners = db.scalar(
            select(func.count())
            .select_from(CompanyMembership)
            .where(CompanyMembership.company_id == company.id, CompanyMembership.member_role == row.member_role.__class__.OWNER)
        ) or 0
        if owners <= 1:
            raise AppError(400, "L'entreprise doit conserver un propriétaire.", "LAST_OWNER")
    row.member_role = data.member_role
    audit(db, "company.member_role", user, "company", company.id)
    db.commit()
    return {"id": row.id, "member_role": row.member_role.value}


def remove_member(db: Session, user: User, membership_id: str) -> None:
    company = first_employer_company(db, user)
    if not company:
        raise AppError(404, "Aucune entreprise associée.", "NO_COMPANY")
    require_company_perm(db, user, company.id, "members:manage")
    row = db.get(CompanyMembership, membership_id)
    if not row or row.company_id != company.id:
        raise AppError(404, "Membre introuvable.", "MEMBER_NOT_FOUND")
    if row.user_id == user.id:
        raise AppError(400, "Vous ne pouvez pas retirer votre propre accès ici.", "FORBIDDEN")
    if row.member_role.value == "OWNER":
        raise AppError(400, "Impossible de retirer le propriétaire.", "FORBIDDEN")
    db.delete(row)
    audit(db, "company.member_remove", user, "company", company.id)
    db.commit()
