from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import utcnow
from app.models.identity import uid


class Prospect(Base):
    __tablename__ = "prospects"
    __table_args__ = (
        UniqueConstraint("side", "email", name="uq_prospect_side_email"),
        Index("ix_prospects_side_stage", "side", "stage"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    side: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    stage: Mapped[str] = mapped_column(String(40), default="nouveau", index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(80), default="")
    last_name: Mapped[str] = mapped_column(String(80), default="")
    phone: Mapped[str] = mapped_column(String(40), default="")
    company_name: Mapped[str] = mapped_column(String(160), default="")
    title: Mapped[str] = mapped_column(String(160), default="")
    city: Mapped[str] = mapped_column(String(80), default="")
    sector: Mapped[str] = mapped_column(String(80), default="")
    source: Mapped[str] = mapped_column(String(40), default="prospection")
    source_detail: Mapped[str] = mapped_column(String(240), default="")
    message: Mapped[str] = mapped_column(Text, default="")
    assigned_recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    candidate_id: Mapped[str | None] = mapped_column(ForeignKey("candidates.id"))
    company_id: Mapped[str | None] = mapped_column(ForeignKey("companies.id"))
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class ProspectSend(Base):
    __tablename__ = "prospect_sends"
    __table_args__ = (UniqueConstraint("prospect_id", "template_key", name="uq_prospect_send_template"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    prospect_id: Mapped[str] = mapped_column(ForeignKey("prospects.id", ondelete="CASCADE"), index=True, nullable=False)
    template_key: Mapped[str] = mapped_column(String(80), nullable=False)
    subject: Mapped[str] = mapped_column(String(180), default="")
    body: Mapped[str] = mapped_column(Text, default="")
    to_email: Mapped[str] = mapped_column(String(255), nullable=False)
    email_log_id: Mapped[str | None] = mapped_column(ForeignKey("email_logs.id"))
    attachment_names: Mapped[str] = mapped_column(String(500), default="")
    sent_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
