from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import Application, Candidate, Company, Interview, JobOffer, User
from app.models.enums import EmailType, InterviewStatus, InterviewType, NotificationType, UserRole
from app.rbac import ADMINS
from app.schemas import InterviewIn, InterviewPatchIn
from app.services.access import company_ids_for_employer
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.email import send_email
from app.services.notifications import notify

TYPE_LABEL = {
    InterviewType.TALENDUS: "Talendus",
    InterviewType.CLIENT: "Client",
    InterviewType.PHONE: "Téléphone",
    InterviewType.VIDEO: "Visio",
    InterviewType.ONSITE: "Sur place",
    InterviewType.OFFER: "Offre",
}


def _parse_when(value: str) -> datetime:
    raw = (value or "").strip().replace("Z", "+00:00")
    if "T" not in raw and " " in raw:
        raw = raw.replace(" ", "T")
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise AppError(400, "Date d'entretien invalide.", "INVALID_DATETIME") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def serialize_interview(row: Interview) -> dict:
    candidate = row.candidate
    user = candidate.user if candidate else None
    return {
        "id": row.id,
        "candidate_id": row.candidate_id,
        "application_id": row.application_id,
        "job_id": row.job_id,
        "company_id": row.company_id,
        "recruiter_id": row.recruiter_id,
        "scheduled_at": row.scheduled_at.isoformat() if row.scheduled_at else None,
        "duration_minutes": row.duration_minutes,
        "location": row.location,
        "type": row.type.value,
        "type_label": TYPE_LABEL.get(row.type, row.type.value),
        "status": row.status.value,
        "notes": row.notes,
        "reminder_sent_at": row.reminder_sent_at.isoformat() if row.reminder_sent_at else None,
        "candidate_name": user.full_name if user else None,
        "job_title": row.job.title if row.job else None,
        "company_name": row.company.name if row.company else None,
    }


def _visible(db: Session, user: User, row: Interview) -> bool:
    if user.role in {UserRole.RECRUITER} | ADMINS:
        return True
    if user.role == UserRole.CANDIDATE:
        cand = ensure_candidate(db, user)
        return row.candidate_id == cand.id
    if user.role == UserRole.EMPLOYER:
        return bool(row.company_id and row.company_id in company_ids_for_employer(db, user))
    return False


def list_interviews(db: Session, user: User) -> list[Interview]:
    stmt = select(Interview).options(
        joinedload(Interview.candidate).joinedload(Candidate.user),
        joinedload(Interview.job),
        joinedload(Interview.company),
    )
    if user.role == UserRole.CANDIDATE:
        cand = ensure_candidate(db, user)
        stmt = stmt.where(Interview.candidate_id == cand.id)
    elif user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(Interview.company_id.in_(ids))
    elif user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux entretiens.", "FORBIDDEN")
    return list(db.scalars(stmt.order_by(Interview.scheduled_at.asc())).unique().all())


def get_interview(db: Session, user: User, interview_id: str) -> Interview:
    row = db.scalar(
        select(Interview)
        .options(
            joinedload(Interview.candidate).joinedload(Candidate.user),
            joinedload(Interview.job),
            joinedload(Interview.company),
        )
        .where(Interview.id == interview_id)
    )
    if not row:
        raise AppError(404, "Entretien introuvable.", "INTERVIEW_NOT_FOUND")
    if not _visible(db, user, row):
        raise AppError(403, "Vous n'avez pas accès à cet entretien.", "FORBIDDEN")
    return row


def create_interview(db: Session, user: User, data: InterviewIn, ip: str | None) -> Interview:
    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Seuls les recruteurs peuvent planifier un entretien.", "FORBIDDEN")
    candidate = db.get(Candidate, data.candidate_id)
    if not candidate:
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    application = None
    job = None
    company_id = data.company_id
    job_id = data.job_id
    if data.application_id:
        application = db.get(Application, data.application_id)
        if not application or application.candidate_id != candidate.id:
            raise AppError(400, "Candidature invalide pour ce candidat.", "INVALID_APPLICATION")
        job_id = application.job_id
        job = db.get(JobOffer, job_id)
        if job:
            company_id = job.company_id
    elif job_id:
        job = db.get(JobOffer, job_id)
        if job:
            company_id = company_id or job.company_id
    when = _parse_when(data.scheduled_at)
    row = Interview(
        candidate_id=candidate.id,
        application_id=application.id if application else None,
        job_id=job_id,
        company_id=company_id,
        recruiter_id=user.id,
        scheduled_at=when,
        duration_minutes=data.duration_minutes or 30,
        location=data.location or "Visio",
        type=data.type or InterviewType.TALENDUS,
        notes=data.notes,
        status=InterviewStatus.SCHEDULED,
    )
    db.add(row)
    db.flush()
    cand_user = candidate.user
    when_label = when.strftime("%Y-%m-%d %H:%M")
    notify(
        db,
        cand_user,
        NotificationType.INTERVIEW_INVITE,
        "Entretien planifié",
        f"{TYPE_LABEL.get(row.type, row.type.value)} le {when_label} — {row.location or ''}".strip(),
        href="/espace.html",
    )
    if cand_user:
        send_email(
            db,
            cand_user.email,
            EmailType.INTERVIEW_INVITE,
            "interview",
            name=cand_user.first_name,
            job_title=(job.title if job else "Talendus"),
            status=when_label,
            comment=row.location or "",
        )
        from app.integrations.hooks import maybe_send_whatsapp

        maybe_send_whatsapp(
            recipient=cand_user.phone,
            template="interview_invite",
            variables={
                "name": cand_user.first_name or "",
                "job": job.title if job else "Talendus",
                "when": when_label,
                "location": row.location or "",
            },
        )
    audit(db, "interview.create", user, "interview", row.id, ip)
    db.commit()
    db.refresh(row)
    return get_interview(db, user, row.id)


