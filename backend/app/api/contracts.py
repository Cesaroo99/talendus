from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import ContractIn, ContractPatchIn, ContractSignIn
from app.services import contracts as contracts_service
from app.services import pdf_docs

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("")
def list_contracts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok([contracts_service.serialize_contract(row) for row in contracts_service.list_contracts(db, user)])


@router.get("/templates")
def contract_templates(user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE))):
    return ok(contracts_service.list_templates())


@router.get("/preview")
def preview_contract(
    company_id: str,
    template: str | None = None,
    commission_percent: int | None = None,
    role: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    return ok(
        contracts_service.preview_contract(
            db, user, company_id, template, commission_percent, role, start_date, end_date
        )
    )


@router.post("")
def create_contract(
    payload: ContractIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    row = contracts_service.create_contract(db, user, payload, client_ip(request))
    return ok(contracts_service.serialize_contract(row), message="Mandat préparé et signé pour Talendus. Envoyez-le au client.")


@router.patch("/{contract_id}")
def update_contract(
    contract_id: str,
    payload: ContractPatchIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    row = contracts_service.update_contract(db, user, contract_id, payload, client_ip(request))
    return ok(contracts_service.serialize_contract(row), message="Brouillon mis à jour.")


@router.get("/{contract_id}")
def get_contract(contract_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(contracts_service.serialize_contract(contracts_service.get_contract(db, user, contract_id, mark_open=True)))


@router.get("/{contract_id}/pdf")
def contract_pdf(
    contract_id: str,
    download: int = 0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = contracts_service.get_contract(db, user, contract_id, mark_open=True)
    data = pdf_docs.contract_pdf(row)
    filename = row.document_name or "mandat-talendus.pdf"
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    disposition = "attachment" if download else "inline"
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'{disposition}; filename="{filename}"'},
    )


@router.post("/{contract_id}/send")
def send_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    row = contracts_service.send_contract(db, user, contract_id)
    first = int(row.reminder_count or 0) == 0
    message = "Mandat envoyé au client." if first and row.sent_at else "Mandat renvoyé au client."
    if row.reminder_count:
        message = "Mandat renvoyé au client."
    return ok(contracts_service.serialize_contract(row), message=message)


@router.post("/{contract_id}/open")
def open_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EMPLOYER)),
):
    row = contracts_service.open_contract(db, user, contract_id)
    return ok(contracts_service.serialize_contract(row), message="Mandat ouvert.")


@router.post("/{contract_id}/sign-talendus")
def sign_talendus(
    contract_id: str,
    payload: ContractSignIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE)),
):
    row = contracts_service.sign_talendus(db, user, contract_id, payload, client_ip(request))
    return ok(contracts_service.serialize_contract(row), message="Mandat signé pour Talendus.")


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
