from conftest import auth_header, company_id_for, promote_admin, register


def test_admin_prepares_filled_mandate_and_employer_signs(client):
    emp = register(client, "mandat-emp@example.com", "EMPLOYER", first_name="Marie", last_name="Rivest")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "mandat-admin@example.com")
    admin_h = auth_header(admin)

    preview = client.get(
        f"/api/contracts/preview?company_id={company_id}&template=succes&role=Soudeur",
        headers=admin_h,
    )
    assert preview.status_code == 200, preview.text
    draft = preview.json()["data"]
    assert draft["company_name"]
    assert "Talendus" in draft["terms"]
    assert "Soudeur" in draft["terms"]
    assert "16 %" in draft["terms"]
    assert draft["document_name"].endswith(".pdf")

    created = client.post(
        "/api/contracts",
        headers=admin_h,
        json={"company_id": company_id, "role": "Soudeur"},
    )
    assert created.status_code == 200, created.text
    body = created.json()["data"]
    assert body["status"] == "DRAFT"
    assert body["commission_percent"] == 16
    assert "Talendus" in body["terms"]
    assert "Soudeur" in body["terms"]
    assert not body["signed"]
    cid = body["id"]

    resent = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert resent.status_code == 200, resent.text

    signed = client.post(
        f"/api/contracts/{cid}/sign",
        headers=auth_header(emp),
        json={"signer_name": "Marie Rivest", "accepted": True},
    )
    assert signed.status_code == 200, signed.text
    assert signed.json()["data"]["signed"] is True
    assert signed.json()["data"]["status"] == "ACTIVE"


def test_search_does_not_start_before_signed_mandate(client):
    emp = register(client, "gate-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    need = client.post(
        "/api/hiring-requests",
        headers=emp_h,
        json={"title": "Cariste", "location": "Laval"},
    ).json()["data"]
    admin = promote_admin(client, "gate-admin@example.com")
    admin_h = auth_header(admin)
    blocked = client.post(
        f"/api/hiring-requests/{need['id']}/status",
        headers=admin_h,
        json={"status": "SOURCING"},
    )
    assert blocked.status_code == 409
    assert blocked.json()["code"] == "MANDATE_NOT_SIGNED"

    created = client.post(
        "/api/contracts",
        headers=admin_h,
        json={"company_id": company_id_for(client, emp)},
    ).json()["data"]
    client.post(
        f"/api/contracts/{created['id']}/sign",
        headers=emp_h,
        json={"signer_name": "Client Test", "accepted": True},
    )
    opened = client.post(
        f"/api/hiring-requests/{need['id']}/status",
        headers=admin_h,
        json={"status": "SOURCING"},
    )
    assert opened.status_code == 200, opened.text
    assert opened.json()["data"]["status"] == "SOURCING"


def test_admin_ui_sends_mandate_for_signature():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    js = (root / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert "Envoyer pour signature" in js
    assert "previewContract" in js
    assert "sendContract" in js
    assert "Envoyer le mandat à signer" in js
