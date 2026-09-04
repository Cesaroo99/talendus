from app.models.enums import EmailType
from app.services.email import EmailAttachment, build_email_message, runtime_email_config
from tests.conftest import auth_header, promote_admin, register


def test_register_creates_prospects(client):
    register(client, "cand-p@example.com", "CANDIDATE", first_name="Hugo")
    emp = client.post(
        "/api/auth/register",
        json={
            "email": "emp-p@example.com",
            "password": "Password1!",
            "first_name": "Jean",
            "last_name": "Test",
            "role": "EMPLOYER",
            "company_name": "Métalco",
        },
    )
    assert emp.status_code == 200, emp.text
    admin = promote_admin(client, "crm-admin@example.com")
    admin_h = auth_header(admin)
    missing_side = client.get("/api/admin/prospects", headers=admin_h)
    assert missing_side.status_code == 422
    cands = client.get("/api/admin/prospects?side=candidate", headers=admin_h)
    assert cands.status_code == 200, cands.text
    emails = {row["email"] for row in cands.json()["data"]}
    assert "cand-p@example.com" in emails
    assert "emp-p@example.com" not in emails
    hugo = next(row for row in cands.json()["data"] if row["email"] == "cand-p@example.com")
    assert hugo["first_name"] == "Hugo"
    assert hugo["source"] == "inscription"
    assert hugo["side"] == "candidate"
    emps = client.get("/api/admin/prospects?side=employer", headers=admin_h).json()["data"]
    emp_emails = {row["email"] for row in emps}
    assert "emp-p@example.com" in emp_emails
    assert "cand-p@example.com" not in emp_emails
    metal = next(row for row in emps if row["email"] == "emp-p@example.com")
    assert metal["company_name"] == "Métalco"
    assert metal["side"] == "employer"
    assert cands.json()["meta"]["side"] == "candidate"
    catalog_trap = client.get("/api/admin/prospects/catalog", headers=admin_h)
    assert catalog_trap.status_code == 200, catalog_trap.text
    assert "Prospect introuvable" not in catalog_trap.text
    catalog_keys = {row["key"] for row in catalog_trap.json()["data"]}
    assert "cand_first_contact" in catalog_keys
    templates = client.get("/api/admin/prospects/templates?side=candidate", headers=admin_h)
    assert templates.status_code == 200, templates.text
    keys = {row["key"] for row in templates.json()["data"]}
    assert "cand_first_contact" in keys
    assert "emp_first_contact" not in keys


def test_list_persists_synced_prospects(client):
    from sqlalchemy import delete

    from app.database import SessionLocal
    from app.models.prospect import Prospect, ProspectSend

    register(client, "ghost.sync@example.com", "CANDIDATE", first_name="Ghost")
    db = SessionLocal()
    db.execute(delete(ProspectSend))
    db.execute(delete(Prospect))
    db.commit()
    db.close()
    admin = promote_admin(client, "crm-sync@example.com")
    admin_h = auth_header(admin)
    listed = client.get("/api/admin/prospects?side=candidate", headers=admin_h)
    assert listed.status_code == 200, listed.text
    ghost = next(row for row in listed.json()["data"] if row["email"] == "ghost.sync@example.com")
    detail = client.get(f"/api/admin/prospects/p/{ghost['id']}", headers=admin_h)
    assert detail.status_code == 200, detail.text
    assert "Prospect introuvable" not in detail.text
    assert detail.json()["data"]["first_name"] == "Ghost"
    send = client.post(
        f"/api/admin/prospects/p/{ghost['id']}/send",
        headers=admin_h,
        json={"template_key": "cand_first_contact"},
    )
    assert send.status_code == 200, send.text
    assert send.json()["data"]["to_email"] == "ghost.sync@example.com"


