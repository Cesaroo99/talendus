from pathlib import Path

from conftest import auth_header, company_id_for, register, staff_publish_job

from app.static_guard import is_hidden_static_path

ROOT = Path(__file__).resolve().parents[2]
PDF = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n" + b"x" * 40


def _promote(client, email: str, role: str) -> dict:
    from app.database import SessionLocal
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


def test_hidden_static_paths_block_source_and_storage():
    assert is_hidden_static_path("backend/app/main.py")
    assert is_hidden_static_path("/backend/app/services/auth.py")
    assert is_hidden_static_path("backend/storage/cv.pdf")
    assert is_hidden_static_path("storage/documents/cv.pdf")
    assert is_hidden_static_path(".env")
    assert is_hidden_static_path("mobile/android/app/src/main/java/ca/talendus/app/MainActivity.java")
    assert is_hidden_static_path("scripts/parts.py")
    assert not is_hidden_static_path("index.html")
    assert not is_hidden_static_path("assets/js/account.js")
    assert not is_hidden_static_path(".well-known/assetlinks.json")


def test_permissions_policy_allows_in_app_calls(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    policy = res.headers.get("permissions-policy") or res.headers.get("Permissions-Policy") or ""
    assert "microphone=(self)" in policy
    assert "camera=(self)" in policy
    assert "microphone=()" not in policy
    assert "camera=()" not in policy


def test_public_apply_honeypot_rejected(client):
    emp = register(client, "hp-emp@example.com", "EMPLOYER")
    staff_publish_job(client, emp, title="Cariste", slug="cariste-honeypot")
    res = client.post(
        "/api/applications/public",
        json={
            "job_slug": "cariste-honeypot",
            "first_name": "Bot",
            "last_name": "Spam",
            "email": "bot.apply@example.com",
            "website_url": "https://spam.example",
        },
    )
    assert res.status_code == 400
    assert res.json()["code"] == "SPAM_REJECTED"


def test_public_talent_honeypot_rejected(client):
    res = client.post(
        "/api/talent-profile",
        json={
            "first_name": "Bot",
            "last_name": "Spam",
            "email": "bot.talent@example.com",
            "message": "Profil usine",
            "website_url": "https://spam.example",
        },
    )
    assert res.status_code == 400
    assert res.json()["code"] == "SPAM_REJECTED"


def test_contact_honeypot_rejected(client):
    res = client.post(
        "/api/contact",
        json={
            "name": "Bot",
            "email": "bot.contact@example.com",
            "message": "Bonjour Talendus",
            "website_url": "https://spam.example",
        },
    )
    assert res.status_code == 400
    assert res.json()["code"] == "SPAM_REJECTED"


def test_finance_cannot_see_candidate_cv_but_can_see_company_docs(client):
    cand = register(client, "docs-fin@example.com")
    upload = client.post(
        "/api/documents",
        headers=auth_header(cand),
        files={"file": ("lettre.pdf", PDF, "application/pdf")},
        data={"kind": "cover_letter"},
    )
    assert upload.status_code == 200, upload.text
    cv_id = upload.json()["data"]["id"]
    emp = register(client, "docs-fin-emp@example.com", "EMPLOYER")
    company_id = company_id_for(client, emp)
    finance = _promote(client, "fin-docs@example.com", "FINANCE")
    headers = auth_header(finance)
    listed = client.get("/api/documents", headers=headers)
    assert listed.status_code == 200
    assert all(item["id"] != cv_id for item in listed.json()["data"])
    denied = client.get(f"/api/documents/{cv_id}/file", headers=headers)
    assert denied.status_code == 403
    company_doc = client.post(
        "/api/documents",
        headers=headers,
        files={"file": ("contrat.pdf", PDF, "application/pdf")},
        data={"kind": "contract", "owner_type": "company", "owner_id": company_id},
    )
    assert company_doc.status_code == 200, company_doc.text
    doc_id = company_doc.json()["data"]["id"]
    listed = client.get("/api/documents", headers=headers)
    assert any(item["id"] == doc_id for item in listed.json()["data"])
    downloaded = client.get(f"/api/documents/{doc_id}/file", headers=headers)
    assert downloaded.status_code == 200
    deleted = client.delete(f"/api/documents/{doc_id}", headers=headers)
    assert deleted.status_code == 403


def test_admin_store_has_no_demo_password():
    store = (ROOT / "admin" / "js" / "store.js").read_text(encoding="utf-8")
    app = (ROOT / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert 'password: "talendus"' not in store
    assert "x.password === password" not in store
    assert "state.live" in store
    assert "_clearSeededLists" in store
    assert "demo-accounts" not in app
    assert "Démo locale" not in app
    assert 'value = "talendus"' not in app


def test_account_space_covers_apply_push_and_ios_download():
    account = (ROOT / "assets" / "js" / "account.js").read_text(encoding="utf-8")
    assert 'id="acc-cover"' in account
    assert "cover_note" in account
    assert "data-quick-apply" in account
    assert "notify_push" in account
    assert "coming soon" not in account.lower()
    assert "window.open(url, \"_blank\")" in account
    assert "location.assign(url)" in account
    talendus = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert "injectHoneypot" in talendus
    assert 'name="website_url"' in talendus
    auth = (ROOT / "assets" / "js" / "auth-gate.js").read_text(encoding="utf-8")
    assert "tl-auth-" in auth
    assert "history.replaceState" in auth


def test_csp_header_is_present(client):
    res = client.get("/api/health")
    csp = res.headers.get("content-security-policy") or ""
    assert "default-src 'self'" in csp
    assert "object-src 'none'" in csp


def test_site_static_hides_backend_source():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from app.main import SITE_ROOT, SiteStatic

    mini = FastAPI()
    mini.mount("/", SiteStatic(directory=str(SITE_ROOT), html=True), name="site")
    with TestClient(mini) as c:
        hidden = c.get("/backend/app/main.py")
        assert hidden.status_code == 404
        ok = c.get("/index.html")
        assert ok.status_code == 200


def test_login_requires_verified_email_when_email_enabled(client, monkeypatch):
    from app.config import get_settings

    register(client, "need-verify@example.com")
    monkeypatch.setenv("EMAIL_ENABLED", "true")
    get_settings.cache_clear()
    try:
        res = client.post("/api/auth/login", json={"email": "need-verify@example.com", "password": "Password1!"})
        assert res.status_code == 403
        assert res.json()["code"] == "EMAIL_NOT_VERIFIED"
    finally:
        monkeypatch.setenv("EMAIL_ENABLED", "false")
        get_settings.cache_clear()


def test_client_ip_uses_real_ip_then_last_forwarded_hop():
    from starlette.requests import Request

    from app.deps import client_ip

    base = {"type": "http", "method": "GET", "path": "/", "client": ("10.0.0.9", 1234)}
    real = Request({**base, "headers": [(b"x-real-ip", b"203.0.113.10"), (b"x-forwarded-for", b"1.1.1.1, 10.0.0.2")]})
    assert client_ip(real) == "203.0.113.10"
    forwarded = Request({**base, "headers": [(b"x-forwarded-for", b"1.1.1.1, 10.0.0.2")]})
    assert client_ip(forwarded) == "10.0.0.2"
    none = Request({**base, "headers": []})
    assert client_ip(none) == "10.0.0.9"


def test_public_html_has_honeypot_and_industrial_trades_first():
    candidats = (ROOT / "candidats.html").read_text(encoding="utf-8")
    contact = (ROOT / "contact.html").read_text(encoding="utf-8")
    besoin = (ROOT / "besoin-de-recrutement.html").read_text(encoding="utf-8")
    for text in (candidats, contact, besoin):
        assert 'name="website_url"' in text
    select = candidats.split('<select name="metier">', 1)[1].split("</select>", 1)[0]
    assert select.index("Cariste") < select.index("Développeur")
    assert "514 555-0199" not in candidats
    assert "tel:+15145550199" not in contact
    assert "tel:+2635585225" in contact
    assert "263 558 5225" in contact
    admin = (ROOT / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert "TLStore.isLive() ? \"\"" in admin or "TLStore.isLive() ?" in admin
    js = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert "c.demo" in js
    assert "mailto:" in js
