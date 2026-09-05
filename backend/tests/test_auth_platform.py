from conftest import auth_header, promote_admin, register, staff_publish_job


def test_auth_providers(client):
    res = client.get("/api/auth/providers")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["password"] is True
    assert data["google"] is False
    assert data["linkedin"] is False
    assert data["google_client_id"] == ""


def test_oauth_unavailable_without_config(client):
    google = client.post("/api/auth/oauth/google", json={"id_token": "x" * 40, "role": "CANDIDATE"})
    assert google.status_code == 503
    assert google.json()["code"] == "OAUTH_UNAVAILABLE"
    linkedin = client.post("/api/auth/oauth/linkedin", json={"access_token": "token-abc", "role": "EMPLOYER"})
    assert linkedin.status_code == 503


def test_register_honeypot_rejected(client):
    res = client.post(
        "/api/auth/register",
        json={
            "email": "bot@example.com",
            "password": "Password1!",
            "first_name": "Bot",
            "last_name": "Spam",
            "role": "CANDIDATE",
            "website_url": "https://spam.example",
        },
    )
    assert res.status_code == 400
    assert res.json()["code"] == "SPAM_REJECTED"


def test_employer_register_uses_company_name(client):
    res = client.post(
        "/api/auth/register",
        json={
            "email": "usine@example.com",
            "password": "Password1!",
            "first_name": "Marie",
            "last_name": "Tremblay",
            "role": "EMPLOYER",
            "company_name": "Usine Nord Inc.",
        },
    )
    assert res.status_code == 200
    headers = auth_header(res.json()["data"])
    company = client.get("/api/companies/me", headers=headers)
    assert company.status_code == 200
    assert company.json()["data"]["name"] == "Usine Nord Inc."


def test_forgot_reset_and_verify_flow(client):
    from app.database import SessionLocal
    from app.models import EmailToken, User
    from app.security import hash_token

    data = register(client, "reset-me@example.com")
    user_id = data["user"]["id"]
    forgot = client.post("/api/auth/forgot-password", json={"email": "reset-me@example.com"})
    assert forgot.status_code == 200
    db = SessionLocal()
    row = db.query(EmailToken).filter(EmailToken.user_id == user_id, EmailToken.purpose == "reset").one()
    raw = "not-stored"
    # Recreate a known token
    from app.security import create_refresh_token

    token = create_refresh_token()
    row.token_hash = hash_token(token)
    db.commit()
    db.close()
    reset = client.post("/api/auth/reset-password", json={"token": token, "new_password": "NewPass12!"})
    assert reset.status_code == 200
    login = client.post("/api/auth/login", json={"email": "reset-me@example.com", "password": "NewPass12!"})
    assert login.status_code == 200

    db = SessionLocal()
    user = db.get(User, user_id)
    verify_row = db.query(EmailToken).filter(EmailToken.user_id == user_id, EmailToken.purpose == "verify").first()
    vtoken = create_refresh_token()
    if verify_row:
        verify_row.token_hash = hash_token(vtoken)
        db.commit()
    db.close()
    if verify_row:
        verified = client.post("/api/auth/verify-email", json={"token": vtoken})
        assert verified.status_code == 200
        me = client.get("/api/users/me", headers=auth_header(login.json()["data"]))
        assert me.json()["data"]["is_email_verified"] is True


def test_login_trims_email(client):
    register(client, "spaced@example.com")
    res = client.post("/api/auth/login", json={"email": "  Spaced@example.com  ", "password": "Password1!"})
    assert res.status_code == 200, res.text
    assert res.json()["data"]["access_token"]
    forgot = client.post("/api/auth/forgot-password", json={"email": "  spaced@example.com "})
    assert forgot.status_code == 200


def test_login_lockout_and_journal(client):
    register(client, "lock@example.com")
    for _ in range(5):
        bad = client.post("/api/auth/login", json={"email": "lock@example.com", "password": "WrongPass1"})
        assert bad.status_code == 401
    locked = client.post("/api/auth/login", json={"email": "lock@example.com", "password": "WrongPass1"})
    assert locked.status_code == 429
    assert locked.json()["code"] == "LOGIN_LOCKED"
    headers = auth_header(register(client, "journal@example.com"))
    events = client.get("/api/auth/login-events", headers=headers)
    assert events.status_code == 200
    assert events.json()["data"]
    sessions = client.get("/api/auth/sessions", headers=headers)
    assert sessions.status_code == 200
    assert sessions.json()["data"]


