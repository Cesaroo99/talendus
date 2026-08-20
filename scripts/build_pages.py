#!/usr/bin/env python3
"""Génère les pages piliers Talendus à partir du header/footer partagés."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parts import (
    wrap as wrap_page, page_hero, speed_strip, cta_band, faq_html, proof_stats,
    FAQ_EMPLOYEURS, FAQ_CANDIDATS, FAQ_HOME, homepage_faq, cv_file_field,
    install_board,
    native_app_page,
)
from positioning import (
    homepage_after_hero, job_search_filters, employer_need_fields,
    talent_trade_options, sectors_cloud, trades_cloud, ai_coming_soon,
    human_hire_band, problems_section, approach_section, process_section,
    why_talendus_section, ai_engine_section, human_section, company_types_section,
    candidate_journey_section, for_companies_section, for_candidates_section,
    placement_process_services_section, technology_section, ai_screening_section,
    competitive_advantage_section, augmented_recruiting_section, hiring_need_form_section,
    bad_hire_calculator_section,
    job_card_html, jobs_listing_header, jobs_empty_state, job_detail_html, related_job_cards,
)
from en_pages import build_en
from seo_pages import write_fr as write_seo_fr

ROOT = Path(__file__).resolve().parents[1]
SPEED_STRIP = speed_strip("fr", "entreprise")
SPEED_TALENT = speed_strip("fr", "talent")
CTA_BAND = cta_band("fr", "gateway")
CTA_TALENT = cta_band("fr", "talent")
CTA_HIRE = cta_band("fr", "entreprise")

def alt_for(slug):
    """English path for a French slug (site-root relative)."""
    special = {
        "": "en/",
        "index.html": "en/",
        "entreprises.html": "en/employers.html",
        "employeurs.html": "en/employers.html",
        "candidats.html": "en/candidates.html",
        "emplois.html": "en/jobs.html",
        "contact.html": "en/contact.html",
        "a-propos.html": "en/about.html",
        "about.html": "en/about.html",
        "services.html": "en/services.html",
        "service.html": "en/services.html",
        "secteurs.html": "en/sectors.html",
        "blog.html": "en/blog.html",
        "blog-single.html": "en/blog.html",
        "confidentialite.html": "en/privacy.html",
        "conditions.html": "en/terms.html",
        "404.html": "en/404.html",
        "espace.html": "en/account.html",
        "espace-employeur.html": "en/account-employer.html",
        "comment-ca-fonctionne.html": "en/how-it-works.html",
        "besoin-de-recrutement.html": "en/hiring-need.html",
        "publier-une-offre.html": "en/hiring-need.html",
        "solutions-rh.html": "en/hr-solutions.html",
        "recrutement-industriel.html": "en/industrial-recruiting.html",
        "recrutement-manufacturier.html": "en/manufacturing-recruiting.html",
        "recrutement-technique.html": "en/technical-recruiting.html",
        "recrutement-permanent.html": "en/permanent-recruiting.html",
        "recrutement-temporaire.html": "en/temporary-recruiting.html",
        "chasse-de-tetes.html": "en/executive-search.html",
        "recrutement-cadres.html": "en/leadership-recruiting.html",
        "recrutement-industriel-montreal.html": "en/industrial-recruiting-montreal.html",
        "recrutement-industriel-laval.html": "en/industrial-recruiting-laval.html",
        "recrutement-industriel-longueuil.html": "en/industrial-recruiting-longueuil.html",
        "recrutement-industriel-quebec.html": "en/industrial-recruiting-quebec.html",
        "app.html": "en/app.html",
    }
    if slug in special:
        return special[slug]
    if slug.startswith("emploi-"):
        return "en/job-" + slug[len("emploi-"):]
    if slug.startswith("secteur-"):
        return "en/sector-" + slug[len("secteur-"):]
    if slug.startswith("article-"):
        return "en/" + slug
    return "en/" + slug

def wrap(title, desc, slug, body, solid=True, lang="fr", alt=None, **seo):
    if alt is None:
        alt = alt_for(slug) if lang == "fr" else ""
    return wrap_page(title, desc, slug, body, solid=solid, lang=lang, alt=alt, **seo)


def job_ld(title, city, slug, typ, sal, req, lang="fr"):
    host = "https://talendus.ca"
    url = f"{host}/emploi-{slug}.html" if lang == "fr" else f"{host}/en/job-{slug}.html"
    emp = "FULL_TIME" if (typ or "").lower().startswith("perm") else "TEMPORARY"
    return {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": title,
        "description": req,
        "identifier": {"@type": "PropertyValue", "name": "Talendus", "value": slug},
        "datePosted": "2026-07-20",
        "employmentType": emp,
        "hiringOrganization": {"@type": "EmploymentAgency", "name": "Talendus", "sameAs": host},
        "jobLocation": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": city,
                "addressRegion": "QC",
                "addressCountry": "CA",
            },
        },
        "baseSalary": {"@type": "MonetaryAmount", "currency": "CAD", "value": sal},
        "url": url,
    }

def write(name, html):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", name)

# slug, titre, ville, cat, type, salaire, horaire, exigences, secteur, compétences, expérience
JOBS = [
    ("cariste", "Cariste", "Laval", "entrepot", "Permanent", "22 à 26 $/h", "Temps plein", "Permis chariot élévateur, 1 an d'expérience en entrepôt.", "transport", "conduite de chariot élévateur", "intermediaire"),
    ("operateur-production", "Opérateur de production", "Longueuil", "production", "Permanent", "20 à 24 $/h", "Temps plein", "Expérience de production, capacité à suivre des procédures, travail d'équipe.", "manufacturier", "production", "debutant"),
    ("soudeur", "Soudeur-monteur", "Drummondville", "metallurgie", "Permanent", "28 à 34 $/h", "Temps plein", "Soudure MIG/TIG, lecture de plans, cartes de compétences un atout.", "manufacturier", "soudure", "intermediaire"),
    ("machiniste-cnc", "Machiniste CNC", "Saint-Jérôme", "manufacturier", "Permanent", "30 à 38 $/h", "Temps plein", "Programmation ou set-up, lecture de dessins, 3 ans d'expérience.", "manufacturier", "usinage CNC", "senior"),
    ("electromecanicien", "Électromécanicien", "Montréal", "maintenance", "Permanent", "32 à 40 $/h", "Temps plein", "Dépannage, hydraulique, pneumatique, électricité.", "ingenierie", "électromécanique", "intermediaire"),
    ("mecanicien-industriel", "Mécanicien industriel", "Sherbrooke", "maintenance", "Permanent", "30 à 36 $/h", "Temps plein", "Entretien préventif, alignement, convoyeurs, fiabilité.", "manufacturier", "mécanique", "intermediaire"),
    ("journalier-usine", "Journalier d'usine", "Boucherville", "production", "Permanent", "18 à 21 $/h", "Temps plein", "Bonne condition physique, ponctualité, formation interne offerte.", "manufacturier", "production", "debutant"),
    ("superviseur-production", "Superviseur de production", "Trois-Rivières", "supervision", "Permanent", "70 000 à 85 000 $", "Temps plein", "Leadership d'équipe, KPI, 5 ans en production.", "manufacturier", "supervision", "senior"),
    ("coordonnateur-logistique", "Coordonnateur logistique", "Anjou", "logistique", "Permanent", "55 000 à 68 000 $", "Temps plein", "WMS, planification, anglais un atout.", "transport", "logistique, WMS", "intermediaire"),
    ("directeur-usine", "Directeur d'usine", "Québec", "cadres", "Permanent", "120 000 à 150 000 $", "Temps plein", "P&L, Lean, gestion d'un site 100+ employés. Mandat confidentiel.", "manufacturier", "direction", "senior"),
    ("developpeur", "Développeur", "Montréal", "technologie", "Permanent", "75 000 à 95 000 $", "Temps plein", "Python ou JavaScript, 2 ans d'expérience, travail en équipe.", "technologie", "Python, JavaScript", "intermediaire"),
    ("comptable", "Comptable", "Québec", "finance", "Permanent", "55 000 à 70 000 $", "Temps plein", "Comptabilité, Excel, diplôme pertinent.", "finance", "Excel, comptabilité", "intermediaire"),
    ("ingenieur", "Ingénieur", "Sherbrooke", "ingenierie", "Permanent", "80 000 à 100 000 $", "Temps plein", "Ingénierie, gestion de projet, 3 ans d'expérience.", "ingenierie", "gestion de projet", "senior"),
    ("chauffeur", "Chauffeur", "Anjou", "transport", "Permanent", "22 à 28 $/h", "Temps plein", "Permis de conduire valide, ponctualité, dossier de conduite propre.", "transport", "conduite", "intermediaire"),
    ("infirmier", "Infirmier", "Laval", "sante", "Permanent", "32 à 42 $/h", "Temps plein", "Permis OIIQ, expérience clinique, travail d'équipe.", "sante", "soins", "intermediaire"),
    ("vendeur", "Vendeur", "Longueuil", "commerce", "Permanent", "18 à 24 $/h", "Temps plein", "Vente au détail, service client, aisance relationnelle.", "commerce", "vente", "debutant"),
    ("responsable-rh", "Responsable RH", "Montréal", "administration", "Permanent", "70 000 à 90 000 $", "Temps plein", "Recrutement, relations de travail, 5 ans en RH.", "administration", "RH", "senior"),
    ("specialiste-marketing", "Spécialiste marketing", "Montréal", "marketing", "Permanent", "55 000 à 75 000 $", "Temps plein", "Marketing digital, communication, gestion de campagnes.", "marketing", "marketing", "intermediaire"),
]

SECTORS = [
    ("manufacturier", "Manufacturier", "Recrutement manufacturier au Québec", "Un exemple parmi d'autres : fabrication, assemblage et métiers de production. Talendus recrute aussi bien au-delà de l'industrie."),
    ("production", "Production", "Recrutement en production au Québec", "Lignes, méthodes, qualité et supervision. Un des nombreux métiers que Talendus peut pourvoir."),
    ("entrepot", "Entrepôt", "Recrutement entrepôt Québec", "Caristes, préparateurs, commis et superviseurs d'entrepôt, un exemple de profils logistiques."),
    ("logistique", "Logistique", "Recrutement logistique Québec", "Planification, transport, WMS et coordination. La logistique est un secteur parmi d'autres."),
    ("distribution", "Distribution", "Recrutement distribution Québec", "Centres de distribution, expédition, réception et gestion des stocks."),
    ("transport", "Transport", "Recrutement transport et logistique", "Chauffeurs, coordination transport et flux. Talendus accompagne aussi d'autres industries."),
    ("transformation-alimentaire", "Transformation alimentaire", "Recrutement alimentaire Québec", "Production alimentaire : hygiène, opérateurs et supervision. Un exemple, pas une spécialisation exclusive."),
    ("metallurgie", "Métallurgie", "Recrutement métallurgie et soudure Québec", "Soudure, usinage, fabrication métallique. D'autres métiers et secteurs sont tout autant concernés."),
    ("plasturgie", "Plasturgie", "Recrutement plasturgie Québec", "Injection, extrusion, set-up et techniciens de procédé."),
    ("maintenance", "Maintenance", "Recrutement maintenance Québec", "Techniciens, mécaniciens et responsables fiabilité, parmi une grande variété de métiers."),
]

ARTICLES = [
    ("mauvaise-embauche", "Combien coûte une mauvaise embauche ?", "RH", "usine-equipe.jpg",
     "Un mauvais fit ne se limite pas au salaire. Entre formation, heures supplémentaires, perte de productivité et roulement, la facture grimpe vite, dans n'importe quel secteur."),
    ("machiniste-cnc", "Recruter un machiniste CNC au Québec en 2026", "Métiers", "cnc-machiniste.jpg",
     "Le machiniste CNC reste un profil tendu. Voici comment attirer, évaluer et retenir ce talent, un exemple parmi beaucoup d'autres métiers."),
    ("caristes-entrepot", "Pénurie de caristes : stratégies pour les entrepôts", "Logistique", "entrepot-logistique.jpg",
     "Les centres de distribution se disputent les caristes expérimentés. Trois leviers concrets, transposables à d'autres métiers rares."),
    ("superviseur-production", "Superviseur de production : le profil qui change une équipe", "Production", "usine-equipe.jpg",
     "Un bon superviseur stabilise la qualité et le climat. Voici le portrait que nous validons, applicable à d'autres rôles de gestion."),
    ("roulement-manufacturier", "Réduire le roulement en recrutement", "Recrutement", "soudeur-atelier.jpg",
     "Le roulement n'est pas qu'un problème salarial. Accueil, clarté du poste et adéquation culturelle font la différence, quel que soit le secteur."),
]

TOPICS = [
    "Rédiger une offre d'emploi claire", "Trop de candidatures, trop peu de fit",
    "Recruter un développeur", "Recruter un comptable", "Recruter en santé",
    "Recrutement en construction", "Télétravail et localisation", "Chasse de têtes cadres",
    "Intégration 30/60/90", "Marque employeur", "Tests en entrevue",
    "Contrats temporaires vs permanents", "Rétention des métiers spécialisés",
    "Coût d'un poste vacant", "Recruter en région", "Compétences plutôt que titres",
    "FAQ garanties de remplacement", "Préparer une entrevue de gestionnaire",
]


INDEX_BODY = r"""
<div class="hero2-arrow-hero tl-gateway-hero">
  <div class="hero2-slider-area">
        <div class="img1"><img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe au travail" fetchpriority="high" decoding="async"></div>
        <div class="container">
            <div class="hero2-heading tl-hero-lock">
                <h5>Talendus. Agence de placement intelligente.</h5>
                <div class="space16"></div>
                <h1 data-persona-only="gateway">Vous recrutez ou vous cherchez un emploi ?</h1>
                <h1 data-persona-only="talent">Votre parcours, étudié. Les bonnes opportunités.</h1>
                <h1 data-persona-only="entreprise">Les bons talents. Plus rapidement. Plus intelligemment.</h1>
                <div class="space16"></div>
                <p data-persona-only="gateway">Choisissez votre côté pour continuer. Candidats et entreprises n'arrivent pas sur les mêmes pages.</p>
                <p data-persona-only="talent">Créez votre profil, déposez votre CV. Nous étudions votre parcours et vous contactons lorsqu'une opportunité correspond. Gratuit pour vous. Appelez-nous ou écrivez-nous : un conseiller s'en occupe.</p>
                <p data-persona-only="entreprise">Confiez-nous votre besoin. Nous recherchons, présélectionnons et vous présentons une shortlist qualifiée. Vous ne parcourez pas une base de CV. Vous gardez la décision finale.</p>
            </div>
            <div class="tl-persona-cards" data-persona-only="gateway">
              <a class="tl-persona-card is-talent" href="candidats.html" data-set-persona="talent">
                <span class="tl-kicker">Candidats</span>
                <h2>Je cherche un emploi</h2>
                <p>Entrez dans le réseau Talendus. Profil, CV, suite du parcours : tout se passe du côté candidats.</p>
                <span class="tl-persona-go">Créer mon profil <i class="fa-solid fa-arrow-right"></i></span>
              </a>
              <a class="tl-persona-card is-hire" href="entreprises.html" data-set-persona="entreprise">
                <span class="tl-kicker">Entreprises</span>
                <h2>Je recrute</h2>
                <p>Transmettez le poste à pourvoir. La recherche, la présélection et la shortlist se font du côté entreprises.</p>
                <span class="tl-persona-go">Confier mon recrutement <i class="fa-solid fa-arrow-right"></i></span>
              </a>
            </div>
        </div>
  </div>
