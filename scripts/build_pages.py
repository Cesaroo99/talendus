#!/usr/bin/env python3
"""Génère les pages piliers Talendus à partir du header/footer partagés."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parts import (
    wrap as wrap_page, page_hero, speed_strip, cta_band, faq_html,
    FAQ_HOME, FAQ_EMPLOYEURS, FAQ_CANDIDATS,
)
from en_pages import build_en
from seo_pages import write_fr as write_seo_fr

ROOT = Path(__file__).resolve().parents[1]
SPEED_STRIP = speed_strip("fr")
CTA_BAND = cta_band("fr")

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

JOBS = [
    ("cariste", "Cariste", "Laval", "entrepot", "Permanent", "22 à 26 $/h", "Quart de jour", "Permis chariot élévateur, 1 an d'expérience en entrepôt, SST."),
    ("operateur-production", "Opérateur de production", "Longueuil", "production", "Permanent", "20 à 24 $/h", "Quarts rotatifs", "Expérience d'usine, capacité à suivre des procédures, travail d'équipe."),
    ("soudeur", "Soudeur-monteur", "Drummondville", "metallurgie", "Permanent", "28 à 34 $/h", "Quart de jour", "Soudure MIG/TIG, lecture de plans, cartes de compétences un atout."),
    ("machiniste-cnc", "Machiniste CNC", "Saint-Jérôme", "manufacturier", "Permanent", "30 à 38 $/h", "Quart de jour", "Programmation ou set-up, lecture de dessins, 3 ans d'expérience."),
    ("electromecanicien", "Électromécanicien", "Montréal", "maintenance", "Permanent", "32 à 40 $/h", "Quarts rotatifs", "Dépannage, hydraulique, pneumatique, électricité industrielle."),
    ("mecanicien-industriel", "Mécanicien industriel", "Sherbrooke", "maintenance", "Permanent", "30 à 36 $/h", "Quart de jour", "Entretien préventif, alignement, convoyeurs, fiabilité."),
    ("journalier-usine", "Journalier d'usine", "Boucherville", "production", "Permanent", "18 à 21 $/h", "Quart de soir", "Bonne condition physique, ponctualité, formation interne offerte."),
    ("superviseur-production", "Superviseur de production", "Trois-Rivières", "supervision", "Permanent", "70 000 à 85 000 $", "Quart de jour", "Leadership d'équipe, KPI, Lean, 5 ans en usine."),
    ("coordonnateur-logistique", "Coordonnateur logistique", "Anjou", "logistique", "Permanent", "55 000 à 68 000 $", "Quart de jour", "WMS, planification, anglais un atout."),
    ("directeur-usine", "Directeur d'usine", "Québec", "cadres", "Permanent", "120 000 à 150 000 $", "Quart de jour", "P&L, Lean, gestion d'une usine 100+ employés. Mandat confidentiel."),
]

SECTORS = [
    ("manufacturier", "Manufacturier", "Recrutement manufacturier au Québec", "Usines de fabrication, assemblage et sous-traitance. Nous plaçons opérateurs, métiers et cadres de plant."),
    ("production", "Production", "Recrutement en production au Québec", "Lignes, méthodes, qualité et supervision. Des profils qui tiennent un quart et un standard."),
    ("entrepot", "Entrepôt", "Recrutement entrepôt Québec", "Caristes, préparateurs, commis et superviseurs d'entrepôt pour centres de distribution."),
    ("logistique", "Logistique", "Recrutement logistique Québec", "Planification, transport interne, WMS et coordination de la chaîne d'approvisionnement."),
    ("distribution", "Distribution", "Recrutement distribution Québec", "Centres de distribution, expédition, réception et gestion des stocks."),
    ("transport", "Transport", "Recrutement transport et logistique", "Coordination transport, expédition usine et profils liés aux flux industriels."),
    ("transformation-alimentaire", "Transformation alimentaire", "Recrutement alimentaire industriel Québec", "Usines alimentaires : hygiène, quarts, opérateurs et supervision de production."),
    ("metallurgie", "Métallurgie", "Recrutement métallurgie et soudure Québec", "Soudure, usinage, fabrication métallique et chaudronnerie."),
    ("plasturgie", "Plasturgie", "Recrutement plasturgie Québec", "Injection, extrusion, set-up de presses et techniciens de procédé."),
    ("maintenance", "Maintenance industrielle", "Recrutement maintenance industrielle Québec", "Électromécaniciens, mécaniciens industriels et responsables fiabilité."),
]

ARTICLES = [
    ("mauvaise-embauche", "Combien coûte une mauvaise embauche en usine ?", "RH", "usine-equipe.jpg",
     "Un mauvais fit en production ne se limite pas au salaire. Entre formation, heures supplémentaires, rebuts et roulement, la facture grimpe vite."),
    ("machiniste-cnc", "Recruter un machiniste CNC au Québec en 2026", "Manufacturier", "cnc-machiniste.jpg",
     "Le machiniste CNC est l'un des profils les plus tendus. Voici comment attirer, évaluer et retenir ce talent rare."),
    ("caristes-entrepot", "Pénurie de caristes : stratégies pour les entrepôts", "Logistique", "entrepot-logistique.jpg",
     "Les centres de distribution se disputent les caristes expérimentés. Trois leviers concrets pour sécuriser vos quarts."),
    ("superviseur-production", "Superviseur de production : le profil qui change une usine", "Production", "usine-equipe.jpg",
     "Un bon superviseur stabilise le quart, la qualité et le climat. Voici le portrait que nous validons sur le terrain."),
    ("roulement-manufacturier", "Réduire le roulement en recrutement manufacturier", "Recrutement", "soudeur-atelier.jpg",
     "Le roulement n'est pas qu'un problème salarial. Processus d'accueil, quarts et adéquation culturelle font la différence."),
]

TOPICS = [
    "Salaire soudeur au Québec", "Recrutement urgent en usine", "Cartes de compétences et SST",
    "Quart de soir : comment recruter", "Chasse de têtes directeur d'usine", "WMS et profils d'entrepôt",
    "Lean manufacturing et recrutement", "Intégration 30/60/90 en usine", "Électromécanicien : rareté du talent",
    "Recrutement en région vs Grand Montréal", "Marque employeur manufacturière", "Tests techniques en entrevue",
    "Préposé à la production alimentaire", "Contrats saisonniers en entrepôt", "Rétention des métiers spécialisés",
    "Coût d'un poste vacant en production", "Recruter des immigrants en usine", "Automatisation et nouveaux métiers",
    "FAQ garanties de remplacement", "Préparer une entrevue de superviseur",
]


INDEX_BODY = r"""
<div class="hero2-arrow-hero">
    <div class="hero-main-slider">
      <div class="hero2-slider-area">
        <div class="img1"><img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe de production dans une usine québécoise" fetchpriority="high" decoding="async"></div>
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="hero2-heading tl-hero-lock">
                        <h5>Les talents qui font tourner l'industrie.</h5>
                        <div class="space16"></div>
                        <h1>Premiers candidats qualifiés à partir de 7 jours.</h1>
                        <div class="space16"></div>
                        <p>Partenaire de recrutement pour les entreprises opérationnelles du Québec — production, maintenance, logistique, supervision et continuité des activités.</p>
                        <div class="space32"></div>
                        <div class="btn-area1">
                            <a href="contact.html" class="vl-btn2">Confier un recrutement <span><i class="fa-solid fa-arrow-right"></i></span></a>
                            <a href="candidats.html#cv" class="vl-btn2 btn2">Déposer mon CV <span><i class="fa-solid fa-arrow-right"></i></span></a>
                        </div>
                        <div class="tl-hero-badges">
                          <span class="tl-badge tl-badge-light">Opérations · Québec</span>
                          <span class="tl-badge tl-badge-light">Consultation sur rendez-vous</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="hero2-slider-area">
        <div class="img1"><img src="assets/img/all-images/industry/entrepot-logistique.jpg" alt="Entrepôt logistique et caristes au Québec" loading="lazy" decoding="async"></div>
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="hero2-heading tl-hero-lock">
                        <h5>Emplois industriels · Québec</h5>
                        <div class="space16"></div>
                        <h1>Trouvez un emploi d’usine au Québec, présenté aux bons employeurs.</h1>
                        <div class="space16"></div>
                        <p>Opérateur, cariste, soudeur, CNC, maintenance, supervision : on vous oriente vers des usines qui recrutent vraiment.</p>
                        <div class="space32"></div>
                        <div class="btn-area1">
                            <a href="emplois.html" class="vl-btn2">Trouver un emploi <span><i class="fa-solid fa-arrow-right"></i></span></a>
                            <a href="candidats.html#cv" class="vl-btn2 btn2">Déposer mon CV <span><i class="fa-solid fa-arrow-right"></i></span></a>
                        </div>
                        <div class="tl-hero-badges">
                          <span class="tl-badge tl-badge-light">Sans frais pour le candidat</span>
                          <span class="tl-badge tl-badge-light">Mandats d’usine réels</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    <div class="testimonial-arrow">
     <div class="prev-arrow-hero">
        <button type="button" aria-label="Slide suivante"><i class="fa-solid fa-arrow-right"></i></button>
        </div>
        <div class="next-arrow-hero">
        <button type="button" aria-label="Slide précédente"><i class="fa-solid fa-arrow-left"></i></button>
        </div>
    </div>
