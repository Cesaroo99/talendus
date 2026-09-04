from fastapi import APIRouter, Depends, File, Query, UploadFile
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
    Recruiter,
    Role,
    User,
)
from app.models.enums import UserRole
from app.rbac import PERMISSIONS
from app.schemas import (
    AdminCandidateIn,
    AdminCandidatePatchIn,
    EmailTestIn,
    SiteContentIn,
    StaffUserIn,
    StaffUserPatchIn,
    SystemSettingIn,
)
from app.services import admin_export, candidates as cand_svc
from app.services.settings import (
    CMS_KEYS,
    ensure_platform_defaults,
    get_json_setting,
    put_json_setting,
    serialize_setting,
    upsert_setting,
)

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


@router.patch("/candidates/{candidate_id}")
def patch_candidate(
    candidate_id: str,
    payload: AdminCandidatePatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    profile = cand_svc.update_staff_candidate(db, user, candidate_id, payload)
    return ok(cand_svc.serialize_candidate(profile, include_private=True), message="Fiche candidat mise à jour.")


@router.post("/candidates/{candidate_id}/resume")
async def upload_candidate_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    data = await file.read()
    if not data:
        raise AppError(400, "Fichier vide.", "VALIDATION_ERROR")
    row = cand_svc.upload_cv_for_candidate(db, user, candidate_id, data, file.filename or "cv")
    return ok(
        {
            "id": row.id,
            "original_name": row.original_name,
            "size_bytes": row.size_bytes,
            "download_path": f"/api/candidates/resumes/{row.id}/file",
        },
        message="Document enregistré.",
    )


@router.get("/site-content/{key}")
def get_site_content(key: str, db: Session = Depends(get_db), _: User = Depends(_staff)):
    if key not in CMS_KEYS:
        raise AppError(404, "Contenu introuvable.", "NOT_FOUND")
    return ok(get_json_setting(db, f"cms.{key}", default=[]))


@router.put("/site-content/{key}")
def put_site_content(
    key: str,
    payload: SiteContentIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.EDITOR, UserRole.ADMIN, UserRole.RECRUITER)),
):
    if key not in CMS_KEYS:
        raise AppError(404, "Contenu introuvable.", "NOT_FOUND")
    items = _normalize_cms_items(key, payload.items)
    stored = put_json_setting(db, user, f"cms.{key}", items, label=f"CMS {key}")
    return ok(stored, message="Contenu enregistré.")


def _normalize_cms_items(key: str, items: list[dict]) -> list[dict]:
    from app.models.identity import uid
    from app.models.enums import utcnow

    cleaned = []
    today = utcnow().strftime("%Y-%m-%d")
    for raw in items or []:
        if not isinstance(raw, dict):
            continue
        item_id = str(raw.get("id") or uid())
        status = str(raw.get("status") or "publie")
        if key == "faq":
            question = str(raw.get("q") or raw.get("title") or "").strip()
            answer = str(raw.get("a") or raw.get("body") or "").strip()
            if not question:
                continue
            cleaned.append({"id": item_id, "q": question, "a": answer, "status": status, "updatedAt": today})
        else:
            author = str(raw.get("author") or raw.get("title") or "").strip()
            quote = str(raw.get("quote") or raw.get("body") or "").strip()
            role = str(raw.get("role") or "").strip()
            if not author and not quote:
                continue
            cleaned.append(
                {"id": item_id, "author": author, "role": role, "quote": quote, "status": status, "updatedAt": today}
            )
    return cleaned


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


@router.get("/analytics")
def analytics(
    period: str = Query(default="mois"),
    db: Session = Depends(get_db),
    _: User = Depends(_staff),
):
    from app.services.tracking import analytics_snapshot

    return ok(analytics_snapshot(db, period))


STAFF_CREATE_ROLES = {UserRole.RECRUITER, UserRole.FINANCE, UserRole.EDITOR, UserRole.ADMIN}


