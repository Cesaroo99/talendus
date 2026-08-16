from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import ContractSignIn
from app.services import contracts as contracts_service

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("")
def list_contracts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok([contracts_service.serialize_contract(row) for row in contracts_service.list_contracts(db, user)])


@router.get("/{contract_id}")
def get_contract(contract_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(contracts_service.serialize_contract(contracts_service.get_contract(db, user, contract_id)))


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
