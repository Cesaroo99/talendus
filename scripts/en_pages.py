"""English pages for Talendus, native copy, not machine-translated chrome."""

from parts import speed_strip, cta_band, faq_html, proof_stats, FAQ_EMPLOYERS_EN, FAQ_CANDIDATES_EN, FAQ_HOME_EN, homepage_faq
from seo_pages import write_en as write_seo_en
from positioning import (
    homepage_after_hero, job_search_filters, employer_need_fields,
    talent_trade_options, sectors_cloud, trades_cloud, ai_coming_soon,
    human_hire_band, problems_section, approach_section, process_section,
    why_talendus_section, ai_engine_section, human_section, company_types_section,
    candidate_journey_section, for_candidates_section,
    placement_process_services_section, technology_section, ai_screening_section,
    competitive_advantage_section, hiring_need_form_section,
    bad_hire_calculator_section,
    job_card_html, jobs_listing_header, jobs_empty_state, job_detail_html, related_job_cards,
)

A = "../assets/"
SPEED = speed_strip("en", "entreprise")
SPEED_TALENT = speed_strip("en", "talent")
CTA = cta_band("en", "entreprise")
CTA_TALENT = cta_band("en", "talent")
CTA_GATE = cta_band("en", "gateway")
WA = "https://wa.me/15145550199?text=Hello%20Talendus%2C%20I%20would%20like%20to%20talk%20about%20a%20hiring%20need."


def img(name):
    return f"{A}img/all-images/industry/{name}"


JOBS_EN = [
    ("cariste", "Forklift operator", "Laval", "entrepot", "Permanent", "$22 to $26/hr", "Full-time", "Forklift permit, 1 year warehouse experience.", "transport", "forklift", "intermediaire"),
    ("operateur-production", "Production operator", "Longueuil", "production", "Permanent", "$20 to $24/hr", "Full-time", "Production experience, ability to follow procedures, teamwork.", "manufacturier", "production", "debutant"),
    ("soudeur", "Welder-fitter", "Drummondville", "metallurgie", "Permanent", "$28 to $34/hr", "Full-time", "MIG/TIG welding, blueprint reading, competency cards an asset.", "manufacturier", "welding", "intermediaire"),
    ("machiniste-cnc", "CNC machinist", "Saint-Jérôme", "manufacturier", "Permanent", "$30 to $38/hr", "Full-time", "Programming or set-up, drawing reading, 3 years of experience.", "manufacturier", "CNC machining", "senior"),
    ("electromecanicien", "Electromechanical technician", "Montreal", "maintenance", "Permanent", "$32 to $40/hr", "Full-time", "Troubleshooting, hydraulics, pneumatics, electricity.", "ingenierie", "electromechanics", "intermediaire"),
    ("mecanicien-industriel", "Industrial mechanic", "Sherbrooke", "maintenance", "Permanent", "$30 to $36/hr", "Full-time", "Preventive maintenance, alignment, conveyors, reliability.", "manufacturier", "mechanics", "intermediaire"),
    ("journalier-usine", "Plant labourer", "Boucherville", "production", "Permanent", "$18 to $21/hr", "Full-time", "Physical fitness, punctuality, on-the-job training provided.", "manufacturier", "production", "debutant"),
    ("superviseur-production", "Production supervisor", "Trois-Rivières", "supervision", "Permanent", "$70,000 to $85,000", "Full-time", "Team leadership, KPIs, 5 years in production.", "manufacturier", "supervision", "senior"),
    ("coordonnateur-logistique", "Logistics coordinator", "Anjou", "logistique", "Permanent", "$55,000 to $68,000", "Full-time", "WMS, planning, English an asset.", "transport", "logistics, WMS", "intermediaire"),
    ("directeur-usine", "Plant manager", "Quebec City", "cadres", "Permanent", "$120,000 to $150,000", "Full-time", "P&L, Lean, managing a 100+ employee site. Confidential mandate.", "manufacturier", "leadership", "senior"),
    ("developpeur", "Developer", "Montreal", "technologie", "Permanent", "$75,000 to $95,000", "Full-time", "Python or JavaScript, 2 years of experience, teamwork.", "technologie", "Python, JavaScript", "intermediaire"),
    ("comptable", "Accountant", "Quebec City", "finance", "Permanent", "$55,000 to $70,000", "Full-time", "Accounting, Excel, relevant diploma.", "finance", "Excel, accounting", "intermediaire"),
    ("ingenieur", "Engineer", "Sherbrooke", "ingenierie", "Permanent", "$80,000 to $100,000", "Full-time", "Engineering, project management, 3 years of experience.", "ingenierie", "project management", "senior"),
    ("chauffeur", "Driver", "Anjou", "transport", "Permanent", "$22 to $28/hr", "Full-time", "Valid driver's licence, punctuality, clean driving record.", "transport", "driving", "intermediaire"),
    ("infirmier", "Nurse", "Laval", "sante", "Permanent", "$32 to $42/hr", "Full-time", "OIIQ licence, clinical experience, teamwork.", "sante", "care", "intermediaire"),
    ("vendeur", "Sales associate", "Longueuil", "commerce", "Permanent", "$18 to $24/hr", "Full-time", "Retail sales, customer service, people skills.", "commerce", "sales", "debutant"),
    ("responsable-rh", "HR manager", "Montreal", "administration", "Permanent", "$70,000 to $90,000", "Full-time", "Recruiting, labour relations, 5 years in HR.", "administration", "HR", "senior"),
    ("specialiste-marketing", "Marketing specialist", "Montreal", "marketing", "Permanent", "$55,000 to $75,000", "Full-time", "Digital marketing, communications, campaign management.", "marketing", "marketing", "intermediaire"),
]

