from app.models.enums import EmailType
from app.services.email import EmailAttachment, build_email_message, runtime_email_config
from tests.conftest import auth_header, promote_admin, register, stub_smtp_delivery


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


def test_list_persists_synced_prospects(client, monkeypatch):
    stub_smtp_delivery(monkeypatch)
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


def test_list_does_not_mark_active_company_as_client(client):
    from app.database import SessionLocal
    from app.models import Company
    from app.models.enums import CompanyStatus

    admin = promote_admin(client, "crm-stage@example.com")
    admin_h = auth_header(admin)
    db = SessionLocal()
    db.add(
        Company(
            name="Usine Veille",
            email="rh@usine-veille.example",
            status=CompanyStatus.ACTIVE,
            city="Laval",
            sector="Manufacturier",
        )
    )
    db.commit()
    db.close()
    listed = client.get("/api/admin/prospects?side=employer", headers=admin_h)
    assert listed.status_code == 200, listed.text
    row = next(item for item in listed.json()["data"] if item["email"] == "rh@usine-veille.example")
    assert row["stage"] != "client"
    assert row["stage"] in {"nouveau", "a-contacter"}


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
    from tests.test_action_emails import _emails_to

    mails = _emails_to(client, admin_h, "info@talendus.ca")
    assert any("Nouveau message site" in (row.get("subject") or "") for row in mails)
    assert not any("Bienvenue chez Talendus" in (row.get("subject") or "") for row in mails)
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


def test_personalized_send_dedup_and_isolation(client, monkeypatch):
    stub_smtp_delivery(monkeypatch)
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
    assert any("Aline" in row["body"] for row in proposals.json()["data"])
    assert all(not row["subject"].startswith("Aline,") for row in proposals.json()["data"])
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
    assert all((row.get("to_email") or "").count("@") == 1 for row in to_a + to_b)
    detail = client.get(f"/api/admin/prospects/p/{a['id']}", headers=admin_h)
    assert detail.status_code == 200
    assert detail.json()["data"]["email"] == "a.talent@example.com"
    missing = client.get("/api/admin/prospects/p/inconnu", headers=admin_h)
    assert missing.status_code == 404
    assert "Prospect introuvable" in missing.text


def test_broadcast_accepts_the_full_employer_list(client, monkeypatch):
    stub_smtp_delivery(monkeypatch)
    admin = promote_admin(client, "bulk-271@talendus.ca")
    admin_h = auth_header(admin)
    created = []
    for i in range(90):
        row = client.post(
            "/api/admin/prospects",
            headers=admin_h,
            json={"side": "employer", "email": f"rh{i}@usine-bulk.example.com", "company_name": f"Usine {i}"},
        )
        assert row.status_code == 200, row.text
        created.append(row.json()["data"]["id"])
    too_many = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": created + [f"x{i}" for i in range(311)], "template_key": "emp_first_contact"},
    )
    assert too_many.status_code == 422, too_many.text
    assert too_many.json()["message"] == "Les données envoyées sont invalides."
    bulk = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": created, "template_key": "emp_first_contact"},
    )
    assert bulk.status_code == 200, bulk.text
    data = bulk.json()["data"]
    assert len(data["sent"]) == 90
    assert not data["failed"]
    logs = client.get("/api/emails?limit=200", headers=admin_h).json()["data"]
    targets = {f"rh{i}@usine-bulk.example.com" for i in range(90)}
    sent_logs = [row for row in logs if row["to_email"] in targets]
    assert len(sent_logs) == 90
    assert {row["to_email"] for row in sent_logs} == targets
    for row in sent_logs:
        assert row["to_email"].count("@") == 1
        assert "Cc:" not in (row.get("body") or "")
        others = targets - {row["to_email"]}
        assert all(other not in (row.get("body") or "") and other not in (row.get("subject") or "") for other in others)


def test_broadcast_stops_at_daily_prospect_cap(client, monkeypatch):
    stub_smtp_delivery(monkeypatch)
    monkeypatch.setattr("app.services.prospects.BULK_SEND_DAILY_MAX", 1)
    admin = promote_admin(client, "bulk-cap@example.com")
    admin_h = auth_header(admin)
    first = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "rh1@cap.example.com", "company_name": "Cap 1"},
    ).json()["data"]
    second = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "rh2@cap.example.com", "company_name": "Cap 2"},
    ).json()["data"]
    ok = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": [first["id"]], "template_key": "emp_first_contact"},
    )
    assert ok.status_code == 200, ok.text
    blocked = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": [second["id"]], "template_key": "emp_first_contact"},
    )
    assert blocked.status_code == 400
    assert blocked.json()["code"] == "BULK_DAILY_LIMIT"


