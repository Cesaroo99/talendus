"""Événements anonymes du site (visites et interactions)."""

from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0010_site_events"
down_revision = "0009_hiring_requests"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    tables = set(inspect(bind).get_table_names())
    if "site_events" in tables:
        op.drop_table("site_events")
