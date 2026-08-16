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
