"""Positionnement multisectoriel Talendus — contenus partagés FR/EN.

Talendus n'est pas une plateforme de recrutement pour une industrie.
Talendus est une plateforme de recrutement pour les entreprises.

L'IA n'est pas encore développée : les emplacements ci-dessous sont conceptuels
et portent la mention « Bientôt disponible » — jamais de faux résultats.
"""

# Pages SEO sectorielles à accueillir plus tard (ne pas générer de pages vides).
FUTURE_SEO_SECTOR_PAGES = (
    "recrutement-construction",
    "recrutement-informatique",
    "recrutement-sante",
    "recrutement-finance",
    "recrutement-logistique",
    "recrutement-manufacturier",
    "recrutement-commerce",
    "recrutement-education",
    "recrutement-hotellerie",
    "recrutement-immobilier",
)

SECTOR_EXAMPLES = {
    "fr": [
        ("technologie", "Technologie et informatique"),
        ("construction", "Construction"),
        ("manufacturier", "Manufacturier"),
        ("transport", "Transport et logistique"),
        ("commerce", "Commerce et vente au détail"),
        ("finance", "Finance"),
        ("assurance", "Assurance"),
        ("sante", "Santé"),
        ("education", "Éducation"),
        ("hotellerie", "Hôtellerie et restauration"),
        ("immobilier", "Immobilier"),
        ("services-pro", "Services professionnels"),
        ("marketing", "Marketing et communication"),
        ("ingenierie", "Ingénierie"),
        ("administration", "Administration"),
        ("agriculture", "Agriculture"),
        ("energie", "Énergie"),
        ("telecom", "Télécommunications"),
        ("services-entreprises", "Services aux entreprises"),
    ],
    "en": [
        ("technologie", "Technology and IT"),
        ("construction", "Construction"),
        ("manufacturier", "Manufacturing"),
        ("transport", "Transportation and logistics"),
        ("commerce", "Retail and commerce"),
        ("finance", "Finance"),
        ("assurance", "Insurance"),
        ("sante", "Healthcare"),
        ("education", "Education"),
        ("hotellerie", "Hospitality"),
        ("immobilier", "Real estate"),
        ("services-pro", "Professional services"),
        ("marketing", "Marketing and communications"),
        ("ingenierie", "Engineering"),
        ("administration", "Administration"),
        ("agriculture", "Agriculture"),
        ("energie", "Energy"),
        ("telecom", "Telecommunications"),
        ("services-entreprises", "Business services"),
    ],
}

TRADE_EXAMPLES = {
    "fr": [
        "Développeur", "Comptable", "Ingénieur", "Chauffeur", "Cariste", "Soudeur",
        "Technicien", "Infirmier", "Vendeur", "Responsable RH", "Gestionnaire",
        "Marketing", "Administration", "Production", "Logistique", "Électromécanicien",
        "Machiniste", "Superviseur",
    ],
    "en": [
        "Developer", "Accountant", "Engineer", "Driver", "Forklift operator", "Welder",
        "Technician", "Nurse", "Sales associate", "HR manager", "Manager",
        "Marketing", "Administration", "Production", "Logistics", "Electromechanical technician",
        "Machinist", "Supervisor",
    ],
}

AI_FEATURES = {
    "fr": [
        ("Matching intelligent", "Relier un besoin de recrutement aux profils les plus pertinents."),
        ("Recommandation de candidats", "Suggérer des dossiers à examiner en priorité."),
        ("Analyse des CV", "Repérer l'expérience, les métiers et les compétences clés."),
        ("Analyse des compétences", "Comparer les compétences demandées et celles du profil."),
        ("Classement des candidats", "Ordonner une shortlist selon le besoin du poste."),
        ("Suggestions de profils", "Proposer des talents proches, même hors recherche active."),
        ("Aide à la rédaction des offres", "Clarifier un descriptif de poste à partir du besoin."),
        ("Identification des compétences", "Extraire ce qu'un poste exige vraiment."),
        ("Recommandations aux recruteurs", "Guider l'équipe Talendus dans le tri des dossiers."),
    ],
    "en": [
        ("Intelligent matching", "Connect a hiring need to the most relevant profiles."),
        ("Candidate recommendations", "Surface files worth reviewing first."),
        ("Resume analysis", "Spot experience, roles and key skills."),
        ("Skills analysis", "Compare required skills with a profile."),
        ("Candidate ranking", "Order a shortlist against the role."),
        ("Profile suggestions", "Propose nearby talent, even if they are not actively looking."),
        ("Job-ad writing help", "Clarify a posting from the hiring need."),
        ("Skill identification", "Extract what a role actually requires."),
        ("Recruiter recommendations", "Guide the Talendus team when screening files."),
    ],
}

