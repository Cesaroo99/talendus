from pathlib import Path

from tests.conftest import auth_header, promote_admin, register, staff_publish_job

ROOT = Path(__file__).resolve().parents[2]


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
    assert interview["candidate_can_start"] is False
    assert interview["can_start_call"] is True
    mine = client.get(f"/api/interviews/{interview['id']}", headers=cand_h).json()["data"]
    assert mine["can_join_call"] is False
    assert mine["call_step"] in {"confirm", "wait_host"}

    blocked = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={"video": True})
    assert blocked.status_code == 409
    assert blocked.json()["code"] == "CALL_WAITING_FOR_HOST"

    staff = client.post(f"/api/calls/{interview['id']}/join", headers=admin_h, json={"video": True})
    assert staff.status_code == 200, staff.text
    assert staff.json()["data"]["call_open"] is True
    opened = client.get(f"/api/interviews/{interview['id']}", headers=cand_h).json()["data"]
    assert opened["can_join_call"] is True
    assert opened["call_step"] == "join"

    join = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={"video": True})
    assert join.status_code == 200, join.text
    body = join.json()["data"]
    assert body["self_id"] == cand["user"]["id"]
    assert body["ice_servers"]
    assert any("stun:" in (item.get("urls") or "") for item in body["ice_servers"])

    peers = client.get(f"/api/calls/{interview['id']}/signals", headers=admin_h)
    assert peers.status_code == 200, peers.text
    assert any(p["user_id"] == cand["user"]["id"] for p in peers.json()["data"]["peers"])

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
    opened = client.post(f"/api/calls/{interview['id']}/open", headers=admin_h)
    assert opened.status_code == 200, opened.text
    waiting = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={})
    assert waiting.status_code == 409
    staff = client.post(f"/api/calls/{interview['id']}/join", headers=admin_h, json={})
    assert staff.status_code == 200, staff.text
    joined = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={})
    assert joined.status_code == 200, joined.text
    assert joined.json()["data"]["video"] is False


def test_admin_bootstrap_exposes_in_app_call(client):
    admin = promote_admin(client, "call-boot-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-boot-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-boot", title="Cariste")
    cand = register(client, "call-boot-cand@example.com")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    video = _interview(client, admin_h, cand, applied, "VIDEO")
    phone = _interview(client, admin_h, cand, applied, "PHONE")
    boot = client.get("/api/admin/bootstrap", headers=admin_h).json()["data"]
    video_row = next(i for i in boot["interviews"] if i["id"] == video["id"])
    phone_row = next(i for i in boot["interviews"] if i["id"] == phone["id"])
    assert video_row["in_app_call"] is True
    assert video_row["call_video"] is True
    assert phone_row["in_app_call"] is True
    assert phone_row["call_video"] is False


def test_candidate_can_start_when_admin_allows(client):
    admin = promote_admin(client, "call-start-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-start-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-start", title="Cariste")
    cand = register(client, "call-start-cand@example.com")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    created = client.post(
        "/api/interviews",
        headers=admin_h,
        json={
            "candidate_id": client.get("/api/candidates/me", headers=cand_h).json()["data"]["id"],
            "application_id": applied["id"],
            "scheduled_at": "2026-08-20T10:00:00+00:00",
            "type": "VIDEO",
            "candidate_can_start": True,
        },
    )
    assert created.status_code == 200, created.text
    interview = created.json()["data"]
    assert interview["candidate_can_start"] is True
    assert interview["can_start_call"] is True
    mine = client.get(f"/api/interviews/{interview['id']}", headers=cand_h).json()["data"]
    assert mine["can_start_call"] is True
    assert mine["can_join_call"] is True
    join = client.post(f"/api/calls/{interview['id']}/join", headers=cand_h, json={"video": True})
    assert join.status_code == 200, join.text


def test_admin_shell_can_join_in_app_call():
    html = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")
    assert "talendus-call.js" in html
    js = (ROOT / "admin" / "js" / "app.js").read_text(encoding="utf-8")
    assert "data-join-call" in js
    assert "TalendusCall" in js
    assert "function callButtons" in js
    assert "candidate_can_start" in js
    assert "data-open-call" in js
    assert "Lancer visio" in js
    assert "Lancer audio" in js
    assert 'var open = i.call_open ? "Rejoindre" : "Lancer"' not in js


