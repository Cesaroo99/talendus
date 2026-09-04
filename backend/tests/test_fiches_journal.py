from tests.conftest import auth_header, company_id_for, promote_admin, register


def test_prospect_dossier_helps_decide(client):
    cand = register(client, "karine.fiche@example.com", "CANDIDATE", first_name="Karine", last_name="Lavoie")
    cand_h = auth_header(cand)
    client.patch(
        "/api/candidates/me",
        headers=cand_h,
        json={
            "title": "Cariste",
            "city": "Laval",
            "availability": "2 semaines",
            "shift_preference": "Jour",
            "desired_salary_min": 22,
            "desired_salary_max": 26,
            "mobility": "Rive-Nord",
        },
    )
    emp = register(client, "metal.fiche@example.com", "EMPLOYER", first_name="Jean", last_name="Rivest")
    emp_h = auth_header(emp)
    company_id = company_id_for(client, emp)
    client.post(
        "/api/hiring-requests",
        headers=emp_h,
        json={
            "company_id": company_id,
            "title": "Soudeur MIG",
            "location": "Drummondville",
            "seats": 2,
            "shift": "Soir",
            "salary_display": "28–32 $/h",
            "notes": "Quart de soir, lecture de plans.",
        },
    )
    admin = promote_admin(client, "fiche-admin@example.com")
    admin_h = auth_header(admin)
    cands = client.get("/api/admin/prospects?side=candidate", headers=admin_h).json()["data"]
    karine = next(row for row in cands if row["email"] == "karine.fiche@example.com")
    detail = client.get(f"/api/admin/prospects/p/{karine['id']}", headers=admin_h)
    assert detail.status_code == 200, detail.text
    data = detail.json()["data"]
    dossier = data["dossier"]
    assert dossier["account"]["email"] == "karine.fiche@example.com"
    assert dossier["account"]["is_active"] is True
    assert dossier["expectations"]["availability"] == "2 semaines"
    assert dossier["expectations"]["shift"] == "Jour"
    assert dossier["expectations"]["salary_min"] == 22
    assert dossier["linked"]["candidate_id"]
    assert "stages" in data

    emps = client.get("/api/admin/prospects?side=employer", headers=admin_h).json()["data"]
    metal = next(row for row in emps if row["email"] == "metal.fiche@example.com")
    emp_detail = client.get(f"/api/admin/prospects/p/{metal['id']}", headers=admin_h)
    assert emp_detail.status_code == 200, emp_detail.text
    emp_dossier = emp_detail.json()["data"]["dossier"]
    assert emp_dossier["account"]["email"] == "metal.fiche@example.com"
    assert emp_dossier["hiring_requests"]
    assert emp_dossier["hiring_requests"][0]["title"] == "Soudeur MIG"
    assert emp_dossier["expectations"]["shift"] == "Soir"


def test_prospect_actions_and_notes_are_audited(client):
    admin = promote_admin(client, "journal-admin@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/admin/prospects",
        headers=admin_h,
        json={"side": "candidate", "email": "audit.cand@example.com", "first_name": "Nadia", "title": "Soudeuse"},
    )
    assert created.status_code == 200, created.text
    pid = created.json()["data"]["id"]
    patched = client.patch(f"/api/admin/prospects/p/{pid}", headers=admin_h, json={"stage": "qualifie"})
    assert patched.status_code == 200, patched.text
    note = client.post(f"/api/admin/prospects/p/{pid}/notes", headers=admin_h, json={"text": "Disponible le quart de jour."})
    assert note.status_code == 200, note.text
    sent = client.post(f"/api/admin/prospects/p/{pid}/send", headers=admin_h, json={"template_key": "cand_first_contact"})
    assert sent.status_code == 200, sent.text
    detail = client.get(f"/api/admin/prospects/p/{pid}", headers=admin_h).json()["data"]
    assert any(n["text"] == "Disponible le quart de jour." for n in detail["dossier"]["notes"])
    actions = {row["action"] for row in detail["dossier"]["recent_actions"]}
    assert "prospect.create" in actions
    assert "prospect.stage" in actions or "prospect.patch" in actions
    assert "prospect.send" in actions
    assert "note.create" in actions


def test_journal_lists_staff_actions_only(client):
    register(client, "talent.journal@example.com", "CANDIDATE", first_name="Hugo")
    admin = promote_admin(client, "journal-chef@example.com")
    admin_h = auth_header(admin)
    created = client.post(
        "/api/admin/users",
        headers=admin_h,
        json={
            "email": "marc.journal@example.com",
            "first_name": "Marc",
            "last_name": "Gagnon",
            "password": "Password1!",
            "role": "RECRUITER",
            "title": "Recruteur",
        },
    )
    assert created.status_code == 200, created.text
    rec_login = client.post("/api/auth/login", json={"email": "marc.journal@example.com", "password": "Password1!"})
    rec_h = auth_header(rec_login.json()["data"])
    rec_create = client.post(
        "/api/admin/prospects",
        headers=rec_h,
        json={"side": "employer", "email": "usine.journal@example.com", "company_name": "Usine Nordique", "first_name": "Luc"},
    )
    assert rec_create.status_code == 200, rec_create.text

    journal = client.get("/api/admin/audit?scope=staff", headers=admin_h)
    assert journal.status_code == 200, journal.text
    rows = journal.json()["data"]
    actions = {row["action"] for row in rows}
    assert "prospect.create" in actions
    assert "admin.user_create" in actions
    assert any(row["actor_name"] and "Marc" in row["actor_name"] for row in rows)
    assert all(row["action_label"] for row in rows)
    assert not any(row.get("actor_email") == "talent.journal@example.com" for row in rows)
    meta = journal.json()["meta"]
    assert any(a["email"] == "marc.journal@example.com" for a in meta["actors"])

    rec_journal = client.get("/api/admin/audit", headers=rec_h)
    assert rec_journal.status_code == 200, rec_journal.text
    everyone = client.get("/api/admin/audit?scope=all", headers=admin_h)
    assert everyone.status_code == 200
    everyone_actions = {row["action"] for row in everyone.json()["data"]}
    assert "account.register" in everyone_actions or "auth.login" in everyone_actions
