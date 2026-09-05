"""Projection des données API vers le format du back-office Talendus."""

import logging

from sqlalchemy import func, select
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
    Message,
    Notification,
    Payment,
    PortalDocument,
    RecruitmentMission,
    User,
)
from app.models.enums import ApplicationStatus, InterviewType, InvoiceStatus, JobStatus, MissionStatus, UserRole, utcnow
from app.services.hiring_requests import STATUS_COPY, serialize_request
from app.services.interviews import CALL_TYPES, LIVE_CALL_STATUSES, host_in_call
from app.services.pipeline import stage_for

logger = logging.getLogger("talendus.admin")

APP_STATUS = {
    ApplicationStatus.SUBMITTED: "nouveau",
    ApplicationStatus.RECEIVED: "nouveau",
    ApplicationStatus.UNDER_REVIEW: "qualifie",
    ApplicationStatus.SHORTLISTED: "presente",
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
    "SUPER_ADMIN": "admin",
    "RECRUITER": "recruiter",
    "FINANCE": "finance",
    "EDITOR": "editor",
}

CONTRACT_STATUS = {
    "ACTIVE": "Actif",
    "DRAFT": "À signer",
    "EXPIRED": "Expire bientôt",
}

SITE_PAGES = [
    {"id": "pg-home", "title": "Accueil", "slug": "/", "status": "publie"},
    {"id": "pg-employers", "title": "Entreprises", "slug": "/entreprises.html", "status": "publie"},
    {"id": "pg-jobs", "title": "Offres d’emploi", "slug": "/emplois.html", "status": "publie"},
    {"id": "pg-talent", "title": "Candidats", "slug": "/candidats.html", "status": "publie"},
    {"id": "pg-contact", "title": "Contact", "slug": "/contact.html", "status": "publie"},
    {"id": "pg-about", "title": "À propos", "slug": "/a-propos.html", "status": "publie"},
    {"id": "pg-services", "title": "Services", "slug": "/services.html", "status": "publie"},
    {"id": "pg-blog", "title": "Blog", "slug": "/blog.html", "status": "publie"},
]


def _editor_bootstrap(db: Session, user: User) -> dict:
    users = db.scalars(select(User).order_by(User.created_at.asc())).all()
    notif_stmt = select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())
    notifications = db.scalars(notif_stmt.limit(100)).all()
    from app.services.settings import get_json_setting

    testimonials = get_json_setting(db, "cms.testimonials", default=[])
    faqs = get_json_setting(db, "cms.faq", default=[])
    unread_messages = int(
        db.scalar(
            select(func.count()).select_from(Message).where(Message.recipient_id == user.id, Message.is_read.is_(False))
        )
        or 0
    )
    return {
        "live": True,
        "unreadMessages": unread_messages,
        "users": [_user(u) for u in users if u.role.value in {"ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"}],
        "clients": [],
        "jobs": [],
        "candidates": [],
        "missions": [],
        "hiringRequests": [],
        "applications": [],
        "contracts": [],
        "notes": [],
        "notifications": [_notification(n) for n in notifications],
        "interviews": [],
        "invoices": [],
        "payments": [],
        "documents": [],
        "pages": [dict(page) for page in SITE_PAGES],
        "testimonials": testimonials if isinstance(testimonials, list) else [],
        "faqs": faqs if isinstance(faqs, list) else [],
        "jobMatches": [],
        "monthly": _monthly([], []),
        "stats": {
            "candidates": 0,
            "clients": 0,
            "jobs": 0,
            "publishedJobs": 0,
            "applications": 0,
            "placements": 0,
            "openMissions": 0,
        },
        "activities": [],
    }