def test_generic_rh_name_is_not_used_in_greeting():
    from app.models.prospect import Prospect
    from app.services.prospects import context_for, display_name, fill_tokens, get_template

    row = Prospect(
        side="employer",
        email="rh@cascades.example",
        company_name="Cascades",
        first_name="Ressources",
        last_name="humaines",
        title="Ressources humaines",
    )
    ctx = context_for(row, None)
    assert display_name(row) == "Cascades"
    assert ctx["hello"] == "Bonjour,"
    assert ctx["first_name"] == ""
    assert ctx["name"] == "Cascades"
    assert ctx["about_company"] == " au sujet de Cascades"
    assert not ctx["title_bit"]
    body = fill_tokens(get_template("emp_first_contact")["body"], ctx)
    assert body.startswith("Bonjour,")
    assert "Bonjour Ressource" not in body
    assert "Bonjour Cascades" not in body
    assert "au sujet de Cascades" in body
    assert "poste (Ressources humaines)" not in body


def test_greeting_without_person_name_and_attachment_note(client):
    from app.models.prospect import Prospect
    from app.services.prospects import append_attachment_note, attachment_note, context_for, fill_tokens, get_template

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
    assert "16 %" not in first["body"]
    assert "honoraires" not in first["body"].lower()
    assert "paiement" not in first["body"].lower()
    assert "payé" not in first["body"].lower()
    assert "étapes" not in first["body"].lower()
    assert "profils qui tiennent" not in first["body"]
    assert "comprendre le contexte" in first["body"]
    assert "tous secteurs" in first["body"]
    assert "tous les types de postes" in first["body"]
    assert "industriel" not in first["body"].lower()
    assert emp["login_link"].startswith("https://talendus.ca/espace-employeur.html#/login")
    assert "info.usine%40example.com" in emp["login_link"]
    assert emp["register_link"].startswith("https://talendus.ca/espace-employeur.html#/register")
    assert "role=EMPLOYER" in emp["register_link"]
    assert "company=Usine%20Nord" in emp["register_link"]
    early_keys = {"emp_first_contact", "emp_followup", "emp_discovery", "emp_mandate", "emp_search_start"}
    amateur = ("répondez simplement « oui »", "sans frais pour vous", "profils qui tiennent", "sans engagement")
    for row in proposals:
        blob = (row["subject"] + "\n" + row["body"]).lower()
        assert "16 %" not in row["subject"] + row["body"]
        assert "je vous enverrai" not in blob
        for phrase in amateur:
            assert phrase not in blob
        if row["key"] in early_keys:
            assert "paiement" not in blob
            assert "honoraires" not in blob
    cand = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "anonyme@example.com", "title": "Cariste"},
    ).json()["data"]
    cand_props = client.get(f"/api/admin/prospects/p/{cand['id']}/proposals", headers=admin_h).json()["data"]
    assert [row["key"] for row in cand_props][0] == "cand_first_contact"
    opener = next(row for row in cand_props if row["key"] == "cand_first_contact")
    assert opener["body"].startswith("Bonjour,")
    assert opener["subject"].startswith("Votre profil")
    assert "Cariste" in opener["subject"]
    assert "tous les secteurs" in opener["body"]
    assert "usine" not in opener["body"].lower()
    assert "industriel" not in opener["body"].lower()
    assert "sans frais" not in opener["subject"].lower()
    assert "sans frais" not in opener["body"].lower()
    assert "débourser" not in opener["body"].lower()
    assert "16 %" not in opener["body"]
    assert "honoraires" not in opener["body"].lower()
    for row in cand_props:
        blob = (row["subject"] + "\n" + row["body"]).lower()
        assert "16 %" not in row["subject"] + row["body"]
        assert "honoraires" not in blob
        assert "répondez simplement" not in blob
        assert "« oui »" not in blob
    note = attachment_note(
        [EmailAttachment(filename="mandat-usine-nord.pdf", data=b"%PDF", mime="application/pdf", kind="contract")],
        {
            "login_link": emp["login_link"],
            "register_link": emp["register_link"],
            "info": "info@talendus.ca",
        },
    )
    assert "trouverez ceci en pièce jointe" in note.lower()
    assert "mandat-usine-nord.pdf" in note
    assert "signer" in note.lower()
    assert "16 %" not in note
    assert "honoraires" not in note.lower()
    assert emp["login_link"] in note
    assert emp["register_link"] in note
    already = append_attachment_note(
        "Bonjour,\n\n" + note,
        [EmailAttachment(filename="mandat-usine-nord.pdf", data=b"%PDF", mime="application/pdf", kind="contract")],
        {"login_link": emp["login_link"], "register_link": emp["register_link"]},
    )
    assert already.count("trouverez ceci en pièce jointe") == 1
    tpl = get_template("emp_mandate")
    ctx = context_for(
        Prospect(side="employer", email="x@y.z", company_name="Usine Nord", first_name=""),
        None,
    )
    body = fill_tokens(tpl["body"], ctx)
    assert body.startswith("Bonjour,")
    assert "au sujet de Usine Nord" in body
    assert "16 %" not in body
    assert "espace-employeur.html#/login?email=x%40y.z" in ctx["login_link"]
    from app.services.email import signed_html

    html = signed_html("Bonjour,\n\nVous trouverez ceci en pièce jointe : F-2026-014.pdf\nOuvrez le fichier.")
    assert "#0b1f3a" in html
    assert "#ff6b00" in html
    assert "pièce jointe" in html.lower()
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
    assert "sendProspectBroadcast" in js
    assert "chunkProspectIds" in js
    assert "Chaque fiche reçoit son propre courriel" in js
    assert "non parti" in js
    assert "email_status" in js
    assert "Maximum 80 destinataires" not in js
    assert "cand_first_contact" not in js
    assert "Vous trouverez ceci en pièce jointe" in js
    assert "syncAttachmentNotes" in js
    assert "lire, signer ou payer" not in js
    assert '"prospects"' in store
    assert "lea.super@talendus.ca" not in js
    templates = Path(__file__).resolve().parents[2] / "backend" / "app" / "emails" / "templates"
    to_sign = (templates / "contract_to_sign.txt").read_text(encoding="utf-8")
    reminder = (templates / "contract_reminder.txt").read_text(encoding="utf-8")
    assert "Honoraires :" not in to_sign
    assert "Honoraires :" not in reminder
    assert "{{percent}}" not in to_sign
    assert "{{percent}}" not in reminder
    auth = (Path(__file__).resolve().parents[2] / "assets" / "js" / "auth-gate.js").read_text(encoding="utf-8")
    assert "prefEmail" in auth
    assert "prefCompany" in auth
    assert "hash.query.company" in auth
    assert 'autocomplete="username" value="' in auth


