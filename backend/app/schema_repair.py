"""Répare le schéma des mandats si Alembic n’a pas pu finir (têtes multiples, enum PG)."""

from __future__ import annotations

import logging

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

logger = logging.getLogger("talendus.schema")

_DONE = False


def _run(conn, sql: str) -> None:
    try:
        conn.execute(text(sql))
    except Exception as exc:  # noqa: BLE001 — chaque correctif est optionnel
        logger.info("schema skip: %s (%s)", sql.split("\n")[0][:80], exc)


def ensure_interviews_schema(engine: Engine) -> None:
    """Ajoute les droits d’appel (lancer / rejoindre) sur interviews. Idempotent."""
    try:
        inspector = inspect(engine)
        if "interviews" not in inspector.get_table_names():
            return
        existing = {col["name"] for col in inspector.get_columns("interviews")}
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            if "candidate_can_start" not in existing:
                _run(conn, "ALTER TABLE interviews ADD COLUMN candidate_can_start BOOLEAN NOT NULL DEFAULT FALSE")
            if "call_opened_at" not in existing:
                _run(conn, "ALTER TABLE interviews ADD COLUMN call_opened_at TIMESTAMPTZ")
    except Exception:
        logger.exception("Réparation du schéma entretiens incomplète")


def ensure_email_logs_schema(engine: Engine) -> None:
    """Suivi de livraison / ouverture sur email_logs. Idempotent."""
    try:
        inspector = inspect(engine)
        if "email_logs" not in inspector.get_table_names():
            return
        existing = {col["name"] for col in inspector.get_columns("email_logs")}
        ts = "TIMESTAMPTZ" if engine.dialect.name == "postgresql" else "DATETIME"
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            if "tracking_token" not in existing:
                _run(conn, "ALTER TABLE email_logs ADD COLUMN tracking_token VARCHAR(64)")
            if "message_id" not in existing:
                _run(conn, "ALTER TABLE email_logs ADD COLUMN message_id VARCHAR(180)")
            if "opened_at" not in existing:
                _run(conn, f"ALTER TABLE email_logs ADD COLUMN opened_at {ts}")
            if "open_count" not in existing:
                _run(conn, "ALTER TABLE email_logs ADD COLUMN open_count INTEGER DEFAULT 0")
            _run(conn, "CREATE UNIQUE INDEX IF NOT EXISTS ix_email_logs_tracking_token ON email_logs (tracking_token)")
    except Exception:
        logger.exception("Réparation du schéma email_logs incomplète")


def ensure_contracts_schema(engine: Engine) -> None:
    """Ajoute DRAFT, élargit le type, stocke le statut en texte. Idempotent."""
    global _DONE
    if _DONE:
        return
    if engine.dialect.name != "postgresql":
        _DONE = True
        return
    try:
        inspector = inspect(engine)
        if "contracts" not in inspector.get_table_names():
            _DONE = True
            return
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            has_enum = conn.execute(text("SELECT 1 FROM pg_type WHERE typname = 'contractstatus'")).scalar()
            if has_enum:
                _run(conn, "ALTER TYPE contractstatus ADD VALUE IF NOT EXISTS 'DRAFT'")
            _run(conn, "ALTER TABLE contracts ALTER COLUMN status DROP DEFAULT")
            _run(
                conn,
                "ALTER TABLE contracts ALTER COLUMN status TYPE VARCHAR(20) USING status::text",
            )
            _run(conn, "ALTER TABLE contracts ALTER COLUMN status SET DEFAULT 'ACTIVE'")
            _run(conn, "ALTER TABLE contracts ALTER COLUMN type TYPE VARCHAR(120)")
            existing = {col["name"] for col in inspect(engine).get_columns("contracts")}
            if "template_key" not in existing:
                _run(conn, "ALTER TABLE contracts ADD COLUMN template_key VARCHAR(40)")
            if "reminder_count" not in existing:
                _run(conn, "ALTER TABLE contracts ADD COLUMN reminder_count INTEGER NOT NULL DEFAULT 0")
        _DONE = True
    except Exception:
        logger.exception("Réparation du schéma contrats incomplète")
