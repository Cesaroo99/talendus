from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import AppError, ok
from app.models import User
from app.models.enums import UserRole
from app.models.prospect import ProspectSend
from app.schemas import ProspectBulkSendIn, ProspectIn, ProspectNoteIn, ProspectPatchIn, ProspectSendIn
from app.services import prospects as svc

router = APIRouter(prefix="/admin/prospects", tags=["prospects"])


def _staff(user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN))) -> User:
    return user


def _req(payload: ProspectSendIn) -> svc.SendRequest:
    return svc.SendRequest(
        template_key=payload.template_key,
        subject=payload.subject,
        body=payload.body,
        invoice_ids=payload.invoice_ids,
        contract_ids=payload.contract_ids,
        force=payload.force,
    )


def _row_sends(db: Session, prospect_id: str) -> list[ProspectSend]:
    return list(
        db.scalars(
            select(ProspectSend).where(ProspectSend.prospect_id == prospect_id).order_by(ProspectSend.created_at.desc())
        ).all()
    )


def _detail(db: Session, staff: User, prospect_id: str) -> dict:
    row = svc.get_prospect(db, prospect_id)
    sent = svc.sent_keys_map(db, [row.id])
    return {
        **svc.serialize_prospect(row, sent.get(row.id, [])),
        "proposals": svc.proposals_for(db, row, staff),
        "attachments": svc.available_attachments(db, row),
        "sends": [svc.serialize_send(item) for item in _row_sends(db, row.id)],
        "dossier": svc.dossier_for(db, row),
        "stages": [{"key": k, "label": l} for k, l in svc.stages_for(row.side)],
    }


@router.get("")
@router.get("/")
def list_prospects(
    side: str,
    stage: str | None = None,
    q: str | None = None,
    source: str | None = None,
    city: str | None = None,
    sector: str | None = None,
    db: Session = Depends(get_db),
    _staff_user: User = Depends(_staff),
):
    side = svc.normalize_side(side)
    rows = svc.list_prospects(db, side=side, stage=stage, q=q, source=source, city=city, sector=sector)
    if any(row.side != side for row in rows):
        raise AppError(500, "Les deux bases ne doivent pas être mélangées.", "SIDE_MIXED")
    # sync_known_people crée des fiches : sans commit, Écrire / Fiche 404 « Prospect introuvable ».
    db.commit()
    sent = svc.sent_keys_map(db, [row.id for row in rows])
    options = svc.filter_options(db, side)
    return ok(
        [svc.serialize_prospect(row, sent.get(row.id, [])) for row in rows],
        meta={
            "side": side,
            "stages": [{"key": k, "label": l} for k, l in svc.stages_for(side)],
            "catalog": svc.catalog(side),
            "sources": [{"key": k, "label": l} for k, l in svc.SOURCE_LABELS],
            "cities": options["cities"],
            "sectors": options["sectors"],
        },
    )


@router.get("/templates")
@router.get("/catalog")
def templates(side: str | None = None, _staff_user: User = Depends(_staff)):
    return ok(svc.catalog(side) if side else svc.catalog())


@router.post("/broadcast")
@router.post("/send-bulk")
def broadcast(payload: ProspectBulkSendIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    result = svc.send_bulk(db, staff, payload.ids, _req(payload))
    db.commit()
    failed = len(result["failed"])
    message = f"{len(result['sent'])} parti(s), {len(result['skipped'])} déjà contacté(s) pour ce message."
    if failed:
        message += f" {failed} non parti(s) — statut inchangé."
    return ok(result, message=message)


@router.post("")
def create_prospect(payload: ProspectIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    try:
        row = svc.create_prospect(db, staff, payload.model_dump())
        db.commit()
        db.refresh(row)
    except IntegrityError:
        db.rollback()
        raise AppError(409, "Ce prospect existe déjà de ce côté.", "PROSPECT_EXISTS") from None
    return ok(svc.serialize_prospect(row), message="Prospect ajouté.")


@router.get("/p/{prospect_id}/proposals")
@router.get("/{prospect_id}/proposals")
def proposals(prospect_id: str, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.get_prospect(db, prospect_id)
    return ok(svc.proposals_for(db, row, staff))


@router.post("/p/{prospect_id}/send")
@router.post("/{prospect_id}/send")
def send_one(prospect_id: str, payload: ProspectSendIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.get_prospect(db, prospect_id)
    result = svc.send_to_prospect(db, staff, row, _req(payload))
    db.commit()
    if not result.get("delivered"):
        raise AppError(
            502,
            (
                f"Le courriel n’a pas quitté le serveur vers {result.get('to_email')}. "
                f"{result.get('email_error') or ''} Le statut du prospect n’a pas été changé."
            ).strip(),
            "SMTP_SEND_FAILED",
        )
    return ok(result, message=f"Parti vers {result['to_email']}.")


@router.get("/p/{prospect_id}")
@router.get("/{prospect_id}")
def get_prospect(prospect_id: str, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    return ok(_detail(db, staff, prospect_id))


@router.post("/p/{prospect_id}/notes")
@router.post("/{prospect_id}/notes")
def add_prospect_note(prospect_id: str, payload: ProspectNoteIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    note = svc.add_prospect_note(db, staff, prospect_id, payload.text)
    db.commit()
    db.refresh(note)
    return ok(
        {
            "id": note.id,
            "text": note.text,
            "author_id": note.author_id,
            "author_name": staff.full_name,
            "created_at": note.created_at.isoformat() if note.created_at else None,
        },
        message="Note enregistrée.",
    )


@router.patch("/p/{prospect_id}")
@router.patch("/{prospect_id}")
def patch_prospect(prospect_id: str, payload: ProspectPatchIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.patch_prospect(db, prospect_id, payload.model_dump(exclude_unset=True), actor=staff)
    db.commit()
    db.refresh(row)
    return ok(svc.serialize_prospect(row), message="Prospect mis à jour.")
