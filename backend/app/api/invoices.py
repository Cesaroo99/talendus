from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import InvoiceIn, InvoicePatchIn, PaymentIn, RefundIn
from app.services import invoices as invoices_service
from app.services import pdf_docs
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


@router.patch("/{invoice_id}")
def patch_invoice(
    invoice_id: str,
    payload: InvoicePatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    row = invoices_service.update_invoice(db, user, invoice_id, payload)
    return ok(invoices_service.serialize_invoice(row), message="Facture mise à jour.")


@router.get("/{invoice_id}")
def get_invoice(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(invoices_service.serialize_invoice(invoices_service.get_invoice(db, user, invoice_id)))


@router.get("/{invoice_id}/pdf")
def invoice_pdf(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = invoices_service.get_invoice(db, user, invoice_id)
    data = pdf_docs.invoice_pdf(row)
    filename = f"{row.number or 'facture'}.pdf"
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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


@router.post("/{invoice_id}/paypal")
def paypal_checkout(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(invoices_service.paypal_checkout(db, user, invoice_id))


@router.post("/{invoice_id}/paypal/capture")
def paypal_capture(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(invoices_service.paypal_capture(db, user, invoice_id))


@router.post("/{invoice_id}/refund")
def refund_invoice(
    invoice_id: str,
    payload: RefundIn | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE)),
):
    data = payload or RefundIn()
    return ok(invoices_service.refund_invoice(db, user, invoice_id, data.amount, data.provider))
