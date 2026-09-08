from app.data.contact_finder_bundle import CONTACT_FINDER, CONTACT_FINDER_REPORT
from app.data.contact_finder_finds import DEEP_CONTACT_FINDS
from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.services.contact_finder import (
    MIN_PRIMARY_CONFIDENCE,
    STATUS_CONTACT_NO_EMAIL,
    STATUS_EXHAUSTED,
    STATUS_FOUND_HIGH,
    STATUS_GENERIC_ONLY,
    STATUS_PATTERN,
    apply_finder_to_lead,
    compile_contact_finder,
    confidence_score,
    contact_relevance,
    filter_view,
    finder_report,
    merge_contacts,
    pick_primary,
    to_finder_record,
)
from app.services.contact_finder_providers import (
    PROVIDERS,
    deep_search_queries,
    should_refresh,
)


def test_ta_manager_outranks_info_mailbox():
    assert contact_relevance("Talent Acquisition Manager", "marie@abc.ca", 400) == 100
    assert contact_relevance("", "info@abc.ca", 400) == 30
    assert contact_relevance("Marketing Director", "pierre@abc.ca", 400) == 20


def test_owner_priority_depends_on_company_size():
    assert contact_relevance("Président / fondateur", "owner@pme.ca", 12) == 78
    assert contact_relevance("Owner", "owner@corp.ca", 800) == 55


def test_guessed_pattern_never_becomes_primary():
    chosen = pick_primary(
        None,
        [
            {
                "email": "jean.tremblay@acme.ca",
                "contact_name": "Jean Tremblay",
                "contact_title": "Talent Acquisition Manager",
                "guessed": True,
                "status": STATUS_PATTERN,
                "confidence_score": 40,
                "source_type": "search",
            }
        ],
        "https://www.acme.ca",
        200,
    )
    assert chosen is None or not chosen.get("email")


def test_confidence_below_50_is_not_primary():
    chosen = pick_primary(
        None,
        [
            {
                "email": "maybe@acme.ca",
                "confidence_score": 49,
                "source_type": "search",
                "discovered_at": "2026-09-08",
            }
        ],
        "https://www.acme.ca",
        80,
    )
    assert chosen is None
    assert MIN_PRIMARY_CONFIDENCE == 70


def test_verified_named_contact_is_not_overwritten_by_info():
    existing = {
        "email": "marie@entreprise.ca",
        "contact_name": "Marie Tremblay",
        "contact_title": "Directrice des ressources humaines",
        "confidence_score": 95,
        "source_type": "website",
        "keep": True,
    }
    winner = pick_primary(
        existing,
        [
            {
                "email": "info@entreprise.ca",
                "confidence_score": 90,
                "source_type": "website",
                "discovered_at": "2026-09-08",
            }
        ],
        "https://www.entreprise.ca",
        250,
    )
    assert winner["email"] == "marie@entreprise.ca"


def test_generic_catalog_email_can_upgrade_to_hr():
    lead = {
        "name": "Usine Demo",
        "email": "info@usine-demo.example",
        "website": "https://www.usine-demo.example",
        "hiring": "info@ déjà au catalogue.",
    }
    record = {
        "primary_email": "rh@usine-demo.example",
        "primary_contact_name": "",
        "primary_contact_title": "Ressources humaines",
        "primary_email_confidence": 92,
        "primary_email_source": "page carrières",
        "primary_email_source_url": "https://www.usine-demo.example/carrieres",
        "contact_relevance_score": 65,
        "email_verified": True,
        "email_last_verified_at": "2026-09-08",
        "secondary_emails": ["info@usine-demo.example"],
        "email_search_status": STATUS_FOUND_HIGH,
    }
    out = apply_finder_to_lead(lead, record)
    assert out["email"] == "rh@usine-demo.example"
    assert out["email_source_url"] == "https://www.usine-demo.example/carrieres"


def test_dedupes_near_duplicate_people():
    merged = merge_contacts(
        [
            {"email": "j.tremblay@abc.ca", "contact_name": "Jean Tremblay", "contact_title": "HR", "confidence_score": 80},
            {"email": "jean.tremblay@abc.ca", "contact_name": "Jean A. Tremblay", "contact_title": "HR Manager", "confidence_score": 90},
            {"email": "", "contact_name": "J. Tremblay", "contact_title": "Recruiter", "confidence_score": 70},
        ]
    )
    assert len(merged) == 1
    assert merged[0]["contact_name"] == "Jean A. Tremblay"


def test_kraft_has_ta_contact_but_no_invented_email():
    kraft = next(row for row in QUEBEC_EMPLOYER_LEADS if row["name"] == "Kraft Heinz Canada")
    assert not kraft.get("email")
    assert kraft.get("contact_name") == "Heidi Turner"
    record = next(row for row in CONTACT_FINDER if row["company_name"] == "Kraft Heinz Canada")
    assert record["primary_email"] == ""
    assert record["email_search_status"] == STATUS_CONTACT_NO_EMAIL
    assert record["primary_contact_title"].startswith("Talent Acquisition")
    assert record["bucket"] == "needs_research"


def test_loto_quebec_uses_public_hr_mailbox():
    loto = next(row for row in QUEBEC_EMPLOYER_LEADS if row["name"] == "Loto-Québec")
    assert loto["email"] == "support.rh@loto-quebec.com"
    assert loto.get("email_source_url")
    record = next(row for row in CONTACT_FINDER if row["company_name"] == "Loto-Québec")
    assert record["primary_email"] == "support.rh@loto-quebec.com"
    assert record["primary_email_confidence"] >= 85
    assert record["contact_relevance_score"] >= 65


