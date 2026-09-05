import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _block(html: str, name: str) -> str:
    match = re.search(rf'(?:name|id)="{re.escape(name)}"[^>]*>(.*?)</select>', html, re.S)
    assert match, name
    return match.group(1)


def test_employer_forms_split_contract_and_hours():
    for rel in ("contact.html", "besoin-de-recrutement.html"):
        page = (ROOT / rel).read_text(encoding="utf-8")
        contrat = _block(page, "contrat")
        horaire = _block(page, "horaire")
        quart = _block(page, "quart")
        assert "Permanent" in contrat
        assert "Temps plein" not in contrat
        assert "Temps partiel" not in contrat
        assert "Temps plein" in horaire
        assert "Permanent" not in horaire
        assert "Quart de jour" in quart
        assert "Temps plein" not in quart
        assert "pas le temps plein ou partiel" in page
        assert "pays ou télétravail" not in page


def test_job_filters_do_not_mix_hours_into_contract():
    jobs = (ROOT / "emplois.html").read_text(encoding="utf-8")
    types = _block(jobs, "job-type")
    hours = _block(jobs, "job-schedule")
    city = _block(jobs, "job-city")
    assert "Temps plein / permanent" not in types
    assert 'value="Partiel"' not in types
    assert "Permanent" in types
    assert "Temps plein" in hours
    assert "Permanent" not in hours
    assert 'value="remote"' not in city
    assert "Type de contrat" in jobs


def test_english_forms_split_contract_and_hours():
    contact = (ROOT / "en" / "contact.html").read_text(encoding="utf-8")
    contrat = _block(contact, "contrat")
    horaire = _block(contact, "horaire")
    assert "Permanent" in contrat
    assert "Full-time" not in contrat
    assert "Full-time" in horaire
    jobs = (ROOT / "en" / "jobs.html").read_text(encoding="utf-8")
    types = _block(jobs, "job-type")
    assert "Full-time / permanent" not in types
    assert "Permanent" in types
    assert 'value="remote"' not in _block(jobs, "job-city")


def test_contact_js_sends_shift_and_schedule():
    js = (ROOT / "assets" / "js" / "talendus.js").read_text(encoding="utf-8")
    assert 'formValue(form, ["quart", "shift"])' in js
    assert 'formValue(form, ["horaire", "schedule"])' in js
