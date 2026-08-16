"""Tables d'intégrations : offres externes, webhooks, journal d'appels."""

from alembic import op

from app.database import Base
from app import models  # noqa: F401

revision = "0004_integrations"
down_revision = "0003_platform"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    op.drop_table("integration_calls")
    op.drop_table("webhook_events")
    op.drop_table("external_jobs")