def test_smtp_off_does_not_mark_prospect_contacted(client):
    admin = promote_admin(client, "smtp-off-admin@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "memolicesar1@gmail.com", "company_name": "Memo Test", "stage": "a-contacter"},
    )
    assert created.status_code == 200, created.text
    pid = created.json()["data"]["id"]
    sent = client.post(
        f"/api/admin/prospects/p/{pid}/send",
        headers=admin_h,
        json={"template_key": "emp_first_contact"},
    )
    assert sent.status_code == 502, sent.text
    assert sent.json()["code"] == "SMTP_SEND_FAILED"
    assert "n’a pas quitté le serveur" in sent.json()["message"]
    detail = client.get(f"/api/admin/prospects/p/{pid}", headers=admin_h).json()["data"]
    assert detail["stage"] == "a-contacter"
    assert not detail.get("last_contacted_at")
    assert detail["sends"] == []
    logs = client.get("/api/emails", headers=admin_h).json()["data"]
    memo = [row for row in logs if row["to_email"] == "memolicesar1@gmail.com"]
    assert memo
    assert memo[0]["status"] == "FAILED"
    assert memo[0]["delivered"] is False
    assert (memo[0]["attempts"] or 0) == 0
    bulk = client.post(
        "/api/admin/prospects/broadcast",
        headers=admin_h,
        json={"ids": [pid], "template_key": "emp_first_contact"},
    )
    assert bulk.status_code == 200, bulk.text
    data = bulk.json()["data"]
    assert data["sent"] == []
    assert data["failed"]
    assert data["failed"][0]["email"] == "memolicesar1@gmail.com"
    again = client.get(f"/api/admin/prospects/p/{pid}", headers=admin_h).json()["data"]
    assert again["stage"] == "a-contacter"