def _finance_bootstrap(db: Session, user: User) -> dict:
    invoices = db.scalars(
        select(Invoice).options(joinedload(Invoice.company), joinedload(Invoice.mission)).order_by(Invoice.created_at.desc())
    ).unique().all()
    payments = db.scalars(select(Payment).options(joinedload(Payment.invoice)).order_by(Payment.created_at.desc())).unique().all()
    notif_stmt = select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())
    notifications = db.scalars(notif_stmt.limit(100)).all()
    unread_messages = int(
        db.scalar(
            select(func.count()).select_from(Message).where(Message.recipient_id == user.id, Message.is_read.is_(False))
        )
        or 0
    )
    users = db.scalars(select(User).order_by(User.created_at.asc())).all()
    paid = [row for row in invoices if row.status == InvoiceStatus.PAID]
    return {
        "live": True,
        "unreadMessages": unread_messages,
        "users": [_user(u) for u in users if u.role.value in {"ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"}],
        "clients": [],
        "jobs": [],
        "candidates": [],
        "missions": [],
        "hiringRequests": [],
        "applications": [],
        "contracts": [],
        "notes": [],
        "notifications": [_notification(n) for n in notifications],
        "interviews": [],
        "invoices": [_invoice(i) for i in invoices],
        "payments": [_payment(p) for p in payments],
        "documents": [],
        "pages": [dict(page) for page in SITE_PAGES],
        "testimonials": [],
        "faqs": [],
        "jobMatches": [],
        "monthly": _monthly([], invoices),
        "stats": {
            "candidates": 0,
            "clients": 0,
            "jobs": 0,
            "publishedJobs": 0,
            "applications": 0,
            "placements": 0,
            "openMissions": 0,
            "paidInvoices": len(paid),
        },
        "activities": [],
    }


def bootstrap(db: Session, user: User | None = None) -> dict:
    if user and user.role == UserRole.EDITOR:
        return _editor_bootstrap(db, user)
    if user and user.role == UserRole.FINANCE:
        return _finance_bootstrap(db, user)
    users = db.scalars(select(User).order_by(User.created_at.asc())).all()
    companies = db.scalars(select(Company).options(joinedload(Company.owner)).order_by(Company.name.asc())).unique().all()
    jobs = db.scalars(select(JobOffer).options(joinedload(JobOffer.company)).order_by(JobOffer.created_at.desc())).unique().all()
    candidates = db.scalars(
        select(Candidate).options(
            joinedload(Candidate.user),
            selectinload(Candidate.experiences),
            selectinload(Candidate.education),
            selectinload(Candidate.resumes),
            selectinload(Candidate.applications).joinedload(Application.job),
        )
    ).unique().all()
    missions = db.scalars(
        select(RecruitmentMission)
        .options(joinedload(RecruitmentMission.company), selectinload(RecruitmentMission.linked_jobs))
        .order_by(RecruitmentMission.created_at.desc())
    ).unique().all()
    try:
        contracts = db.scalars(select(Contract).options(selectinload(Contract.signatures))).all()
    except Exception:
        logger.exception("bootstrap: lecture des mandats impossible")
        db.rollback()
        contracts = []
    notes = db.scalars(select(InternalNote).order_by(InternalNote.created_at.desc()).limit(200)).all()
    notif_stmt = select(Notification).order_by(Notification.created_at.desc())
    if user:
        notif_stmt = notif_stmt.where(Notification.user_id == user.id)
    notifications = db.scalars(notif_stmt.limit(100)).all()
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
    portal_docs = db.scalars(select(PortalDocument).order_by(PortalDocument.created_at.desc())).all()
    from app.services.settings import get_json_setting

    testimonials = get_json_setting(db, "cms.testimonials", default=[])
    faqs = get_json_setting(db, "cms.faq", default=[])

    unread_messages = 0
    if user:
        unread_messages = int(
            db.scalar(
                select(func.count()).select_from(Message).where(Message.recipient_id == user.id, Message.is_read.is_(False))
            )
            or 0
        )

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

    published = sum(1 for j in jobs if j.status == JobStatus.PUBLISHED)
    placed = sum(1 for a in applications if a.status == ApplicationStatus.HIRED)
    open_missions = sum(
        1
        for m in missions
        if m.status
        not in {MissionStatus.CLOSED, MissionStatus.FILLED, MissionStatus.CANCELLED}
    )
    return {
        "live": True,
        "unreadMessages": unread_messages,
        "users": [_user(u) for u in users if u.role.value in {"ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"}],
        "clients": [_company(c) for c in companies],
        "jobs": [_job(j, applications) for j in jobs],
        "candidates": [_candidate(c) for c in candidates],
        "missions": [_mission(m, applications) for m in missions],
        "hiringRequests": [serialize_request(m) for m in missions],
        "applications": [_application(a) for a in applications[:200]],
        "contracts": [_contract(c) for c in contracts],
        "notes": [_note(n) for n in notes],
        "notifications": [_notification(n) for n in notifications],
        "interviews": [_interview(i) for i in interviews],
        "invoices": [_invoice(i) for i in invoices],
        "payments": [_payment(p) for p in payments],
        "documents": _documents(candidates, portal_docs),
        "pages": [dict(page) for page in SITE_PAGES],
        "testimonials": testimonials if isinstance(testimonials, list) else [],
        "faqs": faqs if isinstance(faqs, list) else [],
        "jobMatches": job_matches,
        "monthly": _monthly(applications, invoices),
        "stats": {
            "candidates": len(candidates),
            "clients": len(companies),
            "jobs": len(jobs),
            "publishedJobs": published,
            "applications": len(applications),
            "placements": placed,
            "openMissions": open_missions,
        },
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
        "hasAvatar": bool(u.avatar_path),
    }


