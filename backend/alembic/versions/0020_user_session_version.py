"""Version de session JWT pour révoquer les access tokens."""

import sqlalchemy as sa
from alembic import op

revision = "0020_user_session_version"
down_revision = "0019_prospects"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "users" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("users")}
    if "session_version" not in existing:
        op.add_column(
            "users",
            sa.Column("session_version", sa.Integer(), nullable=False, server_default="0"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "users" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("users")}
    if "session_version" in existing:
        op.drop_column("users", "session_version")
