"""Applique les trouvailles Deep Contact aux fiches catalogue existantes."""

from __future__ import annotations

from typing import Any

from app.data.contact_finder_finds import DEEP_CONTACT_FINDS, PORTAL_ONLY
from app.services.contact_finder import RESEARCHED_AT, apply_finder_to_lead, compile_contact_finder
from app.services.contact_finder_providers import collect_from_providers
from app.services.employer_claim import normalize_company_name


def _finds_index() -> dict[str, list[dict[str, Any]]]:
    finds: dict[str, list[dict[str, Any]]] = {}
    for name, rows in DEEP_CONTACT_FINDS.items():
        payload = collect_from_providers({"name": name}, [dict(item) for item in rows])
        finds[name] = payload
        finds[normalize_company_name(name)] = payload
    for name in PORTAL_ONLY:
        exhausted = [
            {
                "email": "",
                "status": "SEARCH_EXHAUSTED",
                "search_depth": 6,
                "discovered_at": RESEARCHED_AT,
                "source_type": "search",
            }
        ]
        finds.setdefault(name, exhausted)
        finds.setdefault(normalize_company_name(name), finds[name])
    return finds


def apply_deep_contacts(leads: tuple[dict, ...]) -> tuple[dict, ...]:
    """Ne crée aucune entreprise. N’écrase pas un meilleur courriel déjà présent."""
    records = compile_contact_finder(leads, _finds_index())
    by_name = {row["company_name"]: row for row in records}
    return tuple(apply_finder_to_lead(lead, by_name[lead["name"]]) for lead in leads)
