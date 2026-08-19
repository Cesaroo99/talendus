from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import ApplicationStatus, JobStatus, utcnow
from app.models.identity import uid


class JobOffer(Base):
    __tablename__ = "job_offers"
    __table_args__ = (
        Index("ix_jobs_status_published", "status", "published_at"),
        Index("ix_jobs_location_sector", "location", "sector"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    recruiter_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    responsibilities: Mapped[str | None] = mapped_column(Text)
    qualifications: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(80), index=True)
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)
    place_id: Mapped[str | None] = mapped_column(String(128))
    sector: Mapped[str | None] = mapped_column(String(80), index=True)
    contract_type: Mapped[str | None] = mapped_column(String(40))
    salary_min: Mapped[int | None] = mapped_column(Integer)
    salary_max: Mapped[int | None] = mapped_column(Integer)
    salary_display: Mapped[str | None] = mapped_column(String(80))
    currency: Mapped[str] = mapped_column(String(8), default="CAD")
    openings: Mapped[int] = mapped_column(Integer, default=1)
    skills: Mapped[str | None] = mapped_column(Text)
    experience_level: Mapped[str | None] = mapped_column(String(80))
    education_required: Mapped[str | None] = mapped_column(String(160))
    certifications: Mapped[str | None] = mapped_column(Text)
    shift: Mapped[str | None] = mapped_column(String(80))
    schedule: Mapped[str | None] = mapped_column(String(80))
    work_mode: Mapped[str | None] = mapped_column(String(80))
    languages: Mapped[str | None] = mapped_column(String(160))
    overtime: Mapped[str | None] = mapped_column(String(80))
    driver_license: Mapped[str | None] = mapped_column(String(80))
    unionized: Mapped[str | None] = mapped_column(String(40))
    travel: Mapped[str | None] = mapped_column(String(80))
    benefits: Mapped[str | None] = mapped_column(Text)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.DRAFT, index=True)
    start_date: Mapped[str | None] = mapped_column(String(16))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    company = relationship("Company", back_populates="jobs")
    applications: Mapped[list["Application"]] = relationship(back_populates="job")
    missions: Mapped[list] = relationship("RecruitmentMission", back_populates="job", foreign_keys="RecruitmentMission.job_id")
    linked_missions: Mapped[list] = relationship("RecruitmentMission", secondary="mission_jobs", back_populates="linked_jobs")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_application_candidate_job"),
        Index("ix_applications_status_created", "status", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), index=True, nullable=False)
    job_id: Mapped[str] = mapped_column(ForeignKey("job_offers.id"), index=True, nullable=False)
    resume_id: Mapped[str | None] = mapped_column(ForeignKey("resumes.id"))
    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED, index=True)
    cover_note: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(40), default="site")
    staff_notes: Mapped[str | None] = mapped_column(Text)
    match_score: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    candidate = relationship("Candidate", back_populates="applications")
    job: Mapped[JobOffer] = relationship(back_populates="applications")
    resume = relationship("Resume")
    history: Mapped[list["ApplicationStatusHistory"]] = relationship(
        back_populates="application", cascade="all, delete-orphan", order_by="ApplicationStatusHistory.created_at"
    )


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    application_id: Mapped[str] = mapped_column(ForeignKey("applications.id"), index=True, nullable=False)
    old_status: Mapped[str | None] = mapped_column(String(32))
    new_status: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    application: Mapped[Application] = relationship(back_populates="history")
