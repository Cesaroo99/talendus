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
        from app.integrations.errors import IntegrationError

        raise IntegrationError(
            "Les remboursements Stripe ne sont pas encore branchés.",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=self.name,
        )

    def status(self, reference: str) -> PaymentResult:
        require_active(self.name)
        return PaymentResult(provider=self.name, status="unknown", amount=0, currency="CAD", reference=reference)


def service() -> PaymentProvider:
    return StripeService()
