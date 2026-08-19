"""Valeurs proposées pour les offres et les filtres (Québec)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import JobOffer
from app.models.enums import JobStatus

LOCATIONS = [
    "Montréal",
    "Laval",
    "Longueuil",
    "Boucherville",
    "Brossard",
    "Anjou",
    "Terrebonne",
    "Repentigny",
    "Saint-Jérôme",
    "Saint-Hyacinthe",
    "Drummondville",
    "Sherbrooke",
    "Granby",
    "Trois-Rivières",
    "Québec",
    "Lévis",
    "Gatineau",
    "Saguenay",
    "Salaberry-de-Valleyfield",
    "Télétravail",
]

SECTORS = [
    "Production",
    "Entrepôt",
    "Logistique",
    "Maintenance",
    "Manufacturier",
    "Métallurgie",
    "Transport",
    "Agroalimentaire",
    "Ingénierie",
    "Administration",
    "Supervision",
    "Cadres",
    "Santé",
    "Commerce",
    "Technologie",
    "Finance",
    "Marketing",
]

CONTRACT_TYPES = ["Permanent", "Temporaire", "Contractuel", "Saisonnier", "Stage"]

SHIFTS = [
    "Quart de jour",
    "Quart de soir",
    "Quart de nuit",
    "Quarts rotatifs",
    "Fin de semaine",
    "Quarts brisés",
]

SCHEDULES = ["Temps plein", "Temps partiel", "Sur appel", "4 jours / 3"]

WORK_MODES = ["Sur place", "Hybride", "Télétravail"]

LANGUAGES = ["Français", "Français et anglais", "Anglais", "Bilingue (FR/EN)"]

EXPERIENCE_LEVELS = [
    {"value": "debutant", "label": "Débutant", "label_en": "Entry-level"},
    {"value": "intermediaire", "label": "Intermédiaire", "label_en": "Mid-level"},
    {"value": "senior", "label": "Senior", "label_en": "Senior"},
]

PROVINCES = ["Québec", "Ontario", "Nouveau-Brunswick", "Nouvelle-Écosse", "Manitoba"]
COUNTRIES = ["Canada"]
AVAILABILITY = ["Immédiate", "2 semaines", "1 mois", "À convenir"]
MOBILITY = ["Locale", "Grande région", "Tout le Québec", "Relocalisation possible"]
EDUCATION = ["Secondaire", "DEP", "DEC", "Baccalauréat", "Maîtrise", "Aucune exigence"]
CERTIFICATIONS = [
    "Permis chariot élévateur",
    "ASP construction",
    "Carte de compétences",
    "Premiers soins",
    "WHMIS / SIMDUT",
    "Permis OIIQ",
    "Membre OIQ",
]
OVERTIME = ["Oui, payées", "Oui, banque d’heures", "Occasionnelles", "Non"]
DRIVER_LICENSES = ["Aucun", "Classe 5", "Classe 1", "Classe 3", "Permis chariot"]
UNION_STATUS = ["Non syndiqué", "Syndiqué"]
TRAVEL = ["Aucun", "Occasionnel", "Fréquent"]
COMPANY_SIZES = ["1 à 10", "11 à 50", "51 à 200", "201 à 500", "500+"]
BENEFITS = [
    "Assurance collective",
    "REER collectif",
    "Stationnement",
    "Prime de quart",
    "Formation payée",
    "Équipement fourni",
]


def _choices(values: list[str]) -> list[dict]:
    return [{"value": item, "label": item, "label_en": item} for item in values]


def _merge(catalog: list[str], extra: list[str | None]) -> list[str]:
    seen = {item.casefold(): item for item in catalog}
    out = list(catalog)
    for raw in extra:
        value = (raw or "").strip()
        if not value or value.casefold() in seen:
            continue
        seen[value.casefold()] = value
        out.append(value)
    return out


def published_values(db: Session, column) -> list[str]:
    rows = db.scalars(
        select(column).where(JobOffer.status == JobStatus.PUBLISHED, column.is_not(None)).distinct()
    ).all()
    return [str(item) for item in rows if item]


def catalog(db: Session | None = None) -> dict:
    locations = list(LOCATIONS)
    sectors = list(SECTORS)
    contracts = list(CONTRACT_TYPES)
    shifts = list(SHIFTS)
    schedules = list(SCHEDULES)
    modes = list(WORK_MODES)
    languages = list(LANGUAGES)
    if db is not None:
        locations = _merge(locations, published_values(db, JobOffer.location))
        sectors = _merge(sectors, published_values(db, JobOffer.sector))
        contracts = _merge(contracts, published_values(db, JobOffer.contract_type))
        shifts = _merge(shifts, published_values(db, JobOffer.shift))
        schedules = _merge(schedules, published_values(db, JobOffer.schedule))
        modes = _merge(modes, published_values(db, JobOffer.work_mode))
        languages = _merge(languages, published_values(db, JobOffer.languages))
    return {
        "locations": _choices(locations),
        "sectors": _choices(sectors),
        "contract_types": _choices(contracts),
        "shifts": _choices(shifts),
        "schedules": _choices(schedules),
        "work_modes": _choices(modes),
        "languages": _choices(languages),
        "experience_levels": EXPERIENCE_LEVELS,
        "provinces": _choices(PROVINCES),
        "countries": _choices(COUNTRIES),
        "availability": _choices(AVAILABILITY),
        "mobility": _choices(MOBILITY),
        "education": _choices(EDUCATION),
        "certifications": _choices(CERTIFICATIONS),
        "overtime": _choices(OVERTIME),
        "driver_licenses": _choices(DRIVER_LICENSES),
        "union_status": _choices(UNION_STATUS),
        "travel": _choices(TRAVEL),
        "company_sizes": _choices(COMPANY_SIZES),
        "benefits": _choices(BENEFITS),
    }
