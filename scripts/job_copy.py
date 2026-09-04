"""Textes complets des offres du catalogue public (FR / EN)."""

from __future__ import annotations


def _ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def _paras(blocks: list[str]) -> str:
    return "".join(f"<p>{p}</p>" for p in blocks if p)


STORIES: dict[str, dict[str, dict]] = {
    "cariste": {
        "fr": {
            "lead": "Talendus recrute un cariste pour un employeur de Laval. L’équipe cherche quelqu’un de fiable, déjà à l’aise sur chariot, pour tenir le rythme d’un entrepôt qui tourne vraiment.",
            "role": [
                "Vous prenez en charge les mouvements de stock : réception, mise en rack, préparation et quai. Ce n’est pas un poste d’appoint : le flux dépend de votre précision et de votre rythme.",
                "L’employeur veut quelqu’un qui connaît déjà le chariot, qui range proprement et qui signale un palet instable avant qu’il ne pose problème. Talendus présente votre dossier seulement s’il correspond.",
            ],
            "duties": [
                "Conduire le chariot élévateur (contrebalancé / reach selon le site) en toute sécurité",
                "Réceptionner, identifier et ranger les marchandises selon le plan de stockage",
                "Préparer les commandes et charger les quais sans casser le rythme de l’équipe",
                "Tenir les comptes de stock et signaler les écarts au superviseur",
                "Respecter les règles d’entreposage, les zones piétonnes et les EPI",
            ],
            "profile": [
                "Permis de chariot élévateur valide et au moins un an en entrepôt ou centre de distribution.",
                "Vous lisez un bon de commande, vous rangez droit, vous n’improvisez pas avec une charge mal sanglée.",
            ],
            "assets": ["Expérience WMS ou scan", "Disponibilité pour un dépannage de soir", "Carte de compétences"],
            "offer": [
                "Poste permanent, temps plein, quart de jour",
                "Rémunération : 22 à 26 $/h selon expérience",
                "Assurance collective une fois en poste",
                "Un conseiller Talendus étudie votre CV et vous rappelle avant toute présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a forklift operator for an employer in Laval. The team wants someone reliable, already comfortable on a lift truck, who can keep a real warehouse moving.",
            "role": [
                "You own stock movement: receiving, put-away, picking and the dock. This is not a fill-in role — flow depends on your accuracy and pace.",
                "The employer wants someone who already knows the truck, stores cleanly, and flags an unstable pallet before it becomes a problem. Talendus only presents your file if it fits.",
            ],
            "duties": [
                "Operate the forklift (counterbalance / reach depending on site) safely",
                "Receive, identify and store goods according to the slotting plan",
                "Prepare orders and load docks without breaking the team’s pace",
                "Keep stock counts and report variances to the supervisor",
                "Follow storage rules, pedestrian zones and PPE",
            ],
            "profile": [
                "Valid forklift permit and at least one year in a warehouse or DC.",
                "You can read a pick list, store straight, and you do not improvise with a poorly strapped load.",
            ],
            "assets": ["WMS or scan experience", "Availability for an evening fill-in", "Competency card"],
            "offer": [
                "Permanent full-time role, day shift",
                "Pay: $22 to $26/hr depending on experience",
                "Group insurance once in post",
                "A Talendus consultant reviews your résumé and calls you before any presentation",
            ],
        },
    },
    "operateur-production": {
        "fr": {
            "lead": "Talendus recrute un opérateur de production à Longueuil. L’usine cherche quelqu’un qui suit une procédure, tient un poste et ne laisse pas passer une pièce douteuse.",
            "role": [
                "Vous tenez une station sur une ligne : alimentation, contrôle, assemblage ou emballage selon le mandat. La formation interne existe, mais on attend déjà le réflexe « je vérifie avant de laisser partir ».",
                "Les quarts tournent. Si vous aimez un travail concret, mesurable, en équipe, c’est le genre de poste où l’on vous voit vite.",
            ],
            "duties": [
                "Alimenter et faire tourner le poste selon les consignes de production",
                "Contrôler visuellement et par mesures simples la conformité des pièces",
                "Signaler un écart, un bourrage ou une pièce hors tolérance sans attendre",
                "Tenir le poste propre et respecter les règles de sécurité",
                "Appuyer les changements de série avec l’équipe de quart",
            ],
            "profile": [
                "Une première expérience en usine ou en transformation aide, mais un débutant rigoureux et ponctuel sera considéré.",
                "Vous suivez une procédure, vous tenez le rythme, vous travaillez en équipe.",
            ],
            "assets": ["Lecture de documents de travail", "Disponibilité soirs / fins de semaine", "Intérêt pour un métier d’usine durable"],
            "offer": [
                "Poste permanent, temps plein, quarts rotatifs",
                "Rémunération : 20 à 24 $/h",
                "Heures supplémentaires payées selon le besoin de la ligne",
                "Formation interne ; un conseiller Talendus vous rappelle après lecture du dossier",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a production operator in Longueuil. The plant wants someone who follows a procedure, holds a station, and does not let a doubtful part through.",
            "role": [
                "You hold a station on a line: feeding, checking, assembling or packing depending on the mandate. On-the-job training exists, but they already expect the reflex “I check before I let it go”.",
                "Shifts rotate. If you like concrete, measurable team work, this is a role where you are seen quickly.",
            ],
            "duties": [
                "Feed and run the station to production instructions",
                "Check parts visually and with simple measurements",
                "Flag a variance, jam or out-of-tolerance part without waiting",
                "Keep the station clean and follow safety rules",
                "Support changeovers with the shift team",
            ],
            "profile": [
                "A first plant or processing experience helps, but a rigorous, punctual beginner will be considered.",
                "You follow a procedure, you hold the pace, you work in a team.",
            ],
            "assets": ["Ability to read work documents", "Evening / weekend availability", "Interest in a lasting plant trade"],
            "offer": [
                "Permanent full-time role, rotating shifts",
                "Pay: $20 to $24/hr",
                "Paid overtime when the line needs it",
                "On-the-job training; a Talendus consultant calls you after reviewing the file",
            ],
        },
    },
    "soudeur": {
        "fr": {
            "lead": "Talendus recrute un soudeur-monteur à Drummondville. L’atelier cherche un métier qui lit un plan, prépare son joint et livre une soudure propre — pas seulement « qui a déjà tenu un chalumeau ».",
            "role": [
                "Vous montez et soudez des assemblages métalliques (MIG/TIG selon les postes). Le travail est concret : préparation, pointage, soudure, meulage, contrôle visuel.",
                "Les cartes de compétences sont un atout. On veut quelqu’un qui respecte les paramètres et qui n’envoie pas une pièce douteuse au poste suivant.",
            ],
            "duties": [
                "Lire les dessins, les nomenclatures et les procédés de soudage",
                "Préparer, pointer et souder (MIG/TIG) selon les consignes",
                "Contrôler visuellement les joints et reprendre ce qui ne passe pas",
                "Monter les assemblages dans les tolérances demandées",
                "Tenir le poste en ordre et respecter les règles de sécurité atelier",
            ],
            "profile": [
                "Soudure MIG/TIG déjà pratiquée, lecture de plans, au moins un niveau intermédiaire.",
                "DEP ou cartes de compétences : un plus net. On évalue aussi la qualité de vos pièces récentes.",
            ],
            "assets": ["CISA / cartes de compétences", "Expérience structure ou manufacturier", "Lecture d’anglais technique"],
            "offer": [
                "Poste permanent, temps plein, quart de jour",
                "Rémunération : 28 à 34 $/h selon cartes et expérience",
                "Atelier structuré, pièces variées",
                "Talendus vérifie le fit technique avant de vous présenter",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a welder-fitter in Drummondville. The shop wants a tradesperson who reads a drawing, prepares the joint and delivers a clean weld — not just someone who has held a torch.",
            "role": [
                "You fit and weld metal assemblies (MIG/TIG depending on the station). The work is concrete: prep, tack, weld, grind, visual check.",
                "Competency cards are an asset. They want someone who respects parameters and does not send a doubtful part downstream.",
            ],
            "duties": [
                "Read drawings, bills of materials and welding procedures",
                "Prep, tack and weld (MIG/TIG) to instruction",
                "Visually inspect joints and rework what does not pass",
                "Fit assemblies within the required tolerances",
                "Keep the station orderly and follow shop safety rules",
            ],
            "profile": [
                "MIG/TIG already practised, blueprint reading, at least intermediate level.",
                "DEP or competency cards are a clear plus. Recent work quality is also assessed.",
            ],
            "assets": ["CWB / competency cards", "Structural or manufacturing experience", "Technical English"],
            "offer": [
                "Permanent full-time role, day shift",
                "Pay: $28 to $34/hr depending on cards and experience",
                "Structured shop, varied parts",
                "Talendus checks the technical fit before presenting you",
            ],
        },
    },
    "machiniste-cnc": {
        "fr": {
            "lead": "Talendus recrute un machiniste CNC à Saint-Jérôme. L’employeur veut quelqu’un qui set-up, qui lit un dessin et qui ne lance pas une série sans première pièce conforme.",
            "role": [
                "Vous prenez en charge le set-up et la production sur centres d’usinage. Programmation ou édition de programmes, outils, offsets, contrôle dimensionnel.",
                "Trois ans et plus, c’est le niveau visé. Un profil senior qui forme un collègue est le bienvenu.",
            ],
            "duties": [
                "Réaliser les set-up (outils, montages, offsets) et valider la première pièce",
                "Usiner selon dessins et tolérances, ajuster le programme au besoin",
                "Contrôler les cotes (pied, micromètre, indicateur, parfois CMM)",
                "Signaler l’usure d’outil et les dérives avant le rebut",
                "Tenir le poste et documenter les changements de série",
            ],
            "profile": [
                "Programmation ou set-up CNC, lecture de dessins, environ 3 ans d’expérience.",
                "DEP en usinage fortement souhaité. Autonomie sur un centre : attendue.",
            ],
            "assets": ["Fanuc / Haas / Siemens", "Expérience multi-axes", "Habitude du contrôle qualité serré"],
            "offer": [
                "Poste permanent, temps plein, quart de jour",
                "Rémunération : 30 à 38 $/h",
                "Pièces techniques, vrai métier d’usinage",
                "Un conseiller Talendus parle shop avec vous avant la présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a CNC machinist in Saint-Jérôme. The employer wants someone who can set up, read a drawing, and will not launch a run without a conforming first piece.",
            "role": [
                "You own set-up and production on machining centres. Programming or program edits, tools, offsets, dimensional checks.",
                "Three years and up is the target. A senior who can coach a colleague is welcome.",
            ],
            "duties": [
                "Run set-ups (tools, fixtures, offsets) and validate the first piece",
                "Machine to drawings and tolerances, edit the program when needed",
                "Check dimensions (caliper, micrometer, indicator, sometimes CMM)",
                "Flag tool wear and drift before scrap",
                "Keep the station and document changeovers",
            ],
            "profile": [
                "CNC programming or set-up, drawing reading, about 3 years of experience.",
                "Machining DEP strongly preferred. Autonomy on a centre is expected.",
            ],
            "assets": ["Fanuc / Haas / Siemens", "Multi-axis experience", "Tight quality-control habits"],
            "offer": [
                "Permanent full-time role, day shift",
                "Pay: $30 to $38/hr",
                "Technical parts, a real machining trade",
                "A Talendus consultant talks shop with you before any presentation",
            ],
        },
    },
    "electromecanicien": {
        "fr": {
            "lead": "Talendus recrute un électromécanicien à Montréal. L’usine a besoin de quelqu’un qui dépannne — électricité, hydraulique, pneumatique — et qui remet la ligne en marche sans théâtre.",
            "role": [
                "Vous diagnostiquez les pannes, vous changez un composant, vous suivez un schéma. Le poste mélange entretien préventif et urgences de production.",
                "DEP et carte de compétences sont le profil type. Les quarts tournent : il faut aimer le terrain.",
            ],
            "duties": [
                "Dépanner moteurs, variateurs, capteurs, vérins et circuits",
                "Lire schémas électriques, hydrauliques et pneumatiques",
                "Réaliser l’entretien préventif et consigner les interventions",
                "Appuyer les mécaniciens et les opérateurs lors d’un arrêt",
                "Respecter les cadenassages et les procédures de sécurité",
            ],
            "profile": [
                "Dépannage déjà pratiqué : hydraulique, pneumatique, électricité industrielle.",
                "DEP et carte de compétences : fortement souhaités. Autonomie sur le plancher : essentielle.",
            ],
            "assets": ["Automates / variateurs", "Expérience alimentaire ou manufacturière", "Permis de conduire pour plus d’un site"],
            "offer": [
                "Poste permanent, temps plein, quarts rotatifs",
                "Rémunération : 32 à 40 $/h",
                "Vrai métier de maintenance, pas un poste d’observateur",
                "Talendus valide votre terrain avant de parler à l’employeur",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting an electromechanical technician in Montreal. The plant needs someone who troubleshoots — electrical, hydraulic, pneumatic — and gets the line running again without drama.",
            "role": [
                "You diagnose faults, swap a component, follow a schematic. The role mixes preventive work and production emergencies.",
                "A DEP and competency card are the typical profile. Shifts rotate: this is a floor job.",
            ],
            "duties": [
                "Troubleshoot motors, drives, sensors, cylinders and circuits",
                "Read electrical, hydraulic and pneumatic schematics",
                "Carry out preventive maintenance and log the work",
                "Support mechanics and operators during a stop",
                "Follow lockout and safety procedures",
            ],
            "profile": [
                "Troubleshooting already practised: hydraulics, pneumatics, industrial electricity.",
                "DEP and competency card strongly preferred. Floor autonomy is essential.",
            ],
            "assets": ["PLCs / drives", "Food or manufacturing experience", "Driver’s licence for more than one site"],
            "offer": [
                "Permanent full-time role, rotating shifts",
                "Pay: $32 to $40/hr",
                "A real maintenance trade, not an observer seat",
                "Talendus validates your floor experience before speaking to the employer",
            ],
        },
    },
    "mecanicien-industriel": {
        "fr": {
            "lead": "Talendus recrute un mécanicien industriel à Sherbrooke. L’employeur cherche quelqu’un qui aligne, lubrifie, change un roulement et remet un convoyeur en service.",
            "role": [
                "Vous êtes le métier de la mécanique d’usine : préventif, correctif, alignements, convoyeurs, pompes, réducteurs.",
                "On veut de la fiabilité, pas seulement du dépannage de crise. DEP et carte de compétences sont le standard visé.",
            ],
            "duties": [
                "Planifier et exécuter l’entretien préventif des équipements",
                "Diagnostiquer bruits, jeux, fuites et usures",
                "Aligner, remplacer et ajuster les ensembles mécaniques",
                "Travailler avec l’électromécanicien sur les arrêts croisés",
                "Documenter les interventions et les pièces utilisées",
            ],
            "profile": [
                "Entretien préventif, alignement, convoyeurs : déjà faits, pas seulement vus.",
                "DEP mécanique industrielle et carte de compétences : fortement souhaités.",
            ],
            "assets": ["Laser d’alignement", "Lecture de plans mécaniques", "Expérience multi-quarts"],
            "offer": [
                "Poste permanent, temps plein",
                "Rémunération : 30 à 36 $/h",
                "Usine qui investit dans la fiabilité",
                "Présentation seulement si le métier colle — Talendus filtre",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting an industrial mechanic in Sherbrooke. The employer wants someone who aligns, lubricates, changes a bearing and puts a conveyor back in service.",
            "role": [
                "You are the plant mechanical trade: preventive, corrective, alignments, conveyors, pumps, gearboxes.",
                "They want reliability, not only crisis repairs. A DEP and competency card are the target standard.",
            ],
            "duties": [
                "Plan and run preventive maintenance on equipment",
                "Diagnose noise, play, leaks and wear",
                "Align, replace and adjust mechanical assemblies",
                "Work with the electromechanical tech on shared stops",
                "Log interventions and parts used",
            ],
            "profile": [
                "Preventive maintenance, alignment, conveyors: already done, not only observed.",
                "Industrial mechanics DEP and competency card strongly preferred.",
            ],
            "assets": ["Laser alignment", "Mechanical drawing reading", "Multi-shift experience"],
            "offer": [
                "Permanent full-time role",
                "Pay: $30 to $36/hr",
                "A plant that invests in reliability",
                "Presentation only if the trade fits — Talendus screens",
            ],
        },
    },
    "journalier-usine": {
        "fr": {
            "lead": "Talendus recrute un journalier d’usine à Boucherville. Le poste convient à quelqu’un de ponctuel, en forme, prêt à apprendre le poste dès la première semaine.",
            "role": [
                "Vous appuyez la production : alimentation, tri, emballage, ménage de poste, mouvements de matériel. La formation se fait sur le plancher.",
                "Quart de soir. Ce n’est pas un job « en attendant » si vous voulez entrer dans l’usine et monter ensuite.",
            ],
            "duties": [
                "Alimenter les postes et déplacer le matériel selon les consignes",
                "Trier, emballer ou compter selon la série du jour",
                "Tenir les allées et le poste propres",
                "Suivre les règles de sécurité et les EPI",
                "Remplacer un collègue sur une tâche simple après formation",
            ],
            "profile": [
                "Bonne condition physique, ponctualité, secondaire un atout. Aucun métier préalable exigé.",
                "On forme. On n’accepte pas l’à-peu-près sur les horaires.",
            ],
            "assets": ["Expérience d’entrepôt ou de chantier", "Disponibilité immédiate", "Intérêt pour un poste d’opérateur plus tard"],
            "offer": [
                "Poste permanent, temps plein, quart de soir",
                "Rémunération : 18 à 21 $/h",
                "Heures supplémentaires payées selon la production",
                "Formation interne ; Talendus vous rappelle après lecture du CV",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a plant labourer in Boucherville. The role suits someone punctual, fit, and ready to learn the station in the first week.",
            "role": [
                "You support production: feeding, sorting, packing, station housekeeping, material moves. Training happens on the floor.",
                "Evening shift. This is not a “meanwhile” job if you want to enter the plant and move up later.",
            ],
            "duties": [
                "Feed stations and move material as instructed",
                "Sort, pack or count according to the day’s run",
                "Keep aisles and the station clean",
                "Follow safety rules and PPE",
                "Cover a simple task for a colleague after training",
            ],
            "profile": [
                "Physical fitness, punctuality, secondary school an asset. No prior trade required.",
                "They train. They do not accept sloppy attendance.",
            ],
            "assets": ["Warehouse or site experience", "Immediate availability", "Interest in an operator role later"],
            "offer": [
                "Permanent full-time role, evening shift",
                "Pay: $18 to $21/hr",
                "Paid overtime according to production",
                "On-the-job training; Talendus calls you after reading the résumé",
            ],
        },
    },
    "superviseur-production": {
        "fr": {
            "lead": "Talendus recrute un superviseur de production à Trois-Rivières. L’employeur veut quelqu’un qui tient un quart, lit les KPI et parle vrai à l’équipe — pas un titre sans plancher.",
            "role": [
                "Vous pilotez un quart : effectifs, sécurité, cadence, qualité, passation. Vous êtes le relais entre la direction et les opérateurs.",
                "Cinq ans en production, dont de la supervision, c’est le socle. Les heures peuvent déborder quand la ligne lâche.",
            ],
            "duties": [
                "Planifier le quart, les absences et les priorités de la journée",
                "Suivre sécurité, qualité et cadence ; intervenir dès l’écart",
                "Animer l’équipe, former, recadrer au besoin",
                "Faire le pont avec maintenance, logistique et qualité",
                "Rendre compte des KPI et des incidents en fin de quart",
            ],
            "profile": [
                "Leadership d’équipe déjà exercé, lecture de KPI, environ 5 ans en production.",
                "Vous avez tenu un quart. Vous savez arbitrer entre livrer et ne pas brûler le monde.",
            ],
            "assets": ["Lean / 5S", "Bilinguisme", "Expérience multi-quarts"],
            "offer": [
                "Poste permanent, temps plein, quart de jour",
                "Rémunération : 70 000 à 85 000 $",
                "Heures supplémentaires payées selon les pratiques du site",
                "Mandat présenté par Talendus après un entretien de cadrage",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a production supervisor in Trois-Rivières. The employer wants someone who holds a shift, reads KPIs and speaks plainly with the team — not a title without floor time.",
            "role": [
                "You run a shift: headcount, safety, pace, quality, handover. You are the link between management and operators.",
                "Five years in production, including supervision, is the baseline. Hours can overrun when the line fails.",
            ],
            "duties": [
                "Plan the shift, absences and the day’s priorities",
                "Track safety, quality and pace; step in as soon as something drifts",
                "Lead the team, train, reset expectations when needed",
                "Bridge with maintenance, logistics and quality",
                "Report KPIs and incidents at the end of the shift",
            ],
            "profile": [
                "Team leadership already practised, KPI literacy, about 5 years in production.",
                "You have held a shift. You can trade off delivery against burning people out.",
            ],
            "assets": ["Lean / 5S", "Bilingual", "Multi-shift experience"],
            "offer": [
                "Permanent full-time role, day shift",
                "Pay: $70,000 to $85,000",
                "Overtime paid according to site practice",
                "Mandate presented by Talendus after a scoping interview",
            ],
        },
    },
    "coordonnateur-logistique": {
        "fr": {
            "lead": "Talendus recrute un coordonnateur logistique à Anjou. L’employeur a besoin de quelqu’un qui planifie les flux, parle WMS et ne laisse pas un quai à l’abandon.",
            "role": [
                "Vous coordonnez réception, stocks, transport et expédition. Hybride : du bureau, du quai, des appels transporteurs.",
                "L’anglais est un atout réel (clients ou transporteurs). On veut de l’ordre, pas seulement des tableaux.",
            ],
            "duties": [
                "Planifier les arrivées, les vagues et les départs",
                "Suivre le WMS, les écarts et les urgences client",
                "Coordonner transporteurs, entrepôt et service client",
                "Anticiper les goulots (capacité, absences, pics)",
                "Rendre compte des indicateurs de service",
            ],
            "profile": [
                "WMS, planification, coordination déjà pratiqués. Niveau intermédiaire.",
                "Français requis, anglais un atout. À l’aise autant au bureau qu’au quai.",
            ],
            "assets": ["Excel avancé", "Expérience 3PL", "Permis de conduire"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 55 000 à 68 000 $",
                "Français et anglais au quotidien selon les dossiers",
                "Talendus présente seulement un profil qui a déjà tenu un flux",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a logistics coordinator in Anjou. The employer needs someone who plans flow, speaks WMS, and does not leave a dock unattended.",
            "role": [
                "You coordinate receiving, inventory, transport and shipping. Hybrid: desk, dock, carrier calls.",
                "English is a real asset (customers or carriers). They want order, not only spreadsheets.",
            ],
            "duties": [
                "Plan inbound, waves and outbound",
                "Track the WMS, variances and customer urgencies",
                "Coordinate carriers, warehouse and customer service",
                "Anticipate bottlenecks (capacity, absences, peaks)",
                "Report service indicators",
            ],
            "profile": [
                "WMS, planning and coordination already practised. Intermediate level.",
                "French required, English an asset. Comfortable at a desk and on the dock.",
            ],
            "assets": ["Advanced Excel", "3PL experience", "Driver’s licence"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $55,000 to $68,000",
                "French and English day to day depending on files",
                "Talendus only presents a profile that has already held a flow",
            ],
        },
    },
    "directeur-usine": {
        "fr": {
            "lead": "Talendus recrute un directeur d’usine dans la région de Québec. Mandat confidentiel : site de plus de 100 personnes, P&L réel, Lean déjà en place ou à relancer.",
            "role": [
                "Vous tenez le site : sécurité, qualité, coût, livraisons, climat. Vous rendez compte à la direction et vous tenez vos responsables de quart.",
                "Ce n’est pas un poste de représentation. On veut quelqu’un qui a déjà porté un P&L d’usine et qui marche encore dans l’atelier.",
            ],
            "duties": [
                "Porter le P&L et les décisions d’investissement du site",
                "Piloter sécurité, qualité, Lean et performance opérationnelle",
                "Structurer l’équipe de supervision et la relève",
                "Arbitrer production, maintenance et service client",
                "Représenter le site auprès de la direction et, au besoin, des partenaires",
            ],
            "profile": [
                "P&L, Lean, gestion d’un site 100+ employés. Niveau senior.",
                "Baccalauréat ou équivalent d’expérience. Déplacements occasionnels.",
            ],
            "assets": ["Expérience multi-sites", "Bilinguisme", "Transformation Lean déjà menée"],
            "offer": [
                "Poste permanent, sur place, temps plein",
                "Rémunération : 120 000 à 150 000 $",
                "Mandat confidentiel — l’employeur n’est pas nommé ici",
                "Entretien de cadrage Talendus avant toute mise en contact",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a plant manager in the Quebec City area. Confidential mandate: 100+ employee site, real P&L, Lean already in place or to be restarted.",
            "role": [
                "You hold the site: safety, quality, cost, deliveries, climate. You report to leadership and you hold your shift leads.",
                "This is not a figurehead role. They want someone who has already carried a plant P&L and still walks the floor.",
            ],
            "duties": [
                "Own the site P&L and investment decisions",
                "Drive safety, quality, Lean and operational performance",
                "Structure the supervision team and succession",
                "Balance production, maintenance and customer service",
                "Represent the site with leadership and, when needed, partners",
            ],
            "profile": [
                "P&L, Lean, managing a 100+ employee site. Senior level.",
                "Bachelor’s degree or equivalent experience. Occasional travel.",
            ],
            "assets": ["Multi-site experience", "Bilingual", "A Lean transformation already led"],
            "offer": [
                "Permanent on-site full-time role",
                "Pay: $120,000 to $150,000",
                "Confidential mandate — the employer is not named here",
                "Talendus scoping interview before any introduction",
            ],
        },
    },
    "developpeur": {
        "fr": {
            "lead": "Talendus recrute un développeur à Montréal. L’employeur cherche quelqu’un qui livre : Python ou JavaScript, deux ans et plus, à l’aise en équipe hybride.",
            "role": [
                "Vous concevez, codez et maintenez des fonctionnalités produit. Revues de code, tickets, mises en production : le quotidien d’une équipe qui avance.",
                "Français et anglais selon les interlocuteurs. On ne cherche pas un titre : on cherche quelqu’un qui a déjà poussé du code en production.",
            ],
            "duties": [
                "Développer et maintenir des fonctionnalités (Python ou JavaScript)",
                "Participer aux revues, aux tests et aux mises en production",
                "Clarifier un besoin avec le produit ou un conseiller métier",
                "Documenter ce qui doit l’être, sans roman",
                "Améliorer ce qui casse trop souvent",
            ],
            "profile": [
                "Python ou JavaScript, au moins 2 ans, travail en équipe déjà vécu.",
                "Portfolio, Git, une mise en production dont vous pouvez parler clairement.",
            ],
            "assets": ["TypeScript / React / FastAPI", "Expérience produit B2B", "Intérêt pour le recrutement ou les ops"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 75 000 à 95 000 $",
                "Français et anglais",
                "Talendus vérifie le niveau avant de vous présenter",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a developer in Montreal. The employer wants someone who ships: Python or JavaScript, two years plus, comfortable in a hybrid team.",
            "role": [
                "You design, code and maintain product features. Code review, tickets, releases: the day-to-day of a team that moves.",
                "French and English depending on stakeholders. They are not hiring a title — they want someone who has already pushed code to production.",
            ],
            "duties": [
                "Build and maintain features (Python or JavaScript)",
                "Join reviews, tests and releases",
                "Clarify a need with product or a business counterpart",
                "Document what must be documented, without a novel",
                "Improve what breaks too often",
            ],
            "profile": [
                "Python or JavaScript, at least 2 years, teamwork already lived.",
                "A portfolio, Git, and a production release you can talk about clearly.",
            ],
            "assets": ["TypeScript / React / FastAPI", "B2B product experience", "Interest in recruiting or ops"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $75,000 to $95,000",
                "French and English",
                "Talendus checks the level before presenting you",
            ],
        },
    },
    "comptable": {
        "fr": {
            "lead": "Talendus recrute un comptable à Québec. L’employeur veut quelqu’un qui ferme un mois, tient Excel et ne laisse pas une facture orpheline.",
            "role": [
                "Vous tenez la comptabilité courante : fournisseurs, clients, rapprochements, taxes, clôture. Hybride, DEC visé.",
                "Le poste convient à un profil intermédiaire qui aime l’ordre et les échéances, pas seulement la saisie.",
            ],
            "duties": [
                "Saisir et contrôler les écritures, les factures et les paiements",
                "Préparer les rapprochements et la clôture mensuelle",
                "Suivre les taxes et les échéances déclaratives",
                "Appuyer le contrôleur ou le CPA sur les dossiers spéciaux",
                "Tenir des fichiers clairs, exploitables le lundi matin",
            ],
            "profile": [
                "Comptabilité déjà pratiquée, Excel solide, diplôme pertinent (DEC ou équivalent).",
                "Vous avez déjà fermé un mois ou tenu un cycle fournisseur/client sans filet.",
            ],
            "assets": ["Acomba / QuickBooks / Sage", "Notions TPS/TVQ", "Anglais lu"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 55 000 à 70 000 $",
                "Équipe finance structurée",
                "Talendus présente un dossier déjà vérifié",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting an accountant in Quebec City. The employer wants someone who can close a month, hold Excel, and not leave an orphan invoice.",
            "role": [
                "You run day-to-day accounting: payables, receivables, reconciliations, taxes, close. Hybrid, DEC preferred.",
                "The role suits an intermediate profile who likes order and deadlines, not only data entry.",
            ],
            "duties": [
                "Enter and check journals, invoices and payments",
                "Prepare reconciliations and the monthly close",
                "Track taxes and filing deadlines",
                "Support the controller or CPA on special files",
                "Keep files clear enough to use on a Monday morning",
            ],
            "profile": [
                "Accounting already practised, solid Excel, relevant diploma (DEC or equivalent).",
                "You have already closed a month or run an AP/AR cycle without a safety net.",
            ],
            "assets": ["Acomba / QuickBooks / Sage", "GST/QST notions", "Reading English"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $55,000 to $70,000",
                "A structured finance team",
                "Talendus presents a file that has already been checked",
            ],
        },
    },
    "ingenieur": {
        "fr": {
            "lead": "Talendus recrute un ingénieur à Sherbrooke. L’employeur cherche un profil qui mène un projet — pas seulement un titre au mur.",
            "role": [
                "Vous prenez un dossier technique : cadrage, planification, coordination des métiers, mise en service. Hybride, baccalauréat.",
                "Trois ans et plus. On veut quelqu’un qui a déjà livré quelque chose qu’on peut visiter.",
            ],
            "duties": [
                "Cadrer le besoin, les délais et les risques d’un projet",
                "Coordonner fournisseurs, production et qualité",
                "Rédiger et suivre plans, devis et essais",
                "Présenter l’avancement clairement à la direction",
                "Rester proche du terrain jusqu’à la mise en service",
            ],
            "profile": [
                "Ingénierie et gestion de projet, environ 3 ans. Niveau senior sur le mandat.",
                "Baccalauréat. Vous savez expliquer un écart sans noyer le sujet.",
            ],
            "assets": ["OIQ ou démarche d’admission", "Lean / Six Sigma", "Anglais technique"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 80 000 à 100 000 $",
                "Projets concrets, décision proche du site",
                "Entretien Talendus de cadrage avant présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting an engineer in Sherbrooke. The employer wants a profile who leads a project — not only a title on the wall.",
            "role": [
                "You take a technical file: scoping, planning, coordinating trades, commissioning. Hybrid, bachelor’s degree.",
                "Three years and up. They want someone who has already delivered something you can walk through.",
            ],
            "duties": [
                "Scope the need, timeline and risks of a project",
                "Coordinate suppliers, production and quality",
                "Write and follow drawings, specs and trials",
                "Present progress clearly to leadership",
                "Stay close to the floor until commissioning",
            ],
            "profile": [
                "Engineering and project management, about 3 years. Senior on this mandate.",
                "Bachelor’s degree. You can explain a variance without drowning the point.",
            ],
            "assets": ["OIQ or admission in progress", "Lean / Six Sigma", "Technical English"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $80,000 to $100,000",
                "Concrete projects, decisions close to the site",
                "Talendus scoping interview before presentation",
            ],
        },
    },
    "chauffeur": {
        "fr": {
            "lead": "Talendus recrute un chauffeur à Anjou. L’employeur veut un permis valide, un dossier propre et quelqu’un qui livre à l’heure — pas un touriste du volant.",
            "role": [
                "Vous faites des routes régionales ou locales selon le mandat : livraisons, ramasses, retours à la cour. Classe 1 visée.",
                "Les déplacements sont fréquents. Pontualité et communication avec le dispatch : non négociables.",
            ],
            "duties": [
                "Effectuer les courses selon le plan de route et les fenêtres client",
                "Inspecter le véhicule, signaler les anomalies",
                "Charger / décharger dans les règles et les limites du site",
                "Tenir les documents de bord et le lien avec le dispatch",
                "Représenter l’employeur chez le client sans improvisation",
            ],
            "profile": [
                "Permis valide (classe 1 visée), dossier de conduite propre, ponctualité réelle.",
                "Une expérience de livraison ou de transport est un plus. On vérifie le dossier.",
            ],
            "assets": ["Expérience frigorifique ou vrac", "Connaissance du grand Montréal", "Disponibilité tôt le matin"],
            "offer": [
                "Poste permanent, temps plein",
                "Rémunération : 22 à 28 $/h",
                "Routes régulières, dispatch structuré",
                "Talendus vérifie permis et disponibilité avant présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a driver in Anjou. The employer wants a valid licence, a clean record, and someone who delivers on time — not a tourist behind the wheel.",
            "role": [
                "You run regional or local routes depending on the mandate: deliveries, pickups, return to the yard. Class 1 is the target.",
                "Travel is frequent. Punctuality and dispatch communication are not negotiable.",
            ],
            "duties": [
                "Run the trips to the route plan and customer windows",
                "Inspect the vehicle and report faults",
                "Load / unload within site rules and limits",
                "Keep onboard documents and the link with dispatch",
                "Represent the employer at the customer without improvising",
            ],
            "profile": [
                "Valid licence (Class 1 targeted), clean driving record, real punctuality.",
                "Delivery or transport experience is a plus. The record is checked.",
            ],
            "assets": ["Reefer or bulk experience", "Knowledge of Greater Montreal", "Early-morning availability"],
            "offer": [
                "Permanent full-time role",
                "Pay: $22 to $28/hr",
                "Regular routes, structured dispatch",
                "Talendus checks licence and availability before presentation",
            ],
        },
    },
    "infirmier": {
        "fr": {
            "lead": "Talendus recrute un infirmier ou une infirmière à Laval. Permis OIIQ obligatoire. L’employeur cherche un professionnel qui tient un quart clinique, pas seulement un CV de stages.",
            "role": [
                "Vous prenez en charge les soins du quart : évaluation, interventions, notes, relais à l’équipe. Les quarts tournent.",
                "Le milieu exact (clinique, CHSLD, entreprise) est précisé à l’entretien. On ne publie pas le nom de l’employeur ici.",
            ],
            "duties": [
                "Évaluer, soigner et consigner selon les protocoles",
                "Coordonner avec l’équipe soignante et les autres professionnels",
                "Gérer les priorités du quart sans perdre un patient de vue",
                "Communiquer clairement aux familles ou aux usagers selon le milieu",
                "Respecter les normes OIIQ et les règles de l’établissement",
            ],
            "profile": [
                "Permis OIIQ en règle, expérience clinique, aisance en équipe.",
                "On veut quelqu’un qui a déjà tenu un quart, pas seulement observé.",
            ],
            "assets": ["Expérience CHSLD, clinique ou santé au travail", "Bilinguisme", "Disponibilité nights / fins de semaine"],
            "offer": [
                "Poste permanent, temps plein, quarts rotatifs",
                "Rémunération : 32 à 42 $/h selon échelon et milieu",
                "Permis OIIQ exigé",
                "Talendus confirme le permis et le milieu avant présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a nurse in Laval. OIIQ licence required. The employer wants a professional who can hold a clinical shift, not only a student résumé.",
            "role": [
                "You own the shift’s care: assessment, interventions, notes, handover. Shifts rotate.",
                "The exact setting (clinic, CHSLD, workplace) is confirmed at interview. The employer is not named here.",
            ],
            "duties": [
                "Assess, treat and document to protocol",
                "Coordinate with the care team and other professionals",
                "Manage the shift’s priorities without losing a patient",
                "Communicate clearly with families or users depending on the setting",
                "Follow OIIQ standards and site rules",
            ],
            "profile": [
                "Valid OIIQ licence, clinical experience, ease in a team.",
                "They want someone who has already held a shift, not only observed.",
            ],
            "assets": ["CHSLD, clinic or occupational-health experience", "Bilingual", "Nights / weekend availability"],
            "offer": [
                "Permanent full-time role, rotating shifts",
                "Pay: $32 to $42/hr depending on scale and setting",
                "OIIQ licence required",
                "Talendus confirms the licence and setting before presentation",
            ],
        },
    },
    "vendeur": {
        "fr": {
            "lead": "Talendus recrute un vendeur à Longueuil. Le commerce cherche quelqu’un qui accueille, conseille et conclut — y compris en temps partiel selon le plancher.",
            "role": [
                "Vous tenez le plancher : accueil, conseil, caisse, remise en rayon. Le quart de jour est le socle ; des soirées peuvent s’ajouter.",
                "Aucune expérience lourde exigée si l’aisance relationnelle est là. On forme le produit, pas le sourire.",
            ],
            "duties": [
                "Accueillir et qualifier le besoin du client",
                "Conseiller, conclure et encaisser",
                "Tenir le rayon propre et approvisionné",
                "Suivre les consignes de l’équipe et les objectifs du jour",
                "Remonter les irritants (stock, file, produit)",
            ],
            "profile": [
                "Vente au détail ou service client, aisance relationnelle. Niveau débutant accepté.",
                "Ponctualité et présentation soignée. On évalue surtout le contact.",
            ],
            "assets": ["Expérience caisse", "Bilinguisme", "Disponibilité samedis"],
            "offer": [
                "Poste permanent, horaire selon le plancher (temps partiel possible)",
                "Rémunération : 18 à 24 $/h",
                "Quart de jour principalement",
                "Talendus vous rappelle pour caler disponibilités et secteur",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a sales associate in Longueuil. The store wants someone who greets, advises and closes — including part-time depending on the floor plan.",
            "role": [
                "You hold the floor: greeting, advice, checkout, restocking. Day shift is the base; evenings may be added.",
                "No heavy experience required if people skills are there. They train the product, not the smile.",
            ],
            "duties": [
                "Greet and qualify the customer’s need",
                "Advise, close and take payment",
                "Keep the bay clean and stocked",
                "Follow team instructions and the day’s goals",
                "Flag irritants (stock, queue, product)",
            ],
            "profile": [
                "Retail or customer service, people skills. Beginner level accepted.",
                "Punctuality and a tidy presentation. Contact is what they assess first.",
            ],
            "assets": ["Checkout experience", "Bilingual", "Saturday availability"],
            "offer": [
                "Permanent role, hours according to the floor (part-time possible)",
                "Pay: $18 to $24/hr",
                "Mostly day shift",
                "Talendus calls you to lock availability and sector",
            ],
        },
    },
    "responsable-rh": {
        "fr": {
            "lead": "Talendus recrute un responsable RH à Montréal. L’employeur veut quelqu’un qui recrute, tient les relations de travail et parle aux gestionnaires — cinq ans et plus.",
            "role": [
                "Vous pilotez le recrutement interne, l’accueil, une partie des relations de travail et le suivi des dossiers employés. Hybride, français et anglais.",
                "Ce n’est pas un poste de « projets RH » hors sol. On veut quelqu’un qui a déjà fermé des postes et tenu une médiation.",
            ],
            "duties": [
                "Recruter : besoin, affichage, entrevues, offre, intégration",
                "Conseiller les gestionnaires sur les situations d’équipe",
                "Tenir les dossiers, les politiques et les échéances légales de base",
                "Appuyer les relations de travail au quotidien",
                "Faire le pont avec Talendus sur les mandats externes",
            ],
            "profile": [
                "Recrutement et relations de travail, environ 5 ans en RH. Niveau senior.",
                "Français et anglais. À l’aise avec des gestionnaires d’opération, pas seulement du siège.",
            ],
            "assets": ["CRHA", "Expérience manufacturière ou multi-sites", "Dotation volume"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 70 000 à 90 000 $",
                "Français et anglais",
                "Cadrage Talendus avant mise en contact avec l’employeur",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting an HR manager in Montreal. The employer wants someone who hires, holds labour relations and talks to managers — five years plus.",
            "role": [
                "You run internal recruiting, onboarding, part of labour relations and employee files. Hybrid, French and English.",
                "This is not an off-the-floor “HR projects” seat. They want someone who has already closed roles and held a mediation.",
            ],
            "duties": [
                "Recruit: need, posting, interviews, offer, onboarding",
                "Advise managers on team situations",
                "Keep files, policies and basic legal deadlines",
                "Support day-to-day labour relations",
                "Bridge with Talendus on external mandates",
            ],
            "profile": [
                "Recruiting and labour relations, about 5 years in HR. Senior level.",
                "French and English. Comfortable with operations managers, not only head office.",
            ],
            "assets": ["CRHA", "Manufacturing or multi-site experience", "Volume hiring"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $70,000 to $90,000",
                "French and English",
                "Talendus scoping before any introduction to the employer",
            ],
        },
    },
    "specialiste-marketing": {
        "fr": {
            "lead": "Talendus recrute un spécialiste marketing à Montréal. L’employeur cherche quelqu’un qui mène des campagnes — pas seulement qui en parle.",
            "role": [
                "Vous planifiez, produisez et suivez des campagnes (web, contenus, parfois paid). Hybride.",
                "On veut des livrables : pages, séquences, rapports que la direction peut lire. Niveau intermédiaire.",
            ],
            "duties": [
                "Planifier et exécuter des campagnes digitales et de contenu",
                "Rédiger et adapter les messages selon l’audience",
                "Suivre les indicateurs et ajuster ce qui ne performe pas",
                "Coordonner freelances, agence ou internes selon le dossier",
                "Rendre compte clairement, sans jargon inutile",
            ],
            "profile": [
                "Marketing digital, communication, gestion de campagnes déjà pratiqués.",
                "Portfolio ou exemples concrets. Français impeccable ; anglais un plus.",
            ],
            "assets": ["Ads / SEO / automation", "Expérience B2B", "Notion de CRM"],
            "offer": [
                "Poste permanent, temps plein, hybride",
                "Rémunération : 55 000 à 75 000 $",
                "Autonomie sur les campagnes, décision proche du métier",
                "Talendus relit le portfolio avant présentation",
            ],
        },
        "en": {
            "lead": "Talendus is recruiting a marketing specialist in Montreal. The employer wants someone who runs campaigns — not only talks about them.",
            "role": [
                "You plan, produce and track campaigns (web, content, sometimes paid). Hybrid.",
                "They want deliverables: pages, sequences, reports leadership can read. Intermediate level.",
            ],
            "duties": [
                "Plan and run digital and content campaigns",
                "Write and adapt messages for the audience",
                "Track indicators and adjust what does not perform",
                "Coordinate freelancers, an agency or internals depending on the file",
                "Report clearly, without spare jargon",
            ],
            "profile": [
                "Digital marketing, communications and campaign management already practised.",
                "A portfolio or concrete examples. Strong French; English a plus.",
            ],
            "assets": ["Ads / SEO / automation", "B2B experience", "CRM notions"],
            "offer": [
                "Permanent full-time hybrid role",
                "Pay: $55,000 to $75,000",
                "Autonomy on campaigns, decisions close to the work",
                "Talendus reviews the portfolio before presentation",
            ],
        },
    },
}


def job_story(slug: str, lang: str = "fr") -> dict:
    pack = STORIES.get(slug) or {}
    key = "en" if lang == "en" else "fr"
    return pack.get(key) or pack.get("fr") or {}


def job_prose_html(slug: str, fallback_title: str, fallback_city: str, fallback_sector: str, fallback_skills: str, fallback_req: str, chips: str, lang: str = "fr") -> str:
    story = job_story(slug, lang)
    is_en = lang == "en"
    role_h = "The role" if is_en else "Le poste"
    duty_h = "What you will do" if is_en else "Ce que vous ferez"
    profile_h = "Profile we look for" if is_en else "Profil recherché"
    asset_h = "Assets" if is_en else "Atouts"
    offer_h = "What the mandate includes" if is_en else "Ce que comprend le mandat"
    how_h = "How applying works" if is_en else "Comment postuler"

    role_html = _paras(story.get("role") or [
        f"A {fallback_title.lower()} mandate in {fallback_city}, in {fallback_sector}. Skills in focus: {fallback_skills}."
        if is_en
        else f"Un mandat de {fallback_title.lower()} à {fallback_city}, en {fallback_sector}. Compétences visées : {fallback_skills}."
    ])
    duties = story.get("duties") or []
    duties_html = f"<h2>{duty_h}</h2>{_ul(duties)}" if duties else ""
    profile_blocks = story.get("profile") or [fallback_req]
    profile_html = _paras(profile_blocks)
    assets = story.get("assets") or []
    assets_html = f"<h2>{asset_h}</h2>{_ul(assets)}" if assets else ""
    offer = story.get("offer") or []
    offer_html = f"<h2>{offer_h}</h2>{_ul(offer)}" if offer else ""

    if is_en:
        steps = """
          <ol class="tl-job-steps">
            <li><span class="tl-job-step-n">1</span><div><strong>You apply here with your resume.</strong><p>PDF, Word or image. Your file reaches Talendus — not a public job board inbox.</p></div></li>
            <li><span class="tl-job-step-n">2</span><div><strong>A consultant reviews it.</strong><p>We check the fit with the mandate before anything is shared with the employer.</p></div></li>
            <li><span class="tl-job-step-n">3</span><div><strong>If it holds, we present you.</strong><p>We speak to the employer on your behalf and stay on the file.</p></div></li>
            <li><span class="tl-job-step-n">4</span><div><strong>You follow the next steps with us.</strong><p>Interviews, updates and the offer go through Talendus.</p></div></li>
          </ol>"""
    else:
        steps = """
          <ol class="tl-job-steps">
            <li><span class="tl-job-step-n">1</span><div><strong>Vous postulez ici avec votre CV.</strong><p>PDF, Word ou image. Votre dossier arrive chez Talendus — pas dans une boîte publique d’offres.</p></div></li>
            <li><span class="tl-job-step-n">2</span><div><strong>Un conseiller l'étudie.</strong><p>Nous vérifions la correspondance avec le mandat avant tout partage à l’employeur.</p></div></li>
            <li><span class="tl-job-step-n">3</span><div><strong>Si ça colle, nous vous présentons.</strong><p>Nous parlons à l’employeur pour vous et restons sur le dossier.</p></div></li>
            <li><span class="tl-job-step-n">4</span><div><strong>Vous suivez la suite avec nous.</strong><p>Entretiens, nouvelles et offre passent par Talendus.</p></div></li>
          </ol>"""

    return f"""
          <h2>{role_h}</h2>
          {role_html}
          {duties_html}
          <h2>{profile_h}</h2>
          {profile_html}
          {chips}
          {assets_html}
          {offer_html}
          <h2>{how_h}</h2>
          {steps}
    """


def catalog_db_fields(slug: str) -> dict:
    """Champs texte pour JobOffer (FR) à partir du récit public."""
    story = job_story(slug, "fr")
    if not story:
        return {}
    return {
        "description": "\n\n".join(story.get("role") or []),
        "responsibilities": "\n".join(f"- {item}" for item in (story.get("duties") or [])),
        "benefits": " · ".join((story.get("offer") or [])[:3]) or "Assurance collective",
    }
