"""Suivi SMTP et ouverture des courriels."""

import sqlalchemy as sa
from alembic import op

revision = "0020_email_tracking"
down_revision = "0019_prospects"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "email_logs" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("email_logs")}
    if "tracking_token" not in existing:
        op.add_column("email_logs", sa.Column("tracking_token", sa.String(length=64), nullable=True))
    if "message_id" not in existing:
        op.add_column("email_logs", sa.Column("message_id", sa.String(length=180), nullable=True))
    if "opened_at" not in existing:
        op.add_column("email_logs", sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True))
    if "open_count" not in existing:
        op.add_column("email_logs", sa.Column("open_count", sa.Integer(), server_default="0"))
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_email_logs_tracking_token ON email_logs (tracking_token)")


def downgrade() -> None:
    pass