SECTORS_EN = [
    ("manufacturier", "Manufacturing", "Manufacturing recruitment in Quebec", "One example among others: fabrication, assembly and production trades. Talendus also hires well beyond industry."),
    ("production", "Production", "Production recruitment in Quebec", "Lines, methods, quality and supervision. One of many roles Talendus can fill."),
    ("entrepot", "Warehousing", "Warehouse recruitment Quebec", "Forklift operators, pickers, clerks and warehouse supervisors, an example of logistics profiles."),
    ("logistique", "Logistics", "Logistics recruitment Quebec", "Planning, transport, WMS and coordination. Logistics is one industry among many."),
    ("distribution", "Distribution", "Distribution recruitment Quebec", "Distribution centres, shipping, receiving and inventory management."),
    ("transport", "Transportation", "Transportation and logistics recruiting", "Drivers, transport coordination and flow. Talendus also supports other industries."),
    ("transformation-alimentaire", "Food processing", "Food recruitment Quebec", "Food production: hygiene, operators and supervision. An example, not an exclusive specialty."),
    ("metallurgie", "Metals", "Metals and welding recruitment Quebec", "Welding, machining, metal fabrication. Other roles and industries are equally in scope."),
    ("plasturgie", "Plastics", "Plastics recruitment Quebec", "Injection, extrusion, press set-up and process technicians."),
    ("maintenance", "Maintenance", "Maintenance recruitment Quebec", "Technicians, mechanics and reliability leads, among a wide range of roles."),
]

ARTICLES_EN = [
    ("mauvaise-embauche", "What a bad hire really costs", "HR", "usine-equipe.jpg",
     "A poor fit is more than a salary. Training, overtime, lost productivity and turnover add up fast, in any industry."),
    ("machiniste-cnc", "Hiring a CNC machinist in Quebec in 2026", "Roles", "cnc-machiniste.jpg",
     "The CNC machinist remains a tight profile. Here is how to attract, assess and keep this talent, one example among many roles."),
    ("caristes-entrepot", "Forklift shortage: tactics for warehouses", "Logistics", "entrepot-logistique.jpg",
     "Distribution centres compete for experienced operators. Three practical levers, transferable to other scarce roles."),
    ("superviseur-production", "Production supervisor: the profile that steadies a team", "Production", "usine-equipe.jpg",
     "A strong supervisor stabilizes quality and climate. Here is the portrait we validate, applicable to other management roles."),
    ("roulement-manufacturier", "Cutting turnover in recruiting", "Recruiting", "soudeur-atelier.jpg",
     "Turnover is not only a pay problem. Onboarding, role clarity and cultural fit make the difference, whatever the industry."),
]

TOPICS_EN = [
    "Writing a clear job posting", "Too many applications, too little fit",
    "Hiring a developer", "Hiring an accountant", "Hiring in healthcare",
    "Recruiting in construction", "Remote work and location", "Leadership search",
    "30/60/90 onboarding", "Employer brand", "Interview tests",
    "Temporary vs permanent contracts", "Retaining skilled trades",
    "Cost of a vacant seat", "Hiring in the regions", "Skills over titles",
    "Replacement guarantee FAQ", "Preparing a manager interview",
]


INDEX_EN = rf"""
<div class="hero2-arrow-hero tl-gateway-hero">
  <div class="hero2-slider-area">
        <div class="img1"><img src="{img('usine-equipe.jpg')}" alt="Team at work" fetchpriority="high" decoding="async"></div>
        <div class="container">
            <div class="hero2-heading tl-hero-lock">
                <h5>Talendus. An intelligent placement agency.</h5>
                <div class="space16"></div>
                <h1 data-persona-only="gateway">Are you hiring, or looking for a job?</h1>
                <h1 data-persona-only="talent">Your path, studied. The right opportunities.</h1>
                <h1 data-persona-only="entreprise">The right talent. Faster. Smarter.</h1>
                <div class="space16"></div>
                <p data-persona-only="gateway">Pick your side to continue. Candidates and employers do not land on the same pages.</p>
                <p data-persona-only="talent">Create your profile, submit your resume. We study your path and contact you when an opportunity fits. Free for you. Companies do not receive your contact details.</p>
                <p data-persona-only="entreprise">Hand us the need. We search, screen and present a qualified shortlist. You do not browse a resume database. You keep the final decision.</p>
            </div>
            <div class="tl-persona-cards" data-persona-only="gateway">
              <a class="tl-persona-card is-talent" href="candidates.html" data-set-persona="talent">
                <span class="tl-kicker">Candidates</span>
                <h2>I'm looking for a job</h2>
                <p>Join the Talendus network. Profile, resume and next steps live on the candidate side.</p>
                <span class="tl-persona-go">Create my profile <i class="fa-solid fa-arrow-right"></i></span>
              </a>
              <a class="tl-persona-card is-hire" href="employers.html" data-set-persona="entreprise">
                <span class="tl-kicker">Employers</span>
                <h2>I'm hiring</h2>
                <p>Hand us the role to fill. Search, screening and the shortlist live on the employer side.</p>
                <span class="tl-persona-go">Hand us the search <i class="fa-solid fa-arrow-right"></i></span>
              </a>
            </div>
        </div>
  </div>
</div>
"""


