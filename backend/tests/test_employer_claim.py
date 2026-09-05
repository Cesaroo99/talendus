from sqlalchemy import func, select

from app.models import Company, CompanyMembership
from app.models.enums import CompanyStatus
from app.models.prospect import Prospect
from app.services.employer_claim import find_unclaimed_employer_company, normalize_company_name
from app.services.employer_leads import ensure_quebec_employer_leads
from tests.conftest import auth_header, promote_admin


def _lead(
    db,
    *,
    name="Usine Nord",
    email="rh@usine-nord.example",
    website="https://www.usine-nord.example",
    stage="contacte",
    status=CompanyStatus.PROSPECT,
):
    company = Company(
        name=name,
        legal_name=f"{name} Inc.",
        trade_name=name,
        email=email,
        website=website,
        city="Trois-Rivières",
        sector="Industrie",
        province="Québec",
        country="Canada",
        status=status,
        contact_name="Ressources humaines",
    )
    db.add(company)
    db.flush()
    prospect = Prospect(
        side="employer",
        email=email.lower(),
        company_name=name,
        company_id=company.id,
        stage=stage,
        source="prospection",
        city="Trois-Rivières",
        sector="Industrie",
    )
    db.add(prospect)
    db.commit()
    return company.id, prospect.id


def _register(client, email, company_name, first_name="Marie"):
    return client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "Password1!",
            "first_name": first_name,
            "last_name": "Rivest",
            "role": "EMPLOYER",
            "company_name": company_name,
        },
    )


def test_normalize_company_name_strips_legal_suffix_and_accents():
    assert normalize_company_name("Cascades Inc.") == "cascades"
    assert normalize_company_name("Cascades") == "cascades"
    assert normalize_company_name("École des métiers") == "ecole des metiers"
    assert normalize_company_name("Usine Nord Ltée") == "usine nord"


def test_register_with_lead_email_claims_existing_fiche(client, db):
    company_id, prospect_id = _lead(db, stage="contacte")
    res = _register(client, "RH@usine-nord.example", "Usine Nord Inc.")
    assert res.status_code == 200, res.text
    user_id = res.json()["data"]["user"]["id"]
    db.expire_all()
    company = db.get(Company, company_id)
    prospect = db.get(Prospect, prospect_id)
    assert company.owner_user_id == user_id
    assert company.name == "Usine Nord"
    assert company.city == "Trois-Rivières"
    assert company.sector == "Industrie"
    assert company.status == CompanyStatus.PROSPECT
    assert db.scalar(select(func.count()).select_from(Company)) == 1
    assert db.scalar(select(func.count()).select_from(Prospect).where(Prospect.side == "employer")) == 1
    assert prospect.user_id == user_id
    assert prospect.company_id == company_id
    assert prospect.stage == "qualifie"
    assert prospect.first_name == "Marie"
    assert prospect.source == "prospection"
    assert db.scalar(
        select(func.count()).select_from(CompanyMembership).where(CompanyMembership.company_id == company_id)
    ) == 1
    me = client.get("/api/companies/me", headers=auth_header(res.json()["data"]))
    assert me.status_code == 200
    assert me.json()["data"]["id"] == company_id
    assert me.json()["data"]["name"] == "Usine Nord"


def test_register_same_lead_email_twice_is_conflict(client, db):
    _lead(db)
    first = _register(client, "rh@usine-nord.example", "Usine Nord")
    assert first.status_code == 200, first.text
    again = _register(client, "rh@usine-nord.example", "Usine Nord")
    assert again.status_code == 409
    assert again.json()["code"] == "EMAIL_TAKEN"
    db.expire_all()
    assert db.scalar(select(func.count()).select_from(Company)) == 1


def test_register_same_domain_and_name_claims_fiche(client, db):
    company_id, prospect_id = _lead(db, stage="a-contacter")
    res = _register(client, "marie.rh@usine-nord.example", "Usine Nord")
    assert res.status_code == 200, res.text
    user_id = res.json()["data"]["user"]["id"]
    db.expire_all()
    company = db.get(Company, company_id)
    original = db.get(Prospect, prospect_id)
    assert company.owner_user_id == user_id
    assert company.email == "rh@usine-nord.example"
    assert original.user_id == user_id
    assert original.email == "rh@usine-nord.example"
    assert original.stage == "qualifie"
    personal = db.scalar(select(Prospect).where(Prospect.email == "marie.rh@usine-nord.example"))
    assert personal is not None
    assert personal.company_id == company_id
    assert personal.user_id == user_id
    assert db.scalar(select(func.count()).select_from(Company)) == 1


