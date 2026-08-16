"""Schéma complet Talendus — profils, memberships, messagerie, facturation, paramètres."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

from app.database import Base
from app import models  # noqa: F401

revision = "0003_platform"
down_revision = "0002_ops"
branch_labels = None
depends_on = None


NEW_ENUM_VALUES = {
    "userrole": ("SUPER_ADMIN",),
    "jobstatus": ("PENDING_VALIDATION",),
    "applicationstatus": ("RECEIVED", "SECOND_INTERVIEW", "OFFER_SENT"),
    "notificationtype": ("DOCUMENT_ADDED", "SYSTEM"),
}

NEW_COLUMNS = {
    "users": [
        sa.Column("account_status", sa.String(32), nullable=True, server_default="ACTIVE"),
    ],
    "candidates": [
        sa.Column("education_level", sa.String(80), nullable=True),
        sa.Column("job_search_status", sa.String(32), nullable=True, server_default="ACTIVE"),
        sa.Column("work_preferences", sa.Text(), nullable=True),
    ],
    "resumes": [
        sa.Column("storage_url", sa.String(500), nullable=True),
        sa.Column("parse_status", sa.String(32), nullable=True),
        sa.Column("parse_json", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "companies": [
        sa.Column("legal_name", sa.String(160), nullable=True),
        sa.Column("trade_name", sa.String(160), nullable=True),
        sa.Column("logo_path", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("province", sa.String(80), nullable=True, server_default="Québec"),
        sa.Column("country", sa.String(80), nullable=True, server_default="Canada"),
        sa.Column("size_label", sa.String(40), nullable=True),
    ],
    "contracts": [
        sa.Column("document_path", sa.String(255), nullable=True),
        sa.Column("recruiter_id", sa.String(36), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "recruitment_missions": [
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "job_offers": [
        sa.Column("currency", sa.String(8), nullable=True, server_default="CAD"),
        sa.Column("openings", sa.Integer(), nullable=True, server_default="1"),
    ],
    "applications": [
        sa.Column("source", sa.String(40), nullable=True, server_default="site"),
        sa.Column("staff_notes", sa.Text(), nullable=True),
    ],
    "messages": [
        sa.Column("conversation_id", sa.String(36), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "invoices": [
        sa.Column("amount_ht", sa.Integer(), nullable=True),
        sa.Column("tax_amount", sa.Integer(), nullable=True),
        sa.Column("amount_total", sa.Integer(), nullable=True),
        sa.Column("tax_rate_bp", sa.Integer(), nullable=True),
        sa.Column("paid_at", sa.String(16), nullable=True),
        sa.Column("stripe_payment_intent_id", sa.String(80), nullable=True),
        sa.Column("client_user_id", sa.String(36), nullable=True),
    ],
    "notifications": [
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    ],
    "audit_logs": [
        sa.Column("old_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
    ],
}

NEW_INDEXES = [
    ("ix_users_first_name", "users", ["first_name"]),
    ("ix_users_last_name", "users", ["last_name"]),
    ("ix_candidates_city", "candidates", ["city"]),
    ("ix_candidates_sector", "candidates", ["sector"]),
    ("ix_candidates_search_status", "candidates", ["job_search_status"]),
    ("ix_companies_sector", "companies", ["sector"]),
    ("ix_companies_city", "companies", ["city"]),
    ("ix_companies_status", "companies", ["status"]),
    ("ix_jobs_status_published", "job_offers", ["status", "published_at"]),
    ("ix_jobs_location_sector", "job_offers", ["location", "sector"]),
    ("ix_applications_status_created", "applications", ["status", "created_at"]),
    ("ix_messages_conversation_created", "messages", ["conversation_id", "created_at"]),
]


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    if table not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def _create_index_if_missing(inspector, name: str, table: str, columns: list[str]) -> None:
    if table not in inspector.get_table_names():
        return
    existing = {ix["name"] for ix in inspector.get_indexes(table)}
    if name not in existing:
        op.create_index(name, table, columns)


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
    inspector = inspect(bind)
    for name, table, columns in NEW_INDEXES:
        _create_index_if_missing(inspector, name, table, columns)


def downgrade() -> None:
    for table in (
        "system_settings",
        "user_preferences",
        "invoice_lines",
        "message_attachments",
        "conversation_participants",
        "conversations",
        "mission_jobs",
        "company_memberships",
    ):
        op.drop_table(table)
