from tests.conftest import auth_header, promote_admin, register, staff_publish_job


def _interview(client, admin_h, cand, applied, itype="VIDEO"):
    profile = client.get("/api/candidates/me", headers=auth_header(cand)).json()["data"]
    created = client.post(
        "/api/interviews",
        headers=admin_h,
        json={
            "candidate_id": profile["id"],
            "application_id": applied["id"],
            "scheduled_at": "2026-08-20T10:00:00+00:00",
            "location": "Dans l'appli",
            "type": itype,
        },
    )
    assert created.status_code == 200, created.text
    return created.json()["data"]


def test_in_app_call_signals_between_candidate_and_staff(client):
    admin = promote_admin(client, "call-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-cariste", title="Cariste")
    cand = register(client, "call-cand@example.com", first_name="Hugo")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    interview = _interview(client, admin_h, cand, applied, "VIDEO")
    assert interview["in_app_call"] is True
    assert interview["call_video"] is True

    join = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={"video": True})
    assert join.status_code == 200, join.text
    body = join.json()["data"]
    assert body["self_id"] == cand["user"]["id"]
    assert body["ice_servers"]
    assert any("stun:" in (item.get("urls") or "") for item in body["ice_servers"])

    staff = client.post(f"/api/calls/{interview['id']}/join", headers=admin_h, json={"video": True})
    assert staff.status_code == 200, staff.text
    assert any(p["user_id"] == cand["user"]["id"] for p in staff.json()["data"]["peers"])

    offer = client.post(
        f"/api/calls/{interview['id']}/signal",
        headers=cand_h,
        json={"kind": "offer", "payload": {"type": "offer", "sdp": "v=0"}},
    )
    assert offer.status_code == 200, offer.text
    incoming = client.get(f"/api/calls/{interview['id']}/signals", headers=admin_h)
    assert incoming.status_code == 200, incoming.text
    kinds = [row["kind"] for row in incoming.json()["data"]["signals"]]
    assert "offer" in kinds
    last_id = incoming.json()["data"]["signals"][-1]["id"]
    empty = client.get(f"/api/calls/{interview['id']}/signals?after={last_id}", headers=admin_h)
    assert empty.json()["data"]["signals"] == []

    outsider = register(client, "call-out@example.com")
    blocked = client.post(f"/api/calls/{interview['id']}/join", headers=auth_header(outsider), json={"video": True})
    assert blocked.status_code in {403, 404}

    hang = client.post(f"/api/calls/{interview['id']}/hangup", headers=cand_h)
    assert hang.status_code == 200, hang.text


def test_phone_interview_defaults_to_audio(client):
    admin = promote_admin(client, "call-phone-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-phone-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-phone", title="Cariste")
    cand = register(client, "call-phone-cand@example.com")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    interview = _interview(client, admin_h, cand, applied, "PHONE")
    assert interview["in_app_call"] is True
    assert interview["call_video"] is False
    joined = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={})
    assert joined.status_code == 200, joined.text
    assert joined.json()["data"]["video"] is False
