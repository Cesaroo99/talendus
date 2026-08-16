"""Journal des appels d'intégration — jamais de secrets ni de corps de requête."""

from __future__ import annotations

import logging

from app.models.enums import utcnow

logger = logging.getLogger("talendus.integrations")

_memory: list[dict] = []


def recent_calls(limit: int = 50) -> list[dict]:
    return list(_memory[-limit:])


def clear_memory() -> None:
    _memory.clear()


def record_call(
    *,
    provider: str,
    operation: str,
    success: bool,
    status_code: int | None = None,
    duration_ms: int | None = None,
    request_id: str | None = None,
    error_code: str | None = None,
    persist: bool = False,
) -> dict:
    row = {
        "provider": provider,
        "operation": operation,
        "success": success,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "request_id": request_id,
        "error_code": error_code,
        "created_at": utcnow().isoformat(),
    }
    _memory.append(row)
    if len(_memory) > 500:
        del _memory[: len(_memory) - 500]
    logger.info(
        "integration provider=%s op=%s success=%s status=%s duration_ms=%s request_id=%s error=%s",
        provider,
        operation,
        success,
        status_code,
        duration_ms,
        request_id,
        error_code,
    )
    if persist:
        _persist(row)
    return row


def persist_call(**kwargs) -> dict:
    return record_call(persist=True, **kwargs)


def _persist(row: dict) -> None:
    try:
        from app.database import SessionLocal
        from app.models.integrations import IntegrationCall

        db = SessionLocal()
        try:
            db.add(
                IntegrationCall(
                    provider=row["provider"],
                    operation=row["operation"],
                    success=row["success"],
                    status_code=row["status_code"],
                    duration_ms=row["duration_ms"],
                    request_id=row["request_id"],
                    error_code=row["error_code"],
                )
            )
            db.commit()
        finally:
            db.close()
    except Exception:
        logger.exception("integration call persist failed provider=%s", row.get("provider"))
