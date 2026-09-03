from conftest import auth_header, company_id_for, promote_admin, register


def test_admin_and_app_share_jobs_hiring_and_applications(client):
    emp = register(client, "link-emp@example.com", "EMPLOYER", first_name="Marie")
    emp_h = auth_header(emp)
    need = client.post(
        "/api/hiring-requests",
        headers=emp_h,
        json={
            "title": "Soudeur-monteur",
            "location": "Drummondville",
            "sector": "Métallurgie",
            "skills": "MIG, TIG",
            "notes": "Deuxième quart, 3 ans d'expérience.",
        },
    )
    assert need.status_code == 200, need.text
    request_id = need.json()["data"]["id"]

    admin = promote_admin(client, "link-admin@example.com")
    admin_h = auth_header(admin)
    boot = client.get("/api/admin/bootstrap", headers=admin_h)
    assert boot.status_code == 200
    data = boot.json()["data"]
    assert data["live"] is True
    assert "monthly" in data
    assert any(item["id"] == request_id for item in data["hiringRequests"])

    converted = client.post(f"/api/hiring-requests/{request_id}/convert-to-job", headers=admin_h)
    assert converted.status_code == 200, converted.text
    job_id = converted.json()["data"]["job_id"]
    published = client.post(f"/api/jobs/{job_id}/publish", headers=admin_h)
    assert published.status_code == 200
    slug = published.json()["data"]["slug"]
    assert published.json()["data"]["status"] == "PUBLISHED"

    listed = client.get("/api/jobs")
    assert listed.status_code == 200
    assert any(item["id"] == job_id for item in listed.json()["data"])

    page = client.get(f"/emploi-{slug}.html")
    assert page.status_code == 200
    assert "Soudeur-monteur" in page.text
    assert f'data-job-slug="{slug}"' in page.text

    cand = register(client, "link-cand@example.com", first_name="Nadia")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job_id})
    assert applied.status_code == 200, applied.text
    application_id = applied.json()["data"]["id"]
    profile = client.get("/api/candidates/me", headers=cand_h).json()["data"]

    boot2 = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    assert any(a["id"] == application_id for a in boot2["applications"])
    found = next(c for c in boot2["candidates"] if c["id"] == profile["id"])
    assert found["applicationId"] == application_id

    note = client.post(
        "/api/recruiters/notes",
        headers=admin_h,
        json={"entity_type": "candidate", "entity_id": profile["id"], "text": "Profil à présenter après test de soudure."},
    )
    assert note.status_code == 200, note.text
    boot3 = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    assert any("test de soudure" in (n.get("text") or "") for n in boot3["notes"])

    staff_msg = client.post(
        "/api/messages",
        headers=admin_h,
        json={"recipient_id": cand["user"]["id"], "body": "Bonjour Nadia, Talendus a bien reçu votre candidature."},
    )
    assert staff_msg.status_code == 200, staff_msg.text
    inbox = client.get("/api/messages", headers=cand_h)
    assert inbox.status_code == 200
    assert any("Talendus a bien reçu" in (th.get("last_message") or "") for th in inbox.json()["data"])

    mandate = client.post(
        "/api/contracts",
        headers=admin_h,
        json={"company_id": company_id_for(client, emp), "role": "Soudeur-monteur"},
    )
    assert mandate.status_code == 200, mandate.text
    cid = mandate.json()["data"]["id"]
    agency = client.post(
        f"/api/contracts/{cid}/sign-talendus",
        headers=admin_h,
        json={"signer_name": "Lea Super", "accepted": True},
    )
    assert agency.status_code == 200, agency.text
    sent = client.post(f"/api/contracts/{cid}/send", headers=admin_h)
    assert sent.status_code == 200, sent.text
    signed = client.post(
        f"/api/contracts/{cid}/sign",
        headers=emp_h,
        json={"signer_name": "Marie Rivest", "accepted": True},
    )
    assert signed.status_code == 200, signed.text

    launched = client.post(f"/api/hiring-requests/{request_id}/status", headers=admin_h, json={"status": "JOB_PUBLISHED"})
    assert launched.status_code == 200, launched.text
    emp_need = client.get(f"/api/hiring-requests/{request_id}", headers=emp_h)
    assert emp_need.status_code == 200
    assert emp_need.json()["data"]["status"] == "JOB_PUBLISHED"
    assert emp_need.json()["data"]["status_label"] == "Recherche lancée"


def test_bootstrap_notifications_are_staff_only(client):
    admin = promote_admin(client, "notif-admin-link@example.com")
    boot = client.get("/api/admin/bootstrap", headers=auth_header(admin)).json()["data"]
    for row in boot["notifications"]:
        assert row.get("userId") == admin["user"]["id"]


def test_dynamic_job_page_404_when_not_published(client):
    admin = promote_admin(client, "draft-page@example.com")
    emp = register(client, "draft-emp@example.com", "EMPLOYER")
    job = client.post(
        "/api/jobs",
        headers=auth_header(admin),
        json={"title": "Journalier interne", "location": "Laval", "company_id": company_id_for(client, emp)},
    ).json()["data"]
    page = client.get(f"/emploi-{job['slug']}.html")
    assert page.status_code == 404
