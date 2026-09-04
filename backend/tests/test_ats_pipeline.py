from conftest import auth_header, promote_admin, register, staff_publish_job


def test_pipeline_presents_then_employer_can_reply(client):
    admin = promote_admin(client, "pipe-flow-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "pipe-flow-emp@example.com", "EMPLOYER", first_name="Marie")
    emp_h = auth_header(emp)
    job = staff_publish_job(client, emp, admin, slug="pipe-flow-cariste", title="Cariste")
    cand = register(client, "pipe-flow-cand@example.com", first_name="Karine")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    app_id = applied["id"]
    steps = [row["key"] for row in applied["tracker"]["steps"]]
    assert steps == [
        "SUBMITTED",
        "UNDER_REVIEW",
        "INTERVIEW",
        "SHORTLISTED",
        "SECOND_INTERVIEW",
        "OFFER_SENT",
        "HIRED",
    ]

    client.post(f"/api/applications/{app_id}/status", headers=admin_h, json={"status": "INTERVIEW"})
    assert client.get(f"/api/applications/{app_id}", headers=emp_h).status_code == 403
    assert client.get("/api/applications", headers=emp_h).json()["data"] == []

    presented = client.post(
        f"/api/applications/{app_id}/status",
        headers=admin_h,
        json={"status": "SHORTLISTED", "comment": "Profil à montrer."},
    )
    assert presented.status_code == 200
    body = presented.json()["data"]
    assert body["presented"] is True
    assert body["status_label"] == "Présenté à l’employeur"
    assert body["next_action"]["key"] == "client"
    assert body["pipeline_stage"] == "presentation"

    inbox = client.get("/api/applications", headers=emp_h).json()["data"]
    shown = next(item for item in inbox if item["id"] == app_id)
    assert shown["candidate"]["email"] is None
    assert shown["next_action"]["key"] == "feedback"
    emp_notes = client.get("/api/notifications", headers=emp_h).json()["data"]
    assert any("présenté" in ((n.get("title") or "") + (n.get("message") or "")).lower() for n in emp_notes)

    reply = client.post(
        f"/api/applications/{app_id}/client-feedback",
        headers=emp_h,
        json={"action": "interested", "comment": "On veut la rencontrer."},
    )
    assert reply.status_code == 200, reply.text
    assert "Retour employeur" in (reply.json()["data"].get("client_feedback") or "")
    staff_notes = client.get("/api/notifications", headers=admin_h).json()["data"]
    assert any("Retour employeur" in (n.get("title") or "") for n in staff_notes)

    forbidden = client.post(
        f"/api/applications/{app_id}/status",
        headers=emp_h,
        json={"status": "HIRED"},
    )
    assert forbidden.status_code == 403


def test_withdraw_notifies_staff(client):
    admin = promote_admin(client, "pipe-wd-admin@example.com")
    emp = register(client, "pipe-wd-emp@example.com", "EMPLOYER")
    staff_publish_job(client, emp, admin, slug="pipe-wd-job", title="Soudeur")
    cand = register(client, "pipe-wd-cand@example.com", first_name="Hugo")
    cand_h = auth_header(cand)
    app_id = client.post("/api/applications", headers=cand_h, json={"job_slug": "pipe-wd-job"}).json()["data"]["id"]
    withdrawn = client.post(f"/api/applications/{app_id}/withdraw", headers=cand_h)
    assert withdrawn.status_code == 200
    staff_notes = client.get("/api/notifications", headers=auth_header(admin)).json()["data"]
    assert any("retir" in ((n.get("title") or "") + (n.get("message") or "")).lower() for n in staff_notes)
