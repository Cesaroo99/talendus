SITE = "https://talendus.ca"
WA_HREF = "https://wa.me/15145550199?text="
OG_IMAGE = "assets/img/all-images/industry/usine-equipe.jpg"

import html as html_lib
import json

def pfx(lang):
    return "../" if lang == "en" else ""


def wa_link(lang):
    msg = (
        "Hello%20Talendus%2C%20I%20would%20like%20to%20talk%20about%20a%20hiring%20need."
        if lang == "en"
        else "Bonjour%20Talendus%2C%20je%20souhaite%20discuter%20d%27un%20besoin%20de%20recrutement."
    )
    return WA_HREF + msg


COPY = {
    "fr": {
        "html_lang": "fr-CA",
        "og_locale": "fr_CA",
        "tagline": "Les talents qui font tourner l'industrie.",
        "preloader_tag": "Recrutement industriel · Québec",
        "preloader_aria": "Chargement Talendus",
        "nav_home": "Accueil",
        "nav_employers": "Entreprises",
        "nav_why": "Pourquoi Talendus",
        "nav_services": "Services de recrutement",
        "nav_sectors": "Secteurs desservis",
        "nav_calc": "Calculateur d'embauche",
        "nav_candidates": "Candidats",
        "nav_jobs": "Offres d'emploi",
        "nav_cv": "Dépôt de CV",
        "nav_process": "Processus",
        "nav_services_top": "Services",
        "nav_about": "À propos",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "Mon espace",
        "nav_employer_account": "Espace employeur",
        "nav_svc_industrial": "Recrutement industriel",
        "nav_svc_mfg": "Recrutement manufacturier",
        "nav_svc_tech": "Recrutement technique",
        "nav_svc_perm": "Recrutement permanent",
        "nav_svc_temp": "Recrutement temporaire",
        "nav_svc_search": "Chasse de têtes",
        "nav_svc_lead": "Recrutement de cadres",
        "footer_places": "Régions",
        "cta_primary": "Confier un recrutement",
        "cta_secondary": "Déposer mon CV",
        "menu_open": "Ouvrir le menu",
        "menu_close": "Fermer le menu",
        "offcanvas_note": "Réponse moyenne sous 30 minutes durant les heures d’ouverture.",
        "offcanvas_place": "Montréal, Québec · sur rendez-vous",
        "consult": "Réserver une consultation",
        "footer_blurb": "Partenaire de recrutement pour les entreprises opérationnelles du Québec : production, maintenance, logistique, supervision et continuité des activités.",
        "footer_rdv": "Consultations sur rendez-vous uniquement.",
        "footer_cabinet": "Cabinet",
        "footer_recruit": "Recrutement",
        "footer_contact": "Contact",
        "footer_hours": "Lun–Ven, 8 h à 17 h",
        "footer_place": "Montréal · sur rendez-vous",
        "footer_copy": "© 2026 Talendus. Tous droits réservés. talendus.ca",
        "privacy": "Confidentialité",
        "terms": "Conditions",
        "sticky_consult": "Réserver une consultation",
        "wa_label": "Écrire à Talendus sur WhatsApp",
        "speed_kicker": "Délai d’exécution",
        "speed_h2": "Premiers candidats qualifiés à partir de 7 jours.",
        "speed_p": "Une shortlist industrielle, pas une pile de CV. On ouvre le mandat, on filtre comme un contremaître, on vous présente des dossiers défendables.",
        "cta_kicker": "Cabinet industriel",
        "cta_h2": "Votre usine n’a pas besoin d’une agence généraliste.",
        "cta_p": "Un interlocuteur qui parle production, quarts et SST. Consultation gratuite, sur rendez-vous. Réponse moyenne sous 30 minutes durant les heures d’ouverture.",
        "keywords": "recrutement industriel Québec, recrutement manufacturier Québec, recrutement production Québec, recrutement électromécanicien, recrutement soudeur, recrutement cariste, recrutement maintenance industrielle",
    },
    "en": {
        "html_lang": "en-CA",
        "og_locale": "en_CA",
        "tagline": "The talent that keeps industry moving.",
        "preloader_tag": "Industrial recruiting · Quebec",
        "preloader_aria": "Loading Talendus",
        "nav_home": "Home",
        "nav_employers": "Employers",
        "nav_why": "Why Talendus",
        "nav_services": "Recruiting services",
        "nav_sectors": "Industries we serve",
        "nav_calc": "Hiring calculator",
        "nav_candidates": "Candidates",
        "nav_jobs": "Job openings",
        "nav_cv": "Submit a resume",
        "nav_process": "How it works",
        "nav_services_top": "Services",
        "nav_about": "About",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "My account",
        "nav_employer_account": "Employer portal",
        "nav_svc_industrial": "Industrial recruiting",
        "nav_svc_mfg": "Manufacturing recruiting",
        "nav_svc_tech": "Technical recruiting",
        "nav_svc_perm": "Permanent recruiting",
        "nav_svc_temp": "Temporary recruiting",
        "nav_svc_search": "Executive search",
        "nav_svc_lead": "Leadership recruiting",
        "footer_places": "Regions",
        "cta_primary": "Start a hire",
        "cta_secondary": "Submit my resume",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "offcanvas_note": "Average response under 30 minutes during business hours.",
        "offcanvas_place": "Montreal, Quebec · by appointment",
        "consult": "Book a consultation",
        "footer_blurb": "A recruiting partner for Quebec operations: production, maintenance, logistics, supervision and business continuity.",
        "footer_rdv": "Consultations by appointment only.",
        "footer_cabinet": "Firm",
        "footer_recruit": "Recruiting",
        "footer_contact": "Contact",
        "footer_hours": "Mon–Fri, 8 a.m. to 5 p.m.",
        "footer_place": "Montreal · by appointment",
        "footer_copy": "© 2026 Talendus. All rights reserved. talendus.ca",
        "privacy": "Privacy",
        "terms": "Terms",
        "sticky_consult": "Book a consultation",
        "wa_label": "Message Talendus on WhatsApp",
        "speed_kicker": "Time to shortlist",
        "speed_h2": "Qualified candidates from day 7.",
        "speed_p": "An industrial shortlist, not a stack of resumes. We open the mandate, screen like a floor supervisor, and send files you can defend.",
        "cta_kicker": "Industrial firm",
        "cta_h2": "Your plant does not need a generalist agency.",
        "cta_p": "One contact who speaks production, shifts and health & safety. Free consultation, by appointment. Average response under 30 minutes during business hours.",
        "keywords": "industrial recruitment Quebec, manufacturing recruitment Quebec, production recruitment Quebec, electromechanical technician recruitment, welder recruitment, forklift operator recruitment, industrial maintenance recruitment",
    },
}

