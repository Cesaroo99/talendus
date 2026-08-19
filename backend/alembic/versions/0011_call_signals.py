"""Signaux d'appel audio/vidéo gérés dans Talendus."""

from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0011_call_signals"
down_revision = "0010_push_subscriptions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    tables = inspector.get_table_names()
    if "call_signals" in tables:
        op.drop_table("call_signals")
    if "call_peers" in tables:
        op.drop_table("call_peers")
