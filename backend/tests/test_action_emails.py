from pathlib import Path

from tests.conftest import auth_header, promote_admin, register, staff_publish_job

ROOT = Path(__file__).resolve().parents[2]


def _emails_to(client, admin_h, address: str) -> list[dict]:
    rows = client.get("/api/emails", headers=admin_h).json()["data"]
    return [row for row in rows if (row.get("to_email") or "").lower() == address.lower()]


def test_every_template_gets_talendus_signature():
    from app.services.email import (
        SIGNATURE_IMAGE,
        SIGNATURE_CID,
        TEMPLATE_DIR,
        _render,
        build_email_message,
        runtime_email_config,
        signed_html,
        signed_plain,
        strip_legacy_footer,
    )

    assert SIGNATURE_IMAGE.is_file()
    assert SIGNATURE_IMAGE.stat().st_size < 80_000
    assert SIGNATURE_IMAGE.stat().st_size > 8_000
    leftover = strip_legacy_footer(
        "Facture prête.\n\nTalendus · info@talendus.ca · 514 555-0199"
    )
    assert leftover == "Facture prête."
    assert "514 555-0199" not in leftover
    plain = signed_plain("Bonjour Hugo,\n\nVotre entretien est confirmé.")
    assert "Bonjour Hugo" in plain
    assert "263 558 5225" in plain
    assert "info@talendus.ca" in plain
    assert "talendus.ca" in plain
    html = signed_html(plain)
    assert f'cid:{SIGNATURE_CID}' in html
    assert "Bonjour Hugo" in html
    assert "#0b1f3a" in html
    assert "#ff6b00" in html
    assert "Cabinet de recrutement" in html
    assert "514 555-0199" not in html
    cfg = runtime_email_config()
    msg = build_email_message(cfg, "cesarmemoli1@gmail.com", "Test signature", plain)
    raw = msg.as_bytes()
    assert b"image/jpeg" in raw
    assert f"<{SIGNATURE_CID}>".encode() in raw
    assert b'inline; filename="talendus-signature.jpg"' in raw
    payload = msg.get_payload()
    assert len(payload) >= 2
    for path in sorted(TEMPLATE_DIR.glob("*.txt")):
        subject, body = _render(
            path.stem,
            name="Hugo",
            link="https://talendus.ca/espace.html#/messages",
            sender_name="Léa",
            preview="Disponible demain",
            document="CV",
            number="F-100",
            amount="1 200",
            due="30 sept. 2026",
        )
        signed = signed_plain(body)
        assert subject
        assert "263 558 5225" in signed, path.name
        assert "info@talendus.ca" in signed, path.name
        assert "Talendus" in signed, path.name


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
    spaced = client.patch(
        "/api/admin/settings",
        headers=admin_h,
        json={"key": "smtp.password", "value": "abcd efgh ijkl mnop"},
    )
    assert spaced.status_code == 200
    user = client.patch(
        "/api/admin/settings",
        headers=admin_h,
        json={"key": "smtp.username", "value": "Talendus <Info@Talendus.CA>"},
    )
    assert user.status_code == 200
    db = SessionLocal()
    stored = db.scalar(select(SystemSetting).where(SystemSetting.key == "smtp.password"))
    assert stored.value == "abcdefghijklmnop"
    named = db.scalar(select(SystemSetting).where(SystemSetting.key == "smtp.username"))
    assert named.value == "info@talendus.ca"
    db.close()


def test_runtime_strips_app_password_spaces(client):
    from app.database import SessionLocal
    from app.models import SystemSetting
    from app.services.email import (
        is_smtp_bad_credentials,
        normalize_smtp_password,
        normalize_smtp_username,
        runtime_email_config,
    )

    assert normalize_smtp_password("abcd efgh ijkl mnop") == "abcdefghijklmnop"
    assert normalize_smtp_username("Talendus <Info@Talendus.CA>") == "info@talendus.ca"
    assert is_smtp_bad_credentials(
        "(535, b'5.7.8 Username and Password not accepted. For more information, go to\\n5.7.8 https://support.google.com/mail/?p=BadCredentials')"
    )

    db = SessionLocal()
    db.add(SystemSetting(key="smtp.username", value="  Info@Talendus.CA "))
    db.add(SystemSetting(key="smtp.password", value="abcd efgh ijkl mnop"))
    db.commit()
    cfg = runtime_email_config(db)
    db.close()
    assert cfg.username == "info@talendus.ca"
    assert cfg.password == "abcdefghijklmnop"


def test_smtp_test_maps_gmail_535(client, monkeypatch):
    import smtplib

    admin = promote_admin(client, "smtp-535-admin@example.com")
    admin_h = auth_header(admin)
    for key, value in (
        ("smtp.enabled", "oui"),
        ("smtp.host", "smtp.gmail.com"),
        ("smtp.username", "info@talendus.ca"),
        ("smtp.password", "abcd efgh ijkl mnop"),
    ):
        saved = client.patch("/api/admin/settings", headers=admin_h, json={"key": key, "value": value})
        assert saved.status_code == 200

    def boom(*_args, **_kwargs):
        raise smtplib.SMTPAuthenticationError(
            535,
            b"5.7.8 Username and Password not accepted. For more information, go to\n5.7.8 https://support.google.com/mail/?p=BadCredentials",
        )

    monkeypatch.setattr("app.services.email._smtp_send", boom)
    sent = client.post("/api/admin/settings/test-email", headers=admin_h, json={})
    assert sent.status_code == 502, sent.text
    body = sent.json()
    assert body["code"] == "SMTP_BAD_CREDENTIALS"
    assert "535" in body["message"]
    assert "info@talendus.ca" in body["message"]
    assert "16 caractères" in body["message"]
    assert "smtp.gmail.com:587" in body["message"]


def test_smtp_test_email_is_logged(client, monkeypatch):
    from tests.conftest import stub_smtp_delivery

    admin = promote_admin(client, "smtp-test-admin@example.com")
    admin_h = auth_header(admin)
    disabled = client.post("/api/admin/settings/test-email", headers=admin_h, json={})
    assert disabled.status_code == 502, disabled.text
    assert disabled.json()["code"] == "SMTP_DISABLED"
    logs = _emails_to(client, admin_h, "smtp-test-admin@example.com")
    assert logs
    assert logs[0]["delivered"] is False
    stub_smtp_delivery(monkeypatch)
    sent = client.post("/api/admin/settings/test-email", headers=admin_h, json={})
    assert sent.status_code == 200, sent.text
    assert sent.json()["data"]["to_email"] == "smtp-test-admin@example.com"
    logs = _emails_to(client, admin_h, "smtp-test-admin@example.com")
    assert any(row.get("delivered") for row in logs)
    rewritten = client.post(
        "/api/admin/settings/test-email",
        headers=admin_h,
        json={"to_email": "lea.super@talendus.ca"},
    )
    assert rewritten.status_code == 200, rewritten.text
    assert rewritten.json()["data"]["to_email"] == "smtp-test-admin@example.com"
    other = client.post(
        "/api/admin/settings/test-email",
        headers=admin_h,
        json={"to_email": "ops-test@example.net"},
    )
    assert other.status_code == 200, other.text
    assert other.json()["data"]["to_email"] == "ops-test@example.net"


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
    assert "adm-smtp-test-to" in js
    assert "cesarmemoli1@gmail.com" not in js
    assert "EMAIL_ENABLED" in js
    assert "535" in js
    assert "16 lettres" in js
