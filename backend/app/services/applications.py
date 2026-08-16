from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import Application, ApplicationStatusHistory, Candidate, JobOffer, Resume, User
from app.rbac import ADMINS
from app.models.enums import (
    ApplicationStatus,
    EmailType,
    NotificationType,
    UserRole,
)
from app.schemas import ApplicationCreateIn, PublicApplyIn
from app.security import hash_password, random_password
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.email import send_email
from app.services.jobs import assert_job_open, get_public_job
from app.services.notifications import notify
from app.services.pipeline import stage_for


def _history(db: Session, application: Application, old: str | None, new: str, actor: User | None, comment: str | None = None) -> None:
    db.add(
        ApplicationStatusHistory(
            application_id=application.id,
            old_status=old,
            new_status=new,
            actor_id=actor.id if actor else None,
            comment=comment,
        )
    )


def _primary_resume(db: Session, candidate: Candidate, resume_id: str | None) -> Resume | None:
    if resume_id:
        resume = db.get(Resume, resume_id)
        if not resume or resume.candidate_id != candidate.id:
            raise AppError(400, "CV invalide pour ce candidat.", "INVALID_RESUME")
        return resume
    return db.scalar(select(Resume).where(Resume.candidate_id == candidate.id, Resume.is_primary.is_(True)))


def apply(db: Session, user: User, data: ApplicationCreateIn, ip: str | None = None) -> Application:
    candidate = ensure_candidate(db, user)
    job = None
    if data.job_id:
        job = db.get(JobOffer, data.job_id)
    elif data.job_slug:
        job = db.scalar(select(JobOffer).where(JobOffer.slug == data.job_slug))
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    assert_job_open(job)
    existing = db.scalar(
        select(Application).where(Application.candidate_id == candidate.id, Application.job_id == job.id)
    )
    if existing:
        raise AppError(409, "Une candidature existe déjà pour cette offre.", "APPLICATION_ALREADY_EXISTS")
    resume = _primary_resume(db, candidate, data.resume_id)
    from app.services.matching import score_pair

    score, _reasons = score_pair(candidate, job)
    application = Application(
        candidate_id=candidate.id,
        job_id=job.id,
        resume_id=resume.id if resume else None,
        status=ApplicationStatus.SUBMITTED,
        cover_note=data.cover_note,
        source="site",
        match_score=score,
    )
    db.add(application)
    db.flush()
    _history(db, application, None, ApplicationStatus.SUBMITTED.value, user)
    staff = None
    if job.recruiter_id:
        staff = db.get(User, job.recruiter_id)
    notify(
        db, staff, NotificationType.APPLICATION_NEW,
        "Nouvelle candidature",
        f"{user.full_name} a postulé pour {job.title}.",
        href=f"/admin/#/jobs/{job.id}",
    )
    if staff:
        send_email(
            db, staff.email, EmailType.NEW_APPLICATION_RECRUITER, "new_application",
            job_title=job.title, candidate_name=user.full_name, candidate_email=user.email,
        )
    send_email(
        db, user.email, EmailType.APPLICATION_CONFIRMATION, "application_confirm",
        name=user.first_name, job_title=job.title,
    )
    from app.integrations.hooks import maybe_send_whatsapp

    maybe_send_whatsapp(
        recipient=user.phone,
        template="application_confirm",
        variables={"name": user.first_name or "", "job": job.title},
    )
    if staff:
        maybe_send_whatsapp(
            recipient=staff.phone,
            template="employer_notice",
            variables={"candidate": user.full_name, "job": job.title},
        )
    notify(db, user, NotificationType.APPLICATION_NEW, "Candidature envoyée", f"Votre candidature pour {job.title} a été transmise.", href="/espace.html#/applications")
    audit(db, "application.create", user, "application", application.id, ip, {"job_id": job.id})
    db.commit()
    db.refresh(application)
    return application


