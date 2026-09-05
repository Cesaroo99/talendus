from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import Application, ApplicationStatusHistory, Candidate, InternalNote, JobOffer, RecruitmentMission, Resume, User
from app.models.company import mission_jobs
from app.rbac import ADMINS
from app.models.enums import (
    ApplicationStatus,
    EmailType,
    JobStatus,
    MissionStatus,
    NotificationType,
    UserRole,
)
from app.schemas import ApplicationCreateIn, PublicApplyIn, StaffApplicationIn
from app.security import hash_password, random_password
from app.services.access import company_ids_for_employer, is_presented_to_employer
from app.services.audit import audit
from app.services.auth import ensure_candidate
from app.services.email import send_email
from app.services.jobs import assert_job_open, get_public_job
from app.services.labels import application_status_label
from app.services.ops_notify import first_staff, frontend, notify_people
from app.site_jobs import open_site_job_for_apply
from app.services.pipeline import (
    VIVIER_FOR_STATUS,
    client_feedback_from,
    next_action_for,
    stage_for,
    tracker_for,
)


def _talendus_staff(db: Session) -> list[User]:
    return list(
        db.scalars(
            select(User).where(
                User.is_active.is_(True),
                User.role.in_([UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN]),
            )
        ).all()
    )


def _notify_new_application(db: Session, job: JobOffer, applicant: User) -> None:
    seen: set[str] = set()
    staff = db.get(User, job.recruiter_id) if job.recruiter_id else None
    recipients: list[User] = []
    if staff and staff.role in {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN}:
        recipients.append(staff)
    else:
        recipients = _talendus_staff(db)
    for person in recipients:
        if not person or person.id in seen:
            continue
        notify_people(
            db,
            person,
            actor=applicant,
            ntype=NotificationType.APPLICATION_NEW,
            title="Nouvelle candidature",
            message=f"{applicant.full_name} a postulé pour {job.title}.",
            section="jobs",
            item_id=job.id,
            template="new_application",
            email_type=EmailType.NEW_APPLICATION_RECRUITER,
            ctx={
                "job_title": job.title,
                "candidate_name": applicant.full_name,
                "candidate_email": applicant.email,
            },
        )
        seen.add(person.id)
    extras = [person for person in _talendus_staff(db) if person.id not in seen]
    for person in extras:
        notify_people(
            db,
            person,
            actor=applicant,
            ntype=NotificationType.APPLICATION_NEW,
            title="Nouvelle candidature",
            message=f"{applicant.full_name} a postulé pour {job.title}.",
            section="jobs",
            item_id=job.id,
            template="new_application",
            email_type=EmailType.NEW_APPLICATION_RECRUITER,
            ctx={
                "job_title": job.title,
                "candidate_name": applicant.full_name,
                "candidate_email": applicant.email,
            },
        )
        seen.add(person.id)


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
        job = db.scalar(select(JobOffer).options(joinedload(JobOffer.company)).where(JobOffer.id == data.job_id))
    elif data.job_slug:
        job = open_site_job_for_apply(db, data.job_slug)
        if not job:
            job = db.scalar(
                select(JobOffer).options(joinedload(JobOffer.company)).where(JobOffer.slug == data.job_slug)
            )
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
    try:
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
        staff = db.get(User, job.recruiter_id) if job.recruiter_id else None
        _notify_new_application(db, job, user)
        notify_people(
            db,
            user,
            actor=staff or first_staff(db),
            ntype=NotificationType.APPLICATION_NEW,
            title="Candidature envoyée",
            message=f"Votre candidature pour {job.title} a été transmise.",
            section="apps",
            template="application_confirm",
            email_type=EmailType.APPLICATION_CONFIRMATION,
            ctx={"name": user.first_name or "", "job_title": job.title},
            application_id=application.id,
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
        audit(db, "application.create", user, "application", application.id, ip, {"job_id": job.id})
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "Une candidature existe déjà pour cette offre.", "APPLICATION_ALREADY_EXISTS") from None
    db.refresh(application)
    return application


