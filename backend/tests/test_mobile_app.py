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
    assert "tn-splash" in page
    assert "tn-orbit" in page
    assert "tn-ring-a" in page
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


def test_mobile_app_uses_the_dashboard_session():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "canonicalize",
        "portalHash",
        "hydrateSession",
        "dashboard: \"home\"",
        "#/settings",
        "#/pipeline",
        "#/company",
        "#/app/",
        "/candidates/me/dashboard",
        "/companies/me/dashboard",
        "/users/me/preferences",
        "data-open-notif",
        "staffRole",
        "/admin/",
    ):
        assert needle in js
    api = (ROOT / "assets" / "js" / "api.js").read_text(encoding="utf-8")
    assert "talendus_access_token" in api
    assert "localStorage.setItem(USER, JSON.stringify(json.data))" in api
    auth = (ROOT / "assets" / "js" / "auth-gate.js").read_text(encoding="utf-8")
    assert 'isNativeApp()' in auth
    assert "/m.html" in auth
    native = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert "candidate|employer" in native
    page = (ROOT / "espace.html").read_text(encoding="utf-8")
    assert "candidate|employer" in page
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-check" in css


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
    assert ".tn-orbit" in css
    assert ".tn-splash" in css
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    assert "brandOrbit" in js
    assert "tn-title-light" in js


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


def test_mobile_app_javascript_parses():
    import shutil
    import subprocess

    path = ROOT / "assets" / "js" / "mobile-app.js"
    js = path.read_text(encoding="utf-8")
    assert '+ "</a><a href="#' not in js
    assert "function quickLinks" in js
    assert "hydrateSession().then(loadRoute)" in js
    assert "bustCache" in js
    assert "isFresh" in js
    assert "requestIdleCallback" in js
    assert "render();" in js
    node = shutil.which("node")
    if node:
        checked = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
        assert checked.returncode == 0, checked.stderr
