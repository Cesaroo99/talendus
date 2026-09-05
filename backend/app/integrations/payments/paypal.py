"""PayPal Orders API — appel officiel seulement si identifiants présents."""

from __future__ import annotations

import base64
import json
from urllib.parse import urlparse

from app.config import get_settings
from app.integrations import http
from app.integrations.errors import IntegrationError
from app.integrations.payments.base import PaymentProvider, PaymentResult
from app.integrations.registry import require_active

_PAYPAL_CERT_HOSTS = frozenset(
    {
        "api.paypal.com",
        "api.sandbox.paypal.com",
        "api-m.paypal.com",
        "api-m.sandbox.paypal.com",
    }
)


class PayPalService:
    name = "paypal"

    def _token(self) -> str:
        settings = get_settings()
        raw = f"{settings.paypal_client_id}:{settings.paypal_client_secret}".encode()
        basic = base64.b64encode(raw).decode("ascii")
        response = http.request(
            "POST",
            f"{settings.paypal_api_base_url.rstrip('/')}/v1/oauth2/token",
            provider=self.name,
            operation="oauth",
            headers={"Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
        )
        return (response.json() or {}).get("access_token") or ""

    def create_payment(
        self,
        *,
        amount: int,
        currency: str = "CAD",
        invoice_id: str | None = None,
        return_url: str | None = None,
        cancel_url: str | None = None,
    ) -> PaymentResult:
        require_active(self.name)
        if amount <= 0:
            raise IntegrationError("Montant PayPal invalide.", "INTEGRATION_INVALID_REQUEST", provider=self.name)
        settings = get_settings()
        token = self._token()
        if not token:
            raise IntegrationError("PayPal n'a pas renvoyé de jeton.", "INTEGRATION_AUTH", provider=self.name)
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": invoice_id or "talendus",
                    "custom_id": invoice_id or "talendus",
                    "amount": {"currency_code": currency.upper(), "value": f"{int(amount)}.00"},
                }
            ],
            "application_context": {
                "return_url": return_url or f"{settings.frontend_url.rstrip('/')}/espace-employeur.html?paid=1",
                "cancel_url": cancel_url or f"{settings.frontend_url.rstrip('/')}/espace-employeur.html?paid=0",
            },
        }
        response = http.request(
            "POST",
            f"{settings.paypal_api_base_url.rstrip('/')}/v2/checkout/orders",
            provider=self.name,
            operation="create_order",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
        )
        data = response.json() or {}
        approve = next((l.get("href") for l in data.get("links") or [] if l.get("rel") == "approve"), None)
        return PaymentResult(
            provider=self.name,
            status=str(data.get("status") or "CREATED").lower(),
            amount=amount,
            currency=currency,
            invoice_id=invoice_id,
            reference=data.get("id"),
            checkout_url=approve,
        )

    def capture_payment(self, reference: str) -> PaymentResult:
        require_active(self.name)
        settings = get_settings()
        token = self._token()
        response = http.request(
            "POST",
            f"{settings.paypal_api_base_url.rstrip('/')}/v2/checkout/orders/{reference}/capture",
            provider=self.name,
            operation="capture_order",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        data = response.json() or {}
        capture_id = None
        units = data.get("purchase_units") or []
        if units:
            captures = ((units[0].get("payments") or {}).get("captures")) or []
            if captures:
                capture_id = captures[0].get("id")
        return PaymentResult(
            provider=self.name,
            status=str(data.get("status") or "COMPLETED").lower(),
            amount=0,
            currency="CAD",
            invoice_id=None,
            reference=data.get("id") or reference,
            extra={"capture_id": capture_id},
        )

    def refund(self, reference: str, amount: int | None = None) -> PaymentResult:
        require_active(self.name)
        settings = get_settings()
        token = self._token()
        payload = None
        if amount is not None:
            payload = {"amount": {"currency_code": "CAD", "value": f"{int(amount)}.00"}}
        response = http.request(
            "POST",
            f"{settings.paypal_api_base_url.rstrip('/')}/v2/payments/captures/{reference}/refund",
            provider=self.name,
            operation="refund_capture",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
        )
        data = response.json() or {}
        return PaymentResult(
            provider=self.name,
            status=str(data.get("status") or "COMPLETED").lower(),
            amount=int(amount or 0),
            currency="CAD",
            reference=data.get("id") or reference,
        )

    def status(self, reference: str) -> PaymentResult:
        require_active(self.name)
        settings = get_settings()
        token = self._token()
        response = http.request(
            "GET",
            f"{settings.paypal_api_base_url.rstrip('/')}/v2/checkout/orders/{reference}",
            provider=self.name,
            operation="order_status",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json() or {}
        return PaymentResult(
            provider=self.name,
            status=str(data.get("status") or "unknown").lower(),
            amount=0,
            currency="CAD",
            reference=data.get("id") or reference,
        )


def service() -> PaymentProvider:
    return PayPalService()


def verify_paypal_transmission(headers: dict[str, str], payload: bytes) -> None:
    """Refuse un événement PayPal dont la transmission n’est pas confirmée par PayPal."""
    settings = get_settings()
    webhook_id = (settings.paypal_webhook_id or "").strip()
    if not webhook_id:
        raise IntegrationError("Secret webhook paypal manquant.", "INTEGRATION_NOT_CONFIGURED", provider="paypal")
    lowered = {str(key).lower(): str(value or "") for key, value in (headers or {}).items()}
    auth_algo = lowered.get("paypal-auth-algo") or ""
    cert_url = lowered.get("paypal-cert-url") or ""
    transmission_id = lowered.get("paypal-transmission-id") or ""
    transmission_sig = lowered.get("paypal-transmission-sig") or ""
    transmission_time = lowered.get("paypal-transmission-time") or ""
    if not all([auth_algo, cert_url, transmission_id, transmission_sig, transmission_time]):
        raise IntegrationError(
            "En-têtes de transmission PayPal manquants.",
            "INTEGRATION_SIGNATURE_INVALID",
            provider="paypal",
            details=[{"field": "paypal-transmission-id", "message": "Transmission incomplète."}],
        )
    host = (urlparse(cert_url).hostname or "").lower()
    if host not in _PAYPAL_CERT_HOSTS:
        raise IntegrationError(
            "Certificat PayPal refusé.",
            "INTEGRATION_SIGNATURE_INVALID",
            provider="paypal",
            details=[{"field": "paypal-cert-url", "message": "Hôte non autorisé."}],
        )
    try:
        event = json.loads((payload or b"{}").decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise IntegrationError(
            "Événement PayPal illisible.",
            "INTEGRATION_SIGNATURE_INVALID",
            provider="paypal",
        ) from exc
    if not isinstance(event, dict):
        raise IntegrationError("Événement PayPal invalide.", "INTEGRATION_SIGNATURE_INVALID", provider="paypal")
    token = PayPalService()._token()
    if not token:
        raise IntegrationError("PayPal n'a pas renvoyé de jeton.", "INTEGRATION_AUTH", provider="paypal")
    response = http.request(
        "POST",
        f"{settings.paypal_api_base_url.rstrip('/')}/v1/notifications/verify-webhook-signature",
        provider="paypal",
        operation="verify_webhook",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "auth_algo": auth_algo,
            "cert_url": cert_url,
            "transmission_id": transmission_id,
            "transmission_sig": transmission_sig,
            "transmission_time": transmission_time,
            "webhook_id": webhook_id,
            "webhook_event": event,
        },
    )
    status = str((response.json() or {}).get("verification_status") or "").upper()
    if status != "SUCCESS":
        raise IntegrationError(
            "Signature de webhook PayPal invalide.",
            "INTEGRATION_SIGNATURE_INVALID",
            provider="paypal",
        )


def apply_paypal_event(db, payload: bytes) -> None:
    """Met à jour une facture si l'événement PayPal correspond à un paypal_order_id connu."""
    import json
    import logging

    from sqlalchemy import select

    from app.integrations.errors import IntegrationError
    from app.integrations.registry import is_active
    from app.models import Invoice, Payment
    from app.models.enums import InvoiceStatus, PaymentMethod, utcnow

    logger = logging.getLogger("talendus.paypal")
    try:
        body = json.loads((payload or b"{}").decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return
    if not isinstance(body, dict):
        return
    event_type = str(body.get("event_type") or "")
    resource = body.get("resource") or {}
    order_id = ((resource.get("supplementary_data") or {}).get("related_ids") or {}).get("order_id") or resource.get(
        "id"
    )
    custom_id = resource.get("custom_id")
    invoice = db.get(Invoice, custom_id) if custom_id else None
    if invoice is None and order_id:
        invoice = db.scalar(select(Invoice).where(Invoice.paypal_order_id == str(order_id)))
    if invoice is None:
        return
    if order_id:
        invoice.paypal_order_id = str(order_id)
    if event_type == "CHECKOUT.ORDER.APPROVED" and order_id and is_active("paypal"):
        try:
            result = PayPalService().capture_payment(str(order_id))
            capture_id = (result.extra or {}).get("capture_id")
            if capture_id:
                invoice.paypal_capture_id = str(capture_id)
        except IntegrationError:
            logger.warning("paypal capture skipped order=%s", order_id)
        db.commit()
        return
    if event_type in {"PAYMENT.CAPTURE.COMPLETED", "CHECKOUT.ORDER.COMPLETED"}:
        if event_type == "PAYMENT.CAPTURE.COMPLETED" and resource.get("id"):
            invoice.paypal_capture_id = str(resource.get("id"))
        if invoice.status != InvoiceStatus.PAID:
            total = invoice.amount_total if invoice.amount_total is not None else invoice.amount
            db.add(
                Payment(
                    invoice_id=invoice.id,
                    amount=total,
                    method=PaymentMethod.CARD,
                    paid_at=utcnow().date().isoformat(),
                    reference=invoice.paypal_capture_id or invoice.paypal_order_id,
                )
            )
            invoice.status = InvoiceStatus.PAID
            invoice.paid_at = utcnow().date().isoformat()
        db.commit()
        return
    if event_type in {"PAYMENT.CAPTURE.REFUNDED", "PAYMENT.CAPTURE.REVERSED"}:
        amount_value = (resource.get("amount") or {}).get("value")
        try:
            dollars = int(float(amount_value)) if amount_value else int(invoice.amount_total or invoice.amount or 0)
        except (TypeError, ValueError):
            dollars = int(invoice.amount_total or invoice.amount or 0)
        db.add(
            Payment(
                invoice_id=invoice.id,
                amount=-abs(dollars),
                method=PaymentMethod.CARD,
                paid_at=utcnow().date().isoformat(),
                reference=str(resource.get("id") or "")[:80] or None,
            )
        )
        invoice.status = InvoiceStatus.REFUNDED
        db.commit()
