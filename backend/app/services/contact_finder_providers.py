"""Fournisseurs Deep Contact — architecture extensible.

Chaque source est un module indépendant. Ajouter Hunter, Apollo ou un
annuaire B2B = une classe de plus, sans toucher au ranking ni au catalogue.

Aucune requête réseau ici. Les collectes live iront derrière le même
contrat (collect / cache / rate-limit) et devront rester sur des pages
publiques, sans CAPTCHA, login, paywall ni invention d’adresse.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Protocol

from app.services.contact_finder import CACHE_DAYS, RESEARCHED_AT, SOURCE_PROVIDERS


class ContactSourceProvider(Protocol):
    key: str
    level: int
    label: str

    def collect(self, company: dict[str, Any], curated: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Retourne des trouvailles déjà sourcées pour cette entreprise."""


class _TypedProvider:
    def __init__(self, key: str, level: int, label: str, source_types: tuple[str, ...]):
        self.key = key
        self.level = level
        self.label = label
        self.source_types = source_types

    def collect(self, company: dict[str, Any], curated: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = []
        for item in curated:
            source = (item.get("source_type") or "").lower()
            if source in self.source_types or (self.key == "search" and item.get("status") == "SEARCH_EXHAUSTED"):
                row = dict(item)
                row.setdefault("provider", self.key)
                row.setdefault("search_depth", self.level)
                rows.append(row)
        return rows


PROVIDERS: tuple[_TypedProvider, ...] = tuple(
    _TypedProvider(
        spec["key"],
        spec["level"],
        spec["label"],
        {
            "website": ("website", "careers"),
            "search": ("search",),
            "linkedin": ("linkedin",),
            "job_boards": ("job_boards",),
            "documents": ("documents",),
            "professional": ("professional", "government"),
        }[spec["key"]],
    )
    for spec in SOURCE_PROVIDERS
)


def collect_from_providers(company: dict[str, Any], curated: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for provider in PROVIDERS:
        for row in provider.collect(company, curated):
            key = (
                (row.get("email") or "").strip().lower(),
                (row.get("contact_name") or "").strip().casefold(),
            )
            if key in seen and key != ("", ""):
                continue
            seen.add(key)
            out.append(row)
    return out


def should_refresh(researched_at: str | None, today: str | None = None) -> bool:
    """Reprise / cache : ne pas relancer une recherche fiable de moins de CACHE_DAYS."""
    raw = (researched_at or "").strip()
    if not raw:
        return True
    try:
        when = date.fromisoformat(raw[:10])
    except ValueError:
        return True
    now = date.fromisoformat((today or RESEARCHED_AT)[:10]) if (today or RESEARCHED_AT) else date.today()
    return (now - when).days >= CACHE_DAYS


def deep_search_queries(company: dict[str, Any]) -> list[dict[str, str]]:
    """Plan de recherche FR/EN — exécuté plus tard par un fournisseur live, jamais inventé."""
    name = (company.get("name") or "").strip()
    legal = (company.get("legal_name") or name).strip()
    city = (company.get("city") or "").strip()
    website = (company.get("website") or "").strip()
    host = website.replace("https://", "").replace("http://", "").split("/")[0].removeprefix("www.")
    titles = (
        "human resources",
        "HR",
        "recruiter",
        "talent acquisition",
        "HR manager",
        "director human resources",
        "people and culture",
        "ressources humaines",
        "recrutement",
        "responsable RH",
        "directeur des ressources humaines",
        "acquisition de talents",
    )
    queries: list[dict[str, str]] = []

    def add(q: str, kind: str) -> None:
        if q and q not in {row["query"] for row in queries}:
            queries.append({"query": q, "kind": kind})

    for label in {name, legal} - {""}:
        add(f'"{label}" email', "search")
        add(f'"{label}" contact email', "search")
        add(f'"{label}" careers', "search")
        add(f'"{label}" recrutement', "search")
        add(f'"{label}" filetype:pdf', "documents")
        add(f'"{label}" contact filetype:pdf', "documents")
        add(f'"{label}" HR filetype:pdf', "documents")
        add(f'"{label}" annual report filetype:pdf', "documents")
        if city:
            add(f'"{label}" "{city}" RH', "search")
            add(f'"{label}" "{city}" email', "search")
        for title in titles:
            add(f'"{label}" "{title}"', "search")
    if host:
        add(f'"@{host}"', "domain")
        for local in ("contact", "info", "hr", "careers", "recruitment", "jobs", "recrutement", "dotation"):
            add(f'"{local}@{host}"', "domain")
    person = (company.get("contact_name") or company.get("primary_contact_name") or "").strip()
    if person:
        add(f'"{person}" email', "person")
        add(f'"{person}" "{name}"', "person")
        if host:
            add(f'"{person}" "@{host}"', "person")
        add(f'"{person}" LinkedIn', "person")
    return queries


def provider_catalog() -> list[dict[str, Any]]:
    return [
        {
            "key": p.key,
            "level": p.level,
            "label": p.label,
            "live": False,
            "notes": "Collecte publique indexée — pas de scrap ni d’invention.",
        }
        for p in PROVIDERS
    ]


def parse_iso_day(value: str | None) -> datetime | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
