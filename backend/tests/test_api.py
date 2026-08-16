from conftest import auth_header, register

PDF = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n" + b"x" * 40


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_register_and_login(client):
    data = register(client, "cand@example.com")
    assert data["user"]["role"] == "CANDIDATE"
    assert data["access_token"]
    res = client.post("/api/auth/login", json={"email": "cand@example.com", "password": "Password1!"})
    assert res.status_code == 200
    assert res.json()["data"]["user"]["email"] == "cand@example.com"


def test_register_rejects_staff_role(client):
    res = client.post(
        "/api/auth/register",
        json={
            "email": "hacker@example.com",
            "password": "Password1!",
            "first_name": "No",
            "last_name": "Admin",
            "role": "ADMIN",
        },
    )
    assert res.status_code == 403
    assert res.json()["code"] == "ROLE_NOT_ALLOWED"


def test_candidate_cannot_create_job(client):
    tokens = register(client, "cand2@example.com")
    res = client.post(
        "/api/jobs",
        headers=auth_header(tokens),
        json={"title": "Cariste", "description": "Poste usine"},
    )
    assert res.status_code == 403


def test_job_draft_not_public_then_publish(client):
    emp = register(client, "boss@example.com", "EMPLOYER", first_name="Jean", last_name="Rivest")
    headers = auth_header(emp)
    created = client.post(
        "/api/jobs",
        headers=headers,
        json={
            "title": "Soudeur-monteur",
            "description": "Soudure MIG",
            "location": "Drummondville",
            "sector": "Métallurgie",
            "contract_type": "Permanent",
            "skills": "MIG, TIG",
            "salary_min": 28,
            "salary_max": 34,
        },
    )
    assert created.status_code == 200
    job = created.json()["data"]
    assert job["status"] == "DRAFT"
    public = client.get("/api/jobs")
    assert public.status_code == 200
    assert all(item["id"] != job["id"] for item in public.json()["data"])
    published = client.post(f"/api/jobs/{job['id']}/publish", headers=headers)
    assert published.status_code == 200
    assert published.json()["data"]["status"] == "PUBLISHED"
    listed = client.get("/api/jobs", params={"q": "Soudeur"})
    assert any(item["id"] == job["id"] for item in listed.json()["data"])


def test_apply_and_duplicate_and_status_and_notifications(client):
    emp = register(client, "usine@example.com", "EMPLOYER")
    emp_headers = auth_header(emp)
    job = client.post(
        "/api/jobs",
        headers=emp_headers,
        json={"title": "Cariste", "location": "Laval", "sector": "Entrepôt", "slug": "cariste-test"},
    ).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=emp_headers)

    cand = register(client, "karine@example.com", first_name="Karine", last_name="Lavoie")
    cand_headers = auth_header(cand)
    upload = client.post(
        "/api/candidates/me/resume",
        headers=cand_headers,
        files={"file": ("cv.pdf", PDF, "application/pdf")},
    )
    assert upload.status_code == 200
    resume_id = upload.json()["data"]["id"]

    applied = client.post(
        "/api/applications",
        headers=cand_headers,
        json={"job_id": job["id"], "resume_id": resume_id, "cover_note": "Disponible quart de jour."},
    )
    assert applied.status_code == 200
    application_id = applied.json()["data"]["id"]
    assert applied.json()["data"]["status"] == "SUBMITTED"

    dup = client.post("/api/applications", headers=cand_headers, json={"job_id": job["id"]})
    assert dup.status_code == 409
    assert dup.json()["code"] == "APPLICATION_ALREADY_EXISTS"

    notifs = client.get("/api/notifications", headers=cand_headers)
    assert notifs.status_code == 200
    assert len(notifs.json()["data"]) >= 1

    changed = client.post(
        f"/api/applications/{application_id}/status",
        headers=emp_headers,
        json={"status": "SHORTLISTED", "comment": "Profil solide."},
    )
    assert changed.status_code == 200
    assert changed.json()["data"]["status"] == "SHORTLISTED"
    history = changed.json()["data"]["history"]
    assert any(h["new_status"] == "SHORTLISTED" for h in history)

    notifs2 = client.get("/api/notifications", headers=cand_headers)
    titles = [n["title"] for n in notifs2.json()["data"]]
    assert any("candidature" in t.lower() or "Mise à jour" in t for t in titles)