def test_call_restarts_after_hangup_without_stale_signals(client):
    admin = promote_admin(client, "call-retry-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-retry-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-retry", title="Cariste")
    cand = register(client, "call-retry-cand@example.com")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    interview = _interview(client, admin_h, cand, applied, "VIDEO")
    iid = interview["id"]

    assert client.post(f"/api/calls/{iid}/join", headers=admin_h, json={"video": True}).status_code == 200
    assert client.post(f"/api/calls/{iid}/join", headers=cand_h, json={"video": True}).status_code == 200
    offer = client.post(
        f"/api/calls/{iid}/signal",
        headers=admin_h,
        json={"kind": "offer", "payload": {"type": "offer", "sdp": "v=0-first"}},
    )
    assert offer.status_code == 200, offer.text
    assert client.post(f"/api/calls/{iid}/hangup", headers=cand_h).status_code == 200
    assert client.post(f"/api/calls/{iid}/hangup", headers=admin_h).status_code == 200

    leftover = client.get(f"/api/calls/{iid}/signals", headers=admin_h).json()["data"]
    assert leftover["signals"] == []
    assert leftover["peers"] == []
    waiting = client.get(f"/api/interviews/{iid}", headers=cand_h).json()["data"]
    assert waiting["can_join_call"] is False
    assert waiting["host_in_call"] is False
    assert client.post(f"/api/calls/{iid}/join", headers=cand_h, json={"video": True}).status_code == 409

    again = client.post(f"/api/calls/{iid}/join", headers=admin_h, json={"video": True})
    assert again.status_code == 200, again.text
    assert again.json()["data"]["call_open"] is True
    cand_again = client.post(f"/api/calls/{iid}/join", headers=cand_h, json={"video": True})
    assert cand_again.status_code == 200, cand_again.text
    incoming = client.get(f"/api/calls/{iid}/signals", headers=cand_h).json()["data"]
    kinds = [row["kind"] for row in incoming["signals"]]
    assert "hangup" not in kinds
    assert "offer" not in kinds
    assert any(p["user_id"] == admin["user"]["id"] for p in incoming["peers"])

    second_offer = client.post(
        f"/api/calls/{iid}/signal",
        headers=admin_h,
        json={"kind": "offer", "payload": {"type": "offer", "sdp": "v=0-second"}},
    )
    assert second_offer.status_code == 200, second_offer.text
    fresh = client.get(f"/api/calls/{iid}/signals", headers=cand_h).json()["data"]
    offers = [row for row in fresh["signals"] if row["kind"] == "offer"]
    assert len(offers) == 1
    assert offers[0]["payload"]["sdp"] == "v=0-second"


def test_open_room_clears_idle_signaling(client):
    admin = promote_admin(client, "call-open-admin@example.com")
    admin_h = auth_header(admin)
    emp = register(client, "call-open-emp@example.com", "EMPLOYER")
    job = staff_publish_job(client, emp, admin, slug="call-open-room", title="Cariste")
    cand = register(client, "call-open-cand@example.com")
    cand_h = auth_header(cand)
    applied = client.post("/api/applications", headers=cand_h, json={"job_id": job["id"]}).json()["data"]
    interview = _interview(client, admin_h, cand, applied, "VIDEO")
    iid = interview["id"]
    client.post(f"/api/calls/{iid}/join", headers=admin_h, json={"video": True})
    client.post(f"/api/calls/{iid}/signal", headers=admin_h, json={"kind": "offer", "payload": {"sdp": "stale"}})
    client.post(f"/api/calls/{iid}/hangup", headers=admin_h)
    opened = client.post(f"/api/calls/{iid}/open", headers=admin_h)
    assert opened.status_code == 200, opened.text
    lobby = client.get(f"/api/calls/{iid}/lobby", headers=cand_h).json()["data"]
    assert lobby["call_open"] is True
    assert lobby["can_join"] is False
    assert client.post(f"/api/calls/{iid}/join", headers=cand_h, json={"video": True}).status_code == 409
    staff = client.post(f"/api/calls/{iid}/join", headers=admin_h, json={"video": True})
    assert staff.status_code == 200, staff.text
    ready = client.get(f"/api/interviews/{iid}", headers=cand_h).json()["data"]
    assert ready["can_join_call"] is True
    assert ready["host_in_call"] is True
    assert ready["call_step"] == "join"
    joined = client.post(f"/api/calls/{iid}/join", headers=cand_h, json={"video": True})
    assert joined.status_code == 200, joined.text
    signals = client.get(f"/api/calls/{iid}/signals", headers=cand_h).json()["data"]["signals"]
    assert signals == []


def test_candidate_shell_loads_call_engine():
    html = (ROOT / "espace.html").read_text(encoding="utf-8")
    assert "talendus-call.js" in html
    account = (ROOT / "assets" / "js" / "account.js").read_text(encoding="utf-8")
    engine = (ROOT / "assets" / "js" / "talendus-call.js").read_text(encoding="utf-8")
    assert "sessionIsUsable" in engine
    assert "signalIsStale" in engine
    assert "replacePc" in engine
    assert "data-call-retry" in engine
    assert "native ? 12 : 4" in engine
    assert "interviewStepsLead" in account
    assert "can_start_call" in account
    assert "Rejoindre n’apparaît que lorsque le conseiller a lancé" in account
    assert "t.startCallAudio" in account
    assert "t.joinCallAudio" in account
    assert "tl-profile-stack" in account
    assert "notifGroupInterviews" in account
    css = (ROOT / "assets" / "css" / "talendus.css").read_text(encoding="utf-8")
    assert ".tl-session-menu-copy" in css
    assert ".tl-avatar.is-menu" in css
