SITE = "https://talendus.ca"
PUBLIC_EMAIL = "info@talendus.ca"
PHONE_E164 = "12635585225"
PHONE_TEL = "tel:+12635585225"
PHONE_DISPLAY = "263 558 5225"
WA_HREF = f"https://wa.me/{PHONE_E164}?text="
HONEYPOT_INPUT = '<input class="tl-hp" name="website_url" tabindex="-1" autocomplete="off" aria-hidden="true">'
OG_IMAGE = "assets/img/all-images/industry/usine-equipe.jpg"

import html as html_lib
import json
import os

def pfx(lang):
    return "../" if lang == "en" else ""


def wa_link(lang, persona="gateway"):
    if lang == "en":
        if persona == "talent":
            msg = "Hello%20Talendus%2C%20I%20am%20looking%20for%20work."
        elif persona == "entreprise":
            msg = "Hello%20Talendus%2C%20I%20would%20like%20to%20talk%20about%20a%20hiring%20need."
        else:
            msg = "Hello%20Talendus%2C%20I%20would%20like%20to%20talk."
    else:
        if persona == "talent":
            msg = "Bonjour%20Talendus%2C%20je%20cherche%20un%20emploi."
        elif persona == "entreprise":
            msg = "Bonjour%20Talendus%2C%20je%20souhaite%20discuter%20d%27un%20besoin%20de%20recrutement."
        else:
            msg = "Bonjour%20Talendus%2C%20j%27aimerais%20vous%20parler."
    return WA_HREF + msg