def test_idor_application_and_candidate_profile(client):
    emp = register(client, "client@example.com", "EMPLOYER")
    emp_headers = auth_header(emp)
    job = client.post("/api/jobs", headers=emp_headers, json={"title": "Opérateur", "slug": "operateur-idor"}).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=emp_headers)

    owner = register(client, "owner@example.com", first_name="Nadia")
    other = register(client, "other@example.com", first_name="Hugo")
    owner_h = auth_header(owner)
    other_h = auth_header(other)

    app_row = client.post("/api/applications", headers=owner_h, json={"job_slug": "operateur-idor"}).json()["data"]
    forbidden = client.get(f"/api/applications/{app_row['id']}", headers=other_h)
    assert forbidden.status_code == 403
    assert forbidden.json()["code"] == "FORBIDDEN"

    me = client.get("/api/candidates/me", headers=owner_h).json()["data"]
    peek = client.get(f"/api/candidates/{me['id']}", headers=other_h)
    assert peek.status_code == 403


def test_closed_job_rejects_application(client):
    emp = register(client, "close@example.com", "EMPLOYER")
    headers = auth_header(emp)
    job = client.post("/api/jobs", headers=headers, json={"title": "Journalier", "slug": "journalier-close"}).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=headers)
    client.post(f"/api/jobs/{job['id']}/close", headers=headers)
    cand = register(client, "apply-closed@example.com")
    res = client.post("/api/applications", headers=auth_header(cand), json={"job_id": job["id"]})
    assert res.status_code == 409
    assert res.json()["code"] == "JOB_CLOSED"


def test_public_apply_and_search_filters(client):
    emp = register(client, "searchco@example.com", "EMPLOYER")
    headers = auth_header(emp)
    job = client.post(
        "/api/jobs",
        headers=headers,
        json={
            "title": "Machiniste CNC",
            "location": "Saint-Jérôme",
            "sector": "Manufacturier",
            "contract_type": "Permanent",
            "skills": "Fanuc",
            "salary_min": 30,
            "salary_max": 38,
            "slug": "machiniste-cnc-test",
        },
    ).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=headers)
    found = client.get("/api/jobs", params={"q": "CNC", "location": "Saint-Jérôme", "sector": "Manufacturier"})
    assert any(item["slug"] == "machiniste-cnc-test" for item in found.json()["data"])
    applied = client.post(
        "/api/applications/public",
        json={
            "job_slug": "machiniste-cnc-test",
            "first_name": "Éric",
            "last_name": "Nguyen",
            "email": "eric.nguyen@example.com",
            "password": "Password1!",
        },
    )
    assert applied.status_code == 200


def test_validation_error_format(client):
    res = client.post("/api/auth/login", json={"email": "not-an-email", "password": "x"})
    assert res.status_code == 422
    body = res.json()
    assert body["success"] is False
    assert body["code"] == "VALIDATION_ERROR"


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


def test_admin_bootstrap_forbidden_for_candidate(client):
    tokens = register(client, "noadmin@example.com")
    res = client.get("/api/admin/bootstrap", headers=auth_header(tokens))
    assert res.status_code == 403


def test_admin_bootstrap_and_staff_candidate(client):
    admin = _promote_admin(client, "boss-admin@example.com")
    headers = auth_header(admin)
    boot = client.get("/api/admin/bootstrap", headers=headers)
    assert boot.status_code == 200
    assert "candidates" in boot.json()["data"]
    created = client.post(
        "/api/admin/candidates",
        headers=headers,
        json={"email": "nouveau@example.com", "first_name": "Léa", "last_name": "Roy", "title": "Cariste", "city": "Laval"},
    )
    assert created.status_code == 200
    listed = client.get("/api/candidates", headers=headers)
    assert listed.status_code == 200
    emails = [c.get("email") for c in listed.json()["data"]]
    assert "nouveau@example.com" in emails
    cand = register(client, "peek@example.com")
    denied = client.get("/api/candidates", headers=auth_header(cand))
    assert denied.status_code == 403


def _publish_job(client, emp_headers, **fields):
    payload = {"title": "Cariste", "location": "Laval", "sector": "Entrepôt", "skills": "WMS, chariot", "slug": "match-cariste"}
    payload.update(fields)
    job = client.post("/api/jobs", headers=emp_headers, json=payload).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=emp_headers)
    return job


