"""Projection des données API vers le format du back-office Talendus."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import (
    Application,
    Candidate,
    Company,
    Contract,
    InternalNote,
    Interview,
    Invoice,
    JobOffer,
    Notification,
    Payment,
    RecruitmentMission,
    User,
)
from app.models.enums import ApplicationStatus, InvoiceStatus, JobStatus, MissionStatus
from app.services.pipeline import stage_for

APP_STATUS = {
    ApplicationStatus.SUBMITTED: "nouveau",
    ApplicationStatus.RECEIVED: "nouveau",
    ApplicationStatus.UNDER_REVIEW: "a-contacter",
    ApplicationStatus.SHORTLISTED: "qualifie",
    ApplicationStatus.INTERVIEW: "entretien",
    ApplicationStatus.SECOND_INTERVIEW: "entretien-client",
    ApplicationStatus.OFFER_SENT: "offre",
    ApplicationStatus.REJECTED: "refuse",
    ApplicationStatus.HIRED: "place",
    ApplicationStatus.WITHDRAWN: "inactif",
}

JOB_STATUS = {
    JobStatus.DRAFT: "brouillon",
    JobStatus.PUBLISHED: "publiee",
    JobStatus.PAUSED: "suspendue",
    JobStatus.CLOSED: "archivee",
    JobStatus.ARCHIVED: "archivee",
}

MISSION_STATUS = {
    MissionStatus.REQUEST_SUBMITTED: "besoin-transmis",
    MissionStatus.UNDER_REVIEW: "en-analyse",
    MissionStatus.CLIENT_CONTACTED: "echange",
    MissionStatus.NEEDS_CONFIRMED: "profil-defini",
    MissionStatus.JOB_BEING_PREPARED: "offre-preparation",
    MissionStatus.CLIENT_VALIDATION: "validation-client",
    MissionStatus.JOB_PUBLISHED: "publiee",
    MissionStatus.SOURCING: "recherche",
    MissionStatus.SCREENING: "preselection",
    MissionStatus.INTERVIEWS: "entretiens",
    MissionStatus.SHORTLIST: "shortlist",
    MissionStatus.CLIENT_REVIEW: "revue-client",
    MissionStatus.HIRING: "decision",
    MissionStatus.CLOSED: "termine",
    MissionStatus.OPEN: "en-cours",
    MissionStatus.IN_PROGRESS: "en-cours",
    MissionStatus.FILLED: "pourvue",
    MissionStatus.CANCELLED: "annulee",
}

INVOICE_STATUS = {
    InvoiceStatus.DRAFT: "brouillon",
    InvoiceStatus.SENT: "envoyee",
    InvoiceStatus.PENDING: "en-attente",
    InvoiceStatus.PAID: "payee",
    InvoiceStatus.OVERDUE: "en-retard",
    InvoiceStatus.CANCELLED: "annulee",
}

INTERVIEW_TYPE = {
    "TALENDUS": "Talendus",
    "CLIENT": "Client",
    "PHONE": "Téléphone",
    "VIDEO": "Visio",
    "ONSITE": "Sur place",
    "OFFER": "Offre",
}

ROLE = {
    "ADMIN": "admin",
    "RECRUITER": "recruiter",
    "FINANCE": "finance",
    "EDITOR": "editor",
    "EMPLOYER": "recruiter",
    "CANDIDATE": "recruiter",
}


def bootstrap(db: Session) -> dict:
    users = db.scalars(select(User).order_by(User.created_at.asc())).all()
    companies = db.scalars(select(Company).order_by(Company.name.asc())).all()
    jobs = db.scalars(select(JobOffer).options(joinedload(JobOffer.company)).order_by(JobOffer.created_at.desc())).unique().all()
    candidates = db.scalars(
        select(Candidate).options(
            joinedload(Candidate.user),
            selectinload(Candidate.experiences),
            selectinload(Candidate.education),
            selectinload(Candidate.applications).joinedload(Application.job),
        )
    ).unique().all()
    missions = db.scalars(
        select(RecruitmentMission).options(selectinload(RecruitmentMission.linked_jobs)).order_by(RecruitmentMission.created_at.desc())
    ).all()
    contracts = db.scalars(select(Contract).options(selectinload(Contract.signatures))).all()
    notes = db.scalars(select(InternalNote).order_by(InternalNote.created_at.desc()).limit(200)).all()
    notifications = db.scalars(select(Notification).order_by(Notification.created_at.desc()).limit(100)).all()
    applications = db.scalars(
        select(Application).options(joinedload(Application.job), joinedload(Application.candidate)).order_by(Application.created_at.desc())
    ).unique().all()
    interviews = db.scalars(
        select(Interview).options(joinedload(Interview.candidate).joinedload(Candidate.user)).order_by(Interview.scheduled_at.asc())
    ).unique().all()
    invoices = db.scalars(
        select(Invoice).options(joinedload(Invoice.company), joinedload(Invoice.mission)).order_by(Invoice.created_at.desc())
    ).unique().all()
    payments = db.scalars(select(Payment).options(joinedload(Payment.invoice)).order_by(Payment.created_at.desc())).unique().all()

    from app.services.matching import score_pair

    job_matches = []
    for job in jobs[:12]:
        ranked = []
        for cand in candidates:
            score, reasons = score_pair(cand, job)
            if score >= 35:
                ranked.append((score, cand, reasons))
        ranked.sort(key=lambda x: x[0], reverse=True)
        for score, cand, reasons in ranked[:5]:
            job_matches.append(
                {
                    "jobId": job.id,
                    "candidateId": cand.id,
                    "score": score,
                    "reasons": reasons,
                }
            )

    return {
        "users": [_user(u) for u in users if u.role.value in ROLE],
        "clients": [_company(c) for c in companies],
        "jobs": [_job(j, applications) for j in jobs],
        "candidates": [_candidate(c) for c in candidates],
        "missions": [_mission(m, applications) for m in missions],
        "contracts": [_contract(c) for c in contracts],
        "notes": [_note(n) for n in notes],
        "notifications": [_notification(n) for n in notifications],
        "interviews": [_interview(i) for i in interviews],
        "invoices": [_invoice(i) for i in invoices],
        "payments": [_payment(p) for p in payments],
        "jobMatches": job_matches,
        "activities": [
            {
                "id": a.id,
                "text": f"Candidature — {(a.candidate.user.first_name if a.candidate and a.candidate.user else '')} · {(a.job.title if a.job else '')}",
                "at": a.created_at.strftime("%Y-%m-%d %H:%M") if a.created_at else "",
            }
            for a in applications[:20]
        ],
    }


def _user(u: User) -> dict:
    return {
        "id": u.id,
        "firstName": u.first_name,
        "lastName": u.last_name,
        "email": u.email,
        "role": ROLE.get(u.role.value, "recruiter"),
        "title": u.title or "",
        "initials": ((u.first_name or "?")[:1] + (u.last_name or "?")[:1]).upper(),
    }


def _company(c: Company) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "sector": c.sector or "",
        "city": c.city or "",
        "contact": c.contact_name or "",
        "email": c.email or "",
        "phone": c.phone or "",
        "status": "Actif" if c.status and c.status.value == "ACTIVE" else "Prospect",
        "recruiterId": c.assigned_recruiter_id or "",
        "employees": c.employees or 0,
        "website": c.website or "",
        "since": c.created_at.strftime("%Y-%m-%d") if c.created_at else "",
    }


def _job(j: JobOffer, applications: list[Application]) -> dict:
    count = sum(1 for a in applications if a.job_id == j.id)
    return {
        "id": j.id,
        "title": j.title,
        "clientId": j.company_id,
        "city": j.location or "",
        "sector": j.sector or "",
        "type": j.contract_type or "Permanent",
        "salary": j.salary_display or "",
        "shift": j.shift or "",
        "status": JOB_STATUS.get(j.status, "brouillon"),
        "publishedAt": j.published_at.strftime("%Y-%m-%d") if j.published_at else "",
        "expiresAt": j.expires_at.strftime("%Y-%m-%d") if j.expires_at else "",
        "applications": count,
        "experience": j.experience_level or "",
        "skills": j.skills or "",
        "benefits": j.benefits or "",
        "description": j.description or "",
        "responsibilities": j.responsibilities or "",
        "qualifications": j.qualifications or "",
        "slug": j.slug,
    }


def _candidate(c: Candidate) -> dict:
    user = c.user
    app = c.applications[0] if c.applications else None
    langs = [x.strip() for x in (c.languages or "Français").split(",") if x.strip()]
    skills = [x.strip() for x in (c.skills or "").split(",") if x.strip()]
    return {
        "id": c.id,
        "firstName": user.first_name if user else "",
        "lastName": user.last_name if user else "",
        "email": user.email if user else "",
        "phone": user.phone if user else "",
        "city": c.city or "",
        "title": c.title or "",
        "sector": c.sector or "",
        "experience": c.years_experience or 0,
        "level": c.experience_level or "",
        "availability": c.availability or "",
        "status": APP_STATUS.get(app.status, c.pipeline_status or "nouveau") if app else (c.pipeline_status or "nouveau"),
        "languages": langs or ["Français"],
        "recruiterId": c.assigned_recruiter_id or "",
        "createdAt": c.created_at.strftime("%Y-%m-%d") if c.created_at else "",
        "lastActivity": c.updated_at.strftime("%Y-%m-%d") if c.updated_at else "",
        "skills": skills,
        "salaryMin": c.desired_salary_min or 0,
        "salaryMax": c.desired_salary_max or 0,
        "shift": c.shift_preference or "",
        "education": [{"school": e.school, "diploma": e.diploma or "", "year": e.year or ""} for e in c.education],
        "experiences": [{"company": e.company, "role": e.role, "years": e.years or ""} for e in c.experiences],
        "bio": c.bio or "",
        "jobId": app.job_id if app else "",
        "clientId": app.job.company_id if app and app.job else "",
    }


def _mission(m: RecruitmentMission, applications: list[Application]) -> dict:
    job_ids = set()
    if m.job_id:
        job_ids.add(m.job_id)
    linked = getattr(m, "linked_jobs", None) or []
    if hasattr(linked, "id") and not isinstance(linked, (list, tuple)):
        job_ids.add(linked.id)
    else:
        try:
            for job in linked:
                job_ids.add(job.id)
        except TypeError:
            pass
    pipeline = []
    stage_map: dict[str, str] = {}
    for app in applications:
        if app.job_id not in job_ids:
            continue
        stage = stage_for(app.status)
        if not stage:
            continue
        pipeline.append(
            {
                "applicationId": app.id,
                "candidateId": app.candidate_id,
                "stage": stage,
                "status": app.status.value,
            }
        )
        stage_map[app.candidate_id] = stage
    return {
        "id": m.id,
        "clientId": m.company_id,
        "jobId": m.job_id or "",
        "title": m.title,
        "seats": m.seats,
        "recruiterId": m.recruiter_id or "",
        "start": m.start_date or "",
        "due": m.due_date or "",
        "status": MISSION_STATUS.get(m.status, "en-cours"),
        "value": m.value or 0,
        "commission": m.commission or 0,
        "progress": m.progress or 0,
        "stageMap": stage_map,
        "pipeline": pipeline,
    }


def _contract(c: Contract) -> dict:
    latest = c.signatures[-1] if getattr(c, "signatures", None) else None
    return {
        "id": c.id,
        "clientId": c.company_id,
        "type": c.type,
        "start": c.start_date or "",
        "end": c.end_date or "",
        "commission": c.commission_percent or 0,
        "terms": c.terms or "",
        "status": c.status.value if c.status else "",
        "document": c.document_name or "",
        "signed": bool(latest),
        "signedAt": latest.signed_at.strftime("%Y-%m-%d %H:%M") if latest and latest.signed_at else "",
        "signerName": latest.signer_name if latest else "",
        "documentHash": latest.document_hash if latest else "",
    }


def _interview(i: Interview) -> dict:
    when = i.scheduled_at.strftime("%Y-%m-%d %H:%M") if i.scheduled_at else ""
    return {
        "id": i.id,
        "candidateId": i.candidate_id,
        "clientId": i.company_id or "",
        "type": INTERVIEW_TYPE.get(i.type.value if i.type else "", i.type.value if i.type else "Talendus"),
        "at": when,
        "location": i.location or "",
        "recruiterId": i.recruiter_id or "",
        "status": i.status.value if i.status else "SCHEDULED",
        "jobId": i.job_id or "",
    }


def _invoice(i: Invoice) -> dict:
    return {
        "id": i.number,
        "apiId": i.id,
        "clientId": i.company_id,
        "missionId": i.mission_id or "",
        "amount": i.amount,
        "date": i.issued_at or "",
        "due": i.due_date or "",
        "status": INVOICE_STATUS.get(i.status, "brouillon"),
    }


def _payment(p: Payment) -> dict:
    method = {"TRANSFER": "Virement", "CHEQUE": "Chèque", "CARD": "Carte", "OTHER": "Autre"}.get(
        p.method.value if p.method else "", "Virement"
    )
    return {
        "id": p.id,
        "invoiceId": p.invoice.number if p.invoice else p.invoice_id,
        "amount": p.amount,
        "date": p.paid_at or "",
        "method": method,
    }


def _note(n: InternalNote) -> dict:
    return {
        "id": n.id,
        "entity": n.entity_type,
        "entityId": n.entity_id,
        "authorId": n.author_id,
        "text": n.text,
        "at": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else "",
    }


def _notification(n: Notification) -> dict:
    return {
        "id": n.id,
        "type": n.type.value.lower() if n.type else "admin",
        "text": n.title + (" — " + n.message if n.message else ""),
        "at": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else "",
        "read": n.is_read,
        "href": n.href or "#/notifications",
    }
