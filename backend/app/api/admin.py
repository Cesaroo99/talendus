from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.database import get_db
from app.deps import require_roles
from app.errors import AppError, ok
from app.models import (
    Application,
    AuditLog,
    Candidate,
    Company,
    JobOffer,
    Permission,
    Role,
    User,
)
from app.models.enums import UserRole
from app.rbac import PERMISSIONS
from app.schemas import AdminCandidateIn, SystemSettingIn, UserUpdateIn
from app.services import admin_export, candidates as cand_svc
from app.services.settings import list_settings, serialize_setting, upsert_setting

router = APIRouter(prefix="/admin", tags=["admin"])


class RoleIn(BaseModel):
    role: UserRole


def _staff(user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE, UserRole.EDITOR))) -> User:
    return user


def _admin_user(user: User = Depends(require_roles(UserRole.ADMIN))) -> User:
    return user


@router.get("/bootstrap")
def bootstrap(db: Session = Depends(get_db), user: User = Depends(_staff)):
    return ok(admin_export.bootstrap(db, user))


@router.post("/candidates")
def create_candidate(
    payload: AdminCandidateIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    profile = cand_svc.create_staff_candidate(db, user, payload)
    return ok({"id": profile.id, "email": payload.email})


@router.get("/stats")
def stats(db: Session = Depends(get_db), _: User = Depends(_admin_user)):
    def count(model) -> int:
        return int(db.scalar(select(func.count()).select_from(model)) or 0)

    return ok(
        {
            "users": count(User),
            "candidates": count(Candidate),
            "companies": count(Company),
            "jobs": count(JobOffer),
            "applications": count(Application),
        }
    )


@router.get("/users")
def list_users(db: Session = Depends(get_db), _: User = Depends(_admin_user)):
    users = db.scalars(select(User).order_by(User.created_at.desc())).all()
    return ok(
        [
            {
                "id": u.id,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "role": u.role.value,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]
    )


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    payload: UserUpdateIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    from app.services.audit import audit

    target = db.get(User, user_id)
    if not target:
        raise AppError(404, "Utilisateur introuvable.", "USER_NOT_FOUND")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(target, key, value)
    audit(db, "admin.user_update", admin, "user", target.id)
    db.commit()
    return ok({"id": target.id, "email": target.email, "role": target.role.value})


@router.post("/users/{user_id}/role")
def set_role(
    user_id: str,
    payload: RoleIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    from app.services.audit import audit

    target = db.get(User, user_id)
    if not target:
        raise AppError(404, "Utilisateur introuvable.", "USER_NOT_FOUND")
    target.role = payload.role
    audit(db, "admin.role_change", admin, "user", target.id, metadata={"role": payload.role.value})
    db.commit()
    return ok({"id": target.id, "role": target.role.value})


@router.get("/audit")
def audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(_admin_user),
):
    rows = db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)).all()
    return ok(
        [
            {
                "id": r.id,
                "action": r.action,
                "actor_id": r.actor_id,
                "entity_type": r.entity_type,
                "entity_id": r.entity_id,
                "ip_address": r.ip_address,
                "old_value": r.old_value,
                "new_value": r.new_value,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    )


@router.get("/permissions")
def permissions(db: Session = Depends(get_db), _: User = Depends(_admin_user)):
    roles = db.scalars(select(Role)).all()
    catalog = {
        role.code: [p.code for p in role.permissions]
        for role in roles
    }
    if not catalog:
        catalog = {code: sorted(r.value for r in allowed) for code, allowed in PERMISSIONS.items()}
    return ok(catalog)


@router.get("/settings")
def get_settings(db: Session = Depends(get_db), _: User = Depends(_admin_user)):
    return ok([serialize_setting(row) for row in list_settings(db)])


@router.patch("/settings")
def patch_setting(
    payload: SystemSettingIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    row = upsert_setting(db, admin, payload.key, payload.value, payload.label)
    return ok(serialize_setting(row))
