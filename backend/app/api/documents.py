from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.services.portal import delete_document, get_document_for_user, list_documents, serialize_document, upload_document
from app.services.storage import open_stored

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def list_mine(
    owner_type: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return ok(list_documents(db, user, owner_type))


@router.post("")
async def upload(
    file: UploadFile = File(...),
    kind: str = Form(default="other"),
    owner_type: str | None = Form(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await file.read()
    row = upload_document(db, user, data, file.filename or "document.pdf", kind, owner_type)
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


@router.delete("/{document_id}")
def remove(
    document_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    delete_document(db, user, document_id)
    return ok(message="Document supprimé.")
