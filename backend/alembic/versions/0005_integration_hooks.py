"""Colonnes d'accroche intégrations : géoloc, PayPal, rappels, e-sign."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "0005_integration_hooks"
down_revision = "0004_integrations"
branch_labels = None
depends_on = None

NEW_COLUMNS = {
    "companies": [
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lng", sa.Float(), nullable=True),
        sa.Column("place_id", sa.String(128), nullable=True),
    ],
    "job_offers": [
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lng", sa.Float(), nullable=True),
        sa.Column("place_id", sa.String(128), nullable=True),
    ],
    "invoices": [
        sa.Column("paypal_order_id", sa.String(80), nullable=True),
        sa.Column("paypal_capture_id", sa.String(80), nullable=True),
    ],
    "interviews": [
        sa.Column("reminder_sent_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "contracts": [
        sa.Column("esign_envelope_id", sa.String(80), nullable=True),
        sa.Column("esign_status", sa.String(32), nullable=True),
    ],
}


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    if table not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        exists = bind.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'invoicestatus'")).scalar()
        if exists:
            with op.get_context().autocommit_block():
                bind.execute(sa.text("ALTER TYPE invoicestatus ADD VALUE IF NOT EXISTS 'REFUNDED'"))
    inspector = inspect(bind)
    for table, columns in NEW_COLUMNS.items():
        for column in columns:
            _add_column_if_missing(inspector, table, column)


def downgrade() -> None:
    for table, columns in NEW_COLUMNS.items():
        for column in columns:
            op.drop_column(table, column.name)
