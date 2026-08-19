"""Quarts, horaires et autres caractéristiques d'offre."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0012_job_offer_traits"
down_revision = "0011_call_signals"
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
    _add_column("job_offers", sa.Column("schedule", sa.String(length=80), nullable=True))
    _add_column("job_offers", sa.Column("work_mode", sa.String(length=80), nullable=True))
    _add_column("job_offers", sa.Column("languages", sa.String(length=160), nullable=True))
    _add_column("job_offers", sa.Column("overtime", sa.String(length=80), nullable=True))
    _add_column("job_offers", sa.Column("driver_license", sa.String(length=80), nullable=True))
    _add_column("job_offers", sa.Column("unionized", sa.String(length=40), nullable=True))
    _add_column("job_offers", sa.Column("travel", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("shift", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("schedule", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("work_mode", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("overtime", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("driver_license", sa.String(length=80), nullable=True))
    _add_column("recruitment_missions", sa.Column("unionized", sa.String(length=40), nullable=True))
    _add_column("recruitment_missions", sa.Column("travel", sa.String(length=80), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    for table, col in (
        ("job_offers", "schedule"),
        ("job_offers", "work_mode"),
        ("job_offers", "languages"),
        ("job_offers", "overtime"),
        ("job_offers", "driver_license"),
        ("job_offers", "unionized"),
        ("job_offers", "travel"),
        ("recruitment_missions", "shift"),
        ("recruitment_missions", "schedule"),
        ("recruitment_missions", "work_mode"),
        ("recruitment_missions", "overtime"),
        ("recruitment_missions", "driver_license"),
        ("recruitment_missions", "unionized"),
        ("recruitment_missions", "travel"),
    ):
        if table in inspector.get_table_names() and col in {c["name"] for c in inspector.get_columns(table)}:
            op.drop_column(table, col)
