from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Index, Integer, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import CompanyMemberRole, CompanyStatus, ContractStatus, MissionStatus, utcnow
from app.models.identity import uid


mission_jobs = Table(
    "mission_jobs",
    Base.metadata,
    Column("mission_id", ForeignKey("recruitment_missions.id", ondelete="CASCADE"), primary_key=True),
    Column("job_id", ForeignKey("job_offers.id", ondelete="CASCADE"), primary_key=True),
)


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("ix_companies_sector", "sector"),
        Index("ix_companies_city", "city"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    legal_name: Mapped[str | None] = mapped_column(String(160))
    trade_name: Mapped[str | None] = mapped_column(String(160))
    logo_path: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    sector: Mapped[str | None] = mapped_column(String(80))
    city: Mapped[str | None] = mapped_column(String(80))
    address: Mapped[str | None] = mapped_column(String(255))
    province: Mapped[str | None] = mapped_column(String(80), default="Québec")
    country: Mapped[str | None] = mapped_column(String(80), default="Canada")
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)
    place_id: Mapped[str | None] = mapped_column(String(128))
    contact_name: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(40))
    website: Mapped[str | None] = mapped_column(String(160))
    linkedin_url: Mapped[str | None] = mapped_column(String(255))
    facebook_url: Mapped[str | None] = mapped_column(String(255))
    employees: Mapped[int | None] = mapped_column(Integer)
    size_label: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus), default=CompanyStatus.ACTIVE, index=True)
    owner_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    assigned_recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    owner = relationship("User", back_populates="company", foreign_keys=[owner_user_id])
    jobs: Mapped[list["JobOffer"]] = relationship(back_populates="company")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="company")
    missions: Mapped[list["RecruitmentMission"]] = relationship(back_populates="company")
    memberships: Mapped[list["CompanyMembership"]] = relationship(back_populates="company", cascade="all, delete-orphan")


class CompanyMembership(Base):
    __tablename__ = "company_memberships"
    __table_args__ = (UniqueConstraint("company_id", "user_id", name="uq_company_membership"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    member_role: Mapped[CompanyMemberRole] = mapped_column(Enum(CompanyMemberRole), default=CompanyMemberRole.MEMBER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    company: Mapped[Company] = relationship(back_populates="memberships")
    user = relationship("User", back_populates="company_memberships")


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(80), default="Succès")
    start_date: Mapped[str | None] = mapped_column(String(16))
    end_date: Mapped[str | None] = mapped_column(String(16))
    commission_percent: Mapped[int | None] = mapped_column(Integer)
    terms: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ContractStatus] = mapped_column(Enum(ContractStatus), default=ContractStatus.ACTIVE)
    document_name: Mapped[str | None] = mapped_column(String(255))
    document_path: Mapped[str | None] = mapped_column(String(255))
    esign_envelope_id: Mapped[str | None] = mapped_column(String(80))
    esign_status: Mapped[str | None] = mapped_column(String(32))
    recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    notes: Mapped[str | None] = mapped_column(Text)
    template_key: Mapped[str | None] = mapped_column(String(40))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    talendus_signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    client_signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reminder_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_reminded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    company: Mapped[Company] = relationship(back_populates="contracts")
    signatures: Mapped[list["ContractSignature"]] = relationship(
        back_populates="contract",
        order_by="ContractSignature.signed_at",
    )


class RecruitmentMission(Base):
    __tablename__ = "recruitment_missions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    job_id: Mapped[str | None] = mapped_column(ForeignKey("job_offers.id"))
    recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), default=MissionStatus.REQUEST_SUBMITTED)
    value: Mapped[int | None] = mapped_column(Integer)
    commission: Mapped[int | None] = mapped_column(Integer)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[str | None] = mapped_column(String(16))
    due_date: Mapped[str | None] = mapped_column(String(16))
    notes: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(80))
    sector: Mapped[str | None] = mapped_column(String(80))
    contract_type: Mapped[str | None] = mapped_column(String(160))
    experience_level: Mapped[str | None] = mapped_column(String(80))
    skills: Mapped[str | None] = mapped_column(Text)
    qualifications: Mapped[str | None] = mapped_column(Text)
    languages: Mapped[str | None] = mapped_column(String(160))
    shift: Mapped[str | None] = mapped_column(String(160))
    schedule: Mapped[str | None] = mapped_column(String(80))
    work_mode: Mapped[str | None] = mapped_column(String(80))
    overtime: Mapped[str | None] = mapped_column(String(80))
    driver_license: Mapped[str | None] = mapped_column(String(80))
    unionized: Mapped[str | None] = mapped_column(String(40))
    travel: Mapped[str | None] = mapped_column(String(80))
    work_authorization: Mapped[str | None] = mapped_column(String(40))
    can_sponsor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    salary_display: Mapped[str | None] = mapped_column(String(80))
    contact_name: Mapped[str | None] = mapped_column(String(120))
    contact_role: Mapped[str | None] = mapped_column(String(120))
    contact_email: Mapped[str | None] = mapped_column(String(255))
    contact_phone: Mapped[str | None] = mapped_column(String(40))
    company_size: Mapped[str | None] = mapped_column(String(40))
    extra_criteria: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    company: Mapped[Company] = relationship(back_populates="missions")
    job = relationship("JobOffer", back_populates="missions", foreign_keys=[job_id])
    linked_jobs: Mapped[list] = relationship("JobOffer", secondary=mission_jobs, back_populates="linked_missions")
