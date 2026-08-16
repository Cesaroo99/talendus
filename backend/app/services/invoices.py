from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import AppError
from app.models import Company, Invoice, InvoiceLine, Payment, RecruitmentMission, User
from app.models.enums import InvoiceStatus, PaymentMethod, UserRole, utcnow
from app.rbac import ADMINS
from app.schemas import InvoiceIn, PaymentIn
from app.services.access import company_ids_for_employer
from app.services.audit import audit

ADMIN_STATUS = {
    InvoiceStatus.DRAFT: "brouillon",
    InvoiceStatus.SENT: "envoyee",
    InvoiceStatus.PENDING: "en-attente",
    InvoiceStatus.PAID: "payee",
    InvoiceStatus.OVERDUE: "en-retard",
    InvoiceStatus.CANCELLED: "annulee",
}


def _finance(user: User) -> None:
    if user.role not in {UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Accès finance requis.", "FORBIDDEN")


def next_number(db: Session) -> str:
    year = utcnow().year
    prefix = f"F-{year}-"
    last = db.scalar(select(Invoice.number).where(Invoice.number.like(f"{prefix}%")).order_by(Invoice.number.desc()))
    n = 1
    if last:
        try:
            n = int(last.rsplit("-", 1)[-1]) + 1
        except ValueError:
            n = 1
    return f"{prefix}{n:03d}"


def serialize_invoice(row: Invoice) -> dict:
    paid = sum(p.amount for p in (row.payments or []))
    total = row.amount_total if row.amount_total is not None else row.amount
    return {
        "id": row.id,
        "number": row.number,
        "company_id": row.company_id,
        "mission_id": row.mission_id,
        "client_user_id": row.client_user_id,
        "amount": total,
        "amount_ht": row.amount_ht,
        "tax_amount": row.tax_amount,
        "amount_total": total,
        "tax_rate_bp": row.tax_rate_bp,
        "currency": row.currency,
        "status": row.status.value,
        "issued_at": row.issued_at,
        "due_date": row.due_date,
        "paid_at": row.paid_at,
        "stripe_payment_intent_id": row.stripe_payment_intent_id,
        "notes": row.notes,
        "paid_amount": paid,
        "company_name": row.company.name if row.company else None,
        "mission_title": row.mission.title if row.mission else None,
        "lines": [serialize_line(line) for line in (row.lines or [])],
        "payments": [serialize_payment(p) for p in (row.payments or [])],
    }


def serialize_line(row: InvoiceLine) -> dict:
    return {
        "id": row.id,
        "description": row.description,
        "quantity": row.quantity,
        "unit_price": row.unit_price,
        "amount": row.amount,
        "reference": row.reference,
        "job_id": row.job_id,
        "mission_id": row.mission_id,
    }


def serialize_payment(row: Payment) -> dict:
    return {
        "id": row.id,
        "invoice_id": row.invoice_id,
        "amount": row.amount,
        "method": row.method.value,
        "paid_at": row.paid_at,
        "reference": row.reference,
    }


def _load(db: Session, invoice_id: str) -> Invoice | None:
    return db.scalar(
        select(Invoice)
        .options(
            joinedload(Invoice.company),
            joinedload(Invoice.mission),
            selectinload(Invoice.payments),
            selectinload(Invoice.lines),
        )
        .where(Invoice.id == invoice_id)
    )


def _visible(db: Session, user: User, row: Invoice) -> bool:
    if user.role in {UserRole.FINANCE, UserRole.RECRUITER} | ADMINS:
        return True
    if user.role == UserRole.EMPLOYER:
        return row.company_id in company_ids_for_employer(db, user)
    return False


def list_invoices(db: Session, user: User) -> list[Invoice]:
    stmt = select(Invoice).options(
        joinedload(Invoice.company),
        joinedload(Invoice.mission),
        selectinload(Invoice.payments),
        selectinload(Invoice.lines),
    )
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(Invoice.company_id.in_(ids))
    elif user.role not in {UserRole.FINANCE, UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux factures.", "FORBIDDEN")
    return list(db.scalars(stmt.order_by(Invoice.created_at.desc())).unique().all())


def get_invoice(db: Session, user: User, invoice_id: str) -> Invoice:
    row = _load(db, invoice_id)
    if not row:
        raise AppError(404, "Facture introuvable.", "INVOICE_NOT_FOUND")
    if not _visible(db, user, row):
        raise AppError(403, "Vous n'avez pas accès à cette facture.", "FORBIDDEN")
    return row


def create_invoice(db: Session, user: User, data: InvoiceIn, ip: str | None) -> Invoice:
    _finance(user)
    company = db.get(Company, data.company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    if data.mission_id:
        mission = db.get(RecruitmentMission, data.mission_id)
        if not mission or mission.company_id != company.id:
            raise AppError(400, "Mission invalide pour cette entreprise.", "INVALID_MISSION")
    today = utcnow().date().isoformat()
    ht = data.amount_ht if data.amount_ht is not None else data.amount
    tax_bp = data.tax_rate_bp if data.tax_rate_bp is not None else 0
    lines_data = data.lines or []
    if lines_data:
        ht = sum(max(1, line.quantity) * line.unit_price for line in lines_data)
    tax_amount = round(ht * tax_bp / 10000) if tax_bp else (data.tax_amount or 0)
    total = ht + tax_amount
    row = Invoice(
        number=next_number(db),
        company_id=company.id,
        mission_id=data.mission_id,
        client_user_id=data.client_user_id,
        amount=total,
        amount_ht=ht,
        tax_amount=tax_amount,
        amount_total=total,
        tax_rate_bp=tax_bp or None,
        currency=data.currency or "CAD",
        status=InvoiceStatus.DRAFT,
        issued_at=data.issued_at or today,
        due_date=data.due_date,
        notes=data.notes,
    )
    db.add(row)
    db.flush()
    if lines_data:
        for line in lines_data:
            qty = max(1, line.quantity)
            amount = qty * line.unit_price
            db.add(
                InvoiceLine(
                    invoice_id=row.id,
                    description=line.description,
                    quantity=qty,
                    unit_price=line.unit_price,
                    amount=amount,
                    reference=line.reference,
                    job_id=line.job_id,
                    mission_id=line.mission_id or data.mission_id,
                )
            )
    else:
        db.add(
            InvoiceLine(
                invoice_id=row.id,
                description=data.notes or "Honoraires de recrutement",
                quantity=1,
                unit_price=ht,
                amount=ht,
                mission_id=data.mission_id,
            )
        )
    audit(db, "invoice.create", user, "invoice", row.id, ip, {"number": row.number})
    db.commit()
    return get_invoice(db, user, row.id)


def send_invoice(db: Session, user: User, invoice_id: str) -> Invoice:
    _finance(user)
    row = get_invoice(db, user, invoice_id)
    if row.status == InvoiceStatus.CANCELLED:
        raise AppError(409, "Une facture annulée ne peut pas être envoyée.", "INVOICE_CANCELLED")
    row.status = InvoiceStatus.SENT
    if not row.issued_at:
        row.issued_at = utcnow().date().isoformat()
    audit(db, "invoice.send", user, "invoice", row.id)
    db.commit()
    return get_invoice(db, user, row.id)


def add_payment(db: Session, user: User, invoice_id: str, data: PaymentIn, ip: str | None) -> Invoice:
    _finance(user)
    row = get_invoice(db, user, invoice_id)
    if row.status == InvoiceStatus.CANCELLED:
        raise AppError(409, "Impossible d'encaisser une facture annulée.", "INVOICE_CANCELLED")
    if data.amount <= 0:
        raise AppError(400, "Le montant du paiement doit être positif.", "VALIDATION_ERROR")
    payment = Payment(
        invoice_id=row.id,
        amount=data.amount,
        method=data.method or PaymentMethod.TRANSFER,
        paid_at=data.paid_at or utcnow().date().isoformat(),
        reference=data.reference,
        recorded_by=user.id,
    )
    db.add(payment)
    db.flush()
    paid = int(db.scalar(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.invoice_id == row.id)) or 0)
    total = row.amount_total if row.amount_total is not None else row.amount
    if paid >= total:
        row.status = InvoiceStatus.PAID
        row.paid_at = data.paid_at or utcnow().date().isoformat()
    elif row.status in {InvoiceStatus.DRAFT, InvoiceStatus.SENT}:
        row.status = InvoiceStatus.PENDING
    audit(db, "invoice.payment", user, "invoice", row.id, ip, {"amount": data.amount})
    db.commit()
    return get_invoice(db, user, row.id)


def mark_overdue(db: Session) -> int:
    today = utcnow().date().isoformat()
    rows = list(
        db.scalars(
            select(Invoice).where(
                Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PENDING]),
                Invoice.due_date.is_not(None),
                Invoice.due_date < today,
            )
        ).all()
    )
    for row in rows:
        row.status = InvoiceStatus.OVERDUE
    if rows:
        db.commit()
    return len(rows)


def stats(db: Session) -> dict:
    def _sum(status: InvoiceStatus) -> int:
        return int(db.scalar(select(func.coalesce(func.sum(Invoice.amount), 0)).where(Invoice.status == status)) or 0)

    return {
        "paid": _sum(InvoiceStatus.PAID),
        "pending": _sum(InvoiceStatus.PENDING) + _sum(InvoiceStatus.SENT),
        "overdue": _sum(InvoiceStatus.OVERDUE),
        "draft": _sum(InvoiceStatus.DRAFT),
    }
