"""Fusionne les têtes Alembic et rend l’enregistrement des mandats possible."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect, text

revision = "0017_contract_save_schema"
down_revision = ("0016_contract_draft_status", "0010_site_events")
branch_labels = None
depends_on = None


def _run(conn, sql: str) -> None:
    try:
        conn.execute(text(sql))
    except Exception:
        return


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    inspector = inspect(bind)
    if "contracts" not in inspector.get_table_names():
        return
    if bind.dialect.name == "postgresql":
        exists = bind.execute(text("SELECT 1 FROM pg_type WHERE typname = 'contractstatus'")).scalar()
        if exists:
            with op.get_context().autocommit_block():
                _run(bind, "ALTER TYPE contractstatus ADD VALUE IF NOT EXISTS 'DRAFT'")
        _run(bind, "ALTER TABLE contracts ALTER COLUMN status DROP DEFAULT")
        _run(bind, "ALTER TABLE contracts ALTER COLUMN status TYPE VARCHAR(20) USING status::text")
        _run(bind, "ALTER TABLE contracts ALTER COLUMN status SET DEFAULT 'ACTIVE'")
        _run(bind, "ALTER TABLE contracts ALTER COLUMN type TYPE VARCHAR(120)")
        existing = {col["name"] for col in inspect(bind).get_columns("contracts")}
        if "template_key" not in existing:
            op.add_column("contracts", sa.Column("template_key", sa.String(length=40), nullable=True))
        if "reminder_count" not in existing:
            op.add_column(
                "contracts",
                sa.Column("reminder_count", sa.Integer(), nullable=False, server_default="0"),
            )


def downgrade() -> None:
    return
