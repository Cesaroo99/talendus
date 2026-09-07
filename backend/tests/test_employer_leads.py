from sqlalchemy import func, select

from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.models import Company, User
from app.models.enums import CompanyStatus, UserRole
from app.models.prospect import Prospect
from app.services.employer_claim import normalize_company_name
from app.services.employer_leads import (
    _find_company,
    _names_similar,
    _owned_company_is_this_lead,
    ensure_quebec_employer_leads,
)
from tests.conftest import promote_admin


DEMO_FAKES = {
    "Métalco",
    "LogiCentre Laval",
    "Alimor",
    "Plastika",
    "TransQuébec",
    "Usine Nordique",
    "Forge Mauricie",
    "Distro Plus",
    "Talendus",
}


def test_lead_catalog_is_fifty_real_and_unique():
    assert len(QUEBEC_EMPLOYER_LEADS) == 524
    names = [row["name"].casefold() for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(names)) == 524
    websites = [row["website"] for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(websites)) == 524
    emails = [row["email"].casefold() for row in QUEBEC_EMPLOYER_LEADS if row.get("email")]
    assert len(set(emails)) == len(emails)
    assert emails, "Au moins un courriel public RH/info doit être présent."
    wave2 = QUEBEC_EMPLOYER_LEADS[50:100]
    assert len(wave2) == 50
    assert all(row.get("email") for row in wave2), "La 2e vague doit toutes avoir un courriel public."
    extra = QUEBEC_EMPLOYER_LEADS[100:324]
    assert len(extra) == 224
    assert all(row.get("email") for row in extra), "Les fiches 101-324 doivent toutes avoir un courriel public vérifié."
    sectors = {row["sector"] for row in QUEBEC_EMPLOYER_LEADS[50:]}
    assert len(sectors) >= 8, "Les vagues avec courriel doivent couvrir plusieurs secteurs, pas seulement l’usine."
    wave5 = QUEBEC_EMPLOYER_LEADS[300:324]
    assert len(wave5) == 24
    assert all(row.get("email") for row in wave5)
    assert {row["sector"] for row in wave5} >= {
        "Construction",
        "Industrie",
        "Manufacturier",
        "Commerce",
        "Hôtellerie et tourisme",
        "Entrepôt et logistique",
    }
    wave6 = QUEBEC_EMPLOYER_LEADS[324:]
    assert len(wave6) == 200
    assert all(row.get("lead_score") for row in wave6)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C"} for row in wave6)
    assert all(row.get("researched_at") == "2026-09-07" for row in wave6)
    assert sum(1 for row in wave6 if row.get("email")) >= 40
    assert sum(1 for row in wave6 if not row.get("email")) >= 80
    assert {row["sector"] for row in wave6} >= {
        "Manufacturier",
        "Aérospatial",
        "Transformation alimentaire",
        "Logistique",
        "Pharmaceutique",
    }
    for row in QUEBEC_EMPLOYER_LEADS:
        assert row["name"] not in DEMO_FAKES
        assert row["city"]
        assert row["sector"]
        assert row["website"].startswith("https://")
        assert len(row["website"]) <= 160
        assert row.get("hiring")
        assert "555-" not in (row.get("phone") or "")
        assert "example." not in (row.get("email") or "")
        assert "example." not in row["website"]
        if row.get("email"):
            assert "@" in row["email"]
            assert not row["email"].startswith("j.")
            local = row["email"].split("@", 1)[0]
            assert local not in {"jean.tremblay", "prenom.nom", "john.doe"}
    keys = [normalize_company_name(row["name"]) for row in QUEBEC_EMPLOYER_LEADS]
    assert all(keys)
    assert len(set(keys)) == len(keys)


def test_ensure_creates_prospect_clients_without_employer_accounts(client, db):
    promote_admin(client, "leads-admin@talendus.ca")
    created = ensure_quebec_employer_leads(db)
    db.commit()
    assert created == 524
    assert ensure_quebec_employer_leads(db) == 0
    db.commit()

    leads = list(db.scalars(select(Company).where(Company.name.in_([r["name"] for r in QUEBEC_EMPLOYER_LEADS]))))
    assert len(leads) == 524
    assert all(c.status == CompanyStatus.PROSPECT for c in leads)
    assert all(c.province == "Québec" for c in leads)
    assert all(not c.owner_user_id for c in leads)
    assert db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.EMPLOYER)) == 0

    with_email = [r for r in QUEBEC_EMPLOYER_LEADS if r.get("email")]
    prospects = list(db.scalars(select(Prospect).where(Prospect.side == "employer", Prospect.source == "prospection")))
    emails = {p.email for p in prospects}
    for row in with_email:
        assert row["email"].lower() in emails
    casc = next(p for p in prospects if p.email == "contact@cascades.com")
    assert casc.company_name == "Cascades"
    assert casc.stage == "a-contacter"
    assert casc.city == "Kingsey Falls"
    assert not (casc.first_name or "").strip()
    assert not (casc.last_name or "").strip()
    assert all(not (p.first_name or "").casefold().startswith("ressource") for p in prospects)


