import hashlib
import hmac

import httpx

from conftest import auth_header, promote_admin, register, staff_publish_job
from app.config import get_settings
from app.integrations.http import override_client, redact_headers
from app.integrations.inbound import ingest
from app.integrations.logging import clear_memory, recent_calls
from app.integrations.maps.google import GoogleMapsService
from app.integrations.messaging.whatsapp import WhatsAppService


def _promote_admin(client, email: str) -> dict:
    return promote_admin(client, email)


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


def _paypal_headers() -> dict[str, str]:
    return {
        "paypal-auth-algo": "SHA256withRSA",
        "paypal-cert-url": "https://api.sandbox.paypal.com/cert.pem",
        "paypal-transmission-id": "tx-1",
        "paypal-transmission-sig": "c2ln",
        "paypal-transmission-time": "2026-09-05T00:00:00Z",
    }


def test_paypal_webhook_rejects_unsigned_payload(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "paypal_webhook_id", "WH-1")
    monkeypatch.setattr(settings, "paypal_client_id", "paypal-id")
    monkeypatch.setattr(settings, "paypal_client_secret", "paypal-secret")
    missing = client.post("/api/webhooks/paypal", content=b'{"event_type":"PAYMENT.CAPTURE.COMPLETED"}')
    assert missing.status_code == 400
    assert missing.json()["code"] == "INTEGRATION_SIGNATURE_INVALID"
    bad_host = client.post(
        "/api/webhooks/paypal",
        content=b'{"event_type":"PAYMENT.CAPTURE.COMPLETED"}',
        headers={**_paypal_headers(), "paypal-cert-url": "https://evil.example/cert.pem"},
    )
    assert bad_host.status_code == 400
    assert bad_host.json()["code"] == "INTEGRATION_SIGNATURE_INVALID"


def test_paypal_webhook_requires_paypal_confirmation(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "paypal_webhook_id", "WH-1")
    monkeypatch.setattr(settings, "paypal_client_id", "paypal-id")
    monkeypatch.setattr(settings, "paypal_client_secret", "paypal-secret")
    monkeypatch.setattr(settings, "paypal_api_base_url", "https://api-m.sandbox.paypal.com")

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/v1/oauth2/token"):
            return httpx.Response(200, json={"access_token": "tok"})
        if path.endswith("/v1/notifications/verify-webhook-signature"):
            return httpx.Response(200, json={"verification_status": "FAILURE"})
        return httpx.Response(404, json={})

    with override_client(httpx.Client(transport=httpx.MockTransport(handler))):
        refused = client.post(
            "/api/webhooks/paypal",
            content=b'{"event_type":"PAYMENT.CAPTURE.COMPLETED","resource":{"id":"CAP-1"}}',
            headers=_paypal_headers(),
        )
    assert refused.status_code == 400
    assert refused.json()["code"] == "INTEGRATION_SIGNATURE_INVALID"

    def ok_handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/v1/oauth2/token"):
            return httpx.Response(200, json={"access_token": "tok"})
        if path.endswith("/v1/notifications/verify-webhook-signature"):
            return httpx.Response(200, json={"verification_status": "SUCCESS"})
        return httpx.Response(404, json={})

    with override_client(httpx.Client(transport=httpx.MockTransport(ok_handler))):
        accepted = client.post(
            "/api/webhooks/paypal",
            content=b'{"event_type":"PAYMENT.CAPTURE.COMPLETED","resource":{"id":"CAP-1"}}',
            headers=_paypal_headers(),
        )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["data"]["received"] is True


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


def test_hooks_are_noop_when_not_active():
    from app.integrations.hooks import maybe_geocode, maybe_send_whatsapp

    assert maybe_send_whatsapp(recipient="+15145550100", template="application_confirm") is None
    assert maybe_geocode("Montréal, QC") is None


def test_invoice_refund_and_paypal_unconfigured(client):
    admin = _promote_admin(client, "pay-admin@example.com")
    h = auth_header(admin)
    emp = register(client, "pay-emp@example.com", "EMPLOYER")
    company = client.get("/api/companies/me", headers=auth_header(emp)).json()["data"]
    invoice = client.post("/api/invoices", headers=h, json={"company_id": company["id"], "amount": 2500})
    inv_id = invoice.json()["data"]["id"]
    sent = client.post(f"/api/invoices/{inv_id}/send", headers=h)
    assert sent.status_code == 200, sent.text
    refund = client.post(f"/api/invoices/{inv_id}/refund", headers=h, json={})
    assert refund.status_code == 409
    assert refund.json()["code"] == "INVOICE_NOT_REFUNDABLE"
    total = sent.json()["data"].get("amount_total") or sent.json()["data"]["amount"]
    paid = client.post(
        f"/api/invoices/{inv_id}/payments",
        headers=h,
        json={"amount": total, "method": "TRANSFER"},
    )
    assert paid.status_code == 200, paid.text
    manual = client.post(f"/api/invoices/{inv_id}/refund", headers=h, json={})
    assert manual.status_code == 200, manual.text
    assert manual.json()["data"]["provider"] == "manual"
    assert manual.json()["data"]["invoice"]["status"] == "REFUNDED"
    paypal = client.post(f"/api/invoices/{inv_id}/paypal", headers=auth_header(emp))
    assert paypal.status_code == 503
    assert paypal.json()["code"] == "INTEGRATION_NOT_CONFIGURED"