HREFS = {
    "fr": {
        "home": "index.html",
        "employers": "entreprises.html",
        "services": "services.html",
        "sectors": "secteurs.html",
        "calc": "entreprises.html#calculateur",
        "candidates": "candidats.html",
        "jobs": "emplois.html",
        "cv": "candidats.html#cv",
        "process": "candidats.html#processus",
        "about": "a-propos.html",
        "blog": "blog.html",
        "contact": "contact.html",
        "privacy": "confidentialite.html",
        "terms": "conditions.html",
        "headhunt": "chasse-de-tetes.html",
        "urgent": "contact.html",
        "account": "espace.html",
        "employer_account": "espace-employeur.html",
        "svc_industrial": "recrutement-industriel.html",
        "svc_mfg": "recrutement-manufacturier.html",
        "svc_tech": "recrutement-technique.html",
        "svc_perm": "recrutement-permanent.html",
        "svc_temp": "recrutement-temporaire.html",
        "svc_search": "chasse-de-tetes.html",
        "svc_lead": "recrutement-cadres.html",
        "geo_mtl": "recrutement-industriel-montreal.html",
        "geo_laval": "recrutement-industriel-laval.html",
        "geo_long": "recrutement-industriel-longueuil.html",
        "geo_qc": "recrutement-industriel-quebec.html",
    },
    "en": {
        "home": "index.html",
        "employers": "employers.html",
        "services": "services.html",
        "sectors": "sectors.html",
        "calc": "employers.html#calculator",
        "candidates": "candidates.html",
        "jobs": "jobs.html",
        "cv": "candidates.html#cv",
        "process": "candidates.html#process",
        "about": "about.html",
        "blog": "blog.html",
        "contact": "contact.html",
        "privacy": "privacy.html",
        "terms": "terms.html",
        "headhunt": "executive-search.html",
        "urgent": "contact.html",
        "account": "account.html",
        "employer_account": "account-employer.html",
        "svc_industrial": "industrial-recruiting.html",
        "svc_mfg": "manufacturing-recruiting.html",
        "svc_tech": "technical-recruiting.html",
        "svc_perm": "permanent-recruiting.html",
        "svc_temp": "temporary-recruiting.html",
        "svc_search": "executive-search.html",
        "svc_lead": "leadership-recruiting.html",
        "geo_mtl": "industrial-recruiting-montreal.html",
        "geo_laval": "industrial-recruiting-laval.html",
        "geo_long": "industrial-recruiting-longueuil.html",
        "geo_qc": "industrial-recruiting-quebec.html",
    },
}