def _company(c: Company) -> dict:
    owner = c.owner
    return {
        "id": c.id,
        "name": c.name,
        "legalName": c.legal_name or "",
        "address": c.address or "",
        "province": c.province or "Québec",
        "country": c.country or "Canada",
        "sector": c.sector or "",
        "city": c.city or "",
        "contact": c.contact_name or "",
        "email": c.email or "",
        "phone": c.phone or "",
        "status": "Actif" if c.status and c.status.value == "ACTIVE" else "Prospect",
        "recruiterId": c.assigned_recruiter_id or "",
        "employees": c.employees or 0,
        "website": c.website or "",
        "description": c.description or "",
        "sizeLabel": c.size_label or "",
        "ownerUserId": c.owner_user_id or "",
        "ownerEmail": owner.email if owner else (c.email or ""),
        "lastLoginAt": owner.last_login_at.isoformat() if owner and owner.last_login_at else "",
        "emailVerified": bool(owner.is_email_verified) if owner else False,
        "accountActive": bool(owner.is_active) if owner else True,
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
        "url": f"/emploi-{j.slug}.html" if j.slug else "",
        "statusKey": j.status.value if j.status else "",
    }


def _candidate_cv_summary(c: Candidate) -> str:
    from app.services.resume_parse import summary_from_storage

    resumes = list(c.resumes or [])
    primary = next((row for row in resumes if row.is_primary), None) or (resumes[0] if resumes else None)
    return summary_from_storage(primary.parse_json, profile=c) if primary else ""


