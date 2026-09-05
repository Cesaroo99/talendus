from pathlib import Path

from conftest import auth_header, company_id_for, promote_admin, register

ROOT = Path(__file__).resolve().parents[2]


def test_invoice_applies_quebec_taxes_and_pdf_mentions(client):
    emp = register(client, "qc-emp@example.com", "EMPLOYER", first_name="Marie")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "qc-fin@example.com")
    admin_h = auth_header(admin)

    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company_id, "amount": 10000},
    )
    assert invoice.status_code == 200, invoice.text
    data = invoice.json()["data"]
    assert data["tax_rate_bp"] == 14975
    assert data["amount_ht"] == 10000
    assert data["gst_amount"] == 500
    assert data["qst_amount"] == data["tax_amount"] - data["gst_amount"]
    assert data["amount_total"] == 10000 + data["tax_amount"]
    assert data["amount_total"] > 10000
    assert data["issued_at"]
    assert data["due_date"]
    assert data["due_date"] > data["issued_at"]

    pdf = client.get(f"/api/invoices/{data['id']}/pdf", headers=admin_h)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")
    hidden = client.get("/api/invoices", headers=auth_header(emp))
    assert hidden.status_code == 200
    assert hidden.json()["data"] == []
    blocked = client.get(f"/api/invoices/{data['id']}/pdf", headers=auth_header(emp))
    assert blocked.status_code in {403, 404}
    body = pdf.content
    assert b"TALENDUS" in body
    assert b"TPS" in body
    assert b"TVQ" in body
    assert b"CAD" in body
    assert b"Quebec" in body