</div>
""" + r"""
<section class="tl-section-sm">
  <div class="container">
    <div class="tl-split">
      <a class="employeurs" href="entreprises.html">
        <div class="tl-kicker" style="color:#ffb37a">Entreprises</div>
        <h3>Besoin d’un talent qui tient la production, la logistique ou la maintenance ?</h3>
        <p>Consultation gratuite, sur rendez-vous. Présélection calée sur votre quart — pas 80 CV à trier en fin de shift.</p>
        <span class="tl-split-cta">Confier un recrutement →</span>
      </a>
      <a class="candidats" href="candidats.html">
        <div class="tl-kicker" style="color:#cfe0ff">Candidats</div>
        <h3>Un poste en production, en logistique ou en maintenance ?</h3>
        <p>Déposez votre CV. Nous vous présentons aux employeurs opérationnels du Québec — pas à des mandats fourre-tout.</p>
        <span class="tl-split-cta">Déposer mon CV →</span>
      </a>
    </div>
  </div>
</section>

<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Chiffres clés</div>
      <h2 class="tl-h2">Un cabinet calibré pour la réalité des usines québécoises</h2>
    </div>
    <div class="tl-stats">
      <div class="tl-stat"><b>7 j</b><p>Premiers candidats qualifiés à partir de 7 jours, sur les mandats d’opération</p></div>
      <div class="tl-stat"><b>92 %</b><p>Des placements encore en poste après la période d’essai</p></div>
      <div class="tl-stat"><b>100 %</b><p>De nos mandats dans l’industrie, la logistique ou l’entreposage</p></div>
      <div class="tl-stat"><b>1 200+</b><p>Talents industriels actifs dans notre réseau au Québec</p></div>
    </div>
  </div>
</section>