def apply_staff(db: Session, actor: User, data: StaffApplicationIn, ip: str | None = None) -> Application:
    if actor.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Seul le personnel Talendus peut lier un candidat à une offre.", "FORBIDDEN")
    job = db.scalar(select(JobOffer).options(joinedload(JobOffer.company)).where(JobOffer.id == data.job_id))
    candidate = db.scalar(
        select(Candidate)
        .options(joinedload(Candidate.user), joinedload(Candidate.resumes))
        .where(Candidate.id == data.candidate_id)
    )
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    if not candidate:
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    if job.status in {JobStatus.CLOSED, JobStatus.ARCHIVED}:
        raise AppError(409, "Cette offre est fermée.", "JOB_CLOSED")
    existing = db.scalar(
        select(Application).where(Application.candidate_id == candidate.id, Application.job_id == job.id)
    )
    if existing:
        raise AppError(409, "Ce candidat est déjà lié à cette offre.", "APPLICATION_ALREADY_EXISTS")
    resume = _primary_resume(db, candidate, data.resume_id)
    from app.services.matching import score_pair
    from app.services.resume_parse import summary_from_storage

    score, reasons = score_pair(candidate, job)
    application = Application(
        candidate_id=candidate.id,
        job_id=job.id,
        resume_id=resume.id if resume else None,
        status=ApplicationStatus.UNDER_REVIEW,
        cover_note=data.cover_note,
        source="staff",
        match_score=score,
    )
    try:
        db.add(application)
        db.flush()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "Ce candidat est déjà lié à cette offre.", "APPLICATION_ALREADY_EXISTS") from None
    _history(db, application, None, ApplicationStatus.UNDER_REVIEW.value, actor, "Liaison interne Talendus")
    if not candidate.pipeline_status or candidate.pipeline_status in {"nouveau", "inactif"}:
        candidate.pipeline_status = "a-contacter"
    if not candidate.assigned_recruiter_id:
        candidate.assigned_recruiter_id = job.recruiter_id or actor.id
    mission = db.scalar(
        select(RecruitmentMission).where(RecruitmentMission.job_id == job.id).order_by(RecruitmentMission.created_at.desc())
    )
    if not mission:
        mission = db.scalar(
            select(RecruitmentMission)
            .join(mission_jobs, mission_jobs.c.mission_id == RecruitmentMission.id)
            .where(mission_jobs.c.job_id == job.id)
            .order_by(RecruitmentMission.created_at.desc())
        )
    if not mission and job.company_id:
        mission = RecruitmentMission(
            company_id=job.company_id,
            job_id=job.id,
            recruiter_id=job.recruiter_id or actor.id,
            title=job.title,
            seats=max(1, job.openings or 1),
            status=MissionStatus.SCREENING,
            location=job.location,
            sector=job.sector,
            skills=job.skills,
            contract_type=job.contract_type,
        )
        db.add(mission)
        db.flush()
    company_name = job.company.name if job.company else ""
    cand_name = candidate.user.full_name if candidate.user else "Candidat"
    db.add(
        InternalNote(
            entity_type="candidate",
            entity_id=candidate.id,
            author_id=actor.id,
            text=(
                f"Dossier ouvert sur « {job.title} »"
                + (f" ({company_name})" if company_name else "")
                + f". Score {score} %. "
                + (" · ".join(reasons[:3]) if reasons else "Correspondance à valider.")
            ),
        )
    )
    staff_targets = [actor]
    if job.recruiter_id:
        recruiter = db.get(User, job.recruiter_id)
        if recruiter:
            staff_targets.append(recruiter)
    notify_people(
        db,
        staff_targets,
        actor=actor,
        ntype=NotificationType.APPLICATION_NEW,
        title="Dossier ouvert",
        message=f"{cand_name} est maintenant suivi pour {job.title}.",
        section="jobs",
        item_id=job.id,
        template="new_application",
        email_type=EmailType.NEW_APPLICATION_RECRUITER,
        ctx={
            "job_title": job.title,
            "candidate_name": cand_name,
            "candidate_email": candidate.user.email if candidate.user else "",
        },
        application_id=application.id,
    )
    if candidate.user:
        notify_people(
            db,
            candidate.user,
            actor=actor,
            ntype=NotificationType.APPLICATION_STATUS,
            title="Talendus étudie un poste pour vous",
            message=f"Votre conseiller a ouvert un suivi pour {job.title}.",
            section="apps",
            template="application_status",
            email_type=EmailType.APPLICATION_STATUS,
            ctx={
                "name": candidate.user.first_name or "",
                "job_title": job.title,
                "status": "À l’étude",
                "comment": "",
            },
            application_id=application.id,
        )
    audit(
        db,
        "application.staff_link",
        actor,
        "application",
        application.id,
        ip,
        {"job_id": job.id, "candidate_id": candidate.id, "mission_id": mission.id if mission else None},
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "Ce candidat est déjà lié à cette offre.", "APPLICATION_ALREADY_EXISTS") from None
    row = get_application(db, actor, application.id)
    cv_summary = summary_from_storage(resume.parse_json, profile=candidate) if resume else ""
    row.dossier = {
        "score": score,
        "reasons": reasons,
        "cv_summary": cv_summary,
        "candidate_id": candidate.id,
        "candidate_name": cand_name,
        "job_id": job.id,
        "job_title": job.title,
        "company_name": company_name,
        "mission_id": mission.id if mission else None,
        "application_id": row.id,
        "resume_id": resume.id if resume else None,
        "preview_path": f"/api/candidates/resumes/{resume.id}/preview" if resume else None,
        "download_path": f"/api/candidates/resumes/{resume.id}/file" if resume else None,
        "pipeline_status": candidate.pipeline_status,
        "stage": stage_for(row.status),
        "tracker": tracker_for(row),
        "next_steps": [
            {"key": "cv", "label": "Lire le CV"},
            {"key": "interview", "label": "Planifier l’entretien Talendus"},
            {"key": "present", "label": "Présenter le dossier à l’employeur"},
            {"key": "mission", "label": "Suivre dans le kanban"} if mission else {"key": "apps", "label": "Ouvrir le suivi de candidature"},
        ],
    }
    return row