def nav_html(lang):
    t, h = COPY[lang], HREFS[lang]
    return f"""
                              <li data-nav="home"><a href="{h['home']}">{t['nav_home']}</a></li>
                              <li class="has-dropdown" data-nav="employeurs">
                                <a href="{h['employers']}">{t['nav_employers']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['employers']}">{t['nav_why']}</a></li>
                                      <li><a href="{h['services']}">{t['nav_services']}</a></li>
                                      <li><a href="{h['sectors']}">{t['nav_sectors']}</a></li>
                                      <li><a href="{h['calc']}">{t['nav_calc']}</a></li>
                                      <li><a href="{h['employer_account']}">{t['nav_employer_account']}</a></li>
                                  </ul>
                              </li>
                              <li class="has-dropdown" data-nav="candidats">
                                <a href="{h['candidates']}">{t['nav_candidates']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['jobs']}">{t['nav_jobs']}</a></li>
                                      <li><a href="{h['cv']}">{t['nav_cv']}</a></li>
                                      <li><a href="{h['process']}">{t['nav_process']}</a></li>
                                      <li><a href="{h['account']}">{t['nav_account']}</a></li>
                                  </ul>
                              </li>
                              <li class="has-dropdown" data-nav="services">
                                <a href="{h['services']}">{t['nav_services_top']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['svc_industrial']}">{t['nav_svc_industrial']}</a></li>
                                      <li><a href="{h['svc_mfg']}">{t['nav_svc_mfg']}</a></li>
                                      <li><a href="{h['svc_tech']}">{t['nav_svc_tech']}</a></li>
                                      <li><a href="{h['svc_perm']}">{t['nav_svc_perm']}</a></li>
                                      <li><a href="{h['svc_temp']}">{t['nav_svc_temp']}</a></li>
                                      <li><a href="{h['svc_search']}">{t['nav_svc_search']}</a></li>
                                      <li><a href="{h['svc_lead']}">{t['nav_svc_lead']}</a></li>
                                  </ul>
                              </li>
                              <li data-nav="about"><a href="{h['about']}">{t['nav_about']}</a></li>
                              <li data-nav="blog"><a href="{h['blog']}">{t['nav_blog']}</a></li>
                              <li data-nav="contact"><a href="{h['contact']}">{t['nav_contact']}</a></li>
"""


def lang_switcher(lang, alt_url):
    if lang == "fr":
        fr_href, en_href, fr_cls, en_cls = "#", alt_url or "en/index.html", "is-active", ""
    else:
        fr_href, en_href, fr_cls, en_cls = alt_url or "../index.html", "#", "", "is-active"
    return f"""<nav class="tl-lang" aria-label="Language / Langue">
                    <a class="{fr_cls}" href="{fr_href}" lang="fr" hreflang="fr-CA">FR</a>
                    <a class="{en_cls}" href="{en_href}" lang="en" hreflang="en-CA">EN</a>
                  </nav>"""


def preloader(lang, a):
    t = COPY[lang]
    return f"""
<div class="preloader tl-preloader" role="status" aria-label="{t['preloader_aria']}">
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
    <p class="tl-preloader-tag">{t['preloader_tag']}</p>
    <div class="tl-preloader-bar" aria-hidden="true"><span></span></div>
  </div>
</div>
"""


