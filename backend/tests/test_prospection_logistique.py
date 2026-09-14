from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "prospection"))
from build_prospection_logistique import COMPANIES, build, catalog_keys
from app.services.employer_claim import normalize_company_name


def test_no_catalog_duplicates():
    names, hosts = catalog_keys()
    rows = build()
    assert rows
    for row in rows:
        assert normalize_company_name(row["Nom entreprise"]) not in names


def test_every_email_has_a_proof_and_is_not_guessed():
    for company in COMPANIES:
        for item in company.get("emails") or []:
            assert item.get("addr") and "@" in item["addr"]
            assert item.get("proof")
            local = item["addr"].split("@", 1)[0].lower()
            assert local not in {"prenom.nom", "jean.tremblay", "john.doe"}
            assert not item["addr"].startswith("prenom.")


def test_export_marks_empty_when_unproven():
    rows = {r["Nom entreprise"]: r for r in build()}
    stox = rows["Distribution Stox (Unimax)"]
    assert stox["Email #1"] == ""
    assert "Aucun courriel" in stox["Source email"] or "0 email" in stox["Notes"]
    gariepy = rows["Transport Gariépy"]
    assert gariepy["Email recrutement vérifié"] == "cv@transportgariepy.com"
    assert "Page Carrières" in gariepy["Vérification email #1"]
