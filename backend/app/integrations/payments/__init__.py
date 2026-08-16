"""Façade paiements — Stripe par défaut, PayPal en option."""

from app.integrations.errors import IntegrationError
from app.integrations.payments.paypal import PayPalService
from app.integrations.payments.stripe import StripeService


class PaymentService:
    def provider(self, name: str = "stripe"):
        if name == "stripe":
            return StripeService()
        if name == "paypal":
            return PayPalService()
        raise IntegrationError("Fournisseur de paiement inconnu.", "INTEGRATION_NOT_FOUND", provider=name)