def test_refresh_rotates_tokens(client):
    data = register(client, "refresh-me@example.com")
    old_refresh = data["refresh_token"]
    res = client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert res.status_code == 200, res.text
    tokens = res.json()["data"]
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["refresh_token"] != old_refresh
    me = client.get("/api/users/me", headers={"Authorization": "Bearer " + tokens["access_token"]})
    assert me.status_code == 200
    reused = client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert reused.status_code == 401


def test_job_alerts_and_duplicate_job(client):
    emp = register(client, "alert-emp@example.com", "EMPLOYER")
    admin = promote_admin(client, "alert-admin@example.com")
    emp_h = auth_header(emp)
    admin_h = auth_header(admin)
    job = client.post(
        "/api/jobs",
        headers=admin_h,
        json={
            "title": "Machiniste CNC",
            "location": "Laval",
            "sector": "Usinage",
            "slug": "machiniste-alerte",
            "company_id": client.get("/api/companies/me", headers=emp_h).json()["data"]["id"],
        },
    ).json()["data"]
    cand = register(client, "alert-cand@example.com")
    cand_h = auth_header(cand)
    created = client.post("/api/alerts", headers=cand_h, json={"keywords": "Machiniste", "city": "Laval"})
    assert created.status_code == 200
    listed = client.get("/api/alerts", headers=cand_h)
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 1
    blocked_pub = client.post(f"/api/jobs/{job['id']}/publish", headers=emp_h)
    assert blocked_pub.status_code == 403
    pub = client.post(f"/api/jobs/{job['id']}/publish", headers=admin_h)
    assert pub.status_code == 200
    notifs = client.get("/api/notifications", headers=cand_h)
    assert any(n["type"] == "JOB_MATCH" for n in notifs.json()["data"])
    copy_blocked = client.post(f"/api/jobs/{job['id']}/duplicate", headers=emp_h)
    assert copy_blocked.status_code == 403
    copy = client.post(f"/api/jobs/{job['id']}/duplicate", headers=admin_h)
    assert copy.status_code == 200
    assert copy.json()["data"]["status"] == "DRAFT"
    assert "copie" in copy.json()["data"]["title"].lower() or "copie" in copy.json()["data"]["slug"]
    deleted = client.delete(f"/api/jobs/{copy.json()['data']['id']}", headers=admin_h)
    assert deleted.status_code == 200
    blocked = client.delete(f"/api/jobs/{job['id']}", headers=admin_h)
    assert blocked.status_code == 400


def test_candidate_profile_address_fields(client):
    cand = register(client, "addr@example.com")
    headers = auth_header(cand)
    patched = client.patch(
        "/api/candidates/me",
        headers=headers,
        json={"address": "12 rue de l'Usine", "province": "Québec", "country": "Canada", "birth_date": "1990-04-12", "city": "Montréal"},
    )
    assert patched.status_code == 200
    me = client.get("/api/candidates/me", headers=headers)
    body = me.json()["data"]
    assert body["address"] == "12 rue de l'Usine"
    assert body["birth_date"] == "1990-04-12"
    dash = client.get("/api/candidates/me/dashboard", headers=headers)
    assert "saved_jobs" in dash.json()["data"]["stats"]


def test_oauth_refuses_role_switch_and_keeps_existing_role(client):
    from app.database import SessionLocal
    from app.errors import AppError
    from app.models import User
    from app.models.enums import UserRole
    from app.services.auth import login_with_identity

    data = register(client, "oauth-role@example.com")
    db = SessionLocal()
    try:
        try:
            login_with_identity(
                db,
                email="oauth-role@example.com",
                first_name="Alex",
                last_name="Test",
                role=UserRole.EMPLOYER,
                company_name="Usine Nord",
                ip=None,
                user_agent=None,
                provider="google",
                email_verified=True,
            )
            raise AssertionError("expected ACCOUNT_EXISTS")
        except AppError as exc:
            assert exc.status_code == 409
            assert exc.code == "ACCOUNT_EXISTS"
            assert "talent" in exc.message
        user = db.get(User, data["user"]["id"])
        assert user.role == UserRole.CANDIDATE
        same = login_with_identity(
            db,
            email="oauth-role@example.com",
            first_name="Alex",
            last_name="Test",
            role=UserRole.CANDIDATE,
            company_name=None,
            ip=None,
            user_agent=None,
            provider="google",
            email_verified=True,
        )
        assert same[0].role == UserRole.CANDIDATE
        assert same[0].is_email_verified is True
    finally:
        db.close()


