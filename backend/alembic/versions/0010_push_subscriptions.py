"""Abonnements Web Push pour la barre de notifications du téléphone."""

from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0010_push_subscriptions"
down_revision = "0009_hiring_requests"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "push_subscriptions" in inspector.get_table_names():
        op.drop_table("push_subscriptions")