<section class="tl-section">
  <div class="container">
    <div class="row align-items-center g-4">
      <div class="col-lg-6">
        <div class="tl-kicker">Pourquoi Talendus</div>
        <h2 class="tl-h2">Le partenaire d’acquisition de talents pour l’industrie québécoise</h2>
        <p class="tl-lead">Quand une ligne, un quai ou un quart s’arrête, le coût n’est pas un poste vacant : c’est de la production perdue. Nous parlons opérations, maintenance, logistique et supervision — pas un jargon RH générique.</p>
        <div class="space24"></div>
        <ul class="tl-muted">
          <li>Spécialisation : production, manufacturier, logistique, maintenance, transport et supervision.</li>
          <li>Évaluation terrain : compétences, quart de travail, culture opérationnelle.</li>
          <li>Garantie de remplacement sur les mandats permanents.</li>
        </ul>
        <div class="space32"></div>
        <div class="tl-actions">
          <a href="contact.html" class="tl-btn">Confier un recrutement</a>
          <a href="a-propos.html" class="tl-btn tl-btn-ghost-dark">Notre approche</a>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="tl-hero-media" style="height:420px;border-radius:18px;overflow:hidden">
          <img src="assets/img/all-images/industry/cnc-machiniste.jpg" alt="Machiniste CNC dans une usine au Québec">
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Secteurs desservis</div>
      <h2 class="tl-h2">Nous recrutons là où le Québec produit, transforme, expédie et maintient</h2>
    </div>
    <div class="tl-grid-4">
      <a class="tl-card" href="secteur-manufacturier.html"><div class="body"><h3>Manufacturier</h3><p>Usines de fabrication, assemblage et sous-traitance industrielle.</p></div></a>
      <a class="tl-card" href="secteur-production.html"><div class="body"><h3>Production</h3><p>Opérations, méthodes, qualité et supervision de ligne.</p></div></a>
      <a class="tl-card" href="secteur-entrepot.html"><div class="body"><h3>Entrepôt</h3><p>Manutention, caristes, préparation de commandes et WMS.</p></div></a>
      <a class="tl-card" href="secteur-logistique.html"><div class="body"><h3>Logistique</h3><p>Distribution, transport interne et chaîne d’approvisionnement.</p></div></a>
      <a class="tl-card" href="secteur-transformation-alimentaire.html"><div class="body"><h3>Alimentaire</h3><p>Transformation, emballage et normes d’hygiène en usine.</p></div></a>
      <a class="tl-card" href="secteur-metallurgie.html"><div class="body"><h3>Métallurgie</h3><p>Soudure, usinage, fabrication métallique et chaudronnerie.</p></div></a>
      <a class="tl-card" href="secteur-plasturgie.html"><div class="body"><h3>Plasturgie</h3><p>Injection, extrusion et opération de presses.</p></div></a>
      <a class="tl-card" href="secteur-maintenance.html"><div class="body"><h3>Maintenance</h3><p>Électromécanique, mécanique industrielle et fiabilité.</p></div></a>
    </div>
  </div>
</section>

<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Métiers recrutés</div>
      <h2 class="tl-h2">Du journalier d’usine au directeur de plant</h2>
    </div>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Production</span><h3>Métiers d’usine</h3><p>Journalier, opérateur, assembleur, emballeur, préposé à la ligne.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Spécialisés</span><h3>Métiers techniques</h3><p>Soudeur, machiniste CNC, électromécanicien, mécanicien industriel.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Logistique</span><h3>Entrepôt &amp; distribution</h3><p>Cariste, commis, coordonnateur logistique, superviseur d’entrepôt.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Supervision</span><h3>Encadrement</h3><p>Superviseur de production, contremaître, chef d’équipe de quart.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Cadres</span><h3>Gestion manufacturière</h3><p>Directeur d’usine, directeur de production, responsable maintenance.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Urgent</span><h3>Renforts de quart</h3><p>Mandats accélérés quand un quart critique doit être comblé — sans diluer le filtre technique.</p></div></div>
    </div>
    <div class="tl-center" style="margin-top:28px"><a class="tl-btn" href="emplois.html">Trouver un emploi</a></div>
  </div>
</section>

<section class="tl-section tl-dark">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Méthodologie</div>
      <h2 class="tl-h2">Un processus en 5 étapes, calé sur vos délais de production</h2>
    </div>
    <div class="tl-steps">
      <div class="tl-step"><span>01</span><h3>Diagnostic d’usine</h3><p>Quart, compétences, SST, culture et urgence réelle du mandat.</p></div>
      <div class="tl-step"><span>02</span><h3>Ciblage industriel</h3><p>Réseau passif, références d’usine et approche directe.</p></div>
      <div class="tl-step"><span>03</span><h3>Évaluation terrain</h3><p>Entrevues techniques, validations et tests de compétences.</p></div>
      <div class="tl-step"><span>04</span><h3>Présentation</h3><p>Dossiers comparables, recommandation claire. Premiers candidats qualifiés à partir de 7 jours.</p></div>
      <div class="tl-step"><span>05</span><h3>Intégration</h3><p>Suivi 30/60/90 jours et garantie de remplacement.</p></div>
    </div>
  </div>
</section>

<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Études de cas</div>
      <h2 class="tl-h2">Des mandats industriels menés jusqu’à la prise de poste</h2>
    </div>
    <div class="tl-grid-3">
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="assets/img/all-images/industry/soudeur-atelier.jpg" alt="Mandat de recrutement de soudeurs"></div>
        <div class="body">
          <span class="tl-chip">Métallurgie · Drummondville</span>
          <h3>3 soudeurs-monteurs pour un deuxième quart</h3>
          <p>Une PME en croissance devait ouvrir un quart sans arrêter la ligne. Présélection technique, démarrage cadré.</p>
        </div>
      </article>
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="assets/img/all-images/industry/entrepot-logistique.jpg" alt="Recrutement en centre de distribution"></div>
        <div class="body">
          <span class="tl-chip">Entrepôt · Laval</span>
          <h3>Superviseur de quart + 8 caristes</h3>
          <p>Pic saisonnier absorbé en 4 semaines, avec une rétention supérieure à la moyenne du site.</p>
        </div>
      </article>
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="assets/img/all-images/industry/maintenance-tech.jpg" alt="Recrutement d'un directeur d'usine"></div>
        <div class="body">
          <span class="tl-chip">Cadre · Montérégie</span>
          <h3>Directeur d’usine confidentiel</h3>
          <p>Chasse de têtes discrète. Prise de poste en 9 semaines, sans perturbation interne.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Témoignages</div>
      <h2 class="tl-h2">Ce que disent les usines et les candidats</h2>
      <p class="tl-lead">Des retours d’employeurs manufacturiers et de professionnels placés au Québec — pas des citations génériques.</p>
    </div>
    <div class="tl-grid-3 tl-quotes">
      <blockquote class="tl-quote">
        <div class="tl-quote-mark" aria-hidden="true">“</div>
        <p>Ils ont compris nos quarts rotatifs dès le premier appel. Le superviseur présenté connaissait déjà un environnement Lean comparable.</p>
        <footer><strong>M.L.</strong><span>Directrice des opérations · usine alimentaire, Rive-Sud</span></footer>
      </blockquote>
      <blockquote class="tl-quote">
        <div class="tl-quote-mark" aria-hidden="true">“</div>
        <p>Pas une agence qui envoie 40 CV. Trois dossiers solides, un électromécanicien en poste, et un suivi après l’embauche.</p>
        <footer><strong>J.R.</strong><span>Directeur maintenance · métallurgie, Mauricie</span></footer>
      </blockquote>
      <blockquote class="tl-quote">
        <div class="tl-quote-mark" aria-hidden="true">“</div>
        <p>J’étais cariste de nuit. Talendus m’a présenté un poste de coordonnateur logistique à Laval. Entrevue claire, conditions nettes.</p>
        <footer><strong>A.D.</strong><span>Candidate placée · Laval</span></footer>
      </blockquote>
    </div>
  </div>
