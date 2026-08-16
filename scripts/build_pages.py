#!/usr/bin/env python3
"""Génère les pages piliers Talendus à partir du header/footer partagés."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parts import head, header, FOOTER, page_hero

ROOT = Path("/workspace")

def wrap(title, desc, slug, body, solid=True):
    return head(title, desc, slug) + header(solid) + body + FOOTER

def write(name, html):
    (ROOT / name).write_text(html, encoding="utf-8")
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


def simple_page(title, desc, slug, kicker, h1, lead, inner):
    body = page_hero(kicker, h1, lead) + f'<section class="tl-section"><div class="container">{inner}</div></section>'
    write(slug, wrap(title, desc, slug, body))


# À propos
simple_page(
    "À propos de Talendus | Cabinet de recrutement industriel Québec",
    "Histoire, mission, vision et valeurs de Talendus, cabinet exclusivement dédié au recrutement manufacturier, logistique et d'entrepôt au Québec.",
    "a-propos.html", "Le cabinet", "Talendus existe pour une seule industrie : la vôtre.",
    "Nous recrutons exclusivement pour les usines, entrepôts et entreprises manufacturières du Québec.",
    """
    <div class="row"><div class="col-lg-7">
    <h2 class="tl-h2">Histoire</h2>
    <p class="tl-lead">Talendus est né d'un constat simple : trop d'usines québécoises perdent des semaines avec des agences généralistes qui ne distinguent pas un set-up CNC d'un poste de bureau. Nous avons bâti un cabinet qui ne parle qu'usine, quart, SST et performance de ligne.</p>
    <h2 class="tl-h2">Mission</h2>
    <p>Connecter durablement les employeurs industriels du Québec aux talents qui font tourner la production — opérateurs, métiers spécialisés, superviseurs et cadres d'usine.</p>
    <h2 class="tl-h2">Vision</h2>
    <p>Devenir la référence du recrutement industriel au Québec : le premier appel quand une usine doit embaucher juste, et vite.</p>
    <h2 class="tl-h2">Valeurs</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Spécialisation</h3><p>Aucun mandat hors industrie. C'est notre filtre, et votre garantie.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Rigueur terrain</h3><p>Nous évaluons comme un contremaître, pas comme un algorithme.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Parole tenue</h3><p>Délais, dossiers, garantie : ce qui est dit est livré.</p></div></div>
    </div>
    <h2 class="tl-h2">Pourquoi l'industrie manufacturière</h2>
    <p>C'est là que le Québec crée de la valeur réelle. C'est aussi là que la pénurie de métiers se fait le plus sentir. Nous avons choisi ce champ — et seulement celui-là.</p>
    <h2 class="tl-h2">Nos engagements</h2>
    <ul><li>Présélection industrielle avant toute présentation.</li><li>Transparence sur les délais et la rareté du profil.</li><li>Suivi d'intégration 30/60/90 jours.</li><li>Garantie de remplacement sur les mandats permanents.</li></ul>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="assets/img/all-images/industry/usine-equipe.jpg" alt="Équipe Talendus sur le plancher d'usine">
      </div>
      <a class="tl-btn" href="contact.html">Discuter d'un mandat</a>
    </div></div>
    """
)

# Services
services_inner = "".join(
    f'<div class="tl-card" style="margin-bottom:16px"><div class="body"><h2>{t}</h2><p>{p}</p></div></div>'
    for t, p in [
        ("Recrutement permanent", "Mandats de postes stables en usine, entrepôt et gestion manufacturière. Honoraires au succès, garantie de remplacement."),
        ("Chasse de têtes", "Approche directe de candidats passifs pour les profils rares : CNC, électromécanique, cadres d'usine."),
        ("Recrutement de cadres", "Directeurs d'usine, de production, de maintenance et de logistique. Mandats souvent confidentiels."),
        ("Recrutement de superviseurs", "Contremaîtres et superviseurs de quart capables de tenir KPI, SST et climat d'équipe."),
        ("Métiers spécialisés", "Soudeurs, machinistes, mécaniciens industriels, électromécaniciens, set-up, qualité."),
        ("Recrutement urgent", "Processus accéléré quand un quart critique est découvert. Premiers profils en quelques jours."),
        ("Mandats confidentiels", "Remplacements de cadres ou réorganisations menés sans bruit interne."),
        ("Accompagnement RH", "Descriptifs de poste, grilles salariales industrielles, entrevues conjointes et intégration."),
    ]
)
simple_page(
    "Services de recrutement industriel | Talendus Québec",
    "Recrutement permanent, chasse de têtes, cadres, superviseurs, métiers spécialisés, mandats urgents et confidentiels pour les usines du Québec.",
    "services.html", "Services", "Des services pensés pour l'usine, pas pour un siège social.",
    "Du journalier au directeur de plant : un seul cabinet, une seule industrie.",
    services_inner + '<div class="space32"></div><a class="tl-btn" href="contact.html">Demander une consultation</a>'
)

# Employeurs
write("employeurs.html", wrap(
    "Employeurs | Recrutement manufacturier et industriel au Québec — Talendus",
    "Pourquoi les usines et entrepôts du Québec choisissent Talendus : processus, garanties, délais et consultation gratuite.",
    "employeurs.html",
    page_hero("Employeurs", "Votre usine n'a pas besoin de 80 CV. Elle a besoin du bon quart, au bon moment.",
              "Consultation gratuite. Présélection industrielle. Garantie de remplacement.")
    + """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Pourquoi Talendus</h3><p>Spécialisation exclusive, réseau passif d'usine, évaluation technique et suivi d'intégration.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Délais moyens</h3><p>7 à 21 jours pour les métiers d'opération. 3 à 8 semaines pour superviseurs, métiers rares et cadres.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Garanties</h3><p>Remplacement inclus sur les mandats permanents. Conditions confirmées à l'ouverture du dossier.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section tl-ice" id="calculateur"><div class="container">
      <div class="row align-items-center">
        <div class="col-lg-5"><h2 class="tl-h2">Calculateur : coût d'une mauvaise embauche</h2>
        <p class="tl-lead">Estimez l'impact d'un mauvais fit (salaire, formation, heures sup. et perte de productivité).</p></div>
        <div class="col-lg-6 offset-lg-1">
          <div class="tl-calc">
            <label>Salaire annuel du poste ($)</label>
            <input id="tl-salary" type="number" value="55000">
            <label>Mois avant que le problème soit visible</label>
            <input id="tl-months" type="number" value="4">
            <div class="tl-calc-result">Coût estimé<br><b id="tl-cost">—</b></div>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section"><div class="container tl-faq">
      <h2 class="tl-h2">FAQ employeurs</h2>
      <details open><summary>Comment facturez-vous ?</summary><p>Honoraires au succès, calculés sur le salaire annuel du candidat placé. Aucun frais si le mandat n'aboutit pas, selon les conditions de l'entente.</p></details>
      <details><summary>Travaillez-vous en région ?</summary><p>Oui. Outre le Grand Montréal, nous menons des mandats en Montérégie, Estrie, Centre-du-Québec, Mauricie et région de Québec.</p></details>
      <div class="space32"></div>
      <a class="tl-btn" href="contact.html">Réserver une consultation gratuite</a>
    </div></section>
    """
))

# Candidats
write("candidats.html", wrap(
    "Candidats | Emplois usine, entrepôt et métiers spécialisés au Québec — Talendus",
    "Déposez votre CV chez Talendus. Offres en usine, entrepôt, logistique, maintenance et supervision au Québec.",
    "candidats.html",
    page_hero("Candidats", "Des postes d'usine et d'entrepôt, présentés clairement.",
              "Nous travaillons avec des employeurs manufacturiers du Québec — pas des mandats fourre-tout.")
    + """
    <section class="tl-section" id="cv"><div class="container">
      <div class="row">
        <div class="col-lg-5">
          <h2 class="tl-h2">Déposer votre CV</h2>
          <p class="tl-lead">Indiquez votre métier, vos quarts possibles et votre région. Un conseiller vous rejoint si un mandat correspond.</p>
          <p id="processus"></p>
          <h3>Notre processus candidat</h3>
          <ol>
            <li>Réception et qualification de votre profil.</li>
            <li>Entrevue Talendus (compétences, quarts, mobilité).</li>
            <li>Présentation aux employeurs industriels pertinents.</li>
            <li>Préparation à l'entrevue d'usine.</li>
            <li>Suivi jusqu'à la prise de poste.</li>
          </ol>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post">
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
            <button class="tl-btn" type="submit">Envoyer ma candidature</button>
            <div class="tl-success" role="status"></div>
          </form>
        </div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <h2 class="tl-h2">Conseils carrière</h2>
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Préparer une entrevue d'usine</h3><p>Exemples de pannes, SST, travail d'équipe de quart : ce que les contremaîtres écoutent vraiment.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Mettre en valeur vos cartes</h3><p>Chariot, espace clos, cadenassage, soudure : listez-les en tête de CV.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Voir les offres</h3><p><a href="emplois.html">Consultez les postes ouverts</a> ou laissez-nous vous approcher pour un mandat confidentiel.</p></div></div>
      </div>
    </div></section>
    """
))

# Contact
write("contact.html", wrap(
    "Contact | Consultation recrutement industriel Québec — Talendus",
    "Contactez Talendus à Montréal : consultation gratuite, recrutement usine, entrepôt et manufacturier au Québec. 514 555-0199 · info@talendus.ca",
    "contact.html",
    page_hero("Contact", "Consultation gratuite pour votre prochain mandat industriel.",
              "Téléphone, courriel ou formulaire. Adresse affichée configurable selon votre bureau.")
    + """
    <section class="tl-section"><div class="container">
      <div class="row">
        <div class="col-lg-5">
          <h2 class="tl-h2">Nous joindre</h2>
          <p><strong>Téléphone :</strong> <a href="tel:+15145550199">514 555-0199</a><br>
          <strong>Courriel :</strong> <a href="mailto:info@talendus.ca">info@talendus.ca</a><br>
          <strong>Adresse :</strong> Montréal (Québec) — adresse de bureau configurable.</p>
          <div class="tl-hero-media" style="height:280px;border-radius:16px;overflow:hidden;margin-top:18px">
            <iframe title="Carte Montréal" src="https://maps.google.com/maps?q=Montréal%20Québec&t=&z=11&ie=UTF8&iwloc=&output=embed" width="100%" height="280" style="border:0" loading="lazy"></iframe>
          </div>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post">
            <label>Nom</label><input required>
            <label>Entreprise (optionnel)</label><input>
            <label>Courriel</label><input type="email" required>
            <label>Téléphone</label><input>
            <label>Objet</label>
            <select><option>Mandat de recrutement</option><option>Candidature</option><option>Consultation</option></select>
            <label>Message</label><textarea required></textarea>
            <button class="tl-btn" type="submit">Demander une consultation</button>
            <div class="tl-success"></div>
          </form>
        </div>
      </div>
    </div></section>
    """
))

# Emplois listing
cards = []
for slug, title, city, cat, typ, sal, shift, req in JOBS:
    cards.append(f'''
    <article class="tl-job-card" data-job="{title} {city} {cat} {typ}">
      <div class="body">
        <span class="tl-chip orange">{typ}</span><span class="tl-chip">{city}</span>
        <h3><a href="emploi-{slug}.html">{title}</a></h3>
        <p>{sal} · {shift}</p>
        <a href="emploi-{slug}.html">Voir le poste</a>
      </div>
    </article>''')
write("emplois.html", wrap(
    "Offres d'emploi usine et entrepôt au Québec | Talendus",
    "Postes de cariste, opérateur, soudeur, machiniste CNC, électromécanicien, superviseur et directeur d'usine au Québec.",
    "emplois.html",
    page_hero("Offres d'emploi", "Postes industriels ouverts au Québec",
              "Filtrez par métier, catégorie et ville. Candidature en un formulaire.")
    + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-filters">
        <input id="job-search" placeholder="Rechercher un métier">
        <select id="job-cat">
          <option value="">Toutes les catégories</option>
          <option value="production">Production</option>
          <option value="entrepot">Entrepôt</option>
          <option value="maintenance">Maintenance</option>
          <option value="supervision">Supervision</option>
          <option value="cadres">Cadres</option>
        </select>
        <select id="job-city">
          <option value="">Toutes les villes</option>
          <option>Laval</option><option>Longueuil</option><option>Montréal</option>
          <option>Drummondville</option><option>Québec</option>
        </select>
      </div>
      <div class="tl-grid-3">{''.join(cards)}</div>
    </div></section>
    """
))

