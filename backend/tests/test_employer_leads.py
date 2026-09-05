from sqlalchemy import func, select

from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.models import Company, User
from app.models.enums import CompanyStatus, UserRole
from app.models.prospect import Prospect
from app.services.employer_leads import ensure_quebec_employer_leads
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
    assert len(QUEBEC_EMPLOYER_LEADS) == 151
    names = [row["name"].casefold() for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(names)) == 151
    websites = [row["website"] for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(websites)) == 151
    emails = [row["email"].casefold() for row in QUEBEC_EMPLOYER_LEADS if row.get("email")]
    assert len(set(emails)) == len(emails)
    assert emails, "Au moins un courriel public RH/info doit être présent."
    wave2 = QUEBEC_EMPLOYER_LEADS[50:100]
    assert len(wave2) == 50
    assert all(row.get("email") for row in wave2), "La 2e vague doit toutes avoir un courriel public."
    wave4 = QUEBEC_EMPLOYER_LEADS[100:]
    assert len(wave4) == 51
    assert all(row.get("email") for row in wave4), "La 4e vague doit toutes avoir un courriel public vérifié."
    sectors = {row["sector"] for row in wave2}
    assert len(sectors) >= 8, "La 2e vague doit couvrir plusieurs secteurs, pas seulement l’usine."
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


def test_ensure_creates_prospect_clients_without_employer_accounts(client, db):
    promote_admin(client, "leads-admin@talendus.ca")
    created = ensure_quebec_employer_leads(db)
    db.commit()
    assert created == 151
    assert ensure_quebec_employer_leads(db) == 0
    db.commit()

    leads = list(db.scalars(select(Company).where(Company.name.in_([r["name"] for r in QUEBEC_EMPLOYER_LEADS]))))
    assert len(leads) == 151
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
    from tests.conftest import auth_header

    listed = client.get("/api/companies", headers=auth_header(admin))
    assert listed.status_code == 200
    names = {row["name"] for row in listed.json()["data"]}
    assert "Usine Jade" in names
    assert "Cascades" in names
    assert "Métalco" not in names
