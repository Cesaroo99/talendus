"""Lead Intelligence Talendus — croisement multi-sources, sans scrap.

SOURCE → offre/signal → entreprise → volume × nature × croissance →
décideur → coordonnées publiques → score → prospect.

Aucune requête n’est faite vers Indeed, LinkedIn ou un ATS. Les signaux
viennent d’une collecte sur pages publiquement indexées. Pas de CAPTCHA,
pas d’auth, pas de courriel inventé.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from app.services.employer_claim import normalize_company_name
from app.services.indeed_prospecting import is_recruiter_title, is_staffing_agency

RESEARCHED_AT = "2026-09-08"
EMAIL_NOT_FOUND = "NOT_FOUND"

QUEBEC_BOARDS = (
    "Indeed",
    "LinkedIn Jobs",
    "Jobillico",
    "Jobboom",
    "Eluta",
    "Guichet-Emplois",
    "Talent.com",
    "Glassdoor",
    "Workopolis",
    "CareerBeacon",
    "Jooble",
    "Neuvoo",
    "Placement.work",
    "Emploi-Québec",
)

ATS_PLATFORMS = (
    "Workday",
    "Greenhouse",
    "Lever",
    "SmartRecruiters",
    "iCIMS",
    "Workable",
    "Ashby",
    "BambooHR",
    "Taleo",
    "SuccessFactors",
    "Jobvite",
    "Recruitee",
)

_TA_SPECIALIST = re.compile(
    r"talent acquisition specialist|spécialiste(?: en)? acquisition de talents|"
    r"spécialiste attraction|talent acquisition advisor|talent acquisition associate",
    re.IGNORECASE,
)
_TA_MANAGER = re.compile(
    r"talent acquisition manager|talent acquisition director|talent acquisition lead|"
    r"head of talent|head of recruitment|directeur(?:trice)? acquisition|"
    r"gestionnaire acquisition|vp human resources|chief human resources",
    re.IGNORECASE,
)
_RECRUITER = re.compile(
    r"\b(recruiter|recruteur|recruteuse|corporate recruiter|technical recruiter|"
    r"hr recruiter|recruitment specialist|recruitment partner|recruiting lead)\b",
    re.IGNORECASE,
)
_HARD = re.compile(
    r"électromécanicien|soudeur|machiniste|mécanicien industriel|technicien maintenance|"
    r"ingénieur|développeur|infirmier|médecin|opérateur spécialisé|chauffeur|"
    r"certifi|bilingue|quart de nuit|nuit|welder|machinist|industrial mechanic|"
    r"registered nurse|software engineer",
    re.IGNORECASE,
)
_GROWTH = re.compile(
    r"expansion|usine|nouvelle?s? installation|financement|acquisition|"
    r"croissance|succursale|nous (?:recrutons|embauchons|grandissons)|"
    r"we're hiring|we're growing|join our team|actively hiring",
    re.IGNORECASE,
)

VIEWS = (
    "all",
    "hot",
    "talent_acquisition",
    "high_volume",
    "difficult",
    "growing",
    "quebec",
    "montreal",
    "contactable",
)


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _host(url: str | None) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def recency_bonus(days: int | None) -> int:
    if days is None:
        return 0
    if days <= 7:
        return 15
    if days <= 30:
        return 10
    return 0


def priority_for(score: int) -> str:
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def recruitment_volume(row: dict[str, Any]) -> int:
    """Une offre republiee sur 4 boards compte une fois."""
    return max(
        _int(row.get("active_jobs_total") or row.get("total_active_jobs")),
        _int(row.get("linkedin_jobs")),
        _int(row.get("indeed_jobs")),
        _int(row.get("jobboom_jobs")),
        _int(row.get("jobillico_jobs")),
        _int(row.get("career_page_jobs")),
        _int(row.get("ats_jobs")),
    )


def score_intelligence(row: dict[str, Any]) -> dict[str, Any]:
    title = (row.get("indeed_job_title") or row.get("job_title") or "").strip()
    notes = " ".join(
        str(row.get(key) or "")
        for key in ("notes", "hiring_signal", "growth_notes", "talendus_opportunity")
    )
    blob = f"{title} {notes}"
    volume = recruitment_volume(row)
    staffing = is_staffing_agency(row.get("name") or row.get("company_name") or "", row.get("sector") or row.get("industry") or "", blob)

    ta_specialist = bool(
        _TA_SPECIALIST.search(blob) or row.get("hires_ta_specialist") or row.get("hires_ta_partner")
    )
    ta_manager = bool(_TA_MANAGER.search(blob) or row.get("hires_ta_manager"))
    recruiter_word = bool(_RECRUITER.search(title) or row.get("hires_recruiter"))
    recruiter = recruiter_word or (
        is_recruiter_title(title) and not ta_specialist and not ta_manager
    )
    multi_rh = bool(row.get("multi_rh") or _int(row.get("recruitment_jobs")) >= 2)
    internal = ta_specialist or recruiter or ta_manager or bool(row.get("internal_recruitment_signal"))

    points = 0
    if ta_specialist:
        points += 30
    if recruiter and not ta_specialist:
        points += 30
    elif recruiter and ta_specialist and row.get("hires_recruiter") and recruiter_word:
        points += 30
    if multi_rh:
        points += 25
    if ta_manager:
        points += 20

    if volume >= 50:
        points += 30
    elif volume >= 20:
        points += 25
    elif volume >= 10:
        points += 20
    elif volume >= 5:
        points += 10

    if row.get("multi_city"):
        points += 15
    if row.get("multi_province"):
        points += 10

    if row.get("expansion") or row.get("growth_signal") == "expansion":
        points += 20
    elif row.get("strong_growth") or row.get("growth_signal") is True:
        points += 15
    elif row.get("growth") or _GROWTH.search(blob):
        points += 10

    if row.get("many_specialized") or _int(row.get("difficult_to_fill_jobs")) >= 5:
        points += 15
    elif row.get("difficult") or row.get("operational_mass") or _HARD.search(blob) or _int(row.get("difficult_to_fill_jobs")) >= 1:
        points += 10

    points += recency_bonus(row.get("days_since_posting"))

    score = min(100, points)
    if staffing:
        score = min(score, 49)
    return {
        "lead_score": score,
        "priority": priority_for(score),
        "recruitment_volume": volume,
        "internal_recruitment_signal": internal,
        "staffing_agency": staffing,
        "hires_ta_specialist": ta_specialist,
        "hires_recruiter": recruiter,
    }


def explain_opportunity(row: dict[str, Any], scored: dict[str, Any]) -> str:
    name = row.get("name") or row.get("company_name") or "Cette entreprise"
    sector = (row.get("sector") or row.get("industry") or "entreprise").strip()
    volume = scored["recruitment_volume"]
    sources = row.get("sources_found") or []
    if isinstance(sources, str):
        sources = [part.strip() for part in sources.split("+") if part.strip()]
    src = ", ".join(sources[:5]) if sources else "pages publiques indexées"
    if scored.get("staffing_agency"):
        return (
            f"{name} est une agence de placement. Signal de recruteur visible, "
            "mais fit client Talendus faible (concurrent plutôt que donneur d’ordre)."
        )
    bits = [f"{sector[0].upper() + sector[1:] if sector else 'Entreprise'} — {volume} poste(s) uniques estimés ({src})."]
    if scored.get("internal_recruitment_signal"):
        bits.append(
            "Elle renforce en ce moment sa capacité interne de recrutement "
            f"({(row.get('indeed_job_title') or 'poste TA / recruteur')})."
        )
    if row.get("expansion") or row.get("growth_signal"):
        bits.append("Signal de croissance ou d’expansion croisé.")
    if row.get("difficult") or _int(row.get("difficult_to_fill_jobs")):
        bits.append("Plusieurs postes techniques ou difficiles à pourvoir.")
    if scored["lead_score"] >= 80:
        bits.append("Prospect prioritaire pour une proposition de partenariat Talendus.")
    elif scored["lead_score"] >= 65:
        bits.append("Bonne opportunité : un commercial peut ouvrir avec le volume et le signal TA.")
    else:
        bits.append("À surveiller : le signal est documenté mais pas encore prioritaire.")
    return " ".join(bits)


def _sources_list(row: dict[str, Any]) -> list[str]:
    found: list[str] = []
    raw = row.get("sources_found")
    if isinstance(raw, (list, tuple)):
        found.extend(str(item).strip() for item in raw if str(item).strip())
    elif isinstance(raw, str) and raw.strip():
        found.extend(part.strip() for part in raw.replace(",", "+").split("+") if part.strip())
    mapping = (
        ("indeed_job_url", "Indeed"),
        ("indeed_jobs", "Indeed"),
        ("linkedin_jobs", "LinkedIn Jobs"),
        ("linkedin_company", "LinkedIn"),
        ("jobillico_jobs", "Jobillico"),
        ("jobboom_jobs", "Jobboom"),
        ("eluta_jobs", "Eluta"),
        ("glassdoor_jobs", "Glassdoor"),
        ("job_bank_jobs", "Guichet-Emplois"),
        ("career_page", "Company Website"),
        ("career_page_jobs", "Company Website"),
        ("ats_platform", row.get("ats_platform") or "ATS"),
        ("careers_url", "Company Website"),
    )
    for key, label in mapping:
        value = row.get(key)
        if value in (None, "", 0, "0"):
            continue
        if label and label not in found:
            found.append(label)
    if not found:
        found.append("Public index")
    return list(dict.fromkeys(found))


def merge_intelligence(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    for raw in rows:
        row = dict(raw)
        name = normalize_company_name(row.get("name") or row.get("company_name") or "")
        host = _host(row.get("website"))
        found = by_key.get(name) if name else None
        if found is None and host:
            for existing in by_key.values():
                if _host(existing.get("website")) == host:
                    found = existing
                    break
        if found is None:
            if name:
                by_key[name] = row
            continue
        for key in (
            "total_active_jobs",
            "active_jobs_total",
            "linkedin_jobs",
            "indeed_jobs",
            "jobboom_jobs",
            "jobillico_jobs",
            "career_page_jobs",
            "recruitment_jobs",
            "difficult_to_fill_jobs",
        ):
            found[key] = max(_int(found.get(key)), _int(row.get(key)))
        for flag in (
            "hires_recruiter",
            "hires_ta_specialist",
            "hires_ta_manager",
            "hires_ta_partner",
            "multi_rh",
            "multi_city",
            "multi_province",
            "operational_mass",
            "growth",
            "strong_growth",
            "expansion",
            "difficult",
            "many_specialized",
            "internal_recruitment_signal",
        ):
            found[flag] = bool(found.get(flag) or row.get(flag))
        sources = _sources_list(found) + _sources_list(row)
        found["sources_found"] = list(dict.fromkeys(sources))
        if row.get("ats_platform") and not found.get("ats_platform"):
            found["ats_platform"] = row["ats_platform"]
        if row.get("career_page") and not found.get("career_page"):
            found["career_page"] = row["career_page"]
        if (row.get("email") or row.get("professional_email")) and not (
            found.get("email") or found.get("professional_email")
        ):
            found["email"] = row.get("email") or row.get("professional_email")
        if row.get("contact_name") and not found.get("contact_name"):
            found["contact_name"] = row["contact_name"]
            found["contact_title"] = row.get("contact_title")
        urls = list(found.get("source_urls") or [])
        for url in (row.get("indeed_job_url"), row.get("source_url"), row.get("career_page")):
            if url and url not in urls:
                urls.append(url)
        found["source_urls"] = urls
    return list(by_key.values())


def _career_url(row: dict[str, Any]) -> str:
    raw = row.get("career_page")
    if isinstance(raw, str) and raw.startswith("http"):
        return raw
    for key in ("careers_url", "source_url", "indeed_job_url", "website"):
        value = row.get(key)
        if isinstance(value, str) and value.startswith("http"):
            return value
    return str(row.get("website") or "")


def to_intelligence_record(row: dict[str, Any]) -> dict[str, Any]:
    scored = score_intelligence(row)
    opportunity = explain_opportunity(row, scored)
    email = (row.get("professional_email") or row.get("email") or "").strip()
    if not email:
        email = EMAIL_NOT_FOUND
    sources = _sources_list(row)
    volume = scored["recruitment_volume"]
    return {
        "company_name": row.get("name") or row.get("company_name"),
        "industry": row.get("sector") or row.get("industry"),
        "sub_industry": row.get("sub_industry") or "",
        "website": row.get("website"),
        "city": row.get("city"),
        "province": row.get("province") or "Québec",
        "country": row.get("country") or "Canada",
        "company_size": row.get("employees") or row.get("company_size"),
        "linkedin_company": row.get("linkedin_company") or row.get("linkedin_url"),
        "indeed_company": row.get("indeed_job_url") or row.get("indeed_company"),
        "jobboom_company": row.get("jobboom_company"),
        "jobillico_company": row.get("jobillico_company"),
        "glassdoor_company": row.get("glassdoor_company"),
        "career_page": _career_url(row),
        "ats_platform": row.get("ats_platform") or "",
        "sources_found": sources,
        "active_jobs_total": volume,
        "linkedin_jobs": _int(row.get("linkedin_jobs")),
        "indeed_jobs": _int(row.get("indeed_jobs") or row.get("total_active_jobs")),
        "jobboom_jobs": _int(row.get("jobboom_jobs")),
        "jobillico_jobs": _int(row.get("jobillico_jobs")),
        "career_page_jobs": _int(row.get("career_page_jobs")),
        "recruitment_jobs": _int(row.get("recruitment_jobs")),
        "talent_acquisition_jobs": 1 if scored.get("hires_ta_specialist") or row.get("hires_ta_partner") else 0,
        "high_volume_jobs": volume if volume >= 10 else 0,
        "difficult_to_fill_jobs": _int(row.get("difficult_to_fill_jobs")) or (1 if row.get("difficult") or row.get("operational_mass") else 0),
        "growth_signal": bool(row.get("growth") or row.get("strong_growth") or row.get("expansion") or row.get("growth_signal")),
        "internal_recruitment_signal": scored["internal_recruitment_signal"],
        "recruitment_volume": volume,
        "lead_score": scored["lead_score"],
        "priority": scored["priority"],
        "decision_maker_name": row.get("contact_name") or row.get("decision_maker_name") or "",
        "decision_maker_title": row.get("contact_title") or row.get("decision_maker_title") or "",
        "professional_email": email,
        "linkedin_decision_maker": row.get("linkedin_decision_maker") or "",
        "phone_public": row.get("phone") or row.get("phone_public") or "",
        "source_urls": row.get("source_urls")
        or [url for url in (row.get("indeed_job_url"), row.get("source_url"), row.get("career_page")) if url],
        "last_detected": row.get("last_detected") or RESEARCHED_AT,
        "notes": row.get("notes") or row.get("hiring_signal") or opportunity,
        "talendus_opportunity": opportunity,
        "discovery_pass": row.get("discovery_pass") or 1,
        "staffing_agency": scored["staffing_agency"],
        "legal_name": row.get("legal_name") or row.get("name"),
        "indeed_job_title": row.get("indeed_job_title"),
        "days_since_posting": row.get("days_since_posting"),
    }


def compile_intelligence(rows: list[dict[str, Any]] | tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    merged = merge_intelligence([dict(row) for row in rows if row.get("name") or row.get("company_name")])
    records = [to_intelligence_record(row) for row in merged if row.get("website") and (row.get("city") or row.get("name"))]
    records.sort(key=lambda item: (-int(item["lead_score"]), item["company_name"] or ""))
    return tuple(records)


def filter_view(records: tuple[dict[str, Any], ...] | list[dict[str, Any]], view: str = "all") -> list[dict[str, Any]]:
    rows = list(records)
    key = (view or "all").strip().lower()
    montreal = {
        "montréal",
        "montreal",
        "laval",
        "longueuil",
        "brossard",
        "terrebonne",
        "blainville",
        "boisbriand",
        "mirabel",
        "saint-eustache",
        "vaudreuil-dorion",
        "saint-laurent",
        "dorval",
        "pointe-claire",
        "anjou",
        "mont-royal",
        "boucherville",
        "greenfield park",
        "lasalle",
        "lachine",
        "repentigny",
        "saint-jérôme",
        "saint-jerome",
        "westmount",
        "kirkland",
        "beaconsfield",
        "dollard-des-ormeaux",
    }
    if key in {"hot", "a+"}:
        return [row for row in rows if row["priority"] == "A+"]
    if key in {"talent_acquisition", "ta"}:
        return [row for row in rows if row.get("internal_recruitment_signal")]
    if key in {"high_volume", "volume"}:
        return [row for row in rows if _int(row.get("recruitment_volume")) >= 10]
    if key in {"difficult", "hard"}:
        return [row for row in rows if _int(row.get("difficult_to_fill_jobs")) >= 1]
    if key in {"growing", "growth"}:
        return [row for row in rows if row.get("growth_signal")]
    if key in {"quebec", "qc"}:
        return [row for row in rows if (row.get("province") or "").lower().startswith("québec") or (row.get("province") or "").lower().startswith("quebec")]
    if key in {"montreal", "grand-montreal"}:
        return [row for row in rows if (row.get("city") or "").casefold() in montreal]
    if key in {"contactable", "email"}:
        return [
            row
            for row in rows
            if row.get("decision_maker_name")
            and row.get("professional_email") not in {"", None, EMAIL_NOT_FOUND}
        ]
    return rows


def intelligence_report(records: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    contactable = filter_view(rows, "contactable")
    return {
        "total_discovered": len(rows),
        "unique_after_dedupe": len(rows),
        "priority_a_plus": sum(1 for row in rows if row["priority"] == "A+"),
        "priority_a": sum(1 for row in rows if row["priority"] == "A"),
        "priority_b": sum(1 for row in rows if row["priority"] == "B"),
        "priority_c": sum(1 for row in rows if row["priority"] == "C"),
        "priority_d": sum(1 for row in rows if row["priority"] == "D"),
        "hiring_recruiters": sum(1 for row in rows if row.get("internal_recruitment_signal")),
        "hiring_ta_specialists": sum(1 for row in rows if _int(row.get("talent_acquisition_jobs")) >= 1),
        "jobs_10_plus": sum(1 for row in rows if _int(row.get("recruitment_volume")) >= 10),
        "jobs_20_plus": sum(1 for row in rows if _int(row.get("recruitment_volume")) >= 20),
        "jobs_50_plus": sum(1 for row in rows if _int(row.get("recruitment_volume")) >= 50),
        "growth_signals": sum(1 for row in rows if row.get("growth_signal")),
        "decision_makers": sum(1 for row in rows if row.get("decision_maker_name")),
        "professional_emails": sum(1 for row in rows if row.get("professional_email") not in {"", None, EMAIL_NOT_FOUND}),
        "contactable": len(contactable),
        "quebec": len(filter_view(rows, "quebec")),
        "top20": [
            {
                "company_name": row["company_name"],
                "lead_score": row["lead_score"],
                "priority": row["priority"],
                "city": row["city"],
                "talendus_opportunity": row["talendus_opportunity"],
                "sources_found": row["sources_found"],
            }
            for row in rows[:20]
        ],
        "boards_watched": list(QUEBEC_BOARDS),
        "ats_watched": list(ATS_PLATFORMS),
    }


def to_catalog_lead(record: dict[str, Any]) -> dict[str, Any]:
    email = record.get("professional_email")
    if email in {None, "", EMAIL_NOT_FOUND}:
        email = None
    sources = record.get("sources_found") or []
    src = " + ".join(sources) if isinstance(sources, list) else str(sources)
    return {
        "name": record["company_name"],
        "legal_name": record.get("legal_name") or record["company_name"],
        "sector": record.get("industry") or "Services",
        "city": record.get("city") or "Montréal",
        "address": f"{record.get('city') or 'Montréal'} (QC)",
        "phone": record.get("phone_public") or None,
        "email": email,
        "website": record["website"],
        "linkedin_url": record.get("linkedin_company"),
        "employees": record.get("company_size"),
        "careers_url": record.get("career_page") or record["website"],
        "lead_score": record["lead_score"],
        "lead_priority": record["priority"],
        "lead_categories": "LEAD_INTELLIGENCE, MULTI_SOURCE"
        + (", INTERNAL_TA_HIRE" if record.get("internal_recruitment_signal") else "")
        + (", HIGH_VOLUME" if _int(record.get("recruitment_volume")) >= 10 else "")
        + (", GROWTH" if record.get("growth_signal") else ""),
        "commercial_priority": {"A+": "A", "A": "A", "B": "B", "C": "C"}.get(record["priority"], "D"),
        "source": f"vague 10 — lead intelligence multi-sources ({src})",
        "source_url": (record.get("source_urls") or [record.get("website")])[0],
        "researched_at": RESEARCHED_AT,
        "hiring_signal": record.get("talendus_opportunity"),
        "hiring": (record.get("talendus_opportunity") or "") + f" Sources : {src}. Score {record['lead_score']}/100.",
        "contact_name": record.get("decision_maker_name") or None,
        "contact_title": record.get("decision_maker_title") or None,
        "talendus_opportunity": record.get("talendus_opportunity"),
        "total_active_jobs": record.get("recruitment_volume"),
        "province": record.get("province") or "Québec",
    }
