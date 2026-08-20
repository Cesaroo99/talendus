from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import AppError, ok
from app.models import User
from app.models.enums import AccountStatus, UserRole, utcnow
from app.schemas import UserPreferenceIn, UserPublic, UserUpdateIn
from app.services.audit import audit
from app.services.portal import set_avatar
from app.services.settings import ensure_preferences, serialize_preferences, update_preferences
from app.services.storage import open_stored

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return ok(UserPublic.model_validate(user).model_dump(mode="json"))


@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await file.read()
    updated = set_avatar(db, user, data, file.filename or "photo")
    return ok(UserPublic.model_validate(updated).model_dump(mode="json"), message="Photo enregistrée.")


@router.get("/me/avatar")
def my_avatar(user: User = Depends(get_current_user)):
    if not user.avatar_path:
        raise AppError(404, "Aucune photo.", "NOT_FOUND")
    url, path = open_stored(user.avatar_path, None, "avatars")
    if url:
        return RedirectResponse(url)
    return FileResponse(path, media_type="image/jpeg")


@router.patch("/me")
def update_me(payload: UserUpdateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    audit(db, "user.update", user, "user", user.id)
    db.commit()
    db.refresh(user)
    return ok(UserPublic.model_validate(user).model_dump(mode="json"))


@router.get("/me/preferences")
def get_preferences(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = ensure_preferences(db, user)
    db.commit()
    return ok(serialize_preferences(row))


@router.patch("/me/preferences")
def patch_preferences(
    payload: UserPreferenceIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = update_preferences(db, user, payload)
    return ok(serialize_preferences(row))


@router.post("/me/deactivate")
def deactivate(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.is_active = False
    user.account_status = AccountStatus.DEACTIVATED
    user.deactivated_at = utcnow()
    audit(db, "user.deactivate", user, "user", user.id)
    db.commit()
    return ok(message="Compte désactivé.")
