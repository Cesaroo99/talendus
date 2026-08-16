from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import ok
from app.models import User
from app.models.enums import UserRole, utcnow
from app.schemas import UserPublic, UserUpdateIn
from app.services.audit import audit

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return ok(UserPublic.model_validate(user).model_dump())


@router.patch("/me")
def update_me(payload: UserUpdateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    audit(db, "user.update", user, "user", user.id)
    db.commit()
    db.refresh(user)
    return ok(UserPublic.model_validate(user).model_dump())


@router.post("/me/deactivate")
def deactivate(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.is_active = False
    user.deactivated_at = utcnow()
    audit(db, "user.deactivate", user, "user", user.id)
    db.commit()
    return ok(message="Compte désactivé.")
