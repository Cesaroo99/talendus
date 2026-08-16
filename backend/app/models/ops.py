from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import InterviewStatus, InterviewType, InvoiceStatus, PaymentMethod, utcnow
from app.models.identity import uid


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    sender_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    recipient_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    application_id: Mapped[str | None] = mapped_column(ForeignKey("applications.id"))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    application_id: Mapped[str | None] = mapped_column(ForeignKey("applications.id"))
    job_id: Mapped[str | None] = mapped_column(ForeignKey("job_offers.id"))
    company_id: Mapped[str | None] = mapped_column(ForeignKey("companies.id"))
    recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    location: Mapped[str | None] = mapped_column(String(160))
    type: Mapped[InterviewType] = mapped_column(Enum(InterviewType), default=InterviewType.TALENDUS)
    status: Mapped[InterviewStatus] = mapped_column(Enum(InterviewStatus), default=InterviewStatus.SCHEDULED, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    candidate = relationship("Candidate")
    application = relationship("Application")
    job = relationship("JobOffer")
    company = relationship("Company")
    recruiter = relationship("User", foreign_keys=[recruiter_id])


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    mission_id: Mapped[str | None] = mapped_column(ForeignKey("recruitment_missions.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="CAD")
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, index=True)
    issued_at: Mapped[str | None] = mapped_column(String(16))
    due_date: Mapped[str | None] = mapped_column(String(16))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    company = relationship("Company")
    mission = relationship("RecruitmentMission")
    payments: Mapped[list["Payment"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    invoice_id: Mapped[str] = mapped_column(ForeignKey("invoices.id"), index=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), default=PaymentMethod.TRANSFER)
    paid_at: Mapped[str | None] = mapped_column(String(16))
    reference: Mapped[str | None] = mapped_column(String(80))
    recorded_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    invoice: Mapped[Invoice] = relationship(back_populates="payments")


class ContractSignature(Base):
    __tablename__ = "contract_signatures"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    contract_id: Mapped[str] = mapped_column(ForeignKey("contracts.id"), index=True, nullable=False)
    signer_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    signer_name: Mapped[str] = mapped_column(String(160), nullable=False)
    signer_email: Mapped[str | None] = mapped_column(String(255))
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    ip_address: Mapped[str | None] = mapped_column(String(64))
    document_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    document_name: Mapped[str | None] = mapped_column(String(255))
    accepted: Mapped[bool] = mapped_column(Boolean, default=True)

    contract = relationship("Contract", back_populates="signatures")
