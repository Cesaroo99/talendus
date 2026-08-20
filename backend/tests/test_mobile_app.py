from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_mobile_shell_is_not_the_website():
    page = (ROOT / "m.html").read_text(encoding="utf-8")
    assert 'id="tl-native-app"' in page
    assert "mobile-app.js" in page
    assert "talendus-call.js" in page
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
    assert '["welcome", "login", "register", "forgot", "reset", "verify"]' in js
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
    assert "tn-gate-brand" in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-gate-brand" in css
    assert "padding-left: .28em" in css


def test_mobile_app_signs_in_before_creating_an_account():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    assert '<a class="tn-persona" href="#/login/talent"' in js
    assert '<a class="tn-persona" href="#/login/employer"' in js
    assert '<a class="tn-persona" href="#/register/talent"' not in js
    assert "#/forgot" in js
    assert "data-reset" in js
    assert "data-forgot" in js
    assert "sendReset" in js
    assert 'id="tn-forgot-email"' in js
    api = (ROOT / "assets" / "js" / "api.js").read_text(encoding="utf-8")
    assert "if (token && !isPublicAuthPath(path))" in api
    assert 'email: String(email || "").trim().toLowerCase()' in api
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-auth-link" in css
    assert ".tn-hp" in css
    assert "border-radius: 24px 24px 0 0" not in css
    assert ".tn-sheet .tn-title" in css
    assert ".tn-forgot" in css
    assert "text-align: center" in css


def test_native_app_never_asks_to_install_again():
    js = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert "TalendusApp" in js
    assert "isNativeApp" in js
    assert "/m.html" in js
    java = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "java" / "ca" / "talendus" / "app" / "MainActivity.java").read_text(encoding="utf-8")
    assert "TalendusApp/" in java
    assert "https://talendus.ca/m.html" in java
    assert "TalendusNative" in java
    assert "POST_NOTIFICATIONS" in java
    assert "showNotification" in java
    assert "onShowFileChooser" in java
    assert "FILE_CHOOSER" in java
    assert "setAllowFileAccess" in java
    assert "setAuthToken" in java
    assert "CAMERA" in java
    assert "RECORD_AUDIO" in java
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


def test_mobile_app_hub_is_ordered():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "#/profile",
        "#/cv",
        "#/help",
        "#/need",
        "tn-menu",
        "tn-identity",
        "data-avatar",
        "data-exp",
        "data-edu",
        "data-cert",
        "data-dl-cv",
        "data-del-cv",
        "data-hiring",
        "groupFile",
        "identityHead",
        "menuGroup",
        'href="#/home"',
        "data-enable-push",
        "notify_push",
        "/push/subscribe",
        "enablePush",
        "TalendusNative",
        "#/call/",
        "TalendusCall",
        "callAudio",
        "setAuthToken",
    ):
        assert needle in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    for needle in (".tn-menu", ".tn-identity", "a.tn-stat", ".tn-filters", ".tn-avatar", ".tn-push-card"):
        assert needle in css
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
        call_js = ROOT / "assets" / "js" / "talendus-call.js"
        call_checked = subprocess.run([node, "--check", str(call_js)], capture_output=True, text=True)
        assert call_checked.returncode == 0, call_checked.stderr
        account_js = ROOT / "assets" / "js" / "account.js"
        acc_checked = subprocess.run([node, "--check", str(account_js)], capture_output=True, text=True)
        assert acc_checked.returncode == 0, acc_checked.stderr


