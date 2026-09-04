"""Pipelines prospects candidats et employeurs."""

import sqlalchemy as sa
from alembic import op

revision = "0019_prospects"
down_revision = "0018_interview_call_perms"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if "prospects" not in tables:
        op.create_table(
            "prospects",
            sa.Column("id", sa.String(length=36), primary_key=True),
            sa.Column("side", sa.String(length=20), nullable=False),
            sa.Column("stage", sa.String(length=40), server_default="nouveau"),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("first_name", sa.String(length=80), server_default=""),
            sa.Column("last_name", sa.String(length=80), server_default=""),
            sa.Column("phone", sa.String(length=40), server_default=""),
            sa.Column("company_name", sa.String(length=160), server_default=""),
            sa.Column("title", sa.String(length=160), server_default=""),
            sa.Column("city", sa.String(length=80), server_default=""),
            sa.Column("sector", sa.String(length=80), server_default=""),
            sa.Column("source", sa.String(length=40), server_default="prospection"),
            sa.Column("source_detail", sa.String(length=240), server_default=""),
            sa.Column("message", sa.Text(), server_default=""),
            sa.Column("assigned_recruiter_id", sa.String(length=36), nullable=True),
            sa.Column("user_id", sa.String(length=36), nullable=True),
            sa.Column("candidate_id", sa.String(length=36), nullable=True),
            sa.Column("company_id", sa.String(length=36), nullable=True),
            sa.Column("last_contacted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True)),
            sa.Column("updated_at", sa.DateTime(timezone=True)),
        )
        op.create_index("ix_prospects_side", "prospects", ["side"])
        op.create_index("ix_prospects_stage", "prospects", ["stage"])
        op.create_index("ix_prospects_email", "prospects", ["email"])
        op.create_index("ix_prospects_side_stage", "prospects", ["side", "stage"])
        op.create_index("ix_prospects_created_at", "prospects", ["created_at"])
        op.create_unique_constraint("uq_prospect_side_email", "prospects", ["side", "email"])
    if "prospect_sends" not in tables:
        op.create_table(
            "prospect_sends",
            sa.Column("id", sa.String(length=36), primary_key=True),
            sa.Column("prospect_id", sa.String(length=36), nullable=False),
            sa.Column("template_key", sa.String(length=80), nullable=False),
            sa.Column("subject", sa.String(length=180), server_default=""),
            sa.Column("body", sa.Text(), server_default=""),
            sa.Column("to_email", sa.String(length=255), nullable=False),
            sa.Column("email_log_id", sa.String(length=36), nullable=True),
            sa.Column("attachment_names", sa.String(length=500), server_default=""),
            sa.Column("sent_by_id", sa.String(length=36), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True)),
        )
        op.create_index("ix_prospect_sends_prospect_id", "prospect_sends", ["prospect_id"])
        op.create_unique_constraint("uq_prospect_send_template", "prospect_sends", ["prospect_id", "template_key"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if "prospect_sends" in tables:
        op.drop_table("prospect_sends")
    if "prospects" in tables:
        op.drop_table("prospects")
