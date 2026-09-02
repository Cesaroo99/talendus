"""Positionnement Talendus, agence de placement intelligente.

Talendus n'est pas un job board, ni un ATS, ni une marketplace de CV.
Talendus est une agence de placement : l'entreprise confie un besoin,
Talendus recherche, présélectionne et présente une shortlist qualifiée.
L'entreprise conserve la décision finale.

Talendus utilise déjà l'intelligence artificielle dans ses outils internes
de recrutement. L'IA n'est pas un logiciel vendu au client, ni une
fonctionnalité future : elle accélère la recherche, l'analyse et la
présélection au service des équipes Talendus. La qualification finale
reste humaine.
"""

HONEYPOT_INPUT = '<input class="tl-hp" name="website_url" tabindex="-1" autocomplete="off" aria-hidden="true">'
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
        "Cariste", "Soudeur", "Machiniste", "Électromécanicien", "Technicien", "Chauffeur",
        "Production", "Logistique", "Superviseur", "Ingénieur", "Développeur", "Comptable",
        "Infirmier", "Vendeur", "Responsable RH", "Gestionnaire", "Marketing", "Administration",
    ],
    "en": [
        "Forklift operator", "Welder", "Machinist", "Electromechanical technician", "Technician", "Driver",
        "Production", "Logistics", "Supervisor", "Engineer", "Developer", "Accountant",
        "Nurse", "Sales associate", "HR manager", "Manager", "Marketing", "Administration",
    ],
}

AI_FEATURE_GROUPS = {
    "fr": [
        (
            "Relier",
            "Trouver qui correspond vraiment au besoin.",
            [
                ("Matching intelligent", "Relier un besoin de recrutement aux profils les plus pertinents."),
                ("Recommandation de candidats", "Suggérer les dossiers à examiner en priorité."),
                ("Suggestions de profils", "Proposer des talents proches, y compris hors recherche active."),
            ],
        ),
        (
            "Lire",
            "Comprendre un parcours au-delà du titre.",
            [
                ("Analyse des CV", "Repérer l'expérience, les métiers et les compétences clés."),
                ("Analyse des compétences", "Comparer ce que le poste exige et ce que le profil montre."),
                ("Identification des compétences", "Extraire ce qu'un poste demande vraiment."),
            ],
        ),
        (
            "Prioriser",
            "Aider l'équipe Talendus, pas remplacer le conseiller.",
            [
                ("Classement des candidats", "Ordonner une shortlist selon le besoin du poste."),
                ("Aide à la rédaction des offres", "Clarifier un descriptif à partir du besoin, sans inventer d'exigences."),
                ("Recommandations aux recruteurs", "Guider le tri interne. La qualification reste humaine."),
            ],
        ),
    ],
    "en": [
        (
            "Connect",
            "Find who actually fits the need.",
            [
                ("Intelligent matching", "Connect a hiring need to the most relevant profiles."),
                ("Candidate recommendations", "Suggest which files to review first."),
                ("Profile suggestions", "Propose nearby talent, including people not actively looking."),
            ],
        ),
        (
            "Read",
            "Understand a career beyond the title.",
            [
                ("Resume analysis", "Spot experience, occupations and key skills."),
                ("Skills analysis", "Compare what the role requires with what the profile shows."),
                ("Skills identification", "Extract what a role actually demands."),
            ],
        ),
        (
            "Prioritize",
            "Help the Talendus team, not replace the consultant.",
            [
                ("Candidate ranking", "Order a shortlist against the role."),
                ("Job-description support", "Clarify a posting from the need, without inventing requirements."),
                ("Recruiter recommendations", "Guide internal screening. Qualification stays human."),
            ],
        ),
    ],
}

