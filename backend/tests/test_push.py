from pathlib import Path

from tests.conftest import auth_header, register

ROOT = Path(__file__).resolve().parents[2]


def test_vapid_key_requires_auth(client):
    res = client.get("/api/push/vapid-public-key")
    assert res.status_code == 401


def test_subscribe_enables_phone_push(client):
    tokens = register(client, "push-user@example.com")
    headers = auth_header(tokens)
    key = client.get("/api/push/vapid-public-key", headers=headers)
    assert key.status_code == 200, key.text
    public_key = key.json()["data"]["public_key"]
    assert len(public_key) > 20
    sub = client.post(
        "/api/push/subscribe",
        headers=headers,
        json={
            "endpoint": "https://fcm.googleapis.com/fcm/send/talendus-test-endpoint",
            "keys": {"p256dh": "BNxabcdefghijklmnopqrstuvwxyz012345", "auth": "authsecret12"},
        },
    )
    assert sub.status_code == 200, sub.text
    prefs = client.get("/api/users/me/preferences", headers=headers)
    assert prefs.status_code == 200
    assert prefs.json()["data"]["notify_push"] is True
    gone = client.request(
        "DELETE",
        "/api/push/subscribe",
        headers=headers,
        json={"endpoint": "https://fcm.googleapis.com/fcm/send/talendus-test-endpoint"},
    )
    assert gone.status_code == 200, gone.text
    assert gone.json()["data"]["removed"] == 1


def test_notify_delivers_web_push(client, monkeypatch):
    import json

    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import NotificationType
    from app.models.push import PushSubscription
    from app.services.notifications import notify

    tokens = register(client, "push-deliver@example.com")
    headers = auth_header(tokens)
    client.post(
        "/api/push/subscribe",
        headers=headers,
        json={
            "endpoint": "https://fcm.googleapis.com/fcm/send/talendus-deliver",
            "keys": {"p256dh": "BNxabcdefghijklmnopqrstuvwxyz012345", "auth": "authsecret12"},
        },
    )
    calls = []

    def fake_deliver(info, payload, priv, mailto):
        calls.append({"info": info, "payload": payload, "mailto": mailto})

    monkeypatch.setattr("app.services.push._deliver", fake_deliver)
    db = SessionLocal()
    user = db.get(User, tokens["user"]["id"])
    notify(db, user, NotificationType.MESSAGE, "Nouveau message", "Votre conseiller vous a écrit.", "/espace.html#/messages")
    db.commit()
    db.close()
    assert calls
    body = json.loads(calls[0]["payload"].decode("utf-8"))
    assert body["title"] == "Nouveau message"
    assert body["href"] == "/m.html#/messages"
    assert calls[0]["info"]["endpoint"].endswith("talendus-deliver")


def test_gone_subscription_is_removed(client, monkeypatch):
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import NotificationType
    from app.models.push import PushSubscription
    from app.services.notifications import notify

    tokens = register(client, "push-gone@example.com")
    headers = auth_header(tokens)
    client.post(
        "/api/push/subscribe",
        headers=headers,
        json={
            "endpoint": "https://fcm.googleapis.com/fcm/send/talendus-gone",
            "keys": {"p256dh": "BNxabcdefghijklmnopqrstuvwxyz012345", "auth": "authsecret12"},
        },
    )

    class Gone(Exception):
        def __init__(self):
            super().__init__("410 Gone")
            self.response = type("R", (), {"status_code": 410})()

    def fake_deliver(*_args, **_kwargs):
        raise Gone()

    monkeypatch.setattr("app.services.push._deliver", fake_deliver)
    db = SessionLocal()
    user = db.get(User, tokens["user"]["id"])
    notify(db, user, NotificationType.MESSAGE, "Relance", "Un suivi vous attend.", "/espace.html#/notifs")
    db.commit()
    remaining = db.query(PushSubscription).filter(PushSubscription.user_id == user.id).count()
    db.close()
    assert remaining == 0


def test_mobile_app_asks_for_phone_notifications():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "data-enable-push",
        "notify_push",
        "/push/subscribe",
        "/push/vapid-public-key",
        "enablePush",
        "TalendusNative",
        "showNotification",
    ):
        assert needle in js
    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    assert "talendus-app-v19" in sw
    assert "showNotification" in sw
    java = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "java" / "ca" / "talendus" / "app" / "MainActivity.java").read_text(encoding="utf-8")
    assert "TalendusNative" in java
    assert "POST_NOTIFICATIONS" in java
    assert "setAuthToken" in java
    manifest = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
    assert "POST_NOTIFICATIONS" in manifest
    assert "CAMERA" in manifest
    assert "RECORD_AUDIO" in manifest
