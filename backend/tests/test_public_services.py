from conftest import auth_header, promote_admin, register


def test_public_services_hides_unconfigured_payments(client):
    res = client.get("/api/services")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["payments"]["transfer"] is True
    assert data["payments"]["card"] is False
    assert data["payments"]["paypal"] is False
    assert data["login"]["password"] is True
    assert data["login"]["google"] is False
    assert data["messaging"]["email_sending"] is False
    assert data["messaging"]["sms"] is False
    assert data["contact"]["demo"] is True
    assert data["contact"]["phone_display"] == "514 555-0199"
    blob = str(data).lower()
    assert "sk_" not in blob
    assert "secret" not in blob


def test_public_services_uses_real_phone_when_configured(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setenv("PUBLIC_PHONE_E164", "15145550100")
    monkeypatch.setenv("PUBLIC_PHONE_DISPLAY", "514 555-0100")
    monkeypatch.setenv("PUBLIC_EMAIL", "bonjour@talendus.ca")
    get_settings.cache_clear()
    try:
        data = client.get("/api/services").json()["data"]
        assert data["contact"]["demo"] is False
        assert data["contact"]["phone_e164"] == "15145550100"
        assert data["contact"]["phone_display"] == "514 555-0100"
        assert data["contact"]["email"] == "bonjour@talendus.ca"
    finally:
        monkeypatch.delenv("PUBLIC_PHONE_E164", raising=False)
        monkeypatch.delenv("PUBLIC_PHONE_DISPLAY", raising=False)
        monkeypatch.delenv("PUBLIC_EMAIL", raising=False)
        get_settings.cache_clear()


def test_staff_services_overview_lists_next_steps(client):
    admin = promote_admin(client, "svc-admin@example.com")
    res = client.get("/api/integrations/overview", headers=auth_header(admin))
    assert res.status_code == 200
    data = res.json()["data"]
    names = {row["name"] for row in data["providers"]}
    assert "google_login" in names
    assert "stripe" in names
    assert "email" in names
    assert any(row.get("next_step") for row in data["providers"])
    ids = {item["id"] for item in data["todos"]}
    assert "phone" in ids
    assert "email" in ids
    cand = register(client, "svc-cand@example.com")
    denied = client.get("/api/integrations/overview", headers=auth_header(cand))
    assert denied.status_code == 403


def test_linkedin_posting_stays_off_without_partner_api(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setenv("LINKEDIN_CLIENT_ID", "abc")
    monkeypatch.setenv("LINKEDIN_CLIENT_SECRET", "xyz")
    monkeypatch.setenv("LINKEDIN_ENABLED", "true")
    get_settings.cache_clear()
    try:
        data = client.get("/api/integrations/linkedin").json()["data"]
        assert data["share_enabled"] is True
        assert data["posting_enabled"] is False
        assert data["configured"] is True
    finally:
        monkeypatch.delenv("LINKEDIN_CLIENT_ID", raising=False)
        monkeypatch.delenv("LINKEDIN_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("LINKEDIN_ENABLED", raising=False)
        get_settings.cache_clear()
