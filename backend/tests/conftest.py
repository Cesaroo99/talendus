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


def promote_admin(client, email: str) -> dict:
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import UserRole

    data = register(client, email, "EMPLOYER", first_name="Sophie", last_name="Admin")
    db = SessionLocal()
    user = db.get(User, data["user"]["id"])
    user.role = UserRole.ADMIN
    db.commit()
    db.close()
    res = client.post("/api/auth/login", json={"email": email, "password": "Password1!"})
    assert res.status_code == 200
    return res.json()["data"]


def company_id_for(client, emp_tokens: dict) -> str:
    res = client.get("/api/companies/me", headers=auth_header(emp_tokens))
    assert res.status_code == 200, res.text
    return res.json()["data"]["id"]


def staff_publish_job(client, emp_tokens: dict, admin_tokens: dict | None = None, **fields):
    if admin_tokens is None:
        slug = fields.get("slug", "job")
        admin_tokens = promote_admin(client, f"staff-{slug}@example.com")
    payload = {
        "title": "Cariste",
        "location": "Laval",
        "sector": "Entrepôt",
        "company_id": company_id_for(client, emp_tokens),
    }
    payload.update(fields)
    created = client.post("/api/jobs", headers=auth_header(admin_tokens), json=payload)
    assert created.status_code == 200, created.text
    job = created.json()["data"]
    published = client.post(f"/api/jobs/{job['id']}/publish", headers=auth_header(admin_tokens))
    assert published.status_code == 200, published.text
    return published.json()["data"]
