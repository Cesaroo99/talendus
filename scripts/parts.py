SITE = "https://talendus.ca"
WA_HREF = "https://wa.me/15145550199?text="
OG_IMAGE = "assets/img/all-images/industry/usine-equipe.jpg"

import html as html_lib
import json
import os

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
        "tagline": "Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.",
        "brand_line": "La plateforme de recrutement intelligente pour toutes les entreprises.",
        "preloader_tag": "Plateforme de recrutement · Tous secteurs",
        "preloader_aria": "Chargement Talendus",
        "nav_home": "Accueil",
        "nav_employers": "Pour les Entreprises",
        "nav_why": "Pourquoi Talendus",
        "nav_services": "Services de recrutement",
        "nav_sectors": "Tous les secteurs",
        "nav_calc": "Calculateur d'embauche",
        "nav_candidates": "Pour les Talents",
        "nav_jobs": "Offres d'emploi",
        "nav_cv": "Déposer mon CV",
        "nav_process": "Comment ça fonctionne",
        "nav_services_top": "Services",
        "nav_about": "À propos",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "Connexion",
        "nav_register": "Inscription",
        "nav_employer_account": "Espace employeur",
        "nav_publish": "Publier une offre",
        "nav_hr": "Solutions RH",
        "nav_talent_faq": "Questions fréquentes",
        "cta_talent_primary": "Trouver un emploi",
        "cta_talent_secondary": "Créer mon profil",
        "cta_talent_profile": "Créer mon profil",
        "cta_talent_apply": "Postuler",
        "cta_talent_jobs": "Découvrir les offres",
        "cta_hire_primary": "Parler à un recruteur",
        "cta_hire_secondary": "Publier une offre",
        "cta_hire_demo": "Parler à un recruteur",
        "cta_hire_find": "Trouver des talents",
        "cta_hire_need": "Décrire mon besoin de recrutement",
        "cta_gateway_talent": "Je cherche un emploi",
        "cta_gateway_hire": "Je recrute",
        "cta_gateway_kicker": "Emploi ou recrutement",
        "cta_gateway_h2": "Dites-nous ce que vous venez faire.",
        "cta_gateway_p": "Cherchez-vous un emploi, ou avez-vous un poste à pourvoir ? Choisissez. On vous amène à la bonne page.",
        "speed_kicker_talent": "Sans frais pour vous",
        "speed_h2_talent": "On vous présente aux entreprises qui recrutent vraiment.",
        "speed_p_talent": "On regarde votre métier, vos compétences et où vous pouvez travailler. Ensuite on vous présente seulement aux employeurs qui collent.",
        "nav_svc_industrial": "Recrutement industriel",
        "nav_svc_mfg": "Recrutement manufacturier",
        "nav_svc_tech": "Recrutement technique",
        "nav_svc_perm": "Recrutement permanent",
        "nav_svc_temp": "Recrutement temporaire",
        "nav_svc_search": "Chasse de têtes",
        "nav_svc_lead": "Recrutement de cadres",
        "footer_places": "Régions",
        "cta_primary": "Parler à un recruteur",
        "cta_secondary": "Créer mon profil",
        "menu_open": "Ouvrir le menu",
        "menu_close": "Fermer le menu",
        "offcanvas_note": "En semaine, on répond en général en moins de 30 minutes.",
        "offcanvas_place": "Montréal, Québec · sur rendez-vous",
        "consult": "Réserver un appel",
        "footer_blurb": "Plateforme de recrutement pour les entreprises de tous secteurs. Trouvez des talents, publiez une offre, ou confiez-nous votre recrutement.",
        "footer_rdv": "Les appels se font sur rendez-vous.",
        "footer_cabinet": "Cabinet",
        "footer_recruit": "Recrutement",
        "footer_contact": "Contact",
        "footer_hours": "Lun–Ven, 8 h à 17 h",
        "footer_place": "Montréal · sur rendez-vous",
        "footer_copy": "© 2026 Talendus. Tous droits réservés. talendus.ca",
        "privacy": "Confidentialité",
        "terms": "Conditions",
        "sticky_consult": "Réserver un appel",
        "wa_label": "Écrire à Talendus sur WhatsApp",
        "speed_kicker": "Délai",
        "speed_h2": "Moins de temps perdu. De meilleurs recrutements.",
        "speed_p": "Pas une pile de CV. On ouvre le mandat, on filtre, on vous envoie des dossiers que vous pouvez recevoir — quel que soit votre secteur.",
        "cta_kicker": "Recrutement",
        "cta_h2": "Vous avez un besoin de recrutement ? Parlez-nous de votre poste.",
        "cta_p": "Quel que soit votre secteur, un conseiller Talendus peut prendre le mandat. Appel de 30 minutes, gratuit, sur rendez-vous.",
        "cta_talent_kicker": "Emploi",
        "cta_talent_h2": "Prêt à trouver un emploi ?",
        "cta_talent_p": "C'est gratuit. Créez votre profil, parcourez les offres. Un conseiller présente votre dossier aux employeurs.",
        "keywords": "plateforme de recrutement, recrutement entreprises, recrutement tous secteurs, trouver des talents, publier une offre d'emploi, recrutement Québec, Talendus",
    },
    "en": {
        "html_lang": "en-CA",
        "og_locale": "en_CA",
        "tagline": "We hire better, faster and more intelligently with AI.",
        "brand_line": "The intelligent recruiting platform for every company.",
        "preloader_tag": "Recruiting platform · Every industry",
        "preloader_aria": "Loading Talendus",
        "nav_home": "Home",
        "nav_employers": "For employers",
        "nav_why": "Why Talendus",
        "nav_services": "Recruiting services",
        "nav_sectors": "Every industry",
        "nav_calc": "Hiring calculator",
        "nav_candidates": "For talent",
        "nav_jobs": "Job openings",
        "nav_cv": "Submit my resume",
        "nav_process": "How it works",
        "nav_services_top": "Services",
        "nav_about": "About",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "Sign in",
        "nav_register": "Sign up",
        "nav_employer_account": "Employer portal",
        "nav_publish": "Post a job",
        "nav_hr": "HR solutions",
        "nav_talent_faq": "Common questions",
        "cta_talent_primary": "Find a job",
        "cta_talent_secondary": "Create my profile",
        "cta_talent_profile": "Create my profile",
        "cta_talent_apply": "Apply",
        "cta_talent_jobs": "Browse jobs",
        "cta_hire_primary": "Talk to a recruiter",
        "cta_hire_secondary": "Post a job",
        "cta_hire_demo": "Talk to a recruiter",
        "cta_hire_find": "Find talent",
        "cta_hire_need": "Describe my hiring need",
        "cta_gateway_talent": "I'm looking for a job",
        "cta_gateway_hire": "I'm hiring",
        "cta_gateway_kicker": "Job search or hiring",
        "cta_gateway_h2": "Tell us what you came to do.",
        "cta_gateway_p": "Looking for a job, or filling a role? Pick a side. We'll take you to the right page.",
        "speed_kicker_talent": "Free for you",
        "speed_h2_talent": "We introduce you to companies that are actually hiring.",
        "speed_p_talent": "We look at your role, your skills and where you can work. Then we introduce you only to employers that fit.",
        "nav_svc_industrial": "Industrial recruiting",
        "nav_svc_mfg": "Manufacturing recruiting",
        "nav_svc_tech": "Technical recruiting",
        "nav_svc_perm": "Permanent recruiting",
        "nav_svc_temp": "Temporary recruiting",
        "nav_svc_search": "Executive search",
        "nav_svc_lead": "Leadership recruiting",
        "footer_places": "Regions",
        "cta_primary": "Talk to a recruiter",
        "cta_secondary": "Create my profile",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "offcanvas_note": "On weekdays we usually reply within 30 minutes.",
        "offcanvas_place": "Montreal, Quebec · by appointment",
        "consult": "Book a call",
        "footer_blurb": "A recruiting platform for companies in every industry. Find talent, post a job, or hand the search to Talendus.",
        "footer_rdv": "Calls are by appointment.",
        "footer_cabinet": "Firm",
        "footer_recruit": "Recruiting",
        "footer_contact": "Contact",
        "footer_hours": "Mon–Fri, 8 a.m. to 5 p.m.",
        "footer_place": "Montreal · by appointment",
        "footer_copy": "© 2026 Talendus. All rights reserved. talendus.ca",
        "privacy": "Privacy",
        "terms": "Terms",
        "sticky_consult": "Book a call",
        "wa_label": "Message Talendus on WhatsApp",
        "speed_kicker": "Timeline",
        "speed_h2": "Less time wasted. Better hires.",
        "speed_p": "Not a stack of resumes. We open the mandate, screen, and send files you can actually meet — whatever your industry.",
        "cta_kicker": "Hiring",
        "cta_h2": "Have a hiring need? Tell us about the role.",
        "cta_p": "Whatever your industry, a Talendus consultant can take the mandate. A 30-minute call, free, by appointment.",
        "cta_talent_kicker": "Jobs",
        "cta_talent_h2": "Ready to find a job?",
        "cta_talent_p": "It's free. Create your profile, browse openings. A consultant presents your file to employers.",
        "keywords": "recruiting platform, hiring for companies, multi-industry recruiting, find talent, post a job, recruitment Quebec, Talendus",
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
        "process_page": "comment-ca-fonctionne.html",
        "publish": "publier-une-offre.html",
        "hr": "solutions-rh.html",
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
        "process_page": "how-it-works.html",
        "publish": "post-a-job.html",
        "hr": "hr-solutions.html",
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


def infer_persona(slug: str) -> str:
    raw = (slug or "").strip().lower()
    name = raw.split("/")[-1]
    if not name or name in {"index.html", "en"}:
        return "gateway"
    talent = name in {
        "candidats.html",
        "candidates.html",
        "emplois.html",
        "jobs.html",
        "comment-ca-fonctionne.html",
        "how-it-works.html",
        "espace.html",
        "account.html",
    } or name.startswith("emploi-") or name.startswith("job-")
    hire = name in {
        "entreprises.html",
        "employers.html",
        "employeurs.html",
        "services.html",
        "service.html",
        "secteurs.html",
        "sectors.html",
        "publier-une-offre.html",
        "post-a-job.html",
        "solutions-rh.html",
        "hr-solutions.html",
        "espace-employeur.html",
        "account-employer.html",
        "chasse-de-tetes.html",
        "executive-search.html",
    } or name.startswith("secteur-") or name.startswith("sector-") or name.startswith("recrutement-") or "recruiting" in name
    if talent:
        return "talent"
    if hire:
        return "entreprise"
    return "gateway"


def nav_html(lang):
    t, h = COPY[lang], HREFS[lang]
    return f"""
                              <li data-nav="home"><a href="{h['home']}">{t['nav_home']}</a></li>
                              <li class="has-dropdown" data-nav="candidats">
                                <a href="{h['candidates']}" data-set-persona="talent">{t['nav_candidates']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['jobs']}" data-set-persona="talent">{t['nav_jobs']}</a></li>
                                      <li><a href="{h['cv']}" data-set-persona="talent">{t['nav_cv']}</a></li>
                                      <li><a href="{h['process_page']}" data-set-persona="talent">{t['nav_process']}</a></li>
                                      <li><a href="{h['candidates']}#faq" data-set-persona="talent">{t['nav_talent_faq']}</a></li>
                                  </ul>
                              </li>
                              <li class="has-dropdown" data-nav="employeurs">
                                <a href="{h['employers']}" data-set-persona="entreprise">{t['nav_employers']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['employers']}" data-set-persona="entreprise">{t['nav_why']}</a></li>
                                      <li><a href="{h['publish']}" data-set-persona="entreprise">{t['nav_publish']}</a></li>
                                      <li><a href="{h['svc_search']}" data-set-persona="entreprise">{t['nav_svc_search']}</a></li>
                                      <li><a href="{h['hr']}" data-set-persona="entreprise">{t['nav_hr']}</a></li>
                                      <li><a href="{h['services']}" data-set-persona="entreprise">{t['nav_services']}</a></li>
                                      <li><a href="{h['sectors']}" data-set-persona="entreprise">{t['nav_sectors']}</a></li>
                                  </ul>
                              </li>
                              <li data-nav="jobs"><a href="{h['jobs']}" data-set-persona="talent">{t['nav_jobs']}</a></li>
                              <li data-nav="about"><a href="{h['about']}">{t['nav_about']}</a></li>
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
        "logo": f"{SITE}/assets/img/logo/logo1.png",
        "image": f"{SITE}/{OG_IMAGE}",
        "sameAs": [SITE],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Talendus",
        "url": SITE,
        "inLanguage": ["fr-CA", "en-CA"],
        "publisher": {"@type": "Organization", "name": "Talendus", "url": SITE},
    }
    blocks = [agency, website]
    if extra_json_ld:
        blocks.extend(extra_json_ld if isinstance(extra_json_ld, list) else [extra_json_ld])
    json_scripts = "".join(
        f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>\n    '
        for block in blocks
    )
    gsc = (os.environ.get("GOOGLE_SITE_VERIFICATION") or "").strip()
    gsc_meta = (
        f'<meta name="google-site-verification" content="{html_lib.escape(gsc, quote=True)}">\n     '
        if gsc
        else ""
    )
    consent_default = """<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500
});
</script>"""
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>{safe_title}</title>
     <meta name="description" content="{safe_desc}">
     <meta name="keywords" content="{html_lib.escape(t['keywords'], quote=True)}">
     {gsc_meta}<link rel="canonical" href="{self_url}">
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
     <meta name="theme-color" content="#0b1f3a">
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
    {consent_default}
    {json_scripts}
</head>
"""