def test_catalog_unchanged_size_and_no_guessed_primary():
    assert len(QUEBEC_EMPLOYER_LEADS) == 1433
    assert len(CONTACT_FINDER) == 1433
    sourced = {
        (item.get("email") or "").lower()
        for rows in DEEP_CONTACT_FINDS.values()
        for item in rows
        if item.get("email")
    }
    names = [row["name"] for row in QUEBEC_EMPLOYER_LEADS]
    assert len(set(names)) == 1433
    for row in CONTACT_FINDER:
        assert row["email_search_status"] != STATUS_PATTERN
        if row.get("primary_email"):
            assert "@" in row["primary_email"]
            assert not row["primary_email"].startswith("prenom.nom")
            local = row["primary_email"].split("@", 1)[0]
            assert local not in {"jean.tremblay", "john.doe"}
            if row["primary_email"].lower() in sourced:
                assert row["primary_email_confidence"] >= 70


def test_finds_only_target_existing_companies():
    catalog = {row["name"] for row in QUEBEC_EMPLOYER_LEADS}
    assert set(DEEP_CONTACT_FINDS) <= catalog
    for rows in DEEP_CONTACT_FINDS.values():
        for item in rows:
            if item.get("email"):
                assert "@" in item["email"]
                assert not item.get("guessed")


def test_views_and_report_buckets():
    now = filter_view(CONTACT_FINDER, "now")
    contactable = filter_view(CONTACT_FINDER, "contactable")
    research = filter_view(CONTACT_FINDER, "needs_research")
    missing = filter_view(CONTACT_FINDER, "no_email")
    assert now
    assert contactable
    assert research
    assert missing
    assert all(row["bucket"] == "now" for row in now)
    assert all(row.get("primary_email") for row in now)
    assert all(not row.get("primary_email") for row in missing)
    report = finder_report(CONTACT_FINDER)
    assert report["companies_analyzed"] == 1433
    assert report["emails_found"] == CONTACT_FINDER_REPORT["emails_found"]
    assert report["recovery_rate"] == CONTACT_FINDER_REPORT["recovery_rate"]
    assert len(report["failed_top20"]) == 20
    assert report["failed_top20"][0]["company_name"] == "Kraft Heinz Canada"
    kraft = next(row for row in research if row["company_name"] == "Kraft Heinz Canada")
    assert kraft["email_search_status"] == STATUS_CONTACT_NO_EMAIL


def test_desjardins_exhausted_without_invented_inbox():
    row = next(item for item in CONTACT_FINDER if item["company_name"] == "Desjardins")
    assert not row.get("primary_email")
    assert row["email_search_status"] == STATUS_EXHAUSTED
    assert row["email_search_depth"] == 6


def test_polytechnique_prefers_named_hr_over_generic():
    row = next(item for item in CONTACT_FINDER if item["company_name"] == "Polytechnique Montréal")
    assert row["primary_email"] == "brigitte.morneau@polymtl.ca"
    assert row["primary_contact_name"] == "Brigitte Morneau"
    assert "stc@polymtl.ca" in (row.get("secondary_emails") or [])
    assert row["contact_relevance_score"] >= 88


def test_providers_are_pluggable_and_queries_are_multi_pass():
    assert len(PROVIDERS) == 6
    queries = deep_search_queries(
        {
            "name": "ABC Manufacturing",
            "legal_name": "ABC Manufacturing inc.",
            "city": "Trois-Rivières",
            "website": "https://www.abcmanufacturing.ca",
            "contact_name": "Marie Tremblay",
        }
    )
    blobs = " | ".join(row["query"] for row in queries)
    assert '"ABC Manufacturing" email' in blobs
    assert "talent acquisition" in blobs
    assert "ressources humaines" in blobs
    assert '"@abcmanufacturing.ca"' in blobs
    assert "filetype:pdf" in blobs
    assert '"Marie Tremblay" email' in blobs
    assert not should_refresh("2026-09-01", "2026-09-08")
    assert should_refresh("2026-01-01", "2026-09-08")


def test_generic_only_status_for_info_mailbox():
    record = to_finder_record(
        {"name": "Héma-Québec", "website": "https://www.hema-quebec.qc.ca", "lead_score": 80, "employees": 1400},
        {
            "email": "info@hema-quebec.qc.ca",
            "source_type": "website",
            "confidence_score": 90,
            "discovered_at": "2026-09-08",
        },
        [],
    )
    assert record["email_search_status"] == STATUS_GENERIC_ONLY
    assert record["contact_relevance_score"] == 30


def test_compile_does_not_create_companies():
    extra = compile_contact_finder(QUEBEC_EMPLOYER_LEADS[:3], {})
    assert len(extra) == 3
    assert {row["company_name"] for row in extra} == {row["name"] for row in QUEBEC_EMPLOYER_LEADS[:3]}


def test_gmail_is_rejected_unless_official_domain():
    assert confidence_score({"email": "rh@gmail.com", "confidence_score": 99, "source_type": "website"}, "https://www.acme.ca") <= 45
    chosen = pick_primary(
        None,
        [{"email": "boss@gmail.com", "contact_title": "Owner", "confidence_score": 96, "source_type": "website"}],
        "https://www.acme.ca",
        12,
    )
    assert chosen is None
