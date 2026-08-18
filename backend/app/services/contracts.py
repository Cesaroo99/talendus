import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import AppError
from app.models import Company, Contract, ContractSignature, User
from app.models.enums import ContractStatus, UserRole, utcnow
from app.rbac import ADMINS
from app.schemas import ContractIn, ContractSignIn
from app.services.access import company_ids_for_employer
from app.services.audit import audit


def serialize_signature(row: ContractSignature) -> dict:
    return {
        "id": row.id,
        "signer_name": row.signer_name,
        "signer_email": row.signer_email,
        "signed_at": row.signed_at.isoformat() if row.signed_at else None,
        "ip_address": row.ip_address,
        "document_hash": row.document_hash,
        "document_name": row.document_name,
        "accepted": row.accepted,
    }


def serialize_contract(row: Contract) -> dict:
    latest = row.signatures[-1] if row.signatures else None
    return {
        "id": row.id,
        "company_id": row.company_id,
        "type": row.type,
        "start_date": row.start_date,
        "end_date": row.end_date,
        "commission_percent": row.commission_percent,
        "terms": row.terms,
        "status": row.status.value if row.status else None,
        "document_name": row.document_name,
        "esign_envelope_id": row.esign_envelope_id,
        "esign_status": row.esign_status,
        "signed": bool(latest),
        "signature": serialize_signature(latest) if latest else None,
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
        stmt = stmt.where(Contract.company_id.in_(ids))
    elif user.role not in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès aux contrats.", "FORBIDDEN")
    return list(db.scalars(stmt).unique().all())


def get_contract(db: Session, user: User, contract_id: str) -> Contract:
    row = db.scalar(
        select(Contract).options(selectinload(Contract.signatures), joinedload(Contract.company)).where(Contract.id == contract_id)
    )
    if not row:
        raise AppError(404, "Contrat introuvable.", "CONTRACT_NOT_FOUND")
    if not _can_access(db, user, row):
        raise AppError(403, "Vous n'avez pas accès à ce contrat.", "FORBIDDEN")
    return row


def create_contract(db: Session, user: User, data: ContractIn) -> Contract:
    if user.role not in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS:
        raise AppError(403, "Seule l’équipe Talendus peut créer un mandat.", "FORBIDDEN")
    company = db.get(Company, data.company_id)
    if not company:
        raise AppError(404, "Entreprise introuvable.", "COMPANY_NOT_FOUND")
    status = ContractStatus.ACTIVE
    if data.status:
        try:
            status = ContractStatus(data.status.upper())
        except ValueError:
            raise AppError(400, "Statut de contrat invalide.", "VALIDATION_ERROR")
    from app.services.ops_notify import frontend, message_company, notify_company
    from app.services.pdf_docs import DEFAULT_MANDATE_TERMS

    terms = (data.terms or "").strip() or DEFAULT_MANDATE_TERMS
    if data.commission_percent:
        terms = f"Commission : {data.commission_percent} %.\n\n" + terms
    row = Contract(
        company_id=company.id,
        type=data.type.strip(),
        start_date=data.start_date,
        end_date=data.end_date,
        commission_percent=data.commission_percent,
        terms=terms,
        document_name=data.document_name or "mandat-talendus.pdf",
        status=status,
        recruiter_id=user.id,
    )
    db.add(row)
    db.flush()
    audit(db, "contract.create", user, "contract", row.id)
    notify_company(
        db,
        company.id,
        title="Mandat Talendus à signer",
        message="Un mandat de recrutement est prêt. Ouvrez-le, lisez le PDF et signez dans votre espace.",
        section="contracts",
        template="contract_to_sign",
        ctx={
            "name": company.name,
            "company": company.name,
            "type": row.type,
            "percent": str(row.commission_percent or "-"),
            "link": f"{frontend()}/espace-employeur.html#/contracts",
        },
        item_id=row.id,
    )
    db.commit()
    try:
        message_company(
            db,
            user,
            company.id,
            f"Un mandat « {row.type} » est prêt à signer dans Contrats. Signature électronique interne Talendus, sans DocuSign.",
        )
    except Exception:
        pass
    return get_contract(db, user, row.id)


def sign_contract(db: Session, user: User, contract_id: str, data: ContractSignIn, ip: str | None) -> Contract:
    row = get_contract(db, user, contract_id)
    if user.role not in {UserRole.EMPLOYER} | ADMINS:
        raise AppError(403, "Seuls le client ou un administrateur peuvent signer.", "FORBIDDEN")
    if user.role == UserRole.EMPLOYER and not data.accepted:
        raise AppError(400, "Vous devez accepter les conditions pour signer.", "NOT_ACCEPTED")
    if row.signatures:
        raise AppError(409, "Ce contrat est déjà signé.", "ALREADY_SIGNED")
    name = (data.signer_name or user.full_name).strip()
    if not name:
        raise AppError(400, "Le nom du signataire est requis.", "VALIDATION_ERROR")
    stamp = utcnow().isoformat()
    payload = f"{row.id}|{row.terms or ''}|{row.document_name or ''}|{name}|{stamp}|{ip or ''}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    db.add(
        ContractSignature(
            contract_id=row.id,
            signer_user_id=user.id,
            signer_name=name,
            signer_email=data.signer_email or user.email,
            signed_at=utcnow(),
            ip_address=(ip or "")[:64],
            document_hash=digest,
            document_name=row.document_name,
            accepted=True,
        )
    )
    audit(db, "contract.sign", user, "contract", row.id, ip, {"hash": digest})
    from app.services.ops_notify import frontend, notify_company

    company_name = row.company.name if row.company else "l'entreprise"
    notify_company(
        db,
        row.company_id,
        title="Mandat signé",
        message=f"Le mandat a été signé par {name}.",
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
