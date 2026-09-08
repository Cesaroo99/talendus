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
    sync_catalog_emails_to_crm,
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
    assert len(QUEBEC_EMPLOYER_LEADS) == 1433
    names = [row["name"].casefold() for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(names)) == 1433
    websites = [row["website"] for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(websites)) == 1433
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
    wave6 = QUEBEC_EMPLOYER_LEADS[324:524]
    assert len(wave6) == 200
    assert all(row.get("lead_score") for row in wave6)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C"} for row in wave6)
    assert all(row.get("researched_at") == "2026-09-07" for row in wave6)
    assert sum(1 for row in wave6 if row.get("email")) >= 40
    # Géants formulaire-only : on n’invente pas d’adresse pour forcer le quota.
    assert sum(1 for row in wave6 if not row.get("email")) >= 20
    assert {row["sector"] for row in wave6} >= {
        "Manufacturier",
        "Aérospatial",
        "Transformation alimentaire",
        "Logistique",
        "Pharmaceutique",
    }
    wave7 = QUEBEC_EMPLOYER_LEADS[524:724]
    assert len(wave7) == 200
    assert all(row.get("lead_score") for row in wave7)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C"} for row in wave7)
    assert all(row.get("researched_at") == "2026-09-07" for row in wave7)
    assert all(5 <= (row.get("employees") or 0) <= 500 for row in wave7)
    assert sum(1 for row in wave7 if row.get("email")) >= 140
    assert sum(1 for row in wave7 if not row.get("email")) >= 20
    assert {row["sector"] for row in wave7} >= {
        "Technologie",
        "Services professionnels",
        "Assurance",
        "Santé privée",
        "Construction",
    }
    # Nouvel angle : pas seulement l’usine / l’entrepôt.
    assert sum(1 for row in wave7 if row["sector"] in {"Technologie", "Services professionnels", "Assurance"}) >= 40
    wave8 = QUEBEC_EMPLOYER_LEADS[724:924]
    assert len(wave8) == 200
    assert all(row.get("lead_score") for row in wave8)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C"} for row in wave8)
    assert all(row.get("researched_at") == "2026-09-07" for row in wave8)
    assert all(5 <= (row.get("employees") or 0) <= 500 for row in wave8)
    assert sum(1 for row in wave8 if row.get("email")) >= 120
    assert sum(1 for row in wave8 if not row.get("email")) >= 20
    assert all(row.get("commercial_priority") in {"A", "B", "C", "D"} for row in wave8)
    fieldish = {
        "Protection incendie / gicleurs",
        "Maintenance industrielle",
        "Électricité industrielle",
        "Plomberie CMMTQ",
        "NDT / essais",
        "Restauration après sinistre",
    }
    assert {row["sector"] for row in wave8} & fieldish
    # 3e génération : terrain / certifications, pas seulement usine ou techno.
    assert sum(
        1
        for row in wave8
        if "FIELD_WORK" in (row.get("lead_categories") or "")
        or "CERTIFICATION_REQUIRED" in (row.get("lead_categories") or "")
    ) >= 80
    wave9 = QUEBEC_EMPLOYER_LEADS[924:1180]
    assert len(wave9) == 256
    assert all(row.get("lead_score") for row in wave9)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C", "D"} for row in wave9)
    assert all(row.get("researched_at") == "2026-09-08" for row in wave9)
    assert all(row.get("source", "").startswith("vague 9") for row in wave9)
    assert all("INDEED_DISCOVERY" in (row.get("lead_categories") or "") for row in wave9)
    assert any(row["name"] == "Kraft Heinz Canada" for row in wave9)
    kraft = next(row for row in wave9 if row["name"] == "Kraft Heinz Canada")
    assert kraft["lead_score"] >= 80
    assert kraft["lead_priority"] in {"A", "A+"}
    assert kraft.get("indeed_job_url")
    assert "Talent Acquisition" in (kraft.get("indeed_job_title") or "")
    assert kraft.get("talendus_opportunity")
    assert not kraft.get("email"), "Pas de courriel inventé pour Kraft Heinz"
    assert sum(1 for row in wave9 if "INTERNAL_TA_HIRE" in (row.get("lead_categories") or "")) >= 40
    assert sum(1 for row in wave9 if int(row.get("total_active_jobs") or 0) >= 10) >= 40
    assert {row["city"] for row in wave9} >= {"Montréal", "Québec", "Laval", "Lévis", "Mont-Royal"}
    wave10 = QUEBEC_EMPLOYER_LEADS[1180:]
    assert len(wave10) == 253
    assert all(row.get("source", "").startswith("vague 10") for row in wave10)
    assert all(row.get("lead_score") for row in wave10)
    assert all(row.get("lead_priority") in {"A+", "A", "B", "C", "D"} for row in wave10)
    from app.data.contact_finder_finds import DEEP_CONTACT_FINDS

    for row in wave10:
        if not row.get("email"):
            continue
        finds = DEEP_CONTACT_FINDS.get(row["name"]) or []
        assert any((item.get("email") or "").lower() == row["email"].lower() for item in finds), (
            f"Courriel vague 10 non sourcé Deep Contact : {row['name']} {row['email']}"
        )
    stm = next(row for row in wave10 if row["name"] == "STM")
    assert not stm.get("email"), "STM : portail only, pas d’adresse inventée"
    assert any(row["name"] == "STM" for row in wave10)
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
    from app.data.quebec_employer_email_enrichment import PUBLIC_EMAILS, apply_public_emails

    catalog_names = {row["name"] for row in QUEBEC_EMPLOYER_LEADS}
    assert set(PUBLIC_EMAILS) <= catalog_names
    for name, patch in PUBLIC_EMAILS.items():
        lead = next(row for row in QUEBEC_EMPLOYER_LEADS if row["name"] == name)
        assert lead["email"] == patch["email"]
        assert lead.get("email_source")
        assert lead.get("email_source_url")
        assert lead.get("email_confidence") in {"VERIFIED_HIGH", "VERIFIED_MEDIUM", "PUBLIC_UNVERIFIED"}
        assert "@" in patch["email"]
        assert "example." not in patch["email"]
    dummy = ({"name": "Entreprise Inconnue", "email": None, "hiring": ""},)
    assert apply_public_emails(dummy)[0]["email"] is None
    existing = ({"name": "Exceldor", "email": "deja@exceldor.com", "hiring": ""},)
    assert apply_public_emails(existing)[0]["email"] == "deja@exceldor.com"