def _candidate(c: Candidate) -> dict:
    user = c.user
    apps = sorted(c.applications or [], key=lambda a: a.created_at or utcnow(), reverse=True)
    app = apps[0] if apps else None
    langs = [x.strip() for x in (c.languages or "Français").split(",") if x.strip()]
    skills = [x.strip() for x in (c.skills or "").split(",") if x.strip()]
    return {
        "id": c.id,
        "userId": user.id if user else "",
        "hasAvatar": bool(user and user.avatar_path),
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
        "address": c.address or "",
        "province": c.province or "Québec",
        "mobility": c.mobility or "",
        "contractType": c.contract_type or "",
        "workStatus": c.work_status or "",
        "jobSearchStatus": c.job_search_status.value if c.job_search_status else "",
        "workPreferences": c.work_preferences or "",
        "educationLevel": c.education_level or "",
        "cvSummary": _candidate_cv_summary(c),
        "lastLoginAt": user.last_login_at.isoformat() if user and user.last_login_at else "",
        "emailVerified": bool(user.is_email_verified) if user else False,
        "accountActive": bool(user.is_active) if user else True,
        "jobId": app.job_id if app else "",
        "applicationId": app.id if app else "",
        "clientId": app.job.company_id if app and app.job else "",
        "applications": [_application(a) for a in apps],
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
        "statusKey": m.status.value if m.status else "",
        "statusLabel": (STATUS_COPY.get(m.status) or (m.status.value if m.status else "", ""))[0],
        "location": m.location or "",
        "sector": m.sector or "",
        "skills": m.skills or "",
        "notes": m.notes or "",
        "contactName": m.contact_name or "",
        "salary": m.salary_display or "",
        "contractType": m.contract_type or "",
    }


def _dt(value) -> str:
    if not value:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M")
    return str(value)


def _contract(c: Contract) -> dict:
    from app.services.contracts import _role_from_terms, client_status, lifecycle, mandate_window
    from app.services.pdf_docs import PARTY_CLIENT, PARTY_TALENDUS

    signatures = list(getattr(c, "signatures", None) or [])
    client = None
    talendus = None
    for item in signatures:
        party = (getattr(item, "party", None) or PARTY_CLIENT).upper()
        if party == PARTY_TALENDUS:
            talendus = item
        elif party == PARTY_CLIENT:
            client = item
    status = client_status(c)
    _, _, days = mandate_window(c.start_date, c.end_date)
    role = _role_from_terms(c.terms) or ""
    status_label = {
        "signed": "Signé",
        "opened": "Ouvert",
        "received": "Reçu",
        "not_sent": "Non envoyé",
    }.get(status, CONTRACT_STATUS.get(c.status.value if c.status else "", c.status.value if c.status else ""))
    return {
        "id": c.id,
        "clientId": c.company_id,
        "type": c.type,
        "template": c.template_key or "succes",
        "start": c.start_date or "",
        "end": c.end_date or "",
        "durationDays": days,
        "role": role,
        "canEdit": not bool(talendus or c.talendus_signed_at or c.sent_at or client or c.client_signed_at),
        "commission": c.commission_percent or 0,
        "terms": c.terms or "",
        "status": status_label,
        "document": c.document_name or "",
        "signed": bool(client or c.client_signed_at),
        "talendusSigned": bool(talendus or c.talendus_signed_at),
        "clientSigned": bool(client or c.client_signed_at),
        "clientStatus": status,
        "lifecycle": lifecycle(c),
        "sentAt": _dt(c.sent_at),
        "openedAt": _dt(c.opened_at),
        "talendusSignedAt": _dt(c.talendus_signed_at),
        "clientSignedAt": _dt(c.client_signed_at),
        "signedAt": _dt(c.client_signed_at) or (client.signed_at.strftime("%Y-%m-%d %H:%M") if client and client.signed_at else ""),
        "signerName": client.signer_name if client else "",
        "documentHash": client.document_hash if client else "",
        "talendusSigner": talendus.signer_name if talendus else "",
        "reminderCount": int(getattr(c, "reminder_count", 0) or 0),
        "pdfPath": f"/api/contracts/{c.id}/pdf",
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
        "meetingUrl": i.meeting_url or "",
        "typeKey": i.type.value if i.type else "TALENDUS",
        "candidateName": (i.candidate.user.full_name if i.candidate and i.candidate.user else ""),
        "in_app_call": i.type in CALL_TYPES and i.status in LIVE_CALL_STATUSES,
        "call_video": i.type != InterviewType.PHONE,
        "candidate_can_start": bool(getattr(i, "candidate_can_start", False)),
        "call_open": bool(getattr(i, "call_opened_at", None)),
        "host_in_call": host_in_call(i),
        "can_close_call": i.status in LIVE_CALL_STATUSES,
        "candidateUserId": i.candidate.user.id if i.candidate and i.candidate.user else "",
        "candidateHasAvatar": bool(i.candidate.user.avatar_path) if i.candidate and i.candidate.user else False,
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
        "notes": i.notes or "",
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


def _size_label(n: int | None) -> str:
    size = int(n or 0)
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} Mo".replace(".", ",")
    if size >= 1024:
        return f"{max(1, round(size / 1024))} Ko"
    return f"{size} o"


