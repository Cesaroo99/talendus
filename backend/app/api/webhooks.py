from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.errors import ok
from app.integrations.errors import IntegrationError
from app.integrations.inbound import ingest, require_webhook_secret, verify_hmac
from app.integrations.esignature.service import apply_esignature_event
from app.integrations.payments.paypal import apply_paypal_event, verify_paypal_transmission
from app.services import stripe_billing

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    event = stripe_billing.construct_event(payload, signature)
    event_id = str(event.get("id") or "")
    meta = ingest(db, provider="stripe", event_id=event_id, event_type=event.get("type"), payload=payload)
    if not meta["duplicate"]:
        stripe_billing.apply_event(db, event)
    return ok({"received": True, "type": event.get("type"), "duplicate": meta["duplicate"]})


@router.post("/paypal")
async def paypal_webhook(request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    require_webhook_secret("paypal", settings.paypal_webhook_id)
    payload = await request.body()
    verify_paypal_transmission(dict(request.headers), payload)
    transmission_id = request.headers.get("paypal-transmission-id") or ""
    meta = ingest(
        db,
        provider="paypal",
        event_id=transmission_id,
        event_type=request.headers.get("paypal-event-type") or request.headers.get("paypal-auth-algo"),
        payload=payload,
    )
    if not meta["duplicate"]:
        apply_paypal_event(db, payload)
    return ok({"received": True, "duplicate": meta["duplicate"]})


@router.get("/whatsapp")
def whatsapp_verify(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
):
    secret = (get_settings().whatsapp_webhook_secret or "").strip()
    if not secret:
        raise IntegrationError("Webhook WhatsApp non configuré.", "INTEGRATION_NOT_CONFIGURED", provider="whatsapp")
    if hub_mode != "subscribe" or hub_verify_token != secret:
        raise IntegrationError("Vérification WhatsApp rejetée.", "INTEGRATION_FORBIDDEN", provider="whatsapp")
    return PlainTextResponse(hub_challenge or "")


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    require_webhook_secret("whatsapp", settings.whatsapp_webhook_secret)
    payload = await request.body()
    signature = request.headers.get("x-hub-signature-256", "")
    verify_hmac(settings.whatsapp_webhook_secret, payload, signature, header_name="x-hub-signature-256")
    ingest(db, provider="whatsapp", event_id="", event_type="whatsapp", payload=payload)
    return ok({"received": True})


@router.post("/esignature")
async def esignature_webhook(request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    require_webhook_secret("esignature", settings.esignature_webhook_secret)
    payload = await request.body()
    signature = request.headers.get("x-talendus-signature") or request.headers.get("x-docusign-signature-1") or ""
    verify_hmac(settings.esignature_webhook_secret, payload, signature)
    ingest(db, provider="esignature", event_id="", event_type="esignature", payload=payload)
    apply_esignature_event(db, payload)
    return ok({"received": True})
