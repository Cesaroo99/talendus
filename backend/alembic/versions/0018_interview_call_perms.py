"""Droits d’appel : le candidat peut lancer ou seulement rejoindre."""

import sqlalchemy as sa
from alembic import op

revision = "0018_interview_call_perms"
down_revision = "0017_contract_save_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "interviews" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("interviews")}
    if "candidate_can_start" not in existing:
        op.add_column(
            "interviews",
            sa.Column("candidate_can_start", sa.Boolean(), nullable=False, server_default=sa.false()),
        )
    if "call_opened_at" not in existing:
        op.add_column("interviews", sa.Column("call_opened_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "interviews" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("interviews")}
    if "call_opened_at" in existing:
        op.drop_column("interviews", "call_opened_at")
    if "candidate_can_start" in existing:
        op.drop_column("interviews", "candidate_can_start")