PROBLEMS = {
    "fr": [
        ("Trouver les bons candidats", "Le vivier est large. Les profils vraiment pertinents le sont moins. Parcourir des CV n'est pas une stratégie."),
        ("Manque de temps", "Le recrutement s'ajoute au quotidien. Les semaines passent, le poste reste vacant."),
        ("Trop de candidatures", "Trier des dizaines de dossiers n'est pas un processus. C'est du bruit qui éloigne la décision."),
        ("Identifier les profils pertinents", "Un titre de poste ne dit pas si la personne tiendra vraiment le rôle."),
        ("Un processus trop long", "Chaque jour vacant coûte. Chaque mauvaise embauche coûte davantage."),
        ("Peu de visibilité", "Les talents disponibles (y compris déjà en poste) restent souvent hors radar."),
    ],
    "en": [
        ("Finding the right people", "The pool is large. Truly relevant profiles are not. Browsing resumes is not a strategy."),
        ("Not enough time", "Hiring sits on top of the day job. Weeks slip by and the seat stays empty."),
        ("Too many applications", "Sorting dozens of files is not a process. It is noise that delays the decision."),
        ("Spotting a real fit", "A job title does not tell you if someone will actually hold the role."),
        ("A process that drags", "Every vacant day costs. A bad hire costs more."),
        ("Little visibility", "Available talent (including people already in a job) often stays off the radar."),
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
        "Ces exemples n'enferment personne : un mandat ou un profil peut venir de n'importe quel secteur."
        if lang == "fr"
        else "These examples do not box anyone in: a mandate or a profile can come from any industry."
    )
    kicker = "Tous les secteurs" if lang == "fr" else "Every industry"
    heading = (
        "Tous les secteurs. Tous les métiers."
        if lang == "fr"
        else "Every industry. Every kind of role."
    )
    lead = (
        "Entreprises et talents : Talendus travaille dans tous les secteurs, sans spécialisation exclusive."
        if lang == "fr"
        else "Companies and talent: Talendus works across every industry, with no exclusive specialty."
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
        "Des métiers de tous les niveaux."
        if lang == "fr"
        else "Roles at every level."
    )
    lead = (
        "Opérationnel, spécialisé ou cadre : Talendus accompagne le poste à pourvoir et le parcours de la personne."
        if lang == "fr"
        else "Operational, specialist or leadership: Talendus supports both the open role and the person's path."
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
        "Le problème n'est pas de publier une offre. C'est de trouver les bons profils."
        if lang == "fr"
        else "The problem is not posting a job. It is finding the right people."
    )
    lead = (
        "Quand le recrutement reste sur votre bureau, il concurrence tout le reste. Talendus prend en charge la recherche et la présélection."
        if lang == "fr"
        else "When hiring stays on your desk, it competes with everything else. Talendus takes on the search and the shortlist."
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


def for_companies_section(lang="fr"):
    if lang == "en":
        return """
<section class="tl-section" id="entreprises-intro">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">For employers</div>
      <h2 class="tl-h2">A vacant seat costs every day. We take it on.</h2>
      <p>Talendus is a placement agency. You describe the need. A consultant searches, talks to people and brings you only those worth a meeting. You retain. Fees are due at the hire.</p>
      <p>This is not a board where you sort resumes, and not software to learn. It is a mandate: search, first conversation, shortlist, follow-through to start date. Many mandates stay confidential. Some openings are also posted on the site when that helps the search.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Hand us the search</a>
        <a class="tl-btn tl-btn-ghost-dark" href="employers.html">See how it works</a>
      </div>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section" id="entreprises-intro">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">Pour les entreprises</div>
      <h2 class="tl-h2">Un poste vacant coûte chaque jour. On le prend en charge.</h2>
      <p>Talendus est une agence de placement. Vous décrivez le besoin. Un conseiller cherche, parle aux gens et vous amène seulement ceux qui valent une rencontre. Vous retenez. Les honoraires se règlent à l'embauche.</p>
      <p>Ce n'est pas un babillard où vous triez des CV, ni un logiciel à apprendre. C'est un mandat : recherche, premier échange, shortlist, suivi jusqu'à l'entrée en poste. Beaucoup de mandats restent confidentiels. Certaines offres sont aussi publiées sur le site quand ça aide à trouver.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Confier mon recrutement</a>
        <a class="tl-btn tl-btn-ghost-dark" href="entreprises.html">Voir comment ça se passe</a>
      </div>
    </div>
  </div>
</section>
"""


def for_candidates_section(lang="fr"):
    if lang == "en":
        return """
<section class="tl-section tl-ice" id="candidats-intro">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">For talent</div>
      <h2 class="tl-h2">You are not dropping a resume into a database and hoping.</h2>
      <p>Talendus is the professional intermediary between you and companies. You create a profile, share your career, resume, skills and preferences. We study that information. When your profile fits an opportunity, we can contact you, talk with you, and (when the fit holds) present you to an employer.</p>
      <p>You may also apply to openings we publish. In every case, the company does not receive your email or phone number. A consultant presents your file and remains your contact. You are accompanied: screening, conversations, interviews when needed, then a possible introduction. Nothing is sent blindly to fifteen employers.</p>
      <p>Creating a profile is free. Fees are paid by the company. Our role is to understand your path and to consider you for mandates that actually match, not to flood you with interviews that go nowhere.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="candidates.html#cv">Create my profile</a>
        <a class="tl-btn tl-btn-ghost-dark" href="jobs.html">See opportunities</a>
      </div>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section tl-ice" id="candidats-intro">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">Pour les candidats</div>
      <h2 class="tl-h2">Vous ne déposez pas un CV dans une base en croisant les doigts.</h2>
      <p>Talendus est l'intermédiaire professionnel entre vous et les entreprises. Vous créez un profil, renseignez votre parcours, transmettez votre CV, indiquez vos compétences et vos préférences. Nous étudions ces informations. Lorsque votre profil correspond à une opportunité, Talendus peut vous contacter, échanger avec vous, puis (si l'adéquation tient) vous présenter à une entreprise.</p>
      <p>Vous pouvez aussi postuler aux offres que nous publions. Dans tous les cas, l'employeur ne reçoit pas votre courriel ni votre téléphone. Un conseiller présente votre dossier et reste votre interlocuteur. Vous êtes accompagné : analyse, échanges, étapes de sélection si nécessaire, puis une présentation éventuelle. Rien n'est envoyé à l'aveugle chez quinze employeurs.</p>
      <p>Créer un profil est gratuit. Les honoraires sont payés par l'entreprise. Notre rôle est de comprendre votre parcours et de vous considérer pour des mandats qui collent vraiment, pas de vous noyer sous des entrevues qui n'aboutissent pas.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="candidats.html#cv">Créer mon profil</a>
        <a class="tl-btn tl-btn-ghost-dark" href="emplois.html">Voir les opportunités</a>
      </div>
    </div>
  </div>
</section>
"""


def approach_section(lang="fr"):
    if lang == "en":
        items = [
            ("Technology", "Modern tools help Talendus structure needs, track mandates and move faster, without turning hiring into self-serve software for the company."),
            ("Artificial intelligence", "Talendus already uses AI in its internal tools to analyse, search, compare and process information faster. It supports our teams. It does not choose the hire, and it is not a tool we hand to recruiters to search on their own."),
            ("Human expertise", "Consultants verify real fit, speak with candidates, weigh professional personality and context, and qualify the files we present."),
            ("Market knowledge", "We work with companies of every size and with candidates at every level. Understanding both sides is what makes a shortlist useful."),
            ("Selection", "We do not sell volume. We do not send a pile of resumes. The aim is to present the most relevant profiles, so you can focus on the final choice."),
        ]
        kicker, heading, lead = "Our approach", "How Talendus works.", "Technology, AI and human expertise serve one process: search, screen, qualify, present."
    else:
        items = [
            ("Technologie", "Des outils modernes aident Talendus à structurer les besoins, suivre les mandats et avancer plus vite, sans transformer le recrutement en logiciel en libre-service pour l'entreprise."),
            ("Intelligence artificielle", "Talendus utilise déjà l'IA dans ses outils internes pour analyser, rechercher, comparer et traiter les informations plus rapidement. Elle soutient nos équipes. Elle ne choisit pas la personne embauchée, et elle n'est pas un outil remis aux recruteurs pour chercher seuls."),
            ("Expertise humaine", "Les conseillers vérifient la pertinence réelle, échangent avec les candidats, évaluent la personnalité professionnelle et le contexte, puis qualifient les dossiers que nous présentons."),
            ("Connaissance du marché", "Nous travaillons avec des entreprises de toutes tailles et des candidats de tous niveaux. Comprendre les deux côtés, c'est ce qui rend une shortlist utile."),
            ("Sélection", "Nous ne vendons pas du volume. Nous n'envoyons pas une pile de CV. L'objectif est de transmettre les profils les plus pertinents, pour que vous puissiez vous concentrer sur le choix final."),
        ]
        kicker, heading, lead = "Notre approche", "Comment Talendus travaille.", "Technologie, IA et expertise humaine servent un seul processus : rechercher, présélectionner, qualifier, présenter."
    cards = "".join(
        f'<div class="tl-card"><div class="body"><h3>{title}</h3><p>{text}</p></div></div>'
        for title, text in items
    )
    return f"""
<section class="tl-section" id="approche">
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


def process_section(lang="fr"):
    if lang == "en":
        kicker, heading, lead = (
            "How a mandate runs",
            "Four steps. You stay on the decision.",
            "No software to learn. You describe the seat; we come back with people worth meeting.",
        )
        steps = [
            ("01", "You tell us the role", "Title, site, hours, must-haves, pay range. A 20-minute call is usually enough."),
            ("02", "We calibrate", "We compare the brief with what the market will actually accept. If the ask is off, we say so before we waste a week."),
            ("03", "We search and speak", "Network, known profiles, discreet outreach to people already in a job. We talk to them before you do."),
            ("04", "You meet and retain", "A short list, each file defended. You interview. You decide. We stay until the person starts."),
        ]
    else:
        kicker, heading, lead = (
            "Le déroulement",
            "Quatre étapes. Vous gardez la décision.",
            "Pas de logiciel à apprendre. Vous décrivez le poste ; on revient avec des gens qui valent une rencontre.",
        )
        steps = [
            ("01", "Vous nous dites le poste", "Titre, site, horaire, indispensables, fourchette salariale. Un appel de 20 minutes suffit souvent."),
            ("02", "On calibre", "On compare le brief à ce que le marché accepte vraiment. Si la demande est décalée, on le dit avant de perdre une semaine."),
            ("03", "On cherche et on parle", "Réseau, profils déjà connus, approche discrète des gens en poste. On leur parle avant vous."),
            ("04", "Vous rencontrez et vous retenez", "Une shortlist courte, chaque dossier défendu. Vous les recevez. Vous décidez. On reste jusqu'à l'entrée en poste."),
        ]
    cards = "".join(
        f'<div class="tl-step"><span>{n}</span><h3>{t}</h3><p>{p}</p></div>'
        for n, t, p in steps
    )
    return f"""
<section class="tl-section tl-ice" id="processus">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-steps tl-steps-4">{cards}</div>
  </div>
</section>
"""


def employer_takeover_section(lang="fr"):
    if lang == "en":
        kicker, heading, lead = (
            "What leaves your desk",
            "For the open seat, Talendus runs the work.",
            "You do not become a part-time recruiter. Here is what we take on.",
        )
        items = [
            ("01", "The search", "We do not stop at people who answered an ad. We use the network, known profiles, and — when the trade requires it — we approach people already in a job."),
            ("02", "The first conversation", "A consultant talks to candidates before you do. Hours, pay, tickets, what would actually make them move. You do not lose a morning filtering."),
            ("03", "The shortlist", "A few files we will stand behind, not a stack. Each name is someone we can explain."),
            ("04", "Through start date", "Terms, notice period, onboarding. One contact until the person is on site."),
        ]
        close_h, close_p = (
            "You retain the person. The rest is our job.",
            "No resume database to browse. No tool to operate. You meet people who already passed our screen.",
        )
    else:
        kicker, heading, lead = (
            "Ce qui sort de votre bureau",
            "Pour le poste à combler, Talendus mène le travail.",
            "Vous n'avez pas à devenir recruteur à temps partiel. Voici ce qu'on prend en charge.",
        )
        items = [
            ("01", "La recherche", "On ne s'arrête pas aux gens qui ont répondu à une annonce. On mobilise le réseau, les profils déjà connus, et — quand le métier l'exige — on approche ceux qui sont déjà en poste."),
            ("02", "Le premier échange", "Un conseiller parle aux candidats avant vous. Horaire, salaire, tickets, ce qui les ferait vraiment bouger. Vous ne perdez pas une matinée à filtrer."),
            ("03", "La shortlist", "Quelques dossiers que nous sommes prêts à défendre, pas une liasse. Chaque nom est quelqu'un qu'on peut expliquer."),
            ("04", "Jusqu'à l'entrée en poste", "Conditions, préavis, intégration. Un seul interlocuteur jusqu'à ce que la personne soit sur le site."),
        ]
        close_h, close_p = (
            "Vous retenez la personne. Le reste, c'est notre métier.",
            "Pas de base de CV à fouiller. Pas d'outil à opérer. Vous rencontrez des gens qui ont déjà passé notre filtre.",
        )
    cards = "".join(
        f'<article class="tl-takeover-item"><span>{n}</span><h3>{t}</h3><p>{p}</p></article>'
        for n, t, p in items
    )
    return f"""
<section class="tl-section" id="prise-en-charge">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-takeover-list">{cards}</div>
    <div class="tl-takeover-close">
      <h3>{close_h}</h3>
      <p>{close_p}</p>
    </div>
  </div>
</section>
"""


def employer_pillars_section(lang="fr"):
    if lang == "en":
        kicker, heading = "How it is billed", "You move forward without putting money down first."
        items = [
            ("On success", "Fees are due when someone starts. The first call is free. If the mandate does not close, you do not pay, per the agreement."),
            ("Useful files, quickly", "On an operations role we aim for the first profiles within a week. A scarce manager takes longer — we say so at the brief, not after."),
            ("Without noise", "Replacement, reorganization, sensitive seat: we approach without posting until you decide the company should know."),
        ]
    else:
        kicker, heading = "Comment ça se paie", "Vous avancez sans vous exposer d'abord."
        items = [
            ("Au succès", "Les honoraires se règlent quand quelqu'un entre. L'appel de départ est gratuit. Si le mandat n'aboutit pas, vous ne payez pas, selon l'entente."),
            ("Des dossiers utiles, vite", "Sur un métier d'opérations, on vise les premiers profils en une semaine. Un cadre rare prend plus longtemps : on le dit au brief, pas après."),
            ("Sans bruit", "Remplacement, réorganisation, poste sensible : on approche sans afficher tant que vous n'avez pas décidé que l'interne doit le savoir."),
        ]
    cards = "".join(
        f'<article class="tl-pillar"><h3>{t}</h3><p>{p}</p></article>'
        for t, p in items
    )
    return f"""
<section class="tl-section tl-ice" id="conditions">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-pillars">{cards}</div>
  </div>
</section>
"""


def employer_sectors_grid(lang="fr"):
    if lang == "en":
        kicker, heading, lead = (
            "Where we hire",
            "Floor roles as much as office roles.",
            "These are examples. If the seat is not listed, describe it — we open the search.",
        )
        groups = [
            ("Plant and production", ["Production operator", "Welder", "CNC machinist", "Shift supervisor"]),
            ("Warehouse and transport", ["Forklift operator", "Shipping clerk", "Driver", "Logistics coordinator"]),
            ("Maintenance", ["Electromechanical tech", "Industrial mechanic", "Maintenance technician"]),
            ("Construction", ["Site foreman", "Project coordinator", "Skilled trades on site"]),
            ("Office and admin", ["Administrative assistant", "Accounting clerk", "Customer service"]),
            ("Site leadership", ["Plant manager", "Production lead", "Site HR"]),
        ]
    else:
        kicker, heading, lead = (
            "Où on recrute",
            "Des métiers de plancher autant que de bureau.",
            "Ce sont des exemples. Si le poste n'est pas listé, décrivez-le : on ouvre la recherche.",
        )
        groups = [
            ("Usine et production", ["Opérateur de production", "Soudeur", "Machiniste CNC", "Superviseur de quart"]),
            ("Entrepôt et transport", ["Cariste", "Commis d'expédition", "Chauffeur", "Coordonnateur logistique"]),
            ("Maintenance", ["Électromécanicien", "Mécanicien industriel", "Technicien de maintenance"]),
            ("Construction", ["Contremaître", "Coordonnateur de chantier", "Métiers spécialisés sur site"]),
            ("Bureau et admin", ["Adjoint administratif", "Commis comptable", "Service à la clientèle"]),
            ("Direction de site", ["Directeur d'usine", "Responsable production", "RH de site"]),
        ]
    cards = "".join(
        '<article class="tl-hire-sector"><h3>'
        + t
        + "</h3><ul>"
        + "".join(f"<li>{role}</li>" for role in roles)
        + "</ul></article>"
        for t, roles in groups
    )
    return f"""
<section class="tl-section" id="metiers-employeur">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-hire-sectors">{cards}</div>
  </div>
</section>
"""


def employer_risk_section(lang="fr"):
    if lang == "en":
        kicker, heading = "What you commit to", "You pay for a hire that happens, not for a search that drags."
        items = [
            ("Fees on the start date", "Billed against the annual salary of the person placed, when they start."),
            ("Replacement on permanent seats", "If the hire does not hold through the written window, we reopen the search."),
            ("Non-exclusive by default", "You can keep looking. We still treat the mandate as ours until you say otherwise."),
        ]
    else:
        kicker, heading = "À quoi vous vous engagez", "Vous payez une embauche qui a lieu, pas une recherche qui traîne."
        items = [
            ("Honoraires à l'entrée en poste", "Calculés sur le salaire annuel de la personne placée, quand elle commence."),
            ("Remplacement sur les permanents", "Si l'embauche ne tient pas dans la fenêtre écrite, on relance la recherche."),
            ("Non exclusif par défaut", "Vous pouvez continuer à chercher. On traite quand même le mandat comme le nôtre jusqu'à ce que vous disiez le contraire."),
        ]
    cards = "".join(
        f'<article class="tl-risk-item"><h3>{t}</h3><p>{p}</p></article>'
        for t, p in items
    )
    return f"""
<section class="tl-section tl-ice" id="sans-risque">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-risk-list">{cards}</div>
  </div>
</section>
"""


def employer_quotes_section(lang="fr"):
    if lang == "en":
        kicker, heading = "Employers", "What managers tell us after a hire"
        quotes = [
            ("They understood the role on the first call. The files they brought actually matched the floor, not a generic title.", "M.L.", "Director of operations · South Shore"),
            ("Not an agency that dumps 40 resumes. Three solid people, and they stayed on the file after day one.", "J.R.", "Director · Mauricie"),
            ("A confidential replacement, no internal noise. Start date lined up with our shutdown calendar.", "S.B.", "VP · Montérégie"),
        ]
    else:
        kicker, heading = "Employeurs", "Ce que les gestionnaires nous disent après une embauche"
        quotes = [
            ("Ils ont compris le poste dès le premier appel. Les dossiers correspondaient au plancher, pas à un titre générique.", "M.L.", "Directrice des opérations · Rive-Sud"),
            ("Pas une agence qui envoie 40 CV. Trois personnes solides, et ils sont restés sur le dossier après le jour un.", "J.R.", "Directeur · Mauricie"),
            ("Un remplacement confidentiel, sans bruit interne. Date d'entrée calée sur notre arrêt d'usine.", "S.B.", "VP · Montérégie"),
        ]
    cards = "".join(
        f"""<blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>{q}</p>
          <footer><strong>{name}</strong><span>{role}</span></footer>
        </blockquote>"""
        for q, name, role in quotes
    )
    return f"""
<section class="tl-section" id="temoignages">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-grid-3 tl-quotes">{cards}</div>
  </div>
</section>
"""


def employer_faq_block(lang, items, faq_html):
    if lang == "en":
        kicker, heading = "Questions employers ask", "Straight answers before you book a call"
        cta = "Hand us the search"
    else:
        kicker, heading = "Questions des employeurs", "Des réponses nettes avant de réserver un appel"
        cta = "Confier mon recrutement"
    return f"""
<section class="tl-section" id="faq">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    {faq_html(items)}
    <div class="tl-center" style="margin-top:32px">
      <a class="tl-btn tl-btn-lg" href="contact.html">{cta}</a>
    </div>
  </div>
</section>
"""


def employer_landing_sections(lang="fr"):
    """Page Entreprises / Employers : hero fourni par l'appelant."""
    return (
        employer_takeover_section(lang)
        + employer_pillars_section(lang)
        + process_section(lang)
        + employer_sectors_grid(lang)
        + company_types_section(lang)
        + employer_quotes_section(lang)
        + employer_risk_section(lang)
        + bad_hire_calculator_section(lang)
    )


def why_talendus_section(lang="fr"):
    if lang == "en":
        kicker, heading = "Why go through Talendus", "Because hiring well is a job. You already have one."
        items = [
            ("Save time", "Talendus takes on a large part of the search and screening. You describe the role and stay available for the conversations that matter. You do not spend evenings sorting applications that will never fit."),
            ("Reach more talent", "We draw on several sources: people who apply, people already in our network, and people who are not looking publicly. A company acting alone usually sees only who answered an ad."),
            ("Receive qualified applications", "The aim is to cut noise and put your attention on relevant profiles. A shortlist you can actually review is worth more than a hundred unread resumes."),
            ("A search already strengthened by AI", "Talendus already uses AI internally to analyse resumes, skills and criteria faster. You benefit from that work without operating the tools yourself. They are not a self-serve engine for you to hunt candidates on Talendus."),
            ("A human selection", "Profiles are not forwarded automatically. Consultants review, speak with people when needed, and qualify what we present. Fit is more than keywords on a resume."),
            ("One contact", "You hand the need to Talendus and work with a consultant through to the decision. Call us, describe the role, we search and come back with files you can actually review."),
        ]
        cta = "Hand us the search"
        href = "contact.html"
    else:
        kicker, heading = "Pourquoi passer par Talendus", "Parce que bien recruter est un métier. Vous en avez déjà un."
        items = [
            ("Gagnez du temps", "Talendus prend en charge une grande partie de la recherche et de la présélection. Vous décrivez le poste et restez disponible pour les échanges qui comptent. Vous ne passez pas vos soirs à trier des candidatures qui ne colleront pas."),
            ("Accédez à davantage de talents", "Nous mobilisons plusieurs sources : les personnes qui postulent, celles déjà dans notre réseau, et celles qui ne cherchent pas publiquement. Une entreprise seule voit surtout celles qui ont répondu à une annonce."),
            ("Recevez des candidatures qualifiées", "L'objectif est de réduire le bruit et de concentrer votre attention sur des profils pertinents. Une shortlist que vous pouvez vraiment étudier vaut mieux qu'une centaine de CV non lus."),
            ("Une recherche déjà renforcée par l'IA", "Talendus utilise déjà l'intelligence artificielle en interne pour analyser plus vite les parcours, les compétences et les critères. Vous bénéficiez de ce travail sans opérer les outils vous-même. Ils ne sont pas un moteur en libre-service pour que vous chassiez des candidats sur Talendus."),
            ("Une sélection humaine", "Les profils ne sont pas transmis automatiquement. Les conseillers étudient, échangent si besoin, et qualifient ce que nous présentons. L'adéquation dépasse les mots-clés d'un CV."),
            ("Un interlocuteur unique", "Vous confiez votre besoin à Talendus et travaillez avec un conseiller jusqu'à la décision. Appelez-nous, décrivez le poste, on cherche et on revient avec des dossiers que vous pouvez vraiment étudier."),
        ]
        cta = "Confier mon recrutement"
        href = "contact.html"
    cards = "".join(
        f'<div class="tl-card"><div class="body"><h3>{title}</h3><p>{text}</p></div></div>'
        for title, text in items
    )
    return f"""
<section class="tl-section" id="pourquoi">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-why-grid">{cards}</div>
    <div class="tl-center" style="margin-top:32px">
      <a class="tl-btn tl-btn-lg" href="{href}">{cta}</a>
    </div>
  </div>
</section>
"""


def persona_region(persona, html):
    return f'<div data-persona-only="{persona}">{html}</div>'


def gateway_orientation_section(lang="fr"):
    if lang == "en":
        return """
<section class="tl-section" id="parcours">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">After you choose</div>
      <h2 class="tl-h2">Two paths. One agency. A consultant for each side.</h2>
      <p class="tl-lead">Once that choice is made, Talendus does not work the same way. Here is what actually changes on each side.</p>
    </div>
    <div class="tl-gateway-lanes">
      <article class="tl-gateway-lane is-talent">
        <span class="tl-kicker">On the candidate side</span>
        <h3>We represent you</h3>
        <p>You are not dropped into a company inbox. A consultant studies your path, calls you when a mandate fits, then presents your file. Creating a profile is free. Write to us or call — we take it from there.</p>
        <ul class="tl-gateway-points">
          <li>Your resume is reviewed, not blasted to fifteen employers.</li>
          <li>You hear from us when there is a real fit — not a generic job alert.</li>
          <li>A consultant stays with you through screening and any presentation. Call us anytime.</li>
        </ul>
        <a class="tl-btn" href="candidates.html" data-set-persona="talent">See how it works for you</a>
      </article>
      <article class="tl-gateway-lane is-hire">
        <span class="tl-kicker">On the employer side</span>
        <h3>We hire for you</h3>
        <p>You describe the role. We search, talk to people, bring a shortlist. You retain. Fees at the hire.</p>
        <ul class="tl-gateway-points">
          <li>A brief to hand over — not a tool to learn.</li>
          <li>People already qualified, not a pile of CVs.</li>
          <li>One consultant through start date.</li>
        </ul>
        <a class="tl-btn" href="employers.html" data-set-persona="entreprise">See how it works for you</a>
      </article>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section" id="parcours">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Une fois le côté choisi</div>
      <h2 class="tl-h2">Deux parcours. Une agence. Un conseiller pour chaque besoin.</h2>
      <p class="tl-lead">Une fois ce choix fait, Talendus ne travaille pas de la même façon. Voici ce qui change concrètement, de chaque côté.</p>
    </div>
    <div class="tl-gateway-lanes">
      <article class="tl-gateway-lane is-talent">
        <span class="tl-kicker">Du côté candidats</span>
        <h3>On vous représente</h3>
        <p>Vous n'atterrissez pas dans la boîte courriel d'une entreprise. Un conseiller étudie votre parcours, vous rappelle quand un mandat colle, puis présente votre dossier. Créer un profil est gratuit. Écrivez-nous ou appelez : on s'en occupe.</p>
        <ul class="tl-gateway-points">
          <li>Votre CV est lu, pas envoyé à l'aveugle chez quinze employeurs.</li>
          <li>On vous écrit quand ça correspond vraiment — pas une alerte générique.</li>
          <li>Un conseiller vous suit jusqu'à une présentation. Appelez-nous quand vous voulez.</li>
        </ul>
        <a class="tl-btn" href="candidats.html" data-set-persona="talent">Voir comment ça se passe</a>
      </article>
      <article class="tl-gateway-lane is-hire">
        <span class="tl-kicker">Du côté entreprises</span>
        <h3>On recrute pour vous</h3>
        <p>Vous décrivez le poste. On cherche, on parle aux gens, on vous amène une shortlist. Vous retenez. Honoraires à l'embauche.</p>
        <ul class="tl-gateway-points">
          <li>Un brief à nous passer — pas un outil à apprendre.</li>
          <li>Des gens déjà qualifiés, pas une pile de CV.</li>
          <li>Un conseiller jusqu'à l'entrée en poste.</li>
        </ul>
        <a class="tl-btn" href="entreprises.html" data-set-persona="entreprise">Voir comment ça se passe</a>
      </article>
    </div>
  </div>
</section>
"""


def persona_switch_bar(lang="fr"):
    if lang == "en":
        talent = '<p class="tl-persona-switch">Hiring instead? <a href="employers.html" data-set-persona="entreprise">Go to the employer side</a></p>'
        hire = '<p class="tl-persona-switch">Looking for a job? <a href="candidates.html" data-set-persona="talent">Go to the talent side</a></p>'
    else:
        talent = '<p class="tl-persona-switch">Vous recrutez ? <a href="entreprises.html" data-set-persona="entreprise">Aller du côté entreprises</a></p>'
        hire = '<p class="tl-persona-switch">Vous cherchez un emploi ? <a href="candidats.html" data-set-persona="talent">Aller du côté candidats</a></p>'
    return (
        persona_region("talent", f'<div class="container tl-persona-switch-wrap">{talent}</div>')
        + persona_region("entreprise", f'<div class="container tl-persona-switch-wrap">{hire}</div>')
    )


def talent_cta_band(lang="fr"):
    if lang == "en":
        return """
<section class="tl-cta-band" id="profil">
  <div class="container">
    <span class="tl-badge tl-badge-light">Create my profile</span>
    <h2 class="tl-h2">Looking for a job? Enter the Talendus network.</h2>
    <p>Create your profile, submit your resume. We study your path and contact you when an opportunity fits. Free for talent.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="candidates.html#cv">Create my profile</a>
      <a class="tl-btn tl-btn-ghost" href="jobs.html">See opportunities</a>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-cta-band" id="profil">
  <div class="container">
    <span class="tl-badge tl-badge-light">Créer mon profil</span>
    <h2 class="tl-h2">Vous cherchez un emploi ? Entrez dans le réseau Talendus.</h2>
    <p>Créez votre profil, déposez votre CV. Nous étudions votre parcours et vous contactons lorsqu'une opportunité correspond. Gratuit pour les talents.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="candidats.html#cv">Créer mon profil</a>
      <a class="tl-btn tl-btn-ghost" href="emplois.html">Voir les opportunités</a>
    </div>
  </div>
</section>
"""


def ai_engine_section(lang="fr"):
    groups_html = []
    for title, blurb, items in AI_FEATURE_GROUPS[lang]:
        rows = "".join(
            f"<li><strong>{name}</strong> {text}</li>"
            for name, text in items
        )
        groups_html.append(
            f'<div class="tl-ai-group"><h3>{title}</h3><p>{blurb}</p><ul>{rows}</ul></div>'
        )
    groups = "".join(groups_html)
    if lang == "en":
        kicker = "Already in our internal tools"
        heading = "AI already works for Talendus. You receive the result."
        lead = "Matching, resume reading, skills, ranking: our teams use this today. It is not software we hand you. It is how we present the right files faster. Consultants qualify. You keep the final decision."
        badge = "In service"
    else:
        kicker = "Déjà dans nos outils internes"
        heading = "L'IA travaille déjà pour Talendus. Vous, vous recevez le résultat."
        lead = "Matching, lecture des CV, compétences, priorisation : nos équipes s'en servent aujourd'hui. Ce n'est pas un logiciel que nous vous remettons. C'est ce qui nous permet de présenter plus vite les bons dossiers. Les conseillers qualifient. Vous gardez la décision finale."
        badge = "En service"
    return f"""
<section class="tl-section tl-ai-direction" id="ia">
  <div class="container">
    <div class="tl-ai-panel">
      <div class="tl-ai-panel-intro">
        <span class="tl-chip">{badge}</span>
        <div class="tl-kicker">{kicker}</div>
        <h2 class="tl-h2">{heading}</h2>
        <p class="tl-lead">{lead}</p>
      </div>
      <div class="tl-ai-groups">{groups}</div>
    </div>
  </div>
</section>
"""


def augmented_recruiting_section(lang="fr"):
    if lang == "en":
        items = [
            ("Faster search", "Internal tools help our teams cover more ground and treat large volumes of information without leaving the search on your desk."),
            ("Profile analysis", "Resumes are read, structured and compared to the role: skills, experience, qualifications and path."),
            ("Useful correspondences", "AI helps relate a need to profiles that deserve human review. It does not declare a perfect hire."),
            ("Screening support", "A first pass and a clearer order of files, so consultants spend their time on people worth qualifying."),
            ("Structured information", "What a mandate requires and what a career shows is organized so the team works faster."),
            ("Human qualification", "Consultants verify, contact, interview and select. AI accelerates the work. It does not replace Talendus expertise."),
        ]
        return """
<section class="tl-section" id="recrutement-augmente">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Already operational</div>
      <h2 class="tl-h2">Hiring augmented by artificial intelligence.</h2>
      <p class="tl-lead">Talendus already uses AI internally to speed up search, analyse profiles, spot correspondences, support screening and structure information, so our recruiters can focus on human qualification.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
            f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items
        ) + """</div>
  </div>
</section>
"""
    items = [
        ("Recherche accélérée", "Les outils internes aident nos équipes à couvrir davantage de terrain et à traiter de grands volumes d'informations, sans laisser la recherche sur votre bureau."),
        ("Analyse des profils", "Les CV sont lus, structurés et comparés au poste : compétences, expérience, qualifications et parcours."),
        ("Correspondances utiles", "L'IA aide à relier un besoin aux profils qui méritent une revue humaine. Elle ne déclare pas un candidat parfait."),
        ("Aide à la présélection", "Un premier passage et un ordre plus clair des dossiers, pour que les conseillers consacrent leur temps aux personnes à qualifier."),
        ("Informations structurées", "Ce qu'un mandat exige et ce qu'un parcours montre est organisé pour que l'équipe travaille plus vite."),
        ("Qualification humaine", "Les conseillers vérifient, contactent, interviewent et sélectionnent. L'IA accélère le travail. Elle ne remplace pas l'expertise Talendus."),
    ]
    return """
<section class="tl-section" id="recrutement-augmente">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Déjà opérationnel</div>
      <h2 class="tl-h2">Le recrutement augmenté par l'intelligence artificielle.</h2>
      <p class="tl-lead">Talendus utilise déjà l'IA en interne pour accélérer la recherche, analyser les profils, identifier les correspondances, aider à la présélection et structurer les informations, afin que nos recruteurs se concentrent sur la qualification humaine.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
        f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items
    ) + """</div>
  </div>
</section>
"""


def technology_section(lang="fr"):
    if lang == "en":
        items = [
            ("Proprietary technology", "Talendus has built and uses internal tools so its teams work more effectively. They are not a SaaS product you log into to hunt candidates."),
            ("Intelligent tools", "Analysis, matching support, classification, synthesis and writing assistance sit inside our process. You see the result: a more relevant shortlist, delivered faster."),
            ("Benefit over architecture", "You do not need to learn a stack or configure an engine. You hand us the need. We use the technology. You receive qualified profiles."),
        ]
        return """
<section class="tl-section tl-ice" id="technologie">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Our technology</div>
      <h2 class="tl-h2">The intelligent tools that improve Talendus's hiring process.</h2>
      <p class="tl-lead">Technology and AI are Talendus's operational advantage, not a software product we sell instead of placement.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
            f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items
        ) + """</div>
  </div>
</section>
"""
    items = [
        ("Technologie propriétaire", "Talendus a développé et utilise des outils internes pour que ses équipes travaillent plus efficacement. Ce n'est pas un logiciel SaaS dans lequel vous vous connectez pour chasser des candidats."),
        ("Outils intelligents", "Analyse, aide au matching, classification, synthèse et assistance à la rédaction restent dans notre processus. Vous voyez le résultat : une shortlist plus pertinente, plus rapidement."),
        ("Le bénéfice, pas l'architecture", "Vous n'avez pas à apprendre une plateforme ni à paramétrer un moteur. Vous nous confiez le besoin. Nous utilisons la technologie. Vous recevez des profils qualifiés."),
    ]
    return """
<section class="tl-section tl-ice" id="technologie">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Notre technologie</div>
      <h2 class="tl-h2">Les outils intelligents qui améliorent le processus de recrutement de Talendus.</h2>
      <p class="tl-lead">La technologie et l'IA constituent l'avantage opérationnel de Talendus, pas un logiciel que nous vendons à la place du placement.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
        f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items
    ) + """</div>
  </div>
</section>
"""