</div>
"""

write("index.html", wrap(
    "Talendus | Agence de placement intelligente",
    "Talendus est une agence de placement. Entreprises : confiez un besoin, recevez une shortlist. Candidats : créez un profil, soyez contacté lorsqu'une opportunité correspond. Tous secteurs.",
    "",
    INDEX_BODY + homepage_after_hero("fr") + homepage_faq("fr") + sectors_cloud("fr") + trades_cloud("fr"),
    solid=False,
))


def simple_page(title, desc, slug, kicker, h1, lead, inner, actions=""):
    body = page_hero(kicker, h1, lead, actions) + inner
    write(slug, wrap(title, desc, slug, body))


# À propos
simple_page(
    "À propos de Talendus | Agence de placement intelligente",
    "Talendus est une agence de placement qui combine déjà expertise humaine, technologie et intelligence artificielle. Tous secteurs, tous métiers.",
    "a-propos.html", "L'agence", "Talendus construit une nouvelle génération de recrutement : humain, technologique et déjà augmenté par l'IA.",
    "Nous ne donnons pas simplement accès à des candidats. Nous faisons le travail de recherche pour les entreprises. L'intelligence artificielle fait déjà partie de la manière dont Talendus travaille aujourd'hui.",
    """
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <div class="tl-prose" style="max-width:none">
    <h2 class="tl-h2">Pourquoi nous existons</h2>
    <p>Trop d'entreprises perdent des semaines à chercher les bonnes personnes, à trier trop de candidatures, ou à laisser un processus s'éterniser. Trop de talents envoient des CV dans le vide. Le recrutement mérite mieux qu'un tableau d'affichage ou qu'un logiciel que l'on doit apprendre à utiliser seul.</p>
    <p>Talendus a été conçu comme une agence de placement nouvelle génération : généraliste, humaine et technologique. Lorsqu'une entreprise a un besoin, elle nous le transmet. Nous prenons en charge la recherche et la présélection. L'intelligence artificielle est déjà au cœur de nos outils internes : elle accélère l'analyse, la recherche et certaines étapes de présélection. Les conseillers restent là pour comprendre, qualifier et présenter. L'entreprise garde la décision finale.</p>
    <h2 class="tl-h2">Ce que nous faisons</h2>
    <p>Nous rapprochons les entreprises et les talents. Développeurs, comptables, soudeurs, infirmiers, chauffeurs, responsables RH, gestionnaires, et bien d'autres métiers, dans tous les secteurs. Un conseiller présente les dossiers et reste disponible des deux côtés : talents, appelez-nous pour un mandat ; entreprises, confiez-nous un besoin.</p>
    <p>Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA : « nous recrutons » signifie que Talendus mène la recherche et la présélection pour le compte de l'entreprise. « Plus vite » : nos outils et l'IA accélèrent déjà certaines étapes. « Plus intelligemment » : données, technologie, IA et expertise humaine, ensemble, dès aujourd'hui.</p>
    <h2 class="tl-h2">Ce que nous ne sommes pas</h2>
    <p>Pas un job board où l'entreprise parcourt une base. Pas une marketplace. Pas un ATS en libre-service. Pas un logiciel qui promet un candidat parfait sans humain. La technologie reste au service du processus Talendus.</p>
    <h2 class="tl-h2">L'IA, déjà dans notre identité opérationnelle</h2>
    <p>Talendus utilise déjà l'intelligence artificielle dans ses opérations de recrutement. Elle n'est pas une vision à long terme ni une fonctionnalité « bientôt disponible ». Nos équipes s'appuient sur des outils internes pour analyser les CV, extraire les compétences, rapprocher un profil d'un poste, synthétiser l'information et prioriser les dossiers à examiner. Vous n'avez pas à utiliser ces outils : nous les mobilisons pour votre compte. La qualification finale reste humaine.</p>
    </div>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe au travail">
      </div>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">Comment nous travaillons</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Généraliste</h3><p>Tous les secteurs, toutes les tailles d'entreprise, une grande variété de métiers. Le secteur est un paramètre du mandat, pas l'identité de l'agence.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Intermédiaire</h3><p>L'entreprise confie. Le candidat crée son profil. Talendus recherche, présélectionne, présente. Personne n'est laissé seul devant une base de données.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Humain et technologique</h3><p>L'IA accélère l'analyse interne. Les conseillers valident la pertinence. Vous choisissez. Rien n'est promis comme décision automatique.</p></div></div>
    </div>
    </div></section>
    <section class="tl-section"><div class="container">
    <div class="row g-4">
      <div class="col-lg-6">
        <h2 class="tl-h2">Ce à quoi nous nous engageons</h2>
        <ul>
          <li>Présélection avant toute présentation.</li>
          <li>Transparence sur les délais et la rareté du profil.</li>
          <li>Suivi d'intégration 30/60/90 jours.</li>
          <li>Garantie de remplacement sur les mandats permanents.</li>
          <li>L'IA accélère notre travail interne ; la qualification reste humaine.</li>
          <li>Un conseiller disponible des deux côtés : talents et entreprises, contactez-nous selon votre besoin.</li>
        </ul>
      </div>
      <div class="col-lg-6">
        <div class="tl-stats" style="grid-template-columns:1fr 1fr">
          <div class="tl-stat"><b>7 j</b><p>Première shortlist visée, mandat d'opérations</p></div>
          <div class="tl-stat"><b>Tous</b><p>Secteurs d'activité</p></div>
          <div class="tl-stat"><b>92 %</b><p>Encore en poste après 90 jours</p></div>
          <div class="tl-stat"><b>1 200+</b><p>Talents en réseau</p></div>
        </div>
      </div>
    </div>
    </div></section>
    """
    + human_section("fr")
    + sectors_cloud("fr"),
    actions='<a class="tl-btn" href="candidats.html" data-set-persona="talent">Pour les Talents</a><a class="tl-btn tl-btn-ghost" href="entreprises.html" data-set-persona="entreprise">Pour les Entreprises</a>'
)

# Services
services_cards = "".join(
    f'<a class="tl-card" href="{href}"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></a>'
    for href, chip, t, p in [
        ("recrutement-permanent.html", "Permanent", "Recrutement permanent", "Postes stables dans tous les secteurs. Honoraires au succès, garantie de remplacement. Talendus mène la recherche ; vous choisissez."),
        ("chasse-de-tetes.html", "Passif", "Chasse de têtes", "Nous approchons des personnes déjà en poste pour les profils rares. Vous ne parcourez pas une base : nous identifions et présentons."),
        ("recrutement-cadres.html", "Direction", "Recrutement de cadres", "Gestionnaires et dirigeants. Souvent confidentiel. Shortlist qualifiée, décision chez vous."),
        ("recrutement-industriel.html", "Exemple", "Recrutement industriel", "Un exemple parmi d'autres : production, maintenance, logistique. Talendus n'est pas limité à l'industrie."),
        ("recrutement-technique.html", "Métiers", "Métiers spécialisés", "Techniciens, soudeurs, développeurs, infirmiers, comptables, une grande variété de profils, tous secteurs."),
        ("recrutement-temporaire.html", "Urgent", "Recrutement urgent", "Quand un poste critique est découvert. Une shortlist filtrée, pas une avalanche de CV."),
        ("chasse-de-tetes.html", "Discret", "Mandats confidentiels", "Remplacements de cadres ou réorganisations menés sans bruit interne."),
        ("entreprises.html", "RH", "Accompagnement RH", "Descriptifs de poste, grilles salariales, entrevues conjointes et intégration, autour du mandat de placement."),
    ]
)
simple_page(
    "Services de recrutement | Agence de placement Talendus",
    "Recherche de talents, présélection, qualification, shortlist et placement. Talendus utilise déjà l'IA en interne pour accélérer l'analyse. L'entreprise décide. Tous secteurs.",
    "services.html", "Services", "Du besoin à la shortlist : un seul interlocuteur.",
    "Permanent, temporaire, chasse de têtes, cadres et métiers. Vous confiez le mandat. Nous faisons la recherche. Vous gardez le choix final.",
    f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-6">
          <h2 class="tl-h2">Pourquoi les entreprises nous mandatent</h2>
          <p class="tl-lead">Parce qu'un dossier de trop, c'est du temps perdu. Nous présentons peu de candidats. Chacun a déjà passé le filtre Talendus.</p>
          <ul>
            <li>Une shortlist qualifiée, pas un portail d'emplois déguisé.</li>
            <li>Un délai annoncé dès le brief, selon la rareté réelle du profil.</li>
            <li>Un conseiller qui comprend le poste, l'IA est déjà utilisée par Talendus, elle ne vous est pas remise comme un moteur de recherche.</li>
          </ul>
        </div>
        <div class="col-lg-6">
          <div class="tl-hero-media" style="height:340px;border-radius:18px;overflow:hidden">
            <img src="assets/img/all-images/industry/soudeur-atelier.jpg" alt="Recrutement de métiers spécialisés">
          </div>
        </div>
      </div>
    </div></section>
    ''' + placement_process_services_section("fr") + technology_section("fr") + ai_coming_soon("fr") + competitive_advantage_section("fr"),
    actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a>'
)

# Entreprises (URL canonique) + redirection Employeurs
EMPLOYERS_BODY = (
    page_hero(
        "Entreprises",
        "Vous recrutez ? Confiez-nous votre besoin.",
        "Talendus recherche, évalue et présélectionne les talents les plus pertinents. Nous utilisons déjà l'intelligence artificielle dans nos outils internes pour accélérer la recherche, l'analyse et la présélection. Vous étudiez une shortlist qualifiée et vous prenez la décision finale.",
        actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a><a class="tl-btn tl-btn-ghost" href="besoin-de-recrutement.html">Décrire mon besoin</a>',
        badges='<span class="tl-badge tl-badge-light">Agence de placement</span> <span class="tl-badge tl-badge-light">Tous secteurs</span>'
    )
    + problems_section("fr")
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-prose">
        <div class="tl-kicker">La solution Talendus</div>
        <h2 class="tl-h2">Nous faisons le travail de recherche pour vous.</h2>
        <p>Vous avez un poste à pourvoir. Au lieu de publier une annonce et de trier des dizaines (parfois des centaines) de candidatures, vous transmettez le besoin à Talendus. Nous comprenons le poste, nous recherchons les profils, nous analysons les parcours, nous présélectionnons, nous échangeons avec les candidats lorsque c'est nécessaire, nous évaluons, puis nous vous présentons une sélection qualifiée.</p>
        <p>Vous n'accédez pas à une base de CV. Vous ne « cherchez pas des talents » sur Talendus comme sur un logiciel ATS. Vous mandattez une agence. Talendus utilise déjà l'intelligence artificielle dans ses outils internes pour accélérer la recherche, l'analyse et la présélection des talents. Vous bénéficiez de cette puissance sans avoir à l'utiliser vous-même. La décision d'embauche reste la vôtre.</p>
      </div>
    </div></section>
    """
    + process_section("fr")
    + """
    <section class="tl-section"><div class="container">
      <div class="row g-4">
        <div class="col-lg-6">
          <h2 class="tl-h2">Recherche des talents</h2>
          <p>Nous mobilisons le réseau Talendus, les profils déjà connus, les candidatures reçues et, lorsque c'est utile, une offre cadrée. Les personnes déjà en poste peuvent être approchées discrètement. L'objectif n'est pas d'afficher le plus grand nombre d'annonces : c'est d'identifier les profils qui présentent le meilleur potentiel de correspondance avec votre besoin.</p>
        </div>
        <div class="col-lg-6">
          <h2 class="tl-h2">Présélection</h2>
          <p>Chaque profil identifié est analysé : compétences, expérience, qualifications, cohérence avec le poste et critères convenus avec vous. Ce qui ne tient pas n'arrive pas sur votre bureau. Vous ne devenez pas le premier filtre d'une pile de CV.</p>
        </div>
        <div class="col-lg-6">
          <h2 class="tl-h2">Entretiens</h2>
          <p>Lorsque c'est nécessaire, Talendus échange avec les candidats avant de vous les présenter : validation du parcours, motivations, adéquation. Vos entretiens, ensuite, portent sur des personnes déjà qualifiées. Vous organisez votre processus ; nous restons l'intermédiaire.</p>
        </div>
        <div class="col-lg-6">
          <h2 class="tl-h2">Shortlist</h2>
          <p>Nous ne transmettons pas une liste massive. Nous présentons une sélection de profils pertinents, chacun que nous sommes prêts à défendre. La pertinence est ce que nous vendons. Le volume, non.</p>
        </div>
      </div>
    </div></section>
    """
    + ai_engine_section("fr")
    + ai_screening_section("fr")
    + competitive_advantage_section("fr")
    + human_section("fr")
    + why_talendus_section("fr")
    + company_types_section("fr")
    + bad_hire_calculator_section("fr")
    + """
    <section class="tl-section tl-ice" id="temoignages"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Témoignages entreprises</div>
        <h2 class="tl-h2">Ce que disent les employeurs</h2>
      </div>
      <div class="tl-grid-3 tl-quotes">
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Ils ont compris le poste dès le premier appel. Les dossiers présentés correspondaient vraiment à ce qu'on cherchait.</p>
          <footer><strong>M.L.</strong><span>Directrice des opérations · Rive-Sud</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Pas une agence qui envoie 40 CV. Trois dossiers solides, un suivi après l'embauche.</p>
          <footer><strong>J.R.</strong><span>Directeur · Mauricie</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Mandat confidentiel mené sans bruit interne. Prise de poste calée sur notre calendrier.</p>
          <footer><strong>S.B.</strong><span>VP · Montérégie</span></footer>
        </blockquote>
      </div>
    </div></section>
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker" id="faq">FAQ entreprises</div>
        <h2 class="tl-h2">Ce que demandent les RH et les gestionnaires</h2>
      </div>
      """ + faq_html(FAQ_EMPLOYEURS) + """
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Confier mon recrutement</a>
      </div>
    </div></section>
    """
    + sectors_cloud("fr")
    + proof_stats("fr")
)
write("entreprises.html", wrap(
    "Entreprises | Agence de placement | Talendus",
    "Confiez un recrutement à Talendus. Nous utilisons déjà l'IA en interne pour accélérer la recherche, l'analyse et la présélection. Vous recevez une shortlist qualifiée et gardez la décision finale.",
    "entreprises.html",
    EMPLOYERS_BODY,
))
write("employeurs.html", wrap(
    "Employeurs | Recrutement pour toutes les entreprises | Talendus",
    "Redirection vers l’espace entreprises Talendus.",
    "employeurs.html",
    '<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="entreprises.html">Continuer vers Entreprises</a></p><script>location.replace("entreprises.html");</script></div></section>',
))