def test_ensure_creates_prospect_clients_without_employer_accounts(client, db):
    promote_admin(client, "leads-admin@talendus.ca")
    created = ensure_quebec_employer_leads(db)
    db.commit()
    assert created == 1433
    assert ensure_quebec_employer_leads(db) == 0
    db.commit()

    leads = list(db.scalars(select(Company).where(Company.name.in_([r["name"] for r in QUEBEC_EMPLOYER_LEADS]))))
    assert len(leads) == 1433
    assert all(c.status == CompanyStatus.PROSPECT for c in leads)
    assert all(c.province == "Québec" for c in leads)
    assert all(not c.owner_user_id for c in leads)
    assert db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.EMPLOYER)) == 0

    with_email = [r for r in QUEBEC_EMPLOYER_LEADS if r.get("email")]
    prospects = list(db.scalars(select(Prospect).where(Prospect.side == "employer", Prospect.source == "prospection")))
    emails = {p.email for p in prospects}
    for row in with_email:
        assert row["email"].lower() in emails
    exceldor = next(p for p in prospects if p.email == "info@exceldor.com")
    assert exceldor.company_name == "Exceldor"
    assert exceldor.stage == "a-contacter"
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
    db.commit()
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
    assert created == 1433


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
    assert created == 1432
    velans = list(db.scalars(select(Company).where(Company.name.ilike("%velan%"))))
    assert len(velans) == 1
    assert velans[0].name == "Velan Inc."
    assert not db.scalar(select(Prospect.id).where(Prospect.company_name == "Velan"))
    assert not db.scalar(select(Prospect.id).where(Prospect.email == "leads-dedupe@talendus.ca", Prospect.source == "prospection"))
    assert ensure_quebec_employer_leads(db) == 0


def test_sync_catalog_emails_fills_existing_only(client, db):
    promote_admin(client, "leads-sync@talendus.ca")
    db.add(
        Company(
            name="Exceldor",
            status=CompanyStatus.PROSPECT,
            city="Lévis",
            sector="Transformation alimentaire",
            province="Québec",
            country="Canada",
        )
    )
    db.add(
        Company(
            name="Hors Catalogue",
            status=CompanyStatus.PROSPECT,
            province="Québec",
            country="Canada",
        )
    )
    db.commit()
    before = db.scalar(select(func.count()).select_from(Company))
    filled = sync_catalog_emails_to_crm(db)
    db.commit()
    assert filled == 1
    exceldor = db.scalar(select(Company).where(Company.name == "Exceldor"))
    assert exceldor.email == "info@exceldor.com"
    unknown = db.scalar(select(Company).where(Company.name == "Hors Catalogue"))
    assert not unknown.email
    assert db.scalar(select(func.count()).select_from(Company)) == before
    assert db.scalar(select(Company).where(Company.name == "Olymel")) is None
    prospect = db.scalar(select(Prospect).where(Prospect.email == "info@exceldor.com"))
    assert prospect is not None
    assert prospect.company_name == "Exceldor"
    assert prospect.side == "employer"
    assert prospect.stage == "a-contacter"
    assert sync_catalog_emails_to_crm(db) == 0


