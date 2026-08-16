from pydantic import BaseModel, Field


class ExternalJobIn(BaseModel):
    external_id: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=180)
    company: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    employment_type: str | None = None
    original_url: str | None = None
    published_at: str | None = None


class ExternalJobImportIn(BaseModel):
    source: str = Field(min_length=2, max_length=40)
    jobs: list[ExternalJobIn] = Field(min_length=1, max_length=100)


class JobSyncIn(BaseModel):
    source: str = Field(min_length=2, max_length=40)
    query: str | None = Field(default=None, max_length=120)


class WhatsAppSendIn(BaseModel):
    recipient: str = Field(min_length=8, max_length=32)
    template: str = Field(min_length=2, max_length=64)
    variables: dict[str, str] | None = None
    message_type: str = "template"


class GeocodeIn(BaseModel):
    address: str = Field(min_length=3, max_length=255)


class DistanceIn(BaseModel):
    origin: str = Field(min_length=2, max_length=255)
    destination: str = Field(min_length=2, max_length=255)


class AiCompleteIn(BaseModel):
    purpose: str = Field(min_length=3, max_length=64)
    prompt: str = Field(min_length=1, max_length=8000)
    max_tokens: int = Field(default=400, ge=16, le=1200)


class EnvelopeIn(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    file_url: str | None = None


class PayPalCheckoutIn(BaseModel):
    amount: int = Field(ge=1)
    currency: str = Field(default="CAD", min_length=3, max_length=3)
    invoice_id: str | None = None
