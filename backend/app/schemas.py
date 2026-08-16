from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import ApplicationStatus, JobStatus, UserRole


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserPublic"


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    phone: str | None = None
    role: UserRole = UserRole.CANDIDATE


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class RefreshIn(BaseModel):
    refresh_token: str


class PasswordChangeIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class PasswordForgotIn(BaseModel):
    email: EmailStr


class PasswordResetIn(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class EmailVerifyIn(BaseModel):
    token: str


class UserPublic(ORMModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None
    role: UserRole
    title: str | None
    is_active: bool
    is_email_verified: bool


class UserUpdateIn(BaseModel):
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)
    phone: str | None = None
    title: str | None = None


class CandidateProfileIn(BaseModel):
    city: str | None = None
    title: str | None = None
    sector: str | None = None
    years_experience: int | None = Field(default=None, ge=0, le=60)
    experience_level: str | None = None
    availability: str | None = None
    desired_salary_min: int | None = None
    desired_salary_max: int | None = None
    mobility: str | None = None
    contract_type: str | None = None
    shift_preference: str | None = None
    languages: str | None = None
    skills: str | None = None
    bio: str | None = None


class ExperienceIn(BaseModel):
    company: str
    role: str
    years: str | None = None
    description: str | None = None


class EducationIn(BaseModel):
    school: str
    diploma: str | None = None
    year: str | None = None


class CertificationIn(BaseModel):
    name: str
    issuer: str | None = None
    year: str | None = None


class CompanyIn(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    sector: str | None = None
    city: str | None = None
    contact_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    website: str | None = None
    employees: int | None = None


class JobIn(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    description: str = ""
    company_id: str | None = None
    location: str | None = None
    sector: str | None = None
    contract_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_display: str | None = None
    skills: str | None = None
    experience_level: str | None = None
    education_required: str | None = None
    certifications: str | None = None
    shift: str | None = None
    benefits: str | None = None
    responsibilities: str | None = None
    qualifications: str | None = None
    slug: str | None = None


class JobPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    description: str | None = None
    location: str | None = None
    sector: str | None = None
    contract_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_display: str | None = None
    skills: str | None = None
    experience_level: str | None = None
    education_required: str | None = None
    certifications: str | None = None
    shift: str | None = None
    benefits: str | None = None
    responsibilities: str | None = None
    qualifications: str | None = None
    slug: str | None = None


class JobOut(ORMModel):
    id: str
    slug: str
    title: str
    description: str
    location: str | None
    sector: str | None
    contract_type: str | None
    salary_display: str | None
    salary_min: int | None
    salary_max: int | None
    skills: str | None
    experience_level: str | None
    shift: str | None
    status: JobStatus
    published_at: datetime | None
    expires_at: datetime | None
    company_id: str
    company_name: str | None = None


class JobSearchIn(BaseModel):
    q: str | None = None
    sector: str | None = None
    location: str | None = None
    contract_type: str | None = None
    experience: str | None = None
    salary_min: int | None = None
    company: str | None = None
    status: JobStatus | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=50)
    sort: str = "published_at"


class ApplicationCreateIn(BaseModel):
    job_id: str | None = None
    job_slug: str | None = None
    cover_note: str | None = None
    resume_id: str | None = None


class PublicApplyIn(BaseModel):
    job_slug: str
    first_name: str
    last_name: str = ""
    email: EmailStr
    phone: str | None = None
    cover_note: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    cv_url: str | None = None


class StatusChangeIn(BaseModel):
    status: ApplicationStatus
    comment: str | None = None


class NoteIn(BaseModel):
    entity_type: str
    entity_id: str
    text: str = Field(min_length=1, max_length=4000)


class ContactIn(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    subject: str | None = None
    message: str = Field(min_length=2, max_length=5000)
    company: str | None = None


class RecruiterInviteIn(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    title: str | None = None
    specialty: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class MissionIn(BaseModel):
    company_id: str
    job_id: str | None = None
    recruiter_id: str | None = None
    title: str = Field(min_length=2, max_length=180)
    seats: int = Field(default=1, ge=1, le=500)
    value: int | None = None
    commission: int | None = None
    start_date: str | None = None
    due_date: str | None = None


class JobStatusIn(BaseModel):
    status: JobStatus


class AdminCandidateIn(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    phone: str | None = None
    city: str | None = None
    title: str | None = None
    sector: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