</section>

<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">FAQ</div>
      <h2 class="tl-h2">Avant d’ouvrir un mandat ou de déposer un CV</h2>
      <p class="tl-lead">Les questions que se posent les RH, les directeurs d’usine et les candidats — réponses franches.</p>
    </div>
    """ + faq_html(FAQ_HOME) + r"""
  </div>
</section>

<section class="tl-section tl-ice" id="contact-rapide">
  <div class="container">
    <div class="row align-items-center g-4">
      <div class="col-lg-5">
        <div class="tl-kicker">Contact</div>
        <h2 class="tl-h2">Parlez-nous de votre mandat ou de votre CV</h2>
        <p class="tl-lead">Consultations sur rendez-vous uniquement. Réponse moyenne sous 30 minutes durant les heures d’ouverture.</p>
        <div class="tl-notice">Lun–Ven, 8 h à 17 h · Rencontres planifiées selon vos disponibilités.</div>
            <p><a href="tel:+15145550199">514 555-0199</a><br><a href="mailto:info@talendus.ca">info@talendus.ca</a><br><a href="https://wa.me/15145550199?text=Bonjour%20Talendus%2C%20je%20souhaite%20discuter%20d%27un%20besoin%20de%20recrutement." target="_blank" rel="noopener noreferrer">WhatsApp</a></p>
            <div class="tl-actions" style="margin-top:18px">
              <a class="tl-btn" href="contact.html">Confier un recrutement</a>
        </div>
      </div>
      <div class="col-lg-6 offset-lg-1">
        <form class="tl-form" action="#" method="post" data-form="contact">
          <label for="nom">Nom</label>
          <input id="nom" name="nom" required placeholder="Votre nom">
          <label for="courriel">Courriel</label>
          <input id="courriel" type="email" name="courriel" required placeholder="prenom@entreprise.ca">
          <label for="profil">Vous êtes</label>
          <select id="profil" name="profil">
            <option>Employeur — je recrute</option>
            <option>Candidat — je cherche un poste</option>
          </select>
          <label for="msg">Message</label>
          <textarea id="msg" name="message" placeholder="Poste, ville, urgence ou métier visé"></textarea>
          <button class="tl-btn tl-btn-lg" type="submit">Obtenir une consultation gratuite</button>
          <div class="tl-success" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>

""" + CTA_BAND + r"""
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Blog</div>
      <h2 class="tl-h2">Ressources recrutement, RH et industrie au Québec</h2>
    </div>
    <div class="tl-grid-3">
      <a class="tl-card" href="article-mauvaise-embauche.html"><div class="tl-hero-media" style="height:180px"><img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe d'usine au Québec" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">RH</span><h3>Combien coûte une mauvaise embauche en usine ?</h3></div></a>
      <a class="tl-card" href="article-machiniste-cnc.html"><div class="tl-hero-media" style="height:180px"><img src="assets/img/all-images/industry/cnc-machiniste.jpg" alt="Machiniste CNC" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">Manufacturier</span><h3>Recruter un machiniste CNC au Québec</h3></div></a>
      <a class="tl-card" href="article-caristes-entrepot.html"><div class="tl-hero-media" style="height:180px"><img src="assets/img/all-images/industry/entrepot-logistique.jpg" alt="Caristes en entrepôt" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">Logistique</span><h3>Pénurie de caristes : stratégies d’entrepôt</h3></div></a>
    </div>
  </div>
