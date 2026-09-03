"""Le statut DRAFT des mandats existe dans Postgres."""

import sqlalchemy as sa
from alembic import op

revision = "0016_contract_draft_status"
down_revision = "0015_mandate_lifecycle"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    exists = bind.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'contractstatus'")).scalar()
    if not exists:
        return
    with op.get_context().autocommit_block():
        bind.execute(sa.text("ALTER TYPE contractstatus ADD VALUE IF NOT EXISTS 'DRAFT'"))


def downgrade() -> None:
    return
