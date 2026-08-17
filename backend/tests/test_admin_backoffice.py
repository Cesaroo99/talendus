from conftest import auth_header, company_id_for, promote_admin, register


def test_staff_can_edit_candidate_pipeline_and_upload_resume(client):
    admin = promote_admin(client, "bo-admin@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/admin/candidates",
        headers=admin_h,
        json={
            "email": "karine.bo@example.com",
            "first_name": "Karine",
            "last_name": "Lavoie",
            "phone": "514 555-0142",
            "city": "Laval",
            "title": "Cariste",
            "sector": "Entrepôt",
        },
    )
    assert created.status_code == 200, created.text
    candidate_id = created.json()["data"]["id"]

    patched = client.patch(
        f"/api/admin/candidates/{candidate_id}",
        headers=admin_h,
        json={"city": "Longueuil", "title": "Cariste senior", "availability": "Immédiat", "pipeline_status": "qualifie"},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["data"]["city"] == "Longueuil"
    assert patched.json()["data"]["title"] == "Cariste senior"

    uploaded = client.post(
        f"/api/admin/candidates/{candidate_id}/resume",
        headers=admin_h,
        files={"file": ("cv-karine.pdf", b"%PDF-1.4 fake cv", "application/pdf")},
    )
    assert uploaded.status_code == 200, uploaded.text
    resume_id = uploaded.json()["data"]["id"]

    boot = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    found = next(c for c in boot["candidates"] if c["id"] == candidate_id)
    assert found["city"] == "Longueuil"
    assert found["status"] == "qualifie"
    assert any(d["id"] == resume_id and d["entityId"] == candidate_id for d in boot["documents"])

    download = client.get(f"/api/candidates/resumes/{resume_id}/file", headers=admin_h)
    assert download.status_code == 200


def test_staff_can_create_contract_and_manage_invoices(client):
    emp = register(client, "bo-emp@example.com", "EMPLOYER", first_name="Marie")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "bo-finance@example.com")
    admin_h = auth_header(admin)

    contract = client.post(
        "/api/contracts",
        headers=admin_h,
        json={
            "company_id": company_id,
            "type": "Succès",
            "start_date": "2026-08-17",
            "end_date": "2027-08-17",
            "commission_percent": 16,
            "terms": "16 % au succès, garantie 90 jours.",
        },
    )
    assert contract.status_code == 200, contract.text
    contract_id = contract.json()["data"]["id"]

    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company_id, "amount": 5000},
    )
    assert invoice.status_code == 200, invoice.text
    invoice_id = invoice.json()["data"]["id"]

    sent = client.post(f"/api/invoices/{invoice_id}/send", headers=admin_h)
    assert sent.status_code == 200, sent.text
    assert sent.json()["data"]["status"] == "SENT"

    paid = client.post(
        f"/api/invoices/{invoice_id}/payments",
        headers=admin_h,
        json={"amount": 5000, "method": "TRANSFER"},
    )
    assert paid.status_code == 200, paid.text
    assert paid.json()["data"]["status"] == "PAID"

    boot = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    assert any(c["id"] == contract_id for c in boot["contracts"])
    found = next(i for i in boot["invoices"] if i["apiId"] == invoice_id)
    assert found["status"] == "payee"
    assert found["id"].startswith("F-")
    assert any(p["invoiceId"] == found["id"] for p in boot["payments"])


def test_cms_testimonials_and_faq_persist_in_bootstrap(client):
    admin = promote_admin(client, "bo-editor@example.com")
    admin_h = auth_header(admin)
    saved = client.put(
        "/api/admin/site-content/testimonials",
        headers=admin_h,
        json={"items": [{"author": "M.L.", "role": "Directrice des opérations", "quote": "Shortlist claire dès la première semaine.", "status": "publie"}]},
    )
    assert saved.status_code == 200, saved.text
    faq = client.put(
        "/api/admin/site-content/faq",
        headers=admin_h,
        json={"items": [{"q": "Talendus est-il un job board ?", "a": "Non. Agence de placement : Talendus recrute pour l’entreprise.", "status": "publie"}]},
    )
    assert faq.status_code == 200, faq.text

    boot = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    assert any("Shortlist claire" in (t.get("quote") or "") for t in boot["testimonials"])
    assert any("job board" in (f.get("q") or "") for f in boot["faqs"])
    assert any(p["slug"] == "/emplois.html" for p in boot["pages"])

    settings = client.get("/api/admin/settings", headers=admin_h)
    assert settings.status_code == 200
    keys = {row["key"] for row in settings.json()["data"]}
    assert "agency_name" in keys
    assert not any(k.startswith("cms.") for k in keys)