</section>
"""

write("index.html", wrap(
    "Talendus | Recrutement industriel et manufacturier au Québec",
    "Talendus recrute les talents qui font tourner l’industrie québécoise : production, maintenance, logistique et supervision. Consultation sur rendez-vous.",
    "",
    INDEX_BODY,
    solid=False,
))


def simple_page(title, desc, slug, kicker, h1, lead, inner, actions=""):
    body = page_hero(kicker, h1, lead, actions) + inner
    write(slug, wrap(title, desc, slug, body))


# À propos
simple_page(
    "À propos de Talendus | Cabinet de recrutement industriel Québec",
    "Histoire, mission, vision et valeurs de Talendus, cabinet exclusivement dédié au recrutement manufacturier, logistique et d'entrepôt au Québec.",
    "a-propos.html", "Le cabinet", "Talendus existe pour une seule industrie : la vôtre.",
    "Nous recrutons les talents qui assurent la production, les opérations, la maintenance, la logistique et la continuité des entreprises québécoises.",
    """
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <h2 class="tl-h2">Histoire</h2>
    <p class="tl-lead">Talendus est né d'un constat simple : trop d'usines québécoises perdent des semaines avec des agences généralistes qui ne distinguent pas un set-up CNC d'un poste de bureau. Nous avons bâti un cabinet qui ne parle qu'usine, quart, SST et performance de ligne.</p>
    <h2 class="tl-h2">Mission</h2>
    <p>Connecter durablement les employeurs industriels du Québec aux talents qui font tourner la production — opérateurs, métiers spécialisés, superviseurs et cadres d'usine.</p>
    <h2 class="tl-h2">Vision</h2>
    <p>Devenir la référence du recrutement industriel au Québec : le premier appel quand une usine doit embaucher juste, avec un cabinet qui ne dilue pas son vivier.</p>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe Talendus sur le plancher d'usine">
      </div>
      <a class="tl-btn tl-btn-lg" href="contact.html">Réserver une consultation gratuite</a>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">Valeurs</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Spécialisation</h3><p>Aucun mandat hors industrie. C'est notre filtre, et votre garantie de ne pas diluer le vivier.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Rigueur terrain</h3><p>Nous évaluons comme un contremaître, pas comme un algorithme. Compétences, quart, SST, attitude.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Parole tenue</h3><p>Délais, dossiers, garantie : ce qui est dit est livré. Un interlocuteur unique jusqu’à la prise de poste.</p></div></div>
    </div>
    </div></section>
    <section class="tl-section"><div class="container">
    <div class="row g-4">
      <div class="col-lg-6">
        <h2 class="tl-h2">Pourquoi l'industrie manufacturière</h2>
        <p>C'est là que le Québec crée de la valeur réelle. C'est aussi là que la pénurie de métiers se fait le plus sentir. Nous avons choisi ce champ — et seulement celui-là.</p>
        <h2 class="tl-h2">Nos engagements</h2>
        <ul>
          <li>Présélection industrielle avant toute présentation.</li>
          <li>Transparence sur les délais et la rareté du profil.</li>
          <li>Suivi d'intégration 30/60/90 jours.</li>
          <li>Garantie de remplacement sur les mandats permanents.</li>
        </ul>
      </div>
      <div class="col-lg-6">
        <div class="tl-stats" style="grid-template-columns:1fr 1fr">
          <div class="tl-stat"><b>7 j</b><p>Première shortlist qualifiée</p></div>
          <div class="tl-stat"><b>100 %</b><p>Mandats industriels</p></div>
          <div class="tl-stat"><b>92 %</b><p>Rétention post-essai</p></div>
          <div class="tl-stat"><b>1 200+</b><p>Talents en réseau</p></div>
        </div>
      </div>
    </div>
    </div></section>
    """ + CTA_BAND,
    actions='<a class="tl-btn" href="contact.html">Parler à un spécialiste</a><a class="tl-btn tl-btn-ghost" href="services.html">Voir les services</a>'
)

# Services
services_cards = "".join(
    f'<a class="tl-card" href="{href}"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></a>'
    for href, chip, t, p in [
        ("recrutement-permanent.html", "Permanent", "Recrutement permanent", "Mandats de postes stables en usine, entrepôt et gestion manufacturière. Honoraires au succès, garantie de remplacement."),
        ("chasse-de-tetes.html", "Passif", "Chasse de têtes", "Approche directe de candidats passifs pour les profils rares : CNC, électromécanique, cadres d'usine."),
        ("recrutement-cadres.html", "Direction", "Recrutement de cadres", "Directeurs d'usine, de production, de maintenance et de logistique. Mandats souvent confidentiels."),
        ("recrutement-industriel.html", "Quart", "Recrutement de superviseurs", "Contremaîtres et superviseurs de quart capables de tenir KPI, SST et climat d'équipe."),
        ("recrutement-technique.html", "Métiers", "Métiers spécialisés", "Soudeurs, machinistes, mécaniciens industriels, électromécaniciens, set-up, qualité."),
        ("recrutement-temporaire.html", "Urgent", "Recrutement urgent", "Processus accéléré lorsqu’un quart critique est découvert. Shortlist filtrée, pas une avalanche de CV."),
        ("chasse-de-tetes.html", "Discret", "Mandats confidentiels", "Remplacements de cadres ou réorganisations menés sans bruit interne."),
        ("entreprises.html", "RH", "Accompagnement RH", "Descriptifs de poste, grilles salariales industrielles, entrevues conjointes et intégration."),
    ]
)
simple_page(
    "Services de recrutement industriel | Talendus Québec",
    "Recrutement permanent, chasse de têtes, cadres, superviseurs et métiers spécialisés pour les usines du Québec.",
    "services.html", "Services", "Des services pensés pour l'usine, pas pour un siège social.",
    "Du journalier au directeur de plant : un seul cabinet, exclusivement industriel.",
    f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-6">
          <h2 class="tl-h2">Pourquoi les usines nous mandatent</h2>
          <p class="tl-lead">Parce qu'un dossier de trop, c'est du temps de contremaître perdu. Nous présentons peu de candidats, mais chacun a déjà passé le filtre du plancher.</p>
          <ul>
            <li>Shortlist industrielle, pas un portail d'emplois déguisé.</li>
            <li>Délai annoncé dès le brief, selon la rareté réelle du profil.</li>
            <li>Un interlocuteur qui connaît les quarts, la SST et le plancher.</li>
          </ul>
        </div>
        <div class="col-lg-6">
          <div class="tl-hero-media" style="height:340px;border-radius:18px;overflow:hidden">
            <img src="assets/img/all-images/industry/soudeur-atelier.jpg" alt="Recrutement de métiers spécialisés en usine">
          </div>
        </div>
      </div>
      <div class="tl-actions" style="margin-top:36px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Confier un recrutement</a>
        <a class="tl-btn tl-btn-ghost-dark" href="entreprises.html">Espace entreprises</a>
      </div>
    </div></section>
    ''' + CTA_BAND,
    actions='<a class="tl-btn" href="contact.html">Confier un recrutement</a><a class="tl-btn tl-btn-ghost" href="entreprises.html">Parler à un spécialiste</a>'
)

# Entreprises (URL canonique) + redirection Employeurs
EMPLOYERS_BODY = (
    page_hero(
        "Entreprises",
        "Votre opération n'a pas besoin de 80 CV. Elle a besoin du bon talent, au bon quart.",
        "Consultation gratuite, sur rendez-vous. Présélection industrielle. Garantie de remplacement.",
        actions='<a class="tl-btn" href="contact.html">Confier un recrutement</a><a class="tl-btn tl-btn-ghost" href="contact.html">Réserver une consultation</a>',
        badges='<span class="tl-badge tl-badge-light">Consultation sur rendez-vous</span> <span class="tl-badge tl-badge-light">Partenaire opérationnel</span>'
    )
    + SPEED_STRIP
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Spécialisation</span><h3>Pourquoi Talendus</h3><p>Un cabinet dédié aux entreprises opérationnelles. Réseau passif, évaluation technique et suivi d'intégration — pas une agence qui recrute aussi des adjoints administratifs.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Délai</span><h3>Délais tenus</h3><p>Premiers candidats qualifiés à partir de 7 jours sur les métiers d’opération. 3 à 8 semaines pour superviseurs, métiers rares et cadres — annoncé dès le brief.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Confiance</span><h3>Garanties</h3><p>Remplacement inclus sur les mandats permanents. Conditions confirmées à l'ouverture du dossier. Un interlocuteur unique jusqu'à la prise de poste.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Comment ça se passe</div>
        <h2 class="tl-h2">De l'appel au premier dossier, sans friction</h2>
      </div>
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Consultation</h3><p>30 minutes pour comprendre le quart, le salaire réel et l'urgence.</p></div>
        <div class="tl-step"><span>02</span><h3>Ciblage</h3><p>On active le réseau passif et les références d'opération.</p></div>
        <div class="tl-step"><span>03</span><h3>Filtre terrain</h3><p>Entrevue Talendus avant que votre contremaître perde une heure.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>Premiers candidats qualifiés à partir de 7 jours. Dossiers comparables, recommandation claire.</p></div>
        <div class="tl-step"><span>05</span><h3>Suivi</h3><p>Intégration 30/60/90 et garantie de remplacement.</p></div>
      </div>
    </div></section>
    <section class="tl-section" id="calculateur"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-5"><h2 class="tl-h2">Calculateur : coût d'une mauvaise embauche</h2>
        <p class="tl-lead">Estimez l'impact d'un mauvais fit (salaire, formation, heures sup. et perte de productivité). Un mandat Talendus coûte presque toujours moins cher qu'un quart instable.</p>
        <a class="tl-btn" href="contact.html">Confier un recrutement</a></div>
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
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">FAQ entreprises</div>
        <h2 class="tl-h2">Ce que demandent les RH et les directeurs d’opérations</h2>
      </div>
      """ + faq_html(FAQ_EMPLOYEURS) + """
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Confier un recrutement</a>
      </div>
    </div></section>
    """ + CTA_BAND
)
write("entreprises.html", wrap(
    "Entreprises | Recrutement manufacturier et industriel au Québec — Talendus",
    "Confiez un recrutement à Talendus. Présélection industrielle et garantie de remplacement pour les entreprises opérationnelles du Québec.",
    "entreprises.html",
    EMPLOYERS_BODY,
))
write("employeurs.html", wrap(
    "Employeurs | Recrutement manufacturier et industriel au Québec — Talendus",
    "Redirection vers l’espace entreprises Talendus.",
    "employeurs.html",
    '<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="entreprises.html">Continuer vers Entreprises</a></p><script>location.replace("entreprises.html");</script></div></section>',
))

