"""Deep Business Contact Finder Talendus.

Trouve le meilleur point de contact professionnel pour vendre du
recrutement — jamais une adresse inventée ou devinée.

Aucune requête réseau. Les trouvailles viennent d’une collecte sur
pages publiques indexées. Pas de CAPTCHA, pas d’auth, pas de paywall.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from app.services.employer_claim import PUBLIC_MAIL_DOMAINS, normalize_company_name

RESEARCHED_AT = "2026-09-08"
CACHE_DAYS = 30
MIN_PRIMARY_CONFIDENCE = 70

STATUS_FOUND_VERIFIED = "FOUND_VERIFIED"
STATUS_FOUND_HIGH = "FOUND_HIGH_CONFIDENCE"
STATUS_FOUND_MEDIUM = "FOUND_MEDIUM_CONFIDENCE"
STATUS_GENERIC_ONLY = "GENERIC_ONLY"
STATUS_CONTACT_NO_EMAIL = "CONTACT_FOUND_EMAIL_NOT_FOUND"
STATUS_NO_EMAIL = "NO_EMAIL_FOUND"
STATUS_EXHAUSTED = "SEARCH_EXHAUSTED"
STATUS_PATTERN = "EMAIL_PATTERN_GUESSED"

SEARCH_LEVELS = (
    "LEVEL 1 — Website",
    "LEVEL 2 — Search engines",
    "LEVEL 3 — LinkedIn",
    "LEVEL 4 — Job platforms",
    "LEVEL 5 — PDFs / documents",
    "LEVEL 6 — Professional sources",
)

SOURCE_PROVIDERS = (
    {"key": "website", "level": 1, "label": "Site officiel"},
    {"key": "search", "level": 2, "label": "Moteurs de recherche"},
    {"key": "linkedin", "level": 3, "label": "LinkedIn public"},
    {"key": "job_boards", "level": 4, "label": "Sites d’emploi"},
    {"key": "documents", "level": 5, "label": "PDF / rapports"},
    {"key": "professional", "level": 6, "label": "Annuaires / communiqués"},
)

_GENERIC_LOCAL = re.compile(
    r"^(info|contact|hello|bonjour|admin|accueil|reception|communication|"
    r"communications|medias?|presse|webmaster|noreply|no-reply|ventes|sales|"
    r"service|customerservice|support|webmaster)$",
    re.IGNORECASE,
)
_HR_LOCAL = re.compile(
    r"^(rh|hr|recrutement|recruitment|carrieres|careers|emplois|jobs|dotation|"
    r"talent|talents|humanresources|human-resources|people|staffing|"
    r"acquisition|embauch|support\.rh|rhumaines)$",
    re.IGNORECASE,
)
_TA_TITLE = re.compile(
    r"talent acquisition|acquisition de talents|attraction de talents|"
    r"recruteur|recruteuse|recruiter|recruitment|dotation",
    re.IGNORECASE,
)
_HR_TITLE = re.compile(
    r"ressources humaines|human resources|\bhr\b|\brh\b|people & culture|"
    r"people and culture|talents et culture|service talents|"
    r"people operations|partenaire rh|hrbp",
    re.IGNORECASE,
)
_OPS_TITLE = re.compile(
    r"operations|opérations|usine|plant manager|directeur d.?usine|"
    r"directeur g.?n.?ral|general manager|pdg|president|président|"
    r"fondateur|founder|owner|propri.?taire|associ",
    re.IGNORECASE,
)
_MARKETING_TITLE = re.compile(
    r"marketing|communication|ventes|sales|media|presse",
    re.IGNORECASE,
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


def _local(email: str) -> str:
    return (email or "").split("@", 1)[0].strip().lower()


def _domain(email: str) -> str:
    if "@" not in (email or ""):
        return ""
    return email.split("@", 1)[1].strip().lower()


def is_valid_syntax(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", (email or "").strip()))


def is_personal_webmail(email: str, official_host: str = "") -> bool:
    domain = _domain(email)
    if not domain:
        return True
    if official_host and (domain == official_host or official_host.endswith("." + domain) or domain.endswith("." + official_host)):
        return False
    return domain in PUBLIC_MAIL_DOMAINS


def is_generic_mailbox(email: str) -> bool:
    return bool(_GENERIC_LOCAL.match(_local(email)))


def is_hr_mailbox(email: str) -> bool:
    return bool(_HR_LOCAL.match(_local(email)))


def domain_matches_company(email: str, website: str | None) -> bool:
    mail_host = _domain(email)
    site_host = _host(website)
    if not mail_host or not site_host:
        return False
    if mail_host == site_host:
        return True
    site_root = ".".join(site_host.split(".")[-2:]).replace("-", "")
    mail_root = ".".join(mail_host.split(".")[-2:]).replace("-", "")
    return bool(site_root and site_root == mail_root)


def contact_relevance(title: str | None, email: str | None, employees: int | None) -> int:
    blob = f"{title or ''} {email or ''}"
    size = _int(employees)
    if _MARKETING_TITLE.search(title or "") and not _HR_TITLE.search(title or "") and not _TA_TITLE.search(title or ""):
        return 20
    if _TA_TITLE.search(blob):
        if re.search(r"director|directeur|manager|gestionnaire|lead|leader|vp|chef", blob, re.I):
            return 100
        return 90
    if re.search(r"vp human|vice-pr.?sident.? rh|chief people|chro", blob, re.I):
        return 96
    if re.search(r"hr director|directeur(?:trice)?(?: des)? ressources humaines", blob, re.I):
        return 95
    if re.search(r"hr manager|gestionnaire rh|responsable rh", blob, re.I):
        return 93
    if _HR_TITLE.search(blob):
        return 88
    if re.search(r"procurement|achats|vendor management|approvisionnement", blob, re.I) and size and size >= 500:
        return 78
    if is_hr_mailbox(email or ""):
        return 65
    if _OPS_TITLE.search(blob):
        if size and size <= 20:
            return 78
        if size and size <= 100:
            return 72
        if size and size >= 500:
            return 55
        return 70
    if is_generic_mailbox(email or ""):
        return 30
    if email:
        return 45
    return 0


def freshness_score(discovered_at: str | None, source_type: str | None = None) -> int:
    raw = discovered_at or ""
    year = _int(raw[:4]) if raw else 0
    if year >= 2026:
        base = 100
    elif year == 2025:
        base = 80
    elif year >= 2023:
        base = 55
    elif year >= 2018:
        base = 35
    else:
        base = 70
    if source_type in {"website", "careers", "government"}:
        base = min(100, base + 5)
    return base


def confidence_score(row: dict[str, Any], website: str | None = None) -> int:
    if row.get("guessed") or row.get("status") == STATUS_PATTERN:
        return min(49, _int(row.get("confidence_score")))
    given = _int(row.get("confidence_score"))
    if given:
        score = given
    else:
        source = (row.get("source_type") or "").lower()
        score = {"website": 96, "careers": 94, "government": 95, "professional": 82, "documents": 78, "job_boards": 74, "search": 72, "linkedin": 70}.get(source, 60)
    email = (row.get("email") or row.get("primary_email") or "").strip()
    if email and not is_valid_syntax(email):
        return 0
    catalog_trusted = (row.get("source_type") or "").lower() in {"catalog", "catalogue"}
    if email and is_personal_webmail(email, _host(website)):
        score = min(score, 69 if catalog_trusted else 45)
    if email and website and not domain_matches_company(email, website) and not is_personal_webmail(email):
        score = min(score, 80 if catalog_trusted else 68)
    if freshness_score(row.get("discovered_at"), row.get("source_type")) < 40:
        score = min(score, 69)
    return max(0, min(100, score))


def status_for(confidence: int, email: str | None, title: str | None, generic_only: bool) -> str:
    if not email:
        return STATUS_CONTACT_NO_EMAIL if title else STATUS_NO_EMAIL
    if confidence < 50:
        return STATUS_NO_EMAIL
    if generic_only or (is_generic_mailbox(email) and not is_hr_mailbox(email) and not _TA_TITLE.search(title or "")):
        if confidence >= 70:
            return STATUS_GENERIC_ONLY
    if confidence >= 95:
        return STATUS_FOUND_VERIFIED
    if confidence >= 85:
        return STATUS_FOUND_HIGH
    if confidence >= 70:
        return STATUS_FOUND_MEDIUM
    return STATUS_NO_EMAIL


def _normalize_person(name: str | None) -> str:
    raw = re.sub(r"[^a-z0-9]+", " ", (name or "").casefold())
    raw = re.sub(r"\b[a-z]\b", " ", raw)
    return " ".join(raw.split())


def _name_parts(name: str | None) -> list[str]:
    return [part for part in re.sub(r"[^a-z0-9]+", " ", (name or "").casefold()).split() if part]


def same_person(left: str | None, right: str | None) -> bool:
    a, b = _name_parts(left), _name_parts(right)
    if not a or not b:
        return False
    if _normalize_person(left) and _normalize_person(left) == _normalize_person(right):
        return True
    if a[-1] != b[-1]:
        return False
    first_a, first_b = a[0], b[0]
    if first_a == first_b:
        return True
    if len(first_a) == 1 and first_b.startswith(first_a):
        return True
    if len(first_b) == 1 and first_a.startswith(first_b):
        return True
    return False


def merge_contacts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for raw in rows:
        email = (raw.get("email") or "").strip().lower()
        person = raw.get("contact_name") or raw.get("name")
        found = None
        for item in merged:
            same_email = email and email == (item.get("email") or "").strip().lower()
            person_match = same_person(person, item.get("contact_name"))
            if same_email or person_match:
                found = item
                break
        if found is None:
            merged.append(dict(raw))
            continue
        if _int(raw.get("confidence_score")) > _int(found.get("confidence_score")):
            found.update({k: v for k, v in raw.items() if v not in (None, "", [])})
        elif raw.get("contact_title") and not found.get("contact_title"):
            found["contact_title"] = raw["contact_title"]
        seconds = list(found.get("secondary_emails") or [])
        for extra in [raw.get("email"), *(raw.get("secondary_emails") or [])]:
            if extra and extra not in seconds and extra != found.get("email"):
                seconds.append(extra)
        found["secondary_emails"] = seconds
    return merged


def pick_primary(existing: dict[str, Any] | None, candidates: list[dict[str, Any]], website: str | None, employees: int | None) -> dict[str, Any] | None:
    pool = merge_contacts([*(candidates or []), *([existing] if existing and existing.get("email") else [])])
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in pool:
        email = (item.get("email") or "").strip()
        if email and (item.get("guessed") or not is_valid_syntax(email) or is_personal_webmail(email, _host(website))):
            continue
        conf = confidence_score(item, website)
        if email and conf < MIN_PRIMARY_CONFIDENCE:
            continue
        rel = contact_relevance(item.get("contact_title"), email, employees)
        scored.append((rel * 100 + conf, item))
    if not scored:
        return existing if existing and existing.get("email") else None
    scored.sort(key=lambda pair: pair[0], reverse=True)
    winner = scored[0][1]
    if existing and existing.get("email") and existing.get("keep"):
        seconds = list(existing.get("secondary_emails") or [])
        for item in pool:
            for extra in [item.get("email"), *(item.get("secondary_emails") or [])]:
                if extra and extra.lower() != (existing.get("email") or "").lower() and extra not in seconds:
                    seconds.append(extra)
        existing["secondary_emails"] = seconds
        return existing
    if existing and existing.get("email"):
        old_rel = contact_relevance(existing.get("contact_title"), existing.get("email"), employees)
        old_conf = confidence_score(existing, website)
        new_rel = contact_relevance(winner.get("contact_title"), winner.get("email"), employees)
        new_conf = confidence_score(winner, website)
        if old_conf >= 90 and old_rel >= new_rel:
            return existing
        if old_rel > new_rel and old_conf >= MIN_PRIMARY_CONFIDENCE:
            return existing
        if old_rel == new_rel and old_conf >= new_conf:
            return existing
    return winner


def why_this_contact(record: dict[str, Any]) -> str:
    title = record.get("primary_contact_title") or ""
    email = record.get("primary_email") or ""
    status = record.get("email_search_status")
    if status == STATUS_CONTACT_NO_EMAIL:
        return (
            f"Personne pertinente identifiée ({title}) mais aucun courriel professionnel "
            "public n’a été trouvé. Pas d’adresse inventée."
        )
    if status in {STATUS_NO_EMAIL, STATUS_EXHAUSTED}:
        return "Recherche documentée : aucun courriel professionnel public assez fiable pour la prospection."
    if _TA_TITLE.search(title):
        return "Responsable directement lié au recrutement / à l’acquisition de talents."
    if _HR_TITLE.search(title) or is_hr_mailbox(email):
        return "Point de contact RH publié — bon interlocuteur pour une proposition Talendus."
    if is_generic_mailbox(email):
        return "Seul courriel professionnel public trouvé (générique). Utile pour un premier envoi, moins précis qu’un RH."
    if _OPS_TITLE.search(title):
        return "Dirigeant ou opérations publié — pertinent pour une PME où le recrutement passe par la direction."
    return "Meilleur courriel professionnel public disponible, sourcé et non inventé."


def commercial_bucket(record: dict[str, Any]) -> str:
    score = _int(record.get("talendus_score") or record.get("lead_score"))
    status = record.get("email_search_status")
    rel = _int(record.get("contact_relevance_score"))
    conf = _int(record.get("primary_email_confidence"))
    if record.get("primary_email") and status in {STATUS_FOUND_VERIFIED, STATUS_FOUND_HIGH} and score >= 65 and rel >= 65:
        return "now"
    if record.get("primary_email") and conf >= 70 and score >= 50:
        return "contactable"
    if score >= 65 and not record.get("primary_email"):
        return "needs_research"
    if not record.get("primary_email"):
        return "no_email"
    return "contactable"


def to_finder_record(company: dict[str, Any], chosen: dict[str, Any] | None, extras: list[dict[str, Any]]) -> dict[str, Any]:
    website = company.get("website")
    employees = company.get("employees") or company.get("company_size")
    email = (chosen or {}).get("email") or ""
    title = (chosen or {}).get("contact_title") or company.get("contact_title") or ""
    name = (chosen or {}).get("contact_name") or company.get("contact_name") or ""
    conf = confidence_score(chosen, website) if chosen else 0
    rel = contact_relevance(title, email, employees) if (email or title) else 0
    generic_only = bool(email and is_generic_mailbox(email) and not is_hr_mailbox(email) and not _TA_TITLE.search(title))
    status = (chosen or {}).get("status") or status_for(conf, email or None, title or None, generic_only)
    if not email and not title:
        status = (chosen or {}).get("status") or STATUS_NO_EMAIL
    seconds = []
    for item in extras:
        extra = (item.get("email") or "").strip()
        if extra and extra.lower() != email.lower() and extra not in seconds:
            seconds.append(extra)
    for extra in (chosen or {}).get("secondary_emails") or []:
        if extra and extra.lower() != email.lower() and extra not in seconds:
            seconds.append(extra)
    depth = (chosen or {}).get("search_depth") or company.get("email_search_depth") or (6 if status == STATUS_EXHAUSTED else 1)
    record = {
        "company_name": company.get("name"),
        "website": website,
        "city": company.get("city"),
        "industry": company.get("sector") or company.get("industry"),
        "company_size": employees,
        "talendus_score": company.get("lead_score") or 0,
        "talendus_priority": company.get("lead_priority") or company.get("priority") or "",
        "primary_contact_name": name or "",
        "primary_contact_title": title or "",
        "primary_email": email or "",
        "primary_email_confidence": conf if email else 0,
        "primary_email_source": (chosen or {}).get("email_source") or (chosen or {}).get("source_type") or "",
        "primary_email_source_url": (chosen or {}).get("source_url") or (chosen or {}).get("email_source_url") or "",
        "secondary_emails": seconds,
        "contact_linkedin": (chosen or {}).get("linkedin") or "",
        "contact_relevance_score": rel,
        "contact_freshness_score": freshness_score((chosen or {}).get("discovered_at"), (chosen or {}).get("source_type")),
        "email_verified": bool(email and conf >= 85),
        "email_last_verified_at": (chosen or {}).get("discovered_at") or RESEARCHED_AT,
        "email_search_depth": depth,
        "email_search_status": status,
        "why_this_contact": "",
        "search_depth_label": SEARCH_LEVELS[min(5, max(0, _int(depth) - 1))],
        "bucket": "",
        "discovered_at": (chosen or {}).get("discovered_at") or RESEARCHED_AT,
    }
    record["why_this_contact"] = why_this_contact(record)
    record["bucket"] = commercial_bucket(record)
    return record


def existing_as_find(lead: dict[str, Any]) -> dict[str, Any] | None:
    email = (lead.get("email") or "").strip()
    title = lead.get("contact_title")
    name = lead.get("contact_name")
    if not email and not name:
        return None
    conf_label = (lead.get("email_confidence") or "").upper()
    conf = 96 if "HIGH" in conf_label else 86 if "MEDIUM" in conf_label else 74 if "UNVERIFIED" in conf_label else (90 if email else 0)
    return {
        "email": email,
        "contact_name": name,
        "contact_title": title,
        "source_url": lead.get("email_source_url") or lead.get("website"),
        "source_type": "website" if lead.get("email_source") else "catalog",
        "email_source": lead.get("email_source") or "catalogue",
        "discovered_at": lead.get("researched_at") or lead.get("email_verified_at") or RESEARCHED_AT,
        "confidence_score": conf,
        "keep": bool(email and conf >= 90 and not is_generic_mailbox(email)),
        "search_depth": 1,
        "secondary_emails": list(lead.get("secondary_emails") or []),
    }


def compile_contact_finder(
    companies: tuple[dict[str, Any], ...] | list[dict[str, Any]],
    finds: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any], ...]:
    records = []
    for company in companies:
        name = (company.get("name") or "").strip()
        key = normalize_company_name(name)
        incoming = list(finds.get(name) or finds.get(key) or [])
        current = existing_as_find(company)
        chosen = pick_primary(current, incoming, company.get("website"), company.get("employees"))
        extras = incoming + ([current] if current else [])
        records.append(to_finder_record(company, chosen, extras))
    records.sort(key=lambda row: (-_int(row["talendus_score"]), -_int(row["contact_relevance_score"]), row["company_name"] or ""))
    return tuple(records)


def filter_view(records: tuple[dict[str, Any], ...] | list[dict[str, Any]], view: str = "all") -> list[dict[str, Any]]:
    key = (view or "all").strip().lower()
    rows = list(records)
    if key in {"now", "hot", "contactable_now"}:
        return [row for row in rows if row["bucket"] == "now"]
    if key in {"contactable", "orange"}:
        return [row for row in rows if row["bucket"] == "contactable"]
    if key in {"needs_research", "research", "yellow"}:
        return [row for row in rows if row["bucket"] == "needs_research"]
    if key in {"no_email", "red"}:
        return [row for row in rows if row["bucket"] == "no_email"]
    return rows


def finder_report(records: tuple[dict[str, Any], ...] | list[dict[str, Any]], analyzed: int | None = None) -> dict[str, Any]:
    rows = list(records)
    with_email = [row for row in rows if row.get("primary_email")]
    rh = [row for row in with_email if _int(row.get("contact_relevance_score")) >= 65]
    generic = [row for row in with_email if row.get("email_search_status") == STATUS_GENERIC_ONLY]
    named = [row for row in with_email if row.get("primary_contact_name")]
    high = [row for row in with_email if _int(row.get("primary_email_confidence")) >= 85]
    mid = [row for row in with_email if 70 <= _int(row.get("primary_email_confidence")) < 85]
    none = [row for row in rows if not row.get("primary_email")]
    total = analyzed if analyzed is not None else len(rows)
    return {
        "companies_analyzed": total,
        "emails_found": len(with_email),
        "hr_recruitment_emails": len(rh),
        "generic_emails": len(generic),
        "named_contacts": len(named),
        "high_confidence": len(high),
        "medium_confidence": len(mid),
        "no_email": len(none),
        "recovery_rate": round(100 * len(with_email) / total, 1) if total else 0,
        "contactable_now": len(filter_view(rows, "now")),
        "contactable": len(filter_view(rows, "contactable")),
        "needs_research": len(filter_view(rows, "needs_research")),
        "failed_top20": [
            {
                "company_name": row["company_name"],
                "talendus_score": row["talendus_score"],
                "city": row["city"],
                "status": row["email_search_status"],
                "why": row["why_this_contact"],
            }
            for row in sorted(none, key=lambda item: -_int(item["talendus_score"]))[:20]
        ],
        "providers": list(SOURCE_PROVIDERS),
        "cache_days": CACHE_DAYS,
        "researched_at": RESEARCHED_AT,
    }


def apply_finder_to_lead(lead: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    """Enrichit une fiche catalogue sans changer son identité ni inventer."""
    out = dict(lead)
    out["primary_contact_name"] = record.get("primary_contact_name")
    out["primary_contact_title"] = record.get("primary_contact_title")
    out["primary_email"] = record.get("primary_email") or None
    out["primary_email_confidence"] = record.get("primary_email_confidence")
    out["primary_email_source"] = record.get("primary_email_source")
    out["primary_email_source_url"] = record.get("primary_email_source_url")
    out["secondary_emails"] = record.get("secondary_emails") or []
    out["contact_linkedin"] = record.get("contact_linkedin")
    out["contact_relevance_score"] = record.get("contact_relevance_score")
    out["email_verified"] = record.get("email_verified")
    out["email_last_verified_at"] = record.get("email_last_verified_at")
    out["email_search_depth"] = record.get("email_search_depth")
    out["email_search_status"] = record.get("email_search_status")
    new_email = (record.get("primary_email") or "").strip()
    if not new_email:
        if record.get("primary_contact_name") and not out.get("contact_name"):
            out["contact_name"] = record["primary_contact_name"]
            out["contact_title"] = record.get("primary_contact_title")
        return out
    current = (out.get("email") or "").strip()
    if current and current.lower() == new_email.lower():
        if record.get("primary_contact_name") and not out.get("contact_name"):
            out["contact_name"] = record["primary_contact_name"]
            out["contact_title"] = record.get("primary_contact_title")
        return out
    upgrade = False
    if not current:
        upgrade = True
    elif is_generic_mailbox(current) and _int(record.get("contact_relevance_score")) >= 65 and _int(record.get("primary_email_confidence")) >= 70:
        upgrade = True
    if not upgrade:
        return out
    out["email"] = new_email
    out["email_source"] = record.get("primary_email_source") or "recherche publique"
    out["email_source_url"] = record.get("primary_email_source_url")
    conf = _int(record.get("primary_email_confidence"))
    out["email_confidence"] = "VERIFIED_HIGH" if conf >= 95 else "VERIFIED_MEDIUM" if conf >= 85 else "PUBLIC_UNVERIFIED"
    out["email_verified"] = bool(record.get("email_verified"))
    out["email_verified_at"] = record.get("email_last_verified_at")
    if record.get("primary_contact_name"):
        out["contact_name"] = record["primary_contact_name"]
        out["contact_title"] = record.get("primary_contact_title")
    extra = (
        f" Courriel public Deep Contact {RESEARCHED_AT}: {new_email} "
        f"(source {out.get('email_source')}, {out.get('email_source_url')})."
    )
    hiring = (out.get("hiring") or "").rstrip()
    if new_email not in hiring:
        out["hiring"] = (hiring + extra)[:4000]
    return out
