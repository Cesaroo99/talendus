#!/usr/bin/env python3
"""Génère les pages piliers Talendus à partir du header/footer partagés."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parts import (
    wrap as wrap_page, page_hero, speed_strip, cta_band, faq_html, proof_stats,
    FAQ_EMPLOYEURS, FAQ_CANDIDATS,
)
from positioning import (
    homepage_after_hero, job_search_filters, employer_need_fields,
    talent_trade_options, sectors_cloud, trades_cloud, ai_coming_soon,
    human_hire_band,
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
        "publier-une-offre.html": "en/post-a-job.html",
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
    ("entrepot", "Entrepôt", "Recrutement entrepôt Québec", "Caristes, préparateurs, commis et superviseurs d'entrepôt — un exemple de profils logistiques."),
    ("logistique", "Logistique", "Recrutement logistique Québec", "Planification, transport, WMS et coordination. La logistique est un secteur parmi d'autres."),
    ("distribution", "Distribution", "Recrutement distribution Québec", "Centres de distribution, expédition, réception et gestion des stocks."),
    ("transport", "Transport", "Recrutement transport et logistique", "Chauffeurs, coordination transport et flux. Talendus accompagne aussi d'autres industries."),
    ("transformation-alimentaire", "Transformation alimentaire", "Recrutement alimentaire Québec", "Production alimentaire : hygiène, opérateurs et supervision. Un exemple, pas une spécialisation exclusive."),
    ("metallurgie", "Métallurgie", "Recrutement métallurgie et soudure Québec", "Soudure, usinage, fabrication métallique. D'autres métiers et secteurs sont tout autant concernés."),
    ("plasturgie", "Plasturgie", "Recrutement plasturgie Québec", "Injection, extrusion, set-up et techniciens de procédé."),
    ("maintenance", "Maintenance", "Recrutement maintenance Québec", "Techniciens, mécaniciens et responsables fiabilité — parmi une grande variété de métiers."),
]

ARTICLES = [
    ("mauvaise-embauche", "Combien coûte une mauvaise embauche ?", "RH", "usine-equipe.jpg",
     "Un mauvais fit ne se limite pas au salaire. Entre formation, heures supplémentaires, perte de productivité et roulement, la facture grimpe vite — dans n'importe quel secteur."),
    ("machiniste-cnc", "Recruter un machiniste CNC au Québec en 2026", "Métiers", "cnc-machiniste.jpg",
     "Le machiniste CNC reste un profil tendu. Voici comment attirer, évaluer et retenir ce talent — un exemple parmi beaucoup d'autres métiers."),
    ("caristes-entrepot", "Pénurie de caristes : stratégies pour les entrepôts", "Logistique", "entrepot-logistique.jpg",
     "Les centres de distribution se disputent les caristes expérimentés. Trois leviers concrets, transposables à d'autres métiers rares."),
    ("superviseur-production", "Superviseur de production : le profil qui change une équipe", "Production", "usine-equipe.jpg",
     "Un bon superviseur stabilise la qualité et le climat. Voici le portrait que nous validons — applicable à d'autres rôles de gestion."),
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
                <h5>Talendus. La plateforme de recrutement intelligente pour toutes les entreprises.</h5>
                <div class="space16"></div>
                <h1>Recrutez mieux, plus vite et plus intelligemment.</h1>
                <div class="space16"></div>
                <p>Vous cherchez un emploi, ou vous recrutez ? Talendus accompagne les candidats et les entreprises de toutes tailles, des PME aux plus grandes organisations, dans tous les secteurs.</p>
                <p>Du premier besoin de recrutement à l'identification des meilleurs candidats, Talendus simplifie votre processus de recrutement.</p>
            </div>
            <div class="tl-persona-cards">
              <a class="tl-persona-card is-talent" href="candidats.html" data-set-persona="talent">
                <span class="tl-kicker">Candidats</span>
                <h2>Je cherche un emploi</h2>
                <p>Parcourez les offres, créez votre profil, suivez vos candidatures. C'est gratuit. Un conseiller présente votre dossier aux employeurs.</p>
                <span class="tl-persona-go">Trouver un emploi <i class="fa-solid fa-arrow-right"></i></span>
              </a>
              <a class="tl-persona-card is-hire" href="entreprises.html" data-set-persona="entreprise">
                <span class="tl-kicker">Entreprises</span>
                <h2>Je recrute</h2>
                <p>On vous présente les bons talents, dans les meilleurs délais. Une shortlist claire, pas une pile de CV à trier.</p>
                <span class="tl-persona-go">Trouver des talents <i class="fa-solid fa-arrow-right"></i></span>
              </a>
            </div>
        </div>
  </div>
</div>
"""

