"""Demandes de recrutement entreprise et statuts de mandat étendus."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0009_hiring_requests"
down_revision = "0008_account_platform"
branch_labels = None
depends_on = None

NEW_ENUM_VALUES = {
    "missionstatus": (
        "REQUEST_SUBMITTED",
        "UNDER_REVIEW",
        "CLIENT_CONTACTED",
        "NEEDS_CONFIRMED",
        "JOB_BEING_PREPARED",
        "CLIENT_VALIDATION",
        "JOB_PUBLISHED",
        "SOURCING",
        "SCREENING",
        "INTERVIEWS",
        "SHORTLIST",
        "CLIENT_REVIEW",
        "HIRING",
        "CLOSED",
    ),
    "notificationtype": ("HIRING_REQUEST",),
}

NEW_COLUMNS = {
    "recruitment_missions": [
        sa.Column("location", sa.String(length=80), nullable=True),
        sa.Column("sector", sa.String(length=80), nullable=True),
        sa.Column("contract_type", sa.String(length=40), nullable=True),
        sa.Column("experience_level", sa.String(length=80), nullable=True),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("qualifications", sa.Text(), nullable=True),
        sa.Column("languages", sa.String(length=160), nullable=True),
        sa.Column("salary_display", sa.String(length=80), nullable=True),
        sa.Column("contact_name", sa.String(length=120), nullable=True),
        sa.Column("contact_role", sa.String(length=120), nullable=True),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("contact_phone", sa.String(length=40), nullable=True),
        sa.Column("company_size", sa.String(length=40), nullable=True),
        sa.Column("extra_criteria", sa.Text(), nullable=True),
    ],
}


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    if table not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def _pg_add_enum_values(bind) -> None:
    for type_name, values in NEW_ENUM_VALUES.items():
        exists = bind.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = :n"), {"n": type_name}).scalar()
        if not exists:
            continue
        for value in values:
            bind.execute(sa.text(f"ALTER TYPE {type_name} ADD VALUE IF NOT EXISTS '{value}'"))


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        with op.get_context().autocommit_block():
            _pg_add_enum_values(bind)
    Base.metadata.create_all(bind=bind)
    inspector = inspect(bind)
    for table, columns in NEW_COLUMNS.items():
        for column in columns:
            _add_column_if_missing(inspector, table, column)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "recruitment_missions" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("recruitment_missions")}
    for column in reversed(NEW_COLUMNS["recruitment_missions"]):
        if column.name in existing:
            op.drop_column("recruitment_missions", column.name)
