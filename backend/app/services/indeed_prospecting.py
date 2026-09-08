"""Veille B2B Indeed : score, déduplication et opportunité Talendus.

Aucune requête Indeed n’est faite ici. Les signaux viennent d’une collecte
manuelle sur des pages publiquement indexées (moteur de recherche, portails
carrières). Pas de scraping, pas de contournement de CAPTCHA.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from app.services.employer_claim import normalize_company_name

RESEARCHED_AT = "2026-09-08"
SOURCE_LABEL = "vague 9 — veille Indeed QC (listings publics indexés, sans scrap)"

_RECRUITER_TITLE = re.compile(
    r"\b("
    r"talent acquisition|acquisition de talents|attraction de talents|"
    r"recruiter|recruteur|recruteuse|corporate recruiter|technical recruiter|"
    r"hr recruiter|human resources recruiter|staffing specialist|"
    r"recruitment specialist|recruitment coordinator|recruitment manager|"
    r"spécialiste recrutement|coordonnateur recrutement|gestionnaire recrutement|"
    r"responsable recrutement|conseiller(?:e|ère)?(?: en)? recrutement|"
    r"conseiller(?:e|ère)?(?: en)? acquisition|"
    r"partenaire acquisition|talent acquisition partner|talent partner|"
    r"talent manager|talent sourcer|sourcing specialist|hiring specialist|"
    r"recruitment business partner|hr business partner"
    r")\b",
    re.IGNORECASE,
)
_TA_SPECIALIST = re.compile(
    r"talent acquisition specialist|spécialiste(?: en)? acquisition de talents|"
    r"spécialiste attraction",
    re.IGNORECASE,
)
_TA_PARTNER = re.compile(
    r"talent acquisition partner|partenaire(?: d.affaires)?(?: en)? acquisition|"
    r"talent acquisition business partner|partenaire d.affaires rh",
    re.IGNORECASE,
)
_RECRUITER_ONLY = re.compile(
    r"\b(recruiter|recruteur|recruteuse|corporate recruiter|technical recruiter|"
    r"hr recruiter|human resources recruiter)\b",
    re.IGNORECASE,
)
_STAFFING = re.compile(
    r"adecco|randstad|manpower|kelly services|robert half|\bhays\b|"
    r"go rh|racines humaines|agence de placement|gal aerostaff|"
    r"chasse(?:ur|use) de têtes|\brpo\b",
    re.IGNORECASE,
)
_OPS = re.compile(
    r"cariste|journalier|opérateur|manutention|entrepôt|usine|production|"
    r"préposé|commis d.entrepôt|chauffeur|manoeuvre|manœuvre|soudeur|"
    r"électromécanicien|préposé aux bénéficiaires",
    re.IGNORECASE,
)


def is_recruiter_title(title: str | None) -> bool:
    return bool(_RECRUITER_TITLE.search(title or ""))


def is_staffing_agency(name: str = "", sector: str = "", notes: str = "") -> bool:
    blob = f"{name} {sector} {notes}"
    return bool(_STAFFING.search(blob)) or (sector or "").strip().casefold() in {
        "agence de placement",
        "recrutement",
        "staffing",
    }


def recency_factor(days_since_posting: int | None) -> float:
    if days_since_posting is None:
        return 0.75
    if days_since_posting <= 7:
        return 1.0
    if days_since_posting <= 14:
        return 0.95
    if days_since_posting <= 30:
        return 0.85
    if days_since_posting <= 60:
        return 0.7
    return 0.35


def priority_for(score: int) -> str:
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    return "D"


def commercial_priority_for(score: int, *, staffing: bool) -> str:
    if staffing:
        return "D"
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    return "D"


def score_signals(row: dict[str, Any]) -> dict[str, Any]:
    title = (row.get("indeed_job_title") or row.get("job_title") or "").strip()
    notes = (row.get("notes") or row.get("hiring_signal") or "").strip()
    blob = f"{title} {notes}"
    total = int(row.get("total_active_jobs") or 0)
    rec_jobs = int(row.get("recruitment_jobs") or 0)
    if is_recruiter_title(title):
        rec_jobs = max(rec_jobs, 1)
    if _TA_SPECIALIST.search(blob) or row.get("hires_ta_specialist"):
        rec_jobs = max(rec_jobs, 1)
    staffing = is_staffing_agency(row.get("name") or "", row.get("sector") or "", blob)
    factor = recency_factor(row.get("days_since_posting"))

    ta = 0
    if _TA_SPECIALIST.search(blob) or row.get("hires_ta_specialist"):
        ta += 30
    if _RECRUITER_ONLY.search(blob) or row.get("hires_recruiter"):
        ta += 30
    if _TA_PARTNER.search(blob) or row.get("hires_ta_partner"):
        ta += 30
    if ta == 0 and is_recruiter_title(title):
        ta += 30
    ta = int(round(min(ta, 60) * factor))

    volume = 0
    if rec_jobs >= 2 or row.get("multi_rh"):
        volume += 25
    if total >= 50 or row.get("volume_50"):
        volume += 25
    elif total >= 20 or row.get("volume_20"):
        volume += 20
    elif total >= 10 or row.get("volume_10"):
        volume += 15
    if row.get("multi_city"):
        volume += 20
    if row.get("operational_mass") or _OPS.search(notes):
        volume += 20
    if row.get("growth"):
        volume += 20
    if row.get("large_hr_team"):
        volume += 15
    if total >= 3 and volume < 15:
        volume += 15
    if row.get("regular_hiring"):
        volume += 10
    if row.get("career_page") or row.get("careers_url"):
        volume += 10
    if total == 1 and ta == 0:
        volume += 5
    employees = row.get("employees")
    if employees and int(employees) >= 500 and total < 5 and ta == 0:
        volume += 5

    score = min(100, ta + volume)
    if staffing:
        score = min(score, 49)
    priority = priority_for(score)
    return {
        "lead_score": score,
        "lead_priority": priority,
        "commercial_priority": commercial_priority_for(score, staffing=staffing),
        "recruitment_jobs": rec_jobs,
        "staffing_agency": staffing,
        "recruiter_signal": ta > 0,
    }


def talendus_opportunity(row: dict[str, Any], scored: dict[str, Any]) -> str:
    name = row.get("name") or "Cette entreprise"
    sector = (row.get("sector") or "entreprise").strip()
    total = int(row.get("total_active_jobs") or 0)
    title = (row.get("indeed_job_title") or "").strip()
    if scored.get("staffing_agency"):
        return (
            f"{name} est une agence de placement / staffing. Signal Indeed de recruteur "
            "interne, mais fit client Talendus faible (concurrent plutôt que donneur d’ordre)."
        )
    if scored.get("recruiter_signal") and (row.get("operational_mass") or total >= 10):
        return (
            f"{sector[0].upper() + sector[1:] if sector else 'Entreprise'} avec "
            f"{total or 'plusieurs'} offres actives observées et recrutement simultané "
            f"{'d’un ' + title if title else 'd’un poste RH / acquisition de talents'}. "
            "Très fort potentiel pour un partenariat externe."
        )
    if scored.get("recruiter_signal"):
        return (
            f"{name} publie un poste de renforcement de l’équipe de recrutement "
            f"({title or 'recruteur / acquisition de talents'}). Volume interne à confirmer, "
            "mais le signal TA justifie un premier contact Talendus."
        )
    if row.get("operational_mass") or total >= 10:
        return (
            f"{name} recrute un volume opérationnel notable "
            f"({total or 'plusieurs'} offres : production, entrepôt, terrain). "
            "Besoin potentiel élevé en recrutement opérationnel."
        )
    return (
        f"{name} a un signal de recrutement public insuffisant pour une priorité haute, "
        "mais reste à surveiller si le volume Indeed augmente."
    )


def _host(url: str | None) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def dedupe_key(row: dict[str, Any]) -> str:
    name = normalize_company_name(row.get("name") or "")
    host = _host(row.get("website") or row.get("source_url"))
    city = (row.get("city") or "").strip().casefold()
    return "|".join(part for part in (name, host, city) if part)


def merge_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Une entreprise = une fiche. Fusionne offres et conserve le plus fort signal."""
    by_name: dict[str, dict[str, Any]] = {}
    for raw in rows:
        row = dict(raw)
        name_key = normalize_company_name(row.get("name") or "")
        host = _host(row.get("website"))
        found = None
        if name_key and name_key in by_name:
            found = by_name[name_key]
        elif host:
            for existing in by_name.values():
                if _host(existing.get("website")) == host:
                    found = existing
                    break
        if found is None:
            if name_key:
                by_name[name_key] = row
            continue
        found["total_active_jobs"] = max(
            int(found.get("total_active_jobs") or 0), int(row.get("total_active_jobs") or 0)
        )
        found["recruitment_jobs"] = int(found.get("recruitment_jobs") or 0) + int(
            row.get("recruitment_jobs") or 0
        )
        if not found.get("indeed_job_url") and row.get("indeed_job_url"):
            found["indeed_job_url"] = row["indeed_job_url"]
            found["indeed_job_title"] = row.get("indeed_job_title") or found.get("indeed_job_title")
        for flag in (
            "hires_recruiter",
            "hires_ta_specialist",
            "hires_ta_partner",
            "multi_rh",
            "multi_city",
            "operational_mass",
            "growth",
            "large_hr_team",
            "regular_hiring",
            "career_page",
            "volume_10",
            "volume_20",
            "volume_50",
        ):
            found[flag] = bool(found.get(flag) or row.get(flag))
        if row.get("email") and not found.get("email"):
            found["email"] = row["email"]
            found["email_source"] = row.get("email_source")
            found["email_source_url"] = row.get("email_source_url")
    return list(by_name.values())