def ai_screening_section(lang="fr"):
    if lang == "en":
        steps = [
            ("AI", "Analyses available information, spots potential correspondences and helps prioritize files."),
            ("Talendus team", "Verifies, qualifies, contacts, interviews and selects. Human judgment remains essential."),
            ("Company", "Receives a relevant selection and makes the final decision. You do not operate the AI."),
        ]
        return """
<section class="tl-section" id="preselection-ia">
  <div class="container">
    <div class="tl-prose" style="margin-bottom:36px">
      <div class="tl-kicker">AI-assisted screening</div>
      <h2 class="tl-h2">AI accelerates the work. It does not replace Talendus expertise.</h2>
      <p>Artificial intelligence helps Talendus run a first analysis of profiles. It does not send you a pile of resumes, and it does not hire in your place. Technology processes information quickly. AI helps identify correspondences. A Talendus recruiter analyses, verifies, talks and qualifies. The company receives a relevant selection and decides.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
            f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in steps
        ) + """</div>
  </div>
</section>
"""
    steps = [
        ("IA", "Analyse les informations disponibles, identifie les correspondances potentielles et aide à prioriser les dossiers."),
        ("Équipe Talendus", "Vérifie, qualifie, contacte, interviewe et sélectionne. Le jugement humain reste essentiel."),
        ("Entreprise", "Reçoit une sélection de candidats pertinents et prend la décision finale. Vous n'opérez pas l'IA."),
    ]
    return """