def patch_interview(db: Session, user: User, interview_id: str, data: InterviewPatchIn) -> Interview:
    row = get_interview(db, user, interview_id)
    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Modification réservée à l'équipe Talendus.", "FORBIDDEN")
    payload = data.model_dump(exclude_unset=True)
    rescheduled = False
    if "scheduled_at" in payload and payload["scheduled_at"]:
        row.scheduled_at = _parse_when(payload.pop("scheduled_at"))
        row.reminder_sent_at = None
        rescheduled = True
    for key, value in payload.items():
        setattr(row, key, value)
    audit(db, "interview.update", user, "interview", row.id)
    if rescheduled:
        cand_user = row.candidate.user if row.candidate else None
        when_label = row.scheduled_at.strftime("%Y-%m-%d %H:%M") if row.scheduled_at else ""
        if cand_user:
            send_email(
                db,
                cand_user.email,
                EmailType.INTERVIEW_INVITE,
                "interview",
                name=cand_user.first_name,
                job_title=(row.job.title if row.job else "Talendus"),
                status=when_label,
                comment=row.location or "",
            )
            from app.integrations.hooks import maybe_send_whatsapp

            maybe_send_whatsapp(
                recipient=cand_user.phone,
                template="interview_invite",
                variables={"name": cand_user.first_name or "", "when": when_label, "location": row.location or ""},
            )
    db.commit()
    return get_interview(db, user, row.id)


def set_status(db: Session, user: User, interview_id: str, status: InterviewStatus) -> Interview:
    row = get_interview(db, user, interview_id)
    if user.role == UserRole.CANDIDATE and status not in {InterviewStatus.CONFIRMED, InterviewStatus.CANCELLED}:
        raise AppError(403, "Un candidat peut confirmer ou annuler uniquement.", "FORBIDDEN")
    if user.role == UserRole.EMPLOYER and status not in {InterviewStatus.CONFIRMED, InterviewStatus.CANCELLED, InterviewStatus.COMPLETED}:
        raise AppError(403, "Statut non autorisé.", "FORBIDDEN")
    row.status = status
    audit(db, "interview.status", user, "interview", row.id, metadata={"status": status.value})
    cand_user = row.candidate.user if row.candidate else None
    if cand_user and status in {InterviewStatus.CONFIRMED, InterviewStatus.CANCELLED}:
        notify(
            db,
            cand_user,
            NotificationType.INTERVIEW_INVITE,
            "Entretien mis à jour",
            f"Statut : {status.value}",
            href="/espace.html",
        )
        from app.integrations.hooks import maybe_send_whatsapp

        maybe_send_whatsapp(
            recipient=cand_user.phone,
            template="candidate_notice",
            variables={"status": status.value, "when": row.scheduled_at.strftime("%Y-%m-%d %H:%M") if row.scheduled_at else ""},
        )
    db.commit()
    return get_interview(db, user, row.id)


def dispatch_due_reminders(db: Session, *, hours: int = 24) -> dict:
    """Envoie e-mail (toujours journalisé) et WhatsApp (si actif) pour les entretiens à venir."""
    from app.integrations.hooks import maybe_send_whatsapp
    from app.models.enums import utcnow

    now = utcnow()
    until = now + timedelta(hours=max(1, min(hours, 72)))
    rows = list(
        db.scalars(
            select(Interview)
            .options(
                joinedload(Interview.candidate).joinedload(Candidate.user),
                joinedload(Interview.job),
            )
            .where(
                Interview.status.in_([InterviewStatus.SCHEDULED, InterviewStatus.CONFIRMED]),
                Interview.reminder_sent_at.is_(None),
                Interview.scheduled_at >= now,
                Interview.scheduled_at <= until,
            )
        )
        .unique()
        .all()
    )
    sent = skipped = 0
    for row in rows:
        cand_user = row.candidate.user if row.candidate else None
        if not cand_user:
            skipped += 1
            continue
        when_label = row.scheduled_at.strftime("%Y-%m-%d %H:%M") if row.scheduled_at else ""
        send_email(
            db,
            cand_user.email,
            EmailType.INTERVIEW_INVITE,
            "interview",
            name=cand_user.first_name,
            job_title=(row.job.title if row.job else "Talendus"),
            status=when_label,
            comment=row.location or "Rappel",
        )
        maybe_send_whatsapp(
            recipient=cand_user.phone,
            template="interview_reminder",
            variables={"name": cand_user.first_name or "", "when": when_label, "location": row.location or ""},
        )
        row.reminder_sent_at = now
        sent += 1
    if rows:
        db.commit()
    return {"sent": sent, "skipped": skipped, "hours": hours}