# Candidats
write("candidats.html", wrap(
    "Candidats | Rejoindre Talendus",
    "Créez votre profil chez Talendus. Nous étudions votre parcours et vous contactons lorsqu'une opportunité correspond. Gratuit. Tous secteurs.",
    "candidats.html",
    page_hero(
        "Candidats",
        "Créez votre profil. Talendus vous accompagne vers les opportunités qui collent.",
        "Vous n'êtes pas un CV dans une base. Un conseiller étudie votre parcours, peut vous contacter, vous évaluer, et vous présenter à une entreprise lorsque l'adéquation tient. C'est gratuit.",
        actions='<a class="tl-btn" href="candidats.html#cv">Créer mon profil</a><a class="tl-btn tl-btn-ghost" href="emplois.html">Voir les opportunités</a>',
        badges='<span class="tl-badge tl-badge-light">Sans frais pour vous</span> <span class="tl-badge tl-badge-light">Tous secteurs</span>'
    )
    + for_candidates_section("fr")
    + candidate_journey_section("fr")
    + """
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Créer votre profil</h2>
          <p class="tl-lead">Indiquez votre métier, vos compétences, vos préférences et votre région. Déposez votre CV. Un conseiller Talendus étudie le dossier et vous contacte si un mandat correspond. Vous n'êtes pas envoyé à l'aveugle chez quinze employeurs.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">En semaine, on répond en général en moins de 30 minutes.</div>
          <p id="processus"></p>
          <h3>Ce que Talendus fait ensuite</h3>
          <ol>
            <li>Analyse de votre profil et de votre CV.</li>
            <li>Considération pour les mandats pertinents, y compris non affichés.</li>
            <li>Échanges avec un conseiller, puis étapes de sélection si besoin.</li>
            <li>Présentation à une entreprise uniquement lorsque ça colle.</li>
          </ol>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post" data-form="talent-cv" enctype="multipart/form-data">
            <label>Nom</label><input required name="nom" autocomplete="name">
            <label>Courriel</label><input type="email" required name="courriel" autocomplete="email">
            <label>Téléphone</label><input name="tel" autocomplete="tel">
            <label>Métier visé</label>
            <select name="metier">""" + talent_trade_options("fr") + """</select>
            <label>Région</label><input name="region" placeholder="Laval, Montérégie, Québec, télétravail…">
            """ + cv_file_field("fr", required=True) + """
            <label>Lien vers votre CV <span class="tl-optional">(facultatif)</span></label><input name="cv" placeholder="https://">
            <button class="tl-btn tl-btn-lg" type="submit">Créer mon profil</button>
            <div class="tl-success" role="status"></div>
          </form>
        </div>
      </div>
    </div></section>
    """
    + trades_cloud("fr")
    + human_section("fr")
    + """
    <section class="tl-section" id="temoignages"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Témoignages candidats</div>
        <h2 class="tl-h2">Ce que disent les gens qu'on a placés</h2>
      </div>
      <div class="tl-grid-3 tl-quotes">
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Talendus m'a présenté un poste qui collait vraiment. Entrevue claire, conditions nettes.</p>
          <footer><strong>A.D.</strong><span>Candidate placée · Laval</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Pas quinze entrevues inutiles. Un conseiller a compris mon métier, puis m'a présenté une entreprise qui recrutait vraiment.</p>
          <footer><strong>K.T.</strong><span>Candidat placé · Drummondville</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>J'ai déposé mon CV un mardi. Vendredi, j'avais une entrevue. Sans frais, sans pression.</p>
          <footer><strong>R.M.</strong><span>Candidat · Montréal</span></footer>
        </blockquote>
      </div>
    </div></section>
    <section class="tl-section" id="faq"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">FAQ candidats</div>
        <h2 class="tl-h2">Avant de créer votre profil</h2>
      </div>
      """ + faq_html(FAQ_CANDIDATS) + """
    </div></section>
    """
))

