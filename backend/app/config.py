from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Talendus API"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "dev-only-change-me"
    jwt_secret: str = "dev-only-jwt-change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    refresh_token_days: int = 14

    database_url: str = f"sqlite:///{BACKEND_ROOT / 'data' / 'talendus.db'}"

    frontend_url: str = "http://localhost:8000"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000"

    email_enabled: bool = False
    email_server: str = "localhost"
    email_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_from: str = "Talendus <noreply@talendus.ca>"
    email_use_tls: bool = True

    storage_dir: str = str(BACKEND_ROOT / "storage")
    storage_backend: str = "local"
    s3_bucket: str = ""
    s3_region: str = "ca-central-1"
    s3_endpoint_url: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_prefix: str = "talendus"
    stripe_enabled: bool = True
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_publishable_key: str = ""
    job_match_min_score: int = 50
    max_resume_mb: int = 5
    rate_limit_per_minute: int = 80
    seed_password: str = "talendus"
    default_currency: str = "CAD"
    default_tax_rate_bp: int = 14975

    integrations_timeout_seconds: int = 15
    integrations_max_retries: int = 2

    linkedin_enabled: bool = False
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    linkedin_api_base_url: str = "https://api.linkedin.com"

    indeed_enabled: bool = False
    indeed_publisher_id: str = ""
    indeed_api_key: str = ""
    indeed_api_base_url: str = "https://apis.indeed.com"

    whatsapp_enabled: bool = False
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_webhook_secret: str = ""
    whatsapp_api_base_url: str = "https://graph.facebook.com/v21.0"

    google_maps_enabled: bool = False
    google_maps_api_key: str = ""
    google_maps_api_base_url: str = "https://maps.googleapis.com/maps/api"

    paypal_enabled: bool = False
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_webhook_id: str = ""
    paypal_api_base_url: str = "https://api-m.sandbox.paypal.com"

    openai_enabled: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_api_base_url: str = "https://api.openai.com/v1"

    esignature_enabled: bool = False
    esignature_provider: str = "docusign"
    esignature_api_key: str = ""
    esignature_api_base_url: str = ""
    esignature_webhook_secret: str = ""

    tracking_enabled: bool = False
    ga_measurement_id: str = ""
    meta_pixel_id: str = ""
    seo_canonical_host: str = "https://talendus.ca"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def resume_dir(self) -> Path:
        path = Path(self.storage_dir) / "resumes"
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    (BACKEND_ROOT / "data").mkdir(parents=True, exist_ok=True)
    return Settings()