def lead_categories(row: dict[str, Any], scored: dict[str, Any]) -> str:
    tags: list[str] = ["INDEED_DISCOVERY"]
    if scored.get("recruiter_signal"):
        tags.append("INTERNAL_TA_HIRE")
    if row.get("operational_mass"):
        tags.extend(["OPERATIONAL_COMPLEXITY", "RECURRING_NEED"])
    if int(row.get("total_active_jobs") or 0) >= 10:
        tags.append("HIGH_VOLUME")
    if row.get("multi_city"):
        tags.append("MULTI_SITE")
    if row.get("growth"):
        tags.append("GROWTH")
    sector = (row.get("sector") or "").casefold()
    if "manufactur" in sector or "aliment" in sector or "industriel" in sector:
        tags.append("FIELD_WORK")
    if "logistique" in sector or "entrepôt" in sector:
        tags.append("FIELD_WORK")
    if scored.get("staffing_agency"):
        tags.append("STAFFING_AGENCY")
    return ", ".join(dict.fromkeys(tags))


def to_catalog_lead(row: dict[str, Any]) -> dict[str, Any]:
    scored = score_signals(row)
    opportunity = talendus_opportunity(row, scored)
    email = (row.get("professional_email") or row.get("email") or None) or None
    if email:
        email = str(email).strip() or None
    job_url = row.get("indeed_job_url") or row.get("source_url") or row.get("website")
    hiring = (
        f"{opportunity} Offre déclencheur : {row.get('indeed_job_title') or 'volume Indeed'} "
        f"({row.get('job_status') or 'active'}, {row.get('job_posting_date') or 'date inconnue'}). "
        f"Offres actives observées ≈ {row.get('total_active_jobs') or 0}, "
        f"dont {scored['recruitment_jobs']} RH/recrutement. "
        f"Score Talendus {scored['lead_score']}/100, priorité {scored['lead_priority']}. "
        f"{'Courriel public relevé (non inventé) : ' + email + '. ' if email else 'Courriel : non publié (laissé vide). '}"
        f"Source : {job_url}."
    )
    lead = {
        "name": row["name"],
        "legal_name": row.get("legal_name") or row["name"],
        "sector": row["sector"],
        "city": row["city"],
        "address": row.get("address") or f"{row['city']} (QC)",
        "phone": row.get("phone"),
        "email": email,
        "website": row["website"],
        "linkedin_url": row.get("linkedin_company") or row.get("linkedin_url"),
        "employees": row.get("employees") or row.get("company_size"),
        "careers_url": row.get("careers_url") or row.get("indeed_job_url") or row["website"],
        "lead_score": scored["lead_score"],
        "lead_priority": scored["lead_priority"],
        "lead_categories": lead_categories(row, scored),
        "commercial_priority": scored["commercial_priority"],
        "source": SOURCE_LABEL,
        "source_url": job_url,
        "researched_at": RESEARCHED_AT,
        "hiring_signal": (row.get("recruitment_signal") or row.get("hiring_signal") or opportunity)[:240],
        "hiring": hiring[:4000],
        "indeed_job_title": row.get("indeed_job_title"),
        "indeed_job_url": row.get("indeed_job_url"),
        "job_posting_date": row.get("job_posting_date"),
        "job_status": row.get("job_status") or "active",
        "total_active_jobs": int(row.get("total_active_jobs") or 0),
        "recruitment_jobs": scored["recruitment_jobs"],
        "recruitment_signal": row.get("recruitment_signal") or opportunity,
        "talendus_opportunity": opportunity,
        "contact_name": row.get("contact_name"),
        "contact_title": row.get("contact_title"),
        "province": row.get("province") or "Québec",
        "discovery_pass": row.get("discovery_pass") or 1,
    }
    if email:
        lead.update(
            {
                "email_source": row.get("email_source") or "site officiel / page contact publique",
                "email_source_url": row.get("email_source_url") or row.get("website"),
                "email_type": "generic",
                "email_confidence": row.get("email_confidence") or "VERIFIED_MEDIUM",
                "email_verified": True,
                "email_verified_at": RESEARCHED_AT,
            }
        )
    return lead