# Contact
write("contact.html", wrap(
    "Contact | Confier un recrutement ou créer un profil | Talendus",
    "Contactez Talendus à Montréal. Confiez un besoin de recrutement ou créez votre profil. Appels sur rendez-vous. 514 555-0199 · info@talendus.ca",
    "contact.html",
    page_hero(
        "Contact",
        "Écrivez-nous. On vous rappelle.",
        "Cherchez-vous un emploi, ou avez-vous un poste à pourvoir ? Choisissez votre porte. Le formulaire s'ajuste.",
        actions='',
        badges='<span class="tl-badge tl-badge-light">Sur rendez-vous</span> <span class="tl-badge tl-badge-light">Lun–Ven, 8 h à 17 h</span>'
    )
    + """
    <section class="tl-section-sm"><div class="container">
      <div class="tl-info-grid">
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-phone"></i></div>
          <div>
            <h3>Téléphone</h3>
            <p><a href="tel:+15145550199">514 555-0199</a></p>
            <p>En semaine, on répond en général en moins de 30 minutes.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-regular fa-envelope"></i></div>
          <div>
            <h3>Courriel</h3>
            <p><a href="mailto:info@talendus.ca">info@talendus.ca</a></p>
            <p>Lun–Ven, 8 h à 17 h</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-brands fa-whatsapp"></i></div>
          <div>
            <h3>WhatsApp</h3>
            <p><a href="https://wa.me/15145550199?text=Bonjour%20Talendus%2C%20je%20souhaite%20discuter%20d%27un%20besoin%20de%20recrutement." target="_blank" rel="noopener noreferrer">Ouvrir une conversation</a></p>
            <p>Réponse durant les heures d’ouverture.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-calendar-check"></i></div>
          <div>
            <h3>Rencontres</h3>
            <p>Les appels se font sur rendez-vous.</p>
            <p>On s'ajuste à vos disponibilités.</p>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section" id="parcours"><div class="container">
      <div data-persona-only="gateway">
        <div class="tl-center" style="max-width:640px;margin:0 auto 28px">
          <div class="tl-kicker">Vous êtes</div>
          <h2 class="tl-h2">Choisissez votre porte</h2>
        </div>
        <div class="tl-persona-doors">
          <a class="tl-persona-door" href="#formulaire" data-set-persona="talent">
            <span class="tl-kicker">Talents</span>
            <h2>Je cherche un emploi</h2>
            <p>Déposez votre CV ou posez une question sur un poste. C'est gratuit.</p>
            <span class="tl-split-cta">Continuer →</span>
          </a>
          <a class="tl-persona-door" href="#formulaire" data-set-persona="entreprise">
            <span class="tl-kicker">Entreprises</span>
            <h2>Je recrute</h2>
            <p>Ouvrez un mandat : décrivez le poste, nous faisons la recherche.</p>
            <span class="tl-split-cta">Continuer →</span>
          </a>
        </div>
      </div>
      <div class="tl-contact-grid" id="formulaire" style="margin-top:36px">
        <div data-persona-only="talent">
          <div class="tl-kicker">Talents</div>
          <h2 class="tl-h2">Déposer mon CV ou poser une question</h2>
          <p class="tl-lead">C'est gratuit. Un conseiller vous rappelle si un mandat correspond.</p>
          <form class="tl-form" action="#" method="post" data-form="talent-cv" enctype="multipart/form-data">
            <input type="hidden" name="profil" value="Candidat, je cherche un poste">
            <label>Nom</label><input required name="nom" autocomplete="name">
            <label>Courriel</label><input type="email" required name="courriel" autocomplete="email">
            <label>Téléphone</label><input name="tel" autocomplete="tel">
            <label>Objet</label>
            <select name="objet">
              <option>Déposer mon CV</option>
              <option>Rejoindre la banque de talents</option>
              <option>Question sur une offre</option>
            </select>
            """ + cv_file_field("fr", required=False) + """
            <label>Lien vers votre CV <span class="tl-optional">(facultatif)</span></label><input name="cv" placeholder="https://">
            <label>Message</label><textarea name="message" placeholder="Métier, compétences, ville, type d'emploi"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Créer mon profil</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="entreprise">
          <div class="tl-kicker">Entreprises</div>
          <h2 class="tl-h2">Décrire mon besoin de recrutement</h2>
          <p class="tl-lead">Vous transmettez le poste. Talendus recherche et présélectionne. Appel gratuit, sur rendez-vous.</p>
          <form class="tl-form" action="#" method="post" data-form="hiring-need">
            <input type="hidden" name="profil" value="Employeur, je recrute">
            <label>Nom</label><input required name="nom">
            <label>Entreprise</label><input required name="entreprise">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Objet</label>
            <select name="objet">
              <option>Confier mon recrutement</option>
              <option>Décrire mon besoin</option>
              <option>Parler à Talendus</option>
            </select>
            """ + employer_need_fields("fr") + """
            <button class="tl-btn tl-btn-lg" type="submit">Confier mon recrutement</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="gateway"></div>
        <div>
          <div class="tl-map">
            <iframe title="Carte Montréal" src="https://maps.google.com/maps?q=Montréal%20Québec&t=&z=11&ie=UTF8&iwloc=&output=embed" loading="lazy"></iframe>
          </div>
        </div>
      </div>
    </div></section>
    """
))

