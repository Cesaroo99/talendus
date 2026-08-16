"""Ingestion de webhooks : signature, idempotence, sans stockage de payload sensible."""

from __future__ import annotations

import hashlib
import hmac
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.integrations.errors import IntegrationError
from app.models.enums import utcnow
from app.models.integrations import WebhookEvent

logger = logging.getLogger("talendus.integrations.webhooks")


def payload_hash(payload: bytes) -> str:
    return hashlib.sha256(payload or b"").hexdigest()


def ingest(
    db: Session,
    *,
    provider: str,
    event_id: str,
    event_type: str | None,
    payload: bytes,
) -> dict:
    if not event_id:
        event_id = payload_hash(payload)
    existing = db.scalar(
        select(WebhookEvent).where(WebhookEvent.provider == provider, WebhookEvent.event_id == event_id)
    )
    if existing:
        logger.info("webhook duplicate provider=%s event_id=%s", provider, event_id)
        return {"duplicate": True, "id": existing.id, "event_id": event_id, "provider": provider}
    row = WebhookEvent(
        provider=provider,
        event_id=event_id,
        event_type=event_type,
        status="received",
        payload_hash=payload_hash(payload),
        processed_at=utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"duplicate": False, "id": row.id, "event_id": event_id, "provider": provider, "event_type": event_type}


def verify_hmac(secret: str, payload: bytes, signature: str, *, header_name: str = "signature") -> None:
    if not secret:
        raise IntegrationError("Webhook non configuré.", "INTEGRATION_NOT_CONFIGURED")
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    provided = signature.split("=")[-1].strip() if signature else ""
    if not provided or not hmac.compare_digest(expected, provided):
        raise IntegrationError(
            "Signature de webhook invalide.",
            "INTEGRATION_SIGNATURE_INVALID",
            details=[{"field": header_name, "message": "Signature rejetée."}],
        )


def require_webhook_secret(provider: str, secret: str) -> None:
    if not (secret or "").strip():
        raise IntegrationError(
            f"Secret webhook {provider} manquant.",
            "INTEGRATION_NOT_CONFIGURED",
            provider=provider,
        )
