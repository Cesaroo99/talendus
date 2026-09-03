from conftest import auth_header, company_id_for, promote_admin, register


def _prepare_send(client, admin_h, company_id, extra=None):
    payload = {"company_id": company_id}
    if extra:
        payload.update(extra)
    created = client.post("/api/contracts", headers=admin_h, json=payload)
    assert created.status_code == 200, created.text
    body = created.json()["data"]
    cid = body["id"]
    signed = client.post(
        f"/api/contracts/{cid}/sign-talendus",
        headers=admin_h,
        json={"signer_name": "Lea Super", "accepted": True},
    )
    assert signed.status_code == 200, signed.text
    sent = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert sent.status_code == 200, sent.text
    return sent.json()["data"]


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
    assert "NEQ : 2282510496" in draft["terms"]
    assert "Soudeur" in draft["terms"]
    assert "16 %" in draft["terms"]
    assert "ARTICLE 1" in draft["terms"]
    assert "lois du Québec" in draft["terms"]
    assert "candidats présentés" in draft["terms"].lower() or "Candidat présenté" in draft["terms"]
    assert "garantie" in draft["terms"].lower()
    assert "C-1.1" in draft["terms"]
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
    assert "ARTICLE 8" in body["terms"]
    assert not body["signed"]
    assert body["client_status"] == "not_sent"
    assert body["lifecycle"] == "draft"
    cid = body["id"]

    blocked_send = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert blocked_send.status_code == 409
    assert blocked_send.json()["code"] == "TALENDUS_NOT_SIGNED"

    hidden = client.get("/api/contracts", headers=auth_header(emp))
    assert hidden.status_code == 200
    assert hidden.json()["data"] == []

    agency = client.post(
        f"/api/contracts/{cid}/sign-talendus",
        headers=admin_h,
        json={"signer_name": "Lea Super", "accepted": True},
    )
    assert agency.status_code == 200, agency.text
    assert agency.json()["data"]["talendus_signed"] is True
    assert agency.json()["data"]["lifecycle"] == "awaiting_send"
    assert agency.json()["data"]["client_status"] == "not_sent"

    sent = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert sent.status_code == 200, sent.text
    assert sent.json()["data"]["client_status"] == "received"
    assert sent.json()["data"]["sent_at"]

    listed = client.get("/api/contracts", headers=auth_header(emp))
    assert any(row["id"] == cid for row in listed.json()["data"])

    opened = client.post(f"/api/contracts/{cid}/open", headers=auth_header(emp))
    assert opened.status_code == 200, opened.text
    assert opened.json()["data"]["client_status"] == "opened"
    assert opened.json()["data"]["opened_at"]

    admin_view = client.get(f"/api/contracts/{cid}", headers=admin_h)
    assert admin_view.json()["data"]["client_status"] == "opened"

    pdf = client.get(f"/api/contracts/{cid}/pdf", headers=auth_header(emp))
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")
    assert b"inline" in pdf.headers.get("content-disposition", "").encode() or "inline" in pdf.headers.get("content-disposition", "")

    signed = client.post(
        f"/api/contracts/{cid}/sign",
        headers=auth_header(emp),
        json={"signer_name": "Marie Rivest", "accepted": True},
    )
    assert signed.status_code == 200, signed.text
    data = signed.json()["data"]
    assert data["signed"] is True
    assert data["client_signed"] is True
    assert data["talendus_signed"] is True
    assert data["client_status"] == "signed"
    assert data["lifecycle"] == "complete"
    assert data["status"] == "ACTIVE"
    assert len(data["signatures"]) == 2

    reminder = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert reminder.status_code == 409


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

    mandate = _prepare_send(client, admin_h, company_id_for(client, emp))
    still = client.post(
        f"/api/hiring-requests/{need['id']}/status",
        headers=admin_h,
        json={"status": "SOURCING"},
    )
    assert still.status_code == 409
    assert still.json()["code"] == "MANDATE_NOT_SIGNED"

    client.post(
        f"/api/contracts/{mandate['id']}/sign",
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


def test_preview_and_save_follow_chosen_dates(client):
    emp = register(client, "dates-emp@example.com", "EMPLOYER")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "dates-admin@example.com")
    admin_h = auth_header(admin)

    preview = client.get(
        f"/api/contracts/preview?company_id={company_id}&template=succes"
        "&start_date=2026-10-01&end_date=2026-12-30&role=Soudeur",
        headers=admin_h,
    )
    assert preview.status_code == 200, preview.text
    draft = preview.json()["data"]
    assert draft["start_date"] == "2026-10-01"
    assert draft["end_date"] == "2026-12-30"
    assert draft["duration_days"] == 90
    assert "Date d'ouverture du mandat : 2026-10-01" in draft["terms"]
    assert "Date de fin prévue : 2026-12-30" in draft["terms"]
    assert "pour 90 jours" in draft["terms"]

    longer = client.get(
        f"/api/contracts/preview?company_id={company_id}&template=succes"
        "&start_date=2026-01-15&end_date=2026-07-14",
        headers=admin_h,
    )
    assert longer.status_code == 200, longer.text
    body = longer.json()["data"]
    assert body["duration_days"] == 180
    assert "pour 180 jours" in body["terms"]
    assert "2026-01-15" in body["terms"]
    assert "2026-07-14" in body["terms"]

    created = client.post(
        "/api/contracts",
        headers=admin_h,
        json={
            "company_id": company_id,
            "start_date": "2026-03-01",
            "end_date": "2026-06-29",
            "role": "Cariste",
            "commission_percent": 16,
        },
    )
    assert created.status_code == 200, created.text
    saved = created.json()["data"]
    assert saved["start_date"] == "2026-03-01"
    assert saved["end_date"] == "2026-06-29"
    assert saved["duration_days"] == 120
    assert saved["can_edit"] is True
    assert "pour 120 jours" in saved["terms"]
    assert "2026-03-01" in saved["terms"]
    cid = saved["id"]

    patched = client.patch(
        f"/api/contracts/{cid}",
        headers=admin_h,
        json={"start_date": "2026-04-01", "end_date": "2026-09-28"},
    )
    assert patched.status_code == 200, patched.text
    updated = patched.json()["data"]
    assert updated["start_date"] == "2026-04-01"
    assert updated["end_date"] == "2026-09-28"
    assert updated["duration_days"] == 180
    assert "pour 180 jours" in updated["terms"]
    assert "2026-04-01" in updated["terms"]

    client.post(
        f"/api/contracts/{cid}/sign-talendus",
        headers=admin_h,
        json={"signer_name": "Lea Super", "accepted": True},
    )
    blocked = client.patch(
        f"/api/contracts/{cid}",
        headers=admin_h,
        json={"start_date": "2026-05-01"},
    )
    assert blocked.status_code == 409


