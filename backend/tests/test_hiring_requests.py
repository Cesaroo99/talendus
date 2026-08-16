from conftest import auth_header, company_id_for, promote_admin, register


def test_employer_cannot_create_or_publish_job(client):
    emp = register(client, "no-publish@example.com", "EMPLOYER")
    headers = auth_header(emp)
    created = client.post("/api/jobs", headers=headers, json={"title": "Soudeur", "location": "Laval"})
    assert created.status_code == 403
    assert created.json()["code"] == "JOB_STAFF_ONLY"
    admin = promote_admin(client, "publish-admin@example.com")
    job = client.post(
        "/api/jobs",
        headers=auth_header(admin),
        json={"title": "Soudeur", "location": "Laval", "company_id": company_id_for(client, emp)},
    ).json()["data"]
    blocked = client.post(f"/api/jobs/{job['id']}/publish", headers=headers)
    assert blocked.status_code == 403
    assert blocked.json()["code"] == "JOB_STAFF_ONLY"
    dup = client.post(f"/api/jobs/{job['id']}/duplicate", headers=headers)
    assert dup.status_code == 403


def test_employer_submits_hiring_request(client):
    emp = register(client, "need@example.com", "EMPLOYER", first_name="Marie")
    headers = auth_header(emp)
    created = client.post(
        "/api/hiring-requests",
        headers=headers,
        json={
            "title": "Électromécanicien",
            "seats": 2,
            "location": "Longueuil",
            "sector": "Manufacturier",
            "contract_type": "Permanent",
            "skills": "PLC, hydraulique",
            "notes": "Quart de jour, 5 ans d'expérience.",
        },
    )
    assert created.status_code == 200, created.text
    row = created.json()["data"]
    assert row["status"] == "REQUEST_SUBMITTED"
    assert row["status_label"] == "Besoin transmis"
    listed = client.get("/api/hiring-requests", headers=headers)
    assert listed.status_code == 200
    assert any(item["id"] == row["id"] for item in listed.json()["data"])
    notifs = client.get("/api/notifications", headers=headers)
    assert any(n["type"] == "HIRING_REQUEST" for n in notifs.json()["data"])


def test_staff_converts_hiring_request_to_job(client):
    emp = register(client, "convert-emp@example.com", "EMPLOYER")
    emp_h = auth_header(emp)
    need = client.post(
        "/api/hiring-requests",
        headers=emp_h,
        json={"title": "Machiniste CNC", "location": "Laval", "skills": "Fanuc"},
    ).json()["data"]
    admin = promote_admin(client, "convert-admin@example.com")
    admin_h = auth_header(admin)
    converted = client.post(f"/api/hiring-requests/{need['id']}/convert-to-job", headers=admin_h)
    assert converted.status_code == 200, converted.text
    body = converted.json()["data"]
    assert body["status"] == "JOB_BEING_PREPARED"
    assert body["job_id"]
    employer_publish = client.post(f"/api/jobs/{body['job_id']}/publish", headers=emp_h)
    assert employer_publish.status_code == 403
    published = client.post(f"/api/jobs/{body['job_id']}/publish", headers=admin_h)
    assert published.status_code == 200
    assert published.json()["data"]["status"] == "PUBLISHED"
    status = client.post(
        f"/api/hiring-requests/{need['id']}/status",
        headers=admin_h,
        json={"status": "CLIENT_VALIDATION"},
    )
    assert status.status_code == 200
    feedback = client.post(
        f"/api/hiring-requests/{need['id']}/feedback",
        headers=emp_h,
        json={"action": "validate", "comment": "Brief confirmé."},
    )
    assert feedback.status_code == 200
    assert feedback.json()["data"]["status"] == "NEEDS_CONFIRMED"


def test_employer_cannot_set_hiring_status(client):
    emp = register(client, "status-emp@example.com", "EMPLOYER")
    need = client.post(
        "/api/hiring-requests",
        headers=auth_header(emp),
        json={"title": "Comptable"},
    ).json()["data"]
    blocked = client.post(
        f"/api/hiring-requests/{need['id']}/status",
        headers=auth_header(emp),
        json={"status": "JOB_PUBLISHED"},
    )
    assert blocked.status_code == 403
