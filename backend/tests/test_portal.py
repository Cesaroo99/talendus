from conftest import auth_header, register

PDF = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n" + b"x" * 40


def _publish_job(client, headers, title="Soudeur", slug="soudeur-portal"):
    job = client.post("/api/jobs", headers=headers, json={"title": title, "location": "Laval", "sector": "Métallurgie", "slug": slug}).json()["data"]
    client.post(f"/api/jobs/{job['id']}/publish", headers=headers)
    return job


def test_candidate_dashboard_and_saved_job(client):
    emp = register(client, "usine-portal@example.com", "EMPLOYER")
    job = _publish_job(client, auth_header(emp), slug="soudeur-save")
    cand = register(client, "jean-portal@example.com", first_name="Jean")
    headers = auth_header(cand)

    dash = client.get("/api/candidates/me/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["first_name"] == "Jean"
    assert "completeness" in data
    assert data["stats"]["applications"] == 0

    saved = client.post(f"/api/jobs/{job['id']}/save", headers=headers)
    assert saved.status_code == 200
    listed = client.get("/api/jobs/saved", headers=headers)
    assert listed.status_code == 200
    assert any(item["id"] == job["id"] for item in listed.json()["data"])

    search = client.get("/api/jobs", headers=headers, params={"q": "Soudeur"})
    assert search.status_code == 200
    match = next(item for item in search.json()["data"] if item["id"] == job["id"])
    assert match["saved"] is True

    unsaved = client.delete(f"/api/jobs/{job['id']}/save", headers=headers)
    assert unsaved.json()["data"]["saved"] is False


def test_employer_cannot_save_job(client):
    emp = register(client, "boss-save@example.com", "EMPLOYER")
    job = _publish_job(client, auth_header(emp), slug="no-save")
    res = client.post(f"/api/jobs/{job['id']}/save", headers=auth_header(emp))
    assert res.status_code == 403


def test_application_timeline_hides_staff_comment(client):
    emp = register(client, "client-tl@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    job = _publish_job(client, emp_h, slug="operateur-tl")
    cand = register(client, "nadia-tl@example.com", first_name="Nadia")
    cand_h = auth_header(cand)
    app_row = client.post("/api/applications", headers=cand_h, json={"job_slug": "operateur-tl"}).json()["data"]
    client.post(
        f"/api/applications/{app_row['id']}/status",
        headers=emp_h,
        json={"status": "SHORTLISTED", "comment": "Note interne confidentielle"},
    )
    viewed = client.get(f"/api/applications/{app_row['id']}", headers=cand_h).json()["data"]
    assert viewed["status"] == "SHORTLISTED"
    assert "staff_notes" not in viewed
    assert all(h.get("comment") is None for h in viewed["history"])
    emp_view = client.get(f"/api/applications/{app_row['id']}", headers=emp_h).json()["data"]
    assert any(h.get("comment") == "Note interne confidentielle" for h in emp_view["history"])


def test_candidate_cannot_access_employer_dashboard(client):
    cand = register(client, "cand-dash@example.com")
    res = client.get("/api/companies/me/dashboard", headers=auth_header(cand))
    assert res.status_code == 403


def test_employer_dashboard_and_members(client):
    emp = register(client, "abc-inc@example.com", "EMPLOYER", first_name="Marie")
    headers = auth_header(emp)
    dash = client.get("/api/companies/me/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["stats"]["active_jobs"] == 0
    members = client.get("/api/companies/me/members", headers=headers)
    assert members.status_code == 200
    assert len(members.json()["data"]) >= 1
    invited = client.post(
        "/api/companies/me/members",
        headers=headers,
        json={"email": "rh-abc@example.com", "first_name": "Luc", "last_name": "Roy", "member_role": "HR", "password": "Password1!"},
    )
    assert invited.status_code == 200
    rh = client.post("/api/auth/login", json={"email": "rh-abc@example.com", "password": "Password1!"})
    assert rh.status_code == 200
    assert rh.json()["data"]["user"]["role"] == "EMPLOYER"


def test_employer_cannot_see_other_company_candidate(client):
    a = register(client, "co-a@example.com", "EMPLOYER")
    b = register(client, "co-b@example.com", "EMPLOYER")
    job = _publish_job(client, auth_header(a), slug="job-a-only")
    cand = register(client, "solo@example.com")
    client.post("/api/applications", headers=auth_header(cand), json={"job_slug": "job-a-only"})
    profile = client.get("/api/candidates/me", headers=auth_header(cand)).json()["data"]
    peek = client.get(f"/api/candidates/{profile['id']}", headers=auth_header(b))
    assert peek.status_code == 403


def test_documents_are_authenticated(client):
    cand = register(client, "docs@example.com")
    headers = auth_header(cand)
    upload = client.post(
        "/api/documents",
        headers=headers,
        files={"file": ("lettre.pdf", PDF, "application/pdf")},
        data={"kind": "cover_letter"},
    )
    assert upload.status_code == 200
    doc_id = upload.json()["data"]["id"]
    listed = client.get("/api/documents", headers=headers)
    assert any(item["id"] == doc_id for item in listed.json()["data"])
    other = register(client, "other-docs@example.com")
    forbidden = client.get(f"/api/documents/{doc_id}/file", headers=auth_header(other))
    assert forbidden.status_code == 403
    ok_file = client.get(f"/api/documents/{doc_id}/file", headers=headers)
    assert ok_file.status_code == 200


def test_profile_experience_and_resume_delete(client):
    cand = register(client, "cvdel@example.com")
    headers = auth_header(cand)
    client.patch("/api/candidates/me", headers=headers, json={"city": "Montréal", "title": "Machiniste", "skills": "CNC"})
    exp = client.post("/api/candidates/me/experiences", headers=headers, json={"company": "Usine X", "role": "Opérateur", "years": "2019-2024"})
    assert exp.status_code == 200
    exp_id = exp.json()["data"]["id"]
    client.delete(f"/api/candidates/me/experiences/{exp_id}", headers=headers)
    me = client.get("/api/candidates/me", headers=headers).json()["data"]
    assert me["experiences"] == []
    up = client.post("/api/candidates/me/resume", headers=headers, files={"file": ("cv.pdf", PDF, "application/pdf")})
    resume_id = up.json()["data"]["id"]
    deleted = client.delete(f"/api/candidates/me/resume/{resume_id}", headers=headers)
    assert deleted.status_code == 200


def test_notification_mark_read(client):
    emp = register(client, "notif-emp@example.com", "EMPLOYER")
    job = _publish_job(client, auth_header(emp), slug="notif-job")
    cand = register(client, "notif-cand@example.com")
    headers = auth_header(cand)
    client.post("/api/applications", headers=headers, json={"job_slug": "notif-job"})
    rows = client.get("/api/notifications", headers=headers).json()["data"]
    unread = [n for n in rows if not n["is_read"]]
    assert unread
    marked = client.post(f"/api/notifications/{unread[0]['id']}/read", headers=headers)
    assert marked.status_code == 200
    assert marked.json()["data"]["is_read"] is True


def test_portal_routes_exist(client):
    res = client.get("/candidate/dashboard")
    assert res.status_code in {200, 404}
    if res.status_code == 200:
        assert "noindex" in res.headers.get("x-robots-tag", "").lower()


def test_job_detail_includes_saved_flag(client):
    emp = register(client, "save-detail@example.com", "EMPLOYER")
    job = _publish_job(client, auth_header(emp), slug="soudeur-detail")
    cand = register(client, "save-detail-cand@example.com")
    headers = auth_header(cand)
    client.post(f"/api/jobs/{job['id']}/save", headers=headers)
    detail = client.get(f"/api/jobs/{job['slug']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["saved"] is True
    guest = client.get(f"/api/jobs/{job['slug']}")
    assert guest.status_code == 200
    assert guest.json()["data"].get("saved") in (None, False)


def test_application_notifies_employer_inbox_and_candidate_apps(client):
    emp = register(client, "notify-boss@example.com", "EMPLOYER")
    _publish_job(client, auth_header(emp), slug="notify-inbox")
    cand = register(client, "notify-worker@example.com")
    applied = client.post("/api/applications", headers=auth_header(cand), json={"job_slug": "notify-inbox"})
    assert applied.status_code == 200
    app_id = applied.json()["data"]["id"]
    cand_notes = client.get("/api/notifications", headers=auth_header(cand)).json()["data"]
    assert any((n.get("href") or "").endswith("#/apps") for n in cand_notes)
    emp_notes = client.get("/api/notifications", headers=auth_header(emp)).json()["data"]
    assert any("/espace-employeur.html#/inbox" in (n.get("href") or "") for n in emp_notes)
    changed = client.post(
        f"/api/applications/{app_id}/status",
        headers=auth_header(emp),
        json={"status": "SHORTLISTED"},
    )
    assert changed.status_code == 200
    after = client.get("/api/notifications", headers=auth_header(cand)).json()["data"]
    assert any(f"#/application/{app_id}" in (n.get("href") or "") for n in after)