for slug, title, city, cat, typ, sal, shift, req in JOBS:
    write(f"emploi-{slug}.html", wrap(
        f"{title} à {city} | Emploi industriel Québec — Talendus",
        f"Poste de {title} à {city}, Québec. {typ}. Postulez via Talendus, cabinet de recrutement industriel.",
        f"emploi-{slug}.html",
        page_hero(f"{city} · {typ}", title, f"{sal} · {shift} · Recrutement industriel Talendus")
        + f"""
        <section class="tl-section"><div class="container">
          <div class="row">
            <div class="col-lg-7">
              <h2 class="tl-h2">Le poste</h2>
              <p class="tl-lead">Talendus recrute un(e) {title.lower()} pour un employeur manufacturier / logistique à {city}. Environnement d'usine, exigences SST et rythme de production réels.</p>
              <h3>Profil recherché</h3>
              <p>{req}</p>
              <h3>Ce que nous offrons</h3>
              <ul><li>Poste {typ.lower()}</li><li>Rémunération : {sal}</li><li>Horaire : {shift}</li><li>Accompagnement Talendus jusqu'à l'embauche</li></ul>
              <p><a href="emplois.html">← Toutes les offres</a></p>
            </div>
            <div class="col-lg-4 offset-lg-1">
              <h3>Postuler</h3>
              <form class="tl-form"><label>Nom</label><input required>
              <label>Courriel</label><input type="email" required>
              <label>Téléphone</label><input>
              <label>Lien CV</label><input placeholder="https://">
              <button class="tl-btn" type="submit">Envoyer ma candidature</button>
              <div class="tl-success"></div></form>
            </div>
          </div>
        </div></section>
        """
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
    page_hero("Secteurs", "Une expertise par type d'usine, pas un discours générique.",
              "Choisissez votre industrie. Nous parlons déjà votre langage opérationnel.")
    + f'<section class="tl-section"><div class="container"><div class="tl-grid-3">{sec_cards}</div></div></section>'
))
for slug, name, title, desc in SECTORS:
    write(f"secteur-{slug}.html", wrap(
        f"{title} | Talendus",
        desc,
        f"secteur-{slug}.html",
        page_hero("Secteur", name, desc)
        + f"""
        <section class="tl-section"><div class="container">
          <p class="tl-lead">{desc} Talendus n'envoie pas de profils de bureau : uniquement des talents qui ont déjà vécu un plancher d'usine ou un quai de réception.</p>
          <h2 class="tl-h2">Métiers typiques</h2>
          <p>Opération, métiers spécialisés, supervision et cadres selon la taille de votre site.</p>
          <a class="tl-btn" href="contact.html">Ouvrir un mandat {name.lower()}</a>
          <a href="secteurs.html" style="margin-left:12px">Tous les secteurs</a>
        </div></section>
        """
    ))