# Emplois listing
cards = "".join(job_card_html(job, "fr") for job in JOBS)
write("emplois.html", wrap(
    "Offres d'emploi | Opportunités Talendus",
    "Postes accompagnés par Talendus dans tous les secteurs. Postulez : un conseiller étudie votre dossier et vous rappelle.",
    "emplois.html",
    jobs_listing_header("fr")
    + f"""
    <section class="tl-section tl-jobs-board"><div class="container">
      {job_search_filters("fr")}
      <div class="tl-jobs-grid" id="job-list">{cards}</div>
      {jobs_empty_state("fr")}
    </div></section>
    """
    + SPEED_TALENT
    + CTA_TALENT
))

for job in JOBS:
    slug, title, city, cat, typ, sal, shift, req, sector, skills, exp = job
    write(f"emploi-{slug}.html", wrap(
        f"{title} à {city} | Emploi | Talendus",
        f"Poste de {title} à {city}, Québec. {typ}. Postulez via Talendus : un conseiller présente votre dossier. Agence de placement, tous secteurs.",
        f"emploi-{slug}.html",
        job_detail_html(job, related_job_cards(JOBS, slug, "fr"), "fr"),
        extra_json_ld=job_ld(title, city, slug, typ, sal, req),
        og_type="article",
    ))