write("index.html", wrap(
    "Talendus | Plateforme de recrutement pour toutes les entreprises",
    "Talendus est la plateforme de recrutement intelligente pour toutes les entreprises, des PME aux plus grandes organisations. Recrutez mieux, plus vite et plus intelligemment. Tous secteurs.",
    "",
    INDEX_BODY + homepage_after_hero("fr"),
    solid=False,
))


def simple_page(title, desc, slug, kicker, h1, lead, inner, actions=""):
    body = page_hero(kicker, h1, lead, actions) + inner
    write(slug, wrap(title, desc, slug, body))


# À propos
simple_page(
    "À propos de Talendus | Plateforme de recrutement pour toutes les entreprises",
    "Talendus aide les entreprises de tous secteurs à recruter les bons talents. Histoire, mission et façon de travailler.",
    "a-propos.html", "Le cabinet", "Talendus est une plateforme de recrutement pour les entreprises.",
    "Nous aidons les entreprises de tous secteurs à recruter les bons talents. L'industrie, le métier et la localisation sont des paramètres — jamais des limites.",
    """
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <h2 class="tl-h2">Pourquoi on existe</h2>
    <p class="tl-lead">Trop d'entreprises perdent des semaines à chercher les bons candidats, à trier trop de CV, ou à faire durer un processus trop long. On a bâti une plateforme qui simplifie le recrutement — pour toutes les entreprises, pas pour une industrie.</p>
    <h2 class="tl-h2">Ce qu'on fait</h2>
    <p>On connecte les employeurs aux talents dont ils ont besoin : développeurs, comptables, soudeurs, infirmiers, chauffeurs, responsables RH, et bien d'autres. Un conseiller présente les dossiers. Candidats et employeurs restent chacun de leur côté.</p>
    <h2 class="tl-h2">Où on va</h2>
    <p>Recruter mieux, plus vite et plus intelligemment grâce à l'IA. Le matching, l'analyse de CV et le classement des candidats arriveront. Ils ne sont pas simulés aujourd'hui.</p>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe au travail">
      </div>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">Comment on travaille</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Tous les secteurs</h3><p>Talendus s'adresse à toutes les industries. Le secteur est un filtre de recherche, pas le positionnement de la marque.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Rigueur</h3><p>On évalue le métier, les compétences, l'expérience et le fit. Pas une avalanche de CV.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Parole tenue</h3><p>Délais, dossiers, garantie : ce qui est dit est livré. Un seul conseiller jusqu'à l'entrée en poste.</p></div></div>
    </div>
    </div></section>
    <section class="tl-section"><div class="container">
    <div class="row g-4">
      <div class="col-lg-6">
        <h2 class="tl-h2">Ce à quoi on s'engage</h2>
        <ul>
          <li>Présélection avant toute présentation.</li>
          <li>Transparence sur les délais et la rareté du profil.</li>
          <li>Suivi d'intégration 30/60/90 jours.</li>
          <li>Garantie de remplacement sur les mandats permanents.</li>
          <li>Pas de fausses fonctionnalités IA tant qu'elles ne sont pas développées.</li>
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
    + sectors_cloud("fr"),
    actions='<a class="tl-btn" href="candidats.html" data-set-persona="talent">Pour les Talents</a><a class="tl-btn tl-btn-ghost" href="entreprises.html" data-set-persona="entreprise">Pour les Entreprises</a>'
)

# Services
services_cards = "".join(
    f'<a class="tl-card" href="{href}"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></a>'
    for href, chip, t, p in [
        ("recrutement-permanent.html", "Permanent", "Recrutement permanent", "Postes stables dans tous les secteurs. Honoraires au succès, garantie de remplacement."),
        ("chasse-de-tetes.html", "Passif", "Chasse de têtes", "On approche des gens déjà en poste pour les profils rares, quel que soit le secteur."),
        ("recrutement-cadres.html", "Direction", "Recrutement de cadres", "Gestionnaires et dirigeants. Souvent confidentiel."),
        ("recrutement-industriel.html", "Exemple", "Recrutement industriel", "Un exemple parmi d'autres : production, maintenance, logistique. Talendus n'est pas limité à l'industrie."),
        ("recrutement-technique.html", "Métiers", "Métiers spécialisés", "Techniciens, soudeurs, développeurs, infirmiers, comptables — une grande variété de profils."),
        ("recrutement-temporaire.html", "Urgent", "Recrutement urgent", "Quand un poste critique est découvert. Une shortlist filtrée, pas une avalanche de CV."),
        ("chasse-de-tetes.html", "Discret", "Mandats confidentiels", "Remplacements de cadres ou réorganisations menés sans bruit interne."),
        ("entreprises.html", "RH", "Accompagnement RH", "Descriptifs de poste, grilles salariales, entrevues conjointes et intégration."),
    ]
)
simple_page(
    "Services de recrutement | Talendus",
    "Recrutement permanent, chasse de têtes, cadres et métiers spécialisés pour les entreprises de tous secteurs.",
    "services.html", "Services", "Du premier besoin à l'embauche : un seul interlocuteur.",
    "Permanent, temporaire, chasse de têtes, cadres et métiers. Pour toutes les entreprises, pas pour une industrie.",
    f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-6">
          <h2 class="tl-h2">Pourquoi les entreprises nous mandatent</h2>
          <p class="tl-lead">Parce qu'un dossier de trop, c'est du temps perdu. On présente peu de candidats. Chacun a déjà passé le filtre.</p>
          <ul>
            <li>Une shortlist, pas un portail d'emplois déguisé.</li>
            <li>Un délai annoncé dès le brief, selon la rareté réelle du profil.</li>
            <li>Un conseiller qui comprend le poste, pas seulement le secteur.</li>
          </ul>
        </div>
        <div class="col-lg-6">
          <div class="tl-hero-media" style="height:340px;border-radius:18px;overflow:hidden">
            <img src="assets/img/all-images/industry/soudeur-atelier.jpg" alt="Recrutement de métiers spécialisés">
          </div>
        </div>
      </div>
    </div></section>
    ''' + ai_coming_soon("fr"),
    actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a>'
)

# Entreprises (URL canonique) + redirection Employeurs
EMPLOYERS_BODY = (
    page_hero(
        "Entreprises",
        "Trouvez les talents dont votre entreprise a besoin.",
        "Publiez une offre, décrivez un besoin, ou parlez à un recruteur. Quel que soit votre secteur.",
        actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a><a class="tl-btn tl-btn-ghost" href="publier-une-offre.html">Publier une offre</a>',
        badges='<span class="tl-badge tl-badge-light">Appel sur rendez-vous</span> <span class="tl-badge tl-badge-light">Tous secteurs</span>'
    )
    + proof_stats("fr")
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Positionnement</span><h3>Pourquoi Talendus</h3><p>Nous aidons les entreprises de tous secteurs à recruter les bons talents. Pas une agence coincée dans une industrie.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Délai</span><h3>Délais tenus</h3><p>Premiers dossiers visés en 7 jours sur un métier d'opérations. 3 à 8 semaines pour les profils rares et les cadres. On l'annonce dès le brief.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Confiance</span><h3>Garanties</h3><p>Remplacement inclus sur les mandats permanents. Conditions confirmées à l'ouverture. Un seul conseiller jusqu'à l'entrée en poste.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Comment ça se passe</div>
        <h2 class="tl-h2">De l'appel au premier dossier</h2>
      </div>
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Appel</h3><p>30 minutes pour comprendre le poste, le secteur, le volume et l'urgence.</p></div>
        <div class="tl-step"><span>02</span><h3>Ciblage</h3><p>On active le réseau selon le métier, les compétences et la localisation.</p></div>
        <div class="tl-step"><span>03</span><h3>Filtre</h3><p>Entrevue Talendus avant que votre équipe perde une heure.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>Premiers dossiers visés en 7 jours. Comparables, avec une recommandation claire.</p></div>
        <div class="tl-step"><span>05</span><h3>Suivi</h3><p>Intégration 30/60/90 et garantie de remplacement.</p></div>
      </div>
    </div></section>
    <section class="tl-section" id="calculateur"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-5"><h2 class="tl-h2">Combien coûte une mauvaise embauche</h2>
        <p class="tl-lead">Estimez l'impact d'un mauvais fit : salaire, formation, heures sup. et perte de productivité. Un mandat Talendus coûte presque toujours moins cher qu'un poste vacant trop longtemps.</p></div>
        <div class="col-lg-6 offset-lg-1">
          <div class="tl-calc">
            <label for="tl-salary">Salaire annuel du poste ($)</label>
            <input id="tl-salary" type="number" value="55000" min="0">
            <label for="tl-months">Mois avant que le problème soit visible</label>
            <input id="tl-months" type="number" value="4" min="1">
            <div class="tl-calc-result">Coût estimé<br><b id="tl-cost">—</b></div>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Ce que vous pouvez faire ici</div>
        <h2 class="tl-h2">Recruter, publier, chasser, accompagner</h2>
      </div>
      <div class="tl-grid-4">
        <a class="tl-card" href="contact.html"><div class="body"><span class="tl-chip orange">Recruteur</span><h3>Parler à un recruteur</h3><p>Confiez-nous votre recrutement. Secteur, poste, volume, localisation.</p></div></a>
        <a class="tl-card" href="publier-une-offre.html"><div class="body"><span class="tl-chip orange">Mandat</span><h3>Publier une offre</h3><p>Décrivez le poste, le contrat et l'urgence. On ouvre le sourcing.</p></div></a>
        <a class="tl-card" href="chasse-de-tetes.html"><div class="body"><span class="tl-chip orange">Passif</span><h3>Trouver des talents</h3><p>Approche discrète des gens déjà en poste, tous secteurs.</p></div></a>
        <a class="tl-card" href="solutions-rh.html"><div class="body"><span class="tl-chip orange">RH</span><h3>Solutions RH</h3><p>Descriptifs, grilles salariales, entrevues conjointes et intégration 30/60/90.</p></div></a>
      </div>
    </div></section>
    """
    + sectors_cloud("fr")
    + ai_coming_soon("fr")
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
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker" id="faq">FAQ entreprises</div>
        <h2 class="tl-h2">Ce que demandent les RH et les gestionnaires</h2>
      </div>
      """ + faq_html(FAQ_EMPLOYEURS) + """
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Décrire mon besoin de recrutement</a>
      </div>
    </div></section>
    """
)
write("entreprises.html", wrap(
    "Entreprises | Recrutement pour toutes les entreprises — Talendus",
    "Confiez un recrutement à Talendus. Publiez une offre, trouvez des talents ou parlez à un recruteur. Tous secteurs.",
    "entreprises.html",
    EMPLOYERS_BODY,
))
write("employeurs.html", wrap(
    "Employeurs | Recrutement pour toutes les entreprises — Talendus",
    "Redirection vers l’espace entreprises Talendus.",
    "employeurs.html",
    '<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="entreprises.html">Continuer vers Entreprises</a></p><script>location.replace("entreprises.html");</script></div></section>',
))

# Candidats
write("candidats.html", wrap(
    "Candidats | Trouver un emploi au Québec — Talendus",
    "Créez votre profil chez Talendus. Offres dans tous les secteurs : technologie, santé, finance, manufacturier, commerce et plus.",
    "candidats.html",
    page_hero(
        "Candidats",
        "Trouvez un emploi sans enchaîner les entrevues pour rien.",
        "Créez votre profil. Un conseiller vous rappelle si un mandat colle. Vous n'êtes pas envoyé à l'aveugle chez quinze employeurs.",
        actions='<a class="tl-btn" href="candidats.html#cv">Créer mon profil</a><a class="tl-btn tl-btn-ghost" href="emplois.html">Découvrir les offres</a>',
        badges='<span class="tl-badge tl-badge-light">Sans frais pour vous</span> <span class="tl-badge tl-badge-light">Tous secteurs</span>'
    )
    + """
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Créer votre profil</h2>
          <p class="tl-lead">Indiquez votre métier, vos compétences et votre région. Un conseiller vous rappelle si un mandat colle. On ne vous envoie pas sur quinze entrevues pour rien.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">En semaine, on répond en général en moins de 30 minutes.</div>
          <p id="processus"></p>
          <h3>Comment ça se passe</h3>
          <ol>
            <li>Créez votre profil.</li>
            <li>Postulez aux offres ou déposez votre CV.</li>
            <li>Suivez vos candidatures avec un conseiller Talendus.</li>
            <li>On vous contacte quand le poste et le salaire correspondent.</li>
          </ol>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Nom</label><input required name="nom">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Métier visé</label>
            <select name="metier">""" + talent_trade_options("fr") + """</select>
            <label>Région</label><input name="region" placeholder="Laval, Montérégie, Québec, télétravail…">
            <label>Lien vers votre CV (Drive, Dropbox...)</label><input name="cv" placeholder="https://">
            <button class="tl-btn tl-btn-lg" type="submit">Créer mon profil</button>
            <div class="tl-success" role="status"></div>
          </form>
        </div>
      </div>
    </div></section>
    """
    + trades_cloud("fr")
    + """
    <section class="tl-section tl-ice"><div class="container">
      <h2 class="tl-h2">Conseils carrière</h2>
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Préparer une entrevue</h3><p>Exemples concrets, compétences, travail d'équipe : ce que les gestionnaires écoutent vraiment.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Mettre en valeur vos compétences</h3><p>Python, Excel, soudure, conduite : listez-les en tête de CV. C'est souvent le premier filtre.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Voir les offres</h3><p><a href="emplois.html">Consultez les postes ouverts</a> ou laissez-nous vous approcher pour un mandat confidentiel.</p></div></div>
      </div>
    </div></section>
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
    "Contact | Parler à un recruteur — Talendus",
    "Contactez Talendus à Montréal. Décrivez un besoin de recrutement ou créez votre profil. Appels sur rendez-vous. 514 555-0199 · info@talendus.ca",
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
            <p>Ouvrez un mandat, publiez une offre ou réservez un appel.</p>
            <span class="tl-split-cta">Continuer →</span>
          </a>
        </div>
      </div>
      <div class="tl-contact-grid" id="formulaire" style="margin-top:36px">
        <div data-persona-only="talent">
          <div class="tl-kicker">Talents</div>
          <h2 class="tl-h2">Déposer mon CV ou poser une question</h2>
          <p class="tl-lead">C'est gratuit. Un conseiller vous rappelle si un mandat correspond.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <input type="hidden" name="profil" value="Candidat — je cherche un poste">
            <label>Nom</label><input required name="nom">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Objet</label>
            <select name="objet">
              <option>Déposer mon CV</option>
              <option>Rejoindre la banque de talents</option>
              <option>Question sur une offre</option>
            </select>
            <label>Message</label><textarea required name="message" placeholder="Métier, compétences, ville, type d'emploi"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Créer mon profil</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="entreprise">
          <div class="tl-kicker">Entreprises</div>
          <h2 class="tl-h2">Décrire mon besoin de recrutement</h2>
          <p class="tl-lead">Secteur, poste, volume, localisation, type de contrat. Appel gratuit, sur rendez-vous.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <input type="hidden" name="profil" value="Employeur — je recrute">
            <label>Nom</label><input required name="nom">
            <label>Entreprise</label><input required name="entreprise">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Objet</label>
            <select name="objet">
              <option>Parler à un recruteur</option>
              <option>Publier une offre</option>
              <option>Décrire mon besoin de recrutement</option>
            </select>
            """ + employer_need_fields("fr") + """
            <button class="tl-btn tl-btn-lg" type="submit">Confiez-nous votre recrutement</button>
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
cards = []
for slug, title, city, cat, typ, sal, shift, req, sector, skills, exp in JOBS:
    cards.append(f'''
    <article class="tl-job-card" data-job="{title} {city} {cat} {typ} {sal} {shift} {sector} {skills} {exp}" data-city="{city}" data-cat="{cat}" data-type="{typ}" data-shift="{shift}" data-salary="{sal}" data-sector="{sector}" data-skills="{skills}" data-exp="{exp}">
      <div class="body">
        <span class="tl-chip orange">{typ}</span><span class="tl-chip">{city}</span>
        <h3><a href="emploi-{slug}.html">{title}</a></h3>
        <p>{sal} · {shift}</p>
        <a class="tl-split-cta" href="emploi-{slug}.html" style="color:var(--tl-orange);margin-top:auto;padding-top:14px">Voir le poste →</a>
      </div>
    </article>''')
write("emplois.html", wrap(
    "Offres d'emploi | Talendus",
    "Postes ouverts dans tous les secteurs : développeur, comptable, soudeur, infirmier, chauffeur, cariste et plus. Filtrez par secteur, métier, compétences, expérience et localisation.",
    "emplois.html",
    page_hero(
        "Offres d'emploi", "Découvrez les offres. Tous secteurs, tous métiers.",
        "Filtrez par secteur, métier, compétences, expérience, localisation et type d'emploi, puis postulez. Un conseiller Talendus présente votre dossier à l'employeur.",
        actions='<a class="tl-btn" href="candidats.html#cv">Créer mon profil</a>',
        badges='<span class="tl-badge tl-badge-light">Banque de talents</span>'
    )
    + f"""
    <section class="tl-section"><div class="container">
      {job_search_filters("fr")}
      <div class="tl-grid-3" id="job-list">{''.join(cards)}</div>
      <p class="tl-muted" id="job-empty" hidden>Aucun poste ne correspond à ces filtres. Créez votre profil : on vous contacte quand un mandat colle.</p>
    </div></section>
    """
))

for slug, title, city, cat, typ, sal, shift, req, sector, skills, exp in JOBS:
    write(f"emploi-{slug}.html", wrap(
        f"{title} à {city} | Emploi — Talendus",
        f"Poste de {title} à {city}, Québec. {typ}. Postulez via Talendus, plateforme de recrutement pour toutes les entreprises.",
        f"emploi-{slug}.html",
        page_hero(
            f"{city} · {typ}", title, f"{sal} · {shift} · Recrutement Talendus",
            actions='<a class="tl-btn" href="#postuler">Postuler</a>',
            badges='<span class="tl-badge tl-badge-light">Offre Talendus</span>'
        )
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <h2 class="tl-h2">Le poste</h2>
              <p class="tl-lead">Talendus recrute un(e) {title.lower()} pour un employeur à {city}. Secteur : {sector}. Compétences : {skills}.</p>
              <h3>Profil recherché</h3>
              <p>{req}</p>
              <h3>Ce que nous offrons</h3>
              <ul><li>Poste {typ.lower()}</li><li>Rémunération : {sal}</li><li>Horaire : {shift}</li><li>Accompagnement Talendus jusqu'à l'embauche</li></ul>
              <p><a href="emplois.html">← Toutes les offres</a> · <a href="candidats.html">Espace talents</a></p>
            </div>
            <div class="col-lg-4 offset-lg-1" id="postuler">
              <h3>Postuler</h3>
              <form class="tl-form" data-form="apply" data-job-slug="{slug}"><label>Nom</label><input name="nom" required>
              <label>Courriel</label><input type="email" name="courriel" required>
              <label>Téléphone</label><input name="tel">
              <label>Lien CV</label><input name="cv" placeholder="https://">
              <button class="tl-btn tl-btn-lg" type="submit">Postuler</button>
              <div class="tl-success"></div></form>
            </div>
          </div>
        </div></section>
        """,
        extra_json_ld=job_ld(title, city, slug, typ, sal, req),
        og_type="article",
    ))

# Secteurs
sec_cards = "".join(
    f'<a class="tl-card" href="secteur-{s}.html"><div class="body"><h3>{n}</h3><p>{d}</p></div></a>'
    for s, n, t, d in SECTORS
)
write("secteurs.html", wrap(
    "Tous les secteurs | Plateforme de recrutement — Talendus",
    "Talendus s'adresse à toutes les industries. Technologie, construction, santé, finance, manufacturier, commerce et bien plus encore.",
    "secteurs.html",
    page_hero(
        "Tous les secteurs", "Talendus s'adresse à toutes les industries.",
        "Ces secteurs sont des exemples de la capacité de la plateforme, pas une liste exclusive. Quel que soit votre secteur, Talendus vous aide à trouver les bons talents.",
        actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a>'
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
            actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a>'
        )
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} Ce n'est pas une spécialisation exclusive : Talendus recrute pour toutes les entreprises.</p>
              <h2 class="tl-h2">Métiers typiques</h2>
              <p>Opération, métiers spécialisés, supervision, gestion — et d'autres profils selon votre besoin.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="contact.html">Confiez-nous votre recrutement</a>
                <a class="tl-btn tl-btn-ghost-dark" href="secteurs.html">Tous les secteurs</a>
              </div>
            </div>
            <div class="col-lg-5">
              <div class="tl-card"><div class="body">
                <span class="tl-chip orange">Tous secteurs</span>
                <h3>Un exemple, pas une limite</h3>
                <p>Un brief clair, une shortlist, un seul conseiller. Pas 40 CV à trier.</p>
                <a class="tl-btn" href="contact.html" style="margin-top:16px">Parler à un recruteur</a>
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
        actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a>',
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
          <p>On cible des profils selon le métier et les compétences, on valide le fit et on présente peu de dossiers — chacun qu'on est prêt à défendre. L'IA viendra plus tard : matching et classement ne sont pas simulés aujourd'hui.</p>
          <p><a href="secteurs.html">Tous les secteurs</a> · <a href="emplois.html">Offres d'emploi</a> · <a href="entreprises.html">Solutions entreprises</a></p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Parler à un spécialiste</a>
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
    "Connectez-vous pour gérer votre profil, votre CV, vos candidatures et vos notifications Talendus.",
    "espace.html",
    page_hero(
        "Candidats", "Votre dossier Talendus.",
        "Profil, CV, candidatures, messages et entretiens. Suivez votre recherche d'emploi.",
        badges='<span class="tl-badge tl-badge-light">Espace privé</span>'
    )
    + """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account"></div></div></section>""",
    robots="noindex,nofollow",
))
write("espace-employeur.html", wrap(
    "Espace employeur | Talendus",
    "Connectez-vous pour gérer vos offres, candidatures, pipeline et factures Talendus.",
    "espace-employeur.html",
    page_hero(
        "Entreprises", "Votre espace employeur.",
        "Offres, dossiers présentés, pipeline et factures. Suivez vos recrutements.",
        badges='<span class="tl-badge tl-badge-light">Espace privé</span>'
    )
    + """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account" data-space="employer"></div></div></section>""",
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
    "Créez votre profil, postulez, suivez vos candidatures. Talendus présente votre dossier à l'employeur. Gratuit pour les talents.",
    "comment-ca-fonctionne.html",
    "Talents",
    "Du CV jusqu'à l'entrevue, on s'occupe de la présentation.",
    "Créez votre espace, déposez votre CV, postulez. Talendus parle à l'employeur à votre place. Vous n'envoyez jamais vos coordonnées en direct.",
    """
    <section class="tl-section"><div class="container">
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Créer son profil</h3><p>Métier, compétences, région, CV. Cinq minutes pour entrer dans le réseau.</p></div>
        <div class="tl-step"><span>02</span><h3>Postuler</h3><p>Offres ouvertes ou mandat confidentiel. On filtre avant de vous présenter.</p></div>
        <div class="tl-step"><span>03</span><h3>Suivre ses candidatures</h3><p>Un conseiller Talendus fait le pont. Pas de messages directs employeur–candidat.</p></div>
        <div class="tl-step"><span>04</span><h3>Être contacté</h3><p>Quand le poste, le salaire et l'environnement correspondent, on vous appelle.</p></div>
      </div>
    </div></section>
    """,
    actions='<a class="tl-btn" href="espace.html" data-auth-open="register">Créer mon profil</a>',
)

simple_page(
    "Publier une offre | Recrutement Talendus",
    "Publiez une offre d'emploi. Talendus sourcene, filtre et vous présente des dossiers. Tous secteurs.",
    "publier-une-offre.html",
    "Entreprises",
    "Décrivez le poste. On ouvre le sourcing.",
    "Poste, secteur, contrat, urgence : plus c'est clair, plus vite on vous envoie des dossiers. Comptez une trentaine de minutes pour le brief.",
    """
    <section class="tl-section"><div class="container">
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Brief</h3><p>30 minutes : poste, secteur, compétences, salaire réel.</p></div>
        <div class="tl-step"><span>02</span><h3>Publication cadrée</h3><p>Offre visible ou mandat confidentiel, selon votre besoin.</p></div>
        <div class="tl-step"><span>03</span><h3>Filtre Talendus</h3><p>Les candidatures passent par notre équipe. Vous voyez les dossiers présentés.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>Premiers dossiers visés en 7 jours sur un métier d'opérations.</p></div>
      </div>
    </div></section>
    """ + human_hire_band("fr"),
    actions='<a class="tl-btn" href="espace-employeur.html" data-auth-open="register">Publier une offre</a>',
)

simple_page(
    "Solutions RH | Accompagnement recrutement Talendus",
    "Structurer le recrutement : descriptifs, grilles salariales, entrevues conjointes et intégration 30/60/90. Tous secteurs.",
    "solutions-rh.html",
    "Entreprises",
    "Structurer le recrutement, pas seulement combler un trou.",
    "Descriptions de poste, grilles salariales, entrevues conjointes et suivi d'intégration — pour les entreprises qui veulent arrêter d'improviser.",
    """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Descriptifs de poste</h3><p>Un poste écrit comme il se vit : responsabilités, compétences, type de contrat.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Grilles salariales</h3><p>Aligner l'offre sur le marché, sans sous-payer un métier rare.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Intégration 30/60/90</h3><p>Suivi après la prise de poste. Garantie de remplacement sur les mandats permanents.</p></div></div>
      </div>
    </div></section>
    """,
    actions='<a class="tl-btn" href="contact.html">Parler à un recruteur</a>',
)

for old, new in [("about.html", "a-propos.html"), ("service.html", "services.html"), ("blog-single.html", "blog.html")]:
    write(old, wrap("Redirection | Talendus", "Redirection.", old,
                    f'<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="{new}">Continuer</a></p><script>location.replace("{new}");</script></div></section>',
                    robots="noindex,nofollow"))

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
    ("publier-une-offre.html", "en/post-a-job.html"),
    ("solutions-rh.html", "en/hr-solutions.html"),
    ("secteurs.html", "en/sectors.html"),
    ("blog.html", "en/blog.html"),
    ("contact.html", "en/contact.html"),
    ("confidentialite.html", "en/privacy.html"),
    ("conditions.html", "en/terms.html"),
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
    "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\nDisallow: /espace.html\nDisallow: /espace-employeur.html\nDisallow: /en/account.html\nDisallow: /en/account-employer.html\nDisallow: /candidate\nDisallow: /employer\nDisallow: /en/candidate\nDisallow: /en/employer\nDisallow: /index1.html\nDisallow: /index2.html\nDisallow: /index3.html\nDisallow: /index4.html\nDisallow: /index5.html\nDisallow: /index6.html\nDisallow: /index7.html\nDisallow: /index8.html\nDisallow: /index9.html\nDisallow: /index10.html\nDisallow: /projects.html\nDisallow: /team.html\nDisallow: /testimonial.html\nSitemap: https://talendus.ca/sitemap.xml\n",
    encoding="utf-8",
)
print("done")
