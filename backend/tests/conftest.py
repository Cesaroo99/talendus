import os

os.environ["APP_ENV"] = "test"
os.environ["DEBUG"] = "false"
os.environ["JWT_SECRET"] = "test-jwt-secret-not-for-production"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["EMAIL_ENABLED"] = "false"
os.environ["RATE_LIMIT_PER_MINUTE"] = "1000"
os.environ["SEED_PASSWORD"] = "talendus"
os.environ["DATABASE_URL"] = "sqlite://"

from app.config import get_settings

get_settings.cache_clear()

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine, SessionLocal
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def register(client: TestClient, email: str, role: str = "CANDIDATE", **extra) -> dict:
    payload = {
        "email": email,
        "password": "Password1!",
        "first_name": extra.get("first_name", "Alex"),
        "last_name": extra.get("last_name", "Test"),
        "role": role,
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 200, res.text
    return res.json()["data"]


def auth_header(tokens: dict) -> dict:
    return {"Authorization": f"Bearer {tokens['access_token']}"}
