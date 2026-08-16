"""PayPal Orders API — appel officiel seulement si identifiants présents."""

from __future__ import annotations

import base64

from app.config import get_settings
from app.integrations import http
from app.integrations.errors import IntegrationError
from app.integrations.payments.base import PaymentProvider, PaymentResult
from app.integrations.registry import require_active


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

    def refund(self, reference: str, amount: int | None = None) -> PaymentResult:
        require_active(self.name)
        raise IntegrationError(
            "Les remboursements PayPal ne sont pas encore branchés.",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=self.name,
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