# Candidats
write("candidats.html", wrap(
    "Candidats | Emplois usine, entrepôt et métiers spécialisés au Québec — Talendus",
    "Déposez votre CV chez Talendus. Offres en usine, entrepôt, logistique, maintenance et supervision au Québec.",
    "candidats.html",
    page_hero(
        "Candidats",
        "Des postes d'usine et d'entrepôt, présentés clairement.",
        "Nous travaillons avec des employeurs manufacturiers du Québec — pas des mandats fourre-tout. Accompagnement jusqu'à la prise de poste.",
        actions='<a class="tl-btn" href="candidats.html#cv">Déposer mon CV</a><a class="tl-btn tl-btn-ghost" href="emplois.html">Voir les offres</a>',
        badges='<span class="tl-badge tl-badge-light">Sans frais pour vous</span> <span class="tl-badge tl-badge-light">Mandats d’usine réels</span>'
    )
    + """
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Déposer votre CV</h2>
          <p class="tl-lead">Indiquez votre métier, vos quarts possibles et votre région. Un conseiller vous rejoint si un mandat correspond — sans vous envoyer sur 15 entrevues inutiles.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">Réponse moyenne sous 30 minutes durant les heures d’ouverture.</div>
          <p id="processus"></p>
          <h3>Notre processus candidat</h3>
          <ol>
            <li>Réception et qualification de votre profil.</li>
            <li>Entrevue Talendus (compétences, quarts, mobilité).</li>
            <li>Présentation aux employeurs industriels pertinents.</li>
            <li>Préparation à l'entrevue d'usine.</li>
            <li>Suivi jusqu'à la prise de poste.</li>
          </ol>
          <div class="tl-actions" style="margin-top:8px">
            <a class="tl-btn tl-btn-electric" href="emplois.html">Trouver un emploi</a>
          </div>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Nom</label><input required name="nom">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Métier visé</label>
            <select name="metier">
              <option>Cariste</option><option>Opérateur de production</option><option>Soudeur</option>
              <option>Machiniste CNC</option><option>Électromécanicien</option><option>Superviseur</option>
              <option>Autre métier industriel</option>
            </select>
            <label>Région</label><input name="region" placeholder="Laval, Montérégie, Québec...">
            <label>Lien vers votre CV (Drive, Dropbox...)</label><input name="cv" placeholder="https://">
            <button class="tl-btn tl-btn-lg" type="submit">Déposer mon CV</button>
            <div class="tl-success" role="status"></div>
          </form>
        </div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <h2 class="tl-h2">Conseils carrière</h2>
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Préparer une entrevue d'usine</h3><p>Exemples de pannes, SST, travail d'équipe de quart : ce que les contremaîtres écoutent vraiment.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Mettre en valeur vos cartes</h3><p>Chariot, espace clos, cadenassage, soudure : listez-les en tête de CV. C'est souvent le premier filtre.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Voir les offres</h3><p><a href="emplois.html">Consultez les postes ouverts</a> ou laissez-nous vous approcher pour un mandat confidentiel.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">FAQ candidats</div>
        <h2 class="tl-h2">Avant de déposer votre CV</h2>
      </div>
      """ + faq_html(FAQ_CANDIDATS) + """
    </div></section>
    """ + CTA_BAND
))