def test_candidate_ai_and_contract_esign_not_configured(client):
    admin = _promote_admin(client, "ai2-admin@example.com")
    h = auth_header(admin)
    cand = register(client, "ai2-cand@example.com", first_name="Luc")
    profile = client.get("/api/candidates/me", headers=auth_header(cand)).json()["data"]
    ai = client.post(f"/api/candidates/{profile['id']}/ai", headers=h, json={"purpose": "skill_extraction"})
    assert ai.status_code == 503
    emp = register(client, "esign-emp@example.com", "EMPLOYER")
    company = client.get("/api/companies/me", headers=auth_header(emp)).json()["data"]
    from app.database import SessionLocal
    from app.models import Contract
    from app.models.enums import ContractStatus

    db = SessionLocal()
    contract = Contract(company_id=company["id"], type="Succès", terms="ok", status=ContractStatus.ACTIVE, document_name="mandat.pdf")
    db.add(contract)
    db.commit()
    cid = contract.id
    db.close()
    esign = client.post(f"/api/contracts/{cid}/esign", headers=h)
    assert esign.status_code == 503


def test_interview_reminders_without_whatsapp(client):
    from datetime import datetime, timedelta, timezone

    admin = _promote_admin(client, "rem-admin@example.com")
    h = auth_header(admin)
    cand = register(client, "rem-cand@example.com", first_name="Eve")
    cand_h = auth_header(cand)
    emp = register(client, "rem-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, title="Soudeur rappel", location="Tracy", description="Poste usine", slug="soudeur-rappel")
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]})
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]
    when = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    created = client.post(
        "/api/interviews",
        headers=h,
        json={
            "candidate_id": profile["id"],
            "application_id": applied.json()["data"]["id"],
            "scheduled_at": when,
            "location": "Visio",
        },
    )
    assert created.status_code == 200
    reminders = client.post("/api/interviews/reminders?hours=24", headers=h)
    assert reminders.status_code == 200
    assert reminders.json()["data"]["sent"] >= 1
    again = client.post("/api/interviews/reminders?hours=24", headers=h)
    assert again.json()["data"]["sent"] == 0


def test_geocode_on_company_update_when_maps_active(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "google_maps_enabled", True)
    monkeypatch.setattr(settings, "google_maps_api_key", "maps-key")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "status": "OK",
                "results": [
                    {
                        "formatted_address": "Drummondville, QC",
                        "place_id": "place-1",
                        "geometry": {"location": {"lat": 45.88, "lng": -72.48}},
                    }
                ],
            },
        )

    emp = register(client, "geo-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    company = client.get("/api/companies/me", headers=emp_h).json()["data"]
    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with override_client(http_client):
            updated = client.patch(
                f"/api/companies/{company['id']}",
                headers=emp_h,
                json={"name": company["name"], "email": "geo-emp@example.com", "city": "Drummondville", "address": "100 rue Industrielle"},
            )
    assert updated.status_code == 200
    assert updated.json()["data"]["lat"] == 45.88
    assert updated.json()["data"]["lng"] == -72.48


def test_stripe_refund_event_updates_invoice(client):
    from app.database import SessionLocal
    from app.models import Invoice, Payment
    from app.models.enums import InvoiceStatus, PaymentMethod
    from app.services.stripe_billing import apply_event

    admin = _promote_admin(client, "rewe-admin@example.com")
    emp = register(client, "rewe-emp@example.com", "EMPLOYER")
    company = client.get("/api/companies/me", headers=auth_header(emp)).json()["data"]
    invoice = client.post(
        "/api/invoices",
        headers=auth_header(admin),
        json={"company_id": company["id"], "amount": 1000},
    )
    inv_id = invoice.json()["data"]["id"]
    db = SessionLocal()
    row = db.get(Invoice, inv_id)
    row.status = InvoiceStatus.PAID
    row.stripe_payment_intent_id = "pi_test_1"
    db.add(Payment(invoice_id=inv_id, amount=1000, method=PaymentMethod.CARD, reference="pi_test_1"))
    db.commit()
    apply_event(
        db,
        {
            "type": "charge.refunded",
            "data": {
                "object": {
                    "payment_intent": "pi_test_1",
                    "amount_refunded": 100000,
                    "refunds": {"data": [{"id": "re_test_1", "amount": 100000}]},
                }
            },
        },
    )
    db.close()
    shown = client.get(f"/api/invoices/{inv_id}", headers=auth_header(admin)).json()["data"]
    assert shown["status"] == "REFUNDED"