def test_contact_and_manual_prospect(client):
    admin = promote_admin(client, "crm-contact@example.com")
    admin_h = auth_header(admin)
    posted = client.post(
        "/api/contact",
        json={
            "name": "Luc Tremblay",
            "email": "luc.forge@example.com",
            "company": "Forge Mauricie",
            "title": "Soudeur",
            "message": "On cherche deux soudeurs pour le quart de soir.",
        },
    )
    assert posted.status_code == 200, posted.text
    rows = client.get("/api/admin/prospects?side=employer", headers=admin_h).json()["data"]
    luc = next(row for row in rows if row["email"] == "luc.forge@example.com")
    assert luc["company_name"] == "Forge Mauricie"
    assert luc["source"] == "contact"
    created = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "karine.prospect@example.com", "first_name": "Karine", "title": "Cariste", "city": "Trois-Rivières"},
    )
    assert created.status_code == 200, created.text
    again = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "karine.prospect@example.com", "first_name": "Karine"},
    )
    assert again.status_code == 409
    filtered = client.get("/api/admin/prospects?side=candidate&city=Trois-Rivières", headers=admin_h)
    assert filtered.status_code == 200
    assert any(row["email"] == "karine.prospect@example.com" for row in filtered.json()["data"])
    assert "Trois-Rivières" in filtered.json()["meta"]["cities"]
    patched = client.patch(
        f"/api/admin/prospects/p/{created.json()['data']['id']}",
        headers=admin_h,
        json={"stage": "qualifie", "phone": "5145550101"},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["data"]["stage"] == "qualifie"
    assert patched.json()["data"]["phone"] == "5145550101"


def test_personalized_send_dedup_and_isolation(client):
    admin = promote_admin(client, "crm-mail@example.com")
    admin_h = auth_header(admin)
    a = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "a.talent@example.com", "first_name": "Aline", "title": "Cariste"},
    ).json()["data"]
    b = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "b.talent@example.com", "first_name": "Benoit", "title": "Soudeur"},
    ).json()["data"]
    emp = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "usine@example.com", "first_name": "Marc", "company_name": "Usine Nord"},
    ).json()["data"]
    proposals = client.get(f"/api/admin/prospects/p/{a['id']}/proposals", headers=admin_h)
    assert proposals.status_code == 200
    keys = {row["key"] for row in proposals.json()["data"]}
    assert "cand_first_contact" in keys
    assert "emp_first_contact" not in keys
    assert any("Aline" in row["subject"] for row in proposals.json()["data"])
    first = client.post(
        f"/api/admin/prospects/p/{a['id']}/send",
        headers=admin_h,
        json={"template_key": "cand_first_contact"},
    )
    assert first.status_code == 200, first.text
    assert first.json()["data"]["to_email"] == "a.talent@example.com"
    dup = client.post(
        f"/api/admin/prospects/p/{a['id']}/send",
        headers=admin_h,
        json={"template_key": "cand_first_contact"},
    )
    assert dup.status_code == 409
    mixed = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": [a["id"], emp["id"]], "template_key": "cand_first_contact"},
    )
    assert mixed.status_code == 400
    bulk = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": [a["id"], b["id"]], "template_key": "cand_first_contact"},
    )
    assert bulk.status_code == 200, bulk.text
    data = bulk.json()["data"]
    assert len(data["sent"]) == 1
    assert data["sent"][0]["to_email"] == "b.talent@example.com"
    assert any(row["email"] == "a.talent@example.com" for row in data["skipped"])
    logs = client.get("/api/emails", headers=admin_h).json()["data"]
    to_a = [row for row in logs if row["to_email"] == "a.talent@example.com"]
    to_b = [row for row in logs if row["to_email"] == "b.talent@example.com"]
    assert to_a and to_b
    assert all("b.talent@example.com" not in (row.get("body") or "") for row in to_a)
    assert all("a.talent@example.com" not in (row.get("body") or "") for row in to_b)
    assert any("Aline" in (row.get("body") or "") or "Aline" in (row.get("subject") or "") for row in to_a)
    assert any("Benoit" in (row.get("body") or "") or "Benoit" in (row.get("subject") or "") for row in to_b)
    detail = client.get(f"/api/admin/prospects/p/{a['id']}", headers=admin_h)
    assert detail.status_code == 200
    assert detail.json()["data"]["email"] == "a.talent@example.com"
    missing = client.get("/api/admin/prospects/p/inconnu", headers=admin_h)
    assert missing.status_code == 404
    assert "Prospect introuvable" in missing.text


