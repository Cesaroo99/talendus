import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import AppError
from app.models import Company, Contract, ContractSignature, User
from app.models.enums import UserRole, utcnow
from app.schemas import ContractSignIn
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
        "signed": bool(latest),
        "signature": serialize_signature(latest) if latest else None,
    }


def _can_access(db: Session, user: User, contract: Contract) -> bool:
    if user.role in {UserRole.ADMIN, UserRole.RECRUITER, UserRole.FINANCE}:
        return True
    if user.role == UserRole.EMPLOYER:
        company = db.scalar(select(Company).where(Company.owner_user_id == user.id))
        return bool(company and company.id == contract.company_id)
    return False


def list_contracts(db: Session, user: User) -> list[Contract]:
    stmt = select(Contract).options(selectinload(Contract.signatures), joinedload(Contract.company))
    if user.role == UserRole.EMPLOYER:
        company = db.scalar(select(Company).where(Company.owner_user_id == user.id))
        if not company:
            return []
        stmt = stmt.where(Contract.company_id == company.id)
    elif user.role not in {UserRole.ADMIN, UserRole.RECRUITER, UserRole.FINANCE}:
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


def sign_contract(db: Session, user: User, contract_id: str, data: ContractSignIn, ip: str | None) -> Contract:
    row = get_contract(db, user, contract_id)
    if user.role not in {UserRole.EMPLOYER, UserRole.ADMIN}:
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
    db.commit()
    db.expire_all()
    return get_contract(db, user, row.id)
