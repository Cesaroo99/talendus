from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_quebec_form_hints_script_is_wired():
    js = (ROOT / "assets" / "js" / "qc-hints.js").read_text(encoding="utf-8")
    for needle in (
        "Montréal",
        "Laval",
        "Longueuil",
        "Québec",
        "CAD",
        "514 555-0123",
        "datalist",
        "TalendusHints",
        "cariste",
        "ASP Construction",
    ):
        assert needle.lower() in js.lower(), needle
    assert "Français" in js
    admin = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")
    assert "qc-hints.js" in admin
    parts = (ROOT / "scripts" / "parts.py").read_text(encoding="utf-8")
    assert "qc-hints.js" in parts


def test_public_forms_propose_quebec_examples():
    pos = (ROOT / "scripts" / "positioning.py").read_text(encoding="utf-8")
    assert "Laval, Longueuil, Rive-Sud" in pos
    assert "514 555-0123" in pos
    assert "cariste, soudeur, machiniste CNC" in pos
    assert "ASP requise" in pos or "ASP required" in pos
    jobs = (ROOT / "emplois.html").read_text(encoding="utf-8")
    assert "qc-hints.js" in jobs
    assert "Brossard" in jobs
    contact = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert "514 555-0123" in contact
    mobile = (ROOT / "m.html").read_text(encoding="utf-8")
    assert "qc-hints.js" in mobile
    en = (ROOT / "en" / "m.html").read_text(encoding="utf-8")
    assert "qc-hints.js" in en