# Contact
write("contact.html", wrap(
    "Contact | Consultation recrutement industriel Québec — Talendus",
    "Contactez Talendus à Montréal. Consultations sur rendez-vous uniquement. Réponse moyenne sous 30 minutes durant les heures d’ouverture. 514 555-0199 · info@talendus.ca",
    "contact.html",
    page_hero(
        "Contact",
        "Consultation gratuite pour votre prochain mandat industriel.",
        "Consultations sur rendez-vous uniquement. Réponse moyenne sous 30 minutes durant les heures d’ouverture.",
        actions='<a class="tl-btn" href="tel:+15145550199">Parler à un spécialiste</a><a class="tl-btn tl-btn-ghost" href="#formulaire">Réserver une consultation</a>',
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
            <p>Réponse moyenne sous 30 minutes durant les heures d’ouverture.</p>
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
            <p>Employeurs et candidats · réponse durant les heures d’ouverture.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-calendar-check"></i></div>
          <div>
            <h3>Rencontres</h3>
            <p>Consultations sur rendez-vous uniquement.</p>
            <p>Rencontres planifiées selon vos disponibilités.</p>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section" id="formulaire"><div class="container">
      <div class="tl-contact-grid">
        <div>
          <div class="tl-kicker">Formulaire</div>
          <h2 class="tl-h2">Décrivez le poste ou votre profil</h2>
          <p class="tl-lead">Employeur : ouvrez un mandat. Candidat : déposez votre CV. Un conseiller industriel vous revient — en moyenne sous 30 minutes durant les heures d’ouverture.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Nom</label><input required name="nom">
            <label>Entreprise (optionnel)</label><input name="entreprise">
            <label>Courriel</label><input type="email" required name="courriel">
            <label>Téléphone</label><input name="tel">
            <label>Objet</label>
            <select name="objet">
              <option>Confier un recrutement</option>
              <option>Réserver une consultation</option>
              <option>Déposer mon CV</option>
              <option>Rejoindre la banque de talents</option>
            </select>
            <label>Message</label><textarea required name="message" placeholder="Poste, ville, quart, urgence ou métier visé"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Confier un recrutement</button>
            <div class="tl-success"></div>
          </form>
        </div>
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
for slug, title, city, cat, typ, sal, shift, req in JOBS:
    cards.append(f'''
    <article class="tl-job-card" data-job="{title} {city} {cat} {typ} {sal} {shift}" data-city="{city}" data-cat="{cat}" data-type="{typ}" data-shift="{shift}" data-salary="{sal}">
      <div class="body">
        <span class="tl-chip orange">{typ}</span><span class="tl-chip">{city}</span>
        <h3><a href="emploi-{slug}.html">{title}</a></h3>
        <p>{sal} · {shift}</p>
        <a class="tl-split-cta" href="emploi-{slug}.html" style="color:var(--tl-orange);margin-top:auto;padding-top:14px">Voir le poste →</a>
      </div>
    </article>''')
write("emplois.html", wrap(
    "Offres d'emploi usine et entrepôt au Québec | Talendus",
    "Postes de cariste, opérateur, soudeur, machiniste CNC, électromécanicien, superviseur et directeur d'usine au Québec.",
    "emplois.html",
    page_hero(
        "Offres d'emploi", "Postes industriels ouverts au Québec",
        "Recherchez par métier, ville, salaire, type d’emploi et quart de travail. Candidature en un formulaire.",
        actions='<a class="tl-btn" href="candidats.html#cv">Déposer mon CV</a><a class="tl-btn tl-btn-ghost" href="contact.html">Confier un recrutement</a>',
        badges='<span class="tl-badge tl-badge-light">Banque de talents</span>'
    )
    + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-filters">
        <input id="job-search" placeholder="Rechercher un métier, une ville…">
        <select id="job-cat">
          <option value="">Toutes les catégories</option>
          <option value="production">Production</option>
          <option value="entrepot">Entrepôt</option>
          <option value="logistique">Logistique</option>
          <option value="maintenance">Maintenance</option>
          <option value="metallurgie">Métallurgie</option>
          <option value="supervision">Supervision</option>
          <option value="cadres">Cadres</option>
        </select>
        <select id="job-city">
          <option value="">Toutes les villes</option>
          <option>Laval</option><option>Longueuil</option><option>Montréal</option>
          <option>Drummondville</option><option>Saint-Jérôme</option>
          <option>Sherbrooke</option><option>Boucherville</option>
          <option>Anjou</option><option>Trois-Rivières</option><option>Québec</option>
        </select>
        <select id="job-type">
          <option value="">Tous les types</option>
          <option value="Permanent">Permanent</option>
          <option value="Temporaire">Temporaire</option>
        </select>
        <select id="job-shift">
          <option value="">Tous les quarts</option>
          <option value="Quart de jour">Quart de jour</option>
          <option value="Quart de soir">Quart de soir</option>
          <option value="Quarts rotatifs">Quarts rotatifs</option>
        </select>
        <select id="job-sal">
          <option value="">Tous les salaires</option>
          <option value="18">18 $/h et +</option>
          <option value="25">25 $/h et +</option>
          <option value="30">30 $/h et +</option>
          <option value="50000">50 000 $ et +</option>
        </select>
      </div>
      <div class="tl-grid-3" id="job-list">{''.join(cards)}</div>
      <p class="tl-muted" id="job-empty" hidden>Aucun poste ne correspond à ces filtres. Déposez votre CV pour rejoindre la banque de talents.</p>
    </div></section>
    """
))

for slug, title, city, cat, typ, sal, shift, req in JOBS:
    write(f"emploi-{slug}.html", wrap(
        f"{title} à {city} | Emploi industriel Québec — Talendus",
        f"Poste de {title} à {city}, Québec. {typ}. Postulez via Talendus, cabinet de recrutement industriel.",
        f"emploi-{slug}.html",
        page_hero(
            f"{city} · {typ}", title, f"{sal} · {shift} · Recrutement industriel Talendus",
            actions='<a class="tl-btn" href="#postuler">Déposer mon CV</a><a class="tl-btn tl-btn-ghost" href="emplois.html">Trouver un emploi</a>',
            badges='<span class="tl-badge tl-badge-light">Poste industriel</span>'
        )
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <h2 class="tl-h2">Le poste</h2>
              <p class="tl-lead">Talendus recrute un(e) {title.lower()} pour un employeur manufacturier / logistique à {city}. Environnement d'usine, exigences SST et rythme de production réels.</p>
              <h3>Profil recherché</h3>
              <p>{req}</p>
              <h3>Ce que nous offrons</h3>
              <ul><li>Poste {typ.lower()}</li><li>Rémunération : {sal}</li><li>Horaire : {shift}</li><li>Accompagnement Talendus jusqu'à l'embauche</li></ul>
              <p><a href="emplois.html">← Toutes les offres</a> · <a href="recrutement-industriel.html">Recrutement industriel</a> · <a href="candidats.html">Espace candidats</a></p>
            </div>
            <div class="col-lg-4 offset-lg-1" id="postuler">
              <h3>Postuler</h3>
              <form class="tl-form" data-form="apply" data-job-slug="{slug}"><label>Nom</label><input name="nom" required>
              <label>Courriel</label><input type="email" name="courriel" required>
              <label>Téléphone</label><input name="tel">
              <label>Lien CV</label><input name="cv" placeholder="https://">
              <button class="tl-btn tl-btn-lg" type="submit">Déposer mon CV</button>
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
    "Secteurs d'activité | Recrutement industriel Québec — Talendus",
    "Talendus recrute dans le manufacturier, la production, l'entrepôt, la logistique, l'alimentaire, la métallurgie, la plasturgie et la maintenance au Québec.",
    "secteurs.html",
    page_hero(
        "Secteurs", "Une expertise par type d'usine, pas un discours générique.",
        "Choisissez votre industrie. Nous parlons déjà votre langage opérationnel.",
        actions='<a class="tl-btn" href="contact.html">Confier un recrutement</a>'
    )
    + f'<section class="tl-section"><div class="container"><div class="tl-grid-3">{sec_cards}</div></div></section>'
))
for slug, name, title, desc in SECTORS:
    write(f"secteur-{slug}.html", wrap(
        f"{title} | Talendus",
        desc,
        f"secteur-{slug}.html",
        page_hero(
            "Secteur", name, desc,
            actions='<a class="tl-btn" href="contact.html">Confier un recrutement</a><a class="tl-btn tl-btn-ghost" href="contact.html">Réserver une consultation</a>'
        )
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} Talendus n'envoie pas de profils de bureau : uniquement des talents qui ont déjà vécu un plancher d'usine ou un quai de réception.</p>
              <h2 class="tl-h2">Métiers typiques</h2>
              <p>Opération, métiers spécialisés, supervision et cadres selon la taille de votre site. Des profils qui ont déjà vécu un plancher d’usine.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="contact.html">Ouvrir un mandat {name.lower()}</a>
                <a class="tl-btn tl-btn-ghost-dark" href="secteurs.html">Tous les secteurs</a>
              </div>
            </div>
            <div class="col-lg-5">
              <div class="tl-card"><div class="body">
                <span class="tl-chip orange">Expertise terrain</span>
                <h3>Un cabinet qui parle votre usine</h3>
                <p>Un brief clair, une shortlist industrielle, un interlocuteur unique. Pas 40 CV à trier en fin de quart.</p>
                <a class="tl-btn" href="contact.html" style="margin-top:16px">Parler à un spécialiste</a>
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
    "Blog recrutement industriel, RH et manufacturier Québec | Talendus",
    "Articles SEO sur le recrutement manufacturier, la logistique, les entrepôts et les métiers spécialisés au Québec.",
    "blog.html",
    page_hero(
        "Blog", "Recrutement, RH, usine, logistique et carrière.",
        "Des textes utiles pour employeurs industriels et candidats d'usine — sans langue de bois.",
        actions='<a class="tl-btn" href="contact.html">Réserver une consultation gratuite</a>',
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
          <h2>Ce que nous observons au Québec</h2>
          <p>Les usines et centres de distribution n'embauchent pas comme un siège de services. Les quarts, la SST, les cartes de compétences et la culture de plancher pèsent autant que le CV. Un poste vacant de 6 semaines coûte souvent plus cher qu'un mandat de recrutement bien cadré.</p>
          <h2>Pistes concrètes</h2>
          <ul>
            <li>Clarifier le quart, la rémunération réelle et les bonus avant d'approcher le marché.</li>
            <li>Évaluer le savoir-faire (démonstration, mises en situation) plutôt que les seuls diplômes.</li>
            <li>Prévoir l'accueil 30/60/90 jours : c'est là que se joue la rétention.</li>
          </ul>
          <h2>Comment Talendus intervient</h2>
          <p>Nous ciblons des profils industriels, validons le fit de quart et présentons peu de dossiers, mais des dossiers défendables.</p>
          <p><a href="recrutement-industriel.html">Recrutement industriel</a> · <a href="emplois.html">Offres d'emploi</a> · <a href="entreprises.html">Solutions entreprises</a></p>
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
    page_hero("404", "Cette page n'existe pas.", "Le mandat, lui, existe peut-être encore.",
              actions='<a class="tl-btn" href="index.html">Retour à l\'accueil</a><a class="tl-btn tl-btn-ghost" href="contact.html">Réserver une consultation</a>',
              badges="")
    + '<section class="tl-section"><div class="container"><p class="tl-lead">Vérifiez l\'URL ou reprenez depuis l\'accueil, les offres ou le formulaire de consultation.</p></div></section>',
    robots="noindex,nofollow",
))
write("espace.html", wrap(
    "Mon espace candidat | Talendus",
    "Connectez-vous pour gérer votre profil, votre CV, vos candidatures et vos notifications Talendus.",
    "espace.html",
    page_hero(
        "Candidats", "Votre dossier Talendus.",
        "Profil, CV, candidatures, correspondances, messages et entretiens — le suivi de votre recherche d'emploi industriel.",
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
        "Offres, candidatures reçues, pipeline et factures — le suivi de vos mandats industriels.",
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
    page_hero("Légal", "Conditions d'utilisation", "Le site talendus.ca présente les services du cabinet Talendus.", badges="")
    + """<section class="tl-section"><div class="container" style="max-width:800px"><p>Le contenu est fourni à titre informatif. Les mandats font l'objet d'une entente écrite. Les exemples d'offres et statistiques de démonstration peuvent être ajustés selon les données réelles du cabinet.</p><p>L'utilisation du site implique l'acceptation de ces conditions. Pour toute question : info@talendus.ca.</p></div></section>"""
))

for old, new in [("about.html", "a-propos.html"), ("service.html", "services.html"), ("blog-single.html", "blog.html")]:
    write(old, wrap("Redirection | Talendus", "Redirection.", old,
                    f'<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="{new}">Continuer</a></p><script>location.replace("{new}");</script></div></section>',
                    robots="noindex,nofollow"))

write_seo_fr(write, wrap, page_hero, CTA_BAND)
build_en(write, wrap, page_hero)

fr_urls = [("", "en/")]
pairs = [
    ("a-propos.html", "en/about.html"),
    ("services.html", "en/services.html"),
    ("entreprises.html", "en/employers.html"),
    ("candidats.html", "en/candidates.html"),
    ("emplois.html", "en/jobs.html"),
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