PROBLEMS = {
    "fr": [
        ("Trouver les bons candidats", "Le vivier est large. Les profils vraiment pertinents le sont moins."),
        ("Manque de temps", "Le recrutement s'ajoute au quotidien. Les semaines passent."),
        ("Trop de candidatures", "Trier des dizaines de CV n'est pas un processus. C'est du bruit."),
        ("Identifier les profils pertinents", "Un titre de poste ne dit pas si la personne tiendra vraiment le rôle."),
        ("Un processus trop long", "Chaque jour vacant coûte. Chaque mauvaise embauche coûte davantage."),
        ("Peu de visibilité", "Les talents disponibles — y compris déjà en poste — restent souvent hors radar."),
    ],
    "en": [
        ("Finding the right people", "The pool is large. Truly relevant profiles are not."),
        ("Not enough time", "Hiring sits on top of the day job. Weeks slip by."),
        ("Too many applications", "Sorting dozens of resumes is not a process. It is noise."),
        ("Spotting a real fit", "A job title does not tell you if someone will actually hold the role."),
        ("A process that drags", "Every vacant day costs. A bad hire costs more."),
        ("Little visibility", "Available talent — including people already in a job — often stays off the radar."),
    ],
}


def _options(pairs, empty_label):
    opts = [f'<option value="">{empty_label}</option>']
    for value, label in pairs:
        opts.append(f'<option value="{value}">{label}</option>')
    return "".join(opts)


def sectors_cloud(lang="fr"):
    more = "Et bien plus encore" if lang == "fr" else "And many more"
    close = (
        "Quel que soit votre secteur, Talendus vous aide à trouver les bons talents."
        if lang == "fr"
        else "Whatever your industry, Talendus helps you find the right talent."
    )
    kicker = "Tous les secteurs" if lang == "fr" else "Every industry"
    heading = (
        "Talendus s'adresse à toutes les industries."
        if lang == "fr"
        else "Talendus is built for every industry."
    )
    lead = (
        "Ces secteurs sont des exemples. Ils ne limitent pas la plateforme."
        if lang == "fr"
        else "These industries are examples. They do not limit the platform."
    )
    chips = "".join(
        f'<li><span class="tl-sector-chip">{name}</span></li>'
        for _slug, name in SECTOR_EXAMPLES[lang]
    )
    chips += f'<li><span class="tl-sector-chip is-more">{more}</span></li>'
    return f"""
<section class="tl-section" id="secteurs">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <ul class="tl-sectors-cloud">{chips}</ul>
    <p class="tl-center tl-muted" style="margin-top:22px;max-width:640px;margin-left:auto;margin-right:auto">{close}</p>
  </div>
</section>
"""


def trades_cloud(lang="fr"):
    kicker = "Métiers" if lang == "fr" else "Roles"
    heading = (
        "Une grande variété de profils, pas un catalogue fermé."
        if lang == "fr"
        else "A wide range of roles, not a closed catalogue."
    )
    lead = (
        "Développeur, comptable, soudeur, infirmier, chauffeur : Talendus peut accompagner le recrutement de ces métiers — et de bien d'autres."
        if lang == "fr"
        else "Developer, accountant, welder, nurse, driver: Talendus can help hire these roles — and many others."
    )
    chips = "".join(f'<li><span class="tl-trade-chip">{name}</span></li>' for name in TRADE_EXAMPLES[lang])
    return f"""
<section class="tl-section tl-ice" id="metiers">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <ul class="tl-trades-cloud">{chips}</ul>
  </div>
</section>
"""


def problems_section(lang="fr"):
    kicker = "Le recrutement" if lang == "fr" else "Hiring"
    heading = (
        "Le problème, ce n'est pas votre secteur. C'est de recruter juste."
        if lang == "fr"
        else "The problem is not your industry. It is hiring well."
    )
    lead = (
        "Nous aidons les entreprises de tous secteurs à recruter les bons talents."
        if lang == "fr"
        else "We help companies in every industry hire the right people."
    )
    cards = "".join(
        f'<div class="tl-card"><div class="body"><h3>{title}</h3><p>{text}</p></div></div>'
        for title, text in PROBLEMS[lang]
    )
    return f"""
<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-grid-3">{cards}</div>
  </div>
</section>
"""