def whatsapp_fab(lang):
    t = COPY[lang]
    return f"""<a class="tl-whatsapp" href="{wa_link(lang)}" target="_blank" rel="noopener noreferrer" aria-label="{t['wa_label']}">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M19.11 17.47c-.29-.15-1.73-.85-2-.95-.27-.1-.46-.15-.66.15s-.76.95-.93 1.15c-.17.2-.34.22-.63.07-.29-.15-1.22-.45-2.33-1.43-.86-.77-1.44-1.72-1.61-2.01-.17-.29-.02-.45.13-.6.13-.13.29-.34.43-.51.15-.17.2-.29.29-.48.1-.2.05-.36-.02-.51-.07-.15-.66-1.59-.9-2.18-.24-.57-.48-.49-.66-.5h-.56c-.2 0-.51.07-.78.36-.27.29-1.02.99-1.02 2.42s1.05 2.81 1.19 3 .07.15 2.06 3.15c1.64 1.41 2.96 1.85 3.58 2.06.54.17 1.04.15 1.43.09.44-.06 1.73-.71 1.97-1.39.24-.68.24-1.27.17-1.39-.07-.12-.26-.2-.55-.35zM16.03 4.05C9.41 4.05 4.05 9.4 4.05 16.03c0 2.11.55 4.17 1.6 5.99L4 28l6.12-1.6a11.94 11.94 0 0 0 5.91 1.51h.01c6.62 0 11.98-5.36 11.98-11.98 0-3.2-1.25-6.21-3.51-8.47a11.9 11.9 0 0 0-8.48-3.51zm0 21.86h-.01a9.94 9.94 0 0 1-5.06-1.38l-.36-.22-3.63.95.97-3.54-.23-.37a9.93 9.93 0 0 1-1.52-5.32c0-5.48 4.46-9.94 9.95-9.94 2.66 0 5.15 1.04 7.03 2.92a9.87 9.87 0 0 1 2.91 7.02c0 5.49-4.47 9.95-9.95 9.95z"/></svg>
</a>"""


