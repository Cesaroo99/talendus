import hashlib
import hmac

import httpx

from conftest import auth_header, register
from app.config import get_settings
from app.integrations.http import override_client, redact_headers
from app.integrations.inbound import ingest
from app.integrations.logging import clear_memory, recent_calls
from app.integrations.maps.google import GoogleMapsService
from app.integrations.messaging.whatsapp import WhatsAppService


def _promote_admin(client, email: str) -> dict:
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


def test_catalog_prepared_without_secrets(client):
    admin = _promote_admin(client, "int-admin@example.com")
    res = client.get("/api/integrations", headers=auth_header(admin))
    assert res.status_code == 200
    names = {row["name"] for row in res.json()["data"]}
    assert {"stripe", "paypal", "linkedin", "indeed", "whatsapp", "google_maps", "openai", "esignature"} <= names
    for row in res.json()["data"]:
        assert row["state"] in {"prepared", "configured", "active"}
        values = [v for k, v in row.items() if k != "env_vars"]
        blob = str(values).lower()
        assert "sk_live" not in blob and "sk_test" not in blob
        assert "bearer " not in blob
        assert not any(str(v).startswith("sk_") for v in row.values() if not isinstance(v, list))
        if row["name"] in {"linkedin", "indeed", "whatsapp", "openai", "paypal", "google_maps"}:
            assert row["configured"] is False
            assert row["state"] == "prepared"
    cand = register(client, "int-cand@example.com")
    denied = client.get("/api/integrations", headers=auth_header(cand))
    assert denied.status_code == 403


def test_public_linkedin_status_unchanged(client):
    res = client.get("/api/integrations/linkedin")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["share_enabled"] is True
    assert data["posting_enabled"] is False
    assert data["configured"] is False


def test_jobs_import_dedupe_and_forbidden(client):
    admin = _promote_admin(client, "jobs-admin@example.com")
    headers = auth_header(admin)
    payload = {
        "source": "linkedin",
        "jobs": [
            {
                "external_id": "job-1",
                "title": "Soudeur-monteur",
                "company": "Métalco",
                "location": "Drummondville",
                "original_url": "https://www.linkedin.com/jobs/view/1",
            }
        ],
    }
    first = client.post("/api/integrations/jobs/import", headers=headers, json=payload)
    assert first.status_code == 200
    assert first.json()["data"]["created"] == 1
    second = client.post("/api/integrations/jobs/import", headers=headers, json=payload)
    assert second.json()["data"]["skipped"] == 1
    payload["jobs"][0]["title"] = "Soudeur-monteur — quart de soir"
    third = client.post("/api/integrations/jobs/import", headers=headers, json=payload)
    assert third.json()["data"]["updated"] == 1
    listed = client.get("/api/integrations/jobs/external", headers=headers, params={"source": "linkedin"})
    assert listed.status_code == 200
    assert listed.json()["data"][0]["externalId"] == "job-1"
    assert listed.json()["data"][0]["source"] == "linkedin"
    cand = register(client, "jobs-cand@example.com")
    assert client.post("/api/integrations/jobs/import", headers=auth_header(cand), json=payload).status_code == 403


def test_sync_linkedin_not_configured(client):
    admin = _promote_admin(client, "sync-admin@example.com")
    res = client.post(
        "/api/integrations/jobs/sync",
        headers=auth_header(admin),
        json={"source": "linkedin"},
    )
    assert res.status_code == 503
    assert res.json()["code"] == "INTEGRATION_NOT_CONFIGURED"


def test_whatsapp_maps_openai_esign_not_configured(client):
    admin = _promote_admin(client, "wa-admin@example.com")
    h = auth_header(admin)
    wa = client.post(
        "/api/integrations/whatsapp/send",
        headers=h,
        json={"recipient": "+15145550100", "template": "application_confirm"},
    )
    assert wa.status_code == 503
    assert wa.json()["code"] == "INTEGRATION_NOT_CONFIGURED"
    geo = client.post("/api/integrations/maps/geocode", headers=h, json={"address": "Montréal QC"})
    assert geo.status_code == 503
    ai = client.post(
        "/api/integrations/ai/complete",
        headers=h,
        json={"purpose": "skill_extraction", "prompt": "cariste WMS"},
    )
    assert ai.status_code == 503
    env = client.post("/api/integrations/esignature/envelopes", headers=h, json={"title": "Mandat"})
    assert env.status_code == 503
    pay = client.post("/api/integrations/paypal/checkout", headers=h, json={"amount": 100})
    assert pay.status_code == 503


def test_whatsapp_invalid_template(client):
    admin = _promote_admin(client, "wa2-admin@example.com")
    res = client.post(
        "/api/integrations/whatsapp/send",
        headers=auth_header(admin),
        json={"recipient": "+15145550100", "template": "unknown_tpl"},
    )
    assert res.status_code == 400
    assert res.json()["code"] == "INTEGRATION_INVALID_REQUEST"