<section class="tl-section" id="preselection-ia">
  <div class="container">
    <div class="tl-prose" style="margin-bottom:36px">
      <div class="tl-kicker">Présélection assistée par l'IA</div>
      <h2 class="tl-h2">L'intelligence artificielle accélère le travail. Elle ne remplace pas l'expertise humaine.</h2>
      <p>L'IA aide Talendus à effectuer une première analyse des profils. Elle n'envoie pas une pile de CV, et elle n'embauche pas à votre place. La technologie traite rapidement l'information. L'IA aide à identifier les correspondances. Le recruteur Talendus analyse, vérifie, échange et qualifie. L'entreprise reçoit une sélection de candidats pertinents et décide.</p>
    </div>
    <div class="tl-grid-3">""" + "".join(
        f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in steps
    ) + """</div>
  </div>
</section>
"""


def competitive_advantage_section(lang="fr"):
    if lang == "en":
        avoid = [
            "Learn how to use an AI tool",
            "Configure a complex engine",
            "Search hundreds of profiles yourself",
            "Manually analyse a large volume of resumes",
        ]
        return """
<section class="tl-section tl-ice" id="avantage">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">Your advantage</div>
      <h2 class="tl-h2">You do not have to become an AI operator to hire well.</h2>
      <p>While you focus on your company, Talendus works to identify and qualify the talent you need. Thanks to its technological tools and artificial intelligence, Talendus can considerably accelerate certain search and screening steps.</p>
      <p>You do not need to:</p>
      <ul>""" + "".join(f"<li>{x}</li>" for x in avoid) + """</ul>
      <p><strong>Hand the need to Talendus.</strong> We then do the work. Technology improves the service; it does not transfer the work onto the client.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Hand us the search</a>
      </div>
    </div>
  </div>
</section>
"""
    avoid = [
        "apprendre à utiliser une IA",
        "paramétrer un outil complexe",
        "rechercher vous-même des centaines de profils",
        "analyser manuellement une grande quantité de CV",
    ]
    return """
<section class="tl-section tl-ice" id="avantage">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">Votre avantage</div>
      <h2 class="tl-h2">Vous n'avez pas à devenir opérateur d'IA pour bien recruter.</h2>
      <p>Pendant que vous vous concentrez sur votre entreprise, Talendus travaille à identifier et qualifier les talents dont vous avez besoin. Grâce à ses outils technologiques et à l'intelligence artificielle, Talendus peut accélérer considérablement certaines étapes de la recherche et de la présélection.</p>
      <p>Vous n'avez pas besoin :</p>
      <ul>""" + "".join(f"<li>{x}</li>" for x in avoid) + """</ul>
      <p><strong>Confiez votre besoin à Talendus.</strong> Nous faisons ensuite le travail. La technologie améliore le service ; elle ne transfère pas le travail vers le client.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Confier mon recrutement</a>
      </div>
    </div>
  </div>
</section>
"""


def placement_process_services_section(lang="fr"):
    if lang == "en":
        services = [
            ("Search", "We look for people who match the seat: network, known profiles, applications, and a posting when it helps. People already in a job can be approached quietly."),
            ("First conversation", "A consultant talks to candidates before you do. Path, hours, pay, what would make them move. You are not the first filter."),
            ("Shortlist", "A few files we will stand behind. You meet. You decide. Volume is not the product."),
            ("Placement", "We stay through start date. On permanent seats: 30/60/90 follow-up and a written replacement window. Fees on success."),
        ]
        kicker, heading, lead = (
            "From need to start date",
            "One mandate. Four pieces of work.",
            "You describe the role. We run the search. You keep the hire.",
        )
    else:
        services = [
            ("Recherche", "On cherche qui correspond au poste : réseau, profils déjà connus, candidatures, et une offre publiée quand ça aide. Les gens déjà en poste peuvent être approchés sans bruit."),
            ("Premier échange", "Un conseiller parle aux candidats avant vous. Parcours, horaire, salaire, ce qui les ferait bouger. Vous n'êtes pas le premier filtre."),
            ("Shortlist", "Quelques dossiers que nous sommes prêts à défendre. Vous rencontrez. Vous décidez. Le volume n'est pas le produit."),
            ("Placement", "On reste jusqu'à l'entrée en poste. Sur les permanents : suivi 30/60/90 et une fenêtre de remplacement écrite. Honoraires au succès."),
        ]
        kicker, heading, lead = (
            "Du besoin à l'entrée en poste",
            "Un mandat. Quatre morceaux de travail.",
            "Vous décrivez le poste. On mène la recherche. Vous gardez l'embauche.",
        )
    cards = "".join(
        f'<article class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></article>'
        for t, p in services
    )
    return f"""
<section class="tl-section" id="services-processus">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      <p class="tl-lead">{lead}</p>
    </div>
    <div class="tl-grid-4 tl-services-process">{cards}</div>
  </div>
