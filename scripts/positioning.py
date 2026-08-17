"""Positionnement Talendus — agence de placement intelligente.

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
            "Help the Talendus team — not replace the consultant.",
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
        ("Peu de visibilité", "Les talents disponibles — y compris déjà en poste — restent souvent hors radar."),
    ],
    "en": [
        ("Finding the right people", "The pool is large. Truly relevant profiles are not. Browsing resumes is not a strategy."),
        ("Not enough time", "Hiring sits on top of the day job. Weeks slip by and the seat stays empty."),
        ("Too many applications", "Sorting dozens of files is not a process. It is noise that delays the decision."),
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
      <h2 class="tl-h2">You have a role to fill? Don't spend your weeks sorting applications.</h2>
      <p>Hand the need to Talendus. We are not a job board where you browse candidates yourself, and not a software tool that leaves the search on your desk. We are a placement agency: you describe the role, we take on the work of finding, screening and qualifying people.</p>
      <p>Our team studies the mandate, searches across our network and the profiles we already know, analyses resumes, speaks with candidates when needed, and presents a qualified shortlist. You keep the final decision. We do the work you should not have to do alone: understand the need, identify talent, compare skills, run first conversations, and put only relevant files in front of you.</p>
      <p>Talendus already uses artificial intelligence in its internal tools to speed up search, analysis and screening. You benefit from that power without using the tools yourself: we mobilize them to find and qualify the most relevant profiles for your need. Consultants remain essential to confirm fit, motivations and context.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Hand us the search</a>
        <a class="tl-btn tl-btn-ghost-dark" href="employers.html">How we work with companies</a>
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
      <h2 class="tl-h2">Vous avez un poste à pourvoir ? Ne perdez pas votre temps à parcourir des candidatures.</h2>
      <p>Confiez votre besoin à Talendus. Nous ne sommes pas un site d'emplois où vous cherchez vous-même les candidats, ni un logiciel qui vous laisse gérer le recrutement seul. Nous sommes une agence de placement : vous décrivez le poste, nous prenons en charge la recherche, l'analyse et la présélection.</p>
      <p>L'équipe étudie le mandat, recherche dans son réseau et parmi les profils déjà connus, analyse les parcours, échange avec les candidats lorsque c'est nécessaire, puis vous présente une sélection qualifiée. Vous gardez la décision finale. Talendus fait le travail que vous ne souhaitez pas ou ne pouvez pas mener seul : comprendre le besoin, identifier les talents, comparer les compétences, mener les premiers échanges et ne mettre devant vous que des dossiers pertinents.</p>
      <p>Talendus utilise déjà l'intelligence artificielle dans ses outils internes pour accélérer la recherche, l'analyse et la présélection des talents. Vous bénéficiez de cette puissance sans avoir à utiliser les outils vous-même : nous les mobilisons pour rechercher et qualifier les profils les plus pertinents pour votre besoin. Les conseillers restent essentiels pour confirmer la pertinence, les motivations et le contexte.</p>
      <div class="tl-actions" style="margin-top:28px">
        <a class="tl-btn" href="contact.html">Confier mon recrutement</a>
        <a class="tl-btn tl-btn-ghost-dark" href="entreprises.html">Comment nous accompagnons les entreprises</a>
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
      <p>Talendus is the professional intermediary between you and companies. You create a profile, share your career, resume, skills and preferences. We study that information. When your profile fits an opportunity, we can contact you, talk with you, and — when the fit holds — present you to an employer.</p>
      <p>You may also apply to openings we publish. In every case, the company does not receive your email or phone number. A consultant presents your file and remains your contact. You are accompanied: screening, conversations, interviews when needed, then a possible introduction. Nothing is sent blindly to fifteen employers.</p>
      <p>Creating a profile is free. Fees are paid by the company. Our role is to understand your path and to consider you for mandates that actually match — not to flood you with interviews that go nowhere.</p>
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
      <p>Talendus est l'intermédiaire professionnel entre vous et les entreprises. Vous créez un profil, renseignez votre parcours, transmettez votre CV, indiquez vos compétences et vos préférences. Nous étudions ces informations. Lorsque votre profil correspond à une opportunité, Talendus peut vous contacter, échanger avec vous, puis — si l'adéquation tient — vous présenter à une entreprise.</p>
      <p>Vous pouvez aussi postuler aux offres que nous publions. Dans tous les cas, l'employeur ne reçoit pas votre courriel ni votre téléphone. Un conseiller présente votre dossier et reste votre interlocuteur. Vous êtes accompagné : analyse, échanges, étapes de sélection si nécessaire, puis une présentation éventuelle. Rien n'est envoyé à l'aveugle chez quinze employeurs.</p>
      <p>Créer un profil est gratuit. Les honoraires sont payés par l'entreprise. Notre rôle est de comprendre votre parcours et de vous considérer pour des mandats qui collent vraiment — pas de vous noyer sous des entrevues qui n'aboutissent pas.</p>
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
            ("Technology", "Modern tools help Talendus structure needs, track mandates and move faster — without turning hiring into self-serve software for the company."),
            ("Artificial intelligence", "Talendus already uses AI in its internal tools to analyse, search, compare and process information faster. It supports our teams. It does not choose the hire, and it is not a tool we hand to recruiters to search on their own."),
            ("Human expertise", "Consultants verify real fit, speak with candidates, weigh professional personality and context, and qualify the files we present."),
            ("Market knowledge", "We work with companies of every size and with candidates at every level. Understanding both sides is what makes a shortlist useful."),
            ("Selection", "We do not sell volume. We do not send a pile of resumes. The aim is to present the most relevant profiles, so you can focus on the final choice."),
        ]
        kicker, heading, lead = "Our approach", "How Talendus works.", "Technology, AI and human expertise serve one process: search, screen, qualify, present."
    else:
        items = [
            ("Technologie", "Des outils modernes aident Talendus à structurer les besoins, suivre les mandats et avancer plus vite — sans transformer le recrutement en logiciel en libre-service pour l'entreprise."),
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
        kicker, heading = "How our recruiting works", "You hand us the need. We do the search."
        steps = [
            ("01", "You hand us the need", "Describe the role and the profile you are looking for."),
            ("02", "We talk with you", "Our team goes deeper so we understand the context, constraints and the kind of person you actually need."),
            ("03", "We define the profile", "We set the search criteria: must-haves, nice-to-haves, experience, location and conditions."),
            ("04", "We start the search", "Our teams use their methods, network, technology and internal AI tools. You do not hunt candidates yourself."),
            ("05", "We screen", "We analyse and qualify the people we identified. You do not receive a pile of resumes."),
            ("06", "We meet candidates", "We run the evaluation steps required for the mandate: conversations, checks, availability."),
            ("07", "We present the best profiles", "You receive a selection of relevant candidates we are prepared to stand behind."),
            ("08", "You choose", "You review, meet people according to your process, and make the final decision. Talendus does not hire in your place."),
        ]
    else:
        kicker, heading = "Comment fonctionne notre recrutement ?", "Vous nous confiez votre besoin. Nous faisons la recherche."
        steps = [
            ("01", "Vous nous confiez votre besoin", "Décrivez-nous le poste et le profil recherché."),
            ("02", "Nous échangeons avec vous", "Nos équipes approfondissent votre besoin afin de comprendre précisément vos attentes."),
            ("03", "Nous définissons le profil", "Nous établissons les critères nécessaires à la recherche."),
            ("04", "Nous lançons la recherche", "Nos équipes utilisent leurs méthodes, leurs ressources, leur technologie et leurs outils IA."),
            ("05", "Nous présélectionnons", "Nous analysons et qualifions les profils identifiés."),
            ("06", "Nous rencontrons les candidats", "Nous réalisons les étapes d'évaluation nécessaires."),
            ("07", "Nous vous présentons les meilleurs profils", "Vous recevez une sélection de candidats pertinents."),
            ("08", "Vous choisissez", "Vous prenez la décision finale."),
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
    </div>
    <div class="tl-steps tl-steps-8">{cards}</div>
  </div>
</section>
"""