def compile_indeed_leads(rows: list[dict[str, Any]] | tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    merged = merge_rows([dict(row) for row in rows])
    leads = [to_catalog_lead(row) for row in merged if row.get("name") and row.get("website") and row.get("city")]
    leads.sort(key=lambda row: (-int(row.get("lead_score") or 0), row["name"].casefold()))
    return tuple(leads)


def summarize_indeed_leads(leads: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> dict[str, Any]:
    rows = list(leads)
    sectors: dict[str, int] = {}
    cities: dict[str, int] = {}
    for row in rows:
        sectors[row.get("sector") or "—"] = sectors.get(row.get("sector") or "—", 0) + 1
        cities[row.get("city") or "—"] = cities.get(row.get("city") or "—", 0) + 1
    return {
        "total": len(rows),
        "priority_a": sum(1 for row in rows if (row.get("lead_priority") or "") in {"A", "A+"}),
        "priority_b": sum(1 for row in rows if row.get("lead_priority") == "B"),
        "priority_c": sum(1 for row in rows if row.get("lead_priority") == "C"),
        "priority_low": sum(1 for row in rows if (row.get("lead_priority") or "") in {"D", "faible"}),
        "hiring_recruiters": sum(
            1 for row in rows if "INTERNAL_TA_HIRE" in (row.get("lead_categories") or "")
        ),
        "jobs_10_plus": sum(1 for row in rows if int(row.get("total_active_jobs") or 0) >= 10),
        "jobs_20_plus": sum(1 for row in rows if int(row.get("total_active_jobs") or 0) >= 20),
        "emails": sum(1 for row in rows if row.get("email")),
        "decision_makers": sum(1 for row in rows if row.get("contact_name") and row.get("contact_title")),
        "top_sectors": sorted(sectors.items(), key=lambda item: (-item[1], item[0]))[:8],
        "top_cities": sorted(cities.items(), key=lambda item: (-item[1], item[0]))[:8],
    }
