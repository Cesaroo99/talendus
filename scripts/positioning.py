"""Positionnement Talendus — agence de placement intelligente.

Talendus n'est pas un job board, ni un ATS, ni une marketplace de CV.
Talendus est une agence de placement : l'entreprise confie un besoin,
Talendus recherche, présélectionne et présente une shortlist qualifiée.
L'entreprise conserve la décision finale.

L'IA accélère le processus interne de Talendus. Elle n'est pas un outil
mis à disposition du recruteur pour chercher lui-même. Les capacités
d'analyse et de rapprochement encore en cours d'intégration portent
« Bientôt disponible » — aucun score ni classement n'est simulé.
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
        ("Analyse des CV", "Aider les équipes Talendus à lire plus rapidement l'expérience, les métiers et les compétences."),
        ("Compréhension des compétences", "Repérer ce qu'un parcours démontre vraiment, au-delà du titre de poste."),
        ("Rapprochement avec le besoin", "Relier un mandat aux profils qui présentent le meilleur potentiel de correspondance."),
        ("Identification de correspondances", "Faire ressortir des profils pertinents pour analyse humaine."),
        ("Priorisation interne", "Ordonner les dossiers à examiner en premier par un conseiller Talendus."),
        ("Aide à la recherche", "Accélérer le sourcing interne : réseau, candidatures et profils déjà connus."),
        ("Structuration des informations", "Clarifier un besoin et un profil pour que l'équipe travaille plus vite."),
        ("Optimisation du temps de traitement", "Réduire le temps passé sur le bruit, pas remplacer le jugement humain."),
    ],
    "en": [
        ("Resume analysis", "Help Talendus teams read experience, roles and skills faster."),
        ("Skills understanding", "See what a career actually demonstrates, beyond the job title."),
        ("Fit against the need", "Connect a mandate to profiles with the strongest potential match."),
        ("Spotting correspondences", "Surface relevant profiles for human review."),
        ("Internal prioritization", "Order files a Talendus consultant should review first."),
        ("Search support", "Speed up internal sourcing: network, applications and known profiles."),
        ("Structuring information", "Clarify a need and a profile so the team works faster."),
        ("Faster processing", "Cut time spent on noise — without replacing human judgment."),
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
        "Talendus recrute pour tous les secteurs et tous les types de métiers. Ces exemples ne limitent pas le mandat."
        if lang == "fr"
        else "Talendus hires across every industry and every kind of role. These examples do not limit the mandate."
    )
    kicker = "Tous les secteurs" if lang == "fr" else "Every industry"
    heading = (
        "Un accompagnement adapté à chaque besoin de recrutement."
        if lang == "fr"
        else "Support shaped around each hiring need."
    )
    lead = (
        "PME, startups, grandes organisations : Talendus accompagne des entreprises de toutes tailles et de tous horizons."
        if lang == "fr"
        else "SMEs, startups, larger organizations: Talendus supports companies of every size and background."
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
        "Des talents pour tous les métiers."
        if lang == "fr"
        else "Talent for every kind of role."
    )
    lead = (
        "Opérationnel, spécialisé ou cadre : Talendus recherche le profil qui correspond au poste, pas un catalogue fermé."
        if lang == "fr"
        else "Operational, specialist or leadership: Talendus looks for the profile that fits the role, not a closed catalogue."
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
      <p>Artificial intelligence and our tools help Talendus do that work faster and with more information. They are not handed to you as a self-serve search engine. Technology stays inside our process. Human consultants remain essential to confirm fit, motivations and context.</p>
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
      <p>L'intelligence artificielle et nos outils aident Talendus à travailler plus vite, avec davantage d'informations. Ils ne vous sont pas remis comme un moteur de recherche en libre-service. La technologie reste au service de notre processus. Les conseillers restent essentiels pour confirmer la pertinence, les motivations et le contexte.</p>
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
            ("Artificial intelligence", "AI helps Talendus process and analyse information more quickly. It supports our teams. It does not choose the hire, and it is not a tool we hand to recruiters to search on their own."),
            ("Human expertise", "Consultants verify real fit, speak with candidates, weigh professional personality and context, and qualify the files we present."),
            ("Market knowledge", "We work with companies of every size and with candidates at every level. Understanding both sides is what makes a shortlist useful."),
            ("Selection", "We do not sell volume. We do not send a pile of resumes. The aim is to present the most relevant profiles, so you can focus on the final choice."),
        ]
        kicker, heading, lead = "Our approach", "How Talendus works.", "Technology, AI and human expertise serve one process: search, screen, qualify, present."
    else:
        items = [
            ("Technologie", "Des outils modernes aident Talendus à structurer les besoins, suivre les mandats et avancer plus vite — sans transformer le recrutement en logiciel en libre-service pour l'entreprise."),
            ("Intelligence artificielle", "L'IA aide Talendus à traiter et analyser les informations plus rapidement. Elle soutient nos équipes. Elle ne choisit pas la personne embauchée, et elle n'est pas un outil remis aux recruteurs pour chercher seuls."),
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
        kicker, heading = "From need to shortlist", "You describe the role. We do the search."
        steps = [
            ("01", "Your need", "You tell Talendus about the role: responsibilities, skills, experience, location, conditions and what matters most. A form, a call or both — we take the brief from there."),
            ("02", "Analysis", "The team studies the mandate to understand the profile you actually need. We clarify must-haves, nice-to-haves and constraints so the search does not start on a vague title."),
            ("03", "Search", "Talendus looks for people: our network, known profiles, published opportunities when useful, and the tools that help us cover more ground. AI supports that internal search. It does not replace it."),
            ("04", "Screening", "Identified candidates are reviewed against skills, experience, qualifications and the criteria we agreed with you. This is a first filter, not a dump of every resume we collected."),
            ("05", "Evaluation", "When needed, we speak with candidates: path, motivations, fit with the role. Interviews and checks happen before a file reaches you — so your time is spent on people worth meeting."),
            ("06", "Shortlist", "We present a qualified selection, not a massive list. Each file is one we are prepared to stand behind. Relevance is the product. Volume is not."),
            ("07", "Your decision", "You review the profiles, meet people according to your own process, and choose who joins. Talendus does not hire in your place. We make the final choice possible."),
        ]
    else:
        kicker, heading = "De la demande à la shortlist", "Vous décrivez le poste. Nous faisons la recherche."
        steps = [
            ("01", "Votre besoin", "Vous décrivez à Talendus le poste à pourvoir : responsabilités, compétences, expérience, lieu, conditions et ce qui compte vraiment. Formulaire, appel ou les deux : nous partons de ce brief."),
            ("02", "Analyse", "L'équipe étudie le mandat pour comprendre le profil réellement recherché. Nous clarifions l'essentiel, le souhaitable et les contraintes, pour que la recherche ne parte pas d'un titre flou."),
            ("03", "Recherche", "Talendus identifie les personnes : réseau, profils déjà connus, offres publiées si utile, et les outils qui élargissent le terrain. L'IA soutient cette recherche interne. Elle ne la remplace pas."),
            ("04", "Présélection", "Les candidats identifiés sont analysés : compétences, expérience, qualifications, critères convenus avec vous. C'est un premier filtre, pas un envoi de tous les CV collectés."),
            ("05", "Évaluation", "Lorsque c'est nécessaire, nous échangeons avec les candidats : parcours, motivations, adéquation avec le poste. Entretiens et vérifications ont lieu avant qu'un dossier vous parvienne — pour que votre temps aille aux personnes à rencontrer."),
            ("06", "Sélection", "Nous présentons une shortlist qualifiée, pas une liste massive. Chaque dossier est un profil que nous sommes prêts à défendre. La pertinence est le produit. Le volume ne l'est pas."),
            ("07", "Décision", "Vous étudiez les profils, les rencontrez selon votre processus, et choisissez. Talendus n'embauche pas à votre place. Nous rendons le choix final possible."),
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
    <div class="tl-steps tl-steps-7">{cards}</div>
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
            ("A search strengthened by AI", "AI tools help Talendus analyse available information faster — resumes, skills, criteria. They support our teams. They are not a self-serve engine for you to hunt candidates on Talendus."),
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
            ("Une recherche renforcée par l'IA", "Les outils d'intelligence artificielle aident Talendus à analyser plus vite les informations disponibles — parcours, compétences, critères. Ils soutiennent nos équipes. Ils ne sont pas un moteur en libre-service pour que vous chassiez des candidats sur Talendus."),
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


def ai_engine_section(lang="fr"):
    soon = "Bientôt disponible" if lang == "fr" else "Coming soon"
    cards = "".join(
        f'<div class="tl-card tl-ai-soon"><div class="body"><span class="tl-chip">{soon}</span><h3>{title}</h3><p>{text}</p></div></div>'
        for title, text in AI_FEATURES[lang]
    )
    if lang == "en":
        kicker = "Inside Talendus"
        heading = "Artificial intelligence in service of smarter hiring."
        prose = """
      <p>Talendus uses — and continues to build — AI and advanced tools to speed up and improve its own search, analysis and screening. The aim is not to give companies a software product so they can hunt candidates themselves. The aim is to help our teams treat more information, faster, with a better ability to connect a hiring need to relevant profiles.</p>
      <p>In practice, that can mean reading many resumes quickly, understanding skills and experience, relating a profile to the criteria of a role, spotting useful correspondences, prioritizing files for human review, and shortening some screening steps. Technology structures what we collect. It helps us work a mandate more quickly. It does not take the final decision.</p>
      <p>Several of these capabilities are still being integrated. They are not all live. We do not simulate scores, rankings or automatic matches. Until a capability is actually in the process, a Talendus consultant does the work by hand — with the same rule: the company does not search the database; we present a qualified selection.</p>
      <p><strong>Technology speeds up the work. Human expertise validates relevance.</strong> AI plus tools plus consultants: that is how a Talendus selection is built. The company then chooses.</p>
        """
    else:
        kicker = "Au cœur de Talendus"
        heading = "L'intelligence artificielle au service d'un recrutement plus intelligent."
        prose = """
      <p>Talendus utilise — et continue d'intégrer — l'intelligence artificielle et des outils avancés pour accélérer et améliorer son propre processus de recherche, d'analyse et de présélection. L'objectif n'est pas de remettre aux entreprises un logiciel pour qu'elles chassent elles-mêmes les candidats. L'objectif est d'aider nos équipes à traiter davantage d'informations, plus vite, avec une meilleure capacité à rapprocher un besoin de recrutement des profils pertinents.</p>
      <p>Concrètement, cela peut signifier analyser rapidement de nombreux parcours, comprendre les compétences et les expériences, relier un profil aux exigences d'un poste, détecter des correspondances utiles, prioriser des dossiers pour une revue humaine, et raccourcir certaines étapes de présélection. La technologie structure ce que nous recueillons. Elle aide à traiter un mandat plus rapidement. Elle ne prend pas la décision finale.</p>
      <p>Plusieurs de ces capacités sont encore en cours d'intégration. Elles ne sont pas toutes opérationnelles. Nous ne simulons pas de scores, de classements ni de rapprochements automatiques. Tant qu'une capacité n'est pas réellement dans le processus, un conseiller Talendus fait le travail — avec la même règle : l'entreprise ne parcourt pas la base ; nous présentons une sélection qualifiée.</p>
      <p><strong>La technologie accélère le travail. L'expertise humaine valide la pertinence.</strong> IA, outils et conseillers : c'est ainsi qu'une sélection Talendus se construit. L'entreprise choisit ensuite.</p>
        """
    return f"""
