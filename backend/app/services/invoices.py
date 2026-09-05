from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload

from app.config import get_settings
from app.errors import AppError
from app.models import Company, Invoice, InvoiceLine, Payment, RecruitmentMission, SystemSetting, User
from app.models.enums import InvoiceStatus, PaymentMethod, UserRole, utcnow
from app.rbac import ADMINS
from app.schemas import InvoiceIn, InvoicePatchIn, PaymentIn
from app.services.access import company_ids_for_employer
from app.services.audit import audit
from app.services.pdf_docs import qc_tax_split, tax_from_bp

ADMIN_STATUS = {
    InvoiceStatus.DRAFT: "brouillon",
    InvoiceStatus.SENT: "envoyee",
    InvoiceStatus.PENDING: "en-attente",
    InvoiceStatus.PAID: "payee",
    InvoiceStatus.OVERDUE: "en-retard",
    InvoiceStatus.CANCELLED: "annulee",
    InvoiceStatus.REFUNDED: "remboursee",
}


def _finance(user: User) -> None:
    if user.role not in {UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Accès finance requis.", "FORBIDDEN")


def _parse_iso_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def payment_days(db: Session) -> int:
    row = db.scalar(select(SystemSetting).where(SystemSetting.key == "invoice_payment_days"))
    try:
        days = int((row.value if row else None) or 30)
    except (TypeError, ValueError):
        days = 30
    return max(1, min(days, 365))


def default_due_date(db: Session, issued: str | None) -> str:
    start = _parse_iso_date(issued) or utcnow().date()
    return (start + timedelta(days=payment_days(db))).isoformat()


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
    ht = row.amount_ht if row.amount_ht is not None else row.amount
    gst, qst = qc_tax_split(int(ht or 0), int(row.tax_amount or 0))
    return {
        "id": row.id,
        "number": row.number,
        "company_id": row.company_id,
        "mission_id": row.mission_id,
        "client_user_id": row.client_user_id,
        "amount": total,
        "amount_ht": ht,
        "tax_amount": row.tax_amount,
        "gst_amount": gst,
        "qst_amount": qst,
        "amount_total": total,
        "tax_rate_bp": row.tax_rate_bp,
        "currency": row.currency,
        "status": row.status.value,
        "issued_at": row.issued_at,
        "due_date": row.due_date,
        "paid_at": row.paid_at,
        "stripe_payment_intent_id": row.stripe_payment_intent_id,
        "paypal_order_id": row.paypal_order_id,
        "paypal_capture_id": row.paypal_capture_id,
        "notes": row.notes,
        "paid_amount": paid,
        "company_name": row.company.name if row.company else None,
        "mission_title": row.mission.title if row.mission else None,
        "pdf_path": f"/api/invoices/{row.id}/pdf",
        "pay_hint": "Virement ou chèque à l’ordre de Talendus (CAD). TPS 5 % et TVQ 9,975 % selon le Québec.",
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
        if row.status == InvoiceStatus.DRAFT:
            return False
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
        stmt = stmt.where(Invoice.company_id.in_(ids), Invoice.status != InvoiceStatus.DRAFT)
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
    if data.tax_rate_bp is not None:
        tax_bp = data.tax_rate_bp
    else:
        tax_bp = get_settings().default_tax_rate_bp
    lines_data = data.lines or []
    if lines_data:
        ht = sum(max(1, line.quantity) * line.unit_price for line in lines_data)
    if data.tax_amount is not None and data.tax_rate_bp == 0:
        tax_amount = data.tax_amount
    else:
        tax_amount = tax_from_bp(ht, tax_bp) if tax_bp else (data.tax_amount or 0)
    total = ht + tax_amount
    for attempt in range(4):
        try:
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
                due_date=data.due_date or default_due_date(db, data.issued_at or today),
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
        except IntegrityError:
            db.rollback()
            if attempt >= 3:
                raise AppError(409, "Cette facture n'a pas pu être enregistrée. Réessayez.", "INVOICE_CONFLICT") from None
            company = db.get(Company, data.company_id) or company


def update_invoice(db: Session, user: User, invoice_id: str, data: InvoicePatchIn) -> Invoice:
    _finance(user)
    row = get_invoice(db, user, invoice_id)
    if row.status in {InvoiceStatus.PAID, InvoiceStatus.CANCELLED, InvoiceStatus.REFUNDED}:
        raise AppError(409, "Cette facture ne peut plus être modifiée.", "INVOICE_LOCKED")
    if data.issued_at is not None:
        row.issued_at = data.issued_at[:16]
    if data.due_date is not None:
        row.due_date = data.due_date[:16] if data.due_date.strip() else default_due_date(db, row.issued_at)
    elif not row.due_date:
        row.due_date = default_due_date(db, row.issued_at)
    if data.notes is not None:
        row.notes = data.notes
        if row.lines and len(row.lines) == 1 and (row.lines[0].description or "").startswith("Honoraires"):
            row.lines[0].description = data.notes or row.lines[0].description
    if data.amount is not None or data.tax_rate_bp is not None:
        ht = data.amount if data.amount is not None else (row.amount_ht if row.amount_ht is not None else row.amount)
        tax_bp = data.tax_rate_bp if data.tax_rate_bp is not None else row.tax_rate_bp
        tax_amount = tax_from_bp(int(ht or 0), tax_bp) if tax_bp else int(row.tax_amount or 0)
        row.amount_ht = ht
        row.tax_rate_bp = tax_bp
        row.tax_amount = tax_amount
        row.amount_total = int(ht or 0) + tax_amount
        row.amount = row.amount_total
        if row.lines and len(row.lines) == 1:
            row.lines[0].unit_price = int(ht or 0)
            row.lines[0].amount = int(ht or 0)
    audit(db, "invoice.update", user, "invoice", row.id)
    db.commit()
    return get_invoice(db, user, row.id)


def send_invoice(db: Session, user: User, invoice_id: str) -> Invoice:
    from app.services.ops_notify import frontend, message_company, notify_company

    _finance(user)
    row = get_invoice(db, user, invoice_id)
    if row.status == InvoiceStatus.CANCELLED:
        raise AppError(409, "Une facture annulée ne peut pas être envoyée.", "INVOICE_CANCELLED")
    row.status = InvoiceStatus.SENT
    if not row.issued_at:
        row.issued_at = utcnow().date().isoformat()
    if not row.due_date:
        row.due_date = default_due_date(db, row.issued_at)
    audit(db, "invoice.send", user, "invoice", row.id)
    total = row.amount_total if row.amount_total is not None else row.amount
    company_name = row.company.name if row.company else "votre entreprise"
    notify_company(
        db,
        row.company_id,
        title="Nouvelle facture Talendus",
        message=f"La facture {row.number} ({total} CAD) est disponible.",
        section="invoices",
        template="invoice_sent",
        ctx={
            "name": company_name,
            "number": row.number,
            "amount": str(total),
            "due": row.due_date or "sur réception",
            "link": f"{frontend()}/espace-employeur.html#/invoices",
        },
        item_id=row.id,
    )
    db.commit()
    try:
        message_company(
            db,
            user,
            row.company_id,
            f"La facture {row.number} ({total} CAD) a été émise. Téléchargez le PDF dans Factures. Paiement par virement ou chèque.",
        )
    except Exception:
        pass
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
    if row.status == InvoiceStatus.PAID:
        from app.services.ops_notify import frontend, notify_company

        notify_company(
            db,
            row.company_id,
            title="Paiement reçu",
            message=f"Le paiement de la facture {row.number} a été enregistré.",
            section="invoices",
            template="payment_received",
            ctx={
                "name": row.company.name if row.company else "votre entreprise",
                "number": row.number,
                "amount": str(data.amount),
                "status": row.status.value,
                "link": f"{frontend()}/espace-employeur.html#/invoices",
            },
            item_id=row.id,
        )
    db.commit()
    return get_invoice(db, user, row.id)


def mark_overdue(db: Session) -> int:
    today = utcnow().date().isoformat()
    rows = list(
        db.scalars(
            select(Invoice)
            .options(joinedload(Invoice.company))
            .where(
                Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PENDING]),
                Invoice.due_date.is_not(None),
                Invoice.due_date < today,
            )
        ).unique().all()
    )
    if not rows:
        return 0
    from app.services.ops_notify import frontend, notify_company

    for row in rows:
        row.status = InvoiceStatus.OVERDUE
        total = row.amount_total if row.amount_total is not None else row.amount
        notify_company(
            db,
            row.company_id,
            title="Facture en retard",
            message=f"La facture {row.number} est échue.",
            section="invoices",
            template="invoice_overdue",
            ctx={
                "name": row.company.name if row.company else "votre entreprise",
                "number": row.number,
                "amount": str(total),
                "due": row.due_date or "-",
                "link": f"{frontend()}/espace-employeur.html#/invoices",
            },
            item_id=row.id,
        )
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
        "refunded": _sum(InvoiceStatus.REFUNDED),
    }


