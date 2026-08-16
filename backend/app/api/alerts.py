from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.schemas import JobAlertIn, JobAlertPatchIn
from app.services import alerts as alerts_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def list_alerts(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.CANDIDATE))):
    return ok(alerts_service.list_alerts(db, user))


@router.post("")
def create_alert(
    payload: JobAlertIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok(alerts_service.create_alert(db, user, payload))


@router.patch("/{alert_id}")
def update_alert(
    alert_id: str,
    payload: JobAlertPatchIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    return ok(alerts_service.update_alert(db, user, alert_id, payload))


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.CANDIDATE)),
):
    alerts_service.delete_alert(db, user, alert_id)
    return ok(message="Alerte supprimée.")