def header(solid=True, lang="fr", alt_url="", persona="gateway"):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    classes = []
    if solid:
        classes.append("tl-solid-header")
    classes.append(f"tl-persona-{persona}")
    cls = " ".join(classes)
    switch = lang_switcher(lang, alt_url)
    return f"""<body class="{cls}" data-persona="{persona}">
{preloader(lang, a)}
<header class="homepage2-body">
  <div id="vl-header-sticky" class="vl-header-area vl-transparent-header">
      <div class="container">
          <div class="tl-header-bar">
              <div class="vl-logo">
                  <a href="{h['home']}"><img src="{a}assets/img/logo/logo1.png" width="372" height="72" alt="Talendus"></a>
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
                <a href="{h['account']}" class="tl-account-link" data-account-link data-auth-open="login">{t['nav_account']}</a>
                <a href="{h['account']}" class="tl-account-link tl-register-link" data-auth-open="register">{t['nav_register']}</a>
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
                <a href="{h['home']}"><img src="{a}assets/img/logo/logo1.png" width="372" height="72" alt="Talendus"></a>
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
              <a href="{h['account']}" class="tl-btn tl-btn-ghost" data-account-link data-auth-open="login">{t['nav_account']}</a>
              <a href="{h['account']}" class="tl-btn" data-auth-open="register">{t['nav_register']}</a>
            </div>
        </div>
    </div>
  </div>
  <div class="vl-offcanvas-overlay"></div>
</div>
"""