def paypal_checkout(db: Session, user: User, invoice_id: str) -> dict:
    from app.integrations.payments.paypal import PayPalService

    row = get_invoice(db, user, invoice_id)
    if row.status in {InvoiceStatus.PAID, InvoiceStatus.CANCELLED, InvoiceStatus.REFUNDED}:
        raise AppError(409, "Cette facture ne peut pas être payée.", "INVOICE_NOT_PAYABLE")
    total = row.amount_total if row.amount_total is not None else row.amount
    result = PayPalService().create_payment(amount=int(total), currency=row.currency or "CAD", invoice_id=row.id)
    row.paypal_order_id = result.reference
    audit(db, "invoice.paypal.checkout", user, "invoice", row.id, metadata={"order_id": result.reference})
    db.commit()
    return {
        "provider": "paypal",
        "checkout_url": result.checkout_url,
        "reference": result.reference,
        "invoice": serialize_invoice(get_invoice(db, user, row.id)),
    }


def paypal_capture(db: Session, user: User, invoice_id: str) -> dict:
    from app.integrations.payments.paypal import PayPalService

    row = get_invoice(db, user, invoice_id)
    if not row.paypal_order_id:
        raise AppError(409, "Aucune commande PayPal à capturer.", "PAYPAL_CAPTURE_UNAVAILABLE")
    result = PayPalService().capture_payment(row.paypal_order_id)
    capture_id = (result.extra or {}).get("capture_id")
    if capture_id:
        row.paypal_capture_id = str(capture_id)
    if row.status != InvoiceStatus.PAID:
        total = row.amount_total if row.amount_total is not None else row.amount
        db.add(
            Payment(
                invoice_id=row.id,
                amount=total,
                method=PaymentMethod.CARD,
                paid_at=utcnow().date().isoformat(),
                reference=row.paypal_capture_id or row.paypal_order_id,
                recorded_by=user.id,
            )
        )
        row.status = InvoiceStatus.PAID
        row.paid_at = utcnow().date().isoformat()
    audit(db, "invoice.paypal.capture", user, "invoice", row.id)
    db.commit()
    return {
        "provider": "paypal",
        "status": result.status,
        "reference": result.reference,
        "invoice": serialize_invoice(get_invoice(db, user, row.id)),
    }


def paypal_refund(db: Session, user: User, invoice_id: str, amount: int | None = None) -> dict:
    from app.integrations.payments.paypal import PayPalService

    _finance(user)
    row = get_invoice(db, user, invoice_id)
    if not row.paypal_capture_id:
        raise AppError(409, "Aucun capture PayPal à rembourser.", "PAYPAL_REFUND_UNAVAILABLE")
    total = row.amount_total if row.amount_total is not None else row.amount
    dollars = int(amount) if amount is not None else int(total)
    result = PayPalService().refund(row.paypal_capture_id, dollars)
    db.add(
        Payment(
            invoice_id=row.id,
            amount=-abs(dollars),
            method=PaymentMethod.CARD,
            paid_at=utcnow().date().isoformat(),
            reference=result.reference,
            recorded_by=user.id,
        )
    )
    row.status = InvoiceStatus.REFUNDED
    audit(db, "invoice.refund", user, "invoice", row.id, metadata={"amount": dollars, "provider": "paypal"})
    db.commit()
    return {
        "provider": "paypal",
        "status": result.status,
        "amount": dollars,
        "reference": result.reference,
        "invoice": serialize_invoice(get_invoice(db, user, row.id)),
    }
