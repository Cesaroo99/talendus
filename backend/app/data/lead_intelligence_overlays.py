"""Croisements multi-sources documentés (pages indexées, pas de scrap).

Ne fait qu’enrichir une fiche déjà découverte. Les volumes par board
sont des observations publiques, jamais additionnés (dédup dans le score).
"""

from __future__ import annotations

# name -> extra fields
SOURCE_OVERLAYS: dict[str, dict] = {
    "Kraft Heinz Canada": {
        "linkedin_jobs": 8,
        "indeed_jobs": 19,
        "career_page_jobs": 19,
        "career_page": "https://jobs.kraftheinz.com/careers",
        "ats_platform": "Workday",
        "linkedin_company": "https://www.linkedin.com/company/the-kraft-heinz-company",
        "expansion": True,
        "difficult": True,
        "multi_province": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
        "source_urls": [
            "https://ca.indeed.com/cmp/Kraft-Heinz-3e502a27",
            "https://jobs.kraftheinz.com/careers",
        ],
    },
    "Capgemini Canada": {
        "linkedin_jobs": 20,
        "indeed_jobs": 71,
        "career_page": "https://www.capgemini.com/careers",
        "ats_platform": "SuccessFactors",
        "multi_province": True,
        "strong_growth": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "SuccessFactors"],
    },
    "Desjardins": {
        "linkedin_jobs": 40,
        "indeed_jobs": 80,
        "jobillico_jobs": 20,
        "career_page": "https://www.desjardins.com/carrieres",
        "ats_platform": "SuccessFactors",
        "multi_city": True,
        "multi_province": True,
        "expansion": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Jobillico", "Company Website", "SuccessFactors"],
    },
    "Banque Nationale": {
        "linkedin_jobs": 25,
        "indeed_jobs": 60,
        "career_page": "https://carrieres.bnc.ca",
        "ats_platform": "Workday",
        "multi_city": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
    },
    "iA Groupe financier": {
        "linkedin_jobs": 12,
        "indeed_jobs": 35,
        "career_page": "https://ia.ca/emploi/emplois-disponibles",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Jobillico"],
    },
    "Beneva": {
        "linkedin_jobs": 10,
        "indeed_jobs": 40,
        "career_page": "https://www.beneva.ca",
        "strong_growth": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website"],
    },
    "Air Canada": {
        "linkedin_jobs": 20,
        "indeed_jobs": 50,
        "career_page": "https://careers.aircanada.com",
        "ats_platform": "Workday",
        "multi_province": True,
        "difficult": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday", "Eluta"],
    },
    "TELUS": {
        "linkedin_jobs": 18,
        "indeed_jobs": 45,
        "career_page": "https://www.telus.com/fr/about/careers",
        "ats_platform": "Workday",
        "multi_province": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
    },
    "Loblaw": {
        "linkedin_jobs": 15,
        "indeed_jobs": 70,
        "career_page": "https://www.loblaw.ca/fr/carrieres",
        "operational_mass": True,
        "multi_city": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Guichet-Emplois"],
    },
    "Altasciences": {
        "linkedin_jobs": 6,
        "indeed_jobs": 18,
        "career_page": "https://www.altasciences.com/careers",
        "ats_platform": "Workday",
        "growth": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
    },
    "Vantage Data Centers": {
        "linkedin_jobs": 4,
        "career_page": "https://www.vantage-dc.com/careers",
        "expansion": True,
        "sources_found": ["LinkedIn Jobs", "Company Website", "Indeed"],
    },
    "MEDFAR Clinical Solutions": {
        "linkedin_jobs": 3,
        "career_page": "https://www.medfar.ca",
        "growth": True,
        "sources_found": ["LinkedIn Jobs", "Company Website"],
    },
    "Capco": {
        "career_page": "https://job-boards.greenhouse.io/capco",
        "ats_platform": "Greenhouse",
        "growth": True,
        "sources_found": ["Greenhouse", "LinkedIn Jobs", "Company Website"],
    },
    "Agnico Eagle": {
        "linkedin_jobs": 10,
        "indeed_jobs": 25,
        "career_page": "https://careers.agnicoeagle.com",
        "difficult": True,
        "multi_city": True,
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Eluta"],
    },
    "IKEA Canada": {
        "linkedin_jobs": 8,
        "indeed_jobs": 22,
        "career_page": "https://www.ikea.com/ca/fr/jobs",
        "ats_platform": "Workday",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
    },
    "McCain Foods": {
        "career_page": "https://careers.mccain.com",
        "ats_platform": "Workday",
        "difficult": True,
        "sources_found": ["Indeed", "Company Website", "Workday"],
    },
    "Johnson & Johnson": {
        "career_page": "https://www.careers.jnj.com",
        "ats_platform": "Workday",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Workday"],
    },
    "Intact Assurance": {
        "career_page": "https://careers.intactfc.com",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website"],
    },
    "PwC Canada": {
        "career_page": "https://www.pwc.com/ca/fr/careers.html",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website", "Eluta"],
    },
    "Deloitte Canada": {
        "career_page": "https://www2.deloitte.com/ca/fr/careers.html",
        "sources_found": ["Indeed", "LinkedIn Jobs", "Company Website"],
    },
}


def apply_overlays(rows: list[dict]) -> list[dict]:
    out = []
    for raw in rows:
        row = dict(raw)
        extra = SOURCE_OVERLAYS.get(row.get("name") or "")
        if extra:
            for key, value in extra.items():
                if key == "sources_found":
                    current = row.get("sources_found") or []
                    if isinstance(current, str):
                        current = [current]
                    row["sources_found"] = list(dict.fromkeys(list(current) + list(value)))
                elif key == "source_urls":
                    row["source_urls"] = list(dict.fromkeys((row.get("source_urls") or []) + list(value)))
                else:
                    row[key] = value
        elif row.get("indeed_job_url") or row.get("careers_url"):
            sources = ["Indeed"]
            if row.get("careers_url") or row.get("website"):
                sources.append("Company Website")
            row.setdefault("sources_found", sources)
            row.setdefault("indeed_jobs", row.get("total_active_jobs") or 0)
        out.append(row)
    return out