def test_invoice_due_date_can_be_set_and_patched(client):
    emp = register(client, "due-emp@example.com", "EMPLOYER")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "due-fin@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/invoices",
        headers=admin_h,
        json={
            "company_id": company_id,
            "amount": 2500,
            "issued_at": "2026-09-01",
            "due_date": "2026-10-15",
            "notes": "Honoraires Chef de chantier",
        },
    )
    assert created.status_code == 200, created.text
    data = created.json()["data"]
    assert data["issued_at"] == "2026-09-01"
    assert data["due_date"] == "2026-10-15"
    assert data["notes"] == "Honoraires Chef de chantier"
    pdf = client.get(f"/api/invoices/{data['id']}/pdf", headers=admin_h)
    assert b"2026-10-15" in pdf.content
    assert b"Honoraires Chef de chantier" in pdf.content
    patched = client.patch(
        f"/api/invoices/{data['id']}",
        headers=admin_h,
        json={"due_date": "2026-11-01", "notes": "Placement confirme"},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["data"]["due_date"] == "2026-11-01"
    assert patched.json()["data"]["notes"] == "Placement confirme"


def test_staff_invite_and_role_levels(client):
    admin = promote_admin(client, "team-admin@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/admin/users",
        headers=admin_h,
        json={
            "email": "marc.ops@example.com",
            "first_name": "Marc",
            "last_name": "Gagnon",
            "password": "Password1!",
            "role": "RECRUITER",
            "title": "Recruteur",
        },
    )
    assert created.status_code == 200, created.text
    user_id = created.json()["data"]["id"]
    assert created.json()["data"]["role"] == "RECRUITER"

    listed = client.get("/api/admin/users", headers=admin_h)
    assert any(u["email"] == "marc.ops@example.com" for u in listed.json()["data"])

    login = client.post("/api/auth/login", json={"email": "marc.ops@example.com", "password": "Password1!"})
    assert login.status_code == 200
    rec_h = auth_header(login.json()["data"])
    denied = client.post(
        "/api/admin/users",
        headers=rec_h,
        json={
            "email": "other@example.com",
            "first_name": "A",
            "last_name": "B",
            "password": "Password1!",
            "role": "EDITOR",
        },
    )
    assert denied.status_code == 403

    patched = client.patch(
        f"/api/admin/users/{user_id}",
        headers=admin_h,
        json={"is_active": False},
    )
    assert patched.status_code == 200
    assert patched.json()["data"]["is_active"] is False

    blocked = client.post(
        "/api/admin/users",
        headers=admin_h,
        json={
            "email": "ext@example.com",
            "first_name": "Ext",
            "last_name": "User",
            "password": "Password1!",
            "role": "CANDIDATE",
        },
    )
    assert blocked.status_code == 400


def test_tracking_hit_and_admin_analytics(client):
    hit = client.post("/api/tracking/hit", json={"kind": "page_view", "path": "/emplois.html"})
    assert hit.status_code == 200, hit.text
    client.post("/api/tracking/hit", json={"kind": "contact", "path": "/contact.html"})
    client.post("/api/tracking/hit", json={"kind": "submit_application", "path": "/emploi-cariste.html"})

    admin = promote_admin(client, "an-admin@example.com")
    stats = client.get("/api/admin/analytics?period=mois", headers=auth_header(admin))
    assert stats.status_code == 200, stats.text
    data = stats.json()["data"]
    assert data["visits"] >= 1
    assert data["contacts"] >= 1
    assert data["applies"] >= 1
    assert any(p["path"] == "/emplois.html" for p in data["top_pages"])


def test_admin_shell_is_served_without_cache(client):
    for path in ("/admin", "/admin/", "/admin/index.html"):
        res = client.get(path)
        assert res.status_code == 200, path
        assert "no-store" in (res.headers.get("cache-control") or "")
        assert "Talendus Admin" in res.text
        assert "css/admin.css?v=" in res.text
        assert "js/app.js?v=" in res.text
        assert "talendus-admin-rev" in res.text


def test_admin_ui_covers_ops_gaps():
    css = (ROOT / "admin" / "css" / "admin.css").read_text(encoding="utf-8")
    assert "min-height: 0" in css
    assert "#app { height: 100%;" in css or "#app{height:100%" in css.replace(" ", "")
    assert ".inbox" in css
    assert "Source Sans 3" in css
    html = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")
    assert "fonts.googleapis.com" in html
    assert "talendus-admin-rev" in html
    assert "css/admin.css?v=" in html
    assert "js/app.js?v=" in html
    assert "js/store.js?v=" in html
    store = (ROOT / "admin" / "js" / "store.js").read_text(encoding="utf-8")
    assert "INVALID_CREDENTIALS" in store
    assert "invalid-credentials" in store
    js = (ROOT / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert "Identifiants incorrects. Vérifiez le courriel et le mot de passe." in js
    assert 'err === "invalid-credentials"' in js
    assert "viewInterviews" in js
    assert "hydrateTeam" in js
    assert "hydrateAnalytics" in js
    assert "Les entreprises et les candidats ne voient jamais" not in js
    assert "Délai moyen" not in js
    assert "dont 1 prospect" not in js
    track = (ROOT / "assets" / "js" / "tracking.js").read_text(encoding="utf-8")
    assert "/api/tracking/hit" in track


def test_invoice_retries_duplicate_number(client, monkeypatch):
    from app.services import invoices as invoices_svc

    emp = register(client, "dup-inv-emp@example.com", "EMPLOYER")
    company_id = company_id_for(client, emp)
    admin = promote_admin(client, "dup-inv-fin@example.com")
    first = client.post(
        "/api/invoices",
        headers=auth_header(admin),
        json={"company_id": company_id, "amount": 4000},
    )
    assert first.status_code == 200, first.text
    taken = first.json()["data"]["number"]
    seq = [taken, "F-2099-777"]
    monkeypatch.setattr(invoices_svc, "next_number", lambda _db: seq.pop(0) if seq else "F-2099-778")
    second = client.post(
        "/api/invoices",
        headers=auth_header(admin),
        json={"company_id": company_id, "amount": 4100},
    )
    assert second.status_code == 200, second.text
    assert second.json()["data"]["number"] == "F-2099-777"
