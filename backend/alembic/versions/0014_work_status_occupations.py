"""Statut d'autorisation de travail, parrainage et titres plus longs."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0014_work_status_occupations"
down_revision = "0013_multi_choice_fields"
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


def _widen(table: str, column: str, type_: sa.String) -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if table not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column not in existing:
        return
    op.alter_column(table, column, existing_type=sa.String(length=120), type_=type_, existing_nullable=True)


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    _add_column("candidates", sa.Column("work_status", sa.String(length=40), nullable=True))
    _add_column("job_offers", sa.Column("work_authorization", sa.String(length=40), nullable=True))
    _add_column("job_offers", sa.Column("can_sponsor", sa.Boolean(), nullable=False, server_default=sa.false()))
    _add_column("recruitment_missions", sa.Column("work_authorization", sa.String(length=40), nullable=True))
    _add_column("recruitment_missions", sa.Column("can_sponsor", sa.Boolean(), nullable=False, server_default=sa.false()))
    _widen("candidates", "title", sa.String(length=180))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    for table, col in (
        ("candidates", "work_status"),
        ("job_offers", "work_authorization"),
        ("job_offers", "can_sponsor"),
        ("recruitment_missions", "work_authorization"),
        ("recruitment_missions", "can_sponsor"),
    ):
        if table in inspector.get_table_names() and col in {c["name"] for c in inspector.get_columns(table)}:
            op.drop_column(table, col)
