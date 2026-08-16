from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import CompanyStatus, ContractStatus, MissionStatus, utcnow
from app.models.identity import uid


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    sector: Mapped[str | None] = mapped_column(String(80))
    city: Mapped[str | None] = mapped_column(String(80))
    contact_name: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(40))
    website: Mapped[str | None] = mapped_column(String(160))
    employees: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus), default=CompanyStatus.ACTIVE)
    owner_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    assigned_recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    owner = relationship("User", back_populates="company", foreign_keys=[owner_user_id])
    jobs: Mapped[list["JobOffer"]] = relationship(back_populates="company")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="company")
    missions: Mapped[list["RecruitmentMission"]] = relationship(back_populates="company")


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

    company: Mapped[Company] = relationship(back_populates="contracts")


class RecruitmentMission(Base):
    __tablename__ = "recruitment_missions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    job_id: Mapped[str | None] = mapped_column(ForeignKey("job_offers.id"))
    recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), default=MissionStatus.IN_PROGRESS)
    value: Mapped[int | None] = mapped_column(Integer)
    commission: Mapped[int | None] = mapped_column(Integer)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[str | None] = mapped_column(String(16))
    due_date: Mapped[str | None] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    company: Mapped[Company] = relationship(back_populates="missions")
    job = relationship("JobOffer", back_populates="missions")
