from app.data.lead_intelligence_bundle import LEAD_INTELLIGENCE, LEAD_INTELLIGENCE_REPORT
from app.data.lead_intelligence_overlays import apply_overlays
from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.data.quebec_employer_leads_wave10 import QUEBEC_EMPLOYER_LEADS_WAVE10
from app.services.lead_intelligence import (
    EMAIL_NOT_FOUND,
    compile_intelligence,
    filter_view,
    merge_intelligence,
    priority_for,
    recruitment_volume,
    score_intelligence,
)


def test_new_score_bands():
    assert priority_for(95) == "A+"
    assert priority_for(80) == "A"
    assert priority_for(65) == "B"
    assert priority_for(50) == "C"
    assert priority_for(49) == "D"


def test_score_ta_recruiter_volume_and_recency():
    scored = score_intelligence(
        {
            "indeed_job_title": "Talent Acquisition Specialist",
            "hires_recruiter": True,
            "multi_rh": True,
            "total_active_jobs": 52,
            "expansion": True,
            "many_specialized": True,
            "multi_city": True,
            "days_since_posting": 4,
        }
    )
    assert scored["lead_score"] == 100
    assert scored["priority"] == "A+"
    assert scored["internal_recruitment_signal"] is True


def test_volume_is_max_not_sum():
    assert recruitment_volume({"linkedin_jobs": 8, "indeed_jobs": 19, "active_jobs_total": 19}) == 19


def test_staffing_agency_is_capped():
    scored = score_intelligence(
        {
            "name": "Randstad Canada",
            "sector": "Agence de placement",
            "indeed_job_title": "Recruiter",
            "total_active_jobs": 40,
            "days_since_posting": 3,
        }
    )
    assert scored["staffing_agency"] is True
    assert scored["lead_score"] <= 49


def test_dedupe_merges_same_company():
    merged = merge_intelligence(
        [
            {
                "name": "Entreprise X",
                "website": "https://www.entreprise-x.example",
                "indeed_job_title": "Talent Acquisition Partner",
                "total_active_jobs": 4,
                "sources_found": ["LinkedIn Jobs"],
            },
            {
                "name": "Entreprise X",
                "website": "https://www.entreprise-x.example",
                "total_active_jobs": 25,
                "expansion": True,
                "sources_found": ["Indeed", "Company Website"],
            },
        ]
    )
    assert len(merged) == 1
    assert merged[0]["total_active_jobs"] == 25
    assert merged[0]["expansion"] is True
    assert "LinkedIn Jobs" in merged[0]["sources_found"]
    assert "Indeed" in merged[0]["sources_found"]


def test_email_not_found_is_explicit():
    records = compile_intelligence(
        [
            {
                "name": "Sans Courriel Public",
                "website": "https://www.sans-courriel.example",
                "city": "Montréal",
                "sector": "Manufacturier",
                "total_active_jobs": 12,
                "indeed_job_title": "Recruteur",
            }
        ]
    )
    assert records[0]["professional_email"] == EMAIL_NOT_FOUND


def test_intelligence_has_500_unique_and_kraft_is_hot():
    names = [row["company_name"] for row in LEAD_INTELLIGENCE]
    assert len(LEAD_INTELLIGENCE) >= 500
    assert len(set(names)) == len(names)
    websites = [row["website"] for row in LEAD_INTELLIGENCE]
    assert len(set(websites)) == len(websites)
    kraft = next(row for row in LEAD_INTELLIGENCE if row["company_name"] == "Kraft Heinz Canada")
    assert kraft["lead_score"] >= 90
    assert kraft["priority"] == "A+"
    assert kraft["professional_email"] == EMAIL_NOT_FOUND
    assert "Indeed" in kraft["sources_found"]
    assert kraft["ats_platform"] == "Workday"
    assert "Talent Acquisition" in (kraft.get("indeed_job_title") or "")
    assert kraft["talendus_opportunity"]
    assert LEAD_INTELLIGENCE[0]["lead_score"] >= LEAD_INTELLIGENCE[-1]["lead_score"]
    assert LEAD_INTELLIGENCE_REPORT["unique_after_dedupe"] == len(LEAD_INTELLIGENCE)
    assert LEAD_INTELLIGENCE_REPORT["priority_a_plus"] >= 1
    assert LEAD_INTELLIGENCE_REPORT["hiring_recruiters"] >= 40
    assert len(LEAD_INTELLIGENCE_REPORT["top20"]) == 20
    assert filter_view(LEAD_INTELLIGENCE, "hot")
    assert filter_view(LEAD_INTELLIGENCE, "quebec")
    assert filter_view(LEAD_INTELLIGENCE, "talent_acquisition")
    assert all(row["professional_email"] != "" for row in LEAD_INTELLIGENCE)
    assert not any(
        row["professional_email"] not in {EMAIL_NOT_FOUND}
        and "@" not in (row["professional_email"] or "")
        for row in LEAD_INTELLIGENCE
        if row["professional_email"] != EMAIL_NOT_FOUND
    )


def test_wave10_is_catalog_extension_without_invented_email():
    assert QUEBEC_EMPLOYER_LEADS_WAVE10
    names = [row["name"] for row in QUEBEC_EMPLOYER_LEADS_WAVE10]
    assert len(set(names)) == len(names)
    catalog_before = {row["name"].casefold() for row in QUEBEC_EMPLOYER_LEADS[:1180]}
    assert not (set(n.casefold() for n in names) & catalog_before)
    assert all(row.get("source", "").startswith("vague 10") for row in QUEBEC_EMPLOYER_LEADS_WAVE10)
    assert all(row.get("lead_score") for row in QUEBEC_EMPLOYER_LEADS_WAVE10)
    assert all(not row.get("email") for row in QUEBEC_EMPLOYER_LEADS_WAVE10)
    assert any(row["name"] == "STM" for row in QUEBEC_EMPLOYER_LEADS_WAVE10)
    stm = next(row for row in QUEBEC_EMPLOYER_LEADS_WAVE10 if row["name"] == "STM")
    assert stm["lead_score"] >= 65
    assert stm.get("talendus_opportunity")


def test_apply_overlays_adds_workday_to_kraft():
    rows = apply_overlays(
        [
            {
                "name": "Kraft Heinz Canada",
                "website": "https://www.kraftheinz.com",
                "total_active_jobs": 19,
            }
        ]
    )
    assert rows[0]["ats_platform"] == "Workday"
    assert rows[0]["linkedin_jobs"] == 8
