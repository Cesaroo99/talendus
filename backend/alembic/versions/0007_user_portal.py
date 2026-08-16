"""Tables portail utilisateur : offres sauvegardées, documents, colonnes complémentaires."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0007_user_portal"
down_revision = "0006_seo_cms"
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
    _add_column("notifications", sa.Column("channel", sa.String(length=20), nullable=True, server_default="in_app"))
    _add_column("job_offers", sa.Column("start_date", sa.String(length=16), nullable=True))
    _add_column("interviews", sa.Column("meeting_url", sa.String(length=500), nullable=True))
    _add_column("interviews", sa.Column("meeting_provider", sa.String(length=40), nullable=True))
    _add_column("user_preferences", sa.Column("notify_sms", sa.Boolean(), nullable=True, server_default=sa.false()))
    _add_column("user_preferences", sa.Column("notify_whatsapp", sa.Boolean(), nullable=True, server_default=sa.false()))
    _add_column("user_preferences", sa.Column("notify_push", sa.Boolean(), nullable=True, server_default=sa.false()))
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'DOCUMENT_MISSING'")
        op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'PROFILE_INCOMPLETE'")
        op.execute("ALTER TYPE companymemberrole ADD VALUE IF NOT EXISTS 'ADMIN'")
        op.execute("ALTER TYPE companymemberrole ADD VALUE IF NOT EXISTS 'HR'")
        op.execute("ALTER TYPE companymemberrole ADD VALUE IF NOT EXISTS 'RECRUITER'")


def downgrade() -> None:
    op.drop_table("portal_documents")
    op.drop_table("saved_jobs")
