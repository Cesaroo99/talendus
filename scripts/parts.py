HEADER_NAV = """
                              <li data-nav="home"><a href="index.html">Accueil</a></li>
                              <li class="has-dropdown" data-nav="employeurs">
                                <a href="employeurs.html">Employeurs <span><i class="fa-solid fa-angle-down d-lg-inline d-none"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="employeurs.html">Pourquoi Talendus</a></li>
                                      <li><a href="services.html">Services de recrutement</a></li>
                                      <li><a href="secteurs.html">Secteurs desservis</a></li>
                                      <li><a href="employeurs.html#calculateur">Calculateur d'embauche</a></li>
                                  </ul>
                              </li>
                              <li class="has-dropdown" data-nav="candidats">
                                <a href="candidats.html">Candidats <span><i class="fa-solid fa-angle-down d-lg-inline d-none"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="emplois.html">Offres d'emploi</a></li>
                                      <li><a href="candidats.html#cv">Dépôt de CV</a></li>
                                      <li><a href="candidats.html#processus">Processus</a></li>
                                  </ul>
                              </li>
                              <li data-nav="services"><a href="services.html">Services</a></li>
                              <li data-nav="about"><a href="a-propos.html">À propos</a></li>
                              <li data-nav="blog"><a href="blog.html">Blog</a></li>
                              <li data-nav="contact"><a href="contact.html">Contact</a></li>
"""

PRELOADER = """
<div class="preloader tl-preloader" role="status" aria-label="Chargement Talendus">
  <div class="tl-preloader-stage">
    <div class="tl-preloader-orbit" aria-hidden="true">
      <span class="tl-ring tl-ring-a"></span>
      <span class="tl-ring tl-ring-b"></span>
      <span class="tl-ring tl-ring-c"></span>
      <div class="tl-preloader-mark">
        <svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
          <path fill="#ffffff" fill-rule="evenodd" d="M18 1.5c9.113 0 16.5 7.387 16.5 16.5S27.113 34.5 18 34.5 1.5 27.113 1.5 18 8.887 1.5 18 1.5zm-7.25 9.75h14.5a1.75 1.75 0 1 1 0 3.5h-5.5v12.75a1.75 1.75 0 1 1-3.5 0V14.75h-5.5a1.75 1.75 0 1 1 0-3.5z"/>
        </svg>
      </div>
    </div>
    <p class="tl-preloader-word">Talendus</p>
    <p class="tl-preloader-tag">Recrutement industriel · Québec</p>
    <div class="tl-preloader-bar" aria-hidden="true"><span></span></div>
  </div>
</div>
"""