# Secteurs
sec_cards = "".join(
    f'<a class="tl-card" href="secteur-{s}.html"><div class="body"><h3>{n}</h3><p>{d}</p></div></a>'
    for s, n, t, d in SECTORS
)
write("secteurs.html", wrap(
    "Tous les secteurs | Agence de placement | Talendus",
    "Talendus recrute pour tous les secteurs et tous les types de métiers. Technologie, construction, santé, finance, industrie, commerce et bien plus.",
    "secteurs.html",
    page_hero(
        "Tous les secteurs", "Talendus recrute pour tous les secteurs et tous les types de métiers.",
        "Ces secteurs sont des exemples, pas une liste exclusive. PME, startups, grandes organisations : un accompagnement adapté à chaque besoin de recrutement.",
        actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a>'
    )
    + sectors_cloud("fr")
    + f'<section class="tl-section tl-ice"><div class="container"><div class="tl-center" style="max-width:720px;margin:0 auto 28px"><div class="tl-kicker">Exemples de pages</div><h2 class="tl-h2">Quelques verticales déjà documentées</h2><p class="tl-lead">D\'autres pages (construction, santé, finance, informatique…) viendront avec du contenu réel, pas des pages vides.</p></div><div class="tl-grid-3">{sec_cards}</div></div></section>'
    + trades_cloud("fr")
))
for slug, name, title, desc in SECTORS:
    write(f"secteur-{slug}.html", wrap(
        f"{title} | Talendus",
        desc,
        f"secteur-{slug}.html",
        page_hero(
            "Exemple de secteur", name, desc,
            actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a>'
        )
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} Ce n'est pas une spécialisation exclusive : Talendus recrute pour toutes les entreprises, dans tous les métiers.</p>
              <h2 class="tl-h2">Métiers typiques</h2>
              <p>Opération, métiers spécialisés, supervision, gestion, et d'autres profils selon votre besoin.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="contact.html">Confiez-nous votre recrutement</a>
                <a class="tl-btn tl-btn-ghost-dark" href="secteurs.html">Tous les secteurs</a>
              </div>
            </div>
            <div class="col-lg-5">
              <div class="tl-card"><div class="body">
                <span class="tl-chip orange">Tous secteurs</span>
                <h3>Un exemple, pas une limite</h3>
                <p>Un brief clair, une shortlist, un seul conseiller. Vous ne parcourez pas une base de CV.</p>
                <a class="tl-btn" href="contact.html" style="margin-top:16px">Confier mon recrutement</a>
              </div></div>
            </div>
          </div>
        </div></section>
        """
    ))

# Blog
art_cards = "".join(
    f'<a class="tl-card" href="article-{s}.html"><div class="tl-hero-media" style="height:180px"><img src="assets/img/all-images/industry/{img}" alt="{t}" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">{cat}</span><h3>{t}</h3><p>{lead}</p></div></a>'
    for s, t, cat, img, lead in ARTICLES
)
topics = "".join(f'<li style="margin-bottom:8px">{t}</li>' for t in TOPICS)
write("blog.html", wrap(
    "Blog recrutement, RH et carrières | Talendus",
    "Articles sur le recrutement : trouver les bons talents, réduire le roulement, clarifier un poste. Tous secteurs.",
    "blog.html",
    page_hero(
        "Blog", "Recrutement, RH et carrière.",
        "Des textes utiles pour les entreprises et les candidats. Le problème du recrutement, pas une industrie.",
        actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a>',
        badges=""
    )
    + f'<section class="tl-section"><div class="container"><div class="tl-grid-3" id="blog-list">{art_cards}</div><h2 class="tl-h2" style="margin-top:48px">Sujets à venir</h2><ul class="tl-muted">{topics}</ul></div></section>'
))
for slug, title, cat, img, lead in ARTICLES:
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": lead,
        "author": {"@type": "Organization", "name": "Talendus"},
        "publisher": {"@type": "Organization", "name": "Talendus", "url": "https://talendus.ca"},
        "mainEntityOfPage": f"https://talendus.ca/article-{slug}.html",
        "inLanguage": "fr-CA",
        "image": f"https://talendus.ca/assets/img/all-images/industry/{img}",
    }
    write(f"article-{slug}.html", wrap(
        f"{title} | Blog Talendus",
        lead,
        f"article-{slug}.html",
        page_hero(cat, title, lead, badges="")
        + f"""
        <section class="tl-section"><div class="container" style="max-width:800px">
          <img src="assets/img/all-images/industry/{img}" alt="{title}" style="width:100%;border-radius:16px;margin-bottom:24px" loading="lazy" decoding="async">
          <p class="tl-lead">{lead}</p>
          <h2>Ce que nous observons</h2>
          <p>Les entreprises n'embauchent pas toutes de la même façon. Les compétences, l'expérience, le type de contrat et la localisation pèsent autant que le CV. Un poste vacant trop longtemps coûte souvent plus cher qu'un mandat de recrutement bien cadré.</p>
          <h2>Pistes concrètes</h2>
          <ul>
            <li>Clarifier le poste, la rémunération réelle et les compétences avant d'approcher le marché.</li>
            <li>Évaluer le savoir-faire (démonstration, mises en situation) plutôt que les seuls diplômes.</li>
            <li>Prévoir l'accueil 30/60/90 jours : c'est là que se joue la rétention.</li>
          </ul>
          <h2>Comment Talendus intervient</h2>
          <p>Nous ciblons des profils selon le métier et les compétences, nous validons le fit et nous présentons peu de dossiers, chacun que nous sommes prêts à défendre. Talendus utilise déjà l'IA en interne pour analyser plus vite les informations et identifier des correspondances ; elle ne choisit pas à la place de l'entreprise. La qualification reste humaine.</p>
          <p><a href="secteurs.html">Tous les secteurs</a> · <a href="emplois.html">Offres d'emploi</a> · <a href="entreprises.html">Solutions entreprises</a></p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Confier mon recrutement</a>
            <a class="tl-btn tl-btn-ghost-dark" href="blog.html">Retour au blog</a>
          </div>
        </div></section>
        """,
        extra_json_ld=article_schema,
        og_type="article",
        og_image=f"assets/img/all-images/industry/{img}",
    ))

write("404.html", wrap(
    "Page introuvable | Talendus",
    "La page demandée n'existe pas. Retournez à l'accueil Talendus.",
    "404.html",
    page_hero("404", "Cette page n'existe pas.", "Le poste, lui, existe peut-être encore.",
              actions='<a class="tl-btn" href="index.html">Retour à l\'accueil</a><a class="tl-btn tl-btn-ghost" href="contact.html">Nous écrire</a>',
              badges="")
    + '<section class="tl-section"><div class="container"><p class="tl-lead">Vérifiez l\'URL ou reprenez depuis l\'accueil, les offres ou le formulaire de contact.</p></div></section>',
    robots="noindex,nofollow",
))
write("espace.html", wrap(
    "Mon espace candidat | Talendus",
    "Connectez-vous pour gérer votre profil, votre CV, vos candidatures et vos échanges avec Talendus.",
    "espace.html",
    """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account"></div></div></section>""",
    robots="noindex,nofollow",
))
write("espace-employeur.html", wrap(
    "Espace entreprise | Talendus",
    "Suivez les dossiers que Talendus vous présente, vos mandats et vos factures. Vous ne parcourez pas une base de candidats.",
    "espace-employeur.html",
    """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account" data-space="employer"></div></div></section>""",
    robots="noindex,nofollow",
))
write("confidentialite.html", wrap(
    "Politique de confidentialité | Talendus",
    "Politique de confidentialité et cookies de Talendus, talendus.ca.",
    "confidentialite.html",
    page_hero("Légal", "Politique de confidentialité", "Les CV et mandats sont traités de façon confidentielle.", badges="")
    + """<section class="tl-section"><div class="container" style="max-width:800px">
    <h2>Données de recrutement</h2>
    <p>Talendus collecte les informations nécessaires au recrutement (coordonnées, CV, description de poste). Elles ne sont pas vendues à des tiers. Elles sont utilisées uniquement pour évaluer des candidatures, ouvrir des mandats et communiquer avec vous.</p>
    <p>Vous pouvez demander l'accès, la correction ou la suppression en écrivant à info@talendus.ca. Les données sont conservées le temps nécessaire au recrutement et aux obligations légales applicables au Québec.</p>
    <h2>Cookies et mesure d'audience</h2>
    <p>Les cookies essentiels assurent le fonctionnement du site (connexion, sécurité, préférences de langue). Les cookies d'analyse (Google Analytics) et de marketing (Meta Pixel) ne sont chargés qu'<strong>après votre consentement</strong>. Vous pouvez accepter, refuser ou modifier ce choix à tout moment via le bandeau cookies ou en écrivant à info@talendus.ca.</p>
    <p>Aucun identifiant publicitaire n'est déposé tant que vous n'avez pas accepté les cookies non essentiels. Talendus ne revend pas vos données de navigation.</p>
    </div></section>"""
))
write("conditions.html", wrap(
    "Conditions d'utilisation | Talendus",
    "Conditions d'utilisation du site talendus.ca.",
    "conditions.html",
    page_hero("Légal", "Conditions d'utilisation", "Le site talendus.ca présente les services de Talendus.", badges="")
    + """<section class="tl-section"><div class="container" style="max-width:800px"><p>Le contenu est fourni à titre informatif. Les mandats font l'objet d'une entente écrite. Les exemples d'offres et statistiques de démonstration peuvent être ajustés selon les données réelles.</p><p>L'utilisation du site implique l'acceptation de ces conditions. Pour toute question : info@talendus.ca.</p></div></section>"""
))

