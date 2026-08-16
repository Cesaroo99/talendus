import json
import logging

from sqlalchemy.orm import Session

from app.models import AuditLog, User

logger = logging.getLogger("talendus.audit")


def audit(
    db: Session,
    action: str,
    actor: User | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    ip: str | None = None,
    metadata: dict | None = None,
) -> None:
    row = AuditLog(
        actor_id=actor.id if actor else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip,
        metadata_json=json.dumps(metadata, ensure_ascii=False) if metadata else None,
    )
    db.add(row)
    logger.info("audit %s actor=%s entity=%s:%s", action, getattr(actor, "id", None), entity_type, entity_id)
