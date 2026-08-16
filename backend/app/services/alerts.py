from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import User
from app.models.job import JobOffer
from app.models.portal import JobAlert
from app.schemas import JobAlertIn, JobAlertPatchIn
from app.services.auth import ensure_candidate


def serialize_alert(row: JobAlert) -> dict:
    return {
        "id": row.id,
        "keywords": row.keywords,
        "city": row.city,
        "province": row.province,
        "sector": row.sector,
        "contract_type": row.contract_type,
        "active": row.active,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def list_alerts(db: Session, user: User) -> list[dict]:
    ensure_candidate(db, user)
    rows = list(
        db.scalars(select(JobAlert).where(JobAlert.user_id == user.id).order_by(JobAlert.created_at.desc())).all()
    )
    return [serialize_alert(r) for r in rows]


def create_alert(db: Session, user: User, data: JobAlertIn) -> dict:
    ensure_candidate(db, user)
    count = len(list(db.scalars(select(JobAlert).where(JobAlert.user_id == user.id)).all()))
    if count >= 20:
        raise AppError(400, "Maximum de 20 alertes atteint.", "ALERT_LIMIT")
    row = JobAlert(
        user_id=user.id,
        keywords=(data.keywords or "").strip() or None,
        city=(data.city or "").strip() or None,
        province=(data.province or "").strip() or None,
        sector=(data.sector or "").strip() or None,
        contract_type=(data.contract_type or "").strip() or None,
        active=True if data.active is None else bool(data.active),
    )
    if not any([row.keywords, row.city, row.province, row.sector, row.contract_type]):
        raise AppError(400, "Indiquez au moins un critère (mots-clés, ville ou secteur).", "ALERT_EMPTY")
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize_alert(row)


def update_alert(db: Session, user: User, alert_id: str, data: JobAlertPatchIn) -> dict:
    row = db.get(JobAlert, alert_id)
    if not row or row.user_id != user.id:
        raise AppError(404, "Alerte introuvable.", "ALERT_NOT_FOUND")
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        if isinstance(value, str):
            value = value.strip() or None
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return serialize_alert(row)


def delete_alert(db: Session, user: User, alert_id: str) -> None:
    row = db.get(JobAlert, alert_id)
    if not row or row.user_id != user.id:
        raise AppError(404, "Alerte introuvable.", "ALERT_NOT_FOUND")
    db.delete(row)
    db.commit()


def alert_matches_job(alert: JobAlert, job: JobOffer) -> bool:
    hay = " ".join(
        filter(None, [job.title, job.description, job.skills, job.location, job.sector, job.contract_type])
    ).lower()
    if alert.keywords:
        tokens = [t.strip().lower() for t in alert.keywords.replace(",", " ").split() if t.strip()]
        if tokens and not any(tok in hay for tok in tokens):
            return False
    if alert.city and (alert.city or "").lower() not in (job.location or "").lower() and (alert.city or "").lower() not in hay:
        return False
    if alert.province and (alert.province or "").lower() not in hay:
        return False
    if alert.sector and (alert.sector or "").lower() not in (job.sector or "").lower():
        return False
    if alert.contract_type and (alert.contract_type or "").lower() not in (job.contract_type or "").lower():
        return False
    return True