def head(title, description, canonical, extra_css="", lang="fr", alt_path="", robots="index,follow", extra_json_ld=None, og_type="website", og_image=""):
    t = COPY[lang]
    a = pfx(lang)
    can = canonical.lstrip("/")
    if lang == "fr":
        self_url = f"{SITE}/{can}" if can else f"{SITE}/"
        alt_abs = f"{SITE}/{alt_path}" if alt_path else f"{SITE}/en/"
        fr_href, en_href = self_url, alt_abs
    else:
        self_url = f"{SITE}/{can}" if can else f"{SITE}/en/"
        alt_abs = f"{SITE}/{alt_path}" if alt_path else f"{SITE}/"
        fr_href, en_href = alt_abs, self_url
    safe_title = html_lib.escape(title, quote=True)
    safe_desc = html_lib.escape(description, quote=True)
    img_path = og_image or OG_IMAGE
    if img_path.startswith("http"):
        og_abs = img_path
    else:
        og_abs = f"{SITE}/{img_path.lstrip('/')}"
    agency = {
        "@context": "https://schema.org",
        "@type": "EmploymentAgency",
        "name": "Talendus",
        "url": SITE,
        "telephone": "+1-514-555-0199",
        "email": "info@talendus.ca",
        "slogan": t["tagline"],
        "areaServed": "Quebec",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Montreal",
            "addressRegion": "QC",
            "addressCountry": "CA",
        },
        "sameAs": [SITE],
    }
    blocks = [agency]
    if extra_json_ld:
        blocks.extend(extra_json_ld if isinstance(extra_json_ld, list) else [extra_json_ld])
    json_scripts = "".join(
        f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>\n    '
        for block in blocks
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>{safe_title}</title>
     <meta name="description" content="{safe_desc}">
     <link rel="canonical" href="{self_url}">
     <link rel="alternate" hreflang="fr-CA" href="{fr_href}">
     <link rel="alternate" hreflang="en-CA" href="{en_href}">
     <link rel="alternate" hreflang="x-default" href="{fr_href if lang == 'en' else self_url}">
     <meta name="robots" content="{html_lib.escape(robots, quote=True)}">
     <meta property="og:locale" content="{t['og_locale']}">
     <meta property="og:locale:alternate" content="{'en_CA' if lang == 'fr' else 'fr_CA'}">
     <meta property="og:title" content="{safe_title}">
     <meta property="og:description" content="{safe_desc}">
     <meta property="og:type" content="{html_lib.escape(og_type, quote=True)}">
     <meta property="og:url" content="{self_url}">
     <meta property="og:site_name" content="Talendus">
     <meta property="og:image" content="{og_abs}">
     <meta name="twitter:card" content="summary_large_image">
     <meta name="twitter:title" content="{safe_title}">
     <meta name="twitter:description" content="{safe_desc}">
     <meta name="twitter:image" content="{og_abs}">
    <link rel="shortcut icon" href="{a}assets/img/logo/fav-logo1.png" type="image/png">
    <link rel="stylesheet" href="{a}assets/css/plugins/bootstrap.min.css">
    <link rel="stylesheet" href="{a}assets/css/plugins/aos.css">
    <link rel="stylesheet" href="{a}assets/css/plugins/fontawesome.css">
    <link rel="stylesheet" href="{a}assets/css/plugins/magnific-popup.css">
    <link rel="stylesheet" href="{a}assets/css/plugins/slick-slider.css">
    <link rel="stylesheet" href="{a}assets/css/plugins/nice-select.css">
    <link rel="stylesheet" href="{a}assets/css/main.css">
    <link rel="stylesheet" href="{a}assets/css/talendus.css">
    {extra_css}
    {json_scripts}
</head>
"""


def header(solid=True, lang="fr", alt_url=""):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    cls = "tl-solid-header" if solid else ""
    switch = lang_switcher(lang, alt_url)
    return f"""<body class="{cls}">
{preloader(lang, a)}
<header class="homepage2-body">
  <div id="vl-header-sticky" class="vl-header-area vl-transparent-header">
      <div class="container">
          <div class="tl-header-bar">
              <div class="vl-logo">
                  <a href="{h['home']}"><img src="{a}assets/img/logo/logo1.png" alt="Talendus"></a>
              </div>
              <div class="vl-main-menu tl-desktop-nav">
                  <nav class="vl-mobile-menu-active">
                      <ul>
{nav_html(lang)}
                      </ul>
                  </nav>
              </div>
              <div class="tl-header-tools">
                {switch}
                <a href="{h['account']}" class="tl-account-link" data-account-link>{t['nav_account']}</a>
                <div class="hero-btn1">
                  <a href="{h['contact']}" class="vl-btn2 tl-header-cta">{t['cta_primary']} <span><i class="fa-solid fa-arrow-right"></i></span></a>
                </div>
              </div>
              <div class="tl-mobile-tools">
                  {switch}
                  <button type="button" class="vl-offcanvas-toggle" aria-label="{t['menu_open']}" aria-expanded="false" aria-controls="tl-mobile-nav">
                    <i class="fa-solid fa-bars-staggered"></i>
                  </button>
               </div>
          </div>
      </div>
  </div>
</header>
<div class="homepage2-body">
  <div class="vl-offcanvas" id="tl-mobile-nav">
    <div class="vl-offcanvas-wrapper">
        <div class="vl-offcanvas-header d-flex justify-content-between align-items-center">
            <div class="vl-offcanvas-logo">
                <a href="{h['home']}"><img src="{a}assets/img/logo/logo1.png" alt="Talendus"></a>
            </div>
            <div class="vl-offcanvas-close">
               <button type="button" class="vl-offcanvas-close-toggle" aria-label="{t['menu_close']}"><i class="fa-solid fa-xmark"></i></button>
            </div>
        </div>
        <div class="vl-offcanvas-menu"><nav></nav></div>
        <div class="vl-offcanvas-info">
            <h3 class="vl-offcanvas-sm-title">Talendus</h3>
            <p class="tl-offcanvas-tagline">{t['tagline']}</p>
            <div class="space20"></div>
            <span><a href="tel:+15145550199"><i class="fa-solid fa-phone"></i> 514 555-0199</a></span>
            <span><a href="mailto:info@talendus.ca"><i class="fa-regular fa-envelope"></i> info@talendus.ca</a></span>
            <span><a href="{h['contact']}"><i class="fa-solid fa-location-dot"></i> {t['offcanvas_place']}</a></span>
            <span><a href="{wa_link(lang)}" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-whatsapp"></i> WhatsApp</a></span>
            <p class="tl-offcanvas-note">{t['offcanvas_note']}</p>
            <div class="vl-offcanvas-cta">
              <a href="{h['contact']}" class="tl-btn">{t['cta_primary']}</a>
              <a href="{h['cv']}" class="tl-btn tl-btn-electric">{t['cta_secondary']}</a>
            </div>
        </div>
    </div>
  </div>
  <div class="vl-offcanvas-overlay"></div>
</div>
"""


def speed_strip(lang="fr"):
    t, h = COPY[lang], HREFS[lang]
    return f"""
<section class="tl-speed">
  <div class="container">
    <div class="tl-speed-inner">
      <div>
        <span class="tl-badge tl-badge-light">{t['speed_kicker']}</span>
        <h2>{t['speed_h2']}</h2>
        <p>{t['speed_p']}</p>
      </div>
      <div class="tl-speed-actions">
        <a class="tl-btn tl-btn-lg" href="{h['contact']}">{t['cta_primary']}</a>
        <a class="tl-btn tl-btn-ghost" href="{h['contact']}">{t['consult']}</a>
      </div>
    </div>
  </div>
</section>
"""


def cta_band(lang="fr"):
    t, h = COPY[lang], HREFS[lang]
    return f"""
<section class="tl-cta-band">
  <div class="container">
    <span class="tl-badge tl-badge-light">{t['cta_kicker']}</span>
    <h2 class="tl-h2">{t['cta_h2']}</h2>
    <p>{t['cta_p']}</p>
    <div class="tl-actions">
      <a class="tl-btn tl-btn-lg" href="{h['contact']}">{t['cta_primary']}</a>
      <a class="tl-btn tl-btn-ghost" href="{h['cv']}">{t['cta_secondary']}</a>
    </div>
  </div>
</section>
"""


def footer(lang="fr"):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    return f"""
{whatsapp_fab(lang)}
<div class="tl-sticky">
  <a href="{h['contact']}">{t['cta_primary']}</a>
  <a class="alt" href="{h['cv']}">{t['cta_secondary']}</a>
</div>
<div class="vl-footer2-section-area">
  <div class="container">
    <div class="row">
      <div class="col-lg-3 col-md-6">
        <div class="footer-logo-area">
          <img src="{a}assets/img/logo/logo1.png" alt="Talendus">
          <div class="space16"></div>
          <p class="tl-footer-tagline">{t['tagline']}</p>
          <p>{t['footer_blurb']}</p>
          <p class="tl-muted" style="margin-top:12px">{t['footer_rdv']}</p>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area foot-padding1">
          <h3>{t['footer_cabinet']}</h3>
          <ul>
            <li><a href="{h['about']}">{t['nav_about']}</a></li>
            <li><a href="{h['services']}">{t['nav_services_top']}</a></li>
            <li><a href="{h['svc_industrial']}">{t['nav_svc_industrial']}</a></li>
            <li><a href="{h['sectors']}">{t['nav_sectors'].split()[0] if lang == 'fr' else 'Industries'}</a></li>
            <li><a href="{h['blog']}">{t['nav_blog']}</a></li>
            <li><a href="{h['contact']}">{t['nav_contact']}</a></li>
          </ul>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area foot-padding2">
          <h3>{t['footer_recruit']}</h3>
          <ul>
            <li><a href="{h['employers']}">{t['nav_employers']}</a></li>
            <li><a href="{h['candidates']}">{t['nav_candidates']}</a></li>
            <li><a href="{h['jobs']}">{t['nav_jobs']}</a></li>
            <li><a href="{h['svc_perm']}">{t['nav_svc_perm']}</a></li>
            <li><a href="{h['svc_search']}">{'Chasse de têtes' if lang == 'fr' else 'Search mandates'}</a></li>
            <li><a href="{h['svc_lead']}">{t['nav_svc_lead']}</a></li>
          </ul>
        </div>
      </div>
      <div class="col-lg col-md-6">
        <div class="footer-widget-area">
          <h3>{t['footer_contact']}</h3>
          <ul>
            <li><a href="tel:+15145550199">514 555-0199</a></li>
            <li><a href="mailto:info@talendus.ca">info@talendus.ca</a></li>
            <li><a href="{wa_link(lang)}" target="_blank" rel="noopener noreferrer">WhatsApp</a></li>
            <li>{t['footer_hours']}</li>
            <li><a href="{h['contact']}">{t['footer_place']}</a></li>
            <li><a href="{h['geo_mtl']}">{'Montréal' if lang == 'fr' else 'Montreal'}</a></li>
            <li><a href="{h['geo_laval']}">Laval</a></li>
            <li><a href="{h['geo_long']}">Longueuil</a></li>
            <li><a href="{h['geo_qc']}">{'Québec' if lang == 'fr' else 'Quebec'}</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="space48"></div>
    <div class="col-lg-12">
      <div class="copyright-area">
        <a href="{h['home']}">{t['footer_copy']}</a>
        <ul>
          <li><a href="{h['privacy']}">{t['privacy']}</a><span> | </span></li>
          <li><a href="{h['terms']}">{t['terms']}</a><span> | </span></li>
          <li><a href="#" data-consent-open>{'Cookies' if lang == 'fr' else 'Cookies'}</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
<script src="{a}assets/js/plugins/jquery-3-7-1.min.js"></script>
<script src="{a}assets/js/plugins/bootstrap.min.js" defer></script>
<script src="{a}assets/js/plugins/fontawesome.js" defer></script>
<script src="{a}assets/js/plugins/aos.js" defer></script>
<script src="{a}assets/js/plugins/counter.js" defer></script>
<script src="{a}assets/js/plugins/magnific-popup.js" defer></script>
<script src="{a}assets/js/plugins/nice-select.js" defer></script>
<script src="{a}assets/js/plugins/waypoints.js" defer></script>
<script src="{a}assets/js/plugins/slick-slider.js" defer></script>
<script src="{a}assets/js/plugins/circle-progress.js" defer></script>
<script src="{a}assets/js/main.js" defer></script>
<script src="{a}assets/js/api.js" defer></script>
<script src="{a}assets/js/talendus.js" defer></script>
<script src="{a}assets/js/account.js" defer></script>
<script src="{a}assets/js/consent.js" defer></script>
<script src="{a}assets/js/tracking.js" defer></script>
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
     "Non. Nous ne recrutons pas en bureau, en TI, en vente ou en service à la clientèle. Talendus est le partenaire de recrutement des entreprises opérationnelles du Québec : production, maintenance, logistique, supervision et continuité des activités."),
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
     "Oui. Plusieurs mandats sont confidentiels. Nous qualifions votre métier, vos quarts et votre mobilité, puis nous vous présentons lorsqu’un employeur opérationnel correspond."),
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
     "Non. Si le poste n’est pas lié à la production, aux opérations, à la maintenance, à la logistique ou à la supervision industrielle, nous déclinons. C’est ce qui protège la qualité du vivier."),
]

