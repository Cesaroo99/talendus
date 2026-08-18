from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import ContractIn, ContractSignIn
from app.services import contracts as contracts_service
from app.services import pdf_docs

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("")
def list_contracts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok([contracts_service.serialize_contract(row) for row in contracts_service.list_contracts(db, user)])


@router.post("")
def create_contract(
    payload: ContractIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    row = contracts_service.create_contract(db, user, payload)
    return ok(contracts_service.serialize_contract(row), message="Mandat créé.")


@router.get("/{contract_id}")
def get_contract(contract_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(contracts_service.serialize_contract(contracts_service.get_contract(db, user, contract_id)))


@router.get("/{contract_id}/pdf")
def contract_pdf(contract_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = contracts_service.get_contract(db, user, contract_id)
    data = pdf_docs.contract_pdf(row)
    filename = row.document_name or "mandat-talendus.pdf"
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{contract_id}/sign")
def sign_contract(
    contract_id: str,
    payload: ContractSignIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER, UserRole.ADMIN)),
):
    row = contracts_service.sign_contract(db, user, contract_id, payload, client_ip(request))
    return ok(contracts_service.serialize_contract(row), message="Contrat signé.")


@router.post("/{contract_id}/esign")
def request_esign(
    contract_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    return ok(contracts_service.request_esignature(db, user, contract_id))