def test_matching_scores_and_job_board(client):
    emp = register(client, "matchco@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    job = _publish_job(client, emp_h)
    cand = register(client, "forklift@example.com", first_name="Karine")
    cand_h = auth_header(cand)
    client.patch(
        "/api/candidates/me",
        headers=cand_h,
        json={"city": "Laval", "sector": "Entrepôt", "skills": "WMS, chariot élévateur", "years_experience": 5},
    )
    ranked = client.get("/api/matching/jobs", headers=cand_h)
    assert ranked.status_code == 200
    items = ranked.json()["data"]
    assert items
    assert items[0]["job"]["id"] == job["id"]
    assert items[0]["score"] >= 50
    other = register(client, "office@example.com")
    denied = client.get(f"/api/matching/jobs/{job['id']}/candidates", headers=auth_header(other))
    assert denied.status_code == 403
    staff = _promote_admin(client, "match-admin@example.com")
    matches = client.get(f"/api/matching/jobs/{job['id']}/candidates", headers=auth_header(staff))
    assert matches.status_code == 200
    board = client.get("/api/job-board")
    assert board.status_code == 200
    slugs = [j["slug"] for j in board.json()["data"]["jobs"]]
    assert "match-cariste" in slugs
    linkedin = client.get("/api/integrations/linkedin")
    assert linkedin.status_code == 200
    assert linkedin.json()["data"]["share_enabled"] is True
    assert linkedin.json()["data"]["posting_enabled"] is False
    share = client.get("/api/jobs/match-cariste")
    assert "linkedin" in share.json()["data"]["share"]


def test_messaging_idor_and_staff_thread(client):
    admin = _promote_admin(client, "msg-admin@example.com")
    admin_h = auth_header(admin)
    a = register(client, "msg-a@example.com", first_name="Aline")
    b = register(client, "msg-b@example.com", first_name="Bruno")
    a_h = auth_header(a)
    b_h = auth_header(b)
    forbidden = client.post(
        "/api/messages",
        headers=a_h,
        json={"recipient_id": b["user"]["id"], "body": "Salut"},
    )
    assert forbidden.status_code == 403
    sent = client.post(
        "/api/messages",
        headers=a_h,
        json={"recipient_id": admin["user"]["id"], "body": "Bonjour, je cherche un quart de jour."},
    )
    assert sent.status_code == 200
    sneak = client.get(f"/api/messages/{a['user']['id']}", headers=b_h)
    assert sneak.status_code == 403
    admin_as_b = client.get(f"/api/messages/{admin['user']['id']}", headers=b_h)
    assert admin_as_b.status_code == 200
    assert all("quart de jour" not in m["body"] for m in admin_as_b.json()["data"])
    thread = client.get(f"/api/messages/{admin['user']['id']}", headers=a_h)
    assert thread.status_code == 200
    assert any("quart de jour" in m["body"] for m in thread.json()["data"])
    inbox = client.get("/api/messages", headers=admin_h)
    assert inbox.status_code == 200
    assert any(t["user_id"] == a["user"]["id"] for t in inbox.json()["data"])


def test_interview_invoice_contract_and_email_body(client):
    admin = _promote_admin(client, "ops-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "ops-emp@example.com", "EMPLOYER", first_name="Jean")
    emp_h = auth_header(emp)
    job = _publish_job(client, emp_h, slug="ops-cariste", title="Cariste")
    cand = register(client, "ops-cand@example.com", first_name="Hugo")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]

    denied_int = client.post(
        "/api/interviews",
        headers=cand_h,
        json={"candidate_id": profile["id"], "scheduled_at": "2026-08-20T10:00:00+00:00", "location": "Visio"},
    )
    assert denied_int.status_code == 403
    created_int = client.post(
        "/api/interviews",
        headers=admin_h,
        json={
            "candidate_id": profile["id"],
            "application_id": applied["id"],
            "scheduled_at": "2026-08-20T10:00:00+00:00",
            "location": "Visio",
            "type": "TALENDUS",
        },
    )
    assert created_int.status_code == 200
    interview_id = created_int.json()["data"]["id"]
    mine = client.get("/api/interviews", headers=cand_h)
    assert any(i["id"] == interview_id for i in mine.json()["data"])
    confirm = client.post(f"/api/interviews/{interview_id}/status", headers=cand_h, json={"status": "CONFIRMED"})
    assert confirm.status_code == 200
    assert confirm.json()["data"]["status"] == "CONFIRMED"

    company = client.get("/api/companies/me", headers=emp_h).json()["data"]
    denied_inv = client.post("/api/invoices", headers=cand_h, json={"company_id": company["id"], "amount": 5000})
    assert denied_inv.status_code == 403
    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company["id"], "amount": 5000, "due_date": "2026-09-15"},
    )
    assert invoice.status_code == 200
    inv_id = invoice.json()["data"]["id"]
    assert invoice.json()["data"]["number"].startswith("F-")
    sent = client.post(f"/api/invoices/{inv_id}/send", headers=admin_h)
    assert sent.json()["data"]["status"] == "SENT"
    paid = client.post(f"/api/invoices/{inv_id}/payments", headers=admin_h, json={"amount": 5000, "method": "TRANSFER"})
    assert paid.json()["data"]["status"] == "PAID"

    from app.database import SessionLocal
    from app.models import Contract
    from app.models.enums import ContractStatus

    db = SessionLocal()
    contract = Contract(company_id=company["id"], type="Succès", terms="16 % au succès.", status=ContractStatus.ACTIVE, document_name="mandat.pdf")
    db.add(contract)
    db.commit()
    cid = contract.id
    db.close()
    signed = client.post(
        f"/api/contracts/{cid}/sign",
        headers=emp_h,
        json={"signer_name": "Jean Rivest", "accepted": True},
    )
    assert signed.status_code == 200
    assert signed.json()["data"]["signed"] is True
    assert len(signed.json()["data"]["signature"]["document_hash"]) == 64
    again = client.post(f"/api/contracts/{cid}/sign", headers=emp_h, json={"signer_name": "Jean Rivest", "accepted": True})
    assert again.status_code == 409

    emails = client.get("/api/emails", headers=admin_h)
    assert emails.status_code == 200
    assert any(row.get("subject") for row in emails.json()["data"])