def _serialize_staff(u: User) -> dict:
    return {
        "id": u.id,
        "email": u.email,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "role": u.role.value,
        "title": u.title,
        "phone": u.phone,
        "is_active": u.is_active,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


def _assert_can_assign_role(admin: User, role: UserRole) -> None:
    if role not in STAFF_CREATE_ROLES and role != UserRole.SUPER_ADMIN:
        raise AppError(400, "Ce rôle n’est pas un accès interne.", "INVALID_ROLE")
    if role == UserRole.SUPER_ADMIN and admin.role != UserRole.SUPER_ADMIN:
        raise AppError(403, "Seul un super-admin peut attribuer ce niveau.", "FORBIDDEN")


@router.get("/users")
def list_users(db: Session = Depends(get_db), _: User = Depends(_admin_user)):
    users = db.scalars(select(User).order_by(User.created_at.desc())).all()
    return ok([_serialize_staff(u) for u in users])


@router.post("/users")
def create_staff(
    payload: StaffUserIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    from app.security import hash_password
    from app.services.audit import audit
    from app.services.settings import ensure_preferences

    _assert_can_assign_role(admin, payload.role)
    email = str(payload.email).lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise AppError(409, "Un compte existe déjà avec ce courriel.", "EMAIL_TAKEN")
    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        phone=payload.phone,
        role=payload.role,
        title=payload.title,
        is_email_verified=True,
    )
    db.add(user)
    db.flush()
    ensure_preferences(db, user)
    if user.role == UserRole.RECRUITER:
        db.add(Recruiter(user_id=user.id))
    from app.models.enums import EmailType
    from app.services.email import send_email
    from app.services.ops_notify import frontend

    send_email(
        db,
        user.email,
        EmailType.WELCOME,
        "welcome",
        name=user.first_name,
        link=f"{frontend()}/admin/",
    )
    audit(db, "admin.user_create", admin, "user", user.id, metadata={"role": user.role.value})
    db.commit()
    db.refresh(user)
    return ok(_serialize_staff(user), message="Accès créé.")


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    payload: StaffUserPatchIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    from app.services.audit import audit

    target = db.get(User, user_id)
    if not target:
        raise AppError(404, "Utilisateur introuvable.", "USER_NOT_FOUND")
    data = payload.model_dump(exclude_unset=True)
    if "role" in data and data["role"] is not None:
        _assert_can_assign_role(admin, data["role"])
        if target.id == admin.id and data["role"] != admin.role:
            raise AppError(400, "Vous ne pouvez pas modifier votre propre niveau d’accès.", "FORBIDDEN")
    if data.get("is_active") is False and target.id == admin.id:
        raise AppError(400, "Vous ne pouvez pas désactiver votre propre accès.", "FORBIDDEN")
    for key, value in data.items():
        setattr(target, key, value)
    if target.role == UserRole.RECRUITER and not target.recruiter:
        db.add(Recruiter(user_id=target.id))
    audit(db, "admin.user_update", admin, "user", target.id)
    db.commit()
    db.refresh(target)
    return ok(_serialize_staff(target))


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
    _assert_can_assign_role(admin, payload.role)
    if target.id == admin.id and payload.role != admin.role:
        raise AppError(400, "Vous ne pouvez pas modifier votre propre niveau d’accès.", "FORBIDDEN")
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
def get_settings(db: Session = Depends(get_db), user: User = Depends(_admin_user)):
    rows = ensure_platform_defaults(db, user)
    return ok([serialize_setting(row) for row in rows if not row.key.startswith("cms.")])


@router.patch("/settings")
def patch_setting(
    payload: SystemSettingIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    row = upsert_setting(db, admin, payload.key, payload.value, payload.label)
    return ok(serialize_setting(row))


TEST_INBOX = "cesarmemoli1@gmail.com"


def _test_inbox(payload: EmailTestIn, admin: User) -> str:
    if payload.to_email:
        return str(payload.to_email).lower()
    current = (admin.email or "").strip().lower()
    if current in {"lea.super@talendus.ca", "sophie.admin@talendus.ca"} or current.endswith("@talendus.ca"):
        return TEST_INBOX
    return current or TEST_INBOX


@router.post("/settings/test-email")
def send_test_email(
    payload: EmailTestIn,
    db: Session = Depends(get_db),
    admin: User = Depends(_admin_user),
):
    from app.models.enums import EmailStatus, EmailType
    from app.services.email import send_email
    from app.services.ops_notify import frontend

    to_email = _test_inbox(payload, admin)
    log = send_email(
        db,
        to_email,
        EmailType.ADMIN,
        "smtp_test",
        sync=True,
        name=admin.first_name or "Admin",
        link=f"{frontend()}/admin/#/settings",
    )
    db.commit()
    status = log.status.value if log.status else EmailStatus.QUEUED.value
    if log.status == EmailStatus.FAILED:
        raise AppError(
            502,
            f"L’envoi vers {to_email} a échoué : {log.error or 'erreur SMTP'}. Vérifiez identifiant, mot de passe d’application et « Activer l’envoi ».",
            "SMTP_SEND_FAILED",
        )
    return ok(
        {"to_email": to_email, "status": status, "error": log.error},
        message=f"Test {status.lower()} vers {to_email} depuis info@talendus.ca.",
    )