def test_persist_retries_active_when_draft_is_rejected():
    from sqlalchemy.exc import DataError

    from app.models.enums import ContractStatus
    from app.services import contracts as svc

    class FakeDB:
        def __init__(self):
            self.flushes = 0
            self.added = None

        def add(self, row):
            self.added = row

        def flush(self):
            self.flushes += 1
            if self.flushes == 1:
                raise DataError("INSERT", {}, Exception("invalid input value for enum contractstatus: DRAFT"))

        def rollback(self):
            return None

        def get_bind(self):
            return None

    db = FakeDB()
    row = svc._persist_contract(
        db,
        company_id="company-1",
        mandate_type="Mandat de recrutement au succès",
        start="2026-09-03",
        end="2026-12-02",
        percent=16,
        terms="ok",
        status=ContractStatus.DRAFT,
        recruiter_id="user-1",
        template_key="succes",
        company_name="Métalco",
        document_name=None,
    )
    assert db.flushes == 2
    assert row.status == ContractStatus.ACTIVE
    assert row.company_id == "company-1"


def test_admin_ui_sends_mandate_for_signature():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    js = (root / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert "Lire le mandat" in js
    assert "Signer pour Talendus" in js
    assert "Envoyer au client" in js
    assert "previewContract" in js
    assert "updateContract" in js
    assert "sendContract" in js
    assert "signTalendus" in js
    assert "Envoyer le mandat à signer" in js
    assert "Enregistrer le brouillon" in js
    assert "Modifier le brouillon" in js
    assert "start_date=" in js
    assert "data-edit-contract" in js
    assert "Reçu" in js
    assert "Ouvert" in js
    assert "Complet" in js
    account = (root / "assets" / "js" / "account.js").read_text(encoding="utf-8")
    assert "tl-mandate-read" in account
    assert "max-height:220px" not in account