def test_sync_catalog_emails_does_not_overwrite(client, db):
    promote_admin(client, "leads-keep@talendus.ca")
    db.add(
        Company(
            name="Exceldor",
            email="deja@exceldor.com",
            status=CompanyStatus.PROSPECT,
            province="Québec",
            country="Canada",
        )
    )
    db.commit()
    assert sync_catalog_emails_to_crm(db) == 0
    db.commit()
    row = db.scalar(select(Company).where(Company.name == "Exceldor"))
    assert row.email == "deja@exceldor.com"
    assert not db.scalar(select(Prospect.id).where(Prospect.email == "info@exceldor.com"))


def test_crm_lists_show_enriched_company_after_sync(client, db):
    from tests.conftest import auth_header

    admin = promote_admin(client, "leads-crm-visible@talendus.ca")
    db.add(
        Company(
            name="Exceldor",
            status=CompanyStatus.PROSPECT,
            city="Lévis",
            sector="Transformation alimentaire",
            province="Québec",
            country="Canada",
        )
    )
    db.add(
        Company(
            name="Avior Integrated Products",
            status=CompanyStatus.PROSPECT,
            city="Laval",
            sector="Aéronautique",
            province="Québec",
            country="Canada",
        )
    )
    db.commit()
    headers = auth_header(admin)
    boot = client.get("/api/admin/bootstrap", headers=headers)
    assert boot.status_code == 200, boot.text
    clients = boot.json()["data"]["clients"]
    exceldor = next(row for row in clients if row["name"] == "Exceldor")
    avior = next(row for row in clients if row["name"] == "Avior Integrated Products")
    assert not any(row["name"] == "Olymel" for row in clients)
    assert exceldor["email"] == "info@exceldor.com"
    assert exceldor["readyToContact"] is True
    assert exceldor.get("prospectId")
    assert avior["email"] == "rh_laval@avior.ca"
    assert avior["readyToContact"] is True
    listed = client.get("/api/admin/prospects?side=employer", headers=headers)
    assert listed.status_code == 200, listed.text
    rows = listed.json()["data"]
    emails = {row["email"] for row in rows}
    assert "info@exceldor.com" in emails
    assert "rh_laval@avior.ca" in emails
    found = client.get("/api/admin/prospects?side=employer&email=found", headers=headers)
    assert found.status_code == 200, found.text
    found_emails = {row["email"] for row in found.json()["data"]}
    assert "info@exceldor.com" in found_emails
    assert "rh_laval@avior.ca" in found_emails
    refresh = client.post("/api/admin/employer-leads/refresh?force=1", headers=headers)
    assert refresh.status_code == 200, refresh.text
    stats = refresh.json()["data"]
    assert stats["catalog_with_email"] >= 460
    assert stats["prospects_with_catalog_email"] >= 460
    assert stats["companies_with_catalog_email"] >= 460
    boot2 = client.get("/api/admin/bootstrap", headers=headers)
    assert boot2.status_code == 200, boot2.text
    catalog = boot2.json()["data"].get("employerCatalog") or {}
    assert catalog.get("catalog_with_email", 0) >= 460
    clients2 = boot2.json()["data"]["clients"]
    olymel = next(row for row in clients2 if row["name"] == "Olymel")
    assert olymel["email"] == "talent@olymel.com"
    assert olymel.get("prospectId")
    with_email = [row for row in clients2 if (row.get("email") or "").strip()]
    assert len(with_email) >= 460
    listed2 = client.get("/api/admin/prospects?side=employer&email=with", headers=headers)
    assert listed2.status_code == 200, listed2.text
    assert len(listed2.json()["data"]) >= 460


