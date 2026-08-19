from conftest import auth_header, promote_admin, register, staff_publish_job


def test_job_options_catalog_includes_shift(client):
    res = client.get("/api/jobs/options")
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    shifts = [item["value"] for item in data["shifts"]]
    assert "Quart de jour" in shifts
    assert "Quart de soir" in shifts
    schedules = [item["value"] for item in data["schedules"]]
    assert "Temps plein" in schedules
    assert data["work_modes"]
    assert data["languages"]
    assert data["experience_levels"]


def test_search_jobs_by_shift(client):
    emp = register(client, "shift-co@example.com", "EMPLOYER")
    admin = promote_admin(client, "shift-admin@example.com")
    staff_publish_job(
        client,
        emp,
        admin,
        slug="soudeur-nuit",
        title="Soudeur de nuit",
        shift="Quart de nuit",
        schedule="Temps plein",
        work_mode="Sur place",
        languages="Français",
    )
    staff_publish_job(
        client,
        emp,
        admin,
        slug="soudeur-jour",
        title="Soudeur de jour",
        shift="Quart de jour",
        schedule="Temps plein",
    )
    night = client.get("/api/jobs", params={"shift": "Quart de nuit"})
    assert night.status_code == 200, night.text
    titles = [item["title"] for item in night.json()["data"]]
    assert "Soudeur de nuit" in titles
    assert "Soudeur de jour" not in titles
    detail = client.get("/api/jobs/soudeur-nuit")
    body = detail.json()["data"]
    assert body["shift"] == "Quart de nuit"
    assert body["schedule"] == "Temps plein"
    assert body["work_mode"] == "Sur place"


def test_application_tracker_advances_with_status(client):
    admin = promote_admin(client, "track-admin@example.com")
    emp = register(client, "track-co@example.com", "EMPLOYER")
    staff_publish_job(client, emp, admin, slug="cariste-track", title="Cariste")
    cand = register(client, "track-cand@example.com", first_name="Karine")
    headers = auth_header(cand)
    created = client.post("/api/applications", headers=headers, json={"job_slug": "cariste-track"})
    assert created.status_code == 200, created.text
    app_id = created.json()["data"]["id"]
    listed = client.get("/api/applications/me", headers=headers)
    assert listed.status_code == 200, listed.text
    row = listed.json()["data"][0]
    assert row["tracker"]["status"] == "SUBMITTED"
    steps = {step["key"]: step["state"] for step in row["tracker"]["steps"]}
    assert steps["SUBMITTED"] == "current"
    assert steps["UNDER_REVIEW"] == "todo"
    assert steps["HIRED"] == "todo"
    client.post(
        f"/api/applications/{app_id}/status",
        headers=auth_header(admin),
        json={"status": "INTERVIEW"},
    )
    viewed = client.get(f"/api/applications/{app_id}", headers=headers).json()["data"]
    assert viewed["tracker"]["status"] == "INTERVIEW"
    states = {step["key"]: step["state"] for step in viewed["tracker"]["steps"]}
    assert states["SUBMITTED"] == "done"
    assert states["UNDER_REVIEW"] == "done"
    assert states["INTERVIEW"] == "current"
    assert states["OFFER_SENT"] == "todo"
    assert viewed["job"]["shift"] is not None or viewed["job"].get("location")