def test_mobile_app_tracks_applications_and_offers_choice_filters():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "tn-tracker",
        "appTracker",
        "/jobs/options",
        "choiceSelect",
        "jobFacts",
        'choiceSelect("shift"',
        'choiceSelect("schedule"',
        'choiceSelect("work_mode"',
        'choiceSelect("title"',
        'choiceSelect("work_authorization"',
        'labeledChoice("work_status"',
        "o.occupations",
        "can_sponsor",
        '<optgroup label="',
        'mini ? \' aria-hidden="true"\'',
        "if (!mini)",
    ):
        assert needle in js
    assert "tracker.outcome" not in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    for needle in (
        ".tn-tracker",
        ".tn-facts",
        ".tn-search select",
        ".tn-search-bar",
        ".tn-filter-toggle",
        ".tn-tracker.is-mini li b",
        "overflow: hidden",
    ):
        assert needle in css
    jobs = (ROOT / "emplois.html").read_text(encoding="utf-8")
    assert 'id="job-shift"' in jobs
    assert "Quart de jour" in jobs
    en_jobs = (ROOT / "en" / "jobs.html").read_text(encoding="utf-8")
    assert 'id="job-shift"' in en_jobs


def test_mobile_app_searches_jobs_without_a_stray_button():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "tn-search-bar",
        "data-toggle-filters",
        "data-jobs-grid",
        "scheduleJobSearch",
        "runJobSearch",
        'filters: "Filtres"',
    ):
        assert needle in js
    assert "esc(t.go)" not in js
    jobs_view = js.split("function jobsView")[1].split("function jobView")[0]
    assert '<button type="submit">' not in jobs_view
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-search-bar" in css
    assert ".tn-filter-toggle" in css
    assert ".tn-search button" not in css


def test_mobile_app_switches_language_and_hides_status_codes():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "talendus_locale",
        "talendus_locale_chosen",
        "function applyLocale",
        "function langSwitch",
        "function pageIsEn",
        "function localeChosen",
        'data-locale="fr-CA"',
        'data-locale="en-CA"',
        'WITHDRAWN: "Retirée"',
        "var EN =",
        "var FR =",
        'path.indexOf("/en/") === 0',
    ):
        assert needle in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-langs" in css
    assert ".tn-lang.is-on" in css
    account = (ROOT / "assets" / "js" / "account.js").read_text(encoding="utf-8")
    assert "toUpperCase()" in account
    assert 'WITHDRAWN:' in account


def test_mobile_app_uploads_files_and_allows_multiple_choices():
    js = (ROOT / "assets" / "js" / "mobile-app.js").read_text(encoding="utf-8")
    for needle in (
        "function filePicker",
        "function choiceGroup",
        "function formChoice",
        "function sendPickedFiles",
        "function pickedFiles",
        "data-doc",
        "data-native-pick",
        "tn-file-input",
        "tn-file-hit",
        "openDocumentPicker",
        "__tnReceiveFiles",
        "hasNativePicker",
        'choiceGroup("languages"',
        'choiceGroup("contract_type"',
        'choiceGroup("shift_preference"',
        "language_choices",
        "uploadEach",
        "uploadDoc",
        "api.appendFile",
        'esc(t.uploadDoc)',
    ):
        assert needle in js
    assert ".pdf,.doc" not in js
    css = (ROOT / "assets" / "css" / "mobile-app.css").read_text(encoding="utf-8")
    assert ".tn-file-btn" in css
    assert ".tn-file-hit" in css
    assert ".tn-chip-check" in css
    assert "font-size: 80px" in css
    java = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "java" / "ca" / "talendus" / "app" / "MainActivity.java").read_text(encoding="utf-8")
    assert "onShowFileChooser" in java
    assert "EXTRA_ALLOW_MULTIPLE" in java
    assert "ACTION_OPEN_DOCUMENT" in java
    assert "ACTION_GET_CONTENT" in java
    assert "FileChooserParams.parseResult" in java
    assert "openDocumentPicker" in java
    assert "NATIVE_PICK" in java
    manifest = (ROOT / "mobile" / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
    assert 'android:launchMode="singleTop"' in manifest
    api = (ROOT / "assets" / "js" / "api.js").read_text(encoding="utf-8")
    assert "function filePartName" in api
    assert "function appendFile" in api
    assert 'opts.body instanceof FormData' in api
