"""Checkout Stripe branché sur `invoices.stripe_payment_intent_id` (sans changement de schéma)."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.errors import AppError
from app.models import Invoice, Payment, User
from app.models.enums import InvoiceStatus, PaymentMethod, utcnow
from app.services.audit import audit
from app.services.invoices import get_invoice, serialize_invoice

logger = logging.getLogger("talendus.stripe")


def _stripe():
    try:
        import stripe
    except ImportError as exc:
        raise AppError(503, "Le module Stripe n'est pas installé.", "STRIPE_UNAVAILABLE") from exc
    return stripe


def _require_secret() -> str:
    key = (get_settings().stripe_secret_key or "").strip()
    if not key:
        raise AppError(503, "Paiement Stripe non configuré.", "STRIPE_NOT_CONFIGURED")
    return key


def create_checkout(db: Session, user: User, invoice_id: str) -> dict:
    row = get_invoice(db, user, invoice_id)
    secret = _require_secret()
    if row.status in {InvoiceStatus.PAID, InvoiceStatus.CANCELLED}:
        raise AppError(409, "Cette facture ne peut pas être payée.", "INVOICE_NOT_PAYABLE")
    stripe = _stripe()
    stripe.api_key = secret
    settings = get_settings()
    total = row.amount_total if row.amount_total is not None else row.amount
    cents = int(round(float(total) * 100))
    if cents < 50:
        raise AppError(400, "Montant trop faible pour Stripe.", "INVOICE_AMOUNT_INVALID")
    currency = (row.currency or "CAD").lower()
    base = settings.frontend_url.rstrip("/")
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": currency,
                    "unit_amount": cents,
                    "product_data": {"name": f"Facture {row.number}"},
                },
                "quantity": 1,
            }
        ],
        success_url=f"{base}/espace-employeur.html?paid=1",
        cancel_url=f"{base}/espace-employeur.html?paid=0",
        client_reference_id=row.id,
        metadata={"invoice_id": row.id, "invoice_number": row.number},
    )
    intent = session.payment_intent
    if intent:
        row.stripe_payment_intent_id = intent if isinstance(intent, str) else str(intent)
    audit(db, "invoice.checkout", user, "invoice", row.id, metadata={"session_id": session.id})
    db.commit()
    return {
        "checkout_url": session.url,
        "session_id": session.id,
        "invoice": serialize_invoice(get_invoice(db, user, row.id)),
    }


def apply_event(db: Session, event: dict) -> None:
    etype = event.get("type") or ""
    data = (event.get("data") or {}).get("object") or {}
    invoice_id = None
    payment_intent = None
    if etype == "checkout.session.completed":
        invoice_id = (data.get("metadata") or {}).get("invoice_id") or data.get("client_reference_id")
        payment_intent = data.get("payment_intent")
        if payment_intent is not None and not isinstance(payment_intent, str):
            payment_intent = getattr(payment_intent, "id", str(payment_intent))
    elif etype == "payment_intent.succeeded":
        payment_intent = data.get("id")
        invoice_id = (data.get("metadata") or {}).get("invoice_id")
        if not invoice_id and payment_intent:
            found = db.scalar(select(Invoice).where(Invoice.stripe_payment_intent_id == payment_intent))
            if found:
                invoice_id = found.id
    else:
        return
    if not invoice_id:
        logger.info("stripe event %s without invoice_id", etype)
        return
    row = db.get(Invoice, invoice_id)
    if not row:
        logger.warning("stripe event %s unknown invoice %s", etype, invoice_id)
        return
    if payment_intent:
        row.stripe_payment_intent_id = str(payment_intent)
    if row.status == InvoiceStatus.PAID:
        db.commit()
        return
    total = row.amount_total if row.amount_total is not None else row.amount
    db.add(
        Payment(
            invoice_id=row.id,
            amount=total,
            method=PaymentMethod.CARD,
            paid_at=utcnow().date().isoformat(),
            reference=row.stripe_payment_intent_id,
        )
    )
    row.status = InvoiceStatus.PAID
    row.paid_at = utcnow().date().isoformat()
    db.commit()
    logger.info("invoice %s marked paid via Stripe", row.number)


def construct_event(payload: bytes, signature: str) -> dict:
    secret = (get_settings().stripe_webhook_secret or "").strip()
    if not secret:
        raise AppError(503, "Webhook Stripe non configuré.", "STRIPE_NOT_CONFIGURED")
    stripe = _stripe()
    try:
        return stripe.Webhook.construct_event(payload, signature, secret)
    except Exception as exc:
        raise AppError(400, "Signature Stripe invalide.", "STRIPE_SIGNATURE_INVALID") from exc