COPY = {
    "fr": {
        "html_lang": "fr-CA",
        "og_locale": "fr_CA",
        "tagline": "Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.",
        "brand_line": "Agence de placement intelligente pour toutes les entreprises.",
        "preloader_tag": "Agence de placement · Tous secteurs",
        "preloader_aria": "Chargement Talendus",
        "nav_home": "Accueil",
        "nav_employers": "Entreprises",
        "nav_why": "Recruter avec Talendus",
        "nav_services": "Services de recrutement",
        "nav_sectors": "Tous les secteurs",
        "nav_calc": "Calculateur d'embauche",
        "nav_candidates": "Talents",
        "nav_jobs": "Emplois",
        "nav_jobs_list": "Offres d'emploi",
        "nav_cv": "Déposer mon CV",
        "nav_process": "Comment ça fonctionne",
        "nav_services_top": "Services",
        "nav_about": "À propos",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "Connexion",
        "nav_register": "Créer un compte",
        "nav_workspace": "Mon espace",
        "nav_sign_out": "Déconnexion",
        "nav_notifs": "Notifications",
        "nav_settings": "Paramètres",
        "role_talent": "Candidat",
        "role_hire": "Entreprise",
        "nav_employer_account": "Espace employeur",
        "nav_publish": "Soumettre un besoin",
        "nav_hr": "Solutions RH",
        "nav_talent_faq": "Questions fréquentes",
        "cta_talent_primary": "Trouver un emploi",
        "cta_talent_secondary": "Créer mon profil",
        "cta_talent_profile": "Créer mon profil",
        "cta_talent_apply": "Postuler",
        "cta_talent_jobs": "Découvrir les offres",
        "cta_hire_primary": "Réserver une consultation gratuite",
        "cta_hire_secondary": "Décrire le poste",
        "cta_hire_demo": "Réserver une consultation",
        "cta_hire_find": "Réserver une consultation gratuite",
        "cta_hire_need": "Décrire le poste",
        "cta_gateway_talent": "Je cherche un emploi",
        "cta_gateway_hire": "Je recrute",
        "cta_gateway_kicker": "Recrutement ou emploi",
        "cta_gateway_h2": "Dites-nous ce que vous venez faire.",
        "cta_gateway_p": "Avez-vous un poste à pourvoir, ou cherchez-vous un emploi ? Les entreprises parlent d'abord à un chasseur. Talendus est l'intermédiaire.",
        "speed_kicker_talent": "Sans frais pour vous",
        "speed_h2_talent": "Talendus étudie votre profil et vous présente aux entreprises quand ça colle.",
        "speed_p_talent": "Vous créez votre profil. Nous comprenons votre parcours. Lorsqu'une opportunité correspond, un conseiller vous rappelle. Appelez-nous ou écrivez-nous dès que vous voulez avancer.",
        "nav_svc_industrial": "Recrutement industriel",
        "nav_svc_mfg": "Recrutement manufacturier",
        "nav_svc_tech": "Recrutement technique",
        "nav_svc_perm": "Recrutement permanent",
        "nav_svc_temp": "Recrutement temporaire",
        "nav_svc_search": "Chasse de têtes",
        "nav_svc_lead": "Recrutement de cadres",
        "footer_places": "Régions",
        "cta_primary": "Confier mon recrutement",
        "cta_secondary": "Créer mon profil",
        "menu_open": "Ouvrir le menu",
        "menu_close": "Fermer le menu",
        "offcanvas_note": "En semaine, on répond en général en moins de 30 minutes.",
        "offcanvas_place": "Montréal, Québec · sur rendez-vous",
        "consult": "Réserver une consultation gratuite",
        "footer_blurb": "Agence de placement intelligente : vous confiez un besoin, Talendus recherche, présélectionne et présente les profils les plus pertinents. Tous secteurs.",
        "footer_rdv": "Les appels se font sur rendez-vous.",
        "footer_cabinet": "Agence",
        "footer_recruit": "Recrutement",
        "footer_contact": "Contact",
        "footer_hours": "Lun–Ven, 8 h à 17 h",
        "footer_place": "Montréal · sur rendez-vous",
        "footer_copy": "© 2026 Talendus. Tous droits réservés. talendus.ca",
        "privacy": "Confidentialité",
        "terms": "Conditions",
        "sticky_consult": "Consultation gratuite",
        "wa_label": "Écrire à Talendus sur WhatsApp",
        "call_label": "Appeler Talendus",
        "app_install": "Installer l'appli",
        "speed_kicker": "Le mandat",
        "speed_h2": "Nous faisons le travail de recherche. Vous gardez le choix final.",
        "speed_p": "Pas une pile de CV à trier. Vous décrivez le poste ; Talendus recherche, présélectionne et vous présente une shortlist qualifiée, quel que soit votre secteur.",
        "cta_kicker": "Recrutement",
        "cta_h2": "Un poste à combler ? Confiez-nous le brief.",
        "cta_p": "Un conseiller prend la recherche. Vous rencontrez des gens qui valent votre temps. Honoraires à l'embauche. Appel de 20 minutes, gratuit.",
        "cta_talent_kicker": "Emploi",
        "cta_talent_h2": "Prêt à rejoindre Talendus ?",
        "cta_talent_p": "C'est gratuit. Créez votre profil, déposez votre CV. Lorsque votre parcours correspond à une opportunité, un conseiller vous contacte.",
        "keywords": "agence de recrutement, agence de placement, recrutement externalisé, recherche de talents, présélection de candidats, recrutement intelligent, recrutement assisté par IA, placement de personnel, solution de recrutement, recrutement de talents, Talendus Québec",
    },
    "en": {
        "html_lang": "en-CA",
        "og_locale": "en_CA",
        "tagline": "We hire better, faster and more intelligently with AI.",
        "brand_line": "An intelligent placement agency for every company.",
        "preloader_tag": "Placement agency · Every industry",
        "preloader_aria": "Loading Talendus",
        "nav_home": "Home",
        "nav_employers": "For employers",
        "nav_why": "Hire with Talendus",
        "nav_services": "Recruiting services",
        "nav_sectors": "Every industry",
        "nav_calc": "Hiring calculator",
        "nav_candidates": "For talent",
        "nav_jobs": "Job openings",
        "nav_jobs_list": "Job openings",
        "nav_cv": "Submit my resume",
        "nav_process": "How it works",
        "nav_services_top": "Services",
        "nav_about": "About",
        "nav_blog": "Blog",
        "nav_contact": "Contact",
        "nav_account": "Sign in",
        "nav_register": "Create account",
        "nav_workspace": "My workspace",
        "nav_sign_out": "Sign out",
        "nav_notifs": "Notifications",
        "nav_settings": "Settings",
        "role_talent": "Candidate",
        "role_hire": "Employer",
        "nav_employer_account": "Employer portal",
        "nav_publish": "Submit a hiring need",
        "nav_hr": "HR solutions",
        "nav_talent_faq": "Common questions",
        "cta_talent_primary": "Find a job",
        "cta_talent_secondary": "Create my profile",
        "cta_talent_profile": "Create my profile",
        "cta_talent_apply": "Apply",
        "cta_talent_jobs": "Browse jobs",
        "cta_hire_primary": "Book a free consultation",
        "cta_hire_secondary": "Describe the role",
        "cta_hire_demo": "Book a consultation",
        "cta_hire_find": "Book a free consultation",
        "cta_hire_need": "Describe the role",
        "cta_gateway_talent": "I'm looking for a job",
        "cta_gateway_hire": "I'm hiring",
        "cta_gateway_kicker": "Hiring or job search",
        "cta_gateway_h2": "Tell us what you came to do.",
        "cta_gateway_p": "Filling a seat, or looking for a job? Employers talk to a headhunter first. Talendus is the intermediary.",
        "speed_kicker_talent": "Free for you",
        "speed_h2_talent": "Talendus studies your profile and introduces you when it actually fits.",
        "speed_p_talent": "You create your profile. We understand your path. When an opportunity fits, a consultant calls you. Call or write whenever you want to move forward.",
        "nav_svc_industrial": "Industrial recruiting",
        "nav_svc_mfg": "Manufacturing recruiting",
        "nav_svc_tech": "Technical recruiting",
        "nav_svc_perm": "Permanent recruiting",
        "nav_svc_temp": "Temporary recruiting",
        "nav_svc_search": "Executive search",
        "nav_svc_lead": "Leadership recruiting",
        "footer_places": "Regions",
        "cta_primary": "Hand us the search",
        "cta_secondary": "Create my profile",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "offcanvas_note": "On weekdays we usually reply within 30 minutes.",
        "offcanvas_place": "Montreal, Quebec · by appointment",
        "consult": "Book a free consultation",
        "footer_blurb": "An intelligent placement agency: you hand us a hiring need, Talendus searches, screens and presents the most relevant profiles. Every industry.",
        "footer_rdv": "Calls are by appointment.",
        "footer_cabinet": "Agency",
        "footer_recruit": "Recruiting",
        "footer_contact": "Contact",
        "footer_hours": "Mon–Fri, 8 a.m. to 5 p.m.",
        "footer_place": "Montreal · by appointment",
        "footer_copy": "© 2026 Talendus. All rights reserved. talendus.ca",
        "privacy": "Privacy",
        "terms": "Terms",
        "sticky_consult": "Free consultation",
        "wa_label": "Message Talendus on WhatsApp",
        "call_label": "Call Talendus",
        "app_install": "Install the app",
        "speed_kicker": "The mandate",
        "speed_h2": "We do the search. You keep the final choice.",
        "speed_p": "Not a stack of resumes to sort. You describe the role; Talendus searches, screens and presents a qualified shortlist, whatever your industry.",
        "cta_kicker": "Hiring",
        "cta_h2": "A seat to fill? Hand us the brief.",
        "cta_p": "A consultant takes the search. You meet people worth your time. Fees when someone starts. A 20-minute call, free.",
        "cta_talent_kicker": "Jobs",
        "cta_talent_h2": "Ready to join Talendus?",
        "cta_talent_p": "It's free. Create your profile, submit your resume. When your path matches an opportunity, a consultant contacts you.",
        "keywords": "recruitment agency, staffing agency, outsourced recruiting, talent search, candidate screening, intelligent recruiting, AI-assisted recruiting, personnel placement, recruiting solution, talent recruiting, Talendus Quebec",
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
        "publish": "besoin-de-recrutement.html",
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
        "app": "app.html",
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
        "publish": "hiring-need.html",
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
        "app": "app.html",
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
        "besoin-de-recrutement.html",
        "hiring-need.html",
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
                              <li class="has-dropdown" data-nav="candidats">
                                <a href="{h['candidates']}" data-set-persona="talent">{t['nav_candidates']} <span class="tl-nav-caret" aria-hidden="true"><i class="fa-solid fa-angle-down"></i></span></a>
                                  <ul class="sub-menu">
                                      <li><a href="{h['jobs']}" data-set-persona="talent">{t['nav_jobs_list']}</a></li>
                                      <li><a href="{h['cv']}" data-set-persona="talent">{t['nav_cv']}</a></li>
                                      <li><a href="{h['process_page']}" data-set-persona="talent">{t['nav_process']}</a></li>
                                      <li><a href="{h['candidates']}#faq" data-set-persona="talent">{t['nav_talent_faq']}</a></li>
                                  </ul>
                              </li>
                              <li data-nav="jobs"><a href="{h['jobs']}" data-set-persona="talent">{t['nav_jobs']}</a></li>
                              <li data-nav="about"><a href="{h['about']}">{t['nav_about']}</a></li>
                              <li data-nav="contact"><a href="{h['contact']}">{t['nav_contact']}</a></li>
"""


def lang_switcher(lang, alt_url, current="."):
    self_href = current or "."
    if lang == "fr":
        fr_href, en_href, fr_cls, en_cls = self_href, alt_url or "en/index.html", "is-active", ""
    else:
        fr_href, en_href, fr_cls, en_cls = alt_url or "../index.html", self_href, "", "is-active"
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


def whatsapp_fab(lang, persona="gateway"):
    t = COPY[lang]
    return f"""<a class="tl-whatsapp" href="{wa_link(lang, persona)}" target="_blank" rel="noopener noreferrer" aria-label="{t['wa_label']}">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M19.11 17.47c-.29-.15-1.73-.85-2-.95-.27-.1-.46-.15-.66.15s-.76.95-.93 1.15c-.17.2-.34.22-.63.07-.29-.15-1.22-.45-2.33-1.43-.86-.77-1.44-1.72-1.61-2.01-.17-.29-.02-.45.13-.6.13-.13.29-.34.43-.51.15-.17.2-.29.29-.48.1-.2.05-.36-.02-.51-.07-.15-.66-1.59-.9-2.18-.24-.57-.48-.49-.66-.5h-.56c-.2 0-.51.07-.78.36-.27.29-1.02.99-1.02 2.42s1.05 2.81 1.19 3 .07.15 2.06 3.15c1.64 1.41 2.96 1.85 3.58 2.06.54.17 1.04.15 1.43.09.44-.06 1.73-.71 1.97-1.39.24-.68.24-1.27.17-1.39-.07-.12-.26-.2-.55-.35zM16.03 4.05C9.41 4.05 4.05 9.4 4.05 16.03c0 2.11.55 4.17 1.6 5.99L4 28l6.12-1.6a11.94 11.94 0 0 0 5.91 1.51h.01c6.62 0 11.98-5.36 11.98-11.98 0-3.2-1.25-6.21-3.51-8.47a11.9 11.9 0 0 0-8.48-3.51zm0 21.86h-.01a9.94 9.94 0 0 1-5.06-1.38l-.36-.22-3.63.95.97-3.54-.23-.37a9.93 9.93 0 0 1-1.52-5.32c0-5.48 4.46-9.94 9.95-9.94 2.66 0 5.15 1.04 7.03 2.92a9.87 9.87 0 0 1 2.91 7.02c0 5.49-4.47 9.95-9.95 9.95z"/></svg>
</a>"""


def call_fab(lang):
    t = COPY[lang]
    return f"""<a class="tl-call" href="{PHONE_TEL}" aria-label="{t['call_label']}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.7 3.9 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1.1-.3 1.2.4 2.5.6 3.8.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.6.6 3.8.1.4 0 .8-.3 1.1L6.6 10.8z"/></svg>
</a>"""


def place_card(lang="fr"):
    """Bloc lieu sans iframe : la CSP bloque maps.google.com et Chrome affiche une page cassée."""
    maps = "https://www.google.com/maps/search/?api=1&query=Montreal%20Quebec"
    if lang == "en":
        return f"""<aside class="tl-place">
            <p class="tl-kicker">Reach Talendus</p>
            <h3>Montreal · Quebec</h3>
            <p>We work across Quebec. Calls are by appointment.</p>
            <ul class="tl-place-links">
              <li><a href="{PHONE_TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i> {PHONE_DISPLAY}</a></li>
              <li><a href="mailto:info@talendus.ca"><i class="fa-solid fa-envelope" aria-hidden="true"></i> info@talendus.ca</a></li>
            </ul>
            <a class="tl-btn tl-btn-ghost" href="{maps}" target="_blank" rel="noopener noreferrer">Open in Maps</a>
          </aside>"""
    return f"""<aside class="tl-place">
            <p class="tl-kicker">Nous joindre</p>
            <h3>Montréal · Québec</h3>
            <p>Talendus intervient partout au Québec. Les appels se font sur rendez-vous.</p>
            <ul class="tl-place-links">
              <li><a href="{PHONE_TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i> {PHONE_DISPLAY}</a></li>
              <li><a href="mailto:info@talendus.ca"><i class="fa-solid fa-envelope" aria-hidden="true"></i> info@talendus.ca</a></li>
            </ul>
            <a class="tl-btn tl-btn-ghost" href="{maps}" target="_blank" rel="noopener noreferrer">Ouvrir dans Maps</a>
          </aside>"""


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
        "telephone": "+1-263-558-5225",
        "email": PUBLIC_EMAIL,
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
    app_shell_redirect = ""
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
     {app_shell_redirect}
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
     <meta name="apple-mobile-web-app-capable" content="yes">
     <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
     <meta name="apple-mobile-web-app-title" content="Talendus">
     <meta name="mobile-web-app-capable" content="yes">
    <link rel="manifest" href="{a}manifest.webmanifest">
    <link rel="apple-touch-icon" sizes="180x180" href="{a}assets/img/logo/apple-touch-icon.png">
    <link rel="icon" sizes="192x192" href="{a}assets/img/logo/icon-192.png" type="image/png">
    <link rel="shortcut icon" href="{a}assets/img/logo/icon-192.png" type="image/png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap" rel="stylesheet">
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


def header(solid=True, lang="fr", alt_url="", persona="gateway", current="."):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    classes = []
    if solid:
        classes.append("tl-solid-header")
    classes.append(f"tl-persona-{persona}")
    cls = " ".join(classes)
    switch = lang_switcher(lang, alt_url, current)
    acc = h["employer_account"] if persona == "entreprise" else h["account"]
    role_attr = ' data-auth-role="EMPLOYER"' if persona == "entreprise" else ""
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
                <div class="tl-session" data-session="desktop">
                  <a href="{acc}" class="tl-session-login" data-auth-open="login"{role_attr}>
                    <i class="fa-regular fa-user" aria-hidden="true"></i>
                    <span>{t['nav_account']}</span>
                  </a>
                  <a href="{acc}" class="tl-btn tl-session-cta" data-auth-open="register"{role_attr}>{t['nav_register']}</a>
                </div>
              </div>
              <div class="tl-mobile-tools">
                  {switch}
                  <div class="tl-session tl-session-compact" data-session="mobile">
                    <a href="{acc}" class="tl-session-icon-btn" data-auth-open="login"{role_attr} aria-label="{t['nav_account']}">
                      <i class="fa-regular fa-user" aria-hidden="true"></i>
                    </a>
                  </div>
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
            <div class="tl-offcanvas-tools">
                {switch}
                <div class="vl-offcanvas-close">
                   <button type="button" class="vl-offcanvas-close-toggle" aria-label="{t['menu_close']}"><i class="fa-solid fa-xmark"></i></button>
                </div>
            </div>
        </div>
        <div class="vl-offcanvas-menu"><nav></nav></div>
        <div class="vl-offcanvas-info">
            <h3 class="vl-offcanvas-sm-title">Talendus</h3>
            <p class="tl-offcanvas-tagline">{t['tagline']}</p>
            <div class="space20"></div>
            <span><a href="{PHONE_TEL}"><i class="fa-solid fa-phone"></i> {PHONE_DISPLAY}</a></span>
            <span><a href="mailto:info@talendus.ca"><i class="fa-regular fa-envelope"></i> info@talendus.ca</a></span>
            <span><a href="{h['contact']}"><i class="fa-solid fa-location-dot"></i> {t['offcanvas_place']}</a></span>
            <span><a href="{wa_link(lang, persona)}" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-whatsapp"></i> WhatsApp</a></span>
            <p class="tl-offcanvas-note">{t['offcanvas_note']}</p>
            <div class="vl-offcanvas-cta tl-session tl-session-offcanvas" data-session="offcanvas">
              <a href="{acc}" class="tl-btn tl-btn-ghost" data-auth-open="login"{role_attr}>{t['nav_account']}</a>
              <a href="{acc}" class="tl-btn" data-auth-open="register"{role_attr}>{t['nav_register']}</a>
            </div>
        </div>
    </div>
  </div>
  <div class="vl-offcanvas-overlay"></div>
</div>
"""


def proof_stats(lang="fr"):
    if lang == "en":
        kicker, heading = "The firm", "What the mandate looks like"
        items = (
            ("7 d", "Target to put the first files in front of you, on a typical operations role."),
            ("92 %", "Still in the job three months later, on our permanent placements."),
            ("100 %", "One consultant on your file, from the first call through start date."),
        )
    else:
        kicker, heading = "Le cabinet", "Le mandat, en chiffres"
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


def footer(lang="fr", persona="gateway"):
    t, h, a = COPY[lang], HREFS[lang], pfx(lang)
    city_mtl = "Montréal" if lang == "fr" else "Montreal"
    city_qc = "Québec" if lang == "fr" else "Quebec"
    search_label = "Chasse de têtes" if lang == "fr" else "Search mandates"
    return f"""
{call_fab(lang)}
{whatsapp_fab(lang, persona)}
<footer class="vl-footer2-section-area tl-site-footer" role="contentinfo">
  <div class="container">
    <div class="tl-footer-grid">
      <div class="tl-footer-brand footer-logo-area">
        <img src="{a}assets/img/logo/logo1.png" alt="Talendus">
        <p class="tl-footer-tagline">{t['tagline']}</p>
        <p class="tl-footer-blurb">{t['footer_blurb']}</p>
        <p class="tl-footer-rdv">{t['footer_rdv']}</p>
      </div>
      <nav class="footer-widget-area tl-footer-col" aria-label="{t['footer_cabinet']}">
        <h3>{t['footer_cabinet']}</h3>
        <ul>
          <li><a href="{h['about']}">{t['nav_about']}</a></li>
          <li><a href="{h['services']}">{t['nav_services_top']}</a></li>
          <li><a href="{h['sectors']}">{t['nav_sectors']}</a></li>
          <li><a href="{h['svc_industrial']}">{t['nav_svc_industrial']}</a></li>
          <li><a href="{h['blog']}">{t['nav_blog']}</a></li>
          <li><a href="{h['contact']}">{t['nav_contact']}</a></li>
        </ul>
      </nav>
      <nav class="footer-widget-area tl-footer-col" aria-label="{t['footer_recruit']}">
        <h3>{t['footer_recruit']}</h3>
        <ul>
          <li><a href="{h['employers']}">{t['nav_employers']}</a></li>
          <li><a href="{h['candidates']}">{t['nav_candidates']}</a></li>
          <li><a href="{h['jobs']}">{t['nav_jobs']}</a></li>
          <li><a href="{h['svc_perm']}">{t['nav_svc_perm']}</a></li>
          <li><a href="{h['svc_search']}">{search_label}</a></li>
          <li><a href="{h['svc_lead']}">{t['nav_svc_lead']}</a></li>
        </ul>
      </nav>
      <div class="footer-widget-area tl-footer-col tl-footer-contact">
        <h3>{t['footer_contact']}</h3>
        <ul class="tl-footer-coords">
          <li><a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:info@talendus.ca">info@talendus.ca</a></li>
          <li><a href="{wa_link(lang, persona)}" target="_blank" rel="noopener noreferrer">WhatsApp</a></li>
          <li>{t['footer_hours']}</li>
          <li><a href="{h['contact']}">{t['footer_place']}</a></li>
        </ul>
        <ul class="tl-footer-cities">
          <li><a href="{h['geo_mtl']}">{city_mtl}</a></li>
          <li><a href="{h['geo_laval']}">Laval</a></li>
          <li><a href="{h['geo_long']}">Longueuil</a></li>
          <li><a href="{h['geo_qc']}">{city_qc}</a></li>
        </ul>
      </div>
    </div>
    <div class="copyright-area tl-footer-legal">
      <a href="{h['home']}">{t['footer_copy']}</a>
      <ul>
        <li><a href="{h['privacy']}">{t['privacy']}</a></li>
        <li><a href="{h['terms']}">{t['terms']}</a></li>
        <li><a href="#" data-consent-open>Cookies</a></li>
      </ul>
    </div>
  </div>
</footer>
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
    ("Comment fonctionne Talendus ?",
     "Talendus est une agence de placement. L'entreprise confie un besoin de recrutement. Nous recherchons, analysons, présélectionnons et qualifions les profils, puis nous présentons une shortlist. L'entreprise étudie ces dossiers et prend la décision finale. Côté candidat, vous créez un profil : nous vous contactons lorsque votre parcours correspond à une opportunité. Un conseiller reste votre contact à chaque étape : appelez-nous, écrivez-nous ou ouvrez votre espace."),
    ("Talendus est-il limité à certains secteurs ?",
     "Non. Talendus recrute pour tous les secteurs et tous les types de métiers. Technologie, santé, finance, construction, commerce, industrie, services : ce sont des exemples, pas des limites. PME, startups ou plus grandes organisations : l'accompagnement s'adapte au besoin, pas à une spécialisation unique."),
    ("Utilisez-vous réellement l'intelligence artificielle ?",
     "Oui. Talendus utilise déjà des outils intégrant l'intelligence artificielle dans ses processus internes de recrutement. Ces technologies permettent notamment d'accélérer l'analyse des profils, la recherche de correspondances et certaines tâches de présélection. Elles viennent renforcer le travail des équipes Talendus sans remplacer leur expertise humaine."),
    ("Dois-je utiliser un outil d'intelligence artificielle pour recruter avec Talendus ?",
     "Non. Vous n'avez pas besoin d'utiliser vous-même un outil d'IA. Talendus utilise ses propres outils technologiques et ses solutions d'intelligence artificielle en interne pour effectuer le travail de recherche, d'analyse et de présélection des talents pour votre compte."),
    ("L'IA choisit-elle le candidat à ma place ?",
     "Non. L'intelligence artificielle aide Talendus à analyser et à identifier les profils potentiellement pertinents, mais la qualification et l'évaluation humaine restent essentielles. Talendus vous présente ensuite une sélection de candidats correspondant au besoin défini. La décision finale appartient toujours à l'entreprise."),
    ("Quels avantages l'IA apporte-t-elle à mon recrutement ?",
     "Elle permet notamment à Talendus de traiter plus rapidement de grandes quantités d'informations, d'identifier des correspondances pertinentes entre les profils et les postes et d'accélérer certaines étapes de recherche et de présélection. Vous bénéficiez ainsi d'un processus plus efficace sans avoir à gérer vous-même ces outils."),
    ("À partir de quand recevons-nous les premiers candidats ?",
     "Sur un mandat d'opérations typique, nous visons les premiers dossiers en 7 jours. Ce n'est pas une pile de CV : c'est une shortlist déjà filtrée. Un profil rare ou un poste de direction prend plus de temps. Nous le disons dès le brief."),
    ("Comment facturez-vous les employeurs ?",
     "Honoraires au succès, calculés sur le salaire annuel de la personne placée. Pas de frais si le mandat n'aboutit pas, selon l'entente. Le premier appel est gratuit, sur rendez-vous."),
]

FAQ_EMPLOYEURS = [
    ("C'est quoi une agence de recrutement, et pourquoi mon entreprise en aurait besoin ?",
     "Une agence de recrutement prend la recherche, l'approche et la sélection à votre place. Contrairement à un affichage, on n'attend pas que les gens postulent : on les contacte, même s'ils sont déjà en poste. C'est ça, la chasse de têtes. Pour une entreprise qui n'a pas une semaine à passer dans les CV ou les entrevues vides, c'est du temps rendu aux opérations."),
    ("Est-ce qu'un cabinet de recrutement convient aux PME québécoises ?",
     "Encore plus qu'aux grandes organisations. Une grande entreprise a souvent une équipe RH dédiée. Une PME confie le dossier au proprio ou au directeur d'ops, qui a déjà mieux à faire. Chaque heure à éplucher des candidatures est une heure de moins sur le plancher. Le cabinet vous donne un processus complet, sans bâtir cette expertise à l'interne."),
    ("Combien coûte un chasseur de têtes ?",
     "Les honoraires se calculent sur le salaire annuel de la personne embauchée. Ils ne sont dus qu'à l'entrée en poste : sans résultat, vous ne payez pas, selon l'entente. Le pourcentage et la fenêtre de remplacement sont écrits à l'ouverture du mandat. La consultation de départ est gratuite."),
    ("La chasse de têtes, c'est seulement pour les postes de direction ?",
     "Non. Elle s'applique à tous les niveaux. Un mauvais directeur coûte cher. Un mauvais employé sur le plancher aussi. Un poste vacant qui traîne coûte chaque jour. On chasse un électromécanicien ou un superviseur de quart comme on chasse un cadre."),
    ("On paie seulement si on engage : comment ça marche ?",
     "On prend l'analyse du besoin, la prospection, les premières entrevues et la présélection. Vous ne rencontrez que les profils qui valent votre temps. Jusque-là, rien à débourser. Le montant est dû le premier jour de travail. Si ça ne tient pas dans la fenêtre écrite, on relance la recherche sans frais de plus."),
    ("Comment réserver une consultation gratuite ?",
     "Par le formulaire Contact, le brief écrit, ou un appel au 263 558 5225. Vingt minutes suffisent souvent. On dit si on peut prendre le poste et quel délai viser. Aucun frais pour cet échange."),
    ("À partir de quand recevons-nous les premiers candidats ?",
     "Sur un métier d'opérations typique, on vise les premiers dossiers qualifiés en une semaine. Un cadre rare ou un métier très serré : souvent trois à huit semaines. On l'annonce à la consultation, pas en cours de route."),
    ("Quelle garantie après l'entrée en poste ?",
     "Remplacement inclus sur les permanents, pour la durée écrite au départ. Suivi 30/60/90 jours. Si la personne part ou n'est pas maintenue dans la fenêtre, on reprend le processus complet."),
    ("Qui décide de l'embauche ?",
     "Vous. On présente une shortlist déjà passée par notre sélection. Vous rencontrez. Vous retenez. On ne choisit pas à votre place."),
    ("Le mandat peut rester confidentiel ?",
     "Oui. Remplacement, réorganisation, poste sensible : on approche sans bruit interne jusqu'à ce que vous choisissiez le moment de communiquer. Une offre publique n'est jamais obligatoire."),
]

FAQ_CANDIDATS = [
    ("Comment créer mon profil ?",
     "Inscrivez-vous, indiquez votre métier, vos compétences, votre région et vos préférences, puis déposez votre CV. Cinq minutes suffisent pour entrer dans le réseau Talendus. Un conseiller peut ensuite étudier votre dossier lorsque une opportunité correspond."),
    ("Dois-je déposer mon CV ?",
     "Oui, c'est le moyen le plus clair pour que nous comprenions votre parcours. Sans CV, nous pouvons tout de même ouvrir un profil, mais l'analyse et une éventuelle présentation à une entreprise seront plus limitées."),
    ("Comment Talendus utilise-t-il mon profil ?",
     "Pour comprendre votre parcours et vous considérer pour des mandats pertinents. Nous ne vendons pas vos données. Un conseiller étudie votre dossier, vous rappelle quand un mandat colle, et avance avec vous. Contactez-nous dès que vous voulez qu'on s'en occupe."),
    ("Puis-je être contacté pour une opportunité ?",
     "Oui. Même sans offre affichée, votre profil reste actif. Lorsque votre parcours correspond à un besoin, Talendus peut vous joindre, échanger, puis éventuellement vous présenter. Vous n'êtes pas obligé d'accepter."),
    ("Est-ce que Talendus me présente directement aux entreprises ?",
     "Pas sans étape. Nous étudions d'abord le fit. Souvent, un échange avec nous précède toute présentation. Vous n'êtes pas envoyé à l'aveugle chez quinze employeurs. Quand nous présentons, l'entreprise voit un dossier déjà travaillé par un conseiller qui vous a parlé."),
    ("Comment se déroule une présélection ?",
     "Nous comparons votre parcours aux critères du poste : compétences, expérience, localisation, motivations. Nous pouvons vous poser des questions ou vous rencontrer. Si ça ne colle pas, nous ne forçons pas une entrevue inutile. Si ça colle, nous préparons la présentation."),
    ("Puis-je postuler aux offres disponibles ?",
     "Oui. Les offres publiées sur Talendus sont des mandats que nous accompagnons. Postuler envoie votre dossier à notre équipe. Un conseiller vous rappelle, fait le pont et suit la suite avec vous."),
    ("Comment suivre mon parcours ?",
     "Dans votre espace candidat : profil, CV, candidatures, messages avec Talendus, entretiens planifiés. Votre conseiller vous tient au courant. Écrivez-nous dès que vous avez une question. C'est gratuit pour vous ; les honoraires sont payés par l'employeur."),
    ("Dois-je payer pour vos services ?",
     "Non. Créer un profil, déposer un CV, postuler et être accompagné jusqu'à une éventuelle embauche est gratuit pour les talents."),
    ("M'enverrez-vous sur des entrevues au hasard ?",
     "Non. Nous présentons votre dossier seulement lorsque le poste, les conditions et l'environnement correspondent à ce que vous avez indiqué, et après les étapes de présélection prévues."),
]

FAQ_HOME_EN = [
    ("How does Talendus work?",
     "Talendus is a placement agency. A company hands us a hiring need. We search, analyse, screen and qualify profiles, then present a shortlist. The company reviews those files and makes the final decision. As a candidate, you create a profile: we contact you when your path matches an opportunity. A consultant stays your contact at every step: call us, write to us, or open your space."),
    ("Is Talendus limited to certain industries?",
     "No. Talendus hires across every industry and every kind of role. Technology, healthcare, finance, construction, retail, manufacturing, services: those are examples, not limits. SMEs, startups or larger organizations: support follows the need, not a single specialty."),
    ("Do you actually use artificial intelligence?",
     "Yes. Talendus already uses tools that integrate artificial intelligence in its internal recruiting processes. These technologies help speed up profile analysis, correspondence search and some screening tasks. They strengthen Talendus teams without replacing their human expertise."),
    ("Do I have to use an AI tool to hire with Talendus?",
     "No. You do not need to use an AI tool yourself. Talendus uses its own technological tools and AI solutions internally to search, analyse and screen talent on your behalf."),
    ("Does AI choose the candidate for me?",
     "No. Artificial intelligence helps Talendus analyse and identify potentially relevant profiles, but human qualification and evaluation remain essential. Talendus then presents a selection of candidates matching the defined need. The final decision always belongs to the company."),
    ("What advantages does AI bring to my hiring?",
     "It lets Talendus process large amounts of information faster, identify relevant correspondences between profiles and roles, and accelerate certain search and screening steps. You get a more effective process without having to manage those tools yourself."),
    ("When do we see the first candidates?",
     "On a typical operations mandate, we aim for the first files in 7 days. That is a screened shortlist, not a pile of resumes. A scarce profile or a leadership seat takes longer. We say so at the briefing."),
    ("How do you bill employers?",
     "Success fees based on the placed person's annual salary. No fee if the mandate does not close, per the agreement. The first call is free, by appointment."),
]

FAQ_EMPLOYERS_EN = [
    ("What is a recruiting agency, and why would my company need one?",
     "A recruiting agency takes search, outreach and selection off your desk. Unlike a job ad, we do not wait for people to apply: we contact them, even if they already have a job. That is headhunting. For a company that cannot spend a week in resumes or empty interviews, it is time given back to operations."),
    ("Does a recruiting firm fit Quebec SMEs?",
     "Even more than large organizations. A large company often has a dedicated HR team. An SME hands the file to the owner or the ops lead, who already has better things to do. Every hour spent sorting applications is an hour off the floor. The firm gives you a full process without building that expertise in-house."),
    ("How much does a headhunter cost?",
     "Fees are calculated on the hired person's annual salary. They are due only on the start date: no result, no fee, per the agreement. The percentage and the replacement window are written when the mandate opens. The first consultation is free."),
    ("Is headhunting only for senior leadership?",
     "No. It applies at every level. A bad director is costly. So is a bad employee on the floor. A vacant seat that lingers costs money every day. We hunt an electromechanical tech or a shift supervisor the same way we hunt a manager."),
    ("You only pay if you hire: how does that work?",
     "We take needs analysis, prospecting, first interviews and screening. You only meet profiles worth your time. Until then, you pay nothing. The amount is due on the employee's first day. If it does not hold in the written window, we reopen the search at no extra fee."),
    ("How do I book a free consultation?",
     "Through the Contact form, the written brief, or a call to 263 558 5225. Twenty minutes is usually enough. We say if we can take the seat and which delay to aim for. No fee for that conversation."),
    ("When do we see the first candidates?",
     "On a typical operations role we aim for the first qualified files within a week. A scarce manager or a tight trade: often three to eight weeks. We say so at the consultation, not midway."),
    ("What guarantee after start date?",
     "Replacement included on permanent seats, for the window written at kickoff. 30/60/90 follow-up. If the person leaves or is not kept, we restart the full process."),
    ("Who decides the hire?",
     "You. We present a shortlist that already passed our selection. You meet. You retain. We do not choose in your place."),
    ("Can the mandate stay confidential?",
     "Yes. Replacement, reorganization, sensitive seat: we approach without internal noise until you choose when to communicate. A public posting is never required."),
    ("Which roles do you cover?",
     "Floor and office: production, warehouse, maintenance, construction, admin, site leadership, and others. The list on the site is illustrative. Describe the seat, we open the search."),
    ("Do I have to log into an AI tool?",
     "No. You operate nothing. Internal tools help our team sort faster. A consultant qualifies. You receive files, not software."),
]

def homepage_faq(lang="fr"):
    """FAQ d'accueil : questions partagées à l'entrée, puis chaque persona de son côté."""
    if lang == "en":
        gateway = [
            FAQ_HOME_EN[0],
            ("I'm hiring, what should I do?",
             "Book a free consultation. Hand us the need: role, criteria, terms. A headhunter takes the search, the first interview and the shortlist. You keep the hire. Fees when they start."),
            ("I'm looking for a job, what should I do?",
             "Create a profile and submit your resume. Talendus studies your path and contacts you when an opportunity fits. It is free. Call us or write — a consultant takes it from there."),
            FAQ_HOME_EN[1],
        ]
        talent = FAQ_CANDIDATES_EN[:6]
        hire = [FAQ_EMPLOYERS_EN[i] for i in (0, 1, 2, 4, 5)]
        titles = ("What people ask first", "Questions from talent", "Questions from employers")
    else:
        gateway = [
            FAQ_HOME[0],
            ("Je recrute : que dois-je faire ?",
             "Réservez une consultation gratuite. Confiez-nous le besoin : poste, critères, conditions. Un chasseur reprend la recherche, la première entrevue et la shortlist. Vous gardez l'embauche. Honoraires à l'entrée en poste."),
            ("Je cherche un emploi : que dois-je faire ?",
             "Créez un profil et déposez votre CV. Talendus étudie votre parcours et vous contacte lorsqu'une opportunité correspond. C'est gratuit. Appelez-nous ou écrivez-nous : un conseiller s'en occupe."),
            FAQ_HOME[1],
        ]
        talent = FAQ_CANDIDATS[:6]
        hire = [FAQ_EMPLOYEURS[i] for i in (0, 1, 2, 4, 5)]
        titles = ("Ce qu'on nous demande d'abord", "Questions des candidats", "Questions des entreprises")

    def block(persona, title, items):
        return f"""
    <section class="tl-section tl-ice" data-persona-only="{persona}">
      <div class="container">
        <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
          <div class="tl-kicker">FAQ</div>
          <h2 class="tl-h2">{title}</h2>
        </div>
        {faq_html(items)}
      </div>
    </section>
"""

    return (
        '<div id="faq">'
        + block("gateway", titles[0], gateway)
        + block("talent", titles[1], talent)
        + block("entreprise", titles[2], hire)
        + "</div>"
    )


FAQ_CANDIDATES_EN = [
    ("How do I create my profile?",
     "Sign up, tell us your role, skills, region and preferences, then submit your resume. Five minutes is enough to enter the Talendus network. A consultant can then study your file when an opportunity fits."),
    ("Do I have to submit my resume?",
     "Yes, it is the clearest way for us to understand your path. Without a resume we can still open a profile, but analysis and a possible introduction to a company will be more limited."),
    ("How does Talendus use my profile?",
     "To understand your career and consider you for relevant mandates. We do not sell your data. A consultant studies your file, calls you when a mandate fits, and moves forward with you. Contact us whenever you want us on it."),
    ("Can I be contacted about an opportunity?",
     "Yes. Even without a posted job, your profile stays active. When your path matches a need, Talendus can reach you, talk, then possibly introduce you. You are not obliged to accept."),
    ("Does Talendus introduce me directly to companies?",
     "Not without a step first. We study the fit. Often a conversation with us precedes any introduction. You are not sent blindly to fifteen employers. When we present, the company sees a file already worked by a consultant who has spoken with you."),
    ("How does screening work?",
     "We compare your path to the role: skills, experience, location, motivations. We may ask questions or meet you. If it does not fit, we do not force a useless interview. If it holds, we prepare the introduction."),
    ("Can I apply to posted jobs?",
     "Yes. Openings published on Talendus are mandates we support. Applying sends your file to our team. A consultant calls you, bridges the process and follows up with you."),
    ("How do I follow my path?",
     "In your candidate workspace: profile, resume, applications, messages with Talendus, scheduled interviews. Your consultant keeps you posted. Write to us as soon as you have a question. It is free for you; fees are paid by the employer."),
    ("Do I pay for your services?",
     "No. Creating a profile, submitting a resume, applying and being supported through to a possible hire is free for talent."),
    ("Will you send me to random interviews?",
     "No. We present your file only when the role, terms and environment match what you told us, and after the screening steps planned for that mandate."),
]

CV_FILE_ACCEPT = ".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg"


def cv_file_field(lang="fr", required=True):
    req = " required" if required else ""
    if lang == "en":
        hint = "PDF, Word (DOC, DOCX) or image (PNG, JPG). 5 MB max. The file reaches Talendus. A consultant calls you back."
        label = "Your resume" + (" *" if required else "")
        optional = "" if required else ' <span class="tl-optional">(optional)</span>'
        return f"""<label class="tl-file">
              <span>{label}{optional}</span>
              <input type="file" name="cvfile" accept="{CV_FILE_ACCEPT}"{req}>
              <span class="tl-file-hint">{hint}</span>
            </label>"""
    hint = "PDF, Word (DOC, DOCX) ou image (PNG, JPG). 5 Mo max. Le fichier arrive chez Talendus. Un conseiller vous rappelle."
    label = "Votre CV" + (" *" if required else "")
    optional = "" if required else ' <span class="tl-optional">(facultatif)</span>'
    return f"""<label class="tl-file">
              <span>{label}{optional}</span>
              <input type="file" name="cvfile" accept="{CV_FILE_ACCEPT}"{req}>
              <span class="tl-file-hint">{hint}</span>
            </label>"""


def install_board(lang="fr"):
    """Boutons d'installation réelle : APK Android et profil iPhone."""
    a = pfx(lang)
    apk = "/download/talendus.apk"
    ios = "/download/talendus.mobileconfig"
    if lang == "en":
        already = "Talendus is already installed. Tap the icon on your home screen to open it."
        title = "Get Talendus on your phone"
        lead = "Download once. Offers, messages and your consultant stay one tap away — like your other apps."
        safari = "On iPhone, installation works best in Safari (the blue compass icon)."
        add = "Download the app"
        android_btn = "Download for Android"
        ios_btn = "Download for iPhone"
        android_h = "On Android"
        ios_h = "On iPhone"
        a1_t, a1_p = "Tap Download for Android", "Your phone downloads the Talendus file."
        a2_t, a2_p = "Tap the file once", "It sits at the bottom of the screen, or in Downloads."
        a3_t, a3_p = "Tap Install", "If asked, allow Chrome to install apps. The Talendus icon appears."
        i1_t, i1_p = "Tap Download for iPhone", "Safari downloads the Talendus profile."
        i2_t, i2_p = "Allow the profile", "Then open Settings. At the top, tap Profile Downloaded."
        i3_t, i3_p = "Tap Install", "Enter your code if asked. The Talendus icon appears on the home screen."
        after = "After that, open Talendus from the icon, like any other app."
    else:
        already = "Talendus est déjà installé. Touchez l'icône sur l'écran d'accueil pour l'ouvrir."
        title = "Mettez Talendus sur votre téléphone"
        lead = "Téléchargez une fois. Offres, messages et votre conseiller, en un tap — comme vos autres applis."
        safari = "Sur iPhone, l'installation fonctionne le mieux avec Safari (l'icône boussole bleue)."
        add = "Télécharger l'appli"
        android_btn = "Télécharger pour Android"
        ios_btn = "Télécharger pour iPhone"
        android_h = "Sur Android"
        ios_h = "Sur iPhone"
        a1_t, a1_p = "Touchez Télécharger pour Android", "Le téléphone récupère le fichier Talendus."
        a2_t, a2_p = "Touchez le fichier une fois", "Il est en bas de l'écran, ou dans Téléchargements."
        a3_t, a3_p = "Touchez Installer", "Si le téléphone le demande, autorisez Chrome à installer des applis. L'icône Talendus apparaît."
        i1_t, i1_p = "Touchez Télécharger pour iPhone", "Safari télécharge le profil Talendus."
        i2_t, i2_p = "Autorisez le profil", "Puis ouvrez Réglages. En haut, touchez Profil téléchargé."
        i3_t, i3_p = "Touchez Installer", "Entrez votre code si on vous le demande. L'icône Talendus apparaît sur l'écran d'accueil."
        after = "Ensuite, ouvrez Talendus depuis l'icône, comme n'importe quelle appli."
    download_svg = """<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8v22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><path d="M16 24l8 8 8-8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 38h28" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>"""
    file_svg = """<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="12" y="8" width="24" height="32" rx="4" fill="none" stroke="currentColor" stroke-width="3"/><path d="M18 20h12M18 28h8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>"""
    check_svg = """<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="16" fill="#ff6b00"/><path d="M16 24.5l5 5 11-12" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
    gear_svg = """<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="7" fill="none" stroke="currentColor" stroke-width="3"/><path d="M24 8v4M24 36v4M8 24h4M36 24h4M12.5 12.5l2.8 2.8M32.7 32.7l2.8 2.8M12.5 35.5l2.8-2.8M32.7 15.3l2.8-2.8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>"""

    def step(num, heading, text, glyph):
        return f"""
        <li>
          <span class="tl-install-step-num">{num}</span>
          <div class="tl-install-step-copy">
            <h3>{heading}</h3>
            <p>{text}</p>
          </div>
          <div class="tl-install-glyph" aria-hidden="true">{glyph}</div>
        </li>"""

    return f"""
    <section class="tl-section tl-install-section" id="tl-install-board">
      <div class="container">
        <div class="tl-install-canvas">
          <div class="tl-install-hero-card">
            <div class="tl-install-icon-preview" aria-hidden="true">
              <img src="{a}assets/img/logo/icon-192.png" width="72" height="72" alt="">
              <span>Talendus</span>
            </div>
            <p class="tl-install-already" data-install-already hidden>{already}</p>
            <h2>{title}</h2>
            <p>{lead}</p>
            <p class="tl-install-safari-note" data-install-safari hidden>{safari}</p>
            <button type="button" class="tl-btn" data-install-now>{add}</button>
            <div class="tl-install-direct">
              <a class="tl-btn" href="{apk}" data-install-android-file>{android_btn}</a>
              <a class="tl-btn tl-btn-ghost" href="{ios}" data-install-ios-file>{ios_btn}</a>
            </div>
          </div>
          <div class="tl-install-lanes">
            <article class="tl-install-lane" data-install-android>
              <h3>{android_h}</h3>
              <ol class="tl-install-steps">
                {step(1, a1_t, a1_p, download_svg)}
                {step(2, a2_t, a2_p, file_svg)}
                {step(3, a3_t, a3_p, check_svg)}
              </ol>
            </article>
            <article class="tl-install-lane" data-install-ios>
              <h3>{ios_h}</h3>
              <ol class="tl-install-steps">
                {step(1, i1_t, i1_p, download_svg)}
                {step(2, i2_t, i2_p, gear_svg)}
                {step(3, i3_t, i3_p, check_svg)}
              </ol>
            </article>
          </div>
          <p class="tl-muted tl-install-after">{after}</p>
        </div>
      </div>
    </section>
    """


def native_app_page(lang="fr"):
    """L’appli mobile est mise de côté : on renvoie vers le site, en gardant verify/reset."""
    is_en = lang == "en"
    jobs = "/en/jobs.html" if is_en else "/emplois.html"
    portal = "/en/account.html" if is_en else "/espace.html"
    employer = "/en/account-employer.html" if is_en else "/espace-employeur.html"
    html_lang = "en-CA" if is_en else "fr-CA"
    lead = "Continue on the Talendus website." if is_en else "Continuez sur le site Talendus."
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>Talendus</title>
  <script>
  (function () {{
    var raw = (location.hash || "").replace(/^#\\/?/, "");
    var parts = raw.split("/").filter(Boolean);
    var name = parts[0] || "";
    var id = parts.slice(1).join("/");
    var jobs = {jobs!r};
    var portal = {portal!r};
    var employer = {employer!r};
    var dest = jobs;
    if (name === "verify" && id) dest = portal + "#/verify/" + encodeURIComponent(id);
    else if (name === "reset" && id) dest = portal + "#/reset/" + encodeURIComponent(id);
    else if (name === "forgot") dest = portal + "#/forgot";
    else if (name === "hiring" || name === "need" || name === "inbox" || name === "invoices" || name === "company" || name === "pipeline") dest = employer;
    else if (name === "login" || name === "register" || name === "home" || name === "apps" || name === "saved" || name === "settings" || name === "profile" || name === "messages" || name === "notifs") dest = portal;
    location.replace(dest);
  }})();
  </script>
</head>
<body>
  <p><a href="{jobs}">{lead}</a></p>
</body>
</html>
"""


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
        + header(solid, lang=lang, alt_url=switch, persona=persona, current=slug.split("/")[-1] or "index.html")
        + body
        + footer(lang, persona=persona)
    )


# Back-compat aliases used by older imports
SPEED_STRIP = speed_strip("fr")
CTA_BAND = cta_band("fr")
FOOTER = footer("fr")
HEADER_NAV = nav_html("fr")
PRELOADER = preloader("fr", "")
