from types import SimpleNamespace

import pytest

from app.boot import WEAK_SECRETS, assert_runtime_safe, normalize_database_url


def test_normalize_postgres_urls():
    assert normalize_database_url("postgres://u:p@host:5432/db") == "postgresql+psycopg://u:p@host:5432/db"
    assert normalize_database_url("postgresql://u:p@host/db") == "postgresql+psycopg://u:p@host/db"
    assert normalize_database_url("postgresql+psycopg://u:p@host/db") == "postgresql+psycopg://u:p@host/db"
    assert normalize_database_url("sqlite:///./data/talendus.db").startswith("sqlite:")


def test_normalize_keeps_url_encoded_passwords():
    raw = "postgres://talendus:p%40ss%25word@dpg-host:5432/talendus"
    got = normalize_database_url(raw)
    assert got == "postgresql+psycopg://talendus:p%40ss%25word@dpg-host:5432/talendus"
    assert "%25" in got


def test_production_rejects_debug_and_weak_secrets():
    with pytest.raises(RuntimeError, match="DEBUG"):
        assert_runtime_safe(SimpleNamespace(app_env="production", debug=True, secret_key="x" * 40, jwt_secret="y" * 40, database_url="postgresql+psycopg://u:p@h/db", admin_password=""))
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        assert_runtime_safe(SimpleNamespace(app_env="production", debug=False, secret_key="dev-only-change-me", jwt_secret="y" * 40, database_url="postgresql+psycopg://u:p@h/db", admin_password=""))
    with pytest.raises(RuntimeError, match="SQLite"):
        assert_runtime_safe(SimpleNamespace(app_env="production", debug=False, secret_key="x" * 40, jwt_secret="y" * 40, database_url="sqlite:///./x.db", admin_password=""))
    assert_runtime_safe(SimpleNamespace(app_env="production", debug=False, secret_key="x" * 40, jwt_secret="y" * 40, database_url="postgresql+psycopg://u:p@h/db", admin_password=""))
    assert_runtime_safe(SimpleNamespace(app_env="development", debug=True, secret_key="dev-only-change-me", jwt_secret="dev-only-jwt-change-me", database_url="sqlite://", admin_password="talendus"))
    assert "talendus" in WEAK_SECRETS


def test_production_seed_has_no_direct_employer_or_fake_companies(client, monkeypatch):
    from sqlalchemy import func, select

    from app import seed as seed_mod
    from app.database import SessionLocal
    from app.models import Company, User
    from app.models.enums import UserRole

    monkeypatch.setattr(seed_mod.settings, "app_env", "production")
    monkeypatch.setattr(seed_mod.settings, "admin_email", "lea.super@talendus.ca")
    monkeypatch.setattr(seed_mod.settings, "admin_password", "SuperSecret12!")
    seed_mod.seed_if_empty()
    db = SessionLocal()
    try:
        emails = set(db.scalars(select(User.email)))
        assert "lea.super@talendus.ca" in emails
        assert "j.rivest@metalco.ca" not in emails
        assert "karine.lavoie@email.ca" not in emails
        assert db.scalar(select(func.count()).select_from(Company)) == 0
        admin = db.scalar(select(User).where(User.email == "lea.super@talendus.ca"))
        assert admin.role == UserRole.SUPER_ADMIN
        assert seed_mod.bootstrap_production_admin(db) is None
    finally:
        db.close()
