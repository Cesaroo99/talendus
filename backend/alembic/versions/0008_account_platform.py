"""Alertes emploi, journal de connexion, champs profil candidat et réseaux entreprise."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0008_account_platform"
down_revision = "0007_user_portal"
branch_labels = None
depends_on = None


def _add_column(table: str, column: sa.Column) -> None:
    bind = op.get_bind()
    existing = {c["name"] for c in inspect(bind).get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    _add_column("candidates", sa.Column("address", sa.String(length=255), nullable=True))
    _add_column("candidates", sa.Column("province", sa.String(length=80), nullable=True))
    _add_column("candidates", sa.Column("country", sa.String(length=80), nullable=True))
    _add_column("candidates", sa.Column("birth_date", sa.String(length=16), nullable=True))
    _add_column("companies", sa.Column("linkedin_url", sa.String(length=255), nullable=True))
    _add_column("companies", sa.Column("facebook_url", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_table("login_events")
    op.drop_table("job_alerts")
    for table, col in (
        ("candidates", "address"),
        ("candidates", "province"),
        ("candidates", "country"),
        ("candidates", "birth_date"),
        ("companies", "linkedin_url"),
        ("companies", "facebook_url"),
    ):
        bind = op.get_bind()
        existing = {c["name"] for c in inspect(bind).get_columns(table)}
        if col in existing:
            op.drop_column(table, col)