def ai_coming_soon(lang="fr"):
    kicker = "Direction technologique" if lang == "fr" else "Product direction"
    heading = (
        "L'IA, bientôt. Le recrutement, déjà."
        if lang == "fr"
        else "AI, soon. Recruiting, already."
    )
    lead = (
        "Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA — c'est la direction de la plateforme. Ces outils ne sont pas encore disponibles. Aucun score, matching ou analyse n'est simulé."
        if lang == "fr"
        else "We hire better, faster and more intelligently with AI — that is the product direction. These tools are not available yet. No scores, matching or analysis are simulated."
    )
    soon = "Bientôt disponible" if lang == "fr" else "Coming soon"
    cards = "".join(
        f'<div class="tl-card tl-ai-soon"><div class="body"><span class="tl-chip">{soon}</span><h3>{title}</h3><p>{text}</p></div></div>'
        for title, text in AI_FEATURES[lang]
    )
    return f"""
<section class="tl-section" id="ia">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-grid-3">{cards}</div>
  </div>
</section>
"""


def human_hire_band(lang="fr"):
    if lang == "en":
        return """
<section class="tl-cta-band" id="mandat">
  <div class="container">
    <span class="tl-badge tl-badge-light">Talk to a recruiter</span>
    <h2 class="tl-h2">Have a hiring need? Tell us about the role.</h2>
    <p>Whatever your industry, you can also hand the search to Talendus. Sector, role, headcount, location, contract type — we take it from there.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Talk to a recruiter</a>
      <a class="tl-btn tl-btn-ghost" href="post-a-job.html">Post a job</a>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-cta-band" id="mandat">
  <div class="container">
    <span class="tl-badge tl-badge-light">Parler à un recruteur</span>
    <h2 class="tl-h2">Vous avez un besoin de recrutement ? Parlez-nous de votre poste.</h2>
    <p>Quel que soit votre secteur, vous pouvez aussi confier le recrutement à Talendus. Secteur, poste, nombre de personnes, localisation, type de contrat : on s'en occupe.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Parler à un recruteur</a>
      <a class="tl-btn tl-btn-ghost" href="publier-une-offre.html">Publier une offre</a>
    </div>
  </div>
</section>
"""


def employer_need_fields(lang="fr"):
    """Champs du formulaire entreprise : secteur, poste, volume, localisation, contrat, besoins."""
    if lang == "en":
        sectors = _options(SECTOR_EXAMPLES["en"], "Select an industry")
        sectors += '<option value="autre">Other / several industries</option>'
        contracts = """
            <option value="">Select</option>
            <option>Full-time</option>
            <option>Part-time</option>
            <option>Temporary</option>
            <option>Contract</option>
            <option>Internship</option>
            <option>Several contract types</option>
        """
        return f"""
            <label>Industry</label>
            <select name="secteur">{sectors}</select>
            <label>Role to fill</label>
            <input name="poste" placeholder="e.g. accountant, developer, nurse, welder">
            <label>Number of hires</label>
            <input name="volume" type="number" min="1" value="1">
            <label>Location</label>
            <input name="localisation" placeholder="City, region, country or remote">
            <label>Contract type</label>
            <select name="contrat">{contracts}</select>
            <label>Particular needs</label>
            <textarea name="message" required placeholder="Urgency, must-have skills, schedule, anything we should know"></textarea>
        """
    sectors = _options(SECTOR_EXAMPLES["fr"], "Choisir un secteur")
    sectors += '<option value="autre">Autre / plusieurs secteurs</option>'
    contracts = """
            <option value="">Choisir</option>
            <option>Temps plein</option>
            <option>Temps partiel</option>
            <option>Temporaire</option>
            <option>Contractuel</option>
            <option>Stage</option>
            <option>Plusieurs types de contrat</option>
        """
    return f"""
            <label>Secteur</label>
            <select name="secteur">{sectors}</select>
            <label>Poste recherché</label>
            <input name="poste" placeholder="ex. comptable, développeur, infirmier, soudeur">
            <label>Nombre de personnes à recruter</label>
            <input name="volume" type="number" min="1" value="1">
            <label>Localisation</label>
            <input name="localisation" placeholder="Ville, région, pays ou télétravail">
            <label>Type de contrat</label>
            <select name="contrat">{contracts}</select>
            <label>Besoins particuliers</label>
            <textarea name="message" required placeholder="Urgence, compétences indispensables, horaire, tout ce qu'on doit savoir"></textarea>
        """