</section>
"""


def human_section(lang="fr"):
    if lang == "en":
        return """
<section class="tl-section tl-ice" id="humain">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">The human dimension</div>
      <h2 class="tl-h2">Hiring is not matching keywords on a resume.</h2>
      <p>A useful profile is more than a list of tools and job titles. Talendus also needs to understand motivations, the real path, ambitions, professional personality, expectations, the context of the role and (when it matters) the culture of the organization. That reading does not come out of a score. It comes from people who speak with candidates and who have understood the mandate.</p>
      <p>Our consultants stay essential: they check whether a correspondence is real, they run the conversations, they weigh what a CV cannot say, they confirm fit, and they present the files. AI already helps us treat information faster. It does not replace that judgment. The company keeps the final decision. Humans, on both sides, remain at the centre of qualification.</p>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section tl-ice" id="humain">
  <div class="container">
    <div class="tl-prose">
      <div class="tl-kicker">La dimension humaine</div>
      <h2 class="tl-h2">Recruter, ce n'est pas comparer des mots-clés dans un CV.</h2>
      <p>Un profil utile, ce n'est pas seulement une liste d'outils et de titres. Talendus doit aussi comprendre les motivations, le parcours réel, les ambitions, la personnalité professionnelle, les attentes, le contexte du poste et (lorsque c'est pertinent) la culture de l'organisation. Cette lecture ne sort pas d'un score. Elle vient de personnes qui parlent aux candidats et qui ont compris le mandat.</p>
      <p>Nos conseillers restent essentiels : ils vérifient si une correspondance est réelle, ils mènent les échanges, ils évaluent ce qu'un CV ne dit pas, ils confirment l'adéquation, et ils présentent les dossiers. L'IA nous aide déjà à traiter plus vite les informations. Elle ne remplace pas ce jugement. L'entreprise garde la décision finale. L'humain, des deux côtés, reste au centre de la qualification.</p>
    </div>
  </div>
</section>
"""


def company_types_section(lang="fr"):
    if lang == "en":
        items = [
            ("SME without a dedicated HR team", "Hiring lands on the owner or the ops lead. We take the mandate so the site keeps running."),
            ("A plant that is growing", "Several seats at once, little time to sort. We absorb the search."),
            ("First employee", "The same care as a larger file. The first hire sets the tone."),
            ("A larger organization", "Volume, confidentiality, several stakeholders. One consultant, a shortlist, you decide."),
        ]
        kicker, heading = "Who it is for", "Especially companies that cannot park someone on recruiting all week."
    else:
        items = [
            ("PME sans RH dédié", "Le recrutement tombe sur le proprio ou le directeur d'ops. On reprend le mandat pour que le site continue de tourner."),
            ("Un site qui grossit", "Plusieurs postes en même temps, peu de temps pour trier. On absorbe la recherche."),
            ("Premier employé", "Le même soin qu'un dossier plus large. Le premier recrutement pose le ton."),
            ("Organisation plus grande", "Volume, confidentialité, plusieurs interlocuteurs. Un conseiller, une shortlist, vous décidez."),
        ]
        kicker, heading = "Pour qui", "Surtout les entreprises qui ne peuvent pas stationner quelqu'un sur le recrutement toute la semaine."
    cards = "".join(
        f'<div class="tl-card"><div class="body"><h3>{t}</h3><p>{p}</p></div></div>'
        for t, p in items
    )
    return f"""
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-grid-4">{cards}</div>
  </div>
</section>
"""


def candidate_journey_section(lang="fr"):
    if lang == "en":
        kicker, heading = "Your path", "From profile to a possible introduction."
        steps = [
            ("01", "Create your profile", "Name, role, region, skills and preferences. Five minutes to enter the Talendus network. This is not a public CV dump: it is a file our team can study."),
            ("02", "Submit your resume", "A link or an upload. We use it to understand your path. A consultant reads it and calls you when a mandate actually fits."),
            ("03", "Skills and preferences", "What you know how to do, where you can work, the kind of role you want. The clearer this is, the more useful our search for you becomes."),
            ("04", "Opportunities", "You can browse openings we publish and apply. Many mandates never appear: your profile stays active and we can contact you when a fit appears."),
            ("05", "Identified for a role", "When your profile matches a need, Talendus can reach out. We do not send you blindly to fifteen employers."),
            ("06", "Talk with Talendus", "A consultant is your contact. Screening, questions, sometimes an interview with us, then we present you when it fits. Call or write whenever you want news."),
            ("07", "Presented when it fits", "If the fit holds, we present your file. You keep control: you can decline. The company chooses. Your consultant stays with you."),
            ("08", "Follow your path", "In your workspace: applications, messages with Talendus, interviews we schedule. Write to your consultant as soon as you have a question."),
        ]
    else:
        kicker, heading = "Votre parcours", "Du profil à une présentation éventuelle."
        steps = [
            ("01", "Créer votre profil", "Nom, métier, région, compétences et préférences. Cinq minutes pour entrer dans le réseau Talendus. Ce n'est pas un dépôt public de CV : c'est un dossier que notre équipe peut étudier."),
            ("02", "Déposer votre CV", "Un lien ou un fichier. Nous l'utilisons pour comprendre votre parcours. Un conseiller le lit et vous rappelle quand un mandat correspond vraiment."),
            ("03", "Compétences et préférences", "Ce que vous savez faire, où vous pouvez travailler, le type de poste visé. Plus c'est clair, plus notre recherche pour vous est utile."),
            ("04", "Opportunités", "Vous pouvez consulter les offres que nous publions et postuler. Beaucoup de mandats n'apparaissent pas : votre profil reste actif et nous pouvons vous contacter lorsqu'une correspondance se présente."),
            ("05", "Identifié pour un poste", "Lorsque votre profil correspond à un besoin, Talendus peut vous joindre. Nous ne vous envoyons pas à l'aveugle chez quinze employeurs."),
            ("06", "Échanger avec Talendus", "Un conseiller est votre interlocuteur. Analyse, questions, parfois un entretien avec nous, puis nous vous présentons si ça colle. Appelez ou écrivez dès que vous voulez des nouvelles."),
            ("07", "Présenté si ça colle", "Si l'adéquation tient, nous présentons votre dossier. Vous gardez la main : vous pouvez refuser. L'entreprise choisit. Votre conseiller reste avec vous."),
            ("08", "Suivre votre parcours", "Dans votre espace : candidatures, messages avec Talendus, entretiens que nous planifions. Écrivez à votre conseiller dès que vous avez une question."),
        ]
    cards = "".join(
        f'<div class="tl-step"><span>{n}</span><h3>{t}</h3><p>{p}</p></div>'
        for n, t, p in steps
    )
    return f"""
<section class="tl-section" id="parcours-candidat">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-steps tl-steps-7">{cards}</div>
  </div>
</section>
"""


def need_process_section(lang="fr"):
    """Page « besoin de recrutement », 8 étapes côté entreprise."""
    return process_section(lang)


def hiring_need_form_section(lang="fr"):
    fields = employer_need_fields(lang)
    if lang == "en":
        return f"""
<section class="tl-section" id="besoin">
  <div class="container">
    <div class="tl-prose" style="max-width:720px;margin:0 auto 28px">
      <div class="tl-kicker">Hiring request</div>
      <h2 class="tl-h2">Describe your hiring need</h2>
      <p>Not a job-ad form. A brief so a consultant can call you back and open the search.</p>
    </div>
    <form class="tl-form" action="#" method="post" data-form="hiring-need" style="max-width:720px;margin:0 auto">
      {HONEYPOT_INPUT}
      <input type="hidden" name="profil" value="Employer, hiring need">
      <div class="tl-row-2"><div><label>Company name</label><input required name="entreprise"></div>
      <div><label>Your name</label><input required name="nom"></div></div>
      <div class="tl-row-2"><div><label>Role</label><input name="fonction" placeholder="HR, operations, owner…"></div>
      <div><label>Work email</label><input type="email" required name="courriel"></div></div>
      <div class="tl-row-2"><div><label>Phone</label><input name="tel"></div>
      <div><label>Company size</label><input name="taille" placeholder="e.g. 50–200"></div></div>
      {fields}
      <label>Experience level</label><input name="experience" placeholder="e.g. 3–5 years, junior, leadership">
      <label>Key skills</label><input name="competences" placeholder="Must-have skills, languages, qualifications">
      <button class="tl-btn tl-btn-lg" type="submit">Hand us the search</button>
      <div class="tl-success"></div>
    </form>
  </div>
</section>
"""
    return f"""
<section class="tl-section" id="besoin">
  <div class="container">
    <div class="tl-prose" style="max-width:720px;margin:0 auto 28px">
      <div class="tl-kicker">Demande de recrutement</div>
      <h2 class="tl-h2">Décrivez votre besoin de recrutement</h2>
      <p>Pas un formulaire d'annonce. Un brief pour qu'un conseiller vous rappelle et ouvre la recherche.</p>
    </div>
    <form class="tl-form" action="#" method="post" data-form="hiring-need" style="max-width:720px;margin:0 auto">
      {HONEYPOT_INPUT}
      <input type="hidden" name="profil" value="Employeur, je recrute">
      <div class="tl-row-2"><div><label>Nom de l'entreprise</label><input required name="entreprise"></div>
      <div><label>Nom du contact</label><input required name="nom"></div></div>
      <div class="tl-row-2"><div><label>Fonction</label><input name="fonction" placeholder="RH, opérations, direction…"></div>
      <div><label>Courriel professionnel</label><input type="email" required name="courriel"></div></div>
      <div class="tl-row-2"><div><label>Téléphone</label><input name="tel"></div>
      <div><label>Taille de l'entreprise</label><input name="taille" placeholder="ex. 50–200"></div></div>
      {fields}
      <label>Niveau d'expérience</label><input name="experience" placeholder="ex. 3 à 5 ans, junior, cadre">
      <label>Compétences et qualifications</label><input name="competences" placeholder="Compétences indispensables, langues, diplômes">
      <button class="tl-btn tl-btn-lg" type="submit">Confier mon recrutement</button>
      <div class="tl-success"></div>
    </form>
  </div>
</section>
"""


def human_hire_band(lang="fr"):
    if lang == "en":
        return """
<section class="tl-cta-band" id="mandat">
  <div class="container">
    <span class="tl-badge tl-badge-light">Hand us the search</span>
    <h2 class="tl-h2">A seat to fill? Hand us the brief.</h2>
    <p>A consultant takes the search. You meet people worth your time. Fees when someone starts.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Hand us the search</a>
      <a class="tl-btn tl-btn-ghost" href="hiring-need.html">Describe my need</a>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-cta-band" id="mandat">
  <div class="container">
    <span class="tl-badge tl-badge-light">Confier mon recrutement</span>
    <h2 class="tl-h2">Un poste à combler ? Confiez-nous le brief.</h2>
    <p>Un conseiller prend la recherche. Vous rencontrez des gens qui valent votre temps. Honoraires à l'embauche.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Confier mon recrutement</a>
      <a class="tl-btn tl-btn-ghost" href="besoin-de-recrutement.html">Décrire mon besoin</a>
    </div>
  </div>
</section>
"""


# Aligné sur backend/app/services/job_catalog.py :
# contrat = nature du lien, horaire = charge de la semaine, quart = moment.
CONTRACT_CHOICES = {
    "fr": ["Permanent", "Temporaire", "Contractuel", "Saisonnier", "Stage"],
    "en": ["Permanent", "Temporary", "Contract", "Seasonal", "Internship"],
}
SCHEDULE_CHOICES = {
    "fr": ["Temps plein", "Temps partiel", "Sur appel", "4 jours / 3"],
    "en": ["Full-time", "Part-time", "On call", "4 days / 3"],
}
SHIFT_CHOICES = {
    "fr": ["Quart de jour", "Quart de soir", "Quart de nuit", "Quarts rotatifs", "Fin de semaine", "Quarts brisés"],
    "en": ["Day shift", "Evening shift", "Night shift", "Rotating shifts", "Weekend", "Split shifts"],
}


def _plain_options(blank, values, extra=None):
    parts = [f'<option value="">{blank}</option>']
    parts.extend(f"<option>{v}</option>" for v in values)
    if extra:
        parts.append(f"<option>{extra}</option>")
    return "".join(parts)


def _hint(text):
    return f'<p class="tl-field-hint">{text}</p>'


def employer_need_fields(lang="fr"):
    """Champs du formulaire entreprise : secteur, poste, volume, localisation, contrat, besoins."""
    if lang == "en":
        sectors = _options(SECTOR_EXAMPLES["en"], "Select an industry")
        sectors += '<option value="autre">Other / several industries</option>'
        contracts = _plain_options("Select", CONTRACT_CHOICES["en"], "Several contract types")
        shifts = _plain_options("Select", SHIFT_CHOICES["en"])
        hours = _plain_options("Select", SCHEDULE_CHOICES["en"])
        return f"""
            <label>Industry</label>
            <select name="secteur">{sectors}</select>
            <label>Role to fill</label>
            <input name="poste" placeholder="e.g. accountant, developer, nurse, welder">
            <label>Number of hires</label>
            <input name="volume" type="number" min="1" value="1">
            <label>Location</label>
            <input name="localisation" placeholder="City, region or country">
            <label>Contract type</label>
            {_hint("Permanent, temporary, seasonal… — not weekly hours.")}
            <select name="contrat">{contracts}</select>
            <label>Shift</label>
            {_hint("Time of day or week.")}
            <select name="quart">{shifts}</select>
            <label>Hours</label>
            {_hint("Weekly workload: full-time, part-time, on call.")}
            <select name="horaire">{hours}</select>
            <label>What we should know</label>
            <textarea name="message" required placeholder="Responsibilities, must-have skills, experience, urgency, anything that will shape the search"></textarea>
        """
    sectors = _options(SECTOR_EXAMPLES["fr"], "Choisir un secteur")
    sectors += '<option value="autre">Autre / plusieurs secteurs</option>'
    contracts = _plain_options("Choisir", CONTRACT_CHOICES["fr"], "Plusieurs types de contrat")
    shifts = _plain_options("Choisir", SHIFT_CHOICES["fr"])
    hours = _plain_options("Choisir", SCHEDULE_CHOICES["fr"])
    return f"""
            <label>Secteur</label>
            <select name="secteur">{sectors}</select>
            <label>Poste recherché</label>
            <input name="poste" placeholder="ex. comptable, développeur, infirmier, soudeur">
            <label>Nombre de personnes à recruter</label>
            <input name="volume" type="number" min="1" value="1">
            <label>Localisation</label>
            <input name="localisation" placeholder="Ville, région ou pays">
            <label>Type de contrat</label>
            {_hint("Permanent, temporaire, saisonnier… — pas le temps plein ou partiel.")}
            <select name="contrat">{contracts}</select>
            <label>Quart</label>
            {_hint("Moment de la journée ou de la semaine.")}
            <select name="quart">{shifts}</select>
            <label>Horaire</label>
            {_hint("Charge dans la semaine : temps plein, partiel, sur appel.")}
            <select name="horaire">{hours}</select>
            <label>Ce que nous devons savoir</label>
            <textarea name="message" required placeholder="Responsabilités, compétences indispensables, expérience, urgence, tout ce qui orientera la recherche"></textarea>
        """


def job_search_filters(lang="fr"):
    """Filtres de recherche d'offres publiées par Talendus (côté candidat)."""
    if lang == "en":
        sectors = _options(SECTOR_EXAMPLES["en"], "All industries")
        types = _plain_options("All contract types", CONTRACT_CHOICES["en"])
        hours = _plain_options("Any hours", SCHEDULE_CHOICES["en"])
        shifts = _plain_options("Any shift", SHIFT_CHOICES["en"])
        return f"""
      <div class="tl-jobs-toolbar">
      <div class="tl-filters tl-filters-search" data-ai-ready="true">
        <label class="tl-filter tl-filter-search">
          <span>Role or skills</span>
          <input id="job-search" placeholder="Developer, Excel, welding, project management…">
        </label>
        <label class="tl-filter">
          <span>Location</span>
          <select id="job-city">
            <option value="">Anywhere</option>
            <option>Laval</option><option>Longueuil</option><option>Montreal</option>
            <option>Drummondville</option><option>Saint-Jérôme</option>
            <option>Sherbrooke</option><option>Boucherville</option>
            <option>Anjou</option><option>Trois-Rivières</option><option>Quebec City</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Contract type</span>
          <select id="job-type">{types}</select>
        </label>
        <label class="tl-filter">
          <span>Industry</span>
          <select id="job-sector">{sectors}</select>
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
          <span>Shift</span>
          <select id="job-shift">{shifts}</select>
        </label>
        <label class="tl-filter">
          <span>Hours</span>
          <select id="job-schedule">{hours}</select>
        </label>
        <label class="tl-filter">
          <span>Workplace</span>
          <select id="job-mode">
            <option value="">Any workplace</option>
            <option>On-site</option>
            <option>Hybrid</option>
            <option>Remote</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Salary</span>
          <select id="job-sal">
            <option value="">Any salary</option>
            <option value="18">$18/hr+</option>
            <option value="22">$22/hr+</option>
            <option value="25">$25/hr+</option>
            <option value="30">$30/hr+</option>
            <option value="40000">$40,000/yr+</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Category</span>
          <select id="job-cat">
            <option value="">All categories</option>
            <option value="technologie">Technology</option>
            <option value="production">Production</option>
            <option value="entrepot">Warehouse</option>
            <option value="metallurgie">Metals</option>
            <option value="manufacturier">Manufacturing</option>
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
      <div class="tl-jobs-toolbar-foot">
        <p class="tl-jobs-count" id="job-count"></p>
        <p class="tl-muted tl-ai-hint">Apply here: a consultant reviews your file and calls you. The simplest way to move forward.</p>
      </div>
      </div>
"""
    sectors = _options(SECTOR_EXAMPLES["fr"], "Tous les secteurs")
    types = _plain_options("Tous les types de contrat", CONTRACT_CHOICES["fr"])
    hours = _plain_options("Tous les horaires", SCHEDULE_CHOICES["fr"])
    shifts = _plain_options("Tous les quarts", SHIFT_CHOICES["fr"])
    return f"""
      <div class="tl-jobs-toolbar">
      <div class="tl-filters tl-filters-search" data-ai-ready="true">
        <label class="tl-filter tl-filter-search">
          <span>Métier ou compétences</span>
          <input id="job-search" placeholder="Développeur, Excel, soudure, gestion de projet…">
        </label>
        <label class="tl-filter">
          <span>Localisation</span>
          <select id="job-city">
            <option value="">Toutes les localisations</option>
            <option>Laval</option><option>Longueuil</option><option>Montréal</option>
            <option>Drummondville</option><option>Saint-Jérôme</option>
            <option>Sherbrooke</option><option>Boucherville</option>
            <option>Anjou</option><option>Trois-Rivières</option><option>Québec</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Type de contrat</span>
          <select id="job-type">{types}</select>
        </label>
        <label class="tl-filter">
          <span>Secteur</span>
          <select id="job-sector">{sectors}</select>
        </label>
        <label class="tl-filter">
          <span>Expérience</span>
          <select id="job-exp">
            <option value="">Toute expérience</option>
            <option value="debutant">Débutant</option>
            <option value="intermediaire">Intermédiaire</option>
            <option value="senior">Expérimenté</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Quart</span>
          <select id="job-shift">{shifts}</select>
        </label>
        <label class="tl-filter">
          <span>Horaire</span>
          <select id="job-schedule">{hours}</select>
        </label>
        <label class="tl-filter">
          <span>Présence</span>
          <select id="job-mode">
            <option value="">Toutes les présences</option>
            <option>Sur place</option>
            <option>Hybride</option>
            <option>Télétravail</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Salaire</span>
          <select id="job-sal">
            <option value="">Tout salaire</option>
            <option value="18">18 $/h et +</option>
            <option value="22">22 $/h et +</option>
            <option value="25">25 $/h et +</option>
            <option value="30">30 $/h et +</option>
            <option value="40000">40 000 $/an et +</option>
          </select>
        </label>
        <label class="tl-filter">
          <span>Catégorie</span>
          <select id="job-cat">
            <option value="">Toutes les catégories</option>
            <option value="technologie">Technologie</option>
            <option value="production">Production</option>
            <option value="entrepot">Entrepôt</option>
            <option value="metallurgie">Métallurgie</option>
            <option value="manufacturier">Manufacturier</option>
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
      <div class="tl-jobs-toolbar-foot">
        <p class="tl-jobs-count" id="job-count"></p>
        <p class="tl-muted tl-ai-hint">Postulez ici : un conseiller étudie votre dossier et vous rappelle. Le plus simple pour avancer.</p>
      </div>
      </div>
"""


def bad_hire_calculator_section(lang="fr"):
    if lang == "en":
        return """
<section class="tl-section" id="calculator">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Cost calculator</div>
      <h2 class="tl-h2">What a bad hire actually costs your company</h2>
      <p class="tl-lead">It is not “one salary too many”. It is the salary already paid, the training lost, overtime to cover the gap, and the search to start over. Enter the role’s salary: the estimate updates, line by line.</p>
    </div>
    <div class="tl-calc tl-calc-wide">
      <div class="tl-calc-grid">
        <div>
          <label for="tl-salary">Annual salary of the role</label>
          <input id="tl-salary" type="number" value="55000" min="0" step="1000" inputmode="numeric">
          <span class="tl-calc-hint">Gross annual salary, in Canadian dollars. Charges and benefits are not added on top.</span>
          <label for="tl-months">Months before you see it is the wrong person</label>
          <input id="tl-months" type="number" value="4" min="1" max="24">
          <span class="tl-calc-hint">Time already in the job (paid and trained) before the misfit is clear. Three to six months is common.</span>
        </div>
        <div>
          <p class="tl-calc-breakdown-title">Where the money goes</p>
          <ul class="tl-calc-lines">
            <li><span>Salary paid during that period</span><b id="tl-cost-paid">-</b></li>
            <li><span>Training and onboarding lost (35&nbsp;% of salary)</span><b id="tl-cost-training">-</b></li>
            <li><span>Overtime, lost productivity, search to restart</span><b id="tl-cost-restart">-</b></li>
          </ul>
          <div class="tl-calc-result">Estimated cost of a bad hire<br><b id="tl-cost">-</b></div>
        </div>
      </div>
      <p class="tl-calc-note">This is an order of magnitude, not an invoice. A Talendus mandate (search and screening included) always costs 5 to 8 times less than this total. And you avoid paying the wrong person for months.</p>
      <a class="tl-btn" href="contact.html">Hand us the search</a>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section" id="calculateur">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Calculateur de coût</div>
      <h2 class="tl-h2">Ce qu'une mauvaise embauche coûte vraiment à votre entreprise</h2>
      <p class="tl-lead">Ce n'est pas « un salaire de trop ». C'est le salaire déjà versé, la formation perdue, les heures supplémentaires pour couvrir le poste, et le recrutement à recommencer. Entrez le salaire du poste : le coût s'affiche, ligne par ligne.</p>
    </div>
    <div class="tl-calc tl-calc-wide">
      <div class="tl-calc-grid">
        <div>
          <label for="tl-salary">Salaire annuel du poste</label>
          <input id="tl-salary" type="number" value="55000" min="0" step="1000" inputmode="numeric">
          <span class="tl-calc-hint">Salaire brut annuel, en dollars canadiens. Les charges et avantages ne sont pas ajoutés par-dessus.</span>
          <label for="tl-months">Mois avant de constater que ce n'est pas la bonne personne</label>
          <input id="tl-months" type="number" value="4" min="1" max="24">
          <span class="tl-calc-hint">Le temps déjà en poste (payé et formé) avant que le décalage soit clair. Trois à six mois est fréquent.</span>
        </div>
        <div>
          <p class="tl-calc-breakdown-title">Où va l'argent</p>
          <ul class="tl-calc-lines">
            <li><span>Salaire versé pendant cette période</span><b id="tl-cost-paid">-</b></li>
            <li><span>Formation et intégration perdues (35&nbsp;% du salaire)</span><b id="tl-cost-training">-</b></li>
            <li><span>Heures sup., perte de productivité, recherche à relancer</span><b id="tl-cost-restart">-</b></li>
          </ul>
          <div class="tl-calc-result">Coût estimé d'une mauvaise embauche<br><b id="tl-cost">-</b></div>
        </div>
      </div>
      <p class="tl-calc-note">C'est un ordre de grandeur, pas une facture. Un mandat Talendus (recherche et présélection comprises) coûte toujours entre 5 et 8 fois moins que ce total. Et vous évitez de payer le mauvais profil pendant des mois.</p>
      <a class="tl-btn" href="contact.html">Confier mon recrutement</a>
    </div>
  </div>
</section>
"""


def homepage_after_hero(lang="fr"):
    talent = (
        for_candidates_section(lang)
        + candidate_journey_section(lang)
        + talent_cta_band(lang)
    )
    hire = (
        for_companies_section(lang)
        + process_section(lang)
        + why_talendus_section(lang)
        + ai_engine_section(lang)
        + human_hire_band(lang)
    )
    return (
        persona_switch_bar(lang)
        + persona_region("gateway", gateway_orientation_section(lang))
        + persona_region("talent", talent)
        + persona_region("entreprise", hire)
    )


def talent_trade_options(lang="fr"):
    if lang == "en":
        names = TRADE_EXAMPLES["en"] + ["Other"]
    else:
        names = TRADE_EXAMPLES["fr"] + ["Autre"]
    return "".join(f"<option>{n}</option>" for n in names)


# Conservé pour les imports existants (pages services, etc.).
def ai_coming_soon(lang="fr"):
    return ai_engine_section(lang)


JOB_EXP_LABEL = {
    "fr": {"debutant": "Débutant", "intermediaire": "Intermédiaire", "senior": "Expérimenté"},
    "en": {"debutant": "Entry-level", "intermediaire": "Mid-level", "senior": "Senior"},
}

JOB_CAT_LABEL = {
    "fr": {
        "entrepot": "Entrepôt", "production": "Production", "metallurgie": "Métallurgie",
        "manufacturier": "Manufacturier", "maintenance": "Maintenance", "supervision": "Supervision",
        "logistique": "Logistique", "cadres": "Cadres", "technologie": "Technologie",
        "finance": "Finance", "ingenierie": "Ingénierie", "transport": "Transport",
        "sante": "Santé", "commerce": "Commerce", "administration": "Administration",
        "marketing": "Marketing",
    },
    "en": {
        "entrepot": "Warehouse", "production": "Production", "metallurgie": "Metals",
        "manufacturier": "Manufacturing", "maintenance": "Maintenance", "supervision": "Supervision",
        "logistique": "Logistics", "cadres": "Leadership", "technologie": "Technology",
        "finance": "Finance", "ingenierie": "Engineering", "transport": "Transportation",
        "sante": "Healthcare", "commerce": "Retail", "administration": "Administration",
        "marketing": "Marketing",
    },
}


JOB_CAT_ICON = {
    "entrepot": "fa-warehouse",
    "production": "fa-industry",
    "metallurgie": "fa-fire",
    "manufacturier": "fa-gears",
    "maintenance": "fa-wrench",
    "supervision": "fa-user-tie",
    "logistique": "fa-boxes-stacked",
    "cadres": "fa-briefcase",
    "technologie": "fa-laptop-code",
    "finance": "fa-calculator",
    "ingenierie": "fa-compass-drafting",
    "transport": "fa-truck",
    "sante": "fa-heart-pulse",
    "commerce": "fa-store",
    "administration": "fa-building",
    "marketing": "fa-bullhorn",
}


def _job_icon(cat):
    return JOB_CAT_ICON.get(cat, "fa-briefcase")


JOB_SHIFT_BY_SLUG = {
    "operateur-production": ("Quarts rotatifs", "Rotating shifts"),
    "journalier-usine": ("Quart de soir", "Evening shift"),
    "electromecanicien": ("Quarts rotatifs", "Rotating shifts"),
    "infirmier": ("Quarts rotatifs", "Rotating shifts"),
    "vendeur": ("Quart de jour", "Day shift"),
}

JOB_MODE_BY_SLUG = {
    "developpeur": ("Hybride", "Hybrid"),
    "comptable": ("Hybride", "Hybrid"),
    "ingenieur": ("Hybride", "Hybrid"),
    "coordonnateur-logistique": ("Hybride", "Hybrid"),
    "responsable-rh": ("Hybride", "Hybrid"),
    "specialiste-marketing": ("Hybride", "Hybrid"),
}


def job_offer_traits(slug, lang="fr"):
    shift = JOB_SHIFT_BY_SLUG.get(slug, ("Quart de jour", "Day shift"))
    mode = JOB_MODE_BY_SLUG.get(slug, ("Sur place", "On-site"))
    i = 1 if lang == "en" else 0
    return {
        "shift": shift[i],
        "schedule": "Full-time" if lang == "en" else "Temps plein",
        "work_mode": mode[i],
        "languages": "French and English" if lang == "en" and slug in {"coordonnateur-logistique", "developpeur", "responsable-rh"} else ("Français et anglais" if slug in {"coordonnateur-logistique", "developpeur", "responsable-rh"} else ("French" if lang == "en" else "Français")),
    }


def _skill_chips(skills):
    parts = [s.strip() for s in (skills or "").replace(";", ",").split(",") if s.strip()]
    if not parts:
        return ""
    inner = "".join(f"<span>{p}</span>" for p in parts[:6])
    return f'<div class="tl-job-skills">{inner}</div>'


def _job_href(slug, lang="fr"):
    return f"job-{slug}.html" if lang == "en" else f"emploi-{slug}.html"


def job_card_html(job, lang="fr"):
    slug, title, city, cat, typ, sal, shift, req, sector, skills, exp = job
    traits = job_offer_traits(slug, lang)
    quart = traits["shift"]
    horaire = traits["schedule"]
    mode = traits["work_mode"]
    href = _job_href(slug, lang)
    exp_label = JOB_EXP_LABEL[lang].get(exp, exp)
    cat_label = JOB_CAT_LABEL[lang].get(cat, cat)
    icon = _job_icon(cat)
    chips = _skill_chips(skills)
    if lang == "en":
        cta = "View opening and apply"
        via = "Via Talendus"
        loc_l, pay_l, time_l, shift_l, profile_l = "Location", "Pay", "Hours", "Shift", "Profile we look for"
    else:
        cta = "Voir l'offre et postuler"
        via = "Via Talendus"
        loc_l, pay_l, time_l, shift_l, profile_l = "Lieu", "Rémunération", "Horaire", "Quart", "Profil recherché"
    return f'''
    <a class="tl-job-card" href="{href}" aria-label="{cta} : {title}" data-job="{title} {city} {cat} {typ} {sal} {horaire} {quart} {mode} {sector} {skills} {exp}" data-city="{city}" data-cat="{cat}" data-type="{typ}" data-shift="{quart}" data-schedule="{horaire}" data-mode="{mode}" data-salary="{sal}" data-sector="{sector}" data-skills="{skills}" data-exp="{exp}">
      <div class="tl-job-card-banner">
        <span class="tl-job-card-icon" aria-hidden="true"><i class="fa-solid {icon}"></i></span>
        <div class="tl-job-card-banner-text">
          <p class="tl-job-card-cat">{cat_label}</p>
          <p class="tl-job-card-via">{via}</p>
        </div>
      </div>
      <div class="tl-job-card-body">
        <div class="tl-job-card-top">
          <span class="tl-chip orange">{typ}</span>
          <span class="tl-chip">{exp_label}</span>
        </div>
        <h3>{title}</h3>
        <ul class="tl-job-pills">
          <li><i class="fa-solid fa-location-dot" aria-hidden="true"></i><span>{city}</span></li>
          <li class="is-pay"><i class="fa-solid fa-coins" aria-hidden="true"></i><span>{sal}</span></li>
          <li><i class="fa-solid fa-clock" aria-hidden="true"></i><span>{horaire}</span></li>
          <li><i class="fa-solid fa-layer-group" aria-hidden="true"></i><span>{quart}</span></li>
        </ul>
        <p class="tl-job-excerpt-label">{profile_l}</p>
        <p class="tl-job-excerpt">{req}</p>
        {chips}
      </div>
      <span class="tl-job-card-cta">{cta}</span>
    </a>'''


def jobs_listing_header(lang="fr"):
    if lang == "en":
        return """
<section class="tl-jobs-hero">
  <div class="container">
    <p class="tl-kicker">Job openings</p>
    <h1>Opportunities in every industry. Apply through Talendus.</h1>
    <p class="tl-lead">Filter the roles we publish, then send your file to our team. A consultant reviews it and calls you. You can also create a profile: many mandates are never posted.</p>
    <div class="tl-actions">
      <a class="tl-btn" href="candidates.html#cv">Create my profile</a>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-jobs-hero">
  <div class="container">
    <p class="tl-kicker">Offres d'emploi</p>
    <h1>Des opportunités, tous secteurs. Postulez via Talendus.</h1>
    <p class="tl-lead">Filtrez les postes que nous publions, puis envoyez votre dossier à notre équipe. Un conseiller l'étudie et vous rappelle. Vous pouvez aussi créer un profil : beaucoup de mandats n'apparaissent pas.</p>
    <div class="tl-actions">
      <a class="tl-btn" href="candidats.html#cv">Créer mon profil</a>
    </div>
  </div>
</section>
"""


def jobs_empty_state(lang="fr"):
    if lang == "en":
        return """
      <div class="tl-jobs-empty" id="job-empty" hidden>
        <p>No roles match these filters.</p>
        <a class="tl-btn" href="candidates.html#cv">Create my profile</a>
      </div>
"""
    return """
      <div class="tl-jobs-empty" id="job-empty" hidden>
        <p>Aucun poste ne correspond à ces filtres.</p>
        <a class="tl-btn" href="candidats.html#cv">Créer mon profil</a>
      </div>
"""


def _apply_form_html(slug, lang="fr"):
    accept = ".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg"
    if lang == "en":
        return f"""
          <form class="tl-form" data-form="apply" data-job-slug="{slug}" enctype="multipart/form-data">
            {HONEYPOT_INPUT}
            <label>Name <input name="name" required autocomplete="name"></label>
            <label>Email <input type="email" name="email" required autocomplete="email"></label>
            <label>Phone <input name="phone" autocomplete="tel"></label>
            <label class="tl-file">
              <span>Your resume</span>
              <input type="file" name="cvfile" accept="{accept}" required>
              <span class="tl-file-hint">PDF, Word (DOC, DOCX) or image (PNG, JPG). 5 MB max. The file reaches Talendus. A consultant calls you back.</span>
            </label>
            <label>Note for Talendus <span class="tl-optional">(optional)</span></label>
            <textarea name="message" rows="3" maxlength="4000" placeholder="Availability, permit, what you want us to know"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Send my application</button>
            <div class="tl-success"></div>
          </form>
"""
    return f"""
          <form class="tl-form" data-form="apply" data-job-slug="{slug}" enctype="multipart/form-data">
            {HONEYPOT_INPUT}
            <label>Nom <input name="nom" required autocomplete="name"></label>
            <label>Courriel <input type="email" name="courriel" required autocomplete="email"></label>
            <label>Téléphone <input name="tel" autocomplete="tel"></label>
            <label class="tl-file">
              <span>Votre CV</span>
              <input type="file" name="cvfile" accept="{accept}" required>
              <span class="tl-file-hint">PDF, Word (DOC, DOCX) ou image (PNG, JPG). 5 Mo max. Le fichier arrive chez Talendus. Un conseiller vous rappelle.</span>
            </label>
            <label>Note pour Talendus <span class="tl-optional">(facultatif)</span></label>
            <textarea name="message" rows="3" maxlength="4000" placeholder="Disponibilité, permis, ce que vous voulez qu'on sache"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Envoyer ma candidature</button>
            <div class="tl-success"></div>
          </form>
"""


def job_detail_html(job, related_html, lang="fr"):
    slug, title, city, cat, typ, sal, shift, req, sector, skills, exp = job
    traits = job_offer_traits(slug, lang)
    quart = traits["shift"]
    horaire = traits["schedule"]
    mode = traits["work_mode"]
    langs = traits["languages"]
    exp_label = JOB_EXP_LABEL[lang].get(exp, exp)
    cat_label = JOB_CAT_LABEL[lang].get(cat, cat)
    sector_label = JOB_CAT_LABEL[lang].get(sector, sector)
    icon = _job_icon(cat)
    chips = _skill_chips(skills)
    form = _apply_form_html(slug, lang)
    if lang == "en":
        listing = "jobs.html"
        talent = "candidates.html"
        return f"""
<section class="tl-job-page">
  <div class="container">
    <a class="tl-job-back" href="{listing}"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i> All openings</a>
    <header class="tl-job-hero">
      <div class="tl-job-hero-brand">
        <span class="tl-job-hero-icon" aria-hidden="true"><i class="fa-solid {icon}"></i></span>
        <div>
          <p class="tl-kicker">{cat_label} · {sector_label}</p>
          <h1>{title}</h1>
        </div>
      </div>
      <p class="tl-job-hero-lead">Talendus is recruiting this {title.lower()} role for an employer in {city}. Apply here: a consultant reviews your file and calls you. The simplest way to move forward.</p>
      <ul class="tl-job-hero-tags">
        <li>{typ}</li>
        <li>{exp_label}</li>
        <li>{horaire}</li>
        <li>{quart}</li>
        <li>Via Talendus</li>
      </ul>
    </header>
    <div class="tl-job-layout">
      <div class="tl-job-main">
        <ul class="tl-job-facts">
          <li><i class="fa-solid fa-location-dot" aria-hidden="true"></i><span>Location</span><strong>{city}</strong></li>
          <li><i class="fa-solid fa-sack-dollar" aria-hidden="true"></i><span>Pay</span><strong>{sal}</strong></li>
          <li><i class="fa-solid fa-clock" aria-hidden="true"></i><span>Hours</span><strong>{horaire}</strong></li>
          <li><i class="fa-solid fa-moon" aria-hidden="true"></i><span>Shift</span><strong>{quart}</strong></li>
          <li><i class="fa-solid fa-building" aria-hidden="true"></i><span>Workplace</span><strong>{mode}</strong></li>
          <li><i class="fa-solid fa-language" aria-hidden="true"></i><span>Languages</span><strong>{langs}</strong></li>
          <li><i class="fa-solid fa-file-contract" aria-hidden="true"></i><span>Type</span><strong>{typ}</strong></li>
          <li><i class="fa-solid fa-signal" aria-hidden="true"></i><span>Experience</span><strong>{exp_label}</strong></li>
          <li><i class="fa-solid fa-layer-group" aria-hidden="true"></i><span>Category</span><strong>{cat_label}</strong></li>
        </ul>
        <div class="tl-job-prose">
          <h2>The role</h2>
          <p>A {title.lower()} mandate in {city}, in {sector_label}. Skills in focus: {skills}.</p>
          <h2>Profile we look for</h2>
          <p>{req}</p>
          {chips}
          <h2>What the mandate includes</h2>
          <ul>
            <li>{typ} role, {horaire.lower()}, {quart.lower()}</li>
            <li>Pay: {sal}</li>
            <li>A Talendus consultant screens your file and calls you</li>
            <li>If it fits, we present you and stay with you through the next steps</li>
          </ul>
          <h2>How applying works</h2>
          <ol class="tl-job-steps">
            <li><span class="tl-job-step-n">1</span><div><strong>You apply here with your resume.</strong><p>PDF, Word or image. Your file reaches Talendus.</p></div></li>
            <li><span class="tl-job-step-n">2</span><div><strong>A consultant reviews it.</strong><p>We check the fit with the mandate before anything is shared.</p></div></li>
            <li><span class="tl-job-step-n">3</span><div><strong>If it holds, we present you.</strong><p>We speak to the employer on your behalf.</p></div></li>
            <li><span class="tl-job-step-n">4</span><div><strong>You follow the next steps with us.</strong><p>Interviews and updates go through Talendus.</p></div></li>
          </ol>
        </div>
        <p class="tl-job-alt"><a href="{listing}">Browse other openings</a> · <a href="{talent}">Create a talent profile</a></p>
      </div>
      <aside class="tl-job-aside">
        <div class="tl-job-apply-card" id="postuler">
          <p class="tl-job-apply-kicker">Apply</p>
          <h2>Send your file to Talendus</h2>
          <p>Upload your resume. A consultant studies your file and gets back to you. Call us if you want to move faster.</p>
          {form}
        </div>
      </aside>
    </div>
    <div class="tl-job-related">
      <h2>Other openings</h2>
      <div class="tl-jobs-grid">{related_html}</div>
    </div>
  </div>
</section>
<div class="tl-job-mobile-cta"><a class="tl-btn" href="#postuler">Apply with my resume</a></div>
"""
    listing = "emplois.html"
    talent = "candidats.html"
    return f"""
<section class="tl-job-page">
  <div class="container">
    <a class="tl-job-back" href="{listing}"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i> Toutes les offres</a>
    <header class="tl-job-hero">
      <div class="tl-job-hero-brand">
        <span class="tl-job-hero-icon" aria-hidden="true"><i class="fa-solid {icon}"></i></span>
        <div>
          <p class="tl-kicker">{cat_label} · {sector_label}</p>
          <h1>{title}</h1>
        </div>
      </div>
      <p class="tl-job-hero-lead">Talendus recrute ce poste de {title.lower()} pour un employeur à {city}. Postulez ici : un conseiller étudie votre dossier et vous rappelle. Le plus simple pour avancer.</p>
      <ul class="tl-job-hero-tags">
        <li>{typ}</li>
        <li>{exp_label}</li>
        <li>{horaire}</li>
        <li>{quart}</li>
        <li>Via Talendus</li>
      </ul>
    </header>
    <div class="tl-job-layout">
      <div class="tl-job-main">
        <ul class="tl-job-facts">
          <li><i class="fa-solid fa-location-dot" aria-hidden="true"></i><span>Lieu</span><strong>{city}</strong></li>
          <li><i class="fa-solid fa-sack-dollar" aria-hidden="true"></i><span>Rémunération</span><strong>{sal}</strong></li>
          <li><i class="fa-solid fa-clock" aria-hidden="true"></i><span>Horaire</span><strong>{horaire}</strong></li>
          <li><i class="fa-solid fa-moon" aria-hidden="true"></i><span>Quart</span><strong>{quart}</strong></li>
          <li><i class="fa-solid fa-building" aria-hidden="true"></i><span>Présence</span><strong>{mode}</strong></li>
          <li><i class="fa-solid fa-language" aria-hidden="true"></i><span>Langues</span><strong>{langs}</strong></li>
          <li><i class="fa-solid fa-file-contract" aria-hidden="true"></i><span>Type</span><strong>{typ}</strong></li>
          <li><i class="fa-solid fa-signal" aria-hidden="true"></i><span>Expérience</span><strong>{exp_label}</strong></li>
          <li><i class="fa-solid fa-layer-group" aria-hidden="true"></i><span>Catégorie</span><strong>{cat_label}</strong></li>
        </ul>
        <div class="tl-job-prose">
          <h2>Le poste</h2>
          <p>Un mandat de {title.lower()} à {city}, en {sector_label}. Compétences visées : {skills}.</p>
          <h2>Profil recherché</h2>
          <p>{req}</p>
          {chips}
          <h2>Ce que comprend le mandat</h2>
          <ul>
            <li>Poste {typ.lower()}, {horaire.lower()}, {quart.lower()}</li>
            <li>Rémunération : {sal}</li>
            <li>Un conseiller Talendus étudie votre dossier et vous rappelle</li>
            <li>Si ça colle, nous vous présentons et restons avec vous pour la suite</li>
          </ul>
          <h2>Comment postuler</h2>
          <ol class="tl-job-steps">
            <li><span class="tl-job-step-n">1</span><div><strong>Vous postulez ici avec votre CV.</strong><p>PDF, Word ou image. Votre dossier arrive chez Talendus.</p></div></li>
            <li><span class="tl-job-step-n">2</span><div><strong>Un conseiller l'étudie.</strong><p>Nous vérifions la correspondance avec le mandat avant tout partage.</p></div></li>
            <li><span class="tl-job-step-n">3</span><div><strong>Si ça colle, nous vous présentons.</strong><p>Nous parlons à l'employeur pour vous.</p></div></li>
            <li><span class="tl-job-step-n">4</span><div><strong>Vous suivez la suite avec nous.</strong><p>Entretiens et nouvelles passent par Talendus.</p></div></li>
          </ol>
        </div>
        <p class="tl-job-alt"><a href="{listing}">Voir les autres offres</a> · <a href="{talent}">Créer un profil talent</a></p>
      </div>
      <aside class="tl-job-aside">
        <div class="tl-job-apply-card" id="postuler">
          <p class="tl-job-apply-kicker">Candidature</p>
          <h2>Envoyez votre dossier à Talendus</h2>
          <p>Téléversez votre CV. Un conseiller étudie votre dossier et vous relance. Appelez-nous si vous voulez aller plus vite.</p>
          {form}
        </div>
      </aside>
    </div>
    <div class="tl-job-related">
      <h2>Autres opportunités</h2>
      <div class="tl-jobs-grid">{related_html}</div>
    </div>
  </div>
</section>
<div class="tl-job-mobile-cta"><a class="tl-btn" href="#postuler">Postuler avec mon CV</a></div>
"""


def related_job_cards(jobs, current_slug, lang="fr"):
    current = next((j for j in jobs if j[0] == current_slug), None)
    if not current:
        return ""
    same = [j for j in jobs if j[0] != current_slug and (j[3] == current[3] or j[8] == current[8])]
    rest = [j for j in jobs if j[0] != current_slug and j not in same]
    picked = (same + rest)[:3]
    return "".join(job_card_html(j, lang) for j in picked)