# Blog
art_cards = "".join(
    f'<a class="tl-card" href="article-{s}.html"><div class="tl-hero-media" style="height:180px"><img src="assets/img/all-images/industry/{img}" alt=""></div><div class="body"><span class="tl-chip">{cat}</span><h3>{t}</h3></div></a>'
    for s, t, cat, img, lead in ARTICLES
)
topics = "".join(f"<li>{t}</li>" for t in TOPICS)
write("blog.html", wrap(
    "Blog recrutement industriel, RH et manufacturier Québec | Talendus",
    "Articles SEO sur le recrutement manufacturier, la logistique, les entrepôts et les métiers spécialisés au Québec.",
    "blog.html",
    page_hero("Blog", "Recrutement, RH, usine, logistique et carrière.",
              "Des textes utiles pour employeurs industriels et candidats d'usine.")
    + f'<section class="tl-section"><div class="container"><div class="tl-grid-3">{art_cards}</div><h2 class="tl-h2" style="margin-top:48px">20 sujets SEO à venir</h2><ul>{topics}</ul></div></section>'
))
for slug, title, cat, img, lead in ARTICLES:
    write(f"article-{slug}.html", wrap(
        f"{title} | Blog Talendus",
        lead,
        f"article-{slug}.html",
        page_hero(cat, title, lead)
        + f"""
        <section class="tl-section"><div class="container" style="max-width:800px">
          <img src="assets/img/all-images/industry/{img}" alt="" style="width:100%;border-radius:16px;margin-bottom:24px">
          <p class="tl-lead">{lead}</p>
          <h2>Ce que nous observons au Québec</h2>
          <p>Les usines et centres de distribution n'embauchent pas comme un siège de services. Les quarts, la SST, les cartes de compétences et la culture de plancher pèsent autant que le CV.</p>
          <h2>Pistes concrètes</h2>
          <ul>
            <li>Clarifier le quart, la rémunération réelle et les bonus avant d'approcher le marché.</li>
            <li>Évaluer le savoir-faire (démonstration, mises en situation) plutôt que les seuls diplômes.</li>
            <li>Prévoir l'accueil 30/60/90 jours : c'est là que se joue la rétention.</li>
          </ul>
          <h2>Comment Talendus intervient</h2>
          <p>Nous ciblons des profils industriels, validons le fit de quart et présentons peu de dossiers, mais des dossiers défendables. <a href="contact.html">Parlez-nous de votre mandat</a>.</p>
          <p><a href="blog.html">← Blog</a></p>
        </div></section>
        """
    ))