def job_search_filters(lang="fr"):
    """Filtres de recherche : secteur, métier, compétences, expérience, localisation, type d'emploi."""
    if lang == "en":
        sectors = _options(SECTOR_EXAMPLES["en"], "All industries")
        types = """
          <option value="">All job types</option>
          <option value="Permanent">Full-time / permanent</option>
          <option value="Part-time">Part-time</option>
          <option value="Temporary">Temporary</option>
          <option value="Contract">Contract</option>
          <option value="Internship">Internship</option>
        """
        return f"""
      <div class="tl-filters tl-filters-search" data-ai-ready="true">
        <label class="tl-filter">
          <span>Role or skills</span>
          <input id="job-search" placeholder="Developer, Excel, welding, project management…">
        </label>
        <label class="tl-filter">
          <span>Industry</span>
          <select id="job-sector">{sectors}</select>
        </label>
        <label class="tl-filter">
          <span>Location</span>
          <select id="job-city">
            <option value="">Anywhere</option>
            <option>Laval</option><option>Longueuil</option><option>Montreal</option>
            <option>Drummondville</option><option>Saint-Jérôme</option>
            <option>Sherbrooke</option><option>Boucherville</option>
            <option>Anjou</option><option>Trois-Rivières</option><option>Quebec City</option>
            <option value="remote">Remote</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Job type</span>
          <select id="job-type">{types}</select>
        </label>
        <label class="tl-filter">
          <span>Experience</span>
          <select id="job-exp">
            <option value="">Any experience</option>
            <option value="debutant">Entry-level</option>
            <option value="intermediaire">Mid-level</option>
            <option value="senior">Senior</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Category</span>
          <select id="job-cat">
            <option value="">All categories</option>
            <option value="technologie">Technology</option>
            <option value="production">Production</option>
            <option value="entrepot">Warehouse</option>
            <option value="logistique">Logistics</option>
            <option value="maintenance">Maintenance</option>
            <option value="finance">Finance</option>
            <option value="sante">Healthcare</option>
            <option value="commerce">Retail</option>
            <option value="ingenierie">Engineering</option>
            <option value="administration">Administration</option>
            <option value="marketing">Marketing</option>
            <option value="transport">Transportation</option>
            <option value="supervision">Supervision</option>
            <option value="cadres">Leadership</option>
          </select>
        </label>
      </div>
      <p class="tl-muted tl-ai-hint">Filters are ready for a future matching layer. Intelligent ranking is coming soon — it is not active yet.</p>
"""
    sectors = _options(SECTOR_EXAMPLES["fr"], "Tous les secteurs")
    types = """
          <option value="">Tous les types d'emploi</option>
          <option value="Permanent">Temps plein / permanent</option>
          <option value="Partiel">Temps partiel</option>
          <option value="Temporaire">Temporaire</option>
          <option value="Contractuel">Contractuel</option>
          <option value="Stage">Stage</option>
        """
    return f"""
      <div class="tl-filters tl-filters-search" data-ai-ready="true">
        <label class="tl-filter">
          <span>Métier ou compétences</span>
          <input id="job-search" placeholder="Développeur, Excel, soudure, gestion de projet…">
        </label>
        <label class="tl-filter">
          <span>Secteur</span>
          <select id="job-sector">{sectors}</select>
        </label>
        <label class="tl-filter">
          <span>Localisation</span>
          <select id="job-city">
            <option value="">Toutes les localisations</option>
            <option>Laval</option><option>Longueuil</option><option>Montréal</option>
            <option>Drummondville</option><option>Saint-Jérôme</option>
            <option>Sherbrooke</option><option>Boucherville</option>
            <option>Anjou</option><option>Trois-Rivières</option><option>Québec</option>
            <option value="remote">Télétravail</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Type d'emploi</span>
          <select id="job-type">{types}</select>
        </label>
        <label class="tl-filter">
          <span>Expérience</span>
          <select id="job-exp">
            <option value="">Toute expérience</option>
            <option value="debutant">Débutant</option>
            <option value="intermediaire">Intermédiaire</option>
            <option value="senior">Senior</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Catégorie</span>
          <select id="job-cat">
            <option value="">Toutes les catégories</option>
            <option value="technologie">Technologie</option>
            <option value="production">Production</option>
            <option value="entrepot">Entrepôt</option>
            <option value="logistique">Logistique</option>
            <option value="maintenance">Maintenance</option>
            <option value="finance">Finance</option>
            <option value="sante">Santé</option>
            <option value="commerce">Commerce</option>
            <option value="ingenierie">Ingénierie</option>
            <option value="administration">Administration</option>
            <option value="marketing">Marketing</option>
            <option value="transport">Transport</option>
            <option value="supervision">Supervision</option>
            <option value="cadres">Cadres</option>
          </select>
        </label>
      </div>
      <p class="tl-muted tl-ai-hint">Ces filtres pourront accueillir plus tard une couche de matching. Le classement intelligent n'est pas encore actif — bientôt disponible.</p>
"""


def homepage_after_hero(lang="fr"):
    return (
        problems_section(lang)
        + sectors_cloud(lang)
        + trades_cloud(lang)
        + ai_coming_soon(lang)
        + human_hire_band(lang)
    )


def talent_trade_options(lang="fr"):
    if lang == "en":
        names = TRADE_EXAMPLES["en"] + ["Other"]
    else:
        names = TRADE_EXAMPLES["fr"] + ["Autre"]
    return "".join(f"<option>{n}</option>" for n in names)
