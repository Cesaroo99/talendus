from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import EmailLog, SystemSetting
from tests.conftest import auth_header, promote_admin, register

ROOT = Path(__file__).resolve().parents[2]


def _promote(client, email: str, role: str) -> dict:
    from app.models import User
    from app.models.enums import UserRole

    data = register(client, email, "EMPLOYER")
    db = SessionLocal()
    user = db.get(User, data["user"]["id"])
    user.role = UserRole[role]
    db.commit()
    db.close()
    res = client.post("/api/auth/login", json={"email": email, "password": "Password1!"})
    assert res.status_code == 200
    return res.json()["data"]


def test_portal_email_links_follow_role_and_locale(client):
    register(client, "link-cand@example.com")
    register(client, "link-emp@example.com", "EMPLOYER")
    en = client.post(
        "/api/auth/register",
        json={
            "email": "link-en@example.com",
            "password": "Password1!",
            "first_name": "Sam",
            "last_name": "Lee",
            "locale": "en-CA",
        },
    )
    assert en.status_code == 200, en.text
    db = SessionLocal()
    logs = list(db.scalars(select(EmailLog).order_by(EmailLog.created_at.asc())).all())
    bodies = "\n".join((row.body or "") + "\n" + (row.subject or "") for row in logs)
    db.close()
    assert "espace.html#/verify/" in bodies
    assert "espace-employeur.html#/verify/" in bodies
    assert "en/account.html#/verify/" in bodies
    assert "m.html#/verify" not in bodies
    assert "Verify your email" in bodies


def test_resend_verification_email_is_public_and_silent(client):
    register(client, "resend-me@example.com")
    missing = client.post("/api/auth/resend-verification-email", json={"email": "nobody@example.com"})
    assert missing.status_code == 200
    found = client.post("/api/auth/resend-verification-email", json={"email": "resend-me@example.com"})
    assert found.status_code == 200
    db = SessionLocal()
    verify_logs = list(
        db.scalars(select(EmailLog).where(EmailLog.to_email == "resend-me@example.com")).all()
    )
    db.close()
    assert len(verify_logs) >= 3


def test_login_lockout_follows_email_across_ips(client):
    register(client, "lock-ip@example.com")
    for i in range(5):
        bad = client.post(
            "/api/auth/login",
            json={"email": "lock-ip@example.com", "password": "WrongPass1"},
            headers={"X-Real-IP": f"203.0.113.{i + 1}"},
        )
        assert bad.status_code == 401
    locked = client.post(
        "/api/auth/login",
        json={"email": "lock-ip@example.com", "password": "WrongPass1"},
        headers={"X-Real-IP": "198.51.100.9"},
    )
    assert locked.status_code == 429
    assert locked.json()["code"] == "LOGIN_LOCKED"


def test_email_gate_follows_explicit_smtp_override(client):
    register(client, "gate-ov@example.com")
    db = SessionLocal()
    db.add(SystemSetting(key="smtp.enabled", value="oui"))
    db.commit()
    db.close()
    blocked = client.post("/api/auth/login", json={"email": "gate-ov@example.com", "password": "Password1!"})
    assert blocked.status_code == 403
    assert blocked.json()["code"] == "EMAIL_NOT_VERIFIED"
    db = SessionLocal()
    row = db.scalar(select(SystemSetting).where(SystemSetting.key == "smtp.enabled"))
    row.value = "non"
    db.commit()
    db.close()
    ok = client.post("/api/auth/login", json={"email": "gate-ov@example.com", "password": "Password1!"})
    assert ok.status_code == 200, ok.text


def test_oauth_unverified_existing_account_blocked_when_gate_on(client, monkeypatch):
    from app.config import get_settings
    from app.errors import AppError
    from app.models.enums import UserRole
    from app.services.auth import login_with_identity

    register(client, "oauth-gate@example.com")
    monkeypatch.setenv("EMAIL_ENABLED", "true")
    get_settings.cache_clear()
    db = SessionLocal()
    try:
        login_with_identity(
            db,
            email="oauth-gate@example.com",
            first_name="Alex",
            last_name="Test",
            role=UserRole.CANDIDATE,
            company_name=None,
            ip=None,
            user_agent=None,
            provider="linkedin",
            email_verified=False,
        )
        raise AssertionError("EMAIL_NOT_VERIFIED attendu")
    except AppError as exc:
        assert exc.status_code == 403
        assert exc.code == "EMAIL_NOT_VERIFIED"
    finally:
        db.close()
        monkeypatch.setenv("EMAIL_ENABLED", "false")
        get_settings.cache_clear()