def test_reconcile_resets_old_fake_sends(client, monkeypatch):
    from app.database import SessionLocal
    from app.models import EmailLog
    from app.models.enums import EmailStatus, EmailType, utcnow
    from app.models.prospect import Prospect, ProspectSend
    from app.services.email import FAKE_SENT_ERROR
    from app.services.prospects import reconcile_undelivered_prospect_mails

    admin = promote_admin(client, "reconcile-admin@example.com")
    admin_h = auth_header(admin)
    old = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "ancien@usine.example", "company_name": "Ancienne Usine", "stage": "a-contacter"},
    ).json()["data"]
    recent = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "memolicesar1@gmail.com", "company_name": "Memo", "stage": "nouveau"},
    ).json()["data"]
    kept = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "vrai@usine.example", "company_name": "Vraie Usine", "stage": "a-contacter"},
    ).json()["data"]
    later = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "employer", "email": "mandat@usine.example", "company_name": "Mandat Plus", "stage": "proposition"},
    ).json()["data"]

    db = SessionLocal()
    fake_old = EmailLog(
        to_email="ancien@usine.example",
        type=EmailType.ADMIN,
        subject="Recrutement",
        body="Bonjour",
        status=EmailStatus.SENT,
        attempts=0,
        sent_at=utcnow(),
    )
    fake_new = EmailLog(
        to_email="memolicesar1@gmail.com",
        type=EmailType.ADMIN,
        subject="Recrutement",
        body="Bonjour",
        status=EmailStatus.SENT,
        attempts=0,
        sent_at=utcnow(),
    )
    real = EmailLog(
        to_email="vrai@usine.example",
        type=EmailType.ADMIN,
        subject="Recrutement",
        body="Bonjour",
        status=EmailStatus.SENT,
        attempts=1,
        sent_at=utcnow(),
    )
    failed = EmailLog(
        to_email="mandat@usine.example",
        type=EmailType.ADMIN,
        subject="Recrutement",
        body="Bonjour",
        status=EmailStatus.FAILED,
        error="SMTP",
        attempts=1,
    )
    db.add_all([fake_old, fake_new, real, failed])
    db.flush()
    for pid, email, log, stage in (
        (old["id"], "ancien@usine.example", fake_old, "contacte"),
        (recent["id"], "memolicesar1@gmail.com", fake_new, "contacte"),
        (kept["id"], "vrai@usine.example", real, "contacte"),
        (later["id"], "mandat@usine.example", failed, "proposition"),
    ):
        row = db.get(Prospect, pid)
        row.stage = stage
        row.last_contacted_at = utcnow()
        db.add(
            ProspectSend(
                prospect_id=pid,
                template_key="emp_first_contact",
                subject="Recrutement",
                body="Bonjour",
                to_email=email,
                email_log_id=log.id,
            )
        )
    db.commit()
    stats = reconcile_undelivered_prospect_mails(db)
    db.commit()
    assert stats["fake_logs"] == 2
    assert stats["removed_sends"] == 3
    assert stats["reset_stages"] == 2
    db.refresh(fake_old)
    db.refresh(fake_new)
    db.refresh(real)
    assert fake_old.status == EmailStatus.FAILED
    assert FAKE_SENT_ERROR in (fake_old.error or "")
    assert fake_new.status == EmailStatus.FAILED
    assert real.status == EmailStatus.SENT
    assert db.get(Prospect, old["id"]).stage == "a-contacter"
    assert db.get(Prospect, recent["id"]).stage == "a-contacter"
    assert db.get(Prospect, old["id"]).last_contacted_at is None
    assert db.get(Prospect, kept["id"]).stage == "contacte"
    assert db.get(Prospect, kept["id"]).last_contacted_at is not None
    assert db.get(Prospect, later["id"]).stage == "proposition"
    db.close()

    retry = client.post(
        f"/api/admin/prospects/p/{old['id']}/send",
        headers=admin_h,
        json={"template_key": "emp_first_contact"},
    )
    assert retry.status_code == 502
    stub_smtp_delivery(monkeypatch)
    ok_send = client.post(
        f"/api/admin/prospects/p/{old['id']}/send",
        headers=admin_h,
        json={"template_key": "emp_first_contact"},
    )
    assert ok_send.status_code == 200, ok_send.text
    assert ok_send.json()["data"]["delivered"] is True
    contacted = client.get(f"/api/admin/prospects/p/{old['id']}", headers=admin_h).json()["data"]
    assert contacted["stage"] == "contacte"


def test_smtp_does_not_auto_enable_from_credentials(client):
    from app.database import SessionLocal
    from app.models import SystemSetting
    from app.services.email import runtime_email_config

    db = SessionLocal()
    db.add(SystemSetting(key="smtp.host", value="smtp.gmail.com"))
    db.add(SystemSetting(key="smtp.username", value="info@talendus.ca"))
    db.add(SystemSetting(key="smtp.password", value="abcdefghijklmnop"))
    db.commit()
    cfg = runtime_email_config(db)
    assert cfg.enabled is False
    flag = SystemSetting(key="smtp.enabled", value="oui")
    db.add(flag)
    db.commit()
    on = runtime_email_config(db)
    assert on.enabled is True
    flag.value = "non"
    db.commit()
    off = runtime_email_config(db)
    assert off.enabled is False
    db.close()
