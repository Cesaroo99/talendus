"""Offres du site public : les pages HTML doivent toujours pouvoir recevoir une candidature."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models import Company, JobOffer, User
from app.models.enums import CompanyStatus, JobStatus, UserRole, utcnow

AGENCY_COMPANY_NAME = "Talendus"

# Aligné sur scripts/build_pages.py JOBS (slug, titre, ville, catégorie, type, salaire, horaire, exigences).
SITE_JOBS: tuple[dict, ...] = (
    {
        "slug": "cariste",
        "title": "Cariste",
        "location": "Laval",
        "sector": "Entrepôt",
        "contract_type": "Permanent",
        "salary_min": 22,
        "salary_max": 26,
        "salary_display": "22 à 26 $/h",
        "shift": "Quart de jour",
        "qualifications": "Permis chariot élévateur, 1 an d'expérience en entrepôt.",
        "skills": "conduite de chariot élévateur",
        "experience_level": "intermediaire",
    },
    {
        "slug": "operateur-production",
        "title": "Opérateur de production",
        "location": "Longueuil",
        "sector": "Production",
        "contract_type": "Permanent",
        "salary_min": 20,
        "salary_max": 24,
        "salary_display": "20 à 24 $/h",
        "shift": "Quart de jour",
        "qualifications": "Expérience de production, capacité à suivre des procédures, travail d'équipe.",
        "skills": "production",
        "experience_level": "debutant",
    },
    {
        "slug": "soudeur",
        "title": "Soudeur-monteur",
        "location": "Drummondville",
        "sector": "Métallurgie",
        "contract_type": "Permanent",
        "salary_min": 28,
        "salary_max": 34,
        "salary_display": "28 à 34 $/h",
        "shift": "Quart de jour",
        "qualifications": "Soudure MIG/TIG, lecture de plans, cartes de compétences un atout.",
        "skills": "soudure",
        "experience_level": "intermediaire",
    },
    {
        "slug": "machiniste-cnc",
        "title": "Machiniste CNC",
        "location": "Saint-Jérôme",
        "sector": "Manufacturier",
        "contract_type": "Permanent",
        "salary_min": 30,
        "salary_max": 38,
        "salary_display": "30 à 38 $/h",
        "shift": "Quart de jour",
        "qualifications": "Programmation ou set-up, lecture de dessins, 3 ans d'expérience.",
        "skills": "usinage CNC",
        "experience_level": "senior",
    },
    {
        "slug": "electromecanicien",
        "title": "Électromécanicien",
        "location": "Montréal",
        "sector": "Maintenance",
        "contract_type": "Permanent",
        "salary_min": 32,
        "salary_max": 40,
        "salary_display": "32 à 40 $/h",
        "shift": "Quart de jour",
        "qualifications": "Dépannage, hydraulique, pneumatique, électricité.",
        "skills": "électromécanique",
        "experience_level": "intermediaire",
    },
    {
        "slug": "mecanicien-industriel",
        "title": "Mécanicien industriel",
        "location": "Sherbrooke",
        "sector": "Maintenance",
        "contract_type": "Permanent",
        "salary_min": 30,
        "salary_max": 36,
        "salary_display": "30 à 36 $/h",
        "shift": "Quart de jour",
        "qualifications": "Entretien préventif, alignement, convoyeurs, fiabilité.",
        "skills": "mécanique",
        "experience_level": "intermediaire",
    },
    {
        "slug": "journalier-usine",
        "title": "Journalier d'usine",
        "location": "Boucherville",
        "sector": "Production",
        "contract_type": "Permanent",
        "salary_min": 18,
        "salary_max": 21,
        "salary_display": "18 à 21 $/h",
        "shift": "Quart de jour",
        "qualifications": "Bonne condition physique, ponctualité, formation interne offerte.",
        "skills": "production",
        "experience_level": "debutant",
    },
    {
        "slug": "superviseur-production",
        "title": "Superviseur de production",
        "location": "Trois-Rivières",
        "sector": "Supervision",
        "contract_type": "Permanent",
        "salary_min": 70000,
        "salary_max": 85000,
        "salary_display": "70 000 à 85 000 $",
        "shift": "Quart de jour",
        "qualifications": "Leadership d'équipe, KPI, 5 ans en production.",
        "skills": "supervision",
        "experience_level": "senior",
    },
    {
        "slug": "coordonnateur-logistique",
        "title": "Coordonnateur logistique",
        "location": "Anjou",
        "sector": "Logistique",
        "contract_type": "Permanent",
        "salary_min": 55000,
        "salary_max": 68000,
        "salary_display": "55 000 à 68 000 $",
        "shift": "Quart de jour",
        "qualifications": "WMS, planification, anglais un atout.",
        "skills": "logistique, WMS",
        "experience_level": "intermediaire",
    },
    {
        "slug": "directeur-usine",
        "title": "Directeur d'usine",
        "location": "Québec",
        "sector": "Cadres",
        "contract_type": "Permanent",
        "salary_min": 120000,
        "salary_max": 150000,
        "salary_display": "120 000 à 150 000 $",
        "shift": "Quart de jour",
        "qualifications": "P&L, Lean, gestion d'un site 100+ employés. Mandat confidentiel.",
        "skills": "direction",
        "experience_level": "senior",
    },
    {
        "slug": "developpeur",
        "title": "Développeur",
        "location": "Montréal",
        "sector": "Technologie",
        "contract_type": "Permanent",
        "salary_min": 75000,
        "salary_max": 95000,
        "salary_display": "75 000 à 95 000 $",
        "shift": "Quart de jour",
        "qualifications": "Python ou JavaScript, 2 ans d'expérience, travail en équipe.",
        "skills": "Python, JavaScript",
        "experience_level": "intermediaire",
    },
    {
        "slug": "comptable",
        "title": "Comptable",
        "location": "Québec",
        "sector": "Finance",
        "contract_type": "Permanent",
        "salary_min": 55000,
        "salary_max": 70000,
        "salary_display": "55 000 à 70 000 $",
        "shift": "Quart de jour",
        "qualifications": "Comptabilité, Excel, diplôme pertinent.",
        "skills": "Excel, comptabilité",
        "experience_level": "intermediaire",
    },
    {
        "slug": "ingenieur",
        "title": "Ingénieur",
        "location": "Sherbrooke",
        "sector": "Ingénierie",
        "contract_type": "Permanent",
        "salary_min": 80000,
        "salary_max": 100000,
        "salary_display": "80 000 à 100 000 $",
        "shift": "Quart de jour",
        "qualifications": "Ingénierie, gestion de projet, 3 ans d'expérience.",
        "skills": "gestion de projet",
        "experience_level": "senior",
    },
    {
        "slug": "chauffeur",
        "title": "Chauffeur",
        "location": "Anjou",
        "sector": "Transport",
        "contract_type": "Permanent",
        "salary_min": 22,
        "salary_max": 28,
        "salary_display": "22 à 28 $/h",
        "shift": "Quart de jour",
        "qualifications": "Permis de conduire valide, ponctualité, dossier de conduite propre.",
        "skills": "conduite",
        "experience_level": "intermediaire",
    },
    {
        "slug": "infirmier",
        "title": "Infirmier",
        "location": "Laval",
        "sector": "Santé",
        "contract_type": "Permanent",
        "salary_min": 32,
        "salary_max": 42,
        "salary_display": "32 à 42 $/h",
        "shift": "Quart de jour",
        "qualifications": "Permis OIIQ, expérience clinique, travail d'équipe.",
        "skills": "soins",
        "experience_level": "intermediaire",
    },
    {
        "slug": "vendeur",
        "title": "Vendeur",
        "location": "Longueuil",
        "sector": "Commerce",
        "contract_type": "Permanent",
        "salary_min": 18,
        "salary_max": 24,
        "salary_display": "18 à 24 $/h",
        "shift": "Quart de jour",
        "qualifications": "Vente au détail, service client, aisance relationnelle.",
        "skills": "vente",
        "experience_level": "debutant",
    },
    {
        "slug": "responsable-rh",
        "title": "Responsable RH",
        "location": "Montréal",
        "sector": "Administration",
        "contract_type": "Permanent",
        "salary_min": 70000,
        "salary_max": 90000,
        "salary_display": "70 000 à 90 000 $",
        "shift": "Quart de jour",
        "qualifications": "Recrutement, relations de travail, 5 ans en RH.",
        "skills": "RH",
        "experience_level": "senior",
    },
    {
        "slug": "specialiste-marketing",
        "title": "Spécialiste marketing",
        "location": "Montréal",
        "sector": "Marketing",
        "contract_type": "Permanent",
        "salary_min": 55000,
        "salary_max": 75000,
        "salary_display": "55 000 à 75 000 $",
        "shift": "Quart de jour",
        "qualifications": "Marketing digital, communication, gestion de campagnes.",
        "skills": "marketing",
        "experience_level": "intermediaire",
    },
)

SITE_JOBS_BY_SLUG = {item["slug"]: item for item in SITE_JOBS}

# Caractéristiques par défaut, surchargées par métier (quart, présence, permis, etc.).
SITE_JOB_TRAITS = {
    "operateur-production": {"shift": "Quarts rotatifs", "overtime": "Oui, payées"},
    "journalier-usine": {"shift": "Quart de soir", "education_required": "Secondaire", "overtime": "Oui, payées"},
    "electromecanicien": {"shift": "Quarts rotatifs", "education_required": "DEP", "certifications": "Carte de compétences"},
    "mecanicien-industriel": {"education_required": "DEP", "certifications": "Carte de compétences"},
    "cariste": {"certifications": "Permis chariot élévateur", "driver_license": "Permis chariot"},
    "soudeur": {"education_required": "DEP", "certifications": "Carte de compétences"},
    "machiniste-cnc": {"education_required": "DEP", "shift": "Quart de jour"},
    "chauffeur": {"driver_license": "Classe 1", "travel": "Fréquent"},
    "coordonnateur-logistique": {"languages": "Français et anglais", "work_mode": "Hybride"},
    "developpeur": {"work_mode": "Hybride", "languages": "Français et anglais"},
    "comptable": {"work_mode": "Hybride", "education_required": "DEC"},
    "ingenieur": {"education_required": "Baccalauréat", "work_mode": "Hybride"},
    "infirmier": {"shift": "Quarts rotatifs", "certifications": "Permis OIIQ"},
    "directeur-usine": {"work_mode": "Sur place", "travel": "Occasionnel", "education_required": "Baccalauréat"},
    "superviseur-production": {"shift": "Quart de jour", "overtime": "Oui, payées"},
    "vendeur": {"schedule": "Temps partiel", "shift": "Quart de jour"},
    "responsable-rh": {"work_mode": "Hybride", "languages": "Français et anglais"},
    "specialiste-marketing": {"work_mode": "Hybride"},
}


def _catalog_spec(spec: dict) -> dict:
    merged = dict(spec)
    merged.update(SITE_JOB_TRAITS.get(spec["slug"], {}))
    merged.setdefault("schedule", "Temps plein")
    merged.setdefault("work_mode", "Sur place")
    merged.setdefault("languages", "Français")
    merged.setdefault("unionized", "Non syndiqué")
    merged.setdefault("overtime", "Occasionnelles")
    merged.setdefault("travel", "Aucun")
    merged.setdefault("benefits", "Assurance collective")
    return merged


def is_site_job_slug(slug: str | None) -> bool:
    return bool(slug) and slug in SITE_JOBS_BY_SLUG


def _staff_user(db: Session) -> User | None:
    return db.scalar(
        select(User).where(
            User.is_active.is_(True),
            User.role.in_([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.RECRUITER]),
        )
    )


def ensure_agency_company(db: Session) -> Company:
    company = db.scalar(select(Company).where(Company.name == AGENCY_COMPANY_NAME))
    if company:
        return company
    staff = _staff_user(db)
    company = Company(
        name=AGENCY_COMPANY_NAME,
        legal_name=AGENCY_COMPANY_NAME,
        trade_name=AGENCY_COMPANY_NAME,
        description="Agence de placement. Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.",
        sector="Agence de placement",
        city="Montréal",
        province="Québec",
        country="Canada",
        website="https://talendus.ca",
        status=CompanyStatus.ACTIVE,
        owner_user_id=staff.id if staff else None,
        assigned_recruiter_id=staff.id if staff else None,
    )
    db.add(company)
    db.flush()
    return company


def _job_with_company(db: Session, slug: str) -> JobOffer | None:
    return db.scalar(
        select(JobOffer).options(joinedload(JobOffer.company)).where(JobOffer.slug == slug)
    )


def _create_catalog_job(db: Session, spec: dict) -> JobOffer:
    spec = _catalog_spec(spec)
    company = ensure_agency_company(db)
    staff = _staff_user(db)
    now = utcnow()
    job = JobOffer(
        company_id=company.id,
        recruiter_id=staff.id if staff else None,
        slug=spec["slug"],
        title=spec["title"],
        description=f"Poste de {spec['title']} à {spec['location']}. Recrutement Talendus.",
        qualifications=spec["qualifications"],
        location=spec["location"],
        sector=spec["sector"],
        contract_type=spec["contract_type"],
        salary_min=spec["salary_min"],
        salary_max=spec["salary_max"],
        salary_display=spec["salary_display"],
        skills=spec["skills"],
        experience_level=spec["experience_level"],
        shift=spec.get("shift") or "Quart de jour",
        schedule=spec.get("schedule") or "Temps plein",
        work_mode=spec.get("work_mode") or "Sur place",
        languages=spec.get("languages") or "Français",
        overtime=spec.get("overtime"),
        driver_license=spec.get("driver_license"),
        unionized=spec.get("unionized"),
        travel=spec.get("travel"),
        education_required=spec.get("education_required"),
        certifications=spec.get("certifications"),
        benefits=spec.get("benefits"),
        status=JobStatus.PUBLISHED,
        published_at=now,
    )
    try:
        with db.begin_nested():
            db.add(job)
            db.flush()
    except IntegrityError:
        existing = _job_with_company(db, spec["slug"])
        if existing:
            return existing
        raise
    return _job_with_company(db, spec["slug"]) or job


def ensure_catalog_job(db: Session, slug: str) -> JobOffer | None:
    """Crée l'offre du site si elle n'existe pas encore. Ne touche pas une offre déjà en base."""
    spec = SITE_JOBS_BY_SLUG.get(slug or "")
    if not spec:
        return None
    job = _job_with_company(db, slug)
    if job:
        return job
    return _create_catalog_job(db, spec)


def open_site_job_for_apply(db: Session, slug: str) -> JobOffer | None:
    """Trouve ou crée l'offre d'une page du site. Ne rouvre pas une offre pausée ou archivée."""
    spec = SITE_JOBS_BY_SLUG.get(slug or "")
    if not spec:
        return None
    job = ensure_catalog_job(db, slug)
    if not job:
        return None
    if job.company is None:
        job = _job_with_company(db, slug) or job
    return job


def ensure_site_catalog(db: Session) -> None:
    """Publie toutes les offres des pages HTML manquantes. Idempotent, sans faux employeurs."""
    for spec in SITE_JOBS:
        ensure_catalog_job(db, spec["slug"])
