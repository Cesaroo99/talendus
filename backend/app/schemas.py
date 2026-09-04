from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.enums import ApplicationStatus, CompanyMemberRole, InterviewStatus, InterviewType, InvoiceStatus, JobSearchStatus, JobStatus, PaymentMethod, UserRole


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def _clean_email(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    return value


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
    company_name: str | None = Field(default=None, max_length=160)
    website_url: str | None = None  # honeypot anti-spam

    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, value: Any) -> Any:
        return _clean_email(value)


class OAuthGoogleIn(BaseModel):
    id_token: str = Field(min_length=20, max_length=8000)
    role: UserRole = UserRole.CANDIDATE
    company_name: str | None = Field(default=None, max_length=160)


class OAuthLinkedInIn(BaseModel):
    access_token: str = Field(min_length=8, max_length=4000)
    role: UserRole = UserRole.CANDIDATE
    company_name: str | None = Field(default=None, max_length=160)


class LoginIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, value: Any) -> Any:
        return _clean_email(value)


class RefreshIn(BaseModel):
    refresh_token: str


class PasswordChangeIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class PasswordForgotIn(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, value: Any) -> Any:
        return _clean_email(value)


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
    account_status: str | None = None
    last_login_at: datetime | None = None
    avatar_path: str | None = None


class UserUpdateIn(BaseModel):
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)
    phone: str | None = None
    title: str | None = None


STAFF_ROLES = {UserRole.RECRUITER, UserRole.FINANCE, UserRole.EDITOR, UserRole.ADMIN, UserRole.SUPER_ADMIN}


class StaffUserIn(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    role: UserRole
    password: str = Field(min_length=8, max_length=128)
    title: str | None = Field(default=None, max_length=120)
    phone: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def _staff_email(cls, value: Any) -> Any:
        return _clean_email(value)


class StaffUserPatchIn(BaseModel):
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)
    phone: str | None = None
    title: str | None = None
    is_active: bool | None = None
    role: UserRole | None = None


class TrackingHitIn(BaseModel):
    kind: str | None = Field(default="page_view", max_length=40)
    path: str | None = Field(default="/", max_length=180)


class CandidateProfileIn(BaseModel):
    city: str | None = None
    address: str | None = None
    province: str | None = None
    country: str | None = None
    birth_date: str | None = None
    title: str | None = None
    sector: str | None = None
    work_status: str | None = None
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
    education_level: str | None = None
    job_search_status: JobSearchStatus | None = None
    work_preferences: str | None = None


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
    legal_name: str | None = None
    trade_name: str | None = None
    description: str | None = None
    address: str | None = None
    province: str | None = None
    country: str | None = None
    size_label: str | None = None
    linkedin_url: str | None = None
    facebook_url: str | None = None


class JobAlertIn(BaseModel):
    keywords: str | None = Field(default=None, max_length=180)
    city: str | None = Field(default=None, max_length=80)
    province: str | None = Field(default=None, max_length=80)
    sector: str | None = Field(default=None, max_length=80)
    contract_type: str | None = Field(default=None, max_length=40)
    active: bool | None = True


class JobAlertPatchIn(BaseModel):
    keywords: str | None = Field(default=None, max_length=180)
    city: str | None = Field(default=None, max_length=80)
    province: str | None = Field(default=None, max_length=80)
    sector: str | None = Field(default=None, max_length=80)
    contract_type: str | None = Field(default=None, max_length=40)
    active: bool | None = None


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
    schedule: str | None = None
    work_mode: str | None = None
    languages: str | None = None
    overtime: str | None = None
    driver_license: str | None = None
    unionized: str | None = None
    travel: str | None = None
    work_authorization: str | None = None
    can_sponsor: bool | None = None
    benefits: str | None = None
    responsibilities: str | None = None
    qualifications: str | None = None
    slug: str | None = None
    currency: str | None = "CAD"
    openings: int | None = Field(default=1, ge=1, le=500)
    start_date: str | None = None
    expires_at: str | None = None


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
    schedule: str | None = None
    work_mode: str | None = None
    languages: str | None = None
    overtime: str | None = None
    driver_license: str | None = None
    unionized: str | None = None
    travel: str | None = None
    work_authorization: str | None = None
    can_sponsor: bool | None = None
    benefits: str | None = None
    responsibilities: str | None = None
    qualifications: str | None = None
    slug: str | None = None
    currency: str | None = None
    openings: int | None = Field(default=None, ge=1, le=500)
    start_date: str | None = None
    expires_at: str | None = None


