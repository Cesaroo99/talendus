"""Stripe via le service métier existant — pas de données bancaires en base."""

from sqlalchemy.orm import Session

from app.integrations.payments.base import PaymentProvider, PaymentResult
from app.integrations.registry import require_active
from app.models import User
from app.services import stripe_billing


class StripeService:
    name = "stripe"

    def create_payment(self, db: Session, user: User, invoice_id: str) -> PaymentResult:
        require_active(self.name)
        data = stripe_billing.create_checkout(db, user, invoice_id)
        invoice = data.get("invoice") or {}
        return PaymentResult(
            provider=self.name,
            status="pending",
            amount=int(invoice.get("amount_total") or invoice.get("amount") or 0),
            currency=(invoice.get("currency") or "CAD"),
            invoice_id=invoice.get("id") or invoice_id,
            user_id=user.id,
            reference=data.get("session_id"),
            checkout_url=data.get("checkout_url"),
        )

    def refund(self, reference: str, amount: int | None = None) -> PaymentResult:
        require_active(self.name)
        from app.services.stripe_billing import _require_secret, _stripe

        secret = _require_secret()
        stripe = _stripe()
        stripe.api_key = secret
        kwargs: dict = {"payment_intent": reference}
        if amount is not None:
            kwargs["amount"] = int(round(int(amount) * 100))
        refund = stripe.Refund.create(**kwargs)
        refund_id = refund.get("id") if isinstance(refund, dict) else getattr(refund, "id", reference)
        return PaymentResult(
            provider=self.name,
            status="refunded",
            amount=int(amount or 0),
            currency="CAD",
            reference=str(refund_id),
        )

    def status(self, reference: str) -> PaymentResult:
        require_active(self.name)
        return PaymentResult(provider=self.name, status="unknown", amount=0, currency="CAD", reference=reference)


def service() -> PaymentProvider:
    return StripeService()