def test_bootstrap_recovers_prod_stuck_at_406(client, db):
    """Prod à 406 : les fiches existent, les courriels OSINT n’ont jamais été recopiés."""
    from tests.conftest import auth_header

    admin = promote_admin(client, "leads-406@talendus.ca")
    ensure_quebec_employer_leads(db)
    db.commit()
    with_email = [row for row in QUEBEC_EMPLOYER_LEADS if row.get("email")]
    stripped = with_email[-200:]
    for row in stripped:
        company = db.scalar(select(Company).where(Company.name == row["name"]))
        assert company is not None
        company.email = None
        prospect = db.scalar(select(Prospect).where(Prospect.email == row["email"].lower()))
        if prospect is not None:
            db.delete(prospect)
    db.commit()
    before_companies = db.scalar(select(func.count()).select_from(Company))
    remaining = db.scalar(
        select(func.count()).select_from(Company).where(Company.email.is_not(None)).where(Company.email != "")
    )
    assert remaining is not None
    # Les 200 derniers courriels du catalogue ont été retirés : on est
    # clairement sous le total (752 après la vague 8), pas sous un seuil figé.
    assert remaining < len(with_email) - 150
    headers = auth_header(admin)
    boot = client.get("/api/admin/bootstrap", headers=headers)
    assert boot.status_code == 200, boot.text
    catalog = boot.json()["data"].get("employerCatalog") or {}
    assert catalog.get("companies_with_catalog_email", 0) >= 460
    assert catalog.get("prospects_with_catalog_email", 0) >= 460
    assert db.scalar(select(func.count()).select_from(Company)) == before_companies
    clients = {row["name"]: row for row in boot.json()["data"]["clients"]}
    for row in stripped:
        assert clients[row["name"]]["email"] == row["email"]
        assert clients[row["name"]].get("prospectId")


def test_indeed_watch_endpoint_lists_kraft_heinz_first(client):
    from tests.conftest import auth_header

    admin = promote_admin(client, "indeed-watch@talendus.ca")
    res = client.get("/api/admin/employer-leads/indeed-watch", headers=auth_header(admin))
    assert res.status_code == 200, res.text
    payload = res.json()["data"]
    summary = payload["summary"]
    leads = payload["leads"]
    assert summary["total"] >= 200
    assert summary["priority_a"] >= 20
    assert summary["hiring_recruiters"] >= 40
    assert leads[0]["lead_score"] >= leads[-1]["lead_score"]
    kraft = next(row for row in leads if row["company_name"] == "Kraft Heinz Canada")
    assert kraft["priority"] == "A"
    assert kraft["professional_email"] in {None, ""}
    assert kraft["indeed_job_url"]
    assert kraft["talendus_opportunity"]
    assert kraft["city"] == "Mont-Royal"


def test_lead_intelligence_endpoint_lists_kraft_as_hot(client):
    from tests.conftest import auth_header

    admin = promote_admin(client, "lead-intel@talendus.ca")
    res = client.get("/api/admin/employer-leads/intelligence?view=hot", headers=auth_header(admin))
    assert res.status_code == 200, res.text
    payload = res.json()["data"]
    report = payload["report"]
    leads = payload["leads"]
    assert report["unique_after_dedupe"] >= 500
    assert report["priority_a_plus"] >= 1
    assert leads
    assert all(row["priority"] == "A+" for row in leads)
    assert leads[0]["lead_score"] >= leads[-1]["lead_score"]
    kraft = next(row for row in payload["leads"] if row["company_name"] == "Kraft Heinz Canada")
    assert kraft["lead_score"] >= 90
    assert kraft["professional_email"] == "NOT_FOUND"
    assert "Indeed" in kraft["sources_found"]
    assert kraft["talendus_opportunity"]


def test_contact_finder_endpoint_lists_loto_and_keeps_kraft_without_email(client):
    from tests.conftest import auth_header

    admin = promote_admin(client, "deep-contact@talendus.ca")
    res = client.get("/api/admin/employer-leads/contact-finder?view=now", headers=auth_header(admin))
    assert res.status_code == 200, res.text
    payload = res.json()["data"]
    report = payload["report"]
    assert report["companies_analyzed"] == 1433
    assert report["emails_found"] >= 750
    assert report["no_email"] >= 1
    assert len(report["failed_top20"]) == 20
    assert all(row.get("primary_email") for row in payload["leads"])
    all_res = client.get("/api/admin/employer-leads/contact-finder?view=all", headers=auth_header(admin))
    leads = {row["company_name"]: row for row in all_res.json()["data"]["leads"]}
    assert leads["Loto-Québec"]["primary_email"] == "support.rh@loto-quebec.com"
    assert leads["Kraft Heinz Canada"]["primary_email"] == ""
    assert leads["Kraft Heinz Canada"]["email_search_status"] == "CONTACT_FOUND_EMAIL_NOT_FOUND"
    assert leads["Kraft Heinz Canada"]["primary_contact_name"] == "Heidi Turner"
