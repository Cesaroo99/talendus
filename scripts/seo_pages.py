"""Pages SEO services et locales, contenus distincts, pas de duplication automatique."""


def _page(hero, sections):
    return hero + "".join(sections)


def write_fr(write, wrap, page_hero, cta):
    pages = [
        (
            "recrutement-industriel.html",
            "Recrutement industriel au Québec | Agence Talendus",
            "Cabinet de recrutement au Québec. Page exemple : production, maintenance, logistique. Talendus recrute pour toutes les entreprises, tous secteurs. Shortlist filtrée, consultation sur rendez-vous.",
            "Services",
            "Recrutement industriel : un exemple parmi d'autres.",
            "Talendus est une agence de placement pour toutes les entreprises. Cette page illustre un secteur, pas une limite. Vous confiez un mandat ; nous recherchons, filtrons et présentons des dossiers.",
            "Confier mon recrutement",
            """
            <section class="tl-section"><div class="container">
              <div class="row g-4">
                <div class="col-lg-7">
                  <h2 class="tl-h2">Un exemple de secteur, pas une spécialisation exclusive</h2>
                  <p class="tl-lead">Production, maintenance, entrepôt, logistique, supervision. La technologie, la santé, la finance, le commerce et les autres industries sont tout autant concernées. <a href="secteurs.html">Voir tous les secteurs</a>.</p>
                  <h3>Pour qui</h3>
                  <p>Toute entreprise qui doit pourvoir un poste, souvent dans un délai serré. L'industrie n'est qu'un paramètre de recherche.</p>
                  <h3>Comment on travaille</h3>
                  <p>Brief sur le poste, le salaire réel et l'urgence. Approche de candidats actifs et passifs. Shortlist courte. Suivi 30/60/90 jours sur les mandats permanents.</p>
                  <p>Voir aussi : <a href="recrutement-manufacturier.html">recrutement manufacturier</a>, <a href="recrutement-technique.html">recrutement technique</a>, <a href="emplois.html">offres d'emploi</a>.</p>
                </div>
                <div class="col-lg-5">
                  <div class="tl-card"><div class="body">
                    <span class="tl-chip orange">Québec</span>
                    <h3>Grand Montréal et régions</h3>
                    <p>Nous recrutons à <a href="recrutement-industriel-montreal.html">Montréal</a>, <a href="recrutement-industriel-laval.html">Laval</a>, <a href="recrutement-industriel-longueuil.html">Longueuil</a> et partout au <a href="recrutement-industriel-quebec.html">Québec</a> lorsque le profil l'exige.</p>
                    <a class="tl-btn" href="contact.html" style="margin-top:16px">Réserver un appel</a>
                  </div></div>
                </div>
              </div>
            </div></section>
            """,
        ),
        (
            "recrutement-manufacturier.html",
            "Recrutement manufacturier au Québec | Talendus",
            "Recrutement manufacturier pour les usines québécoises : un exemple parmi d'autres secteurs que Talendus dessert. Pas une spécialisation exclusive.",
            "Manufacturier",
            "Recrutement manufacturier : un secteur parmi d'autres.",
            "Une usine n'embauche pas comme un siège. Nous évaluons le rythme, les procédures et le fit avant de vous envoyer un dossier. Talendus recrute aussi en santé, finance, technologie, commerce, et bien plus.",
            "Ouvrir un mandat manufacturier",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Usines de fabrication, assemblage et sous-traitance</h2>
              <p class="tl-lead">Opérateurs, set-up, qualité, machinistes, soudeurs et supervision de production. Le même cabinet suit le mandat du brief à l'intégration.</p>
              <h3>Ce qui bloque souvent l'embauche</h3>
              <p>Descriptif flou, salaire annoncé trop bas par rapport au marché, ou entrevues trop tardives. On le dit dès l'appel, sans maquiller le diagnostic.</p>
              <p>Besoin d'un volume d'opérateurs ? D'un machiniste CNC ? D'un superviseur ? <a href="contact.html">Parlez-nous du poste</a>. Lectures utiles : <a href="article-machiniste-cnc.html">recruter un machiniste CNC</a>, <a href="article-roulement-manufacturier.html">réduire le roulement</a>. <a href="secteurs.html">Tous les secteurs</a>.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="secteur-manufacturier.html">Secteur manufacturier</a>
                <a class="tl-btn tl-btn-ghost-dark" href="recrutement-industriel-montreal.html">Mandats à Montréal</a>
              </div>
            </div></section>
            """,
        ),
        (
            "recrutement-technique.html",
            "Recrutement de talents techniques et métiers qualifiés | Talendus",
            "Recrutement de travailleurs qualifiés : électromécaniciens, mécaniciens industriels, soudeurs, machinistes CNC et techniciens de procédé au Québec.",
            "Métiers",
            "Recrutement technique : les métiers que le marché se dispute.",
            "Cartes de compétences, machines, quarts rotatifs : on valide le savoir-faire, pas seulement le titre sur le CV.",
            "Recruter un métier technique",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Travailleurs qualifiés, pas des profils génériques</h2>
              <p>Électromécanique, mécanique industrielle, soudure, usinage, plasturgie, maintenance. Beaucoup de candidats sont déjà en poste : on les approche discrètement.</p>
              <h3>Évaluation</h3>
              <p>Mises en situation, lecture de plans, outils et cartes SST. Votre contremaître ne devrait pas découvrir l'écart en entrevue finale.</p>
              <p><a href="chasse-de-tetes.html">Chasse de têtes</a> pour les profils rares · <a href="emplois.html">Postes ouverts</a> · <a href="secteur-maintenance.html">Maintenance industrielle</a></p>
            </div></section>
            """,
        ),
        (
            "recrutement-permanent.html",
            "Recrutement permanent industriel au Québec | Talendus",
            "Recrutement permanent en usine, entrepôt et supervision. Honoraires au succès et garantie de remplacement sur les mandats permanents.",
            "Permanent",
            "Recrutement permanent : des gens qui restent après l'essai.",
            "Un poste stable se joue autant à l'accueil 30/60/90 jours qu'à l'entrevue. Le mandat inclut le suivi d'intégration.",
            "Confier un poste permanent",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Postes stables en production, logistique et gestion</h2>
              <p>Honoraires au succès. Garantie de remplacement confirmée à l'ouverture du dossier. Pas de frais si le mandat n'aboutit pas, selon l'entente.</p>
              <h3>Quand choisir le permanent</h3>
              <p>Lorsque le quart est structurel, que la formation interne est longue, ou qu'un métier rare doit rester. Pour un pic saisonnier, voir le <a href="recrutement-temporaire.html">recrutement temporaire</a>.</p>
              <p><a href="entreprises.html">Solutions entreprises</a> · <a href="article-mauvaise-embauche.html">Coût d'une mauvaise embauche</a></p>
            </div></section>
            """,
        ),
        (
            "recrutement-temporaire.html",
            "Recrutement temporaire et renforts d'usine | Talendus",
            "Recrutement temporaire industriel au Québec : renforts de quart, pics d'entrepôt et continuité de production. Shortlist filtrée, pas une pile de CV.",
            "Temporaire",
            "Recrutement temporaire : tenir le quart sans baisser la barre.",
            "Un pic saisonnier ou un arrêt maladie ne justifie pas d'envoyer n'importe qui sur le plancher. On filtre encore le fit SST et l'horaire.",
            "Demander un renfort",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Renforts de production et d'entrepôt</h2>
              <p>Journaliers, opérateurs, caristes et commis d'expédition lorsque le volume monte. Le délai annoncé dépend du métier et de la région, dès le brief.</p>
              <h3>Permanent ensuite ?</h3>
              <p>Plusieurs mandats temporaires deviennent permanents. Nous le prévoyons avec vous pour éviter un second recrutement improvisé. <a href="recrutement-permanent.html">Voir le recrutement permanent</a>.</p>
              <p><a href="secteur-entrepot.html">Entrepôt</a> · <a href="article-caristes-entrepot.html">Pénurie de caristes</a></p>
            </div></section>
            """,
        ),
        (
            "chasse-de-tetes.html",
            "Chasse de têtes au Québec | Talendus",
            "Chasseurs de têtes : recherche active, première entrevue, shortlist. Consultation gratuite. Honoraires à l'embauche. Québec.",
            "Chasse de têtes",
            "Les meilleurs candidats ne sont pas en recherche d'emploi.",
            "On ne se contente pas d'une annonce. Un chasseur fouille le marché, approche les gens déjà en poste, mène la première entrevue. Vous dites oui.",
            "Réserver une consultation gratuite",
            """
            <section class="tl-section"><div class="container">
              <div class="tl-prose" style="max-width:720px;margin:0 auto 36px">
                <div class="tl-kicker">Processus de chasse</div>
                <h2 class="tl-h2">Un processus simple, conçu pour combler le poste vite.</h2>
                <p>Nous contacter. Prise de besoins. Recrutement actif. Accompagnement jusqu'à l'embauche. C'est seulement à ce moment que vous payez.</p>
              </div>
              <div class="tl-takeover-list tl-takeover-list-3">
                <article class="tl-takeover-item"><span>01</span><h3>Nous contacter</h3><p>Parlez à un chasseur de têtes. Consultation gratuite, vingt minutes. On dit si on peut prendre le poste.</p></article>
                <article class="tl-takeover-item"><span>02</span><h3>Prise de besoins</h3><p>On écoute le poste affiché et celui que vous n'oseriez pas afficher. Puis on ajuste la stratégie au marché réel.</p></article>
                <article class="tl-takeover-item"><span>03</span><h3>Recrutement actif</h3><p>Les meilleurs ne regardent pas les babillards. Le chasseur fait le tour du bassin et approche le talent déjà en poste.</p></article>
                <article class="tl-takeover-item"><span>04</span><h3>Accompagnement</h3><p>Première entrevue, suivi, conditions. Vous rencontrez. Vous retenez. On reste jusqu'à l'entrée en poste.</p></article>
              </div>
            </div></section>
            <section class="tl-section tl-ice"><div class="container">
              <h2 class="tl-h2">Pas seulement les titres de direction</h2>
              <p>La chasse sert un cadre, oui. Elle sert aussi un machiniste CNC, un superviseur de quart, un responsable maintenance. Un poste vacant qui traîne coûte chaque jour.</p>
              <p>Complète le <a href="recrutement-cadres.html">recrutement de cadres</a> et le <a href="recrutement-technique.html">recrutement technique</a>. Une offre peut paraître sur <a href="emplois.html">talendus.ca</a> si vous le voulez — ce n'est jamais obligatoire.</p>
              <div class="tl-actions" style="margin-top:28px">
                <a class="tl-btn" href="contact.html">Réserver une consultation gratuite</a>
              </div>
            </div></section>
            """,
        ),
        (
            "recrutement-cadres.html",
            "Recrutement de cadres industriels | Talendus Québec",
            "Recrutement de cadres : directeurs d'usine, de production, de maintenance et de logistique. Mandats souvent confidentiels, au Québec.",
            "Cadres",
            "Recrutement de cadres d'usine, pas de cadres de siège.",
            "P&L, Lean, SST, climat de quart : on valide l'expérience de plant, pas seulement le titre.",
            "Confier un mandat cadre",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Direction, supervision et continuité d'usine</h2>
              <p>Directeurs d'usine, responsables production, maintenance et logistique. Entrevues structurées, références industrielles, discrétion.</p>
              <h3>Lien avec la chasse de têtes</h3>
              <p>La plupart des mandats cadres passent par une <a href="chasse-de-tetes.html">approche directe</a>. Pour un superviseur de quart, voir aussi <a href="article-superviseur-production.html">ce que nous validons sur le terrain</a>.</p>
              <p><a href="entreprises.html">Solutions pour entreprises</a></p>
            </div></section>
            """,
        ),
        (
            "recrutement-industriel-montreal.html",
            "Recrutement industriel à Montréal | Talendus",
            "Agence de recrutement industriel à Montréal : usines, entrepôts et métiers techniques du Grand Montréal. Consultation sur rendez-vous.",
            "Montréal",
            "Recrutement industriel à Montréal, ancré dans les quarts réels.",
            "Est, Ouest, Rive-Nord et Rive-Sud : on recrute pour des sites qui tournent, pas pour un discours métropolitain générique.",
            "Mandat à Montréal",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Grand Montréal : production, logistique, maintenance</h2>
              <p>Le bassin est dense, la concurrence aussi. Un salaire « marché Montréal » mal cadré fait fuir les métiers. Nous le disons au brief.</p>
              <h3>Ce qui change ici</h3>
              <p>Mobilité, transports, quarts de soir et bilingue opérationnel selon le site. Pas une copie de la page Laval ou Longueuil : le mix d'industries (agro, métal, distribution) n'est pas le même.</p>
              <p>Voir <a href="recrutement-industriel-laval.html">Laval</a>, <a href="recrutement-industriel-longueuil.html">Longueuil</a>, <a href="emplois.html">offres</a> et <a href="recrutement-manufacturier.html">recrutement manufacturier</a>.</p>
            </div></section>
            """,
        ),
        (
            "recrutement-industriel-laval.html",
            "Recrutement industriel à Laval | Talendus",
            "Recrutement industriel à Laval : entrepôts, centres de distribution, production et maintenance. Cabinet Talendus, consultation sur rendez-vous.",
            "Laval",
            "Recrutement industriel à Laval, surtout là où les quais tournent.",
            "Laval concentre beaucoup de logistique et d'usines de proximité. Les caristes expérimentés et les superviseurs d'entrepôt se disputent.",
            "Recruter à Laval",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Entrepôt, distribution et usines de la Rive-Nord</h2>
              <p>Permis chariot, WMS, SST et cadence de quai : le filtre n'est pas le même qu'un poste de production alimentaire à Longueuil. Nous ciblons en conséquence.</p>
              <h3>Candidats du nord de Montréal</h3>
              <p>Plusieurs profils habitent Laval, Terrebonne ou la Rive-Nord et refusent un trajet vers l'est. Le mandat doit le dire. <a href="article-caristes-entrepot.html">Pénurie de caristes</a> · <a href="secteur-entrepot.html">Secteur entrepôt</a></p>
            </div></section>
            """,
        ),
        (
            "recrutement-industriel-longueuil.html",
            "Recrutement industriel à Longueuil | Talendus",
            "Recrutement industriel à Longueuil et sur la Rive-Sud : transformation alimentaire, production et métiers d'usine. Cabinet Talendus.",
            "Longueuil",
            "Recrutement industriel à Longueuil et sur la Rive-Sud.",
            "Agroalimentaire, fabrication et logistique de proximité : des quarts rotatifs et des exigences d'hygiène que le CV seul ne montre pas.",
            "Mandat Rive-Sud",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Rive-Sud : alimentaire, production, maintenance</h2>
              <p>Longueuil, Boucherville, Brossard : les employeurs se disputent opérateurs et superviseurs qui acceptent les rotatifs. L'accueil et le climat de quart pèsent autant que le taux horaire.</p>
              <h3>Pas un duplicata de Montréal</h3>
              <p>Le bassin de candidats, les trajets et le mix agro / fabrication sont spécifiques. <a href="secteur-transformation-alimentaire.html">Transformation alimentaire</a> · <a href="recrutement-industriel-montreal.html">Montréal</a></p>
            </div></section>
            """,
        ),
        (
            "recrutement-industriel-quebec.html",
            "Recrutement industriel au Québec | Talendus",
            "Recrutement au Québec : Grand Montréal, Montérégie, Estrie, Centre-du-Québec, Mauricie et région de Québec. Tous secteurs.",
            "Québec",
            "Recrutement industriel au Québec, au-delà d'une seule ville.",
            "Nous menons des mandats là où vos usines sont, y compris en région lorsque le profil l'exige. Un cabinet, un réseau industriel.",
            "Parler d'un mandat au Québec",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Une couverture provinciale, des mandats locaux</h2>
              <p>Grand Montréal, Laval, Rive-Sud, Montérégie, Estrie, Centre-du-Québec, Mauricie, région de Québec. Chaque site a son salaire réel et sa rareté de métier : nous ne recyclons pas une page unique.</p>
              <h3>Pages locales déjà utiles</h3>
              <p>Nous n'avons créé que les territoires où Talendus intervient réellement : <a href="recrutement-industriel-montreal.html">Montréal</a>, <a href="recrutement-industriel-laval.html">Laval</a>, <a href="recrutement-industriel-longueuil.html">Longueuil</a>. D'autres villes viendront si l'activité le justifie. Pas des pages clones.</p>
              <p><a href="secteurs.html">Secteurs desservis</a> · <a href="a-propos.html">Le cabinet</a></p>
            </div></section>
            """,
        ),
    ]
    for slug, title, desc, kicker, h1, lead, cta_label, inner in pages:
        write(
            slug,
            wrap(
                title,
                desc,
                slug,
                page_hero(
                    kicker,
                    h1,
                    lead,
                    actions=f'<a class="tl-btn" href="contact.html">{cta_label}</a>',
                    badges='<span class="tl-badge tl-badge-light">Exemple de secteur</span>',
                )
                + inner
                + cta,
            ),
        )


def write_en(write, wrap, page_hero, cta):
    pages = [
        (
            "en/industrial-recruiting.html",
            "Industrial recruiting in Quebec | Talendus",
            "Placement agency in Quebec: production, maintenance, logistics, and every other industry. Screened shortlist, call by appointment.",
            "Services",
            "Industrial recruiting: one example among others.",
            "Talendus is a placement agency for every company. This page illustrates one industry, not a limit. You hand us a mandate; we search, screen and present files.",
            "Request a hire",
            "industrial recruiting Montreal",
            """
            <section class="tl-section"><div class="container">
              <div class="row g-4"><div class="col-lg-7">
              <h2 class="tl-h2">What industrial means here</h2>
              <p class="tl-lead">Production, maintenance, warehousing, logistics, supervision. Technology, healthcare, finance, retail and other industries are equally in scope. <a href="sectors.html">See every industry</a>.</p>
              <p>Also see <a href="manufacturing-recruiting.html">manufacturing recruiting</a>, <a href="technical-recruiting.html">technical recruiting</a> and <a href="jobs.html">open roles</a>.</p>
              </div>
              <div class="col-lg-5"><div class="tl-card"><div class="body">
                <h3>Greater Montreal and regions</h3>
                <p><a href="industrial-recruiting-montreal.html">Montreal</a>, <a href="industrial-recruiting-laval.html">Laval</a>, <a href="industrial-recruiting-longueuil.html">Longueuil</a> and across <a href="industrial-recruiting-quebec.html">Quebec</a>.</p>
              </div></div></div></div>
            </div></section>
            """,
        ),
        (
            "en/manufacturing-recruiting.html",
            "Manufacturing recruiting in Quebec | Talendus",
            "Manufacturing recruitment for Quebec plants: one example among the industries Talendus serves. Not an exclusive specialty.",
            "Manufacturing",
            "Manufacturing recruiting: people who can hold a line.",
            "A plant does not hire like a head office. We screen pace, procedures and shift fit before a file reaches you.",
            "Open a manufacturing mandate",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Fabrication, assembly and industrial subcontracting</h2>
              <p>Operators, set-up, quality, machinists, welders and production supervision. Useful reading: <a href="article-machiniste-cnc.html">hiring a CNC machinist</a>.</p>
            </div></section>
            """,
        ),
        (
            "en/technical-recruiting.html",
            "Technical and skilled-trades recruiting | Talendus",
            "Skilled-trades recruiting in Quebec: electromechanical technicians, industrial mechanics, welders, CNC machinists and process technicians.",
            "Trades",
            "Technical recruiting for trades the market is fighting over.",
            "Competency cards, machines, rotating shifts: we validate know-how, not just the job title.",
            "Hire a skilled trade",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Qualified trades, not generic profiles</h2>
              <p>A large share of the pool is passive. See <a href="executive-search.html">executive search</a> for scarce profiles.</p>
            </div></section>
            """,
        ),
        (
            "en/permanent-recruiting.html",
            "Permanent industrial recruiting in Quebec | Talendus",
            "Permanent recruiting for plants, warehouses and supervision. Success fees and a replacement guarantee on permanent mandates.",
            "Permanent",
            "Permanent recruiting: people who stay after probation.",
            "A stable seat is won as much in the 30/60/90-day welcome as in the interview.",
            "Start a permanent hire",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Stable production, logistics and leadership roles</h2>
              <p>For seasonal peaks, see <a href="temporary-recruiting.html">temporary recruiting</a>.</p>
            </div></section>
            """,
        ),
        (
            "en/temporary-recruiting.html",
            "Temporary industrial recruiting | Talendus Quebec",
            "Temporary industrial recruiting in Quebec: shift coverage, warehouse peaks and production continuity. A screened shortlist.",
            "Temporary",
            "Temporary recruiting without lowering the floor.",
            "A seasonal peak is not a reason to send anyone onto the floor. We still screen health &amp; safety and hours.",
            "Request coverage",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Production and warehouse coverage</h2>
              <p>Labourers, operators, forklift drivers and shipping clerks when volume rises.</p>
            </div></section>
            """,
        ),
        (
            "en/executive-search.html",
            "Headhunting in Quebec | Talendus",
            "Headhunters: active search, first interview, shortlist. Free consultation. Fees at the hire. Quebec.",
            "Headhunting",
            "The best candidates are not looking for a job.",
            "We do not stop at an ad. A headhunter maps the market, approaches people already in a job, runs the first interview. You say yes.",
            "Book a free consultation",
            "",
            """
            <section class="tl-section"><div class="container">
              <div class="tl-prose" style="max-width:720px;margin:0 auto 36px">
                <div class="tl-kicker">Search process</div>
                <h2 class="tl-h2">A simple process, built to fill the seat fast.</h2>
                <p>Contact us. Needs intake. Active search. Support through the hire. That is when you pay.</p>
              </div>
              <div class="tl-takeover-list tl-takeover-list-3">
                <article class="tl-takeover-item"><span>01</span><h3>Contact us</h3><p>Talk to a headhunter. Free consultation, twenty minutes. We say if we can take the seat.</p></article>
                <article class="tl-takeover-item"><span>02</span><h3>Needs intake</h3><p>We hear the role you would post and the one you would not. Then we adjust the strategy to the real market.</p></article>
                <article class="tl-takeover-item"><span>03</span><h3>Active search</h3><p>The best people do not watch job boards. The headhunter maps the pool and approaches talent already in a job.</p></article>
                <article class="tl-takeover-item"><span>04</span><h3>Support</h3><p>First interview, follow-up, terms. You meet. You retain. We stay through start date.</p></article>
              </div>
            </div></section>
            <section class="tl-section tl-ice"><div class="container">
              <h2 class="tl-h2">Not only executive titles</h2>
              <p>Search serves a manager, yes. It also serves a CNC machinist, a shift supervisor, a maintenance lead. A vacant seat that lingers costs every day.</p>
              <p>Complements <a href="leadership-recruiting.html">leadership recruiting</a> and <a href="technical-recruiting.html">technical recruiting</a>. A posting can still appear on <a href="jobs.html">talendus.ca</a> if you want — it is never required.</p>
              <div class="tl-actions" style="margin-top:28px">
                <a class="tl-btn" href="contact.html">Book a free consultation</a>
              </div>
            </div></section>
            """,
        ),
        (
            "en/leadership-recruiting.html",
            "Industrial leadership recruiting | Talendus Quebec",
            "Leadership recruiting: managers and executives. Often confidential mandates in Quebec.",
            "Leadership",
            "Leadership recruiting, in every industry.",
            "P&amp;L, Lean, health &amp; safety, shift climate: we validate plant experience, not just the title.",
            "Start a leadership mandate",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Direction, supervision and continuity</h2>
              <p>Most leadership mandates use a <a href="executive-search.html">direct approach</a>.</p>
            </div></section>
            """,
        ),
        (
            "en/industrial-recruiting-montreal.html",
            "Industrial recruiting in Montreal | Talendus",
            "Industrial recruiting agency in Montreal: plants, warehouses and technical trades across Greater Montreal. Consultation by appointment.",
            "Montreal",
            "Industrial recruiting in Montreal, tied to real shifts.",
            "East, West, North and South Shore: we hire for sites that run, not for a generic metro pitch.",
            "Montreal mandate",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Greater Montreal: production, logistics, maintenance</h2>
              <p>The pool is dense and so is the competition. See <a href="industrial-recruiting-laval.html">Laval</a> and <a href="industrial-recruiting-longueuil.html">Longueuil</a> for distinct mixes.</p>
            </div></section>
            """,
        ),
        (
            "en/industrial-recruiting-laval.html",
            "Industrial recruiting in Laval | Talendus",
            "Industrial recruiting in Laval: warehouses, distribution centres, production and maintenance. Talendus, consultation by appointment.",
            "Laval",
            "Industrial recruiting in Laval, where the docks actually move.",
            "Laval concentrates logistics and nearby plants. Experienced forklift operators and warehouse supervisors are in demand.",
            "Hire in Laval",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Warehousing, distribution and North Shore plants</h2>
              <p>Forklift permits, WMS and dock pace: not the same filter as a food plant in Longueuil.</p>
            </div></section>
            """,
        ),
        (
            "en/industrial-recruiting-longueuil.html",
            "Industrial recruiting in Longueuil | Talendus",
            "Industrial recruiting in Longueuil and the South Shore: food processing, production and plant trades. Talendus.",
            "Longueuil",
            "Industrial recruiting in Longueuil and the South Shore.",
            "Food processing, fabrication and nearby logistics: rotating shifts and hygiene rules a resume does not show.",
            "South Shore mandate",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">South Shore: food, production, maintenance</h2>
              <p>Longueuil, Boucherville, Brossard, operators and supervisors who accept rotating shifts are scarce.</p>
            </div></section>
            """,
        ),
        (
            "en/industrial-recruiting-quebec.html",
            "Industrial recruiting in Quebec | Talendus",
            "Industrial recruiting across Quebec: Greater Montreal, Montérégie, the Eastern Townships, Centre-du-Québec, Mauricie and the Quebec City area.",
            "Quebec",
            "Industrial recruiting across Quebec, not a single city page.",
            "We run mandates where your plants are, including the regions when the profile requires it.",
            "Talk about a Quebec mandate",
            "",
            """
            <section class="tl-section"><div class="container">
              <h2 class="tl-h2">Provincial coverage, local mandates</h2>
              <p>Only territories where Talendus actually works have local pages. No auto-generated clones.</p>
            </div></section>
            """,
        ),
    ]
    for slug, title, desc, kicker, h1, lead, cta_label, _unused, inner in pages:
        alt = slug.split("/", 1)[-1]
        fr_alt = {
            "industrial-recruiting.html": "recrutement-industriel.html",
            "manufacturing-recruiting.html": "recrutement-manufacturier.html",
            "technical-recruiting.html": "recrutement-technique.html",
            "permanent-recruiting.html": "recrutement-permanent.html",
            "temporary-recruiting.html": "recrutement-temporaire.html",
            "executive-search.html": "chasse-de-tetes.html",
            "leadership-recruiting.html": "recrutement-cadres.html",
            "industrial-recruiting-montreal.html": "recrutement-industriel-montreal.html",
            "industrial-recruiting-laval.html": "recrutement-industriel-laval.html",
            "industrial-recruiting-longueuil.html": "recrutement-industriel-longueuil.html",
            "industrial-recruiting-quebec.html": "recrutement-industriel-quebec.html",
        }[alt]
        write(
            slug,
            wrap(
                title,
                desc,
                slug,
                page_hero(
                    kicker,
                    h1,
                    lead,
                    actions=f'<a class="tl-btn" href="contact.html">{cta_label}</a>',
                    badges='<span class="tl-badge tl-badge-light">Industry example</span>',
                )
                + inner
                + cta,
                lang="en",
                alt=fr_alt,
            ),
        )
