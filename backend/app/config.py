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
    max_resume_mb: int = 5
    rate_limit_per_minute: int = 80
    seed_password: str = "talendus"

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