FAQ_CANDIDATS = [
    ("Dois-je payer pour vos services ?",
     "Non. Les honoraires sont assumés par l’employeur. Le dépôt de CV et l’accompagnement jusqu’à l’embauche sont sans frais pour vous."),
    ("Que se passe-t-il après l’envoi de mon CV ?",
     "Nous qualifions votre métier, vos quarts et votre région. S’il y a correspondance, un conseiller vous appelle. Réponse moyenne sous 30 minutes durant les heures d’ouverture lorsque vous nous écrivez ou nous joignez."),
    ("Puis-je postuler s’il n’y a pas d’offre affichée ?",
     "Oui. Plusieurs usines recrutent en mandat confidentiel. Votre profil reste actif dans notre banque de talents."),
    ("Quels métiers placez-vous ?",
     "Journalier, opérateur, cariste, soudeur, machiniste CNC, électromécanicien, mécanicien industriel, superviseur, coordonnateur logistique, directeur d’usine — et les métiers connexes d’atelier, de quai et de maintenance."),
    ("M’enverrez-vous sur des entrevues au hasard ?",
     "Non. Nous présentons votre dossier uniquement aux employeurs dont le quart, le salaire et l’environnement correspondent à ce que vous avez indiqué."),
    ("Travaillez-vous partout au Québec ?",
     "Principalement le Grand Montréal, Laval, la Rive-Sud, la Montérégie, l’Estrie, le Centre-du-Québec et Québec. Dites-nous votre mobilité : nous ciblons en conséquence."),
]

