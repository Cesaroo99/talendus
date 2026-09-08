from app.services.indeed_prospecting import (
    compile_indeed_leads,
    merge_rows,
    priority_for,
    score_signals,
    summarize_indeed_leads,
    talendus_opportunity,
)


def test_score_ta_specialist_and_volume_is_priority_a():
    scored = score_signals(
        {
            "indeed_job_title": "Talent Acquisition Specialist",
            "hires_recruiter": True,
            "multi_rh": True,
            "total_active_jobs": 37,
            "operational_mass": True,
            "multi_city": True,
            "career_page": True,
            "days_since_posting": 5,
        }
    )
    assert scored["lead_score"] >= 80
    assert scored["lead_priority"] in {"A", "A+"}
    assert scored["recruiter_signal"] is True


def test_staffing_agency_is_capped():
    scored = score_signals(
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
    assert scored["lead_priority"] == "C"


def test_old_posting_is_discounted():
    fresh = score_signals({"indeed_job_title": "Recruiter", "days_since_posting": 3})
    stale = score_signals({"indeed_job_title": "Recruiter", "days_since_posting": 90})
    assert fresh["lead_score"] > stale["lead_score"]


def test_priority_bands():
    assert priority_for(95) == "A+"
    assert priority_for(80) == "A"
    assert priority_for(60) == "B"
    assert priority_for(40) == "C"
    assert priority_for(20) == "D"


def test_dedupe_merges_same_company():
    merged = merge_rows(
        [
            {
                "name": "Kraft Heinz Canada",
                "website": "https://www.kraftheinz.com",
                "city": "Mont-Royal",
                "indeed_job_title": "Recruiter",
                "total_active_jobs": 8,
                "recruitment_jobs": 1,
            },
            {
                "name": "Kraft Heinz Canada",
                "website": "https://www.kraftheinz.com",
                "city": "Montréal",
                "indeed_job_title": "Talent Acquisition Partner",
                "total_active_jobs": 19,
                "recruitment_jobs": 1,
                "operational_mass": True,
            },
        ]
    )
    assert len(merged) == 1
    assert merged[0]["total_active_jobs"] == 19
    assert merged[0]["recruitment_jobs"] == 2
    assert merged[0]["operational_mass"] is True


def test_compile_kraft_heinz_style_lead_has_opportunity_and_no_invented_email():
    leads = compile_indeed_leads(
        [
            {
                "name": "Kraft Heinz Canada",
                "legal_name": "Kraft Heinz Canada ULC",
                "sector": "Transformation alimentaire",
                "city": "Mont-Royal",
                "website": "https://www.kraftheinz.com",
                "indeed_job_title": "Talent Acquisition Specialist",
                "indeed_job_url": "https://ca.indeed.com/cmp/Kraft-Heinz-3e502a27",
                "total_active_jobs": 19,
                "hires_ta_specialist": True,
                "hires_recruiter": True,
                "operational_mass": True,
                "multi_city": True,
                "career_page": True,
                "days_since_posting": 10,
            }
        ]
    )
    assert len(leads) == 1
    lead = leads[0]
    assert lead["email"] is None
    assert lead["lead_score"] >= 80
    assert "Indeed" in lead["source"]
    assert "partenariat externe" in (lead["talendus_opportunity"] or "").lower() or "Talendus" in (
        lead["talendus_opportunity"] or ""
    )
    assert lead["indeed_job_url"].startswith("https://")


def test_opportunity_mentions_operational_volume():
    text = talendus_opportunity(
        {
            "name": "Entrepôt Nord",
            "sector": "logistique",
            "total_active_jobs": 22,
            "operational_mass": True,
            "indeed_job_title": "Cariste",
        },
        {"recruiter_signal": False, "staffing_agency": False},
    )
    assert "opérationnel" in text.lower() or "cariste" in text.lower()


def test_summarize_counts_priorities():
    leads = [
        {"lead_priority": "A+", "lead_categories": "INTERNAL_TA_HIRE", "total_active_jobs": 25, "email": None, "sector": "Finance", "city": "Montréal"},
        {"lead_priority": "B", "lead_categories": "", "total_active_jobs": 12, "email": "rh@ok.example", "sector": "Finance", "city": "Québec", "contact_name": "Ada", "contact_title": "DRH"},
        {"lead_priority": "C", "lead_categories": "", "total_active_jobs": 2, "email": None, "sector": "Commerce", "city": "Laval"},
    ]
    summary = summarize_indeed_leads(leads)
    assert summary["total"] == 3
    assert summary["priority_a"] == 1
    assert summary["priority_b"] == 1
    assert summary["jobs_10_plus"] == 2
    assert summary["jobs_20_plus"] == 1
    assert summary["emails"] == 1
    assert summary["decision_makers"] == 1
    assert summary["hiring_recruiters"] == 1
