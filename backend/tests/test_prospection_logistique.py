from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "prospection"))
from build_prospection_logistique import COMPANIES, HUBS, build, merged_companies, normalize_company_name
from hubs_messagerie import HUBS as HUBS_SRC


def test_every_email_has_a_proof_and_is_not_guessed():
    for company in list(COMPANIES) + list(HUBS_SRC):
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


def test_catalog_hubs_are_included_not_excluded():
    rows = {r["Nom entreprise"]: r for r in build()}
    assert "Purolator" in rows
    assert rows["Purolator"]["Présence Talendus"] == "Catalogue"
    assert rows["Purolator"]["Email recrutement vérifié"] == "TalentCOE@purolator.com"
    assert "careers.purolator.com" in rows["Purolator"]["Vérification email #1"]
    assert "GLS Canada" in rows
    assert rows["GLS Canada"]["Email recrutement vérifié"] == "recrutement@gls-canada.com"
    assert "Loomis Express" in rows
    assert rows["Loomis Express"]["Email recrutement vérifié"] == "careers@loomis-express.com"


def test_new_purolator_like_companies_are_present():
    rows = {r["Nom entreprise"]: r for r in build()}
    assert rows["Nationex"]["Présence Talendus"] == "Nouveau"
    assert rows["Nationex"]["Email recrutement vérifié"] == "carrieres@nationex.com"
    assert rows["ICS Courier"]["Présence Talendus"] == "Nouveau"
    assert rows["ICS Courier"]["Email #1"] == ""
    assert rows["Groupe Fastfrate"]["Email recrutement vérifié"] == "careers@www.fastfrate.com"


def test_merged_companies_dedupe_boutin():
    keys = [normalize_company_name(c["name"]) for c in merged_companies()]
    assert len(keys) == len(set(keys))
    boutin = next(c for c in merged_companies() if "boutin" in c["name"].lower())
    assert any(e["addr"] == "info@boutin3pl.com" for e in boutin.get("emails") or [])


def test_hubs_imported_in_builder():
    assert HUBS
    assert any(h["name"] == "Purolator" for h in HUBS)