def head(title, description, canonical, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="fr-CA">
<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>{title}</title>
     <meta name="description" content="{description}">
     <link rel="canonical" href="https://talendus.ca/{canonical}">
     <meta property="og:title" content="{title}">
     <meta property="og:description" content="{description}">
     <meta property="og:type" content="website">
     <meta property="og:url" content="https://talendus.ca/{canonical}">
     <meta name="robots" content="index,follow">
    <link rel="shortcut icon" href="assets/img/logo/fav-logo1.png" type="image/png">
    <link rel="stylesheet" href="assets/css/plugins/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/plugins/aos.css">
    <link rel="stylesheet" href="assets/css/plugins/fontawesome.css">
    <link rel="stylesheet" href="assets/css/plugins/magnific-popup.css">
    <link rel="stylesheet" href="assets/css/plugins/slick-slider.css">
    <link rel="stylesheet" href="assets/css/plugins/nice-select.css">
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/talendus.css">
    {extra_css}
</head>
"""

def header(solid=True):
    cls = "tl-solid-header" if solid else ""
    return f"""<body class="{cls}">
{PRELOADER}
<header class="homepage2-body">
  <div id="vl-header-sticky" class="vl-header-area vl-transparent-header">
      <div class="container">
          <div class="row align-items-center">
              <div class="col-lg-2 col-md-6 col-6">
                  <div class="vl-logo">
                      <a href="index.html"><img src="assets/img/logo/logo1.png" alt="Talendus"></a>
                  </div>
              </div>
              <div class="col-lg-7 d-none d-lg-block">
                  <div class="vl-main-menu text-center">
                      <nav class="vl-mobile-menu-active">
                          <ul>
{HEADER_NAV}
                          </ul>
                      </nav>
                  </div>
              </div>
              <div class="col-lg-3 col-md-6 col-6">
                <div class="vl-hero-btn d-none d-lg-block text-end">
                  <div class="hero-btn1">
                    <a href="contact.html" class="vl-btn2 tl-header-cta">Consultation gratuite <span><i class="fa-solid fa-arrow-right"></i></span></a>
                  </div>
                </div>
                  <div class="vl-header-action-item d-block d-lg-none">
                      <button type="button" class="vl-offcanvas-toggle">
                        <i class="fa-solid fa-bars-staggered"></i>
                      </button>
                   </div>
              </div>
          </div>
      </div>
  </div>
</header>
<div class="homepage2-body">
  <div class="vl-offcanvas">
    <div class="vl-offcanvas-wrapper">
        <div class="vl-offcanvas-header d-flex justify-content-between align-items-center mb-90">
            <div class="vl-offcanvas-logo">
                <a href="index.html"><img src="assets/img/logo/logo1.png" alt="Talendus"></a>
            </div>
            <div class="vl-offcanvas-close">
               <button class="vl-offcanvas-close-toggle"><i class="fa-solid fa-xmark"></i></button>
            </div>
        </div>
        <div class="vl-offcanvas-menu d-lg-none mb-40"><nav></nav></div>
        <div class="vl-offcanvas-info">
            <h3 class="vl-offcanvas-sm-title">Talendus</h3>
            <div class="space20"></div>
            <span><a href="tel:+15145550199"><i class="fa-solid fa-phone"></i> 514 555-0199</a></span>
            <span><a href="mailto:info@talendus.ca"><i class="fa-regular fa-envelope"></i> info@talendus.ca</a></span>
            <span><a href="contact.html"><i class="fa-solid fa-location-dot"></i> Montréal, Québec · sur rendez-vous</a></span>
            <p class="tl-offcanvas-note">Réponse moyenne sous 30 minutes durant les heures d'ouverture.</p>
            <div class="vl-offcanvas-cta">
              <a href="contact.html" class="tl-btn">Réserver une consultation</a>
              <a href="candidats.html#cv" class="tl-btn tl-btn-electric">Déposer mon CV</a>
            </div>
        </div>
    </div>
  </div>
  <div class="vl-offcanvas-overlay"></div>
</div>
"""

SPEED_STRIP = """
<section class="tl-speed">
  <div class="container">
    <div class="tl-speed-inner">
      <div>
        <span class="tl-badge tl-badge-light">Délai d’exécution</span>
        <h2>Premiers candidats qualifiés à partir de 7 jours.</h2>
        <p>Une shortlist industrielle, pas une pile de CV. On ouvre le mandat, on filtre comme un contremaître, on vous présente des dossiers défendables.</p>
      </div>
      <div class="tl-speed-actions">
        <a class="tl-btn tl-btn-lg" href="contact.html">Réserver une consultation gratuite</a>
        <a class="tl-btn tl-btn-ghost" href="contact.html">Demander un recrutement</a>
      </div>
    </div>
  </div>
</section>
"""

CTA_BAND = """
<section class="tl-cta-band">
  <div class="container">
    <span class="tl-badge tl-badge-light">Cabinet industriel</span>
    <h2 class="tl-h2">Votre usine n’a pas besoin d’une agence généraliste.</h2>
    <p>Un interlocuteur qui parle production, quarts et SST. Consultation gratuite, sur rendez-vous. Réponse moyenne sous 30 minutes durant les heures d’ouverture.</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="contact.html">Obtenir une consultation gratuite</a>
      <a class="tl-btn tl-btn-ghost" href="candidats.html#cv">Déposer mon CV</a>
    </div>
  </div>
</section>
"""

FOOTER = """
<div class="tl-sticky">
  <a href="contact.html">Réserver une consultation</a>
  <a class="alt" href="candidats.html#cv">Déposer mon CV</a>
</div>
<div class="vl-footer2-section-area">
  <div class="container">
    <div class="row">
      <div class="col-lg-3 col-md-6">
        <div class="footer-logo-area">
          <img src="assets/img/logo/logo1.png" alt="Talendus">
          <div class="space16"></div>
          <p>Nous recrutons exclusivement pour les usines, entrepôts et entreprises manufacturières du Québec.</p>
          <p class="tl-muted" style="margin-top:12px">Consultations sur rendez-vous uniquement.</p>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area foot-padding1">
          <h3>Cabinet</h3>
          <ul>
            <li><a href="a-propos.html">À propos</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="secteurs.html">Secteurs</a></li>
            <li><a href="blog.html">Blog</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area foot-padding2">
          <h3>Recrutement</h3>
          <ul>
            <li><a href="employeurs.html">Employeurs</a></li>
            <li><a href="candidats.html">Candidats</a></li>
            <li><a href="emplois.html">Offres d'emploi</a></li>
            <li><a href="services.html">Chasse de têtes</a></li>
            <li><a href="contact.html">Mandat urgent</a></li>
          </ul>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area">
          <h3>Contact</h3>
          <ul>
            <li><a href="tel:+15145550199">514 555-0199</a></li>
            <li><a href="mailto:info@talendus.ca">info@talendus.ca</a></li>
            <li>Lun–Ven, 8 h à 17 h</li>
            <li><a href="contact.html">Montréal · sur rendez-vous</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="space48"></div>
    <div class="col-lg-12">
      <div class="copyright-area">
        <a href="index.html">© 2026 Talendus. Tous droits réservés. talendus.ca</a>
        <ul>
          <li><a href="confidentialite.html">Confidentialité</a><span> | </span></li>
          <li><a href="conditions.html">Conditions</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
<script src="assets/js/plugins/jquery-3-7-1.min.js"></script>
<script src="assets/js/plugins/bootstrap.min.js"></script>
<script src="assets/js/plugins/fontawesome.js"></script>
<script src="assets/js/plugins/aos.js"></script>
<script src="assets/js/plugins/counter.js"></script>
<script src="assets/js/plugins/magnific-popup.js"></script>
<script src="assets/js/plugins/nice-select.js"></script>
<script src="assets/js/plugins/waypoints.js"></script>
<script src="assets/js/plugins/slick-slider.js"></script>
<script src="assets/js/plugins/circle-progress.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/talendus.js"></script>
</body>
</html>
"""

def page_hero(kicker, title, lead, actions="", badges=""):
    act = f'<div class="tl-actions">{actions}</div>' if actions else ""
    return f"""
<section class="tl-page-hero">
  <div class="container">
    {badges}
    <div class="tl-kicker">{kicker}</div>
    <h1 class="tl-h1">{title}</h1>
    <p class="tl-lead">{lead}</p>
    {act}
  </div>
</section>
"""

def faq_html(items, open_first=True):
    parts = ['<div class="tl-faq">']
    for i, (q, a) in enumerate(items):
        opened = " open" if open_first and i == 0 else ""
        parts.append(f"<details{opened}><summary>{q}</summary><p>{a}</p></details>")
    parts.append("</div>")
    return "".join(parts)

FAQ_HOME = [
    ("Talendus est-il une agence de placement généraliste ?",
     "Non. Nous ne recrutons pas en bureau, en TI, en vente ou en service à la clientèle. Talendus travaille exclusivement avec des usines, des entrepôts et des entreprises manufacturières du Québec."),
    ("À partir de quand recevons-nous les premiers candidats ?",
     "Sur les mandats d’opération, de cariste et plusieurs métiers d’usine, les premiers candidats qualifiés arrivent à partir de 7 jours. Ce délai correspond à une shortlist filtrée — pas à une pile de CV. Un machiniste CNC rare ou un directeur d’usine prend davantage de temps : nous l’annonçons dès le brief."),
    ("Dans quelles régions du Québec recrutez-vous ?",
     "Grand Montréal, Laval, Rive-Sud, Montérégie, Estrie, Centre-du-Québec, Mauricie et région de Québec. Nous menons aussi des mandats en région lorsque le profil l’exige."),
    ("Comment se passe une consultation ?",
     "Les consultations sont sur rendez-vous uniquement. Un appel de 30 minutes suffit pour comprendre le quart, le salaire réel, la SST et l’urgence. Réponse moyenne sous 30 minutes durant les heures d’ouverture (lun.–ven., 8 h à 17 h)."),
    ("Offrez-vous une garantie de remplacement ?",
     "Oui, sur les mandats permanents. La durée est confirmée à l’ouverture du dossier, par écrit. Le suivi 30/60/90 jours fait partie du mandat, pas d’une option."),
    ("Travaillez-vous avec des candidats en recherche active seulement ?",
     "Non. Une part importante de notre vivier est passive : opérateurs, métiers et cadres déjà en poste que nous approchons discrètement. C’est souvent là que se trouvent les profils qui restent."),
    ("Puis-je déposer un CV même s’il n’y a pas d’offre affichée ?",
     "Oui. Plusieurs mandats sont confidentiels. Nous qualifions votre métier, vos quarts et votre mobilité, puis nous vous présentons lorsqu’un employeur industriel correspond."),
    ("Comment facturez-vous les employeurs ?",
     "Honoraires au succès, calculés sur le salaire annuel du candidat placé. Aucun frais si le mandat n’aboutit pas, selon les conditions de l’entente. La consultation initiale est gratuite."),
]

FAQ_EMPLOYEURS = [
    ("Combien de temps avant les premiers dossiers ?",
     "Premiers candidats qualifiés à partir de 7 jours sur les métiers d’opération et plusieurs postes d’usine. Superviseurs, métiers rares et cadres : 3 à 8 semaines, annoncé dès la consultation — sans promesse cosmétique."),
    ("Que se passe-t-il pendant la consultation ?",
     "Sur rendez-vous. Nous parlons quart, compétences, SST, salaire réel et ce qui a déjà échoué. Vous repartez avec un plan de recherche, pas un discours RH générique."),
    ("Présentez-vous beaucoup de CV ?",
     "Non. L’objectif est que votre contremaître ne perde pas une heure. Nous filtrons, nous rencontrons, nous présentons peu de dossiers — chacun défendable."),
    ("Intervenez-vous en région ?",
     "Oui. Outre le Grand Montréal, nous menons des mandats en Montérégie, Estrie, Centre-du-Québec, Mauricie et région de Québec."),
    ("Comment sont calculés les honoraires ?",
     "Au succès, sur le salaire annuel du candidat placé. Pas de frais si le mandat n’aboutit pas, selon l’entente. La consultation est gratuite."),
    ("Quelle garantie offrez-vous ?",
     "Remplacement inclus sur les mandats permanents. Durée confirmée à l’ouverture. Suivi d’intégration 30/60/90 jours."),
    ("Pouvez-vous mener un mandat confidentiel ?",
     "Oui. Remplacement de cadre, réorganisation ou poste sensible : approche discrète, sans bruit interne, jusqu’à ce que vous choisissiez le moment de communiquer."),
    ("Recrutez-vous aussi du personnel de bureau ?",
     "Non. Si le poste n’est pas en usine, en entrepôt, en logistique ou en gestion manufacturière, nous déclinons. C’est ce qui protège la qualité du vivier."),
]

FAQ_CANDIDATS = [
    ("Dois-je payer pour vos services ?",
     "Non. Les honoraires sont assumés par l’employeur. Le dépôt de CV et l’accompagnement jusqu’à l’embauche sont sans frais pour vous."),
    ("Que se passe-t-il après l’envoi de mon CV ?",
     "Nous qualifions votre métier, vos quarts et votre région. S’il y a correspondance, un conseiller vous appelle. Réponse moyenne sous 30 minutes durant les heures d’ouverture lorsque vous nous écrivez ou nous joignez."),
    ("Puis-je postuler s’il n’y a pas d’offre affichée ?",
     "Oui. Plusieurs usines recrutent en mandat confidentiel. Votre profil reste actif dans notre vivier industriel."),
    ("Quels métiers placez-vous ?",
     "Journalier, opérateur, cariste, soudeur, machiniste CNC, électromécanicien, mécanicien industriel, superviseur, coordonnateur logistique, directeur d’usine — et les métiers connexes d’atelier."),
    ("M’enverrez-vous sur des entrevues au hasard ?",
     "Non. Nous présentons votre dossier uniquement aux employeurs manufacturiers dont le quart, le salaire et l’environnement correspondent à ce que vous avez indiqué."),
    ("Travaillez-vous partout au Québec ?",
     "Principalement le Grand Montréal, Laval, la Rive-Sud, la Montérégie, l’Estrie, le Centre-du-Québec et Québec. Dites-nous votre mobilité : nous ciblons en conséquence."),
]