FAQ_HOME_EN = [
    ("Is Talendus a general staffing agency?",
     "No. We do not recruit for office, IT, sales or customer service roles. Talendus is the recruiting partner for Quebec operations: production, maintenance, logistics, supervision and business continuity."),
    ("When do we see the first candidates?",
     "On operations, forklift and many plant roles, qualified candidates arrive from day 7. That is a screened shortlist — not a pile of resumes. A scarce CNC machinist or a plant manager takes longer; we say so at the briefing."),
    ("Which regions of Quebec do you cover?",
     "Greater Montreal, Laval, the South Shore, Montérégie, the Eastern Townships, Centre-du-Québec, Mauricie and the Quebec City area. We also run regional mandates when the profile requires it."),
    ("How does a consultation work?",
     "Consultations are by appointment only. A 30-minute call is enough to cover shift, real pay, health & safety and urgency. Average response under 30 minutes during business hours (Mon–Fri, 8 a.m. to 5 p.m.)."),
    ("Do you offer a replacement guarantee?",
     "Yes, on permanent mandates. The term is confirmed in writing when the file opens. 30/60/90-day follow-up is part of the mandate, not an add-on."),
    ("Do you only work with active job seekers?",
     "No. A large share of our network is passive: operators, trades and supervisors already in post whom we approach discreetly. That is often where the people who stay are found."),
    ("Can I submit a resume if there is no posting?",
     "Yes. Many mandates are confidential. We qualify your trade, shifts and mobility, then introduce you when an operational employer matches."),
    ("How do you bill employers?",
     "Success fees based on the placed candidate’s annual salary. No fee if the mandate does not close, per the agreement. The first consultation is free."),
]

