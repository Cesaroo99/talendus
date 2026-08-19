from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_mobile_shell_is_not_the_website():
    page = (ROOT / "m.html").read_text(encoding="utf-8")
    assert 'id="tl-native-app"' in page
    assert "mobile-app.js" in page
    assert "mobile-app.css" in page
    assert "vl-header-area" not in page
    assert "footer-widget" not in page
    assert "preloader" not in page
    assert "data-install-now" not in page
    assert "talendus.js" not in page
    en = (ROOT / "en" / "m.html").read_text(encoding="utf-8")
    assert 'id="tl-native-app"' in en
    assert "mobile-app.js" in en


def test_mobile_app_has_recruiting_screens():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in ("#/jobs", "#/messages", "#/me", "#/hiring", "data-apply-form", "data-login"):
        assert needle in js
    assert "blog" not in js.lower()
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-tabs" in css


def test_mobile_app_persona_extras():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "#/notifs",
        "#/saved",
        "#/alerts",
        "#/interviews",
        "#/inbox",
        "#/invoices",
        "#/contracts",
        "data-save-job",
        "data-withdraw",
        "data-forgot",
        "data-alert",
        "data-sign",
        "data-pdf",
        "data-pay",
        "data-int-status",
        "forgotPassword",
        "cover_note",
    ):
        assert needle in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    for needle in (".tn-badge", ".tn-chips", ".tn-quick", ".tn-notif.is-unread", ".tn-forgot"):
        assert needle in css


def test_mobile_app_gates_access_by_persona():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    assert 'data-choose="talent"' in js
    assert 'data-choose="employer"' in js
    assert "#/welcome" in js
    assert "allowedRoute" in js
    assert 'name === "welcome"' in js
    assert "if (!state.user)" in js
    assert "if (!isCandidate()) return" in js
    assert "if (!isEmployer()) return" in js
    assert "isCandidate() && (r.name === \"home\" || r.name === \"jobs\")" in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-persona" in css
    assert "body.tn-gated" in css


def test_native_app_never_asks_to_install_again():
    js = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert "TalendusApp" in js
    assert "isNativeApp" in js
    assert "/m.html" in js
    java = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "java" / "ca" / "talendus" / "app" / "MainActivity.java").read_text(encoding="utf-8")
    assert "TalendusApp/1.0" in java
    assert "https://talendus.ca/m.html" in java
    profile = (ROOT / "assets" / "app" / "talendus.mobileconfig").read_text(encoding="utf-8")
    assert "https://talendus.ca/m.html" in profile


def test_manifest_opens_the_mobile_shell():
    text = (ROOT / "manifest.webmanifest").read_text(encoding="utf-8")
    assert '"start_url": "/m.html"' in text


def test_mobile_shell_is_served(client):
    res = client.get("/m.html")
    assert res.status_code == 200, res.text
    assert "tl-native-app" in res.text
    en = client.get("/en/m.html")
    assert en.status_code == 200, en.text
    assert "tl-native-app" in en.text