def why_talendus_section(lang="fr"):
    if lang == "en":
        kicker, heading = "Why go through Talendus", "Because hiring well is a job. You already have one."
        items = [
            ("Save time", "Talendus takes on a large part of the search and screening. You describe the role and stay available for the conversations that matter. You do not spend evenings sorting applications that will never fit."),
            ("Reach more talent", "We draw on several sources: people who apply, people already in our network, and people who are not looking publicly. A company acting alone usually sees only who answered an ad."),
            ("Receive qualified applications", "The aim is to cut noise and put your attention on relevant profiles. A shortlist you can actually review is worth more than a hundred unread resumes."),
            ("A search already strengthened by AI", "Talendus already uses AI internally to analyse resumes, skills and criteria faster. You benefit from that work without operating the tools yourself. They are not a self-serve engine for you to hunt candidates on Talendus."),
            ("A human selection", "Profiles are not forwarded automatically. Consultants review, speak with people when needed, and qualify what we present. Fit is more than keywords on a resume."),
            ("One contact", "You hand the need to Talendus and work with a consultant through to the decision. Candidates and companies stay on their own side. We remain the intermediary."),
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
            ("Un interlocuteur unique", "Vous confiez votre besoin à Talendus et travaillez avec un conseiller jusqu'à la décision. Candidats et entreprises restent chacun de leur côté. Nous restons l'intermédiaire."),
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
      <div class="tl-kicker">Two sides. No mix-up.</div>
      <h2 class="tl-h2">Talendus does not put companies and candidates in the same flow.</h2>
      <p class="tl-lead">Choose your side. The next pages, the actions and the support follow that choice.</p>
    </div>
    <div class="tl-gateway-lanes">
      <article class="tl-gateway-lane is-talent">
        <span class="tl-kicker">Candidates</span>
        <h3>You are looking for a job</h3>
        <p>Create a profile, submit your resume. We study your path and contact you when an opportunity fits. Companies do not receive your email or phone number. It is free.</p>
        <a class="tl-btn" href="candidates.html" data-set-persona="talent">Create my profile</a>
      </article>
      <article class="tl-gateway-lane is-hire">
        <span class="tl-kicker">Employers</span>
        <h3>You are hiring</h3>
        <p>Hand us the need. We search, screen and present a qualified shortlist. You do not browse a resume database. You keep the final decision.</p>
        <a class="tl-btn" href="employers.html" data-set-persona="entreprise">Hand us the search</a>
      </article>
    </div>
  </div>
</section>
"""
    return """
<section class="tl-section" id="parcours">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Deux côtés. Aucun mélange.</div>
      <h2 class="tl-h2">Talendus ne met pas les entreprises et les candidats dans le même parcours.</h2>
      <p class="tl-lead">Choisissez votre côté. Les pages suivantes, les actions et l'accompagnement suivent ce choix.</p>
    </div>
    <div class="tl-gateway-lanes">
      <article class="tl-gateway-lane is-talent">
        <span class="tl-kicker">Candidats</span>
        <h3>Vous cherchez un emploi</h3>
        <p>Créez un profil, déposez votre CV. Nous étudions votre parcours et vous contactons lorsqu'une opportunité correspond. Les entreprises ne reçoivent pas votre courriel ni votre téléphone. C'est gratuit.</p>
        <a class="tl-btn" href="candidats.html" data-set-persona="talent">Créer mon profil</a>
      </article>
      <article class="tl-gateway-lane is-hire">
        <span class="tl-kicker">Entreprises</span>
        <h3>Vous recrutez</h3>
        <p>Confiez-nous votre besoin. Nous recherchons, présélectionnons et vous présentons une shortlist qualifiée. Vous ne parcourez pas une base de CV. Vous gardez la décision finale.</p>
        <a class="tl-btn" href="entreprises.html" data-set-persona="entreprise">Confier mon recrutement</a>
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
      <p class="tl-lead">Talendus already uses AI internally to speed up search, analyse profiles, spot correspondences, support screening and structure information — so our recruiters can focus on human qualification.</p>
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
      <p class="tl-lead">Talendus utilise déjà l'IA en interne pour accélérer la recherche, analyser les profils, identifier les correspondances, aider à la présélection et structurer les informations — afin que nos recruteurs se concentrent sur la qualification humaine.</p>
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
      <p class="tl-lead">Technology and AI are Talendus's operational advantage — not a software product we sell instead of placement.</p>
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
      <p class="tl-lead">La technologie et l'IA constituent l'avantage opérationnel de Talendus — pas un logiciel que nous vendons à la place du placement.</p>
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
            ("Talent search", "Talendus looks for people who match the company's need — not a public dump of every resume we hold. We draw on our network, known profiles, applications received and, when useful, a framed posting. People already in a role can be approached discreetly, without internal noise. Internal tools, including artificial intelligence, help our teams cover more ground, treat large volumes of information and spot correspondences worth a human look. You do not browse a candidate database and you do not operate a search engine. You describe the role; we open the search on your behalf, then we come back with profiles that actually relate to the mandate."),
            ("Screening", "Identified profiles are analysed and filtered against skills, experience, qualifications, location and the criteria we agreed with you. AI can help with a first pass, with structuring information and with prioritizing files for review. A Talendus consultant then verifies what holds and drops what does not. What fails that filter never reaches your desk. Screening is a professional step, not an automatic reject and not a pile of unread resumes left for you to sort. The aim is to reduce noise so your time goes to people worth meeting."),
            ("Qualification", "Talendus does not merely forward resumes. We structure qualification around the path, consistency with the role, skills, experience, motivations, availability, expectations and other criteria defined with you. AI can help process and analyse information faster, including synthesizing what a file actually shows. Final qualification stays human: a consultant weighs what a CV cannot say, speaks with the person when needed, and decides whether a file is ready to present. You receive a reasoned file, not a raw document dumped into your inbox."),
            ("Interviews", "When needed, Talendus talks with candidates before a file reaches you: path, motivations, fit with the role and the conditions of the mandate. Your interviews then involve people already qualified, not a first filter of dozens of unvetted applications. You run your own process; we remain the intermediary. Candidates and companies do not contact each other outside Talendus. We coordinate the exchanges, keep context, and stay available so neither side is left alone in front of a listing or a resume pile."),
            ("Shortlist", "We present a qualified selection of relevant profiles, not a massive list. Each file is one we are prepared to stand behind after search, analysis and human review. Relevance is the product; volume is not. You study those files, meet people according to your process, and choose. Talendus does not hire in your place. We make the final choice possible — and faster — by doing the search and screening first, with internal tools and AI accelerating some of that work without transferring it onto you."),
            ("Placement", "Talendus supports the introduction through to the planned hiring steps: presentation of the file, follow-up with both sides, coordination of exchanges and, on permanent mandates, onboarding follow-up at 30, 60 and 90 days. We stay between the company and the talent. There is no unmediated channel and no self-serve inbox. Fees are success-based, per the agreement, with a replacement guarantee on permanent mandates. Placement is the close of a recruiting process we ran for you — not access to software you would have to operate yourself."),
            ("AI-accelerated search", "Talendus already uses its artificial-intelligence tools to accelerate certain search and analysis steps: resume reading, skills extraction, relating a profile to a role, synthesis and internal prioritization. These tools sit inside our process; they are not a product you log into. You benefit from that power through the quality and speed of the Talendus service. Consultants remain essential to qualify, contact, interview and present. The company keeps the final decision. AI helps us work better, faster and more intelligently — it does not replace the agency."),
        ]
        kicker, heading, lead = (
            "From need to placement",
            "A complete recruiting process — not a software catalogue.",
            "Each service is a step Talendus runs for you. Technology and AI strengthen the work. They do not replace the agency.",
        )
    else:
        services = [
            ("Recherche de talents", "Talendus recherche les profils correspondant au besoin de l'entreprise — pas un dépôt public de tous les CV que nous détenons. Nous mobilisons le réseau, les profils déjà connus, les candidatures reçues et, lorsque c'est utile, une offre cadrée. Les personnes déjà en poste peuvent être approchées discrètement, sans bruit interne. Les outils internes, dont l'intelligence artificielle, aident nos équipes à couvrir davantage de terrain, à traiter de grands volumes d'informations et à faire ressortir des correspondances qui méritent une revue humaine. Vous ne parcourez pas une base de candidats et vous n'opérez pas un moteur de recherche. Vous décrivez le poste ; nous ouvrons la recherche pour votre compte, puis nous revenons avec des profils réellement liés au mandat."),
            ("Présélection", "Les profils identifiés sont analysés et filtrés : compétences, expérience, qualifications, localisation et critères convenus avec vous. L'IA peut aider à un premier passage, à structurer l'information et à prioriser les dossiers à examiner. Un conseiller Talendus vérifie ensuite ce qui tient et écarte ce qui ne correspond pas. Ce qui échoue ce filtre n'arrive pas sur votre bureau. La présélection est une étape professionnelle, pas un rejet automatique et pas une pile de CV non lus à trier vous-même. L'objectif est de réduire le bruit pour que votre temps aille aux personnes à rencontrer."),
            ("Qualification", "Talendus ne se contente pas d'envoyer des CV. Nous structurons la qualification autour du parcours, de la cohérence avec le poste, des compétences, de l'expérience, des motivations, de la disponibilité, des attentes et des autres critères définis avec vous. L'IA peut contribuer au traitement et à l'analyse de l'information, y compris en synthétisant ce qu'un dossier montre vraiment. La qualification finale reste humaine : un conseiller pèse ce qu'un CV ne dit pas, échange avec la personne lorsque c'est nécessaire, et décide si un dossier est prêt à être présenté. Vous recevez un dossier raisonné, pas un document brut déposé dans votre boîte."),
            ("Entretiens", "Lorsque c'est nécessaire, Talendus échange avec les candidats avant qu'un dossier vous parvienne : parcours, motivations, adéquation avec le poste et conditions du mandat. Vos entretiens portent ensuite sur des personnes déjà qualifiées, pas sur un premier filtre de dizaines de candidatures non vérifiées. Vous organisez votre processus ; nous restons l'intermédiaire. Candidats et entreprises ne se contactent pas hors de Talendus. Nous coordonnons les échanges, conservons le contexte et restons disponibles pour qu'aucun des deux côtés ne soit laissé seul devant une annonce ou une pile de CV."),
            ("Shortlist", "Nous présentons une sélection de profils qualifiés et pertinents, pas une liste massive. Chaque dossier est un profil que nous sommes prêts à défendre après recherche, analyse et revue humaine. La pertinence est le produit ; le volume ne l'est pas. Vous étudiez ces dossiers, rencontrez les personnes selon votre processus, et choisissez. Talendus n'embauche pas à votre place. Nous rendons le choix final possible — et plus rapide — en menant d'abord la recherche et la présélection, avec des outils internes et l'IA qui accélèrent une partie de ce travail sans le transférer vers vous."),
            ("Placement", "Talendus accompagne la mise en relation jusqu'aux étapes prévues du recrutement : présentation du dossier, suivi auprès des deux parties, coordination des échanges et, sur les mandats permanents, suivi d'intégration à 30, 60 et 90 jours. Nous restons entre l'entreprise et le talent. Il n'y a pas de canal direct non médié ni de messagerie en libre-service. Les honoraires sont au succès, selon l'entente, avec une garantie de remplacement sur les mandats permanents. Le placement clôt un processus de recrutement que nous avons mené pour vous — ce n'est pas l'accès à un logiciel que vous auriez à opérer vous-même."),
            ("Recherche accélérée par l'IA", "Talendus utilise déjà ses outils d'intelligence artificielle pour accélérer certaines étapes de la recherche et de l'analyse : lecture des CV, extraction des compétences, rapprochement d'un profil et d'un poste, synthèse et priorisation interne. Ces outils restent dans notre processus ; ce n'est pas un produit auquel vous vous connectez. Vous bénéficiez de cette puissance à travers la qualité et la rapidité du service Talendus. Les conseillers restent essentiels pour qualifier, contacter, interviewer et présenter. L'entreprise garde la décision finale. L'IA nous aide à travailler mieux, plus vite et plus intelligemment — elle ne remplace pas l'agence."),
        ]
        kicker, heading, lead = (
            "Du besoin au placement",
            "Un processus de recrutement complet — pas un catalogue de logiciels.",
            "Chaque service est une étape que Talendus mène pour vous. La technologie et l'IA renforcent le travail. Elles ne remplacent pas l'agence.",
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
    <div class="tl-grid-2 tl-services-process">{cards}</div>
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
      <p>A useful profile is more than a list of tools and job titles. Talendus also needs to understand motivations, the real path, ambitions, professional personality, expectations, the context of the role and — when it matters — the culture of the organization. That reading does not come out of a score. It comes from people who speak with candidates and who have understood the mandate.</p>
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
      <p>Un profil utile, ce n'est pas seulement une liste d'outils et de titres. Talendus doit aussi comprendre les motivations, le parcours réel, les ambitions, la personnalité professionnelle, les attentes, le contexte du poste et — lorsque c'est pertinent — la culture de l'organisation. Cette lecture ne sort pas d'un score. Elle vient de personnes qui parlent aux candidats et qui ont compris le mandat.</p>
      <p>Nos conseillers restent essentiels : ils vérifient si une correspondance est réelle, ils mènent les échanges, ils évaluent ce qu'un CV ne dit pas, ils confirment l'adéquation, et ils présentent les dossiers. L'IA nous aide déjà à traiter plus vite les informations. Elle ne remplace pas ce jugement. L'entreprise garde la décision finale. L'humain, des deux côtés, reste au centre de la qualification.</p>
    </div>
  </div>
</section>
"""


def company_types_section(lang="fr"):
    if lang == "en":
        items = [
            ("First hire", "A company recruiting its first employee still needs a serious search. We take the mandate with the same care as a larger file."),
            ("Growing SME", "Several seats, mixed roles, limited HR time: we absorb the search so growth does not stall on vacant posts."),
            ("Startup", "A specialized or hybrid profile, often urgent. We clarify the real need before we search — titles in startups drift."),
            ("Larger organization", "Volume, confidentiality, several stakeholders. One Talendus contact, a qualified shortlist, you keep the decision."),
        ]
        kicker, heading = "Who we work with", "From the first employee to specialized roles."
    else:
        items = [
            ("Premier employé", "Une entreprise qui recrute sa première personne a tout autant besoin d'une recherche sérieuse. Nous prenons le mandat avec le même soin qu'un dossier plus large."),
            ("PME en croissance", "Plusieurs postes, métiers mixtes, peu de temps RH : nous absorbons la recherche pour que la croissance ne bloque pas sur des sièges vides."),
            ("Startup", "Un profil spécialisé ou hybride, souvent urgent. Nous clarifions le besoin réel avant de chercher — les titres bougent vite en startup."),
            ("Grande organisation", "Volume, confidentialité, plusieurs interlocuteurs. Un contact Talendus, une shortlist qualifiée, vous gardez la décision."),
        ]
        kicker, heading = "Pour qui", "Du premier employé aux profils très spécialisés."
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
            ("02", "Submit your resume", "A link or an upload. We use it to understand your path. Companies do not receive the document until we present you — and they still do not get your direct contact details."),
            ("03", "Skills and preferences", "What you know how to do, where you can work, the kind of role you want. The clearer this is, the more useful our search for you becomes."),
            ("04", "Opportunities", "You can browse openings we publish and apply. Many mandates never appear: your profile stays active and we can contact you when a fit appears."),
            ("05", "Identified for a role", "When your profile matches a need, Talendus can reach out. We do not send you blindly to fifteen employers."),
            ("06", "Talk with Talendus", "A consultant is your contact. Screening, questions, sometimes an interview with us — before any introduction to a company."),
            ("07", "Presented when it fits", "If the fit holds, we present your file. You keep control: you can decline. The company chooses. We remain in the middle."),
            ("08", "Follow your path", "In your workspace: applications, messages with Talendus, interviews we schedule. No direct employer inbox."),
        ]
    else:
        kicker, heading = "Votre parcours", "Du profil à une présentation éventuelle."
        steps = [
            ("01", "Créer votre profil", "Nom, métier, région, compétences et préférences. Cinq minutes pour entrer dans le réseau Talendus. Ce n'est pas un dépôt public de CV : c'est un dossier que notre équipe peut étudier."),
            ("02", "Déposer votre CV", "Un lien ou un fichier. Nous l'utilisons pour comprendre votre parcours. Les entreprises ne reçoivent le document que lorsque nous vous présentons — et elles n'ont toujours pas vos coordonnées directes."),
            ("03", "Compétences et préférences", "Ce que vous savez faire, où vous pouvez travailler, le type de poste visé. Plus c'est clair, plus notre recherche pour vous est utile."),
            ("04", "Opportunités", "Vous pouvez consulter les offres que nous publions et postuler. Beaucoup de mandats n'apparaissent pas : votre profil reste actif et nous pouvons vous contacter lorsqu'une correspondance se présente."),
            ("05", "Identifié pour un poste", "Lorsque votre profil correspond à un besoin, Talendus peut vous joindre. Nous ne vous envoyons pas à l'aveugle chez quinze employeurs."),
            ("06", "Échanger avec Talendus", "Un conseiller est votre interlocuteur. Analyse, questions, parfois un entretien avec nous — avant toute présentation à une entreprise."),
            ("07", "Présenté si ça colle", "Si l'adéquation tient, nous présentons votre dossier. Vous gardez la main : vous pouvez refuser. L'entreprise choisit. Nous restons au milieu."),
            ("08", "Suivre votre parcours", "Dans votre espace : candidatures, messages avec Talendus, entretiens que nous planifions. Pas de boîte de réception employeur en direct."),
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
    """Page « besoin de recrutement » — 8 étapes côté entreprise."""
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
      <p>This is not a job-posting form. It helps Talendus understand the mandate so we can contact you, define the profile and take on the search.</p>
    </div>
    <form class="tl-form" action="#" method="post" data-form="hiring-need" style="max-width:720px;margin:0 auto">
      <input type="hidden" name="profil" value="Employer — hiring need">
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
      <p>Ce n'est pas un formulaire de publication. Il permet à Talendus de comprendre le mandat, de vous recontacter et de définir le profil recherché avant de lancer la recherche.</p>
    </div>
    <form class="tl-form" action="#" method="post" data-form="hiring-need" style="max-width:720px;margin:0 auto">
      <input type="hidden" name="profil" value="Employeur — je recrute">
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
    <h2 class="tl-h2">Hiring? Tell Talendus about the role.</h2>
    <p>Whatever your industry, describe the need. We search, screen and present a qualified shortlist. You keep the final decision.</p>
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
    <h2 class="tl-h2">Vous recrutez ? Confiez-nous votre besoin.</h2>
    <p>Quel que soit votre secteur, décrivez le poste. Nous recherchons, présélectionnons et vous présentons une shortlist qualifiée. Vous gardez la décision finale.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Confier mon recrutement</a>
      <a class="tl-btn tl-btn-ghost" href="besoin-de-recrutement.html">Décrire mon besoin</a>
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
            <label>What we should know</label>
            <textarea name="message" required placeholder="Responsibilities, must-have skills, experience, urgency, anything that will shape the search"></textarea>
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
            <label>Ce que nous devons savoir</label>
            <textarea name="message" required placeholder="Responsabilités, compétences indispensables, expérience, urgence, tout ce qui orientera la recherche"></textarea>
        """


def job_search_filters(lang="fr"):
    """Filtres de recherche d'offres publiées par Talendus (côté candidat)."""
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
      <p class="tl-muted tl-ai-hint">These filters help you browse openings Talendus publishes. Applying still goes through us: a consultant presents your file. Intelligent ranking of candidates for employers is not a self-serve feature.</p>
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
      <p class="tl-muted tl-ai-hint">Ces filtres vous aident à parcourir les offres que Talendus publie. Postuler passe toujours par nous : un conseiller présente votre dossier. Le classement intelligent des candidats n'est pas un outil en libre-service pour les entreprises.</p>
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
