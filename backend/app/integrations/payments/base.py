from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class PaymentResult:
    provider: str
    status: str
    amount: int
    currency: str
    invoice_id: str | None = None
    user_id: str | None = None
    reference: str | None = None
    checkout_url: str | None = None
    extra: dict | None = None


class PaymentProvider(Protocol):
    name: str

    def create_payment(self, **kwargs) -> PaymentResult: ...

    def refund(self, reference: str, amount: int | None = None) -> PaymentResult: ...

    def status(self, reference: str) -> PaymentResult: ...
