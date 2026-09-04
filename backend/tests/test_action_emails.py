from pathlib import Path

from tests.conftest import auth_header, promote_admin, register, staff_publish_job

ROOT = Path(__file__).resolve().parents[2]


def _emails_to(client, admin_h, address: str) -> list[dict]:
    rows = client.get("/api/emails", headers=admin_h).json()["data"]
    return [row for row in rows if (row.get("to_email") or "").lower() == address.lower()]


def test_runtime_from_is_info():
    from app.services.email import runtime_email_config

    cfg = runtime_email_config()
    assert "info@talendus.ca" in cfg.from_addr
    assert cfg.reply_to == "info@talendus.ca"


def test_smtp_settings_persist_and_mask_password(client):
    admin = promote_admin(client, "smtp-admin@example.com")
    admin_h = auth_header(admin)
    listed = client.get("/api/admin/settings", headers=admin_h)
    assert listed.status_code == 200
    keys = {row["key"] for row in listed.json()["data"]}
    assert "smtp.from" in keys
    assert "smtp.host" in keys
    assert "smtp.password" in keys
    saved = client.patch(
        "/api/admin/settings",
        headers=admin_h,
        json={"key": "smtp.from", "value": "Talendus <info@talendus.ca>"},
    )
    assert saved.status_code == 200
    secret = client.patch(
        "/api/admin/settings",
        headers=admin_h,
        json={"key": "smtp.password", "value": "super-secret-smtp"},
    )
    assert secret.status_code == 200
    again = client.get("/api/admin/settings", headers=admin_h).json()["data"]
    pwd = next(row for row in again if row["key"] == "smtp.password")
    assert pwd["value"] == "••••••••"
    assert pwd.get("secret") is True
    keep = client.patch(
        "/api/admin/settings",
        headers=admin_h,
        json={"key": "smtp.password", "value": "••••••••"},
    )
    assert keep.status_code == 200
    from app.database import SessionLocal
    from app.models import SystemSetting
    from sqlalchemy import select

    db = SessionLocal()
    stored = db.scalar(select(SystemSetting).where(SystemSetting.key == "smtp.password"))
    assert stored is not None
    assert stored.value == "super-secret-smtp"
    db.close()


def test_smtp_test_email_is_logged(client):
    admin = promote_admin(client, "smtp-test-admin@example.com")
    admin_h = auth_header(admin)
    sent = client.post("/api/admin/settings/test-email", headers=admin_h, json={})
    assert sent.status_code == 200, sent.text
    assert sent.json()["data"]["to_email"] == "cesarmemoli1@gmail.com"
    logs = _emails_to(client, admin_h, "cesarmemoli1@gmail.com")
    assert any("test" in (row.get("subject") or "").lower() for row in logs)
    rewritten = client.post(
        "/api/admin/settings/test-email",
        headers=admin_h,
        json={"to_email": "lea.super@talendus.ca"},
    )
    assert rewritten.status_code == 200, rewritten.text
    assert rewritten.json()["data"]["to_email"] == "cesarmemoli1@gmail.com"


def test_interview_actions_email_and_thread(client):
    admin = promote_admin(client, "mail-int-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "mail-int-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="mail-int", title="Cariste")
    cand = register(client, "mail-int-cand@example.com", first_name="Hugo")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]
    created = client.post(
        "/api/interviews",
        headers=admin_h,
        json={
            "candidate_id": profile["id"],
            "application_id": applied["id"],
            "scheduled_at": "2026-08-20T10:00:00+00:00",
            "type": "VIDEO",
            "location": "Visio Talendus",
        },
    )
    assert created.status_code == 200, created.text
    interview_id = created.json()["data"]["id"]
    invites = _emails_to(client, admin_h, "mail-int-cand@example.com")
    assert any("entretien" in (row.get("subject") or "").lower() for row in invites)
    assert any("/espace.html#/interviews" in (row.get("body") or "") for row in invites)

    thread = client.get(f"/api/messages/{admin['user']['id']}", headers=cand_h)
    assert thread.status_code == 200
    assert any("Entretien planifié" in (m.get("body") or "") for m in thread.json()["data"])

    allowed = client.patch(
        f"/api/interviews/{interview_id}",
        headers=admin_h,
        json={"candidate_can_start": True},
    )
    assert allowed.status_code == 200, allowed.text
    after_start = _emails_to(client, admin_h, "mail-int-cand@example.com")
    assert any("lancer l’appel" in (row.get("subject") or "").lower() or "lancer l'appel" in (row.get("subject") or "").lower() for row in after_start)

    closed = client.post(f"/api/interviews/{interview_id}/status", headers=admin_h, json={"status": "COMPLETED"})
    assert closed.status_code == 200, closed.text
    after_close = _emails_to(client, admin_h, "mail-int-cand@example.com")
    assert any("terminé" in (row.get("subject") or "").lower() or "terminé" in (row.get("body") or "").lower() for row in after_close)
    thread2 = client.get(f"/api/messages/{admin['user']['id']}", headers=cand_h).json()["data"]
    assert any("terminé" in (m.get("body") or "").lower() for m in thread2)


def test_call_launch_emails_candidate(client):
    admin = promote_admin(client, "mail-call-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "mail-call-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="mail-call", title="Cariste")
    cand = register(client, "mail-call-cand@example.com", first_name="Lina")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]
    created = client.post(
        "/api/interviews",
        headers=admin_h,
        json={
            "candidate_id": profile["id"],
            "application_id": applied["id"],
            "scheduled_at": "2026-08-20T10:00:00+00:00",
            "type": "VIDEO",
        },
    )
    interview_id = created.json()["data"]["id"]
    joined = client.post(f"/api/calls/{interview_id}/join", headers=admin_h, json={"video": True})
    assert joined.status_code == 200, joined.text
    mails = _emails_to(client, admin_h, "mail-call-cand@example.com")
    assert any("lancé" in (row.get("subject") or "").lower() or "lancé" in (row.get("body") or "").lower() for row in mails)


def test_direct_message_sends_email(client):
    admin = promote_admin(client, "mail-msg-admin@example.com")
    admin_h = auth_header(admin)
    cand = register(client, "mail-msg-cand@example.com", first_name="Aline")
    cand_h = auth_header(cand)
    sent = client.post(
        "/api/messages",
        headers=cand_h,
        json={"recipient_id": admin["user"]["id"], "body": "Bonjour, je confirme ma disponibilité."},
    )
    assert sent.status_code == 200, sent.text
    mails = _emails_to(client, admin_h, "mail-msg-admin@example.com")
    assert any("nouveau message" in (row.get("subject") or "").lower() for row in mails)
    assert any("disponibilité" in (row.get("body") or "") for row in mails)
    assert any("espace.html#/messages" in (row.get("body") or "") or "admin/#/messages" in (row.get("body") or "") for row in mails)


def test_admin_ui_explains_smtp_steps():
    js = (ROOT / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert 'data-stab="email"' in js
    assert "Google Workspace" in js
    assert "smtp.gmail.com" in js
    assert "apppasswords" in js
    assert "info@talendus.ca" in js
    assert "adm-smtp-form" in js
    assert "Envoyer un test" in js
    assert "cesarmemoli1@gmail.com" in js