write("404.html", wrap(
    "Page introuvable | Talendus",
    "La page demandée n'existe pas. Retournez à l'accueil Talendus.",
    "404.html",
    page_hero("404", "Cette page n'existe pas.", "Le mandat, lui, existe peut-être encore.")
    + '<section class="tl-section"><div class="container"><a class="tl-btn" href="index.html">Retour à l\'accueil</a></div></section>'
))
write("confidentialite.html", wrap(
    "Politique de confidentialité | Talendus",
    "Politique de confidentialité de Talendus, talendus.ca.",
    "confidentialite.html",
    page_hero("Légal", "Politique de confidentialité", "Les CV et mandats sont traités de façon confidentielle.")
    + """<section class="tl-section"><div class="container"><p>Talendus collecte les informations nécessaires au recrutement (coordonnées, CV, description de poste). Elles ne sont pas vendues. Vous pouvez demander l'accès ou la suppression en écrivant à info@talendus.ca.</p></div></section>"""
))
write("conditions.html", wrap(
    "Conditions d'utilisation | Talendus",
    "Conditions d'utilisation du site talendus.ca.",
    "conditions.html",
    page_hero("Légal", "Conditions d'utilisation", "Le site talendus.ca présente les services du cabinet Talendus.")
    + """<section class="tl-section"><div class="container"><p>Le contenu est fourni à titre informatif. Les mandats font l'objet d'une entente écrite. Les exemples d'offres et statistiques de démonstration peuvent être ajustés selon les données réelles du cabinet.</p></div></section>"""
))

# Redirects from old English slugs
for old, new in [("about.html", "a-propos.html"), ("service.html", "services.html"), ("blog-single.html", "blog.html")]:
    write(old, wrap("Redirection | Talendus", "Redirection.", old,
                    f'<section class="tl-section"><div class="container"><p>Cette page a été déplacée. <a href="{new}">Continuer</a></p><script>location.replace("{new}");</script></div></section>'))

urls = ["", "a-propos.html", "services.html", "employeurs.html", "candidats.html", "emplois.html",
        "secteurs.html", "blog.html", "contact.html"] + [f"emploi-{s}.html" for s, *_ in JOBS] + [
        f"secteur-{s}.html" for s, *_ in SECTORS] + [f"article-{s}.html" for s, *_ in ARTICLES]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(f"  <url><loc>https://talendus.ca/{u}</loc></url>" for u in urls)
    + "\n</urlset>\n",
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://talendus.ca/sitemap.xml\n", encoding="utf-8")
print("done")
