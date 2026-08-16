"""Tables opérationnelles : messages, entretiens, factures, signatures, file d'e-mails."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0002_ops"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    if table not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    inspector = inspect(bind)
    _add_column_if_missing(inspector, "email_logs", sa.Column("body", sa.Text(), nullable=True))
    _add_column_if_missing(inspector, "email_logs", sa.Column("attempts", sa.Integer(), nullable=True, server_default="0"))
    _add_column_if_missing(inspector, "email_logs", sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True))
    _add_column_if_missing(inspector, "applications", sa.Column("match_score", sa.Integer(), nullable=True))


def downgrade() -> None:
    for table in ("contract_signatures", "payments", "invoices", "interviews", "messages"):
        op.drop_table(table)