def apply_public(
    db: Session,
    data: PublicApplyIn,
    ip: str | None = None,
    *,
    cv_file: bytes | None = None,
    cv_filename: str | None = None,
) -> Application:
    job = open_site_job_for_apply(db, data.job_slug) or get_public_job(db, data.job_slug)
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
        send_email(
            db,
            user.email,
            EmailType.WELCOME,
            "welcome",
            name=user.first_name,
            link=f"{frontend()}/espace.html",
        )
    resume_id = None
    if cv_file and cv_filename:
        from app.services.candidates import upload_cv

        resume = upload_cv(db, user, cv_file, cv_filename)
        resume_id = resume.id
    payload = ApplicationCreateIn(
        job_slug=data.job_slug,
        cover_note=data.cover_note or (None if resume_id else data.cv_url),
        resume_id=resume_id,
    )
    return apply(db, user, payload, ip)


def list_own(db: Session, user: User) -> list[Application]:
    candidate = ensure_candidate(db, user)
    return list(
        db.scalars(
            select(Application)
            .options(
                joinedload(Application.job).joinedload(JobOffer.company),
                joinedload(Application.history),
            )
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
        if not is_presented_to_employer(app_row):
            raise AppError(403, "Ce dossier n'a pas encore été transmis par Talendus.", "FORBIDDEN")
    elif user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès à cette candidature.", "FORBIDDEN")
    return app_row


def change_status(db: Session, user: User, application_id: str, status: ApplicationStatus, comment: str | None) -> Application:
    if user.role == UserRole.EMPLOYER:
        raise AppError(403, "Le suivi des candidatures est assuré par Talendus.", "FORBIDDEN")
    application = get_application(db, user, application_id)
    if user.role == UserRole.CANDIDATE:
        if status != ApplicationStatus.WITHDRAWN:
            raise AppError(403, "Un candidat ne peut que retirer sa candidature.", "FORBIDDEN")
    old = application.status.value
    application.status = status
    _history(db, application, old, status.value, user, comment)
    if application.candidate:
        vivier = VIVIER_FOR_STATUS.get(status)
        if vivier:
            application.candidate.pipeline_status = vivier
    _notify_pipeline_parties(db, user, application, status, comment)
    _advance_mission_for_status(db, application, status)
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


def record_client_feedback(db: Session, user: User, application_id: str, action: str, comment: str | None) -> Application:
    if user.role != UserRole.EMPLOYER:
        raise AppError(403, "Ce retour est réservé à l’entreprise.", "FORBIDDEN")
    application = get_application(db, user, application_id)
    if not is_presented_to_employer(application):
        raise AppError(403, "Ce dossier n'a pas encore été transmis par Talendus.", "FORBIDDEN")
    key = (action or "").strip().lower()
    labels = {
        "interested": "intéressé",
        "interview": "demande un entretien",
        "pass": "non retenu",
    }
    if key not in labels:
        raise AppError(400, "Indiquez intéressé, entretien ou non retenu.", "VALIDATION_ERROR")
    note = f"Retour employeur : {labels[key]}"
    extra = (comment or "").strip()
    if extra:
        note = f"{note}. {extra}"
    _history(db, application, application.status.value, application.status.value, user, note)
    job_title = application.job.title if application.job else "un poste"
    cand_name = application.candidate.user.full_name if application.candidate and application.candidate.user else "un candidat"
    staff_targets = _talendus_staff(db)
    if application.job and application.job.recruiter_id:
        recruiter = db.get(User, application.job.recruiter_id)
        if recruiter:
            staff_targets.append(recruiter)
    notify_people(
        db,
        staff_targets,
        actor=user,
        ntype=NotificationType.APPLICATION_STATUS,
        title="Retour employeur",
        message=f"{cand_name} · {job_title} : {labels[key]}.",
        section="candidates",
        item_id=application.candidate_id,
        template="hiring_update",
        email_type=EmailType.ADMIN,
        ctx={
            "name": "",
            "title": "Retour employeur",
            "detail": note,
            "job_title": job_title,
        },
        application_id=application.id,
    )
    audit(db, "application.client_feedback", user, "application", application.id, metadata={"action": key})
    db.commit()
    db.refresh(application)
    return application


def _notify_pipeline_parties(
    db: Session, actor: User, application: Application, status: ApplicationStatus, comment: str | None
) -> None:
    from app.integrations.hooks import maybe_send_whatsapp
    from app.services.ops_notify import company_users

    candidate_user = application.candidate.user if application.candidate else None
    job = application.job
    job_title = job.title if job else "un poste"
    company_name = job.company.name if job and job.company else ""
    cand_name = candidate_user.full_name if candidate_user else "Candidat"
    shown = application_status_label(status, candidate_user)
    comment_text = (comment or "").strip()

    if candidate_user and status != ApplicationStatus.UNDER_REVIEW:
        ntype = NotificationType.APPLICATION_STATUS
        title = "Mise à jour de candidature"
        message = f"{job_title} : {shown}"
        template = "application_status"
        email_type = EmailType.APPLICATION_STATUS
        if status == ApplicationStatus.HIRED:
            ntype = NotificationType.APPLICATION_ACCEPTED
            title = "Placement confirmé"
            message = f"Bonne nouvelle : le suivi pour {job_title} est maintenant confirmé."
        elif status == ApplicationStatus.REJECTED:
            ntype = NotificationType.APPLICATION_REJECTED
            title = "Suivi de candidature"
        elif status == ApplicationStatus.INTERVIEW:
            ntype = NotificationType.INTERVIEW_INVITE
            title = "Entretien Talendus"
            template = "interview"
            email_type = EmailType.INTERVIEW_INVITE
        elif status == ApplicationStatus.SHORTLISTED:
            title = "Dossier présenté"
            message = f"Talendus a présenté votre dossier pour {job_title}."
        elif status == ApplicationStatus.SECOND_INTERVIEW:
            title = "Entretien chez l’employeur"
            message = f"La suite pour {job_title} se poursuit avec l’employeur."
        elif status == ApplicationStatus.OFFER_SENT:
            title = "Offre en cours"
            message = f"Une offre est en préparation pour {job_title}."
        elif status == ApplicationStatus.WITHDRAWN:
            title = "Candidature retirée"
        notify_people(
            db,
            candidate_user,
            actor=actor,
            ntype=ntype,
            title=title,
            message=message,
            section="application",
            item_id=application.id,
            template=template,
            email_type=email_type,
            ctx={
                "name": candidate_user.first_name or "",
                "job_title": job_title,
                "status": shown,
                "comment": comment_text if status in {ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN} else "",
            },
            application_id=application.id,
        )
        maybe_send_whatsapp(
            recipient=candidate_user.phone,
            template="interview_invite" if status == ApplicationStatus.INTERVIEW else "application_status",
            variables={"name": candidate_user.first_name or "", "job": job_title, "status": shown},
        )

    employer_statuses = {
        ApplicationStatus.SHORTLISTED,
        ApplicationStatus.SECOND_INTERVIEW,
        ApplicationStatus.OFFER_SENT,
        ApplicationStatus.HIRED,
        ApplicationStatus.REJECTED,
    }
    if job and job.company_id and status in employer_statuses:
        if status == ApplicationStatus.REJECTED and not is_presented_to_employer(application):
            pass
        else:
            emp_title = {
                ApplicationStatus.SHORTLISTED: "Dossier présenté",
                ApplicationStatus.SECOND_INTERVIEW: "Entretien client",
                ApplicationStatus.OFFER_SENT: "Offre en cours",
                ApplicationStatus.HIRED: "Placement confirmé",
                ApplicationStatus.REJECTED: "Dossier non retenu",
            }[status]
            emp_message = {
                ApplicationStatus.SHORTLISTED: f"{cand_name} vous est présenté pour {job_title}. Donnez une suite à Talendus.",
                ApplicationStatus.SECOND_INTERVIEW: f"Entretien client à prévoir pour {cand_name} · {job_title}.",
                ApplicationStatus.OFFER_SENT: f"Une offre est en cours pour {cand_name} · {job_title}.",
                ApplicationStatus.HIRED: f"{cand_name} est placé sur {job_title}.",
                ApplicationStatus.REJECTED: f"Le suivi de {cand_name} pour {job_title} est refermé.",
            }[status]
            notify_people(
                db,
                company_users(db, job.company_id),
                actor=actor,
                ntype=NotificationType.APPLICATION_NEW if status == ApplicationStatus.SHORTLISTED else NotificationType.APPLICATION_STATUS,
                title=emp_title,
                message=emp_message,
                section="inbox",
                template="candidate_presented" if status == ApplicationStatus.SHORTLISTED else "employer_application",
                email_type=EmailType.ADMIN,
                ctx={
                    "name": "",
                    "candidate_name": cand_name,
                    "job_title": job_title,
                    "company_name": company_name,
                    "detail": emp_message,
                    "title": emp_title,
                },
                application_id=application.id,
            )

    if status == ApplicationStatus.WITHDRAWN:
        staff_targets = _talendus_staff(db)
        if job and job.recruiter_id:
            recruiter = db.get(User, job.recruiter_id)
            if recruiter:
                staff_targets.append(recruiter)
        notify_people(
            db,
            staff_targets,
            actor=actor,
            ntype=NotificationType.APPLICATION_STATUS,
            title="Candidature retirée",
            message=f"{cand_name} s’est retiré de {job_title}.",
            section="candidates",
            item_id=application.candidate_id,
            template="hiring_update",
            email_type=EmailType.ADMIN,
            ctx={"title": "Candidature retirée", "detail": f"{cand_name} s’est retiré de {job_title}."},
            application_id=application.id,
        )


def _advance_mission_for_status(db: Session, application: Application, status: ApplicationStatus) -> None:
    job = application.job
    if not job:
        return
    mission = db.scalar(
        select(RecruitmentMission).where(RecruitmentMission.job_id == job.id).order_by(RecruitmentMission.created_at.desc())
    )
    if not mission:
        mission = db.scalar(
            select(RecruitmentMission)
            .join(mission_jobs, mission_jobs.c.mission_id == RecruitmentMission.id)
            .where(mission_jobs.c.job_id == job.id)
            .order_by(RecruitmentMission.created_at.desc())
        )
    if not mission:
        return
    desired = {
        ApplicationStatus.UNDER_REVIEW: MissionStatus.SCREENING,
        ApplicationStatus.INTERVIEW: MissionStatus.INTERVIEWS,
        ApplicationStatus.SHORTLISTED: MissionStatus.CLIENT_REVIEW,
        ApplicationStatus.SECOND_INTERVIEW: MissionStatus.CLIENT_REVIEW,
        ApplicationStatus.OFFER_SENT: MissionStatus.HIRING,
        ApplicationStatus.HIRED: MissionStatus.HIRING,
    }.get(status)
    if not desired:
        return
    order = [item.value for item in MissionStatus]
    try:
        if order.index(desired.value) <= order.index(mission.status.value if mission.status else ""):
            return
    except ValueError:
        return
    from app.services.contracts import WORK_STATUSES, company_has_signed_mandate

    if desired.value in WORK_STATUSES and not company_has_signed_mandate(db, mission.company_id):
        return
    mission.status = desired


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
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(JobOffer.company_id.in_(ids))
    elif user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux candidatures.", "FORBIDDEN")
    if job_id:
        stmt = stmt.where(Application.job_id == job_id)
    rows = list(db.scalars(stmt.order_by(Application.created_at.desc())).unique().all())
    if user.role == UserRole.EMPLOYER:
        rows = [row for row in rows if is_presented_to_employer(row)]
    return rows


def serialize_application(row: Application, viewer: User | None = None) -> dict:
    staff_viewer = viewer is not None and viewer.role in {UserRole.RECRUITER} | ADMINS
    hide_internal = viewer is None or viewer.role in {UserRole.CANDIDATE, UserRole.EMPLOYER}
    payload = {
        "id": row.id,
        "status": row.status.value,
        "status_label": application_status_label(row.status, viewer),
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
            "shift": row.job.shift,
            "schedule": row.job.schedule,
            "work_mode": row.job.work_mode,
            "work_authorization": row.job.work_authorization,
            "can_sponsor": bool(row.job.can_sponsor),
        },
        "resume_id": row.resume_id,
        "pipeline_stage": stage_for(row.status),
        "tracker": tracker_for(row),
        "presented": is_presented_to_employer(row),
        "next_action": next_action_for(row, viewer),
        "client_feedback": client_feedback_from(row) if not hide_internal or (viewer and viewer.role == UserRole.EMPLOYER) else None,
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
    if staff_viewer:
        payload["staff_notes"] = row.staff_notes
        if row.candidate and row.candidate.user:
            payload["candidate"] = {
                "id": row.candidate.id,
                "first_name": row.candidate.user.first_name,
                "last_name": row.candidate.user.last_name,
                "email": row.candidate.user.email,
                "title": row.candidate.title,
                "city": row.candidate.city,
                "skills": row.candidate.skills,
                "years_experience": row.candidate.years_experience,
            }
    elif viewer and viewer.role == UserRole.EMPLOYER and row.candidate and row.candidate.user:
        payload["candidate"] = {
            "id": row.candidate.id,
            "first_name": row.candidate.user.first_name,
            "last_name": row.candidate.user.last_name,
            "email": None,
            "title": row.candidate.title,
            "city": row.candidate.city,
            "skills": row.candidate.skills,
            "years_experience": row.candidate.years_experience,
        }
    return payload