simple_page(
    "Comment ça fonctionne | Parcours talent Talendus",
    "Créez votre profil, déposez votre CV, soyez considéré pour des opportunités. Talendus présente votre dossier. Gratuit pour les talents.",
    "comment-ca-fonctionne.html",
    "Talents",
    "Du profil à une présentation éventuelle, un conseiller reste avec vous.",
    "Créez votre espace, déposez votre CV, postulez aux offres si vous le souhaitez. Nous étudions votre parcours, vous rappelons quand un mandat colle, et avançons avec vous. Appelez-nous ou écrivez-nous dès que vous voulez qu'on s'en occupe.",
    candidate_journey_section("fr"),
    actions='<a class="tl-btn" href="espace.html" data-auth-open="register">Créer mon profil</a>',
)

simple_page(
    "Vous recrutez ? Confiez-nous votre besoin | Talendus",
    "Agence de placement : décrivez votre besoin de recrutement. Talendus analyse, définit le profil, recherche, présélectionne et vous présente les meilleurs candidats. Vous prenez la décision finale.",
    "besoin-de-recrutement.html",
    "Entreprises",
    "Vous recrutez ? Confiez-nous votre besoin.",
    "Décrivez-nous le profil que vous recherchez. Notre équipe analyse votre besoin, définit les critères de recherche et prend en charge le processus de recrutement afin de vous présenter les candidats les plus pertinents.",
    process_section("fr")
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-prose">
        <h2 class="tl-h2">Un service de recrutement, pas une publication d'offre</h2>
        <p>Avec Talendus, vous ne vous contentez pas de publier une offre et d'attendre des candidatures. Vous nous confiez votre besoin et nous prenons en charge la recherche et la présélection des talents.</p>
        <p>Vous n'avez pas besoin de passer des heures à publier, trier et analyser des centaines de candidatures. Talendus prend en charge le processus pour vous. Grâce à nos équipes, nos méthodes et nos outils technologiques intégrant l'intelligence artificielle, nous accélérons la recherche et la qualification des talents.</p>
        <p>Vous nous confiez la recherche. Nous nous chargeons du travail de sourcing, de présélection et de qualification afin que vous puissiez vous concentrer sur votre décision finale. Nous ne vous transmettons pas simplement des candidatures. Nous vous présentons une sélection de profils que nous avons déjà recherchés et qualifiés en fonction de votre besoin.</p>
      </div>
    </div></section>
    """
    + hiring_need_form_section("fr")
    + human_hire_band("fr"),
    actions='<a class="tl-btn" href="#besoin">Décrire mon besoin</a><a class="tl-btn tl-btn-ghost" href="espace-employeur.html" data-auth-open="register">Ouvrir un espace entreprise</a>',
)

simple_page(
    "Solutions RH | Accompagnement recrutement Talendus",
    "Structurer le recrutement : descriptifs, grilles salariales, entrevues conjointes et intégration 30/60/90. Tous secteurs.",
    "solutions-rh.html",
    "Entreprises",
    "Structurer le recrutement, pas seulement combler un trou.",
    "Descriptions de poste, grilles salariales, entrevues conjointes et suivi d'intégration, pour les entreprises qui veulent arrêter d'improviser.",
    """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Descriptifs de poste</h3><p>Un poste écrit comme il se vit : responsabilités, compétences, type de contrat.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Grilles salariales</h3><p>Aligner l'offre sur le marché, sans sous-payer un métier rare.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Intégration 30/60/90</h3><p>Suivi après la prise de poste. Garantie de remplacement sur les mandats permanents.</p></div></div>
      </div>
    </div></section>
    """,
    actions='<a class="tl-btn" href="contact.html">Confier mon recrutement</a>',
)

for old, new in [("about.html", "a-propos.html"), ("service.html", "services.html"), ("blog-single.html", "blog.html"), ("publier-une-offre.html", "besoin-de-recrutement.html")]:
    write(old, wrap("Redirection | Talendus", "Redirection.", old,
                    f'<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="{new}">Continuer</a></p><script>location.replace("{new}");</script></div></section>',
                    robots="noindex,nofollow"))

write("app.html", wrap(
    "Télécharger Talendus | Android et iPhone",
    "Mettez Talendus sur votre téléphone. Offres, messages et votre conseiller, en un tap — comme vos autres applis.",
    "app.html",
    page_hero(
        "Sur votre téléphone",
        "Talendus dans votre poche.",
        "Téléchargez l'application une fois. Ensuite, elle s'ouvre comme vos autres applis — offres, messages et votre conseiller compris.",
        actions='<a class="tl-btn" href="#tl-install-board">Télécharger l\'appli</a><a class="tl-btn tl-btn-ghost" href="espace.html">Ouvrir mon espace</a>',
        badges='<span class="tl-badge tl-badge-light">Android</span> <span class="tl-badge tl-badge-light">iPhone</span>'
    )
    + install_board("fr")
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-app-grid">
        <article class="tl-app-card">
          <h3>Candidats</h3>
          <p>Profil, CV, candidatures et messages avec votre conseiller. Il vous rappelle pour un vrai mandat. Écrivez-nous dès que vous voulez avancer.</p>
          <p><a class="tl-btn" href="espace.html">Ouvrir mon espace</a></p>
        </article>
        <article class="tl-app-card">
          <h3>Entreprises</h3>
          <p>Mandats, profils présentés, contrats à signer et factures. Un conseiller prend votre recrutement : décrivez le poste, on vous rappelle.</p>
          <p><a class="tl-btn" href="espace-employeur.html">Espace employeur</a></p>
        </article>
      </div>
    </div></section>
    """
))

