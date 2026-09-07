"""Tâches internes périodiques : factures en retard, rappels d'entretien."""

from __future__ import annotations

import logging
import threading
import time

from app.database import SessionLocal

logger = logging.getLogger("talendus.ops")

_lock = threading.Lock()
_started = False


def run_ops_tick() -> dict:
    from app.services import invoices as invoices_service
    from app.services.interviews import dispatch_due_reminders

    db = SessionLocal()
    result = {"overdue": 0, "reminders": {}}
    try:
        result["overdue"] = invoices_service.mark_overdue(db)
        result["reminders"] = dispatch_due_reminders(db)
        from app.services.email import flush_outbound_queue

        result["mail"] = flush_outbound_queue(db)
        db.commit()
        logger.info("ops tick overdue=%s reminders=%s mail=%s", result["overdue"], result["reminders"], result["mail"])
    except Exception:
        logger.exception("ops tick failed")
        db.rollback()
        raise
    finally:
        db.close()
    return result


def _loop() -> None:
    time.sleep(25)
    while True:
        try:
            run_ops_tick()
        except Exception:
            logger.exception("ops worker cycle")
        time.sleep(900)


def start_ops_worker() -> None:
    global _started
    with _lock:
        if _started:
            return
        thread = threading.Thread(target=_loop, name="talendus-ops", daemon=True)
        thread.start()
        _started = True
        logger.info("ops worker started")