def test_linkedin_provider_requires_secret(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setenv("LINKEDIN_OAUTH_CLIENT_ID", "li-client")
    monkeypatch.delenv("LINKEDIN_OAUTH_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("LINKEDIN_CLIENT_SECRET", raising=False)
    get_settings.cache_clear()
    try:
        res = client.get("/api/auth/providers")
        assert res.status_code == 200
        assert res.json()["data"]["linkedin"] is False
        monkeypatch.setenv("LINKEDIN_OAUTH_CLIENT_SECRET", "li-secret")
        get_settings.cache_clear()
        on = client.get("/api/auth/providers")
        assert on.json()["data"]["linkedin"] is True
    finally:
        monkeypatch.delenv("LINKEDIN_OAUTH_CLIENT_ID", raising=False)
        monkeypatch.delenv("LINKEDIN_OAUTH_CLIENT_SECRET", raising=False)
        get_settings.cache_clear()


def test_password_change_invalidates_access_token(client):
    data = register(client, "ver-token@example.com")
    headers = auth_header(data)
    assert client.get("/api/users/me", headers=headers).status_code == 200
    changed = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={"current_password": "Password1!", "new_password": "NewerPass12!"},
    )
    assert changed.status_code == 200
    dead = client.get("/api/users/me", headers=headers)
    assert dead.status_code == 401


def test_finance_bootstrap_omits_crm_pii(client):
    admin = promote_admin(client, "fin-admin@example.com")
    admin_h = auth_header(admin)
    client.post(
        "/api/admin/candidates",
        headers=admin_h,
        json={
            "email": "secret.fin@example.com",
            "first_name": "Secret",
            "last_name": "Candidat",
            "phone": "514 555-0188",
            "city": "Montréal",
            "title": "Soudeur",
        },
    )
    finance = _promote(client, "fin-user@example.com", "FINANCE")
    boot = client.get("/api/admin/bootstrap", headers=auth_header(finance)).json()["data"]
    assert boot["candidates"] == []
    assert boot["applications"] == []
    assert boot["notes"] == []
    assert boot["documents"] == []
    assert boot["jobMatches"] == []
    assert boot["activities"] == []
    assert isinstance(boot["invoices"], list)
    assert isinstance(boot["payments"], list)
    assert "revenue" in boot["monthly"]


def test_recruiter_company_list_hides_assigned_to_other(client):
    from app.models import Company

    promote_admin(client, "list-admin@example.com")
    emp = register(client, "list-emp@example.com", "EMPLOYER")
    rec_a = _promote(client, "list-rec-a@example.com", "RECRUITER")
    rec_b = _promote(client, "list-rec-b@example.com", "RECRUITER")
    company = client.get("/api/companies/me", headers=auth_header(emp)).json()["data"]
    db = SessionLocal()
    row = db.get(Company, company["id"])
    row.assigned_recruiter_id = rec_a["user"]["id"]
    db.commit()
    db.close()
    listed_a = client.get("/api/companies", headers=auth_header(rec_a)).json()["data"]
    listed_b = client.get("/api/companies", headers=auth_header(rec_b)).json()["data"]
    assert any(item["id"] == company["id"] for item in listed_a)
    assert all(item["id"] != company["id"] for item in listed_b)


def test_duplicate_prospect_returns_409(client):
    admin = promote_admin(client, "pros-dup-admin@example.com")
    h = auth_header(admin)
    payload = {"side": "employer", "email": "dup.lead@example.com", "company_name": "Usine Dup"}
    first = client.post("/api/admin/prospects", headers=h, json=payload)
    assert first.status_code == 200, first.text
    second = client.post("/api/admin/prospects", headers=h, json=payload)
    assert second.status_code == 409
    assert second.json()["code"] == "PROSPECT_EXISTS"


def test_overlay_and_copy_are_optimal():
    auth = (ROOT / "assets" / "js" / "auth-gate.js").read_text(encoding="utf-8")
    assert "resend-verification-email" in auth or "resendVerificationEmail" in auth
    assert "data-resend-verify" in auth
    assert "EMAIL_NOT_VERIFIED" in auth
    api = (ROOT / "assets" / "js" / "api.js").read_text(encoding="utf-8")
    assert "resend-verification-email" in api
    assert "AUTH_CODE_EN" in api
    account = (ROOT / "assets" / "js" / "account.js").read_text(encoding="utf-8")
    assert "__tlPushEnabled" in account
    assert "notify_push" in account
    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    assert "talendus-app-v34" in sw
    assert '"/assets/js/mobile-app.js"' not in sw
    about = (ROOT / "about.html").read_text(encoding="utf-8")
    assert 'rel="canonical" href="https://talendus.ca/a-propos.html"' in about
    footer = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
    assert "Executive search" in footer
    assert "Search mandates" not in footer
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Disallow: /app.html" in robots
    assert "Disallow: /projects-left.html" in robots
