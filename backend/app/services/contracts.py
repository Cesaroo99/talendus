import hashlib
import logging
import re
from datetime import date, timedelta

from sqlalchemy import inspect, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, selectinload

logger = logging.getLogger("talendus.contracts")

from app.errors import AppError
from app.models import Company, Contract, ContractSignature, User
from app.models.enums import ContractStatus, NotificationType, UserRole, utcnow
from app.rbac import ADMINS
from app.schemas import ContractIn, ContractPatchIn, ContractSignIn
from app.services.access import company_ids_for_employer
from app.services.audit import audit
from app.services.pdf_docs import (
    DEFAULT_COMMISSION_PERCENT,
    MANDATE_TEMPLATES,
    PARTY_CLIENT,
    PARTY_TALENDUS,
    mandate_terms,
)

STAFF = {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS
WORK_STATUSES = {
    "JOB_PUBLISHED",
    "SOURCING",
    "SCREENING",
    "INTERVIEWS",
    "SHORTLIST",
    "CLIENT_REVIEW",
    "HIRING",
    "IN_PROGRESS",
    "OPEN",
}


def serialize_signature(row: ContractSignature) -> dict:
    return {
        "id": row.id,
        "party": (row.party or PARTY_CLIENT).upper(),
        "signer_name": row.signer_name,
        "signer_email": row.signer_email,
        "signer_role": row.signer_role,
        "signed_at": row.signed_at.isoformat() if row.signed_at else None,
        "ip_address": row.ip_address,
        "document_hash": row.document_hash,
        "document_name": row.document_name,
        "accepted": row.accepted,
    }


def _iso(value) -> str | None:
    if not value:
        return None
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", (value or "").lower())
    return text.strip("-")[:48] or "client"


def _template_meta(key: str | None) -> dict:
    wanted = (key or "succes").strip().lower()
    for item in MANDATE_TEMPLATES:
        if item["key"] == wanted:
            return item
    return MANDATE_TEMPLATES[0]


def _party_signature(row: Contract, party: str) -> ContractSignature | None:
    wanted = (party or PARTY_CLIENT).upper()
    found = None
    for item in row.signatures or []:
        current = (item.party or PARTY_CLIENT).upper()
        if current == wanted:
            found = item
    return found


def client_status(row: Contract) -> str:
    if row.client_signed_at or _party_signature(row, PARTY_CLIENT):
        return "signed"
    if row.opened_at:
        return "opened"
    if row.sent_at:
        return "received"
    return "not_sent"


def lifecycle(row: Contract) -> str:
    talendus = bool(row.talendus_signed_at or _party_signature(row, PARTY_TALENDUS))
    client = bool(row.client_signed_at or _party_signature(row, PARTY_CLIENT))
    if client and talendus:
        return "complete"
    if client:
        return "signed"
    if row.opened_at:
        return "opened"
    if row.sent_at:
        return "received"
    if talendus:
        return "awaiting_send"
    return "draft"


def _parse_iso_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def mandate_window(start: str | None, end: str | None, default_days: int | None = None) -> tuple[str, str, int]:
    days = max(int(default_days or 90), 1)
    start_d = _parse_iso_date(start) or date.today()
    end_d = _parse_iso_date(end)
    if end_d and end_d >= start_d:
        days = max((end_d - start_d).days, 1)
    else:
        end_d = start_d + timedelta(days=days)
    return start_d.isoformat(), end_d.isoformat(), days


def _role_from_terms(terms: str | None) -> str | None:
    match = re.search(r"Poste visé\s*:\s*(.+)", terms or "")
    if not match:
        return None
    role = match.group(1).strip()
    if not role or role.lower().startswith("le poste confié"):
        return None
    return role[:180]


def filled_terms(company: Company | None, data: ContractIn | None = None, *, template: str | None = None) -> str:
    meta = _template_meta(template or (data.template if data else None))
    commission = None
    mandate_type = meta["type"]
    role = None
    start = None
    end = None
    if data:
        commission = data.commission_percent
        if data.type:
            mandate_type = data.type.strip()
        role = data.role
        start = data.start_date
        end = data.end_date
    start, end, days = mandate_window(start, end, meta.get("duration_days"))
    return mandate_terms(
        company_name=company.name if company else "le client",
        legal_name=company.legal_name if company else None,
        address=company.address if company else None,
        city=company.city if company else None,
        province=company.province if company else None,
        commission=commission if commission is not None else meta["commission_percent"],
        mandate_type=mandate_type,
        role=role,
        start_date=start,
        end_date=end,
        template=meta["key"],
        duration_days=days,
        guarantee_days=meta.get("guarantee_days"),
        presented_months=meta.get("presented_months"),
    )


def preview_contract(
    db: Session,
    user: User,
    company_id: str,
    template: str | None = None,
    commission: int | None = None,
    role: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    if user.role not in STAFF:
        raise AppError(403, "Aperçu réservé à l'équipe Talendus.", "FORBIDDEN")
    company = db.get(Company, company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    meta = _template_meta(template)
    percent = commission if commission is not None else meta["commission_percent"]
    start, end, days = mandate_window(start_date, end_date, meta.get("duration_days"))
    draft = ContractIn(
        company_id=company.id,
        type=meta["type"],
        start_date=start,
        end_date=end,
        commission_percent=percent,
        template=meta["key"],
        role=role,
    )
    terms = filled_terms(company, draft, template=meta["key"])
    return {
        "template": meta["key"],
        "type": meta["type"],
        "company_id": company.id,
        "company_name": company.name,
        "start_date": start,
        "end_date": end,
        "commission_percent": percent,
        "duration_days": days,
        "guarantee_days": meta.get("guarantee_days"),
        "role": (role or "").strip() or None,
        "document_name": f"mandat-talendus-{_slug(company.name)}-{start}.pdf",
        "terms": terms,
        "templates": list(MANDATE_TEMPLATES),
    }


def list_templates() -> list[dict]:
    return list(MANDATE_TEMPLATES)


def company_has_signed_mandate(db: Session, company_id: str) -> bool:
    row = db.scalar(
        select(Contract.id)
        .where(Contract.company_id == company_id, Contract.client_signed_at.is_not(None))
        .limit(1)
    )
    if row:
        return True
    signed = db.scalar(
        select(ContractSignature.id)
        .join(Contract, ContractSignature.contract_id == Contract.id)
        .where(Contract.company_id == company_id, ContractSignature.party == PARTY_CLIENT)
        .limit(1)
    )
    return bool(signed)


def serialize_contract(row: Contract) -> dict:
    by_party = {
        PARTY_TALENDUS: _party_signature(row, PARTY_TALENDUS),
        PARTY_CLIENT: _party_signature(row, PARTY_CLIENT),
    }
    client = by_party[PARTY_CLIENT]
    talendus = by_party[PARTY_TALENDUS]
    status = client_status(row)
    _, _, days = mandate_window(row.start_date, row.end_date)
    locked = bool(row.talendus_signed_at or talendus or row.sent_at or row.client_signed_at or client)
    return {
        "id": row.id,
        "company_id": row.company_id,
        "type": row.type,
        "template": row.template_key,
        "start_date": row.start_date,
        "end_date": row.end_date,
        "duration_days": days,
        "role": _role_from_terms(row.terms),
        "commission_percent": row.commission_percent or DEFAULT_COMMISSION_PERCENT,
        "terms": row.terms,
        "can_edit": not locked,
        "status": row.status.value if row.status else None,
        "document_name": row.document_name,
        "esign_envelope_id": row.esign_envelope_id,
        "esign_status": row.esign_status,
        "signed": bool(client),
        "talendus_signed": bool(talendus or row.talendus_signed_at),
        "client_signed": bool(client or row.client_signed_at),
        "can_sign": bool(row.sent_at and (talendus or row.talendus_signed_at) and not client),
        "client_status": status,
        "lifecycle": lifecycle(row),
        "sent_at": _iso(row.sent_at),
        "opened_at": _iso(row.opened_at),
        "talendus_signed_at": _iso(row.talendus_signed_at),
        "client_signed_at": _iso(row.client_signed_at),
        "reminder_count": int(row.reminder_count or 0),
        "last_reminded_at": _iso(row.last_reminded_at),
        "signature": serialize_signature(client) if client else None,
        "signatures": [serialize_signature(item) for item in (row.signatures or [])],
        "talendus_signature": serialize_signature(talendus) if talendus else None,
        "client_signature": serialize_signature(client) if client else None,
        "pdf_path": f"/api/contracts/{row.id}/pdf",
        "company_name": row.company.name if row.company else None,
    }


def _can_access(db: Session, user: User, contract: Contract) -> bool:
    if user.role in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS:
        return True
    if user.role == UserRole.EMPLOYER:
        return contract.company_id in company_ids_for_employer(db, user)
    return False


def list_contracts(db: Session, user: User) -> list[Contract]:
    stmt = select(Contract).options(selectinload(Contract.signatures), joinedload(Contract.company))
    if user.role == UserRole.EMPLOYER:
        ids = company_ids_for_employer(db, user)
        if not ids:
            return []
        stmt = stmt.where(Contract.company_id.in_(ids), Contract.sent_at.is_not(None))
    elif user.role not in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux contrats.", "FORBIDDEN")
    return list(db.scalars(stmt).unique().all())


def get_contract(db: Session, user: User, contract_id: str, *, mark_open: bool = False) -> Contract:
    row = db.scalar(
        select(Contract).options(selectinload(Contract.signatures), joinedload(Contract.company)).where(Contract.id == contract_id)
    )
    if not row:
        raise AppError(404, "Contrat introuvable.", "CONTRACT_NOT_FOUND")
    if not _can_access(db, user, row):
        raise AppError(403, "Vous n'avez pas accès à ce contrat.", "FORBIDDEN")
    if user.role == UserRole.EMPLOYER and not row.sent_at:
        raise AppError(404, "Contrat introuvable.", "CONTRACT_NOT_FOUND")
    if mark_open and user.role == UserRole.EMPLOYER and row.sent_at and not row.opened_at:
        row.opened_at = utcnow()
        db.commit()
        row = db.scalar(
            select(Contract).options(selectinload(Contract.signatures), joinedload(Contract.company)).where(Contract.id == contract_id)
        )
    return row


def create_contract(db: Session, user: User, data: ContractIn) -> Contract:
    if user.role not in STAFF:
        raise AppError(403, "Seule l’équipe Talendus peut créer un mandat.", "FORBIDDEN")
    company = db.get(Company, data.company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    status = ContractStatus.DRAFT
    if data.status:
        try:
            status = ContractStatus(data.status.upper())
        except ValueError:
            raise AppError(400, "Statut de contrat invalide.", "VALIDATION_ERROR")
    meta = _template_meta(data.template)
    start, end, _days = mandate_window(data.start_date, data.end_date, meta.get("duration_days"))
    percent = data.commission_percent if data.commission_percent is not None else meta["commission_percent"]
    mandate_type = (data.type or "").strip() or meta["type"]
    draft = ContractIn(
        company_id=company.id,
        type=mandate_type,
        start_date=start,
        end_date=end,
        commission_percent=percent,
        template=meta["key"],
        role=data.role,
    )
    terms = filled_terms(company, draft, template=meta["key"])
    company_id = company.id
    company_name = company.name
    document_name = data.document_name or f"mandat-talendus-{_slug(company_name)}-{start}.pdf"
    try:
        from app.schema_repair import ensure_contracts_schema

        ensure_contracts_schema(db.get_bind())
    except Exception:
        logger.exception("ensure_contracts_schema")
    row = _persist_contract(
        db,
        company_id=company_id,
        mandate_type=mandate_type[:120],
        start=start,
        end=end,
        percent=percent,
        terms=terms,
        status=status,
        recruiter_id=user.id,
        template_key=meta["key"],
        company_name=company_name,
        document_name=document_name,
    )
    audit(db, "contract.create", user, "contract", row.id)
    db.commit()
    return get_contract(db, user, row.id)


def _contract_row(
    company_id: str,
    mandate_type: str,
    start: str,
    end: str,
    percent: int,
    terms: str,
    status: ContractStatus,
    recruiter_id: str,
    template_key: str,
    company_name: str,
    document_name: str | None,
) -> Contract:
    return Contract(
        company_id=company_id,
        type=mandate_type,
        start_date=start,
        end_date=end,
        commission_percent=percent,
        terms=terms,
        document_name=document_name or f"mandat-talendus-{_slug(company_name)}-{start}.pdf",
        status=status,
        recruiter_id=recruiter_id,
        template_key=template_key,
        reminder_count=0,
    )


def _column_names(db: Session) -> set[str]:
    try:
        return {col["name"] for col in inspect(db.get_bind()).get_columns("contracts")}
    except Exception:
        return set()


def _persist_contract(
    db: Session,
    *,
    company_id: str,
    mandate_type: str,
    start: str,
    end: str,
    percent: int,
    terms: str,
    status: ContractStatus,
    recruiter_id: str,
    template_key: str,
    company_name: str,
    document_name: str | None,
) -> Contract:
    attempts = [status]
    if status != ContractStatus.ACTIVE:
        attempts.append(ContractStatus.ACTIVE)
    last_error: Exception | None = None
    for current in attempts:
        row = _contract_row(
            company_id,
            mandate_type,
            start,
            end,
            percent,
            terms,
            current,
            recruiter_id,
            template_key,
            company_name,
            document_name,
        )
        try:
            db.add(row)
            db.flush()
            return row
        except SQLAlchemyError as exc:
            last_error = exc
            logger.warning("Enregistrement mandat status=%s en échec: %s", current, exc)
            db.rollback()
    row_id = _insert_contract_core(
        db,
        company_id=company_id,
        mandate_type=mandate_type,
        start=start,
        end=end,
        percent=percent,
        terms=terms,
        recruiter_id=recruiter_id,
        template_key=template_key,
        company_name=company_name,
        document_name=document_name,
    )
    if row_id:
        row = db.get(Contract, row_id)
        if row:
            return row
    logger.exception("Mandat impossible à enregistrer: %s", last_error)
    raise AppError(
        400,
        "Le brouillon n’a pas pu être enregistré. Vérifiez les dates et l’entreprise, puis réessayez.",
        "CONTRACT_SAVE_FAILED",
    )


def _insert_contract_core(
    db: Session,
    *,
    company_id: str,
    mandate_type: str,
    start: str,
    end: str,
    percent: int,
    terms: str,
    recruiter_id: str,
    template_key: str,
    company_name: str,
    document_name: str | None,
) -> str | None:
    from sqlalchemy import insert

    from app.models.identity import uid

    cols = _column_names(db)
    row_id = uid()
    payload: dict = {
        "id": row_id,
        "company_id": company_id,
        "type": (mandate_type or "Mandat")[:32],
        "start_date": start,
        "end_date": end,
        "commission_percent": percent,
        "terms": terms,
        "status": "ACTIVE",
        "document_name": document_name or f"mandat-talendus-{_slug(company_name)}-{start}.pdf",
        "recruiter_id": recruiter_id,
        "template_key": template_key,
        "reminder_count": 0,
    }
    if cols:
        payload = {key: value for key, value in payload.items() if key in cols}
    try:
        db.execute(insert(Contract.__table__).values(**payload))
        db.flush()
        return row_id
    except SQLAlchemyError as exc:
        logger.warning("Insert SQL mandat en échec: %s", exc)
        db.rollback()
        short = {key: payload[key] for key in ("id", "company_id", "type", "status", "terms") if key in payload}
        short["type"] = (mandate_type or "Mandat")[:20]
        short["status"] = "ACTIVE"
        if "start_date" in (cols or payload):
            short["start_date"] = start
        if "end_date" in (cols or payload):
            short["end_date"] = end
        try:
            db.execute(insert(Contract.__table__).values(**short))
            db.flush()
            return row_id
        except SQLAlchemyError:
            db.rollback()
            return None


def update_contract(db: Session, user: User, contract_id: str, data: ContractPatchIn) -> Contract:
    if user.role not in STAFF:
        raise AppError(403, "Seule l’équipe Talendus peut modifier un mandat.", "FORBIDDEN")
    row = get_contract(db, user, contract_id)
    if row.client_signed_at or _party_signature(row, PARTY_CLIENT):
        raise AppError(409, "Ce mandat est déjà signé par le client.", "ALREADY_SIGNED")
    if row.talendus_signed_at or _party_signature(row, PARTY_TALENDUS):
        raise AppError(409, "Talendus a déjà signé. Préparez un nouveau brouillon pour changer les dates.", "ALREADY_SIGNED")
    if row.sent_at:
        raise AppError(409, "Ce mandat a déjà été envoyé au client.", "ALREADY_SENT")
    company = row.company or db.get(Company, row.company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    meta = _template_meta(data.template or row.template_key)
    start, end, _days = mandate_window(
        data.start_date if data.start_date is not None else row.start_date,
        data.end_date if data.end_date is not None else row.end_date,
        meta.get("duration_days"),
    )
    percent = data.commission_percent if data.commission_percent is not None else (row.commission_percent or meta["commission_percent"])
    mandate_type = (data.type or "").strip() or row.type or meta["type"]
    role = data.role if data.role is not None else _role_from_terms(row.terms)
    row.type = mandate_type
    row.start_date = start
    row.end_date = end
    row.commission_percent = percent
    row.template_key = meta["key"]
    row.terms = filled_terms(
        company,
        ContractIn(
            company_id=company.id,
            type=mandate_type,
            start_date=start,
            end_date=end,
            commission_percent=percent,
            template=meta["key"],
            role=role,
        ),
        template=meta["key"],
    )
    row.document_name = f"mandat-talendus-{_slug(company.name)}-{start}.pdf"
    audit(db, "contract.update", user, "contract", row.id)
    db.commit()
    return get_contract(db, user, row.id)


def _add_signature(db: Session, row: Contract, user: User, data: ContractSignIn, ip: str | None, party: str) -> ContractSignature:
    name = (data.signer_name or user.full_name).strip()
    if not name:
        raise AppError(400, "Le nom du signataire est requis.", "VALIDATION_ERROR")
    stamp = utcnow().isoformat()
    payload = f"{row.id}|{party}|{row.terms or ''}|{row.document_name or ''}|{name}|{stamp}|{ip or ''}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    sig = ContractSignature(
        contract_id=row.id,
        signer_user_id=user.id,
        signer_name=name,
        signer_email=data.signer_email or user.email,
        signed_at=utcnow(),
        ip_address=(ip or "")[:64],
        document_hash=digest,
        document_name=row.document_name,
        accepted=True,
        party=party,
        signer_role=user.role.value if user.role else None,
    )
    db.add(sig)
    return sig


def sign_talendus(db: Session, user: User, contract_id: str, data: ContractSignIn, ip: str | None) -> Contract:
    if user.role not in STAFF:
        raise AppError(403, "Seule l'équipe Talendus peut signer pour l'agence.", "FORBIDDEN")
    row = get_contract(db, user, contract_id)
    if row.talendus_signed_at or _party_signature(row, PARTY_TALENDUS):
        raise AppError(409, "Talendus a déjà signé ce mandat.", "ALREADY_SIGNED")
    now = utcnow()
    _add_signature(db, row, user, data, ip, PARTY_TALENDUS)
    row.talendus_signed_at = now
    audit(db, "contract.sign_talendus", user, "contract", row.id)
    db.commit()
    db.expire_all()
    return get_contract(db, user, row.id)


def sign_contract(db: Session, user: User, contract_id: str, data: ContractSignIn, ip: str | None) -> Contract:
    row = get_contract(db, user, contract_id)
    if user.role not in {UserRole.EMPLOYER} | ADMINS:
        raise AppError(403, "Seuls le client ou un administrateur peuvent signer.", "FORBIDDEN")
    if user.role == UserRole.EMPLOYER and not data.accepted:
        raise AppError(400, "Vous devez accepter les conditions pour signer.", "NOT_ACCEPTED")
    if user.role == UserRole.EMPLOYER and not row.sent_at:
        raise AppError(409, "Ce mandat ne vous a pas encore été transmis.", "NOT_SENT")
    if not row.talendus_signed_at and not _party_signature(row, PARTY_TALENDUS):
        raise AppError(409, "Talendus doit signer le mandat avant le client.", "TALENDUS_NOT_SIGNED")
    if row.client_signed_at or _party_signature(row, PARTY_CLIENT):
        raise AppError(409, "Ce contrat est déjà signé par le client.", "ALREADY_SIGNED")
    now = utcnow()
    sig = _add_signature(db, row, user, data, ip, PARTY_CLIENT)
    row.client_signed_at = now
    row.status = ContractStatus.ACTIVE
    if user.role == UserRole.EMPLOYER and not row.opened_at:
        row.opened_at = now
    audit(db, "contract.sign", user, "contract", row.id, ip, {"hash": sig.document_hash, "party": PARTY_CLIENT})
    from app.services.notifications import notify
    from app.services.ops_notify import frontend, notify_company

    company_name = row.company.name if row.company else "l'entreprise"
    name = sig.signer_name
    notify_company(
        db,
        row.company_id,
        title="Mandat signé",
        message=f"Le mandat a été signé par {name}. La recherche peut commencer.",
        section="contracts",
        template="contract_signed",
        ctx={
            "name": company_name,
            "company": company_name,
            "signer": name,
            "link": f"{frontend()}/espace-employeur.html#/contracts",
        },
        item_id=row.id,
    )
    recipients = []
    if row.recruiter_id:
        recruiter = db.get(User, row.recruiter_id)
        if recruiter and recruiter.is_active:
            recipients.append(recruiter)
    if not recipients:
        recipients = list(
            db.scalars(
                select(User).where(User.role.in_(ADMINS), User.is_active.is_(True)).order_by(User.created_at.asc())
            )
        )
    for person in recipients:
        notify(
            db,
            person,
            NotificationType.ADMIN,
            "Mandat signé par le client",
            f"{name} a signé le mandat de {company_name}. La recherche peut commencer.",
            href=f"/admin/#/clients/{row.company_id}",
        )
    db.commit()
    db.expire_all()
    return get_contract(db, user, row.id)


def send_contract(db: Session, user: User, contract_id: str) -> Contract:
    if user.role not in STAFF:
        raise AppError(403, "Seul l'admin peut envoyer un mandat à signer.", "FORBIDDEN")
    row = get_contract(db, user, contract_id)
    if row.client_signed_at or _party_signature(row, PARTY_CLIENT):
        raise AppError(409, "Ce contrat est déjà signé par le client.", "ALREADY_SIGNED")
    if not row.talendus_signed_at and not _party_signature(row, PARTY_TALENDUS):
        raise AppError(409, "Signez le mandat pour Talendus avant de l'envoyer au client.", "TALENDUS_NOT_SIGNED")
    from app.services.ops_notify import frontend, message_company, notify_company

    first_send = row.sent_at is None
    now = utcnow()
    if first_send:
        row.sent_at = now
    else:
        row.reminder_count = int(row.reminder_count or 0) + 1
        row.last_reminded_at = now
    company = row.company
    title = "Mandat Talendus à signer" if first_send else "Rappel : mandat Talendus à signer"
    message = (
        "Un mandat de recrutement est prêt. Ouvrez-le, lisez-le entièrement, puis signez dans votre espace."
        if first_send
        else "Rappel : un mandat Talendus attend votre lecture et votre signature."
    )
    notify_company(
        db,
        row.company_id,
        title=title,
        message=message,
        section="contracts",
        template="contract_to_sign" if first_send else "contract_reminder",
        ctx={
            "name": company.name if company else "",
            "company": company.name if company else "",
            "type": row.type,
            "percent": str(row.commission_percent or "-"),
            "link": f"{frontend()}/espace-employeur.html#/contracts",
        },
        item_id=row.id,
    )
    audit(db, "contract.send" if first_send else "contract.remind", user, "contract", row.id)
    db.commit()
    try:
        verb = "a été transmis" if first_send else "vous a été renvoyé"
        message_company(
            db,
            user,
            row.company_id,
            f"Le mandat « {row.type} » {verb} pour lecture et signature électronique dans Contrats.",
        )
    except Exception:
        pass
    return get_contract(db, user, row.id)


def open_contract(db: Session, user: User, contract_id: str) -> Contract:
    if user.role != UserRole.EMPLOYER:
        raise AppError(403, "Seul le client peut marquer le mandat comme ouvert.", "FORBIDDEN")
    row = get_contract(db, user, contract_id)
    if not row.opened_at:
        row.opened_at = utcnow()
        audit(db, "contract.open", user, "contract", row.id)
        db.commit()
        db.expire_all()
    return get_contract(db, user, row.id)


def request_esignature(db: Session, user: User, contract_id: str) -> dict:
    from app.integrations.esignature.service import ESignatureService

    row = get_contract(db, user, contract_id)
    if user.role not in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Envoi pour signature électronique réservé à l'équipe Talendus.", "FORBIDDEN")
    result = ESignatureService().create_document(title=row.document_name or row.type or "Contrat Talendus")
    envelope_id = result.get("id") or result.get("envelope_id")
    if envelope_id:
        row.esign_envelope_id = str(envelope_id)[:80]
        row.esign_status = str(result.get("status") or "created")[:32]
        db.commit()
    return result