def test_schema_tables_and_constraints(client):
    from sqlalchemy import inspect

    from app.database import engine

    tables = set(inspect(engine).get_table_names())
    expected = {
        "users",
        "candidates",
        "resumes",
        "companies",
        "company_memberships",
        "job_offers",
        "applications",
        "application_status_history",
        "conversations",
        "conversation_participants",
        "messages",
        "message_attachments",
        "notifications",
        "invoices",
        "invoice_lines",
        "payments",
        "contracts",
        "recruitment_missions",
        "mission_jobs",
        "user_preferences",
        "system_settings",
        "audit_logs",
        "external_jobs",
        "webhook_events",
        "integration_calls",
    }
    assert expected.issubset(tables)
    uniques = {u["name"] for u in inspect(engine).get_unique_constraints("applications")}
    assert "uq_application_candidate_job" in uniques


def test_staff_notes_hidden_from_candidate(client):
    emp = register(client, "notes-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    job = _publish_job(client, emp_h, slug="notes-cariste", title="Cariste")
    cand = register(client, "notes-cand@example.com", first_name="Karine")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    from app.database import SessionLocal
    from app.models import Application

    db = SessionLocal()
    row = db.get(Application, applied["id"])
    row.staff_notes = "Salaire négocié — interne seulement."
    db.commit()
    db.close()
    mine = client.get(f"/api/applications/{applied['id']}", headers=cand_h).json()["data"]
    assert "staff_notes" not in mine
    inbox = client.get("/api/applications", headers=emp_h).json()["data"]
    assert any(item["id"] == applied["id"] and item.get("staff_notes") == "Salaire négocié — interne seulement." for item in inbox)


def test_suspended_account_cannot_login(client):
    data = register(client, "suspended@example.com")
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import AccountStatus

    db = SessionLocal()
    user = db.get(User, data["user"]["id"])
    user.account_status = AccountStatus.SUSPENDED
    db.commit()
    db.close()
    res = client.post("/api/auth/login", json={"email": "suspended@example.com", "password": "Password1!"})
    assert res.status_code == 403
    assert res.json()["code"] == "ACCOUNT_DISABLED"


def test_super_admin_preferences_settings_and_conversation(client):
    admin = _promote_admin(client, "schema-admin@example.com")
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import UserRole

    db = SessionLocal()
    user = db.get(User, admin["user"]["id"])
    user.role = UserRole.SUPER_ADMIN
    db.commit()
    db.close()
    res = client.post("/api/auth/login", json={"email": "schema-admin@example.com", "password": "Password1!"})
    tokens = res.json()["data"]
    headers = auth_header(tokens)
    boot = client.get("/api/admin/bootstrap", headers=headers)
    assert boot.status_code == 200
    prefs = client.get("/api/users/me/preferences", headers=headers)
    assert prefs.status_code == 200
    assert prefs.json()["data"]["locale"] == "fr-CA"
    patched = client.patch("/api/users/me/preferences", headers=headers, json={"locale": "en-CA", "notify_match": False})
    assert patched.status_code == 200
    assert patched.json()["data"]["locale"] == "en-CA"
    setting = client.patch(
        "/api/admin/settings",
        headers=headers,
        json={"key": "billing.currency", "value": "CAD", "label": "Devise"},
    )
    assert setting.status_code == 200
    listed = client.get("/api/admin/settings", headers=headers)
    assert any(row["key"] == "billing.currency" for row in listed.json()["data"])
    cand = register(client, "conv-cand@example.com", first_name="Nadia")
    sent = client.post(
        "/api/messages",
        headers=auth_header(cand),
        json={"recipient_id": tokens["user"]["id"], "body": "Bonjour, je postule en usine."},
    )
    assert sent.status_code == 200
    assert sent.json()["data"]["conversation_id"]
    emp = register(client, "member-emp@example.com", "EMPLOYER")
    company = client.get("/api/companies/me", headers=auth_header(emp))
    assert company.status_code == 200
    assert company.json()["data"]["province"] == "Québec"


def test_resume_parse_status_on_upload(client):
    cand = register(client, "parse-cv@example.com")
    upload = client.post(
        "/api/candidates/me/resume",
        headers=auth_header(cand),
        files={"file": ("cv.pdf", PDF, "application/pdf")},
    )
    assert upload.status_code == 200
    assert upload.json()["data"]["parse_status"] in {"done", "failed", "unsupported"}
    me = client.get("/api/candidates/me", headers=auth_header(cand)).json()["data"]
    assert me["resumes"]
    assert me["resumes"][0]["parse_status"] in {"done", "failed", "unsupported"}


def test_job_match_notification_on_publish(client):
    cand = register(client, "match-notify@example.com", first_name="Karine")
    cand_h = auth_header(cand)
    client.patch(
        "/api/candidates/me",
        headers=cand_h,
        json={"city": "Laval", "sector": "Entrepôt", "skills": "WMS, chariot", "years_experience": 5},
    )
    emp = register(client, "match-pub@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    job = client.post(
        "/api/jobs",
        headers=emp_h,
        json={
            "title": "Cariste",
            "location": "Laval",
            "sector": "Entrepôt",
            "skills": "WMS, chariot",
            "slug": "cariste-notify",
        },
    ).json()["data"]
    published = client.post(f"/api/jobs/{job['id']}/publish", headers=emp_h)
    assert published.status_code == 200
    notifs = client.get("/api/notifications", headers=cand_h).json()["data"]
    assert any(n["type"] == "JOB_MATCH" for n in notifs)


def test_pipeline_bootstrap_and_status_api(client):
    admin = _promote_admin(client, "pipe-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "pipe-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    company = client.get("/api/companies/me", headers=emp_h).json()["data"]
    job = _publish_job(client, emp_h, slug="pipe-cariste", title="Cariste")
    cand = register(client, "pipe-cand@example.com", first_name="Karine")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    assert applied["pipeline_stage"] == "nouveaux"
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]
    mission = client.post(
        "/api/recruiters/missions",
        headers=admin_h,
        json={"title": "Caristes Laval", "company_id": company["id"], "job_id": job["id"], "seats": 2},
    )
    assert mission.status_code == 200
    boot = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    found = next(m for m in boot["missions"] if m["id"] == mission.json()["data"]["id"])
    assert found["stageMap"][profile["id"]] == "nouveaux"
    assert any(p["applicationId"] == applied["id"] and p["stage"] == "nouveaux" for p in found["pipeline"])
    changed = client.post(
        f"/api/applications/{applied['id']}/status",
        headers=emp_h,
        json={"status": "INTERVIEW"},
    )
    assert changed.status_code == 200
    assert changed.json()["data"]["pipeline_stage"] == "entretien-talendus"
    boot2 = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    found2 = next(m for m in boot2["missions"] if m["id"] == mission.json()["data"]["id"])
    assert found2["stageMap"][profile["id"]] == "entretien-talendus"


def test_stripe_checkout_and_webhook_without_keys(client):
    admin = _promote_admin(client, "stripe-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "stripe-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    company = client.get("/api/companies/me", headers=emp_h).json()["data"]
    invoice = client.post(
        "/api/invoices",
        headers=admin_h,
        json={"company_id": company["id"], "amount": 5000, "due_date": "2026-09-15"},
    )
    assert invoice.status_code == 200
    inv_id = invoice.json()["data"]["id"]
    checkout = client.post(f"/api/invoices/{inv_id}/checkout", headers=emp_h)
    assert checkout.status_code == 503
    assert checkout.json()["code"] == "STRIPE_NOT_CONFIGURED"
    hook = client.post("/api/webhooks/stripe", content=b"{}", headers={"stripe-signature": "t=1,v1=x"})
    assert hook.status_code == 503
    assert hook.json()["code"] == "STRIPE_NOT_CONFIGURED"
    cand = register(client, "stripe-cand@example.com")
    denied = client.post(f"/api/invoices/{inv_id}/checkout", headers=auth_header(cand))
    assert denied.status_code == 403
