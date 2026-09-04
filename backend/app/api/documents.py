from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.rbac import is_admin
from app.services.portal import (
    _finance_can_see,
    delete_document,
    get_document_for_user,
    list_all_documents,
    list_documents,
    list_documents_for_owner,
    serialize_document,
    staff_upload_document,
    upload_document,
)
from app.services.storage import open_stored

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def list_mine(
    owner_type: str | None = None,
    owner_id: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if owner_id and (is_admin(user) or user.role in {UserRole.RECRUITER, UserRole.FINANCE}):
        otype = owner_type or "candidate"
        return ok([serialize_document(row) for row in list_documents_for_owner(db, otype, owner_id) if user.role != UserRole.FINANCE or _finance_can_see(row)])
    if (is_admin(user) or user.role in {UserRole.RECRUITER, UserRole.FINANCE}) and owner_type is None and owner_id is None:
        return ok([serialize_document(row) for row in list_all_documents(db, user)])
    return ok(list_documents(db, user, owner_type))


@router.post("")
async def upload(
    file: UploadFile = File(...),
    kind: str = Form(default="other"),
    owner_type: str | None = Form(default=None),
    owner_id: str | None = Form(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await file.read()
    if owner_id and (is_admin(user) or user.role in {UserRole.RECRUITER, UserRole.FINANCE}):
        row = staff_upload_document(db, user, data, file.filename or "document", kind, owner_type or "candidate", owner_id)
        return ok(serialize_document(row), message="Document enregistré.")
    row = upload_document(db, user, data, file.filename or "document", kind, owner_type)
    return ok(serialize_document(row), message="Document enregistré.")


@router.get("/{document_id}/file")
def download(
    document_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = get_document_for_user(db, user, document_id)
    url, path = open_stored(row.stored_name, row.storage_url, "documents")
    if url:
        return RedirectResponse(url)
    return FileResponse(path, media_type=row.mime_type, filename=row.original_name)


@router.get("/{document_id}/preview")
def preview_document(
    document_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.resume_parse import preview_html
    from app.services.storage import read_stored_bytes

    row = get_document_for_user(db, user, document_id)
    data = read_stored_bytes(row.stored_name, row.storage_url, "documents")
    return HTMLResponse(preview_html(data, row.mime_type, row.original_name))


@router.delete("/{document_id}")
def remove(
    document_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    delete_document(db, user, document_id)
    return ok(message="Document supprimé.")
