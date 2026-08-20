import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import JobSearchStatus, utcnow
from app.models.identity import uid


class Candidate(Base):
    """Profil candidat (1–1 avec users). Table `candidates` = candidate_profiles."""

    __tablename__ = "candidates"
    __table_args__ = (
        Index("ix_candidates_city", "city"),
        Index("ix_candidates_sector", "sector"),
        Index("ix_candidates_search_status", "job_search_status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    city: Mapped[str | None] = mapped_column(String(80))
    address: Mapped[str | None] = mapped_column(String(255))
    province: Mapped[str | None] = mapped_column(String(80))
    country: Mapped[str | None] = mapped_column(String(80), default="Canada")
    birth_date: Mapped[str | None] = mapped_column(String(16))
    title: Mapped[str | None] = mapped_column(String(120))
    sector: Mapped[str | None] = mapped_column(String(80))
    years_experience: Mapped[int | None] = mapped_column(Integer)
    experience_level: Mapped[str | None] = mapped_column(String(40))
    availability: Mapped[str | None] = mapped_column(String(80))
    desired_salary_min: Mapped[int | None] = mapped_column(Integer)
    desired_salary_max: Mapped[int | None] = mapped_column(Integer)
    mobility: Mapped[str | None] = mapped_column(String(120))
    contract_type: Mapped[str | None] = mapped_column(String(160))
    shift_preference: Mapped[str | None] = mapped_column(String(160))
    languages: Mapped[str | None] = mapped_column(Text)  # CSV
    skills: Mapped[str | None] = mapped_column(Text)  # CSV
    bio: Mapped[str | None] = mapped_column(Text)
    education_level: Mapped[str | None] = mapped_column(String(80))
    job_search_status: Mapped[JobSearchStatus] = mapped_column(Enum(JobSearchStatus), default=JobSearchStatus.ACTIVE)
    work_preferences: Mapped[str | None] = mapped_column(Text)
    pipeline_status: Mapped[str | None] = mapped_column(String(40))
    assigned_recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="candidate", foreign_keys=[user_id])
    experiences: Mapped[list["CandidateExperience"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    education: Mapped[list["CandidateEducation"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    certifications: Mapped[list["CandidateCertification"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    resumes: Mapped[list["Resume"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="candidate")


class CandidateExperience(Base):
    __tablename__ = "candidate_experiences"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    company: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(120), nullable=False)
    years: Mapped[str | None] = mapped_column(String(80))
    description: Mapped[str | None] = mapped_column(Text)

    candidate: Mapped[Candidate] = relationship(back_populates="experiences")


class CandidateEducation(Base):
    __tablename__ = "candidate_education"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    school: Mapped[str] = mapped_column(String(160), nullable=False)
    diploma: Mapped[str | None] = mapped_column(String(160))
    year: Mapped[str | None] = mapped_column(String(16))

    candidate: Mapped[Candidate] = relationship(back_populates="education")


class CandidateCertification(Base):
    __tablename__ = "candidate_certifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    issuer: Mapped[str | None] = mapped_column(String(160))
    year: Mapped[str | None] = mapped_column(String(16))

    candidate: Mapped[Candidate] = relationship(back_populates="certifications")


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_url: Mapped[str | None] = mapped_column(String(500))
    mime_type: Mapped[str] = mapped_column(String(80), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True)
    parse_status: Mapped[str | None] = mapped_column(String(32))
    parse_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    candidate: Mapped[Candidate] = relationship(back_populates="resumes")