<section class="tl-section" id="ia">
  <div class="container">
    <div class="tl-prose" style="margin-bottom:36px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
      {prose}
    </div>
    <div class="tl-grid-3">{cards}</div>
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
      <p>Our consultants stay essential: they check whether a correspondence is real, they run the conversations, they weigh what a CV cannot say, they confirm fit, and they present the files. AI can help us treat information faster. It does not replace that judgment. The company keeps the final decision. Humans, on both sides, remain at the centre of qualification.</p>
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
      <p>Nos conseillers restent essentiels : ils vérifient si une correspondance est réelle, ils mènent les échanges, ils évaluent ce qu'un CV ne dit pas, ils confirment l'adéquation, et ils présentent les dossiers. L'IA peut nous aider à traiter plus vite les informations. Elle ne remplace pas ce jugement. L'entreprise garde la décision finale. L'humain, des deux côtés, reste au centre de la qualification.</p>
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
    """Page « besoin de recrutement » — 7 étapes côté entreprise."""
    return process_section(lang)


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
      <a class="tl-btn tl-btn-ghost" href="post-a-job.html">Describe my need</a>
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
      <a class="tl-btn tl-btn-ghost" href="publier-une-offre.html">Décrire mon besoin</a>
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
    return (
        for_companies_section(lang)
        + for_candidates_section(lang)
        + approach_section(lang)
        + process_section(lang)
        + why_talendus_section(lang)
        + ai_engine_section(lang)
        + human_section(lang)
        + sectors_cloud(lang)
        + trades_cloud(lang)
        + human_hire_band(lang)
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