def test_greeting_without_person_name_and_attachment_note(client):
    from app.models.prospect import Prospect
    from app.services.prospects import attachment_note, context_for, fill_tokens, get_template

    admin = promote_admin(client, "crm-copy@example.com")
    admin_h = auth_header(admin)
    emp = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "info.usine@example.com", "company_name": "Usine Nord"},
    ).json()["data"]
    assert not emp.get("first_name")
    proposals = client.get(f"/api/admin/prospects/p/{emp['id']}/proposals", headers=admin_h).json()["data"]
    keys = [row["key"] for row in proposals]
    assert keys == [
        "emp_first_contact",
        "emp_followup",
        "emp_discovery",
        "emp_mandate",
        "emp_search_start",
        "emp_talent_ready",
        "emp_invoice",
        "emp_reactivate",
    ]
    first = next(row for row in proposals if row["key"] == "emp_first_contact")
    assert first["subject"].startswith("Usine Nord")
    assert first["body"].startswith("Bonjour,")
    assert "Bonjour Usine Nord" not in first["body"]
    assert "honoraires" in first["body"].lower() or "16 %" in first["body"]
    cand = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "anonyme@example.com", "title": "Cariste"},
    ).json()["data"]
    cand_props = client.get(f"/api/admin/prospects/p/{cand['id']}/proposals", headers=admin_h).json()["data"]
    assert [row["key"] for row in cand_props][0] == "cand_first_contact"
    opener = next(row for row in cand_props if row["key"] == "cand_first_contact")
    assert opener["body"].startswith("Bonjour,")
    assert opener["subject"].startswith("Talendus")
    assert "sans frais" in opener["subject"]
    note = attachment_note(
        [EmailAttachment(filename="mandat-usine-nord.pdf", data=b"%PDF", mime="application/pdf", kind="contract")],
        {"employer_link": "https://talendus.ca/employeur.html", "info": "info@talendus.ca"},
    )
    assert note.startswith("Pièce jointe — mandat")
    assert "signer" in note.lower()
    assert "16 %" in note
    tpl = get_template("emp_mandate")
    ctx = context_for(
        Prospect(side="employer", email="x@y.z", company_name="Usine Nord", first_name=""),
        None,
    )
    body = fill_tokens(tpl["body"], ctx)
    assert body.startswith("Bonjour,")
    assert "au sujet de Usine Nord" in body
    from app.services.email import signed_html

    html = signed_html("Bonjour,\n\nPièce jointe — facture\nLe fichier F-2026-014.pdf est joint.")
    assert "#0b1f3a" in html
    assert "#ff6b00" in html
    assert "Pièce jointe" in html
    assert "cid:talendus-signature@talendus.ca" in html


def test_attachment_stays_on_one_message():
    cfg = runtime_email_config()
    msg = build_email_message(
        cfg,
        "seul@example.com",
        "Mandat",
        "Bonjour Aline,\n\nLe mandat est joint.",
        [EmailAttachment(filename="mandat-talendus.pdf", data=b"%PDF-1.4 test", mime="application/pdf")],
    )
    raw = msg.as_bytes()
    assert b"To: seul@example.com" in raw
    assert b"Cc:" not in raw and b"Bcc:" not in raw
    assert raw.count(b"seul@example.com") == 1
    assert b"mandat-talendus.pdf" in raw
    assert b"application/pdf" in raw


def test_admin_ui_has_prospects_module():
    from pathlib import Path

    js = (Path(__file__).resolve().parents[2] / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    store = (Path(__file__).resolve().parents[2] / "admin" / "js" / "store.js").read_text(encoding="utf-8")
    css = (Path(__file__).resolve().parents[2] / "admin" / "css" / "admin.css").read_text(encoding="utf-8")
    assert '["prospects", "Prospects"' in js
    assert "prospect-kanban" not in js
    assert "prospect-kanban" not in css
    assert "prospect-list" in js
    assert "data-pcheck" in js
    assert "Prospects candidats" in js
    assert "/admin/prospects/p/" in js
    assert "/admin/prospects/broadcast" in js
    assert "cand_first_contact" not in js
    assert '"prospects"' in store
    assert "lea.super@talendus.ca" not in js