write("m.html", native_app_page("fr"))

write_seo_fr(write, wrap, page_hero, CTA_HIRE)
build_en(write, wrap, page_hero)

fr_urls = [("", "en/")]
pairs = [
    ("a-propos.html", "en/about.html"),
    ("services.html", "en/services.html"),
    ("entreprises.html", "en/employers.html"),
    ("candidats.html", "en/candidates.html"),
    ("emplois.html", "en/jobs.html"),
    ("comment-ca-fonctionne.html", "en/how-it-works.html"),
    ("besoin-de-recrutement.html", "en/hiring-need.html"),
    ("solutions-rh.html", "en/hr-solutions.html"),
    ("secteurs.html", "en/sectors.html"),
    ("blog.html", "en/blog.html"),
    ("contact.html", "en/contact.html"),
    ("confidentialite.html", "en/privacy.html"),
    ("conditions.html", "en/terms.html"),
    ("app.html", "en/app.html"),
    ("recrutement-industriel.html", "en/industrial-recruiting.html"),
    ("recrutement-manufacturier.html", "en/manufacturing-recruiting.html"),
    ("recrutement-technique.html", "en/technical-recruiting.html"),
    ("recrutement-permanent.html", "en/permanent-recruiting.html"),
    ("recrutement-temporaire.html", "en/temporary-recruiting.html"),
    ("chasse-de-tetes.html", "en/executive-search.html"),
    ("recrutement-cadres.html", "en/leadership-recruiting.html"),
    ("recrutement-industriel-montreal.html", "en/industrial-recruiting-montreal.html"),
    ("recrutement-industriel-laval.html", "en/industrial-recruiting-laval.html"),
    ("recrutement-industriel-longueuil.html", "en/industrial-recruiting-longueuil.html"),
    ("recrutement-industriel-quebec.html", "en/industrial-recruiting-quebec.html"),
]
pairs += [(f"emploi-{s}.html", f"en/job-{s}.html") for s, *_ in JOBS]
pairs += [(f"secteur-{s}.html", f"en/sector-{s}.html") for s, *_ in SECTORS]
pairs += [(f"article-{s}.html", f"en/article-{s}.html") for s, *_ in ARTICLES]
fr_urls += pairs

def sitemap_url(fr, en):
    loc_fr = f"https://talendus.ca/{fr}" if fr else "https://talendus.ca/"
    loc_en = f"https://talendus.ca/{en}" if en else "https://talendus.ca/en/"
    return f"""  <url>
    <loc>{loc_fr}</loc>
    <xhtml:link rel="alternate" hreflang="fr-CA" href="{loc_fr}"/>
    <xhtml:link rel="alternate" hreflang="en-CA" href="{loc_en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{loc_fr}"/>
  </url>
  <url>
    <loc>{loc_en}</loc>
    <xhtml:link rel="alternate" hreflang="fr-CA" href="{loc_fr}"/>
    <xhtml:link rel="alternate" hreflang="en-CA" href="{loc_en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{loc_fr}"/>
  </url>"""

(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(sitemap_url(fr, en) for fr, en in fr_urls)
    + "\n</urlset>\n",
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\nDisallow: /espace.html\nDisallow: /espace-employeur.html\nDisallow: /en/account.html\nDisallow: /en/account-employer.html\nDisallow: /candidate\nDisallow: /employer\nDisallow: /en/candidate\nDisallow: /en/employer\nDisallow: /m.html\nDisallow: /en/m.html\nDisallow: /index1.html\nDisallow: /index2.html\nDisallow: /index3.html\nDisallow: /index4.html\nDisallow: /index5.html\nDisallow: /index6.html\nDisallow: /index7.html\nDisallow: /index8.html\nDisallow: /index9.html\nDisallow: /index10.html\nDisallow: /projects.html\nDisallow: /team.html\nDisallow: /testimonial.html\nSitemap: https://talendus.ca/sitemap.xml\n",
    encoding="utf-8",
)
print("done")