FAQ_EMPLOYERS_EN = [
    ("How long before the first files?",
     "Qualified candidates from day 7 on operations roles and many plant jobs. Supervisors, scarce trades and managers: 3 to 8 weeks, stated at the consultation — no cosmetic promises."),
    ("What happens on the consultation call?",
     "By appointment. We talk shift, skills, health & safety, real pay and what has already failed. You leave with a search plan, not a generic HR speech."),
    ("Do you send a lot of resumes?",
     "No. Your floor supervisor should not lose an hour. We screen, we meet, we present few files — each one defensible."),
    ("Do you work outside Montreal?",
     "Yes. Beyond Greater Montreal we run mandates in Montérégie, the Eastern Townships, Centre-du-Québec, Mauricie and the Quebec City region."),
    ("How are fees calculated?",
     "On success, against the placed candidate’s annual salary. No fee if the mandate does not close, per the agreement. The consultation is free."),
    ("What guarantee do you offer?",
     "Replacement included on permanent mandates. Term confirmed at kickoff. 30/60/90-day onboarding follow-up."),
    ("Can you run a confidential mandate?",
     "Yes. Manager replacement, reorganization or a sensitive seat: a discreet approach, no internal noise, until you choose when to communicate."),
    ("Do you also recruit office staff?",
     "No. If the role is not tied to production, operations, maintenance, logistics or industrial supervision, we decline. That is what protects the quality of the pool."),
]

FAQ_CANDIDATES_EN = [
    ("Do I pay for your services?",
     "No. Fees are paid by the employer. Submitting a resume and support through to hire are free for you."),
    ("What happens after I send my resume?",
     "We qualify your trade, shifts and region. If there is a match, a consultant calls you. Average response under 30 minutes during business hours when you write or call."),
    ("Can I apply if there is no posting?",
     "Yes. Many plants hire on confidential mandates. Your profile stays active in our talent pool."),
    ("Which roles do you place?",
     "Labourer, operator, forklift driver, welder, CNC machinist, electromechanical technician, industrial mechanic, supervisor, logistics coordinator, plant manager — and related shop, dock and maintenance trades."),
    ("Will you send me to random interviews?",
     "No. We present your file only to employers whose shift, pay and environment match what you told us."),
    ("Do you work across Quebec?",
     "Mainly Greater Montreal, Laval, the South Shore, Montérégie, the Eastern Townships, Centre-du-Québec and Quebec City. Tell us your mobility and we target accordingly."),
]

def wrap(title, desc, slug, body, solid=True, lang="fr", alt="", robots="index,follow", extra_json_ld=None, og_type="website", og_image=""):
    if lang == "fr":
        switch = alt or "en/index.html"
    elif not alt or alt in ("", "index.html"):
        switch = "../index.html"
    else:
        switch = "../" + alt.lstrip("/")
    return (
        head(
            title,
            desc,
            slug,
            lang=lang,
            alt_path=alt,
            robots=robots,
            extra_json_ld=extra_json_ld,
            og_type=og_type,
            og_image=og_image,
        )
        + header(solid, lang=lang, alt_url=switch)
        + body
        + footer(lang)
    )


# Back-compat aliases used by older imports
SPEED_STRIP = speed_strip("fr")
CTA_BAND = cta_band("fr")
FOOTER = footer("fr")
HEADER_NAV = nav_html("fr")
PRELOADER = preloader("fr", "")
