from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import client_ip, require_roles
from app.errors import ok
from app.models import EmailLog, User
from app.models.enums import EmailType, UserRole
from app.schemas import ContactIn, PublicTalentProfileIn
from app.services.audit import audit
from app.services.capabilities import public_services
from app.services.email import email_actually_sent, send_email
from app.services import candidates as cand_svc
from app.services.spam import reject_honeypot

router = APIRouter(tags=["public"])


@router.get("/health")
def health():
    """Liveness : ne touche pas la base. Render s'en sert ; un 502 ici coupe tout le site."""
    return ok({"status": "ok", "service": "talendus-api", "env": get_settings().app_env})


@router.get("/services")
def public_site_services():
    """État public des services (paiements, contact, connexion) — aucun secret."""
    return ok(public_services())


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        from app.errors import AppError

        raise AppError(503, "Base de données indisponible.", "DB_UNAVAILABLE") from None
    return ok({"status": "ready", "service": "talendus-api", "db": True})


@router.get("/job-board")
def job_board(db: Session = Depends(get_db)):
    from app.services import jobs as jobs_service

    return ok(jobs_service.export_board(db))


@router.post("/contact")
def contact(payload: ContactIn, request: Request, db: Session = Depends(get_db)):
    reject_honeypot(payload.website_url)
    details = [
        payload.message,
        f"Entreprise : {payload.company}" if payload.company else "",
        f"Poste : {payload.title}" if payload.title else "",
        f"Secteur : {payload.sector}" if payload.sector else "",
        f"Lieu : {payload.location}" if payload.location else "",
        f"Contrat : {payload.contract_type}" if payload.contract_type else "",
        f"Postes : {payload.seats}" if payload.seats else "",
        f"Expérience : {payload.experience_level}" if payload.experience_level else "",
        f"Compétences : {payload.skills}" if payload.skills else "",
        f"Fonction : {payload.contact_role}" if payload.contact_role else "",
        f"Taille : {payload.company_size}" if payload.company_size else "",
        f"Quart : {payload.shift}" if payload.shift else "",
        f"Horaire : {payload.schedule}" if payload.schedule else "",
        f"Téléphone : {payload.phone}" if payload.phone else "",
    ]
    body = "\n".join(part for part in details if part)
    send_email(
        db,
        "info@talendus.ca",
        EmailType.ADMIN,
        "contact_alert",
        name=payload.name,
        link=body[:1500],
    )
    audit(
        db,
        "public.contact",
        None,
        "contact",
        None,
        client_ip(request),
        {"email": payload.email, "subject": payload.subject or payload.title or payload.company},
    )
    from app.services.prospects import upsert_prospect

    hiring = bool(payload.title or payload.company)
    first, last = (payload.name or "").strip(), ""
    parts = [p for p in (payload.name or "").split() if p]
    if parts:
        first, last = parts[0], " ".join(parts[1:])
    upsert_prospect(
        db,
        side="employer" if hiring else "candidate",
        email=payload.email,
        source="contact",
        first_name=first,
        last_name=last,
        phone=payload.phone or "",
        company_name=payload.company or "",
        title=payload.title or "",
        city=payload.location or "",
        sector=payload.sector or "",
        source_detail=payload.subject or "Formulaire contact",
        message=payload.message or "",
    )
    db.commit()
    hiring = bool(payload.title or payload.company)
    message = (
        "Votre besoin a bien été transmis à Talendus. Notre équipe va analyser les informations communiquées et vous contacter afin de mieux comprendre votre besoin et de définir avec vous le profil recherché."
        if hiring
        else "Message reçu. Un conseiller vous rejoint sous peu."
    )
    return ok(message=message)


def _form_text(form, key: str) -> str:
    value = form.get(key)
    if value is None or hasattr(value, "read"):
        return ""
    return str(value).strip()


def _talent_payload(raw: dict) -> PublicTalentProfileIn:
    try:
        return PublicTalentProfileIn.model_validate(raw)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc


@router.post("/talent-profile")
async def talent_profile(request: Request, db: Session = Depends(get_db)):
    content_type = (request.headers.get("content-type") or "").lower()
    cv_file = None
    cv_filename = None
    if "multipart/form-data" in content_type:
        form = await request.form()
        reject_honeypot(_form_text(form, "website_url"))
        payload = _talent_payload(
            {
                "first_name": _form_text(form, "first_name") or _form_text(form, "nom"),
                "last_name": _form_text(form, "last_name"),
                "email": _form_text(form, "email") or _form_text(form, "courriel"),
                "phone": _form_text(form, "phone") or _form_text(form, "tel") or None,
                "title": _form_text(form, "title") or _form_text(form, "metier") or None,
                "city": _form_text(form, "city") or _form_text(form, "region") or None,
                "sector": _form_text(form, "sector") or _form_text(form, "secteur") or None,
                "availability": _form_text(form, "availability") or None,
                "cv_url": _form_text(form, "cv_url") or _form_text(form, "cv") or None,
                "message": _form_text(form, "message") or None,
                "subject": _form_text(form, "subject") or _form_text(form, "objet") or None,
                "password": _form_text(form, "password") or None,
            }
        )
        upload = form.get("file") or form.get("cvfile")
        if upload is not None and hasattr(upload, "read"):
            data = await upload.read()
            if data:
                cv_file = data
                cv_filename = (getattr(upload, "filename", None) or "").strip() or "cv"
    else:
        raw = await request.json()
        reject_honeypot(str((raw or {}).get("website_url") or ""))
        payload = _talent_payload(raw)
    result = cand_svc.submit_public_talent(
        db, payload, client_ip(request), cv_file=cv_file, cv_filename=cv_filename
    )
    return ok(result, message="Profil reçu. Un conseiller Talendus vous rejoint sous peu.")


@router.post("/ops/tick")
def ops_tick(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE, UserRole.RECRUITER))):
    from app.services.scheduler import run_ops_tick

    return ok(run_ops_tick(), message="Relances internes exécutées.")


emails_router = APIRouter(prefix="/emails", tags=["emails"])


@emails_router.get("")
def list_emails(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    rows = db.scalars(select(EmailLog).order_by(EmailLog.created_at.desc()).limit(limit)).all()
    return ok(
        [
            {
                "id": r.id,
                "to_email": r.to_email,
                "type": r.type.value,
                "subject": r.subject,
                "body": r.body,
                "status": r.status.value,
                "error": r.error,
                "attempts": r.attempts,
                "delivered": email_actually_sent(r),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    )