def test_register_gmail_and_unique_prospect_name_claims_fiche(client, db):
    company_id, prospect_id = _lead(db)
    res = _register(client, "marie.usine@gmail.com", "Usine Nord")
    assert res.status_code == 200, res.text
    db.expire_all()
    assert db.get(Company, company_id).owner_user_id == res.json()["data"]["user"]["id"]
    assert db.get(Prospect, prospect_id).user_id == res.json()["data"]["user"]["id"]
    assert db.scalar(select(func.count()).select_from(Company)) == 1


def test_register_unrelated_company_does_not_steal_lead(client, db):
    company_id, _ = _lead(db)
    res = _register(client, "jade@example.com", "Usine Jade")
    assert res.status_code == 200, res.text
    db.expire_all()
    lead = db.get(Company, company_id)
    assert lead.owner_user_id is None
    names = set(db.scalars(select(Company.name)).all())
    assert names == {"Usine Nord", "Usine Jade"}


def test_register_does_not_steal_already_owned_company(client, db):
    company_id, _ = _lead(db)
    first = _register(client, "rh@usine-nord.example", "Usine Nord")
    assert first.status_code == 200, first.text
    second = _register(client, "autre.boss@gmail.com", "Usine Nord")
    assert second.status_code == 200, second.text
    db.expire_all()
    original = db.get(Company, company_id)
    assert original.owner_user_id == first.json()["data"]["user"]["id"]
    assert db.scalar(select(func.count()).select_from(Company)) == 2
    me = client.get("/api/companies/me", headers=auth_header(second.json()["data"]))
    assert me.status_code == 200
    assert me.json()["data"]["id"] != company_id


def test_register_preserves_advanced_pipeline_stage(client, db):
    _, prospect_id = _lead(db, stage="discussion")
    res = _register(client, "rh@usine-nord.example", "Usine Nord")
    assert res.status_code == 200, res.text
    db.expire_all()
    assert db.get(Prospect, prospect_id).stage == "discussion"


def test_find_skips_short_or_active_name_only_matches(client, db):
    _lead(db, name="CGI", email="rh@cgi-demo.example", website="https://www.cgi-demo.example", status=CompanyStatus.ACTIVE)
    found = find_unclaimed_employer_company(db, email="personne@gmail.com", company_name="CGI")
    assert found is None
    other_id, _ = _lead(db, name="Atelier Lynx", email="rh@atelier-lynx.example", status=CompanyStatus.ACTIVE)
    found_active = find_unclaimed_employer_company(db, email="marie@gmail.com", company_name="Atelier Lynx")
    assert found_active is None
    assert db.get(Company, other_id).owner_user_id is None


def test_catalog_lead_register_does_not_duplicate_cascades(client, db):
    promote_admin(client, "claim-admin@talendus.ca")
    ensure_quebec_employer_leads(db)
    db.commit()
    before = db.scalar(select(func.count()).select_from(Company).where(Company.name == "Cascades"))
    assert before == 1
    casc_id = db.scalar(select(Company.id).where(Company.name == "Cascades"))
    prospect = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    assert prospect is not None
    assert prospect.company_id == casc_id
    res = _register(client, "contact@cascades.com", "Cascades")
    assert res.status_code == 200, res.text
    db.expire_all()
    assert db.scalar(select(func.count()).select_from(Company).where(Company.name == "Cascades")) == 1
    casc = db.get(Company, casc_id)
    assert casc.owner_user_id == res.json()["data"]["user"]["id"]
    assert casc.city
    assert casc.website
    again = db.scalar(select(Prospect).where(Prospect.email == "contact@cascades.com"))
    assert again.company_id == casc_id
    assert again.user_id == casc.owner_user_id
    assert ensure_quebec_employer_leads(db) == 0
    db.commit()
    assert db.scalar(select(func.count()).select_from(Company).where(Company.name == "Cascades")) == 1
