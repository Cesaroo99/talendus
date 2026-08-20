"""Élargit les champs de profil pour plusieurs choix."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0013_multi_choice_fields"
down_revision = "0012_job_offer_traits"
branch_labels = None
depends_on = None


def _widen(table: str, column: str, type_: sa.String) -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if table not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column not in existing:
        return
    op.alter_column(table, column, existing_type=sa.String(length=80), type_=type_, existing_nullable=True)


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    _widen("candidates", "contract_type", sa.String(length=160))
    _widen("candidates", "shift_preference", sa.String(length=160))
    _widen("recruitment_missions", "contract_type", sa.String(length=160))
    _widen("recruitment_missions", "shift", sa.String(length=160))


def downgrade() -> None:
    return
