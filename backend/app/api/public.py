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
    send_email(
        db,
        "info@talendus.ca",
        EmailType.ADMIN,
        "welcome",
        name=payload.name,
        link=payload.message[:500],
    )
    audit(
        db,
        "public.contact",
        None,
        "contact",
        None,
        client_ip(request),
        {"email": payload.email, "subject": payload.subject or payload.company},
    )
    db.commit()
    return ok(message="Message reçu. Un conseiller vous rejoint sous peu.")


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
