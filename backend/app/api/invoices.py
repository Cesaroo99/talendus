from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import InvoiceIn, PaymentIn
from app.services import invoices as invoices_service
from app.services import stripe_billing

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("")
def list_invoices(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok([invoices_service.serialize_invoice(row) for row in invoices_service.list_invoices(db, user)])


@router.get("/stats")
def invoice_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    invoices_service.mark_overdue(db)
    return ok(invoices_service.stats(db))


@router.post("")
def create_invoice(
    payload: InvoiceIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    row = invoices_service.create_invoice(db, user, payload, client_ip(request))
    return ok(invoices_service.serialize_invoice(row), message="Facture créée.")


@router.get("/{invoice_id}")
def get_invoice(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(invoices_service.serialize_invoice(invoices_service.get_invoice(db, user, invoice_id)))


@router.post("/{invoice_id}/send")
def send_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    return ok(invoices_service.serialize_invoice(invoices_service.send_invoice(db, user, invoice_id)))


@router.post("/{invoice_id}/payments")
def add_payment(
    invoice_id: str,
    payload: PaymentIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    row = invoices_service.add_payment(db, user, invoice_id, payload, client_ip(request))
    return ok(invoices_service.serialize_invoice(row), message="Paiement enregistré.")


@router.post("/{invoice_id}/checkout")
def checkout_invoice(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(stripe_billing.create_checkout(db, user, invoice_id))