def _documents(candidates: list[Candidate], portal_docs: list[PortalDocument]) -> list[dict]:
    from app.services.resume_parse import is_previewable, summary_from_storage

    docs = []
    for cand in candidates:
        for resume in cand.resumes or []:
            mime = resume.mime_type or ""
            docs.append(
                {
                    "id": resume.id,
                    "name": resume.original_name,
                    "entity": "candidate",
                    "entityId": cand.id,
                    "size": _size_label(resume.size_bytes),
                    "kind": "resume",
                    "mimeType": mime,
                    "summary": summary_from_storage(resume.parse_json, profile=cand),
                    "previewable": is_previewable(mime, resume.original_name),
                    "url": f"/api/candidates/resumes/{resume.id}/file",
                    "previewUrl": f"/api/candidates/resumes/{resume.id}/preview",
                }
            )
    for row in portal_docs:
        mime = row.mime_type or ""
        docs.append(
            {
                "id": row.id,
                "name": row.original_name,
                "entity": row.owner_type,
                "entityId": row.owner_id,
                "size": _size_label(row.size_bytes),
                "kind": row.kind,
                "mimeType": mime,
                "summary": "",
                "previewable": is_previewable(mime, row.original_name),
                "url": f"/api/documents/{row.id}/file",
                "previewUrl": f"/api/documents/{row.id}/preview",
            }
        )
    return docs


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
        "userId": n.user_id,
    }


def _application(a: Application) -> dict:
    return {
        "id": a.id,
        "applicationId": a.id,
        "candidateId": a.candidate_id,
        "jobId": a.job_id,
        "jobTitle": a.job.title if a.job else "",
        "status": APP_STATUS.get(a.status, "nouveau"),
        "statusKey": a.status.value if a.status else "",
        "stage": stage_for(a.status) or "",
        "matchScore": a.match_score,
        "createdAt": a.created_at.strftime("%Y-%m-%d") if a.created_at else "",
    }


def _monthly(applications: list[Application], invoices: list[Invoice]) -> dict:
    now = utcnow()
    keys: list[str] = []
    labels: list[str] = []
    months_fr = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
    for offset in range(7, -1, -1):
        year = now.year
        month = now.month - offset
        while month <= 0:
            month += 12
            year -= 1
        keys.append(f"{year:04d}-{month:02d}")
        labels.append(months_fr[month - 1])
    index = {key: i for i, key in enumerate(keys)}
    apps = [0] * 8
    placements = [0] * 8
    revenue = [0] * 8
    for row in applications:
        if not row.created_at:
            continue
        key = row.created_at.strftime("%Y-%m")
        if key not in index:
            continue
        apps[index[key]] += 1
        if row.status == ApplicationStatus.HIRED:
            placements[index[key]] += 1
    for invoice in invoices:
        if invoice.status != InvoiceStatus.PAID:
            continue
        key = str(invoice.issued_at or "")[:7]
        if (not key or len(key) < 7) and invoice.created_at:
            key = invoice.created_at.strftime("%Y-%m")
        if key in index:
            revenue[index[key]] += invoice.amount or 0
    return {"applications": apps, "placements": placements, "revenue": revenue, "months": labels}