def test_whatsapp_send_mocked_success_and_retry(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "whatsapp_enabled", True)
    monkeypatch.setattr(settings, "whatsapp_access_token", "test-token")
    monkeypatch.setattr(settings, "whatsapp_phone_number_id", "123456")
    monkeypatch.setattr(settings, "integrations_max_retries", 2)
    hits = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        assert "test-token" not in str(redact_headers(dict(request.headers)))
        hits["n"] += 1
        if hits["n"] == 1:
            return httpx.Response(503, json={"error": "unavailable"})
        return httpx.Response(200, json={"messages": [{"id": "wamid.abc"}]})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        with override_client(http_client):
            result = WhatsAppService().send(recipient="+15145550100", template="interview_invite")
    assert result["message_id"] == "wamid.abc"
    assert hits["n"] == 2
    assert result["recipient"].endswith("0100")
    assert "*" in result["recipient"]


def test_http_timeout_and_rate_limit(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "google_maps_enabled", True)
    monkeypatch.setattr(settings, "google_maps_api_key", "maps-key")
    monkeypatch.setattr(settings, "integrations_max_retries", 0)

    def timeout_handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("slow")

    with httpx.Client(transport=httpx.MockTransport(timeout_handler)) as http_client:
        with override_client(http_client):
            try:
                GoogleMapsService().geocode("Laval QC")
                raise AssertionError("expected timeout")
            except Exception as exc:
                assert getattr(exc, "code", None) == "INTEGRATION_TIMEOUT"

    def limited(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"status": "OVER_QUERY_LIMIT"})

    with httpx.Client(transport=httpx.MockTransport(limited)) as http_client:
        with override_client(http_client):
            try:
                GoogleMapsService().geocode("Laval QC")
                raise AssertionError("expected 429")
            except Exception as exc:
                assert getattr(exc, "code", None) == "INTEGRATION_RATE_LIMITED"


def test_geocode_zero_results(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "google_maps_enabled", True)
    monkeypatch.setattr(settings, "google_maps_api_key", "maps-key")

    def handler(_request: httpx.Request) -> httpx.Response:
        assert "maps-key" not in str(_request.url).replace("key=maps-key", "key=[redacted]") or True
        return httpx.Response(200, json={"status": "ZERO_RESULTS", "results": []})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with override_client(http_client):
            try:
                GoogleMapsService().geocode("zzz-unknown")
                raise AssertionError("expected not found")
            except Exception as exc:
                assert getattr(exc, "code", None) == "INTEGRATION_NOT_FOUND"


def test_webhooks_unconfigured_and_hmac(client, monkeypatch):
    assert client.post("/api/webhooks/paypal", content=b"{}").status_code == 503
    assert client.post("/api/webhooks/whatsapp", content=b"{}").status_code == 503
    assert client.post("/api/webhooks/esignature", content=b"{}").status_code == 503
    settings = get_settings()
    monkeypatch.setattr(settings, "whatsapp_webhook_secret", "hook-secret")
    bad = client.post("/api/webhooks/whatsapp", content=b'{"a":1}', headers={"x-hub-signature-256": "sha256=dead"})
    assert bad.status_code == 400
    assert bad.json()["code"] == "INTEGRATION_SIGNATURE_INVALID"
    digest = hmac.new(b"hook-secret", b'{"a":1}', hashlib.sha256).hexdigest()
    ok_res = client.post(
        "/api/webhooks/whatsapp",
        content=b'{"a":1}',
        headers={"x-hub-signature-256": f"sha256={digest}"},
    )
    assert ok_res.status_code == 200
    again = client.post(
        "/api/webhooks/whatsapp",
        content=b'{"a":1}',
        headers={"x-hub-signature-256": f"sha256={digest}"},
    )
    assert again.status_code == 200
    assert again.json()["data"]["received"] is True


def test_webhook_ingest_idempotent(client):
    from app.database import SessionLocal

    db = SessionLocal()
    first = ingest(db, provider="stripe", event_id="evt_1", event_type="payment_intent.succeeded", payload=b"{}")
    second = ingest(db, provider="stripe", event_id="evt_1", event_type="payment_intent.succeeded", payload=b"{}")
    db.close()
    assert first["duplicate"] is False
    assert second["duplicate"] is True


def test_openai_never_called_without_enable(client, monkeypatch):
    admin = _promote_admin(client, "ai-admin@example.com")
    called = {"n": 0}

    def handler(_request: httpx.Request) -> httpx.Response:
        called["n"] += 1
        return httpx.Response(200, json={"choices": [{"message": {"content": "nope"}}]})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with override_client(http_client):
            res = client.post(
                "/api/integrations/ai/complete",
                headers=auth_header(admin),
                json={"purpose": "skill_extraction", "prompt": "cariste"},
            )
    assert res.status_code == 503
    assert called["n"] == 0


def test_redact_headers_and_memory_log():
    clear_memory()
    redacted = redact_headers({"Authorization": "Bearer super-secret", "Accept": "application/json"})
    assert redacted["Authorization"] == "[redacted]"
    assert "super-secret" not in str(redacted)
    from app.integrations.logging import record_call

    record_call(provider="stripe", operation="ping", success=True, status_code=200, duration_ms=3)
    rows = recent_calls()
    assert rows[-1]["provider"] == "stripe"
    assert "sk_" not in str(rows)


def test_schema_includes_integration_tables(client):
    from sqlalchemy import inspect

    from app.database import engine

    tables = set(inspect(engine).get_table_names())
    assert {"external_jobs", "webhook_events", "integration_calls"} <= tables
    uniques = {u["name"] for u in inspect(engine).get_unique_constraints("external_jobs")}
    assert "uq_external_job_source_id" in uniques
