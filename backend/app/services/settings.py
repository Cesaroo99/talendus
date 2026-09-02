from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import SystemSetting, User, UserPreference
from app.services.audit import audit


def serialize_preferences(row: UserPreference) -> dict:
    return {
        "locale": row.locale,
        "notify_email": row.notify_email,
        "notify_in_app": row.notify_in_app,
        "notify_application": row.notify_application,
        "notify_message": row.notify_message,
        "notify_match": row.notify_match,
        "notify_interview": row.notify_interview,
        "notify_sms": getattr(row, "notify_sms", False),
        "notify_whatsapp": getattr(row, "notify_whatsapp", False),
        "notify_push": getattr(row, "notify_push", False),
        "privacy_profile_public": row.privacy_profile_public,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


def ensure_preferences(db: Session, user: User) -> UserPreference:
    if user.preferences:
        return user.preferences
    row = UserPreference(user_id=user.id)
    db.add(row)
    db.flush()
    return row


def update_preferences(db: Session, user: User, data) -> UserPreference:
    row = ensure_preferences(db, user)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    audit(db, "user.preferences", user, "user", user.id)
    db.commit()
    db.refresh(row)
    return row


def list_settings(db: Session) -> list[SystemSetting]:
    from sqlalchemy import select

    return list(db.scalars(select(SystemSetting).order_by(SystemSetting.key.asc())).all())


def upsert_setting(db: Session, user: User, key: str, value: str, label: str | None = None) -> SystemSetting:
    from sqlalchemy import select

    key = key.strip()
    if not key:
        raise AppError(400, "La clé de paramètre est requise.", "VALIDATION_ERROR")
    row = db.scalar(select(SystemSetting).where(SystemSetting.key == key))
    old = row.value if row else None
    if row:
        row.value = value
        if label is not None:
            row.label = label
        row.updated_by = user.id
    else:
        row = SystemSetting(key=key, value=value, label=label, updated_by=user.id)
        db.add(row)
    audit(db, "admin.setting", user, "system_setting", row.id, metadata={"key": key}, old_value=old, new_value=value)
    db.commit()
    db.refresh(row)
    return row


def serialize_setting(row: SystemSetting) -> dict:
    return {
        "id": row.id,
        "key": row.key,
        "value": row.value,
        "label": row.label,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        "updated_by": row.updated_by,
    }


PLATFORM_DEFAULTS = (
    ("agency_name", "Talendus", "Nom de l’agence"),
    ("support_email", "ivan.p@example.net", "Courriel interne"),
    ("default_commission_percent", "16", "Commission type (%)"),
    ("invoice_payment_days", "30", "Délai de paiement (jours)"),
    ("billing.legal_name", "Talendus", "Raison sociale (factures)"),
    ("billing.address", "Montréal (Québec) Canada", "Adresse de facturation"),
    ("billing.neq", "", "NEQ (Registraire des entreprises du Québec)"),
    ("billing.gst", "", "N° de TPS (RT)"),
    ("billing.qst", "", "N° de TVQ"),
)

CMS_KEYS = {"testimonials", "faq"}


def ensure_platform_defaults(db: Session, user: User | None = None) -> list[SystemSetting]:
    from sqlalchemy import select

    existing = {row.key: row for row in list_settings(db)}
    changed = False
    for key, value, label in PLATFORM_DEFAULTS:
        if key in existing:
            continue
        db.add(SystemSetting(key=key, value=value, label=label, updated_by=user.id if user else None))
        changed = True
    if changed:
        db.commit()
    return list_settings(db)


def get_json_setting(db: Session, key: str, default=None):
    import json
    from sqlalchemy import select

    row = db.scalar(select(SystemSetting).where(SystemSetting.key == key))
    if not row or not (row.value or "").strip():
        return default if default is not None else []
    try:
        return json.loads(row.value)
    except json.JSONDecodeError:
        return default if default is not None else []


def put_json_setting(db: Session, user: User, key: str, value, label: str | None = None) -> list | dict:
    import json

    payload = json.dumps(value, ensure_ascii=False)
    upsert_setting(db, user, key, payload, label)
    parsed = get_json_setting(db, key, default=value)
    return parsed
