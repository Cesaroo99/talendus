"""Suivi du mandat : envoi, ouverture, double signature."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0015_mandate_lifecycle"
down_revision = "0014_work_status_occupations"
branch_labels = None
depends_on = None


def _add_column(table: str, column: sa.Column) -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if table not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    _add_column("contracts", sa.Column("template_key", sa.String(length=40), nullable=True))
    _add_column("contracts", sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True))
    _add_column("contracts", sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True))
    _add_column("contracts", sa.Column("talendus_signed_at", sa.DateTime(timezone=True), nullable=True))
    _add_column("contracts", sa.Column("client_signed_at", sa.DateTime(timezone=True), nullable=True))
    _add_column("contracts", sa.Column("reminder_count", sa.Integer(), nullable=False, server_default="0"))
    _add_column("contracts", sa.Column("last_reminded_at", sa.DateTime(timezone=True), nullable=True))
    _add_column("contract_signatures", sa.Column("party", sa.String(length=20), nullable=False, server_default="CLIENT"))
    _add_column("contract_signatures", sa.Column("signer_role", sa.String(length=20), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    for table, col in (
        ("contracts", "template_key"),
        ("contracts", "sent_at"),
        ("contracts", "opened_at"),
        ("contracts", "talendus_signed_at"),
        ("contracts", "client_signed_at"),
        ("contracts", "reminder_count"),
        ("contracts", "last_reminded_at"),
        ("contract_signatures", "party"),
        ("contract_signatures", "signer_role"),
    ):
        if table in inspector.get_table_names() and col in {c["name"] for c in inspector.get_columns(table)}:
            op.drop_column(table, col)
