"""Prospection B2B logistique Grand Montréal — Talendus.

Courriels uniquement s’ils ont été vus sur une page publique officielle.
Aucune adresse déduite du prénom.

Inclut les messageries / 3PL / CD déjà au catalogue (Purolator, UPS, etc.)
plus les nouvelles entreprises du même genre (Nationex, ICS, Fastfrate).
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from hubs_messagerie import HUBS

_LEGAL_SUFFIXES = re.compile(
    r"\b("
    r"inc|incorporated|ltd|ltee|ltée|limited|limitee|limitée|"
    r"corp|corporation|cie|co|company|compagnie|"
    r"s\.?e\.?c\.?|s\.?e\.?n\.?c\.?|sencrl|senc|sec|"
    r"s\.?a\.?|sarl|llc"
    r")\b",
    re.IGNORECASE,
)


def normalize_company_name(name: str | None) -> str:
    text = unicodedata.normalize("NFKD", name or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = _LEGAL_SUFFIXES.sub(" ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())

VERIFIED_ON = "2026-09-14"
OUT_DIR = Path(__file__).resolve().parent

COLUMNS = [
    "Rang",
    "Score Talendus",
    "Priorité",
    "Nom entreprise",
    "Site web",
    "Ville",
    "Secteur",
    "Nombre d'employés estimé",
    "Type d'activité",
    "Signal de recrutement",
    "Nombre d'offres actuelles",
    "Postes recherchés",
    "Quart de travail",
    "Nom du décideur #1",
    "Fonction #1",
    "LinkedIn #1",
    "Email #1",
    "Vérification email #1",
    "Nom du décideur #2",
    "Fonction #2",
    "LinkedIn #2",
    "Email #2",
    "Vérification email #2",
    "Email général vérifié",
    "Email RH vérifié",
    "Email recrutement vérifié",
    "Téléphone",
    "Adresse",
    "Source entreprise",
    "Source offre emploi",
    "Source personne",
    "Source email",
    "Date de vérification",
    "Niveau de confiance",
    "Pourquoi Talendus devrait les contacter",
    "Angle d'approche recommandé",
    "Priorité de contact",
    "Notes",
    "Taille bande",
    "Emails vérifiés (n)",
    "Score besoin recrutement /5",
    "Présence Talendus",
]


def _host(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def score_row(row: dict) -> int:
    s = 0
    offers = int(row.get("offers") or 0)
    if offers >= 3:
        s += 25
    elif offers == 2:
        s += 15
    elif offers == 1:
        s += 10
    if row.get("ops_roles"):
        s += 15
    if row.get("night_shift"):
        s += 10
    if row.get("growth"):
        s += 10
    size = int(row.get("employees") or 0)
    if 20 <= size <= 300:
        s += 10
    elif 5 <= size <= 500:
        s += 6
    if row.get("repeat_roles"):
        s += 10
    if row.get("hard_to_fill"):
        s += 5
    if row.get("person1"):
        s += 5
    emails = [e for e in row.get("emails") or [] if e.get("addr")]
    if any(e.get("kind") == "direct" for e in emails):
        s += 5
    if len(emails) >= 2:
        s += 5
    if not row.get("hiring_signal"):
        s -= 20
    if size > 500 and row.get("centralized"):
        s -= 15
    if not row.get("person1") and not emails:
        s -= 10
    if int(row.get("need_score") or 0) <= 1:
        s -= 10
    return max(0, min(100, s))


def priority_of(score: int) -> str:
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def size_band(n: int) -> str:
    if n <= 25:
        return "A"
    if n <= 75:
        return "B"
    if n <= 150:
        return "C"
    if n <= 300:
        return "D"
    if n <= 500:
        return "E"
    return "F"


def email_by_kind(emails: list[dict], kind: str) -> str:
    for item in emails:
        if item.get("kind") == kind:
            return item["addr"]
    return ""


# Chaque fiche : preuves publiques uniquement. emails[].proof obligatoire.
COMPANIES: list[dict] = [
    {
        "name": "Distribution Stox (Unimax)",
        "website": "https://unimax.ca",
        "city": "Boucherville",
        "sector": "Distribution / pneus",
        "employees": 280,
        "activity": "Centres de distribution pneus (Stox / RSSW / Point S), multi-quarts, expansion Ottawa/Sudbury",
        "hiring_signal": "17 offres Boucherville + 4 Laval (cariste/manutentionnaire jour-soir-nuit, livreurs)",
        "offers": 21,
        "roles": "Cariste/manutentionnaire jour, soir, nuit ; manutentionnaire ; chauffeur-livreur classe 5 ; aide-livreur",
        "shift": "Jour / soir / nuit (ex. 22h30–7h00) + prime rush oct-nov",
        "ops_roles": True,
        "night_shift": True,
        "growth": True,
        "repeat_roles": True,
        "hard_to_fill": True,
        "need_score": 5,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "1-866-906-8848",
        "address": "235, rue J.-A.-Bombardier, Boucherville (QC) J4B 8P1",
        "src_co": "https://unimax.ca/fr — siège Boucherville, divisions Stox / RSSW / Point S",
        "src_job": "https://careers.smartrecruiters.com/distributionstox2 (17 postes Boucherville le 2026-09-14)",
        "src_person": "",
        "src_email": "Aucun courriel public assez fiable. Portail SmartRecruiters uniquement.",
        "confidence": "Élevé sur le volume d’offres ; faible sur le contact nominatif",
        "why": "Volume exceptionnel de postes opérationnels multi-quarts sur la Rive-Sud et Laval, plus rush saisonnier pneus. PME/mid-market plus accessible qu’un géant national.",
        "angle": "Proposer un bassin caristes/manutentionnaires soir-nuit et un filet rush octobre-novembre, sans remplacer leur ATS.",
        "notes": "Seulement 0 email vérifiable trouvé. Ne pas inventer rh@ ou jobs@.",
    },
    {
        "name": "Transport Gariépy",
        "website": "https://transportgariepy.com",
        "city": "Montréal",
        "sector": "Transport / entrepôt",
        "employees": 80,
        "activity": "Cueillettes et livraisons locales Grand Montréal, mécaniciens châssis, cariste quai Est",
        "hiring_signal": "Plusieurs offres simultanées : classe 1 jour/nuit/week-end, classe 3, cariste, 2 mécaniciens",
        "offers": 8,
        "roles": "Camionneur classe 1 (jour, nuit, week-end) ; classe 3 ; cariste ; mécanicien châssis/remorque",
        "shift": "Jour, soir (16h–), week-end",
        "ops_roles": True,
        "night_shift": True,
        "growth": False,
        "repeat_roles": True,
        "hard_to_fill": True,
        "need_score": 5,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "cv@transportgariepy.com", "kind": "recrutement", "who": "", "proof": "Page Carrières officielle — « Send your resume to cv@transportgariepy.com »"},
            {"addr": "info@transportgariepy.com", "kind": "general", "who": "", "proof": "Page Carrières officielle — Customer service"},
            {"addr": "rsvp@transportgariepy.com", "kind": "ops", "who": "", "proof": "Page Carrières officielle — Dispatch"},
            {"addr": "rate_request@transportgariepy.com", "kind": "other", "who": "", "proof": "Page Carrières officielle — Spot quotes"},
        ],
        "phone": "514-494-3400",
        "address": "11525, avenue Armand-Chaput, Montréal (QC) H1C 1S8",
        "src_co": "https://transportgariepy.com",
        "src_job": "https://transportgariepy.com/en/careers",
        "src_person": "",
        "src_email": "Site officiel > Carrières (cv@, info@, rsvp@, rate_request@)",
        "confidence": "Élevé — 4 boîtes publiées sur la page carrières",
        "why": "PME de l’Est qui embauche en continu des chauffeurs (nuit/week-end) et un cariste. Décideur opérations joignable via dispatch publié.",
        "angle": "Offrir des chauffeurs classe 1 soir/week-end et un cariste quai, CV déjà acceptés à cv@.",
        "notes": "4 emails vérifiables trouvés. Owner-led probable ; nom du dirigeant non confirmé publiquement.",
    },
    {
        "name": "Groupe Lafrance",
        "website": "https://groupe-lafrance.com",
        "city": "Montréal",
        "sector": "Transport / entrepôt LTL",
        "employees": 120,
        "activity": "LTL, intermodal, terminal Montréal, entreposage — entreprise familiale 2e génération",
        "hiring_signal": "8 postes ouverts : gérant opérations, répartiteurs LTL/intermodal, gérant d’entrepôt, manutentionnaire, inventaires",
        "offers": 8,
        "roles": "Gérant d’opérations transport ; répartiteur LTL ; répartiteur intermodal ; gérant d’entrepôt ; manutentionnaire ; responsable inventaires",
        "shift": "Jour",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 5,
        "person1": "Famille Bineau",
        "title1": "Direction / 2e génération (nommée sur la page carrières)",
        "li1": "",
        "emails": [
            {"addr": "jobs@lafrance.qc.ca", "kind": "rh", "who": "", "proof": "Page Postes disponibles — « À l’attention des ressources humaines — jobs@lafrance.qc.ca »"},
            {"addr": "info@groupe-lafrance.com", "kind": "general", "who": "", "proof": "Pied de page / contact officiel groupe-lafrance.com"},
        ],
        "phone": "514-254-6688",
        "address": "7055, boulevard Notre-Dame Est, Montréal (QC) H1N 3R8",
        "src_co": "https://groupe-lafrance.com",
        "src_job": "https://groupe-lafrance.com/carrieres/postes-disponibles/",
        "src_person": "Page carrières — entreprise gérée par la 2e génération de la famille Bineau",
        "src_email": "Site officiel > Carrières (jobs@) + contact (info@)",
        "confidence": "Élevé",
        "why": "Ils cherchent à la fois un gérant d’entrepôt et un manutentionnaire : signal classique d’un terminal sous tension. PME familiale, RH publié.",
        "angle": "Mandat mixte : superviseur d’entrepôt + bassin manutentionnaires/répartiteurs LTL. Écrire à jobs@.",
        "notes": "Seulement 2 emails vérifiables trouvés. Nom individuel du RH non publié.",
    },
    {
        "name": "Cozey",
        "website": "https://www.cozey.ca",
        "city": "Mont-Royal",
        "sector": "E-commerce / fulfillment meubles",
        "employees": 160,
        "activity": "Nouveau centre de distribution 8191, ch. Montview ; croissance d’effectif ~+36 %",
        "hiring_signal": "Fulfilment Center Clerk sur ATS Rippling — nouveau CD Mont-Royal",
        "offers": 1,
        "roles": "Commis centre de fulfillment (réception conteneurs, picking, retours)",
        "shift": "Jour 7h–15h30 lundi–vendredi",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 4,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "rh@cozey.ca", "kind": "rh", "who": "", "proof": "Page LinkedIn officielle de l’entreprise : « Send us your resume at rh@cozey.ca »"},
            {"addr": "support@cozey.ca", "kind": "general", "who": "", "proof": "Coordonnées publiques de l’entreprise (page LinkedIn officielle)"},
        ],
        "phone": "1-833-521-1089",
        "address": "8191, chemin Montview, Mont-Royal (QC) H4P 2P2",
        "src_co": "https://www.cozey.ca + page LinkedIn officielle Cozey",
        "src_job": "https://ats.rippling.com/cozey/jobs/6c63d6c0-30ef-4c86-80ba-9f64ee1b8c02",
        "src_person": "",
        "src_email": "LinkedIn entreprise officiel (rh@) — pas une déduction de nom",
        "confidence": "Élevé sur rh@ ; moyen sur le volume (1 offre visible)",
        "why": "Nouveau CD + croissance d’équipe : besoin typique de commis/préparateurs avant d’avoir une grosse TA interne.",
        "angle": "Proposer un bassin fulfillment (réception, picking, retours) pour le nouveau site Montview.",
        "notes": "Seulement 2 emails vérifiables trouvés.",
    },
    {
        "name": "Techo-Bloc",
        "website": "https://www.techo-bloc.com",
        "city": "Saint-Hubert",
        "sector": "Manufacturier / cour / expédition",
        "employees": 800,
        "activity": "Usine et cour Saint-Hubert, quart de nuit 16h–4h, multi-sites NA",
        "hiring_signal": "Yard forklift driver NIGHT Saint-Hubert — offre active sept. 2026",
        "offers": 1,
        "roles": "Cariste de cour — quart de nuit",
        "shift": "Nuit lun–jeu 16h–4h + prime 2 $/h",
        "ops_roles": True,
        "night_shift": True,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "centralized": True,
        "need_score": 4,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@techo-bloc.com", "kind": "general", "who": "", "proof": "Pied de page officiel techo-bloc.com / flyer PDF officiel"},
        ],
        "phone": "1-877-832-4625",
        "address": "5255, rue Albert-Millichamp, Saint-Hubert (QC) J3Y 8Z8",
        "src_co": "https://www.techo-bloc.com/fr/about-us/contact-us",
        "src_job": "Offre cariste de cour nuit Saint-Hubert (publication sept. 2026)",
        "src_person": "",
        "src_email": "Site officiel > pied de page / PDF studio",
        "confidence": "Moyen — 1 offre nuit forte, entreprise plus grande (recrutement plus centralisé)",
        "why": "Quart de nuit 12 h en cour : profil difficile à pourvoir. Utile si on a un bassin caristes soir/nuit Rive-Sud.",
        "angle": "Mandat ciblé caristes de cour nuit Saint-Hubert, pas un contrat national.",
        "notes": "Seulement 1 email vérifiable trouvé. Taille >500 : pénalité centralisation appliquée.",
    },
    {
        "name": "K-Logistics",
        "website": "https://www.klogistics.ca",
        "city": "Montréal",
        "sector": "3PL / e-commerce",
        "employees": 25,
        "activity": "Entreposage, pick & pack, alimentaire sec, FBA, cross-dock — 15+ ans",
        "hiring_signal": "Commis Pick Pack Ship affiché sur le site officiel (section Carrières)",
        "offers": 1,
        "roles": "Commis pick pack ship",
        "shift": "Non précisé (ops e-comm, rush -4h mentionné)",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@klogistics.ca", "kind": "general", "who": "", "proof": "Site officiel klogistics.ca — « E-mail : info@klogistics.ca »"},
        ],
        "phone": "514-443-6124",
        "address": "8584, boulevard Pie-IX, Montréal (QC) H1Z 4G2",
        "src_co": "https://www.klogistics.ca",
        "src_job": "https://www.klogistics.ca — bloc Carrières Commis Pick Pack Ship",
        "src_person": "",
        "src_email": "Site officiel > pied de page / contact",
        "confidence": "Élevé sur l’email ; moyen sur le volume",
        "why": "3PL PME Saint-Michel qui affiche déjà un besoin pick-pack. Décideur probablement owner-led.",
        "angle": "Proposer 2–4 commis pick-pack flexibles (rush e-comm / FBA) plutôt qu’un ATS.",
        "notes": "Seulement 1 email vérifiable trouvé.",
    },
    {
        "name": "Precise Warehousing",
        "website": "https://www.precisewarehousing.com",
        "city": "Baie-d'Urfé",
        "sector": "3PL / entrepôt alimentaire BRC",
        "employees": 30,
        "activity": "2 entrepôts sec + réfrigéré, fulfillment Shopify/Amazon, certifié BRC depuis 2011",
        "hiring_signal": "Ops 3PL alimentaire + e-comm (pas d’offre dénombrée aujourd’hui — besoin structurel de pickers)",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@precisewarehousing.com", "kind": "general", "who": "", "proof": "Site officiel FR — en-tête « info@precisewarehousing.com »"},
        ],
        "phone": "514-447-3671",
        "address": "555, avenue Lee, Baie-d'Urfé (QC) H9X 3S3",
        "src_co": "https://www.precisewarehousing.com/fr/",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel > en-tête contact",
        "confidence": "Moyen — email officiel, signal d’offre faible aujourd’hui",
        "why": "3PL alimentaire Ouest-de-l’Île : quand ils embauchent, ce sont des profils froids/BRC difficiles.",
        "angle": "Se présenter comme bassin caristes/préparateurs formés alimentaire (froid, lots, dates).",
        "notes": "Seulement 1 email vérifiable. Score besoin 2/5 faute d’offre datée.",
    },
    {
        "name": "Frigologix",
        "website": "https://frigologix.ca",
        "city": "Dorval",
        "sector": "Entrepôt frigorifique / 3PL",
        "employees": 20,
        "activity": "Entrepôt surgelé 35 000 pi² ouvert 2023, BRCGS, sous douane, 5000 palettes — aéroport",
        "hiring_signal": "Nouvelle installation 2023 + ops froid 24/7 typiques ; emails service publiés",
        "offers": 0,
        "roles": "",
        "shift": "Ops froid (souvent multi-quarts — non daté sur le site)",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "csr.team@frigologix.ca", "kind": "general", "who": "", "proof": "Page Contact officielle frigologix.ca/contact/"},
            {"addr": "info@frigologix.ca", "kind": "general", "who": "", "proof": "Pages services / accueil officielles frigologix.ca"},
        ],
        "phone": "514-683-1212",
        "address": "107, rue Avro, Dorval (QC) H9P 0A8",
        "src_co": "https://frigologix.ca et https://frigologix.ca/contact/",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel > Contact (csr.team@) + pages services (info@)",
        "confidence": "Élevé sur les emails ; moyen sur les offres (aucune datée aujourd’hui)",
        "why": "Nouvel entrepôt surgelé Dorval : main-d’œuvre froid difficile. PME, pas un Lineage.",
        "angle": "Bassin caristes/manutentionnaires chambre froide près de l’aéroport.",
        "notes": "2 emails vérifiables. Pas d’offre d’emploi datée au 2026-09-14.",
    },
    {
        "name": "Bulletproof Logistics",
        "website": "https://www.bulletprooflogistics.com",
        "city": "Pointe-Claire",
        "sector": "3PL / fulfillment e-comm",
        "employees": 40,
        "activity": "Fulfillment DTC, WMS, transport, réseau multi-entrepôts — Sources",
        "hiring_signal": "3PL e-comm en croissance (pas d’offre dénombrée aujourd’hui)",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@bulletprooflogistics.com", "kind": "general", "who": "", "proof": "Site officiel homepage — bloc contact 2001 boul. des Sources"},
        ],
        "phone": "1-855-275-1888",
        "address": "2001, boulevard des Sources, bureau 102, Pointe-Claire (QC) H9R 5Z4",
        "src_co": "https://www.bulletprooflogistics.com",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel > contact homepage",
        "confidence": "Moyen",
        "why": "3PL Ouest-de-l’Île, taille contactable. Utile dès qu’une vague pick-pack apparaît.",
        "angle": "Se positionner pour les pics e-comm (préparateurs, emballeurs, caristes).",
        "notes": "Seulement 1 email vérifiable. Score besoin 2/5.",
    },
    {
        "name": "3PL Montréal",
        "website": "https://3plmtl.com",
        "city": "Montréal-Nord",
        "sector": "3PL / entreposage",
        "employees": 20,
        "activity": "Entrepôt 6789 boul. Léger, production/assemblage, expédition, surveillance",
        "hiring_signal": "Ops 3PL actives (heures 7h30–15h30 publiées) — offre non listée aujourd’hui",
        "offers": 0,
        "roles": "",
        "shift": "Jour 7h30–15h30",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@3plmtl.com", "kind": "general", "who": "", "proof": "Site officiel 3plmtl.com — Reach Us / E-mail"},
        ],
        "phone": "514-509-8150",
        "address": "6789, boulevard Léger, Montréal-Nord (QC) H1G 6E9",
        "src_co": "https://3plmtl.com",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel > Reach Us",
        "confidence": "Moyen",
        "why": "Petit 3PL Nord-de-l’Île, owner-led probable, pas de TA interne.",
        "angle": "Offrir commis d’entrepôt / caristes à la journée selon volume clients.",
        "notes": "Seulement 1 email vérifiable.",
    },
    {
        "name": "Tandem 3PL",
        "website": "https://tandem.ca",
        "city": "Longueuil",
        "sector": "3PL e-commerce",
        "employees": 8,
        "activity": "Picking/packing 7 j/7, entrepôt Longueuil, marques e-comm QC",
        "hiring_signal": "Ops 7 jours (publié) ; micro-équipe 7 pers. — tout départ pèse",
        "offers": 0,
        "roles": "",
        "shift": "7 jours / préparation 24 h",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@tandem.ca", "kind": "general", "who": "", "proof": "Page officielle tandem.ca/en/3-months-free/ — Contact us directly"},
        ],
        "phone": "438-355-3975",
        "address": "Longueuil (QC) — entrepôt 3PL e-comm",
        "src_co": "https://tandem.ca et page LinkedIn officielle Tandem 3PL (7 employés)",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel tandem.ca (info@tandem.ca)",
        "confidence": "Moyen-élevé sur le contact ; petit volume",
        "why": "Micro-3PL 7 j/7 : un arrêt maladie crée un trou. Plus facile à convertir qu’un national.",
        "angle": "Renfort pick-pack week-end / 7 j, pas un département RH.",
        "notes": "Seulement 1 email vérifiable. LinkedIn indique 7 employés.",
    },
    {
        "name": "GETPAQ",
        "website": "https://www.getpaq.ca",
        "city": "Montréal",
        "sector": "3PL / courtage transport",
        "employees": 35,
        "activity": "Entreposage + transport depuis Pointe-aux-Trembles, 3PL multi-villes",
        "hiring_signal": "3PL actif PAT (offre non dénombrée aujourd’hui)",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@getpaq.ca", "kind": "general", "who": "", "proof": "Site officiel getpaq.ca — bloc Email Info@GETPAQ.ca"},
        ],
        "phone": "514-323-4680",
        "address": "12225, boulevard Industriel, Pointe-aux-Trembles (QC) H1B 5M7",
        "src_co": "https://www.getpaq.ca/en/",
        "src_job": "https://www.getpaq.ca/emplois.php — CV à Info@GETPAQ.ca",
        "src_person": "",
        "src_email": "Page Emplois officielle + pied de page",
        "confidence": "Élevé sur info@ (aussi publié comme destinataire des CV)",
        "why": "3PL Est de Montréal, taille PME, entrepôt + courtage. Page emplois invite les CV à Info@GETPAQ.ca.",
        "angle": "Commis d’entrepôt / coordonnateurs transport à info@getpaq.ca.",
        "notes": "1 email vérifiable, aussi utilisé pour les candidatures.",
    },
    {
        "name": "LPF Logistique",
        "website": "https://lpf-logistique.com",
        "city": "Montréal",
        "sector": "Dernier kilomètre / 3PL local",
        "employees": 12,
        "activity": "Livraison jour même, tournées pharmacies/cliniques, e-comm, flotte électrique",
        "hiring_signal": "Service urgence + jour même (besoin livreurs structurel)",
        "offers": 0,
        "roles": "",
        "shift": "Lun–ven 8h–18h + urgence",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [
            {"addr": "info@lpf-logistique.com", "kind": "general", "who": "", "proof": "Site officiel lpf-logistique.com — section Contact"},
        ],
        "phone": "514-865-2873",
        "address": "Montréal (QC)",
        "src_co": "https://lpf-logistique.com",
        "src_job": "",
        "src_person": "",
        "src_email": "Site officiel > Contact",
        "confidence": "Moyen",
        "why": "Last-mile local : livreurs classe 5 difficiles à garder. Très petite structure.",
        "angle": "Livreurs / aides last-mile Grand Montréal, pas un mandat usine.",
        "notes": "Seulement 1 email vérifiable. Adresse civique non publiée.",
    },
    {
        "name": "GoBolt",
        "website": "https://www.gobolt.com",
        "city": "Montréal",
        "sector": "3PL / last mile / fulfillment",
        "employees": 200,
        "activity": "Entrepôt 429, rue Deslauriers (H4N) ; last-mile + fulfillment NA",
        "hiring_signal": "Warehouse Associate Montréal affiché sur ATS Rippling",
        "offers": 1,
        "roles": "Manutentionnaire d’entrepôt (pick/pack, quais, FIFO)",
        "shift": "Lundi–vendredi",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "Art Lee",
        "title1": "Founder & CEO (présenté sur gobolt.com)",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "429, rue Deslauriers, Montréal (QC) H4N 1W8",
        "src_co": "https://www.gobolt.com + offre Rippling",
        "src_job": "https://ats.rippling.com/en-CA/gobolt/jobs/e1aa7a9b-5ba7-45de-98d9-8b04e82da9ea",
        "src_person": "Page entreprise officielle — Art Lee, Founder & CEO",
        "src_email": "Aucun courriel RH/général publié sur le site (formulaire seulement). hello@ vu sur Trustpilot : NON retenu.",
        "confidence": "Moyen — offre réelle, email absent",
        "why": "3PL last-mile + entrepôt Ahuntsic/Saint-Laurent, embauche de manutentionnaires. Plus petit qu’Amazon.",
        "angle": "Bassin pick-pack Deslauriers ; ne pas écrire au CEO pour un commis.",
        "notes": "0 email vérifiable sur source officielle. Cellules email vides.",
    },
    {
        "name": "FortNine",
        "website": "https://www.fortnine.ca",
        "city": "Montréal",
        "sector": "E-commerce / entrepôt powersports",
        "employees": 80,
        "activity": "Entrepôt e-comm (Canada's Motorcycle / FortNine), horaires variables incl. week-end",
        "hiring_signal": "Warehouse Associate — picking, horaire flexible dont week-ends (sept. 2026)",
        "offers": 1,
        "roles": "Commis d’entrepôt — préparation de commandes",
        "shift": "Flexible / week-ends possibles",
        "ops_roles": True,
        "night_shift": True,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Montréal (QC)",
        "src_co": "https://www.fortnine.ca",
        "src_job": "Offre Warehouse Associate / Commis d’entrepôt — préparation de commandes (sept. 2026)",
        "src_person": "",
        "src_email": "Aucun courriel public vérifié.",
        "confidence": "Moyen",
        "why": "E-comm en croissance, picking + week-end : besoin opérationnel classique Talendus.",
        "angle": "Préparateurs d’entrepôt à horaires flexibles.",
        "notes": "0 email vérifiable. Ne pas inventer careers@fortnine.",
    },
    {
        "name": "XTL Transport",
        "website": "https://www.xtl.com",
        "city": "Montréal",
        "sector": "Transport / logistique",
        "employees": 400,
        "activity": "Flotte + répartition Montréal, transport/distribution",
        "hiring_signal": "Répartiteur / Dispatch — page carrière officielle applytojob",
        "offers": 1,
        "roles": "Répartiteur / dispatch",
        "shift": "Ops (non détaillé)",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 3,
        "person1": "Frédérick",
        "title1": "Contact recrutement mentionné (poste 5147)",
        "li1": "",
        "emails": [],
        "phone": "514-636-1499 poste 5147",
        "address": "Montréal (QC)",
        "src_co": "https://www.xtl.com",
        "src_job": "https://xtltransportlogistics.applytojob.com/apply/xN8e3JRnIX/Rpartiteur-Dispatch",
        "src_person": "Offre officielle : « contacter Frédérick au 514-636-1499 poste 5147 »",
        "src_email": "Aucun courriel publié sur l’offre (téléphone seulement).",
        "confidence": "Moyen",
        "why": "Répartiteur = poste clé difficile. Taille mid-market Montréal.",
        "angle": "Mandat répartiteur bilingue, pas un volume d’entrepôt.",
        "notes": "0 email. Prénom seulement — pas inventé en fiche complète.",
    },
    {
        "name": "Mactrans Logistique",
        "website": "https://mactrans.ca",
        "city": "Longueuil",
        "sector": "3PL / courtage transport",
        "employees": 40,
        "activity": "Gestion transport routier/rail/maritime, 3PL, Longueuil",
        "hiring_signal": "Page entreprise Jobillico + recrutement ventes/ops (profil employeur)",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "370, chemin de Chambly, bureau 120, Longueuil (QC) J4H 3Z6",
        "src_co": "https://mactrans.ca + https://www.jobillico.com/voir-entreprise/mactrans-logistique-montreal",
        "src_job": "Profil Jobillico Mactrans Logistique",
        "src_person": "",
        "src_email": "Aucun courriel public vérifié.",
        "confidence": "Moyen-faible",
        "why": "3PL PME Rive-Sud, plus courtage que plancher — à activer si offres ops.",
        "angle": "Coordonnateurs transport / CS plutôt que caristes.",
        "notes": "0 email vérifiable.",
    },
    {
        "name": "J.G. Rive-Sud & Légumes",
        "website": "",
        "city": "Longueuil",
        "sector": "Distribution alimentaire",
        "employees": 40,
        "activity": "Livraison produits frais HRI, camions 26' reefers, 12–20 arrêts/jour GMA",
        "hiring_signal": "2 chauffeurs classe 3 temps plein/partiel (offre juin 2026)",
        "offers": 2,
        "roles": "Chauffeur-livreur classe 3",
        "shift": "Jour, horaire 2 à 5 jours",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": True,
        "hard_to_fill": True,
        "need_score": 4,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Rive-Sud de Montréal (QC)",
        "src_co": "Offre employeur J.G. Rive-Sud & Légumes Inc. (affichage public 2026)",
        "src_job": "Offre Chauffeur Livreur Classe 3 — 2 postes",
        "src_person": "",
        "src_email": "Aucun courriel public dans l’offre (candidature via portail).",
        "confidence": "Moyen — signal fort, contact faible",
        "why": "PME alimentaire qui cherche 2 livreurs à la fois : pénurie de classe 3 locale.",
        "angle": "Deux chauffeurs classe 3 reefers, horaires flexibles.",
        "notes": "0 email. Site web non confirmé.",
    },
    {
        "name": "Remorquage Unipro",
        "website": "https://remorquageunipro.ca",
        "city": "Dorval",
        "sector": "Transport spécialisé / remorquage",
        "employees": 25,
        "activity": "Répartition remorquage léger/lourd, Dorval, quarts jour/soir/week-end",
        "hiring_signal": "Répartiteur jour/soir/week-end — page carrière officielle",
        "offers": 1,
        "roles": "Répartiteur / répartitrice — transport et remorquage",
        "shift": "Jour / soir / fin de semaine",
        "ops_roles": True,
        "night_shift": True,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "514-685-0300",
        "address": "Dorval (QC)",
        "src_co": "https://remorquageunipro.ca",
        "src_job": "https://remorquageunipro.ca/carriere/repartiteur-repartitrice-transport-et-remorquage/",
        "src_person": "",
        "src_email": "Aucun courriel sur la page carrière (téléphone seulement).",
        "confidence": "Moyen",
        "why": "Répartition multi-quarts près de l’aéroport — poste stress, roulement élevé.",
        "angle": "Répartiteur bilingue soir/week-end.",
        "notes": "0 email vérifiable.",
    },
    {
        "name": "Caratrans Logistique",
        "website": "https://www.caratrans.com",
        "city": "Montréal",
        "sector": "3PL / transport",
        "employees": 10,
        "activity": "Logistique et transport spécialisés, très petite équipe",
        "hiring_signal": "Coordonnateur logistique recherché (publication LinkedIn entreprise, 2024) — à reconfirmer",
        "offers": 0,
        "roles": "Coordonnateur(trice) logistique (signal antérieur)",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "Marie Michelle Caron",
        "title1": "Directrice Opérations et Solutions Clients",
        "li1": "https://www.linkedin.com/in/marie-michelle-caron-7538b7132",
        "emails": [],
        "phone": "",
        "address": "Montréal (QC)",
        "src_co": "Page LinkedIn entreprise Groupe Caratrans",
        "src_job": "Publication LinkedIn entreprise 2024 — coordonnateur logistique",
        "src_person": "Profil LinkedIn public Marie Michelle Caron",
        "src_email": "Aucun email professionnel public trouvé. Ne pas inventer.",
        "confidence": "Moyen sur la personne ; faible sur l’offre actuelle",
        "why": "Décideuse ops identifiée dans une micro-3PL — conversion owner/ops.",
        "angle": "Parler à la directrice ops d’un renfort coordonnateur / chauffeur selon volume.",
        "notes": "0 email. Offre 2024 non reconfirmée en 2026.",
    },
    {
        "name": "Fredyma International",
        "website": "https://www.fredyma.com",
        "city": "Laval",
        "sector": "3PL / transport international",
        "employees": 25,
        "activity": "Entreposage Laval, FCL, groupage import/export, 25 ans",
        "hiring_signal": "Ops 3PL Laval (offre non listée aujourd’hui)",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "514-965-2832",
        "address": "5755, boulevard des Rossignols, Laval (QC) H7L 5X4",
        "src_co": "https://www.fredyma.com/entreprise-3pl.php",
        "src_job": "",
        "src_person": "",
        "src_email": "Formulaire seulement — aucun courriel en clair.",
        "confidence": "Moyen-faible",
        "why": "3PL Laval avec quais conteneurs — besoin ponctuel de débardeurs/caristes.",
        "angle": "Renfort réception conteneurs / caristes.",
        "notes": "0 email vérifiable.",
    },
    {
        "name": "Boutin 3PL",
        "website": "https://www.boutin3pl.com",
        "city": "Boucherville",
        "sector": "3PL alimentaire",
        "employees": 15,
        "activity": "Préparation commandes, transbordement conteneurs, certifié SQF, depuis 1945",
        "hiring_signal": "Croissance d’équipe LinkedIn (+6) ; ops alimentaire Boucherville",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "Jean-Philippe Boutin",
        "title1": "Direction (signataire public LinkedIn entreprise)",
        "li1": "",
        "emails": [
            {"addr": "info@boutin3pl.com", "kind": "general", "who": "", "proof": "Page Contact officielle boutin3pl.com/en/contact-us/"},
            {"addr": "renseignements.personnels@boutin3pl.com", "kind": "other", "who": "Jean-Philippe Boutin", "proof": "Politique de confidentialité officielle boutin3pl.com/politique/"},
        ],
        "phone": "1-450-906-8900",
        "address": "1400, Graham-Bell, Boucherville (QC) J4B 6H5",
        "src_co": "https://www.boutin3pl.com/en/contact-us/",
        "src_job": "",
        "src_person": "Politique de confidentialité — Jean-Philippe Boutin",
        "src_email": "Site officiel EN contact (info@) + politique (renseignements.personnels@)",
        "confidence": "Élevé sur info@",
        "why": "3PL alimentaire Rive-Sud — email officiel confirmé sur la page Contact EN.",
        "angle": "Préparateurs / caristes SQF à info@.",
        "notes": "2 emails. Doublon catalogue BOUTIN 3PL fusionné à l’export.",
    },
    {
        "name": "Trans-Pro Logistique",
        "website": "https://trans-pro.com",
        "city": "Montréal",
        "sector": "Logistique / transport frais",
        "employees": 60,
        "activity": "Transport produits frais, bureaux multi-villes, équipe ops/ventes",
        "hiring_signal": "Page carrière « toujours à la recherche » ops/ventes",
        "offers": 0,
        "roles": "",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": True,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Montréal (QC)",
        "src_co": "https://trans-pro.com/fr/a-propos/",
        "src_job": "https://trans-pro.com/fr/a-propos/ — bloc carrières",
        "src_person": "",
        "src_email": "Aucun courriel public vérifié.",
        "confidence": "Moyen-faible",
        "why": "Logistique frais, croissance géographique — à relancer quand une offre ops sort.",
        "angle": "Coordonnateurs / répartiteurs produits frais.",
        "notes": "0 email.",
    },
    {
        "name": "Madessa",
        "website": "",
        "city": "Montréal",
        "sector": "Manufacturier / entrepôt",
        "employees": 80,
        "activity": "Ops industrielles Montréal — cariste continental de nuit",
        "hiring_signal": "Cariste continental de nuit — offre active (août–sept. 2026)",
        "offers": 1,
        "roles": "Cariste continental de nuit",
        "shift": "Nuit",
        "ops_roles": True,
        "night_shift": True,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Montréal (QC)",
        "src_co": "Offre employeur Madessa (agrégateurs d’emploi, août 2026)",
        "src_job": "Cariste continental de nuit à Montréal",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Moyen-faible (site non confirmé)",
        "why": "Quart de nuit cariste — profil Talendus cœur de métier.",
        "angle": "Caristes nuit seulement.",
        "notes": "0 email. Site officiel non confirmé — ne pas prioriser sans revalidation.",
    },
    {
        "name": "Groupe Beauchesne",
        "website": "",
        "city": "Laval",
        "sector": "Distribution / entrepôt",
        "employees": 50,
        "activity": "Entrepôt Laval — cariste de soir",
        "hiring_signal": "Cariste de soir — Entrepôt Laval (agrégateur Indeed)",
        "offers": 1,
        "roles": "Cariste de soir",
        "shift": "Soir",
        "ops_roles": True,
        "night_shift": True,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": True,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Laval (QC)",
        "src_co": "Offre « Cariste de soir-Entrepôt Laval » — Groupe Beauchesne",
        "src_job": "Indeed / agrégateurs — Laval",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Moyen-faible",
        "why": "Cariste de soir Laval — besoin opérationnel clair.",
        "angle": "Caristes soir Laval.",
        "notes": "0 email. Confirmer le site avant envoi.",
    },
    {
        "name": "ITC Technologies",
        "website": "",
        "city": "Laval",
        "sector": "Distribution / entrepôt",
        "employees": 40,
        "activity": "Entrepôt Laval",
        "hiring_signal": "Cariste manutentionnaire — Laval (Indeed)",
        "offers": 1,
        "roles": "Cariste manutentionnaire",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Laval (QC)",
        "src_co": "Offre Indeed ITC Technologies Inc. Laval",
        "src_job": "Cariste manutentionnaire — Laval",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Moyen-faible",
        "why": "Poste cariste Laval.",
        "angle": "Cariste / manutentionnaire.",
        "notes": "0 email.",
    },
    {
        "name": "Servomax",
        "website": "",
        "city": "Boucherville",
        "sector": "Distribution / entrepôt",
        "employees": 30,
        "activity": "Entrepôt + service client Boucherville",
        "hiring_signal": "Commis entrepôt et service client — Boucherville",
        "offers": 1,
        "roles": "Commis entrepôt / service client",
        "shift": "Jour",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Boucherville (QC)",
        "src_co": "Offre Indeed Servomax Inc.",
        "src_job": "Commis entrepôt et service client — Boucherville",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Moyen-faible",
        "why": "PME Rive-Sud, poste hybride entrepôt.",
        "angle": "Commis polyvalent entrepôt.",
        "notes": "0 email.",
    },
    {
        "name": "Vanfax",
        "website": "",
        "city": "Boucherville",
        "sector": "Distribution",
        "employees": 60,
        "activity": "Distribution Boucherville — manutention temporaire",
        "hiring_signal": "Manutentionnaire (contrat) — Boucherville",
        "offers": 1,
        "roles": "Manutentionnaire (contrat)",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Boucherville (QC)",
        "src_co": "Offre Indeed Manutentionnaire (contrat) - Vanfax",
        "src_job": "Indeed — Boucherville",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Moyen-faible",
        "why": "Contrat manutention : porte d’entrée temporaire → permanent.",
        "angle": "Mandat temporaire manutentionnaires.",
        "notes": "0 email.",
    },
    {
        "name": "Service Remtec",
        "website": "",
        "city": "Montréal",
        "sector": "Entrepôt",
        "employees": 25,
        "activity": "Entrepôt / cariste",
        "hiring_signal": "Commis entrepôt / cariste",
        "offers": 1,
        "roles": "Commis entrepôt / cariste",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Grand Montréal (QC)",
        "src_co": "Offre Indeed Service Remtec",
        "src_job": "Commis entrepôt / cariste",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Faible-moyen",
        "why": "Poste cariste mixte.",
        "angle": "Cariste / commis.",
        "notes": "0 email. Confirmer l’adresse.",
    },
    {
        "name": "Mat&Max",
        "website": "",
        "city": "Montréal",
        "sector": "Distribution / entrepôt",
        "employees": 40,
        "activity": "Inventaire et entrepôt",
        "hiring_signal": "Commis à l’inventaire et entrepôt",
        "offers": 1,
        "roles": "Commis inventaire / entrepôt",
        "shift": "Jour",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 3,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "Grand Montréal (QC)",
        "src_co": "Offre Indeed COMMIS À L’INVENTAIRE ET ENTREPÔT — Mat&Max",
        "src_job": "Indeed",
        "src_person": "",
        "src_email": "Aucun courriel public.",
        "confidence": "Faible-moyen",
        "why": "Commis inventaire — volume possible en saison.",
        "angle": "Commis inventaire.",
        "notes": "0 email.",
    },
    {
        "name": "Entrepôt de Montréal 1470 (Groupe Monaco)",
        "website": "https://groupe-monaco.ca",
        "city": "Montréal",
        "sector": "Distribution pièces auto",
        "employees": 150,
        "activity": "CD 160 000 pi², 240 000 SKU, livraisons jobbers, sièges Jarry",
        "hiring_signal": "Profil employeur Jobillico (1 offre récente listée hors GMA) — ops distribution continues",
        "offers": 1,
        "roles": "Chauffeur longue distance (affichage Jobillico) — ops CD Montréal en continu",
        "shift": "",
        "ops_roles": True,
        "night_shift": False,
        "growth": False,
        "repeat_roles": False,
        "hard_to_fill": False,
        "need_score": 2,
        "person1": "",
        "title1": "",
        "li1": "",
        "emails": [],
        "phone": "",
        "address": "3455, rue Jarry Est, Montréal (QC) H1Z 2G1",
        "src_co": "https://groupe-monaco.ca/ + profil Jobillico Entrepôt de Montréal 1470 inc.",
        "src_job": "https://www.jobillico.com/see-company/entrepot-de-montreal-1470-inc",
        "src_person": "",
        "src_email": "Aucun courriel public vérifié.",
        "confidence": "Moyen",
        "why": "Gros CD pièces auto Saint-Michel — besoin chronique chauffeur/commis.",
        "angle": "Livreurs locaux / commis d’entrepôt pièces.",
        "notes": "0 email.",
    },
]


def flatten(row: dict, rank: int, score: int) -> dict:
    emails = [e for e in row.get("emails") or [] if e.get("addr")]
    e1 = emails[0] if emails else {}
    e2 = emails[1] if len(emails) > 1 else {}
    prio = priority_of(score)
    contact_prio = "Immédiat" if prio == "A" else "Cette semaine" if prio == "B" else "File d’attente" if prio == "C" else "Ne pas prioriser"
    return {
        "Rang": rank,
        "Score Talendus": score,
        "Priorité": prio,
        "Nom entreprise": row["name"],
        "Site web": row.get("website") or "",
        "Ville": row["city"],
        "Secteur": row["sector"],
        "Nombre d'employés estimé": row.get("employees") or "",
        "Type d'activité": row.get("activity") or "",
        "Signal de recrutement": row.get("hiring_signal") or "",
        "Nombre d'offres actuelles": row.get("offers") if row.get("offers") is not None else "",
        "Postes recherchés": row.get("roles") or "",
        "Quart de travail": row.get("shift") or "",
        "Nom du décideur #1": row.get("person1") or "",
        "Fonction #1": row.get("title1") or (e1.get("who") or ""),
        "LinkedIn #1": row.get("li1") or "",
        "Email #1": e1.get("addr") or "",
        "Vérification email #1": e1.get("proof") or "",
        "Nom du décideur #2": row.get("person2") or "",
        "Fonction #2": row.get("title2") or (e2.get("who") or ""),
        "LinkedIn #2": row.get("li2") or "",
        "Email #2": e2.get("addr") or "",
        "Vérification email #2": e2.get("proof") or "",
        "Email général vérifié": email_by_kind(emails, "general"),
        "Email RH vérifié": email_by_kind(emails, "rh"),
        "Email recrutement vérifié": email_by_kind(emails, "recrutement"),
        "Téléphone": row.get("phone") or "",
        "Adresse": row.get("address") or "",
        "Source entreprise": row.get("src_co") or "",
        "Source offre emploi": row.get("src_job") or "",
        "Source personne": row.get("src_person") or "",
        "Source email": row.get("src_email") or "",
        "Date de vérification": VERIFIED_ON,
        "Niveau de confiance": row.get("confidence") or "",
        "Pourquoi Talendus devrait les contacter": row.get("why") or "",
        "Angle d'approche recommandé": row.get("angle") or "",
        "Priorité de contact": contact_prio,
        "Notes": row.get("notes") or "",
        "Taille bande": size_band(int(row.get("employees") or 0)),
        "Emails vérifiés (n)": len(emails),
        "Score besoin recrutement /5": row.get("need_score") or "",
        "Présence Talendus": {
            "catalogue": "Catalogue",
            "indeed": "Veille Indeed",
            "nouveau": "Nouveau",
        }.get(row.get("presence") or "", "Nouveau"),
    }


def merged_companies() -> list[dict]:
    """PME de la 1re passe + hubs catalogue/Indeed/nouveaux. Plus d’emails gagne."""
    by_key: dict[str, dict] = {}
    for raw in list(COMPANIES) + list(HUBS):
        key = normalize_company_name(raw["name"])
        prev = by_key.get(key)
        if prev is None or len(raw.get("emails") or []) > len(prev.get("emails") or []):
            by_key[key] = raw
    return list(by_key.values())


def build() -> list[dict]:
    kept = []
    for raw in merged_companies():
        raw = dict(raw)
        raw["_score"] = score_row(raw)
        kept.append(raw)
    kept.sort(key=lambda r: (-r["_score"], r["name"]))
    return [flatten(r, i + 1, r["_score"]) for i, r in enumerate(kept)]


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: list[dict], path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Prospection"
    header_fill = PatternFill("solid", fgColor="1B365D")
    header_font = Font(color="FFFFFF", bold=True)
    fills = {
        "A": PatternFill("solid", fgColor="FDE68A"),
        "B": PatternFill("solid", fgColor="FED7AA"),
        "C": PatternFill("solid", fgColor="FEF3C7"),
        "D": PatternFill("solid", fgColor="E5E7EB"),
    }
    ws.append(COLUMNS)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for row in rows:
        ws.append([row.get(col, "") for col in COLUMNS])
        fill = fills.get(row["Priorité"])
        if fill:
            ws.cell(ws.max_row, 3).fill = fill
    widths = {1: 8, 2: 12, 3: 10, 4: 32, 5: 36, 6: 16, 10: 48, 35: 48, 36: 40, 38: 36}
    for idx in range(1, len(COLUMNS) + 1):
        ws.column_dimensions[get_column_letter(idx)].width = widths.get(idx, 22)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{ws.max_row}"
    ws.freeze_panes = "A2"
    summary = wb.create_sheet("Resume")
    a = sum(1 for r in rows if r["Priorité"] == "A")
    b = sum(1 for r in rows if r["Priorité"] == "B")
    c = sum(1 for r in rows if r["Priorité"] == "C")
    people = sum(1 for r in rows if r["Nom du décideur #1"])
    emails = sum(int(r["Emails vérifiés (n)"] or 0) for r in rows)
    with3 = sum(1 for r in rows if int(r["Emails vérifiés (n)"] or 0) >= 3)
    with5 = sum(1 for r in rows if int(r["Emails vérifiés (n)"] or 0) >= 5)
    active = sum(1 for r in rows if int(r["Nombre d'offres actuelles"] or 0) >= 1)
    lines = [
        ("Date", VERIFIED_ON),
        ("Entreprises (catalogue + nouveaux + veille)", len(rows)),
        ("Dont déjà au catalogue", sum(1 for r in rows if r["Présence Talendus"] == "Catalogue")),
        ("Dont veille Indeed", sum(1 for r in rows if r["Présence Talendus"] == "Veille Indeed")),
        ("Dont nouvelles (Nationex, ICS, Fastfrate, PME)", sum(1 for r in rows if r["Présence Talendus"] == "Nouveau")),
        ("Priorité A (80–100)", a),
        ("Priorité B (65–79)", b),
        ("Priorité C (50–64)", c),
        ("Personnes identifiées", people),
        ("Emails vérifiés (total boîtes)", emails),
        ("Entreprises avec 3+ emails vérifiés", with3),
        ("Entreprises avec 5 emails vérifiés", with5),
        ("Entreprises avec offre(s) active(s)", active),
        ("Règle", "PREUVE > QUANTITÉ. Aucun email inventé."),
    ]
    summary.append(["Indicateur", "Valeur"])
    for item in lines:
        summary.append(list(item))
    summary.append([])
    summary.append(["Top 20", "Score", "Pourquoi"])
    for row in rows[:20]:
        summary.append([row["Nom entreprise"], row["Score Talendus"], row["Pourquoi Talendus devrait les contacter"]])
    summary.column_dimensions["A"].width = 48
    summary.column_dimensions["B"].width = 14
    summary.column_dimensions["C"].width = 80
    wb.save(path)


def main() -> None:
    rows = build()
    csv_path = OUT_DIR / "TALENDUS_PROSPECTION_LOGISTIQUE_MONTREAL.csv"
    xlsx_path = OUT_DIR / "TALENDUS_PROSPECTION_LOGISTIQUE_MONTREAL.xlsx"
    write_csv(rows, csv_path)
    write_xlsx(rows, xlsx_path)
    a = sum(1 for r in rows if r["Priorité"] == "A")
    b = sum(1 for r in rows if r["Priorité"] == "B")
    c = sum(1 for r in rows if r["Priorité"] == "C")
    people = sum(1 for r in rows if r["Nom du décideur #1"])
    emails = sum(int(r["Emails vérifiés (n)"] or 0) for r in rows)
    with3 = sum(1 for r in rows if int(r["Emails vérifiés (n)"] or 0) >= 3)
    with5 = sum(1 for r in rows if int(r["Emails vérifiés (n)"] or 0) >= 5)
    active = sum(1 for r in rows if int(r["Nombre d'offres actuelles"] or 0) >= 1)
    print(f"Fichiers : {csv_path.name} / {xlsx_path.name}")
    print(f"Entreprises : {len(rows)}")
    print(f"A : {a}   B : {b}   C : {c}")
    print(f"Personnes identifiées : {people}")
    print(f"Emails vérifiés : {emails}")
    print(f"Entreprises 3+ emails : {with3}")
    print(f"Entreprises 5 emails : {with5}")
    print(f"Avec offres actives : {active}")
    print("--- TOP 20 ---")
    for row in rows[:20]:
        print(f"{row['Rang']:>2}. [{row['Priorité']}] {row['Score Talendus']:>3}  {row['Nom entreprise']} — {row['Ville']}")
        print(f"    {row['Pourquoi Talendus devrait les contacter']}")


if __name__ == "__main__":
    main()
