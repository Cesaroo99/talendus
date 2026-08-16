"""Gardes-fous de démarrage : production uniquement avec secrets forts et PostgreSQL."""

from __future__ import annotations

WEAK_SECRETS = frozenset(
    {
        "",
        "dev-only-change-me",
        "dev-only-jwt-change-me",
        "change-me-to-a-long-random-string",
        "change-me-to-another-long-random-string",
        "talendus",
        "secret",
        "changeme",
    }
)


def normalize_database_url(url: str) -> str:
    """Render / Heroku fournissent postgres:// ; SQLAlchemy 2 + psycopg 3 exigent postgresql+psycopg://."""
    value = (url or "").strip()
    if value.startswith("postgres://"):
        value = "postgresql://" + value[len("postgres://") :]
    if value.startswith("postgresql://"):
        value = "postgresql+psycopg://" + value[len("postgresql://") :]
    return value


def assert_runtime_safe(settings) -> None:
    if getattr(settings, "app_env", "development") != "production":
        return
    if getattr(settings, "debug", False):
        raise RuntimeError("DEBUG=true est interdit en production.")
    for label, value in (
        ("SECRET_KEY", getattr(settings, "secret_key", "")),
        ("JWT_SECRET", getattr(settings, "jwt_secret", "")),
    ):
        secret = (value or "").strip()
        if secret in WEAK_SECRETS or len(secret) < 32:
            raise RuntimeError(f"{label} trop faible pour la production (32 caractères minimum, pas de valeur d'exemple).")
    database_url = getattr(settings, "database_url", "")
    if database_url.startswith("sqlite"):
        raise RuntimeError("SQLite est interdit en production. Utilisez PostgreSQL (DATABASE_URL).")
    admin_password = (getattr(settings, "admin_password", "") or "").strip()
    if admin_password and admin_password in WEAK_SECRETS:
        raise RuntimeError("ADMIN_PASSWORD trop faible pour la production.")