def test_ensure_clears_generic_contact_names(client, db):
    promote_admin(client, "leads-generic@talendus.ca")
    ensure_quebec_employer_leads(db)
    db.commit()
    row = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    row.first_name = "Ressources"
    row.last_name = "humaines"
    db.commit()
    ensure_quebec_employer_leads(db)
    db.commit()
    again = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    assert again.first_name == ""
    assert again.last_name == ""
    assert again.company_name == "Cascades"


def test_ensure_does_not_reset_prospect_stage(client, db):
    promote_admin(client, "leads-stage@talendus.ca")
    ensure_quebec_employer_leads(db)
    db.commit()
    row = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    row.stage = "discussion"
    db.commit()
    ensure_quebec_employer_leads(db)
    db.commit()
    again = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    assert again.stage == "discussion"


def test_register_employer_not_confused_with_leads(client, db):
    created = client.post(
        "/api/auth/register",
        json={
            "email": "new-plant@example.com",
            "password": "Password1!",
            "first_name": "Jade",
            "last_name": "Test",
            "role": "EMPLOYER",
            "company_name": "Usine Jade",
        },
    )
    assert created.status_code == 200, created.text
    admin = promote_admin(client, "leads-mix@talendus.ca")
    ensure_quebec_employer_leads(db)
    db.commit()
    db.expire_all()
    names = set(db.scalars(select(Company.name)))
    assert "Usine Jade" in names
    assert "Cascades" in names
    assert "Métalco" not in names
    assert {row["name"] for row in QUEBEC_EMPLOYER_LEADS} <= names
    from tests.conftest import auth_header

    listed = client.get("/api/companies", headers=auth_header(admin))
    assert listed.status_code == 200
    api_names = {row["name"] for row in listed.json()["data"]}
    assert "Usine Jade" in api_names
    assert "Cascades" in api_names, f"api={len(api_names)} db={len(names)}"


def test_owned_company_does_not_absorb_unrelated_lead():
    owned = Company(name="Usine Jade", legal_name="Usine Jade", owner_user_id="user-1")
    unowned = Company(name="Usine Jade", legal_name="Usine Jade")
    lead = {"name": "Cascades", "legal_name": "Cascades inc."}
    assert not _owned_company_is_this_lead(owned, lead)
    assert _owned_company_is_this_lead(unowned, lead)
    assert _owned_company_is_this_lead(owned, {"name": "Usine Jade Inc.", "legal_name": "Usine Jade"})


def test_names_similar_requires_real_overlap():
    assert _names_similar("Velan Inc.", "Velan")
    assert _names_similar("Cascades Inc.", "Cascades")
    assert not _names_similar("Fairmont Le Château Frontenac", "Fairmont Le Château Montebello")
    assert not _names_similar("Admin Inc.", "CAE")
    assert not _names_similar("Admin Inc.", "AD")
    assert not _names_similar("Admin Inc.", "Velan")


def test_find_company_matches_normalized_name(client, db):
    existing = Company(
        name="Velan Inc.",
        legal_name="Velan inc.",
        status=CompanyStatus.PROSPECT,
        province="Québec",
        country="Canada",
    )
    db.add(existing)
    db.commit()
    found = _find_company(db, {"name": "Velan", "legal_name": "Velan inc.", "website": "https://velan.com"})
    assert found is not None
    assert found.id == existing.id
    assert _find_company(db, {"name": "Bombardier", "website": "https://bombardier.com"}) is None


def test_ensure_survives_stale_prospect_left_in_caller_session(client, db):
    from app.database import SessionLocal

    promote_admin(client, "leads-stale@talendus.ca")
    row = db.scalar(select(Prospect).where(Prospect.email == "leads-stale@talendus.ca"))
    assert row is not None
    other = SessionLocal()
    other.delete(other.get(Prospect, row.id))
    other.commit()
    other.close()
    row.city = "Montréal"
    created = ensure_quebec_employer_leads(db)
    db.commit()
    assert created == 524


def test_ensure_dedupes_normalized_name_and_keeps_empty_email(client, db):
    promote_admin(client, "leads-dedupe@talendus.ca")
    db.add(
        Company(
            name="Velan Inc.",
            legal_name="Velan inc.",
            status=CompanyStatus.PROSPECT,
            province="Québec",
            country="Canada",
        )
    )
    db.commit()
    db.expire_all()
    created = ensure_quebec_employer_leads(db)
    db.expire_all()
    db.commit()
    assert created == 523
    velans = list(db.scalars(select(Company).where(Company.name.ilike("%velan%"))))
    assert len(velans) == 1
    assert velans[0].name == "Velan Inc."
    assert not db.scalar(select(Prospect.id).where(Prospect.company_name == "Velan"))
    assert not db.scalar(select(Prospect.id).where(Prospect.email == "leads-dedupe@talendus.ca", Prospect.source == "prospection"))
    assert ensure_quebec_employer_leads(db) == 0
