import logging
import re
from pathlib import Path

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import AppError
from app.models import User
from app.models.enums import UserRole
from app.rbac import can, is_admin
from app.security import decode_access_token

logger = logging.getLogger("talendus")
bearer = HTTPBearer(auto_error=False)


def get_current_user_optional(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User | None:
    if not creds:
        return None
    try:
        payload = decode_access_token(creds.credentials)
    except ValueError:
        return None
    user = db.get(User, payload.get("sub"))
    if not user or not user.is_active:
        return None
    if user.account_status and user.account_status.value in {"SUSPENDED", "DEACTIVATED"}:
        return None
    return user


def get_current_user(user: User | None = Depends(get_current_user_optional)) -> User:
    if not user:
        raise AppError(401, "Authentification requise.", "UNAUTHENTICATED")
    return user


def require_roles(*roles: UserRole):
    def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles and not is_admin(user):
            raise AppError(403, "Vous n'avez pas accès à cette ressource.", "FORBIDDEN")
        return user

    return _dep


def require_permission(permission: str):
    def _dep(user: User = Depends(get_current_user)) -> User:
        if not can(user.role, permission):
            raise AppError(403, "Permission insuffisante.", "FORBIDDEN")
        return user

    return _dep


def client_ip(request: Request, forwarded: str | None = None) -> str:
    header = forwarded or request.headers.get("x-forwarded-for")
    if header:
        return header.split(",")[0].strip()[:64]
    return (request.client.host if request.client else "")[:64]


SLUG_RE = re.compile(r"[^a-z0-9-]+")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[àáâä]", "a", value)
    value = re.sub(r"[éèêë]", "e", value)
    value = re.sub(r"[îï]", "i", value)
    value = re.sub(r"[ôö]", "o", value)
    value = re.sub(r"[ùûü]", "u", value)
    value = re.sub(r"[ç]", "c", value)
    value = re.sub(r"\s+", "-", value)
    value = SLUG_RE.sub("", value)
    return value.strip("-") or "offre"


def safe_filename(name: str) -> str:
    base = Path(name).name
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    return base[:180] or "cv.pdf"
