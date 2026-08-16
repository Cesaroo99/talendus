"""Endpoints d'intégrations — le front n'appelle jamais les API privées des fournisseurs."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import ok
from app.integrations.ai.openai import OpenAIService
from app.integrations.esignature.service import ESignatureService
from app.integrations.jobs.base import ExternalJobPayload
from app.integrations.jobs.sync import list_external_jobs, serialize_external_job, sync_from_provider, upsert_jobs
from app.integrations.maps.google import GoogleMapsService
from app.integrations.messaging.whatsapp import WhatsAppService
from app.integrations.payments.paypal import PayPalService
from app.integrations.registry import catalog, provider_status
from app.integrations.schemas import (
    AiCompleteIn,
    DistanceIn,
    EnvelopeIn,
    ExternalJobImportIn,
    GeocodeIn,
    JobSyncIn,
    PayPalCheckoutIn,
    WhatsAppSendIn,
)
from app.models import User
from app.models.enums import UserRole

router = APIRouter(prefix="/integrations", tags=["integrations"])
_staff = require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)
_admin = require_roles(UserRole.ADMIN)


@router.get("")
def list_integrations(_: User = Depends(_staff)):
    return ok(catalog())


@router.get("/linkedin")
def linkedin_public_status():
    status = provider_status("linkedin")
    return ok(
        {
            "configured": status["configured"],
            "share_enabled": True,
            "posting_enabled": status["configured"],
            "state": status["state"],
            "message": (
                "Publication LinkedIn prête (OAuth configuré)."
                if status["configured"]
                else "Partage d’offre via URL LinkedIn disponible. La publication automatique nécessite LINKEDIN_CLIENT_ID et LINKEDIN_CLIENT_SECRET."
            ),
        }
    )


@router.get("/status/{name}")
def get_integration(name: str, _: User = Depends(_staff)):
    return ok(provider_status(name))


@router.get("/jobs/external")
def list_imported_jobs(
    source: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(_staff),
):
    rows = list_external_jobs(db, source, limit)
    return ok([serialize_external_job(row) for row in rows])


@router.post("/jobs/import")
def import_jobs(payload: ExternalJobImportIn, db: Session = Depends(get_db), _: User = Depends(_staff)):
    jobs = [
        ExternalJobPayload(source=payload.source, **item.model_dump())
        for item in payload.jobs
    ]
    return ok(upsert_jobs(db, jobs), message="Offres externes enregistrées.")


@router.post("/jobs/sync")
def sync_jobs(payload: JobSyncIn, db: Session = Depends(get_db), _: User = Depends(_admin)):
    return ok(sync_from_provider(db, payload.source, payload.query))


@router.post("/whatsapp/send")
def send_whatsapp(payload: WhatsAppSendIn, _: User = Depends(_staff)):
    result = WhatsAppService().send(
        recipient=payload.recipient,
        template=payload.template,
        variables=payload.variables,
        message_type=payload.message_type,
    )
    return ok(result)


@router.post("/maps/geocode")
def geocode(payload: GeocodeIn, _: User = Depends(_staff)):
    return ok(GoogleMapsService().geocode(payload.address))


@router.post("/maps/distance")
def distance(payload: DistanceIn, _: User = Depends(_staff)):
    return ok(GoogleMapsService().distance(payload.origin, payload.destination))


@router.post("/ai/complete")
def ai_complete(payload: AiCompleteIn, _: User = Depends(_admin)):
    return ok(OpenAIService().complete(purpose=payload.purpose, prompt=payload.prompt, max_tokens=payload.max_tokens))


@router.post("/esignature/envelopes")
def create_envelope(payload: EnvelopeIn, _: User = Depends(_staff)):
    return ok(ESignatureService().create_document(title=payload.title, file_url=payload.file_url))


@router.post("/paypal/checkout")
def paypal_checkout(payload: PayPalCheckoutIn, _: User = Depends(_staff)):
    result = PayPalService().create_payment(
        amount=payload.amount,
        currency=payload.currency,
        invoice_id=payload.invoice_id,
    )
    return ok(
        {
            "provider": result.provider,
            "status": result.status,
            "amount": result.amount,
            "currency": result.currency,
            "reference": result.reference,
            "checkout_url": result.checkout_url,
            "invoice_id": result.invoice_id,
        }
    )