def proof_stats(lang="fr"):
    if lang == "en":
        kicker, heading = "In practice", "What that looks like"
        items = (
            ("7 d", "Target to put the first files in front of you, on a typical operations role."),
            ("92 %", "Still in the job three months later, on our permanent placements."),
            ("100 %", "One consultant on your file, from the first call through start date."),
        )
    else:
        kicker, heading = "Concrètement", "Ce que ça donne"
        items = (
            ("7 j", "Délai visé pour vous présenter les premiers dossiers, sur un mandat d'opérations typique."),
            ("92 %", "Des gens encore en poste trois mois après l'embauche, sur nos placements permanents."),
            ("100 %", "Un seul conseiller sur votre dossier, du premier appel jusqu'à l'entrée en poste."),
        )
    cards = "".join(f'<div class="tl-stat"><b>{n}</b><p>{p}</p></div>' for n, p in items)
    return f"""
<section class="tl-section-sm">
  <div class="container">
    <div class="tl-center" style="max-width:640px;margin:0 auto 28px">
      <div class="tl-kicker">{kicker}</div>
      <h2 class="tl-h2">{heading}</h2>
    </div>
    <div class="tl-stats tl-stats-compact">{cards}</div>
  </div>
</section>
"""


def speed_strip(lang="fr", persona="entreprise"):
    t = COPY[lang]
    if persona == "talent":
        kicker, heading, copy = t["speed_kicker_talent"], t["speed_h2_talent"], t["speed_p_talent"]
    else:
        kicker, heading, copy = t["speed_kicker"], t["speed_h2"], t["speed_p"]
    return f"""
<section class="tl-speed">
  <div class="container">
    <div class="tl-speed-inner">
      <div>
        <span class="tl-badge tl-badge-light">{kicker}</span>
        <h2>{heading}</h2>
        <p>{copy}</p>
      </div>
    </div>
  </div>
</section>
"""


