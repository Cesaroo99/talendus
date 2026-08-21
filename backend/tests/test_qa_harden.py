from pathlib import Path

from conftest import auth_header, register, staff_publish_job

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


def test_finance_can_download_document_but_not_delete(client):
    cand = register(client, "docs-fin@example.com")
    upload = client.post(
        "/api/documents",
        headers=auth_header(cand),
        files={"file": ("lettre.pdf", PDF, "application/pdf")},
        data={"kind": "cover_letter"},
    )
    assert upload.status_code == 200, upload.text
    doc_id = upload.json()["data"]["id"]
    finance = _promote(client, "fin-docs@example.com", "FINANCE")
    headers = auth_header(finance)
    listed = client.get("/api/documents", headers=headers)
    assert listed.status_code == 200
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