def build_en(write, wrap, page_hero):
    write("en/index.html", wrap(
        "Talendus | Intelligent placement agency",
        "Talendus is a placement agency. Companies: hand us a need, receive a shortlist. Candidates: create a profile, be contacted when an opportunity fits. Every industry.",
        "en/",
        INDEX_EN + homepage_after_hero("en") + homepage_faq("en") + sectors_cloud("en") + trades_cloud("en"),
        solid=False,
        lang="en",
        alt="",
    ))

    write("en/about.html", wrap(
        "About Talendus | Intelligent placement agency",
        "Talendus is a placement agency that already combines human expertise, technology and artificial intelligence. Every industry, every kind of role.",
        "en/about.html",
        page_hero(
            "The agency",
            "Talendus was built as a next-generation placement agency: human, technological, and already augmented by AI.",
            "We do not merely give access to candidates. We do the search for companies. Artificial intelligence is already part of how Talendus works today.",
            actions='<a class="tl-btn" href="candidates.html" data-set-persona="talent">For talent</a><a class="tl-btn tl-btn-ghost" href="employers.html" data-set-persona="entreprise">For employers</a>',
        )
        + f"""
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <div class="tl-prose" style="max-width:none">
    <h2 class="tl-h2">Why we exist</h2>
    <p>Too many companies lose weeks looking for the right people, sorting too many applications, or letting a process drag. Too many talented people send resumes into the void. Hiring deserves better than a job board or software you have to operate alone.</p>
    <p>Talendus was designed as a next-generation placement agency: generalist, human and technological. When a company has a need, it hands it to us. We take on the search and the screening. Artificial intelligence is already at the heart of our internal tools: it speeds up analysis, search and some screening steps. Consultants stay there to understand, qualify and present. The company keeps the final decision.</p>
    <h2 class="tl-h2">What we do</h2>
    <p>We connect companies and talent. Developers, accountants, welders, nurses, drivers, HR managers, and many other roles, in every industry. A consultant presents the files. Candidates and employers stay on their own side. There is no unmediated direct channel.</p>
    <p>We hire better, faster and more intelligently with AI: “we hire” means Talendus runs the search and screening for the company. “Faster”: our tools and AI already accelerate certain steps. “More intelligently”: data, technology, AI and human expertise, together, today.</p>
    <h2 class="tl-h2">What we are not</h2>
    <p>Not a job board where the company browses a database. Not a marketplace. Not a self-serve ATS. Not software that promises a perfect candidate without a human. Technology stays in service of the Talendus process.</p>
    <h2 class="tl-h2">AI is already part of how we operate</h2>
    <p>Talendus already uses artificial intelligence in its recruiting operations. It is not a long-term vision and not a “coming soon” feature. Our teams rely on internal tools to analyse resumes, extract skills, relate a profile to a role, synthesize information and prioritize files for review. You do not have to use those tools: we mobilize them on your behalf. Final qualification stays human.</p>
    </div>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="{img('usine-equipe.jpg')}" alt="Team at work">
      </div>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">How we work</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Generalist</h3><p>Every industry, every company size, a wide range of roles. Sector is a parameter of the mandate, not the agency's identity.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Intermediary</h3><p>The company hands us the need. The candidate creates a profile. Talendus searches, screens, presents. Nobody is left alone in front of a database.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Human and technological</h3><p>AI speeds internal analysis. Consultants validate relevance. You choose. Nothing is promised as an automatic decision.</p></div></div>
    </div>
    </div></section>
    """
        + human_section("en")
        + sectors_cloud("en"),
        lang="en",
        alt="a-propos.html",
    ))

    services_cards = "".join(
        f'<a class="tl-card" href="{href}"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></a>'
        for href, chip, t, p in [
            ("permanent-recruiting.html", "Permanent", "Permanent recruiting", "Stable roles in every industry. Success fees, replacement guarantee."),
            ("executive-search.html", "Passive", "Search mandates", "Direct approach of passive candidates for scarce profiles, whatever the industry."),
            ("leadership-recruiting.html", "Leadership", "Manager recruiting", "Managers and executives. Often confidential."),
            ("industrial-recruiting.html", "Example", "Industrial recruiting", "One example among others: production, maintenance, logistics. Talendus is not limited to industry."),
            ("technical-recruiting.html", "Trades", "Skilled roles", "Technicians, welders, developers, nurses, accountants, a wide range of profiles."),
            ("temporary-recruiting.html", "Urgent", "Urgent recruiting", "When a critical seat is uncovered. A filtered shortlist, not a resume flood."),
            ("executive-search.html", "Discreet", "Confidential mandates", "Manager replacements or reorganizations run without internal noise."),
            ("employers.html", "HR", "HR support", "Job descriptions, salary grids, joint interviews and onboarding."),
        ]
    )
    write("en/services.html", wrap(
        "Recruiting services | Talendus",
        "Talent search, screening, qualification, shortlist and placement. Talendus already uses AI internally to speed up analysis. The company decides. Every industry.",
        "en/services.html",
        page_hero(
            "Services",
            "From the first need to the hire: one contact.",
            "Permanent, temporary, search, leadership and skilled roles. For every company, not for one industry.",
            actions='<a class="tl-btn" href="contact.html">Talk to Talendus</a>',
        )
        + f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    '''
        + placement_process_services_section("en")
        + technology_section("en")
        + ai_coming_soon("en")
        + competitive_advantage_section("en"),
        lang="en",
        alt="services.html",
    ))

    write("en/employers.html", wrap(
        "Employers | Placement agency | Talendus",
        "Hand a hire to Talendus. We already use AI internally to speed up search, analysis and screening. You receive a qualified shortlist and keep the final decision.",
        "en/employers.html",
        page_hero(
            "Employers",
            "Hiring? Hand us the need.",
            "Talendus searches, evaluates and shortlists the most relevant talent. We already use artificial intelligence in our internal tools to speed up search, analysis and screening. You review a qualified selection and make the final decision.",
            actions='<a class="tl-btn" href="contact.html">Hand us the search</a><a class="tl-btn tl-btn-ghost" href="hiring-need.html">Describe my need</a>',
            badges='<span class="tl-badge tl-badge-light">Placement agency</span> <span class="tl-badge tl-badge-light">Every industry</span>',
        )
        + problems_section("en")
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-prose">
        <div class="tl-kicker">The Talendus solution</div>
        <h2 class="tl-h2">We do the search for you.</h2>
        <p>You have a role to fill. Instead of posting an ad and sorting dozens (sometimes hundreds) of applications, you hand the need to Talendus. We understand the role, search for profiles, analyse careers, screen, speak with candidates when needed, evaluate, then present a qualified selection.</p>
        <p>You do not access a resume database. You do not “find talent” on Talendus as if it were ATS software. You mandate an agency. Talendus already uses artificial intelligence in its internal tools to speed up search, analysis and screening. You benefit from that power without using it yourself. The hiring decision stays yours.</p>
      </div>
    </div></section>
    """
        + process_section("en")
        + """
    <section class="tl-section"><div class="container">
      <div class="row g-4">
        <div class="col-lg-6"><h2 class="tl-h2">Searching for talent</h2><p>We draw on the Talendus network, known profiles, applications received and, when useful, a framed posting. People already in a job can be approached discreetly. The aim is not to publish the most ads: it is to identify the profiles with the strongest potential fit.</p></div>
        <div class="col-lg-6"><h2 class="tl-h2">Screening</h2><p>Each identified profile is reviewed: skills, experience, qualifications, fit with the role and the criteria we agreed with you. What does not hold never reaches your desk.</p></div>
        <div class="col-lg-6"><h2 class="tl-h2">Interviews</h2><p>When needed, Talendus speaks with candidates before presenting them: path, motivations, fit. Your interviews then involve people already qualified. You run your process; we stay the intermediary.</p></div>
        <div class="col-lg-6"><h2 class="tl-h2">Shortlist</h2><p>We do not send a massive list. We present a selection of relevant profiles, each one we are prepared to stand behind. Relevance is what we sell. Volume is not.</p></div>
      </div>
    </div></section>
    """
        + ai_engine_section("en")
        + ai_screening_section("en")
        + competitive_advantage_section("en")
        + human_section("en")
        + why_talendus_section("en")
        + company_types_section("en")
        + bad_hire_calculator_section("en")
        + f"""
    <section class="tl-section tl-ice" id="temoignages"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Employer testimonials</div>
        <h2 class="tl-h2">What employers say</h2>
      </div>
      <div class="tl-grid-3 tl-quotes">
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>They understood the role on the first call. The files they presented actually matched what we needed.</p>
          <footer><strong>M.L.</strong><span>Director of operations · South Shore</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Not an agency that sends 40 resumes. Three solid files, and follow-up after the hire.</p>
          <footer><strong>J.R.</strong><span>Director · Mauricie</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>A confidential mandate run without internal noise. Start date aligned with our calendar.</p>
          <footer><strong>S.B.</strong><span>VP · Montérégie</span></footer>
        </blockquote>
      </div>
    </div></section>
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker" id="faq">Employer FAQ</div>
        <h2 class="tl-h2">What HR and managers ask</h2>
      </div>
      {faq_html(FAQ_EMPLOYERS_EN)}
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Hand us the search</a>
      </div>
    </div></section>
    """
        + sectors_cloud("en")
        + proof_stats("en"),
        lang="en",
        alt="entreprises.html",
    ))

    write("en/candidates.html", wrap(
        "Candidates | Join Talendus",
        "Create your profile with Talendus. We study your path and contact you when an opportunity fits. Free. Every industry.",
        "en/candidates.html",
        page_hero(
            "Candidates",
            "Create your profile. Talendus accompanies you toward opportunities that fit.",
            "You are not a resume in a database. A consultant studies your path, may contact you, evaluate you, and introduce you to a company when the fit holds. It's free.",
            actions='<a class="tl-btn" href="candidates.html#cv">Create my profile</a><a class="tl-btn tl-btn-ghost" href="jobs.html">See opportunities</a>',
            badges='<span class="tl-badge tl-badge-light">Free for you</span> <span class="tl-badge tl-badge-light">Every industry</span>',
        )
        + for_candidates_section("en")
        + candidate_journey_section("en")
        + f"""
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Create your profile</h2>
          <p class="tl-lead">Tell us your role, skills and region. A consultant calls if a mandate fits. We don't send you to fifteen interviews for nothing.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">On weekdays we usually reply within 30 minutes.</div>
          <p id="process"></p>
          <h3>How it works</h3>
          <ol>
            <li>Create your profile.</li>
            <li>Apply to openings or submit your resume.</li>
            <li>Track applications with a Talendus consultant.</li>
            <li>We contact you when the role and pay match.</li>
          </ol>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Name</label><input required name="nom">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Target role</label>
            <select name="metier">""" + talent_trade_options("en") + """</select>
            <label>Region</label><input name="region" placeholder="Laval, Montérégie, Quebec City, remote…">
            <label>Link to your resume (Drive, Dropbox…)</label><input name="cv" placeholder="https://">
            <button class="tl-btn tl-btn-lg" type="submit">Create my profile</button>
            <div class="tl-success" role="status"></div>
          </form>
        </div>
      </div>
    </div></section>
    <section class="tl-section" id="temoignages"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Talent testimonials</div>
        <h2 class="tl-h2">What placed candidates say</h2>
      </div>
      <div class="tl-grid-3 tl-quotes">
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>I was a night forklift operator. Talendus introduced me to a logistics coordinator role in Laval. Clear interview, clean terms.</p>
          <footer><strong>A.D.</strong><span>Candidate placed · Laval</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Not fifteen useless interviews. A consultant understood my role, then introduced me to a company actually hiring.</p>
          <footer><strong>K.T.</strong><span>Candidate placed · Drummondville</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>I submitted my resume on a Tuesday. Friday I had an interview in Montreal. Free, no pressure.</p>
          <footer><strong>R.M.</strong><span>Candidate · Montreal</span></footer>
        </blockquote>
      </div>
    </div></section>
    <section class="tl-section" id="faq"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">Candidate FAQ</div>
        <h2 class="tl-h2">Before you submit your resume</h2>
      </div>
      """ + faq_html(FAQ_CANDIDATES_EN) + """
    </div></section>
    """,
        lang="en",
        alt="candidats.html",
    ))

    write("en/contact.html", wrap(
        "Contact | Talk to Talendus",
        "Contact Talendus in Montreal. Describe a hiring need or create your profile. Calls by appointment. 514 555-0199 · info@talendus.ca",
        "en/contact.html",
        page_hero(
            "Contact",
            "Write to us. We'll call you back.",
            "Looking for a job, or filling a seat? Pick your door. The form follows.",
            actions='',
            badges='<span class="tl-badge tl-badge-light">By appointment</span> <span class="tl-badge tl-badge-light">Mon–Fri, 8 a.m. to 5 p.m.</span>',
        )
        + f"""
    <section class="tl-section-sm"><div class="container">
      <div class="tl-info-grid">
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-phone"></i></div>
          <div>
            <h3>Phone</h3>
            <p><a href="tel:+15145550199">514 555-0199</a></p>
            <p>On weekdays we usually reply within 30 minutes.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-regular fa-envelope"></i></div>
          <div>
            <h3>Email</h3>
            <p><a href="mailto:info@talendus.ca">info@talendus.ca</a></p>
            <p>Mon–Fri, 8 a.m. to 5 p.m.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-brands fa-whatsapp"></i></div>
          <div>
            <h3>WhatsApp</h3>
            <p><a href="{WA}" target="_blank" rel="noopener noreferrer">Open a conversation</a></p>
            <p>Replies during business hours.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-calendar-check"></i></div>
          <div>
            <h3>Meetings</h3>
            <p>Calls are by appointment.</p>
            <p>We work around your availability.</p>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section" id="parcours"><div class="container">
      <div data-persona-only="gateway">
        <div class="tl-center" style="max-width:640px;margin:0 auto 28px">
          <div class="tl-kicker">You are</div>
          <h2 class="tl-h2">Pick your door</h2>
        </div>
        <div class="tl-persona-doors">
          <a class="tl-persona-door" href="#formulaire" data-set-persona="talent">
            <span class="tl-kicker">Talent</span>
            <h2>I'm looking for a job</h2>
            <p>Submit your resume or ask about a role. It's free.</p>
            <span class="tl-split-cta">Continue →</span>
          </a>
          <a class="tl-persona-door" href="#formulaire" data-set-persona="entreprise">
            <span class="tl-kicker">Employers</span>
            <h2>I'm hiring</h2>
            <p>Open a mandate, post a job or book a call.</p>
            <span class="tl-split-cta">Continue →</span>
          </a>
        </div>
      </div>
      <div class="tl-contact-grid" id="formulaire" style="margin-top:36px">
        <div data-persona-only="talent">
          <div class="tl-kicker">Talent</div>
          <h2 class="tl-h2">Submit my resume or ask a question</h2>
          <p class="tl-lead">It's free. A consultant calls if a mandate matches.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <input type="hidden" name="profil" value="Candidate, I am looking for a role">
            <label>Name</label><input required name="nom">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Subject</label>
            <select name="objet">
              <option>Submit my resume</option>
              <option>Join the talent pool</option>
              <option>Question about a job</option>
            </select>
            <label>Message</label><textarea required name="message" placeholder="Role, skills, city, job type"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Create my profile</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="entreprise">
          <div class="tl-kicker">Employers</div>
          <h2 class="tl-h2">Describe my hiring need</h2>
          <p class="tl-lead">Industry, role, headcount, location, contract type. Free call, by appointment.</p>
          <form class="tl-form" action="#" method="post" data-form="hiring-need">
            <input type="hidden" name="profil" value="Employer, I am hiring">
            <label>Name</label><input required name="nom">
            <label>Company</label><input required name="entreprise">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Subject</label>
            <select name="objet">
              <option>Hand us the search</option>
              <option>Describe my need</option>
              <option>Talk to Talendus</option>
            </select>
            """ + employer_need_fields("en") + """
            <button class="tl-btn tl-btn-lg" type="submit">Hand us the search</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="gateway"></div>
        <div>
          <div class="tl-map">
            <iframe title="Montreal map" src="https://maps.google.com/maps?q=Montreal%20Quebec&t=&z=11&ie=UTF8&iwloc=&output=embed" loading="lazy"></iframe>
          </div>
        </div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="contact.html",
    ))

    cards = "".join(job_card_html(job, "en") for job in JOBS_EN)
    write("en/jobs.html", wrap(
        "Job openings | Talendus",
        "Openings in every industry: developer, accountant, welder, nurse, driver, forklift operator and more. Filter by industry, role, skills, experience and location.",
        "en/jobs.html",
        jobs_listing_header("en")
        + f"""
    <section class="tl-section tl-jobs-board"><div class="container">
      {job_search_filters("en")}
      <div class="tl-jobs-grid" id="job-list">{cards}</div>
      {jobs_empty_state("en")}
    </div></section>
    """
        + SPEED_TALENT
        + CTA_TALENT,
        lang="en",
        alt="emplois.html",
    ))

    for job in JOBS_EN:
        slug, title, city, cat, typ, sal, shift, req, sector, skills, exp = job
        write(f"en/job-{slug}.html", wrap(
            f"{title} in {city} | Job | Talendus",
            f"{title} role in {city}, Quebec. {typ}. Apply through Talendus: a consultant presents your file. Placement agency, every industry.",
            f"en/job-{slug}.html",
            job_detail_html(job, related_job_cards(JOBS_EN, slug, "en"), "en"),
            lang="en",
            alt=f"emploi-{slug}.html",
            extra_json_ld={
                "@context": "https://schema.org",
                "@type": "JobPosting",
                "title": title,
                "description": req,
                "identifier": {"@type": "PropertyValue", "name": "Talendus", "value": slug},
                "datePosted": "2026-07-20",
                "employmentType": "FULL_TIME" if typ.lower().startswith("perm") else "TEMPORARY",
                "hiringOrganization": {"@type": "EmploymentAgency", "name": "Talendus", "sameAs": "https://talendus.ca"},
                "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "QC", "addressCountry": "CA"}},
                "baseSalary": {"@type": "MonetaryAmount", "currency": "CAD", "value": sal},
                "url": f"https://talendus.ca/en/job-{slug}.html",
            },
            og_type="article",
        ))
    sec_cards = "".join(
        f'<a class="tl-card" href="sector-{s}.html"><div class="body"><h3>{n}</h3><p>{d}</p></div></a>'
        for s, n, t, d in SECTORS_EN
    )
    write("en/sectors.html", wrap(
        "Every industry | Recruiting platform | Talendus",
        "Talendus is for every industry. Technology, construction, healthcare, finance, manufacturing, retail and many more.",
        "en/sectors.html",
        page_hero(
            "Every industry", "Talendus is built for every industry.",
            "These industries are examples of what the platform can do, not an exclusive list. Whatever your industry, Talendus helps you find the right talent.",
            actions='<a class="tl-btn" href="contact.html">Talk to Talendus</a>',
        )
        + sectors_cloud("en")
        + f'<section class="tl-section tl-ice"><div class="container"><div class="tl-center" style="max-width:720px;margin:0 auto 28px"><div class="tl-kicker">Sample pages</div><h2 class="tl-h2">A few verticals already documented</h2><p class="tl-lead">More pages (construction, healthcare, finance, IT…) will come with real content, not empty shells.</p></div><div class="tl-grid-3">{sec_cards}</div></div></section>'
        + trades_cloud("en"),
        lang="en",
        alt="secteurs.html",
    ))
    for slug, name, title, desc in SECTORS_EN:
        write(f"en/sector-{slug}.html", wrap(
            f"{title} | Talendus",
            desc,
            f"en/sector-{slug}.html",
            page_hero(
                "Industry example", name, desc,
                actions='<a class="tl-btn" href="contact.html">Talk to Talendus</a>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} This is not an exclusive specialty: Talendus recruits for every company.</p>
              <h2 class="tl-h2">Typical roles</h2>
              <p>Operations, skilled trades, supervision, management, and other profiles depending on the need.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="contact.html">Hand us the search</a>
                <a class="tl-btn tl-btn-ghost-dark" href="sectors.html">Every industry</a>
              </div>
            </div>
          </div>
        </div></section>
        """,
            lang="en",
            alt=f"secteur-{slug}.html",
        ))

    art_cards = "".join(
        f'<a class="tl-card" href="article-{s}.html"><div class="tl-hero-media" style="height:180px"><img src="{img(im)}" alt="{t}" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">{cat}</span><h3>{t}</h3><p>{lead}</p></div></a>'
        for s, t, cat, im, lead in ARTICLES_EN
    )
    topics = "".join(f'<li style="margin-bottom:8px">{t}</li>' for t in TOPICS_EN)
    write("en/blog.html", wrap(
        "Recruiting, HR and careers blog | Talendus",
        "Articles on recruiting: finding the right talent, cutting turnover, clarifying a role. Every industry.",
        "en/blog.html",
        page_hero(
            "Blog", "Recruiting, HR and careers.",
            "Useful writing for companies and candidates. The hiring problem, not one industry.",
            actions='<a class="tl-btn" href="contact.html">Talk to Talendus</a>',
            badges="",
        )
        + f'<section class="tl-section"><div class="container"><div class="tl-grid-3" id="blog-list">{art_cards}</div><h2 class="tl-h2" style="margin-top:48px">Coming topics</h2><ul class="tl-muted">{topics}</ul></div></section>',
        lang="en",
        alt="blog.html",
    ))
    for slug, title, cat, im, lead in ARTICLES_EN:
        write(f"en/article-{slug}.html", wrap(
            f"{title} | Talendus blog",
            lead,
            f"en/article-{slug}.html",
            page_hero(cat, title, lead, badges="")
            + f"""
        <section class="tl-section"><div class="container" style="max-width:800px">
          <img src="{img(im)}" alt="{title}" style="width:100%;border-radius:16px;margin-bottom:24px" loading="lazy" decoding="async">
          <p class="tl-lead">{lead}</p>
          <h2>What we see</h2>
          <p>Companies do not all hire the same way. Skills, experience, contract type and location weigh as much as the resume. A seat left vacant too long often costs more than a well-scoped recruiting mandate.</p>
          <h2>Practical moves</h2>
          <ul>
            <li>Clarify the role, real pay and required skills before approaching the market.</li>
            <li>Assess know-how (demonstration, scenarios) rather than diplomas alone.</li>
            <li>Plan 30/60/90-day onboarding: that is where retention is won.</li>
          </ul>
          <h2>How Talendus steps in</h2>
          <p>We target profiles by role and skills, validate the fit and present a few files, each one we're ready to stand behind. Talendus already uses AI internally to analyse information faster and spot correspondences; it does not choose in the company's place. Qualification stays human.</p>
          <p><a href="sectors.html">Every industry</a> · <a href="jobs.html">Job openings</a></p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Talk to Talendus</a>
            <a class="tl-btn tl-btn-ghost-dark" href="blog.html">Back to the blog</a>
          </div>
        </div></section>
        """,
            lang="en",
            alt=f"article-{slug}.html",
            extra_json_ld={
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": lead,
                "author": {"@type": "Organization", "name": "Talendus"},
                "publisher": {"@type": "Organization", "name": "Talendus", "url": "https://talendus.ca"},
                "mainEntityOfPage": f"https://talendus.ca/en/article-{slug}.html",
                "inLanguage": "en-CA",
                "image": f"https://talendus.ca/assets/img/all-images/industry/{im}",
            },
            og_type="article",
            og_image=f"assets/img/all-images/industry/{im}",
        ))

    write("en/404.html", wrap(
        "Page not found | Talendus",
        "The requested page does not exist. Return to the Talendus home page.",
        "en/404.html",
        page_hero("404", "This page does not exist.", "The mandate might still exist.",
                  actions='<a class="tl-btn" href="index.html">Back to home</a><a class="tl-btn tl-btn-ghost" href="contact.html">Write to us</a>',
                  badges=""),
        lang="en",
        alt="404.html",
        robots="noindex,nofollow",
    ))
    write("en/account.html", wrap(
        "My candidate account | Talendus",
        "Sign in to manage your profile, resume, applications and Talendus notifications.",
        "en/account.html",
        """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account"></div></div></section>""",
        lang="en",
        alt="espace.html",
        robots="noindex,nofollow",
    ))
    write("en/account-employer.html", wrap(
        "Employer portal | Talendus",
        "Sign in to manage job openings, applications, pipeline and Talendus invoices.",
        "en/account-employer.html",
        """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account" data-space="employer"></div></div></section>""",
        lang="en",
        alt="espace-employeur.html",
        robots="noindex,nofollow",
    ))
    write("en/privacy.html", wrap(
        "Privacy policy | Talendus",
        "Talendus privacy policy, talendus.ca.",
        "en/privacy.html",
        page_hero("Legal", "Privacy policy", "Resumes and mandates are handled confidentially.", badges="")
        + """<section class="tl-section"><div class="container" style="max-width:800px">
        <h2>Recruiting data</h2>
        <p>Talendus collects information needed for recruiting (contact details, resumes, job descriptions). It is not sold to third parties. It is used only to assess applications, open mandates and communicate with you.</p>
        <p>You may request access, correction or deletion by writing to info@talendus.ca. Data is kept as long as needed for recruiting and legal obligations in Quebec.</p>
        <h2>Cookies and measurement</h2>
        <p>Essential cookies keep the site working (sign-in, security, language). Analytics (Google Analytics) and marketing (Meta Pixel) cookies load <strong>only after you consent</strong>. You can accept, refuse or change this later via the cookie banner or by writing to info@talendus.ca.</p>
        <p>No advertising identifier is set until you accept non-essential cookies. Talendus does not sell browsing data.</p>
        </div></section>""",
        lang="en",
        alt="confidentialite.html",
    ))
    write("en/terms.html", wrap(
        "Terms of use | Talendus",
        "Terms of use for talendus.ca.",
        "en/terms.html",
        page_hero("Legal", "Terms of use", "talendus.ca presents the services of the Talendus firm.", badges="")
        + """<section class="tl-section"><div class="container" style="max-width:800px"><p>Content is provided for information. Mandates are subject to a written agreement. Sample openings and demonstration statistics may be adjusted to the firm’s live data.</p><p>Using the site implies acceptance of these terms. Questions: info@talendus.ca.</p></div></section>""",
        lang="en",
        alt="conditions.html",
    ))
    write("en/how-it-works.html", wrap(
        "How it works | Talent path | Talendus",
        "Create your profile, submit your resume, be considered for opportunities. Talendus presents your file. Free for talent.",
        "en/how-it-works.html",
        page_hero(
            "Talent",
            "From profile to a possible introduction, Talendus stays in the middle.",
            "Create your account, submit your resume, apply to openings if you wish. We study your path, may contact you, and talk to the company for you. Your contact details never go out on their own.",
            actions='<a class="tl-btn" href="account.html" data-auth-open="register">Create my profile</a>',
        )
        + candidate_journey_section("en"),
        lang="en",
        alt="comment-ca-fonctionne.html",
    ))
    write("en/hiring-need.html", wrap(
        "Hiring? Hand us the need | Talendus",
        "Placement agency: describe your hiring need. Talendus analyses, defines the profile, searches, screens and presents the best candidates. You make the final decision.",
        "en/hiring-need.html",
        page_hero(
            "Employers",
            "Hiring? Hand us the need.",
            "Describe the profile you are looking for. Our team analyses your need, defines the search criteria and takes on the recruiting process so we can present the most relevant candidates.",
            actions='<a class="tl-btn" href="#besoin">Describe my need</a><a class="tl-btn tl-btn-ghost" href="account-employer.html" data-auth-open="register">Open a company workspace</a>',
        )
        + process_section("en")
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-prose">
        <h2 class="tl-h2">A recruiting service, not a job posting</h2>
        <p>With Talendus, you do not simply post a job and wait for applications. You hand us the need and we take on the search and screening of talent.</p>
        <p>You do not need to spend hours posting, sorting and analysing hundreds of applications. Talendus takes the process on for you. With our teams, methods and technological tools that already include AI, we speed up search and qualification.</p>
        <p>You hand us the search. We take on sourcing, screening and qualification so you can focus on the final decision. We do not simply forward applications. We present a selection of profiles we have already searched and qualified against your need.</p>
      </div>
    </div></section>
    """
        + hiring_need_form_section("en")
        + human_hire_band("en"),
        lang="en",
        alt="besoin-de-recrutement.html",
    ))
    write("en/post-a-job.html", wrap(
        "Redirect | Talendus",
        "Redirect.",
        "en/post-a-job.html",
        '<section class="tl-section"><div class="container"><p>This page has moved. <a href="hiring-need.html">Continue</a></p><script>location.replace("hiring-need.html");</script></div></section>',
        lang="en",
        alt="besoin-de-recrutement.html",
        robots="noindex,nofollow",
    ))
    write("en/hr-solutions.html", wrap(
        "HR solutions | Recruiting support | Talendus",
        "HR support: job descriptions, salary grids, joint interviews and 30/60/90 onboarding. Every industry.",
        "en/hr-solutions.html",
        page_hero(
            "Employers",
            "Build a hiring process, not just plug a hole.",
            "Job descriptions, pay grids, joint interviews and onboarding follow-up, for companies tired of winging it.",
            actions='<a class="tl-btn" href="contact.html">Talk to Talendus</a>',
        )
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Job descriptions</h3><p>A role written as it is lived: responsibilities, skills, contract type.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Salary grids</h3><p>Align the offer with the market, without underpaying a scarce role.</p></div></div>
        <div class="tl-card"><div class="body"><h3>30/60/90 onboarding</h3><p>Follow-up after start date. Replacement guarantee on permanent mandates.</p></div></div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="solutions-rh.html",
    ))
    write_seo_en(write, wrap, page_hero, CTA)