def cta_band(lang="fr", persona="gateway"):
    t, h = COPY[lang], HREFS[lang]
    if persona == "talent":
        kicker, heading, copy = t["cta_talent_kicker"], t["cta_talent_h2"], t["cta_talent_p"]
        action = f'<a class="tl-btn tl-btn-lg" href="{h["cv"]}">{t["cta_talent_secondary"]}</a>'
    elif persona == "entreprise":
        kicker, heading, copy = t["cta_kicker"], t["cta_h2"], t["cta_p"]
        action = f'<a class="tl-btn tl-btn-lg" href="{h["contact"]}">{t["cta_hire_primary"]}</a>'
    else:
        return ""
    return f"""
<section class="tl-cta-band">
  <div class="container">
    <span class="tl-badge tl-badge-light">{kicker}</span>
    <h2 class="tl-h2">{heading}</h2>
    <p>{copy}</p>
    <div class="tl-actions">
      {action}
    </div>
  </div>
</section>
"""


def footer(lang="fr"):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    return f"""
{whatsapp_fab(lang)}
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
            <li><a href="{h['sectors']}">{t['nav_sectors']}</a></li>
            <li><a href="{h['svc_industrial']}">{t['nav_svc_industrial']}</a></li>
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
<script src="{a}assets/js/persona.js" defer></script>
<script src="{a}assets/js/auth-gate.js" defer></script>
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
    ("Talendus est-il limité à certains secteurs ?",
     "Non. Talendus est une plateforme de recrutement pour toutes les entreprises. Construction, santé, finance, technologie, manufacturier, commerce : ce sont des exemples, pas des limites. Quel que soit votre secteur, on vous aide à trouver les bons talents."),
    ("L'intelligence artificielle est-elle déjà disponible ?",
     "Pas encore. L'IA est la direction de la plateforme — matching, analyse de CV, classement des candidats — mais ces outils ne sont pas actifs. Rien n'est simulé. En attendant, un conseiller Talendus mène le recrutement."),
    ("À partir de quand recevons-nous les premiers candidats ?",
     "Sur un mandat d'opérations typique, on vise les premiers dossiers en 7 jours. Ce n'est pas une pile de CV : c'est une shortlist déjà filtrée. Un profil rare ou un poste de direction prend plus de temps. On le dit dès le brief."),
    ("Dans quelles régions recrutez-vous ?",
     "Grand Montréal, Laval, Rive-Sud, Montérégie, Estrie, Centre-du-Québec, Mauricie et région de Québec. On mène aussi des mandats ailleurs au Québec, et à distance, quand le profil l'exige."),
    ("Comment se passe un premier appel ?",
     "Sur rendez-vous. Trente minutes suffisent pour parler du poste, du secteur, du nombre de personnes à recruter, de la localisation et de l'urgence. En semaine, on répond en général en moins de 30 minutes (lun.–ven., 8 h à 17 h)."),
    ("Offrez-vous une garantie de remplacement ?",
     "Oui, sur les mandats permanents. La durée est écrite à l'ouverture du dossier. Le suivi 30/60/90 jours fait partie du mandat, pas d'une option."),
    ("Puis-je simplement parler à un recruteur ?",
     "Oui. Publier une offre n'est pas obligatoire. Décrivez votre besoin — secteur, poste, volume, localisation, type de contrat — et un conseiller Talendus s'en occupe."),
    ("Comment facturez-vous les employeurs ?",
     "Honoraires au succès, calculés sur le salaire annuel de la personne placée. Pas de frais si le mandat n'aboutit pas, selon l'entente. Le premier appel est gratuit."),
]

FAQ_EMPLOYEURS = [
    ("Combien de temps avant les premiers dossiers ?",
     "Sur un métier d'opérations, on vise 7 jours. Profils rares et cadres : 3 à 8 semaines. On l'annonce dès l'appel, sans promesse en l'air."),
    ("Que se passe-t-il pendant l'appel ?",
     "Sur rendez-vous. On parle du poste, du secteur, des compétences, du salaire réel et de ce qui a déjà échoué. Vous repartez avec un plan de recherche, pas un discours RH générique."),
    ("Présentez-vous beaucoup de CV ?",
     "Non. L'idée, c'est que vous ne perdiez pas une heure. On filtre, on rencontre, on présente peu de dossiers — chacun qu'on est prêt à défendre."),
    ("Recrutez-vous seulement dans l'industrie ?",
     "Non. L'industrie, la santé, la finance, la technologie, le commerce et les autres secteurs sont des paramètres de recherche. Talendus s'adresse à toutes les entreprises."),
    ("Comment sont calculés les honoraires ?",
     "Au succès, sur le salaire annuel de la personne placée. Pas de frais si le mandat n'aboutit pas, selon l'entente. L'appel de départ est gratuit."),
    ("Quelle garantie offrez-vous ?",
     "Remplacement inclus sur les mandats permanents. Durée confirmée à l'ouverture. Suivi d'intégration 30/60/90 jours."),
    ("Pouvez-vous mener un mandat confidentiel ?",
     "Oui. Remplacement de cadre, réorganisation ou poste sensible : on approche sans bruit interne, jusqu'à ce que vous choisissiez le moment de communiquer."),
    ("L'IA classe-t-elle déjà les candidats ?",
     "Pas encore. Matching intelligent, analyse de CV et classement : bientôt disponibles. Aujourd'hui, un conseiller Talendus filtre les dossiers."),
]

FAQ_CANDIDATS = [
    ("Dois-je payer pour vos services ?",
     "Non. Les honoraires sont payés par l'employeur. Créer votre profil et vous accompagner jusqu'à l'embauche, c'est gratuit pour vous."),
    ("Que se passe-t-il après l'envoi de mon CV ?",
     "On regarde votre métier, vos compétences et votre région. S'il y a une correspondance, un conseiller vous appelle. En semaine, on répond en général en moins de 30 minutes quand vous nous écrivez ou nous joignez."),
    ("Puis-je postuler s'il n'y a pas d'offre affichée ?",
     "Oui. Plusieurs entreprises recrutent sans afficher. Votre profil reste actif ; on vous contacte quand un mandat colle."),
    ("Quels métiers placez-vous ?",
     "Développeur, comptable, ingénieur, chauffeur, cariste, soudeur, technicien, infirmier, vendeur, responsable RH, gestionnaire, marketing, administration, production, logistique — et bien d'autres. Ce sont des exemples, pas une liste fermée."),
    ("M'enverrez-vous sur des entrevues au hasard ?",
     "Non. On présente votre dossier seulement aux employeurs dont le poste, le salaire et l'environnement correspondent à ce que vous avez dit."),
    ("Travaillez-vous partout au Québec ?",
     "Surtout le Grand Montréal, Laval, la Rive-Sud, la Montérégie, l'Estrie, le Centre-du-Québec et Québec. Dites-nous jusqu'où vous pouvez vous déplacer — ou si vous visez le télétravail : on cible en conséquence."),
]

FAQ_HOME_EN = [
    ("Is Talendus limited to certain industries?",
     "No. Talendus is a recruiting platform for every company. Construction, healthcare, finance, technology, manufacturing, retail: those are examples, not limits. Whatever your industry, we help you find the right talent."),
    ("Is artificial intelligence already available?",
     "Not yet. AI is the product direction — matching, resume analysis, candidate ranking — but those tools are not live. Nothing is simulated. Until then, a Talendus consultant runs the search."),
    ("When do we see the first candidates?",
     "On a typical operations mandate, we aim for the first files in 7 days. That's a screened shortlist, not a pile of resumes. A scarce profile or a leadership seat takes longer. We say so at the briefing."),
    ("Which regions do you cover?",
     "Greater Montreal, Laval, the South Shore, Montérégie, the Eastern Townships, Centre-du-Québec, Mauricie and the Quebec City area. We also run mandates elsewhere in Quebec, and remote roles, when the profile requires it."),
    ("How does the first call work?",
     "By appointment. Thirty minutes is enough to cover the role, industry, headcount, location and urgency. On weekdays we usually reply within 30 minutes (Mon–Fri, 8 a.m. to 5 p.m.)."),
    ("Do you offer a replacement guarantee?",
     "Yes, on permanent mandates. The term is written down when the file opens. 30/60/90-day follow-up is part of the mandate, not an add-on."),
    ("Can I just talk to a recruiter?",
     "Yes. Posting a job is not required. Describe the need — industry, role, headcount, location, contract type — and a Talendus consultant takes it from there."),
    ("How do you bill employers?",
     "Success fees based on the placed person's annual salary. No fee if the mandate doesn't close, per the agreement. The first call is free."),
]

FAQ_EMPLOYERS_EN = [
    ("How long before the first files?",
     "On an operations role, we aim for 7 days. Scarce profiles and managers: 3 to 8 weeks. We say so on the first call — no inflated promises."),
    ("What happens on the call?",
     "By appointment. We talk about the role, industry, skills, real pay and what has already failed. You leave with a search plan, not a generic HR speech."),
    ("Do you send a lot of resumes?",
     "No. You shouldn't lose an hour. We screen, we meet, we present a few files — each one we're ready to stand behind."),
    ("Do you only recruit in industry?",
     "No. Industry, healthcare, finance, technology, retail and other sectors are search parameters. Talendus is for every company."),
    ("How are fees calculated?",
     "On success, against the placed person's annual salary. No fee if the mandate doesn't close, per the agreement. The first call is free."),
    ("What guarantee do you offer?",
     "Replacement included on permanent mandates. Term confirmed at kickoff. 30/60/90-day onboarding follow-up."),
    ("Can you run a confidential mandate?",
     "Yes. Manager replacement, reorganization or a sensitive seat: we approach without internal noise, until you choose when to communicate."),
    ("Does AI already rank candidates?",
     "Not yet. Intelligent matching, resume analysis and ranking: coming soon. Today, a Talendus consultant screens the files."),
]

FAQ_CANDIDATES_EN = [
    ("Do I pay for your services?",
     "No. Fees are paid by the employer. Creating your profile and support through to hire are free for you."),
    ("What happens after I send my resume?",
     "We look at your role, skills and region. If there's a match, a consultant calls you. On weekdays we usually reply within 30 minutes when you write or call."),
    ("Can I apply if there is no posting?",
     "Yes. Plenty of companies hire without posting. Your profile stays active; we contact you when a mandate fits."),
    ("Which roles do you place?",
     "Developer, accountant, engineer, driver, forklift operator, welder, technician, nurse, sales associate, HR manager, manager, marketing, administration, production, logistics — and many others. Those are examples, not a closed list."),
    ("Will you send me to random interviews?",
     "No. We present your file only to employers whose role, pay and environment match what you told us."),
    ("Do you work across Quebec?",
     "Mainly Greater Montreal, Laval, the South Shore, Montérégie, the Eastern Townships, Centre-du-Québec and Quebec City. Tell us how far you can travel — or if you want remote work — and we target accordingly."),
]

def wrap(title, desc, slug, body, solid=True, lang="fr", alt="", robots="index,follow", extra_json_ld=None, og_type="website", og_image="", persona=None):
    if lang == "fr":
        switch = alt or "en/index.html"
    elif not alt or alt in ("", "index.html"):
        switch = "../index.html"
    else:
        switch = "../" + alt.lstrip("/")
    persona = persona or infer_persona(slug)
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
        + header(solid, lang=lang, alt_url=switch, persona=persona)
        + body
        + footer(lang)
    )


# Back-compat aliases used by older imports
SPEED_STRIP = speed_strip("fr")
CTA_BAND = cta_band("fr")
FOOTER = footer("fr")
HEADER_NAV = nav_html("fr")
PRELOADER = preloader("fr", "")
