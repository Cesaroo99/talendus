from conftest import auth_header, company_id_for, promote_admin, register


def test_invoice_and_contract_pdf_and_internal_mail(client):
    emp = register(client, "ops-emp@example.com", "EMPLOYER", first_name="Marie")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "ops-finance@example.com")
    admin_h = auth_header(admin)
    emp_h = auth_header(emp)

    contract = client.post(
        "/api/contracts",
        headers=admin_h,
        json={
            "company_id": company_id,
            "type": "Succès",
            "start_date": "2026-08-18",
            "commission_percent": 18,
        },
    )
    assert contract.status_code == 200, contract.text
    cid = contract.json()["data"]["id"]
    agency = client.post(
        f"/api/contracts/{cid}/sign-talendus",
        headers=admin_h,
        json={"signer_name": "Lea Super", "accepted": True},
    )
    assert agency.status_code == 200, agency.text
    sent = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert sent.status_code == 200, sent.text
    assert "Talendus" in (contract.json()["data"]["terms"] or "")

    listed = client.get("/api/contracts", headers=emp_h)
    assert listed.status_code == 200
    assert any(row["id"] == cid for row in listed.json()["data"])

    pdf = client.get(f"/api/contracts/{cid}/pdf", headers=emp_h)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")
    assert len(pdf.content) > 200

    signed = client.post(
        f"/api/contracts/{cid}/sign",
        headers=emp_h,
        json={"accepted": True, "signer_name": "Marie Test"},
    )
    assert signed.status_code == 200, signed.text
    assert signed.json()["data"]["signed"] is True

    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company_id, "amount": 4200, "due_date": "2026-09-01"},
    )
    assert invoice.status_code == 200, invoice.text
    iid = invoice.json()["data"]["id"]
    sent = client.post(f"/api/invoices/{iid}/send", headers=admin_h)
    assert sent.status_code == 200
    assert sent.json()["data"]["status"] == "SENT"
    assert sent.json()["data"]["pdf_path"] == f"/api/invoices/{iid}/pdf"

    inv_pdf = client.get(f"/api/invoices/{iid}/pdf", headers=emp_h)
    assert inv_pdf.status_code == 200
    assert inv_pdf.content.startswith(b"%PDF")
    assert b"BROUILLON" not in inv_pdf.content
    assert b"A PAYER" in inv_pdf.content

    from sqlalchemy import select

    from app.database import SessionLocal
    from app.models import EmailLog

    db = SessionLocal()
    try:
        logs = list(db.scalars(select(EmailLog).where(EmailLog.to_email == "ops-emp@example.com")))
        subjects = " ".join((row.subject or "") + (row.body or "") for row in logs)
        assert "facture" in subjects.lower() or "Facture" in subjects
        assert "mandat" in subjects.lower() or "Mandat" in subjects
    finally:
        db.close()


def test_ops_tick_marks_overdue_invoices(client):
    emp = register(client, "late-emp@example.com", "EMPLOYER")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "late-admin@example.com")
    admin_h = auth_header(admin)
    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company_id, "amount": 1000, "due_date": "2020-01-01"},
    )
    iid = invoice.json()["data"]["id"]
    client.post(f"/api/invoices/{iid}/send", headers=admin_h)
    tick = client.post("/api/ops/tick", headers=admin_h)
    assert tick.status_code == 200, tick.text
    assert tick.json()["data"]["overdue"] >= 1
    shown = client.get(f"/api/invoices/{iid}", headers=admin_h)
    assert shown.json()["data"]["status"] == "OVERDUE"


def test_pdf_builder_latin_accents():
    from app.services.pdf_docs import build_pdf

    data = build_pdf("Facture été", ["Honoraires : 1 200 CAD", "Échéance : demain"])
    assert data.startswith(b"%PDF")
    assert b"%%EOF" in data
