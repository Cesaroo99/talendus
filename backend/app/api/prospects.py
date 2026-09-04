from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import ProspectBulkSendIn, ProspectIn, ProspectPatchIn, ProspectSendIn
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


@router.get("")
def list_prospects(
    side: str | None = None,
    stage: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    _staff_user: User = Depends(_staff),
):
    rows = svc.list_prospects(db, side=side, stage=stage, q=q)
    sent = svc.sent_keys_map(db, [row.id for row in rows])
    return ok(
        [svc.serialize_prospect(row, sent.get(row.id, [])) for row in rows],
        meta={
            "candidate_stages": [{"key": k, "label": l} for k, l in svc.CANDIDATE_STAGES],
            "employer_stages": [{"key": k, "label": l} for k, l in svc.EMPLOYER_STAGES],
            "catalog": svc.catalog(side) if side else svc.catalog(),
        },
    )


@router.get("/catalog")
def catalog(side: str | None = None, _staff_user: User = Depends(_staff)):
    return ok(svc.catalog(side))


@router.post("/send-bulk")
def send_bulk(payload: ProspectBulkSendIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    result = svc.send_bulk(db, staff, payload.ids, _req(payload))
    db.commit()
    sent_n = len(result["sent"])
    skip_n = len(result["skipped"])
    return ok(result, message=f"{sent_n} envoyé(s), {skip_n} déjà contacté(s) pour ce message.")


@router.post("")
def create_prospect(payload: ProspectIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.create_prospect(db, staff, payload.model_dump())
    db.commit()
    db.refresh(row)
    return ok(svc.serialize_prospect(row), message="Prospect ajouté.")


@router.get("/{prospect_id}")
def get_prospect(prospect_id: str, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.get_prospect(db, prospect_id)
    sent = svc.sent_keys_map(db, [row.id])
    return ok(
        {
            **svc.serialize_prospect(row, sent.get(row.id, [])),
            "proposals": svc.proposals_for(db, row, staff),
            "attachments": svc.available_attachments(db, row),
            "sends": [svc.serialize_send(s) for s in row_sends(db, row.id)],
        }
    )


def row_sends(db: Session, prospect_id: str):
    from sqlalchemy import select
    from app.models.prospect import ProspectSend

    return list(db.scalars(select(ProspectSend).where(ProspectSend.prospect_id == prospect_id).order_by(ProspectSend.created_at.desc())).all())


@router.patch("/{prospect_id}")
def patch_prospect(prospect_id: str, payload: ProspectPatchIn, db: Session = Depends(get_db), _staff_user: User = Depends(_staff)):
    row = svc.patch_prospect(db, prospect_id, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(row)
    return ok(svc.serialize_prospect(row), message="Prospect mis à jour.")


@router.get("/{prospect_id}/proposals")
def proposals(prospect_id: str, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.get_prospect(db, prospect_id)
    return ok(svc.proposals_for(db, row, staff))


@router.post("/{prospect_id}/send")
def send_one(prospect_id: str, payload: ProspectSendIn, db: Session = Depends(get_db), staff: User = Depends(_staff)):
    row = svc.get_prospect(db, prospect_id)
    result = svc.send_to_prospect(db, staff, row, _req(payload))
    db.commit()
    return ok(result, message=f"Envoyé à {result['to_email']}.")