def apply_public(db: Session, data: PublicApplyIn, ip: str | None = None) -> Application:
    job = get_public_job(db, data.job_slug)
    assert_job_open(job)
    email = data.email.lower()
    user = db.scalar(select(User).where(User.email == email))
    if user:
        if user.role != UserRole.CANDIDATE:
            raise AppError(409, "Ce courriel est déjà utilisé par un autre type de compte.", "EMAIL_TAKEN")
        if data.password:
            from app.security import verify_password
            if not verify_password(data.password, user.password_hash):
                raise AppError(401, "Compte existant : mot de passe incorrect.", "INVALID_CREDENTIALS")
    else:
        password = data.password or random_password()
        parts = (data.last_name or "").split(" ", 1)
        last = data.last_name or (parts[0] if parts else "")
        user = User(
            email=email,
            password_hash=hash_password(password),
            first_name=data.first_name.strip(),
            last_name=last.strip(),
            phone=data.phone,
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.flush()
        from app.models import UserPreference

        db.add(UserPreference(user_id=user.id))
        db.add(Candidate(user_id=user.id, city=None, title=None))
        send_email(db, user.email, EmailType.WELCOME, "welcome", name=user.first_name, link=f"{job.title}")
    payload = ApplicationCreateIn(job_slug=data.job_slug, cover_note=data.cover_note or data.cv_url)
    return apply(db, user, payload, ip)


def list_own(db: Session, user: User) -> list[Application]:
    candidate = ensure_candidate(db, user)
    return list(
        db.scalars(
            select(Application)
            .options(joinedload(Application.job).joinedload(JobOffer.company))
            .where(Application.candidate_id == candidate.id)
            .order_by(Application.created_at.desc())
        ).unique().all()
    )


def get_application(db: Session, user: User, application_id: str) -> Application:
    app_row = db.scalar(
        select(Application)
        .options(
            joinedload(Application.job).joinedload(JobOffer.company),
            joinedload(Application.candidate).joinedload(Candidate.user),
            joinedload(Application.history),
        )
        .where(Application.id == application_id)
    )
    if not app_row:
        raise AppError(404, "Candidature introuvable.", "APPLICATION_NOT_FOUND")
    if user.role == UserRole.CANDIDATE:
        cand = ensure_candidate(db, user)
        if app_row.candidate_id != cand.id:
            raise AppError(403, "Vous n'avez pas accès à cette candidature.", "FORBIDDEN")
    elif user.role == UserRole.EMPLOYER:
        from app.services.access import user_belongs_to_company

        if not user_belongs_to_company(db, user, app_row.job.company_id):
            raise AppError(403, "Vous n'avez pas accès à cette candidature.", "FORBIDDEN")
    elif user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès à cette candidature.", "FORBIDDEN")
    return app_row


def change_status(db: Session, user: User, application_id: str, status: ApplicationStatus, comment: str | None) -> Application:
    application = get_application(db, user, application_id)
    if user.role == UserRole.CANDIDATE:
        if status != ApplicationStatus.WITHDRAWN:
            raise AppError(403, "Un candidat ne peut que retirer sa candidature.", "FORBIDDEN")
    old = application.status.value
    application.status = status
    _history(db, application, old, status.value, user, comment)
    candidate_user = application.candidate.user
    ntype = NotificationType.APPLICATION_STATUS
    if status == ApplicationStatus.HIRED:
        ntype = NotificationType.APPLICATION_ACCEPTED
    elif status == ApplicationStatus.REJECTED:
        ntype = NotificationType.APPLICATION_REJECTED
    elif status == ApplicationStatus.INTERVIEW:
        ntype = NotificationType.INTERVIEW_INVITE
    notify(
        db, candidate_user, ntype,
        "Mise à jour de candidature",
        f"{application.job.title} : {status.value}",
        href="/espace.html#/applications/" + application.id,
    )
    template = "interview" if status == ApplicationStatus.INTERVIEW else "application_status"
    send_email(
        db, candidate_user.email,
        EmailType.INTERVIEW_INVITE if status == ApplicationStatus.INTERVIEW else EmailType.APPLICATION_STATUS,
        template,
        name=candidate_user.first_name, job_title=application.job.title, status=status.value, comment=comment or "",
    )
    from app.integrations.hooks import maybe_send_whatsapp

    wa_template = "interview_invite" if status == ApplicationStatus.INTERVIEW else "application_status"
    maybe_send_whatsapp(
        recipient=candidate_user.phone,
        template=wa_template,
        variables={"name": candidate_user.first_name or "", "job": application.job.title, "status": status.value},
    )
    audit(
        db,
        "application.status",
        user,
        "application",
        application.id,
        metadata={"from": old, "to": status.value},
        old_value=old,
        new_value=status.value,
    )
    db.commit()
    db.refresh(application)
    return application


def list_inbox(db: Session, user: User, job_id: str | None = None) -> list[Application]:
    stmt = (
        select(Application)
        .options(
            joinedload(Application.job).joinedload(JobOffer.company),
            joinedload(Application.candidate).joinedload(Candidate.user),
            joinedload(Application.history),
        )
        .join(JobOffer)
    )
    if user.role == UserRole.EMPLOYER:
        from app.services.access import company_ids_for_employer

        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(JobOffer.company_id.in_(ids))
    elif user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux candidatures.", "FORBIDDEN")
    if job_id:
        stmt = stmt.where(Application.job_id == job_id)
    return list(db.scalars(stmt.order_by(Application.created_at.desc())).unique().all())


def serialize_application(row: Application, viewer: User | None = None) -> dict:
    include_staff = viewer is not None and viewer.role != UserRole.CANDIDATE
    hide_internal = viewer is None or viewer.role == UserRole.CANDIDATE
    payload = {
        "id": row.id,
        "status": row.status.value,
        "cover_note": row.cover_note,
        "source": row.source,
        "match_score": row.match_score,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        "job": {
            "id": row.job.id,
            "slug": row.job.slug,
            "title": row.job.title,
            "location": row.job.location,
            "company_name": row.job.company.name if row.job.company else None,
            "sector": row.job.sector,
            "contract_type": row.job.contract_type,
        },
        "resume_id": row.resume_id,
        "pipeline_stage": stage_for(row.status),
        "history": [
            {
                "old_status": h.old_status,
                "new_status": h.new_status,
                "comment": None if hide_internal else h.comment,
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "actor_id": None if hide_internal else h.actor_id,
            }
            for h in (row.history or [])
        ],
    }
    if include_staff:
        payload["staff_notes"] = row.staff_notes
        if row.candidate and row.candidate.user:
            payload["candidate"] = {
                "id": row.candidate.id,
                "first_name": row.candidate.user.first_name,
                "last_name": row.candidate.user.last_name,
                "email": row.candidate.user.email if viewer and viewer.role != UserRole.EMPLOYER else None,
                "title": row.candidate.title,
                "city": row.candidate.city,
                "skills": row.candidate.skills,
                "years_experience": row.candidate.years_experience,
            }
    return payload