def test_oauth_linkedin_does_not_verify_existing_password_account(client):
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import UserRole
    from app.services.auth import login_with_identity

    data = register(client, "oauth-li@example.com")
    db = SessionLocal()
    user = db.get(User, data["user"]["id"])
    assert user.is_email_verified is False
    login_with_identity(
        db,
        email="oauth-li@example.com",
        first_name="Alex",
        last_name="Test",
        role=UserRole.CANDIDATE,
        company_name=None,
        ip=None,
        user_agent=None,
        provider="linkedin",
        email_verified=False,
    )
    db.expire_all()
    user = db.get(User, data["user"]["id"])
    assert user.is_email_verified is False
    db.close()


def test_reset_and_change_password_revoke_sessions(client):
    from app.database import SessionLocal
    from app.models import EmailToken
    from app.security import create_refresh_token, hash_token

    data = register(client, "revoke-me@example.com")
    old_refresh = data["refresh_token"]
    forgot = client.post("/api/auth/forgot-password", json={"email": "revoke-me@example.com"})
    assert forgot.status_code == 200
    db = SessionLocal()
    row = (
        db.query(EmailToken)
        .filter(EmailToken.user_id == data["user"]["id"], EmailToken.purpose == "reset")
        .order_by(EmailToken.created_at.desc())
        .first()
    )
    token = create_refresh_token()
    row.token_hash = hash_token(token)
    db.commit()
    db.close()
    reset = client.post("/api/auth/reset-password", json={"token": token, "new_password": "NewPass12!"})
    assert reset.status_code == 200
    reused = client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert reused.status_code == 401
    login = client.post("/api/auth/login", json={"email": "revoke-me@example.com", "password": "NewPass12!"})
    assert login.status_code == 200
    fresh = login.json()["data"]
    changed = client.post(
        "/api/auth/change-password",
        headers=auth_header(fresh),
        json={"current_password": "NewPass12!", "new_password": "NewerPass12!"},
    )
    assert changed.status_code == 200
    reused2 = client.post("/api/auth/refresh", json={"refresh_token": fresh["refresh_token"]})
    assert reused2.status_code == 401


def test_reset_and_verify_missing_user_return_400(client):
    from datetime import timedelta

    from sqlalchemy import text

    from app.database import SessionLocal
    from app.models import EmailToken
    from app.models.enums import utcnow
    from app.security import create_refresh_token, hash_token

    data = register(client, "ghost-reset@example.com")
    user_id = data["user"]["id"]
    token = create_refresh_token()
    vtoken = create_refresh_token()
    db = SessionLocal()
    db.add(EmailToken(user_id=user_id, purpose="reset", token_hash=hash_token(token), expires_at=utcnow() + timedelta(hours=2)))
    db.add(EmailToken(user_id=user_id, purpose="verify", token_hash=hash_token(vtoken), expires_at=utcnow() + timedelta(hours=2)))
    db.commit()
    db.execute(text("PRAGMA foreign_keys=OFF"))
    db.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
    db.commit()
    db.close()
    reset = client.post("/api/auth/reset-password", json={"token": token, "new_password": "NewPass12!"})
    assert reset.status_code == 400
    assert reset.json()["code"] == "INVALID_TOKEN"
    verified = client.post("/api/auth/verify-email", json={"token": vtoken})
    assert verified.status_code == 400
    assert verified.json()["code"] == "INVALID_TOKEN"


def test_unverified_jwt_blocked_when_email_sending_is_on(client, monkeypatch):
    from app.config import get_settings

    data = register(client, "gate-me@example.com")
    headers = auth_header(data)
    monkeypatch.setenv("EMAIL_ENABLED", "true")
    get_settings.cache_clear()
    try:
        blocked = client.get("/api/candidates/me", headers=headers)
        assert blocked.status_code == 403
        assert blocked.json()["code"] == "EMAIL_NOT_VERIFIED"
        me = client.get("/api/users/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["data"]["is_email_verified"] is False
        resend = client.post("/api/auth/resend-verification", headers=headers)
        assert resend.status_code == 200
        reused = client.post("/api/auth/refresh", json={"refresh_token": data["refresh_token"]})
        assert reused.status_code == 403
        assert reused.json()["code"] == "EMAIL_NOT_VERIFIED"
    finally:
        monkeypatch.setenv("EMAIL_ENABLED", "false")
        get_settings.cache_clear()
