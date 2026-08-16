from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import client_ip, require_roles
from app.errors import ok
from app.models import EmailLog, User
from app.models.enums import EmailType, UserRole
from app.schemas import ContactIn
from app.services.audit import audit
from app.services.email import send_email

router = APIRouter(tags=["public"])


@router.get("/health")
def health():
    """Liveness : ne touche pas la base. Render s'en sert ; un 502 ici coupe tout le site."""
    return ok({"status": "ok", "service": "talendus-api", "env": get_settings().app_env})


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        from app.errors import AppError

        raise AppError(503, "Base de données indisponible.", "DB_UNAVAILABLE") from None
    return ok({"status": "ready", "service": "talendus-api"})


@router.get("/job-board")
def job_board(db: Session = Depends(get_db)):
    from app.services import jobs as jobs_service

    return ok(jobs_service.export_board(db))


@router.post("/contact")
def contact(payload: ContactIn, request: Request, db: Session = Depends(get_db)):
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
        f"Téléphone : {payload.phone}" if payload.phone else "",
    ]
    body = "\n".join(part for part in details if part)
    send_email(
        db,
        "info@talendus.ca",
        EmailType.ADMIN,
        "welcome",
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
    db.commit()
    hiring = bool(payload.title or payload.company)
    message = (
        "Votre besoin a bien été transmis à Talendus. Notre équipe va analyser les informations communiquées et vous contacter afin de mieux comprendre votre besoin et de définir avec vous le profil recherché."
        if hiring
        else "Message reçu. Un conseiller vous rejoint sous peu."
    )
    return ok(message=message)


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
                "status": r.status.value,
                "error": r.error,
                "attempts": r.attempts,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    )