class HiringRequestIn(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    seats: int = Field(default=1, ge=1, le=500)
    location: str | None = None
    sector: str | None = None
    contract_type: str | None = None
    experience_level: str | None = None
    skills: str | None = None
    qualifications: str | None = None
    languages: str | None = None
    shift: str | None = None
    schedule: str | None = None
    work_mode: str | None = None
    overtime: str | None = None
    driver_license: str | None = None
    unionized: str | None = None
    travel: str | None = None
    work_authorization: str | None = None
    can_sponsor: bool | None = None
    salary_display: str | None = None
    start_date: str | None = None
    notes: str | None = Field(default=None, max_length=5000)
    extra_criteria: str | None = Field(default=None, max_length=5000)
    contact_name: str | None = None
    contact_role: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    company_size: str | None = None
    company_id: str | None = None


class HiringRequestPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    seats: int | None = Field(default=None, ge=1, le=500)
    location: str | None = None
    sector: str | None = None
    contract_type: str | None = None
    experience_level: str | None = None
    skills: str | None = None
    qualifications: str | None = None
    languages: str | None = None
    shift: str | None = None
    schedule: str | None = None
    work_mode: str | None = None
    overtime: str | None = None
    driver_license: str | None = None
    unionized: str | None = None
    travel: str | None = None
    work_authorization: str | None = None
    can_sponsor: bool | None = None
    salary_display: str | None = None
    start_date: str | None = None
    notes: str | None = None
    extra_criteria: str | None = None
    contact_name: str | None = None
    contact_role: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    company_size: str | None = None


class HiringRequestStatusIn(BaseModel):
    status: str
    comment: str | None = None


class HiringRequestFeedbackIn(BaseModel):
    action: str = Field(min_length=2, max_length=40)
    comment: str | None = Field(default=None, max_length=4000)


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
    schedule: str | None = None
    work_mode: str | None = None
    languages: str | None = None
    overtime: str | None = None
    driver_license: str | None = None
    unionized: str | None = None
    travel: str | None = None
    work_authorization: str | None = None
    can_sponsor: bool = False
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
    website_url: str | None = None  # honeypot anti-spam


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
    title: str | None = None
    sector: str | None = None
    location: str | None = None
    contract_type: str | None = None
    seats: int | None = Field(default=None, ge=1, le=500)
    experience_level: str | None = None
    skills: str | None = None
    contact_role: str | None = None
    company_size: str | None = None
    website_url: str | None = None  # honeypot anti-spam


class PublicTalentProfileIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = ""
    email: EmailStr
    phone: str | None = None
    title: str | None = None
    city: str | None = None
    sector: str | None = None
    availability: str | None = None
    cv_url: str | None = None
    message: str | None = None
    subject: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    website_url: str | None = None  # honeypot anti-spam


class CompanyMemberIn(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    member_role: CompanyMemberRole = CompanyMemberRole.MEMBER
    password: str | None = Field(default=None, min_length=8, max_length=128)


class CompanyMemberPatchIn(BaseModel):
    member_role: CompanyMemberRole


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


class AdminCandidatePatchIn(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    phone: str | None = None
    city: str | None = None
    title: str | None = None
    sector: str | None = None
    availability: str | None = None
    bio: str | None = None
    skills: str | None = None
    languages: str | None = None
    years_experience: int | None = Field(default=None, ge=0, le=60)
    experience_level: str | None = None
    shift_preference: str | None = None
    work_status: str | None = None
    desired_salary_min: int | None = None
    desired_salary_max: int | None = None
    pipeline_status: str | None = Field(default=None, max_length=40)
    assigned_recruiter_id: str | None = None


class MessageIn(BaseModel):
    recipient_id: str
    body: str = Field(min_length=1, max_length=4000)
    application_id: str | None = None


class InterviewIn(BaseModel):
    candidate_id: str
    application_id: str | None = None
    job_id: str | None = None
    company_id: str | None = None
    scheduled_at: str
    duration_minutes: int | None = Field(default=30, ge=10, le=240)
    location: str | None = None
    type: InterviewType | None = None
    notes: str | None = None
    meeting_url: str | None = Field(default=None, max_length=500)
    meeting_provider: str | None = Field(default=None, max_length=40)
    candidate_can_start: bool | None = None


class InterviewPatchIn(BaseModel):
    scheduled_at: str | None = None
    duration_minutes: int | None = Field(default=None, ge=10, le=240)
    location: str | None = None
    type: InterviewType | None = None
    notes: str | None = None
    meeting_url: str | None = Field(default=None, max_length=500)
    meeting_provider: str | None = Field(default=None, max_length=40)
    status: InterviewStatus | None = None
    candidate_can_start: bool | None = None


class InterviewStatusIn(BaseModel):
    status: InterviewStatus


class InvoiceLineIn(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    quantity: int = Field(default=1, ge=1, le=10000)
    unit_price: int = Field(ge=0)
    reference: str | None = None
    job_id: str | None = None
    mission_id: str | None = None


class InvoiceIn(BaseModel):
    company_id: str
    mission_id: str | None = None
    client_user_id: str | None = None
    amount: int = Field(ge=1)
    amount_ht: int | None = Field(default=None, ge=0)
    tax_amount: int | None = Field(default=None, ge=0)
    tax_rate_bp: int | None = Field(default=None, ge=0, le=100000)
    currency: str | None = "CAD"
    issued_at: str | None = None
    due_date: str | None = None
    notes: str | None = None
    lines: list[InvoiceLineIn] | None = None


class InvoicePatchIn(BaseModel):
    issued_at: str | None = None
    due_date: str | None = None
    notes: str | None = None
    amount: int | None = Field(default=None, ge=1)
    tax_rate_bp: int | None = Field(default=None, ge=0, le=100000)


class InvoiceStatusIn(BaseModel):
    status: InvoiceStatus


class PaymentIn(BaseModel):
    amount: int = Field(ge=1)
    method: PaymentMethod | None = None
    paid_at: str | None = None
    reference: str | None = None


class RefundIn(BaseModel):
    amount: int | None = Field(default=None, ge=1)
    provider: str = "stripe"


class ContractSignIn(BaseModel):
    signer_name: str = Field(min_length=2, max_length=160)
    signer_email: EmailStr | None = None
    accepted: bool = True


class ContractIn(BaseModel):
    company_id: str
    type: str = Field(default="Mandat de recrutement au succès", min_length=2, max_length=120)
    start_date: str | None = None
    end_date: str | None = None
    commission_percent: int | None = Field(default=None, ge=0, le=100)
    terms: str | None = None
    document_name: str | None = Field(default=None, max_length=255)
    status: str | None = None
    template: str | None = Field(default=None, max_length=40)
    role: str | None = Field(default=None, max_length=180)


class ContractPatchIn(BaseModel):
    type: str | None = Field(default=None, min_length=2, max_length=120)
    start_date: str | None = None
    end_date: str | None = None
    commission_percent: int | None = Field(default=None, ge=0, le=100)
    template: str | None = Field(default=None, max_length=40)
    role: str | None = Field(default=None, max_length=180)


class SiteContentIn(BaseModel):
    items: list[dict] = Field(default_factory=list)


class UserPreferenceIn(BaseModel):
    locale: str | None = Field(default=None, max_length=12)
    notify_email: bool | None = None
    notify_in_app: bool | None = None
    notify_application: bool | None = None
    notify_message: bool | None = None
    notify_match: bool | None = None
    notify_interview: bool | None = None
    notify_sms: bool | None = None
    notify_whatsapp: bool | None = None
    notify_push: bool | None = None
    privacy_profile_public: bool | None = None


class SystemSettingIn(BaseModel):
    key: str = Field(min_length=1, max_length=80)
    value: str = ""
    label: str | None = None


class EmailTestIn(BaseModel):
    to_email: EmailStr | None = None


class ProspectIn(BaseModel):
    side: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    company_name: str | None = None
    title: str | None = None
    city: str | None = None
    sector: str | None = None
    source: str | None = None
    source_detail: str | None = None
    message: str | None = None
    stage: str | None = None
    assigned_recruiter_id: str | None = None


class ProspectPatchIn(BaseModel):
    stage: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    company_name: str | None = None
    title: str | None = None
    city: str | None = None
    sector: str | None = None
    source_detail: str | None = None
    message: str | None = None
    assigned_recruiter_id: str | None = None


class ProspectSendIn(BaseModel):
    template_key: str | None = None
    subject: str | None = Field(default=None, max_length=180)
    body: str | None = Field(default=None, max_length=8000)
    invoice_ids: list[str] | None = None
    contract_ids: list[str] | None = None
    force: bool = False


class ProspectBulkSendIn(ProspectSendIn):
    ids: list[str] = Field(min_length=1, max_length=80)
