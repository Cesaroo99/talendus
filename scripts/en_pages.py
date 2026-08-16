"""English pages for Talendus — native copy, not machine-translated chrome."""

from parts import speed_strip, cta_band, faq_html, proof_stats, FAQ_EMPLOYERS_EN, FAQ_CANDIDATES_EN
from seo_pages import write_en as write_seo_en
from positioning import (
    homepage_after_hero, job_search_filters, employer_need_fields,
    talent_trade_options, sectors_cloud, trades_cloud, ai_coming_soon,
    human_hire_band,
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
    ("entrepot", "Warehousing", "Warehouse recruitment Quebec", "Forklift operators, pickers, clerks and warehouse supervisors — an example of logistics profiles."),
    ("logistique", "Logistics", "Logistics recruitment Quebec", "Planning, transport, WMS and coordination. Logistics is one industry among many."),
    ("distribution", "Distribution", "Distribution recruitment Quebec", "Distribution centres, shipping, receiving and inventory management."),
    ("transport", "Transportation", "Transportation and logistics recruiting", "Drivers, transport coordination and flow. Talendus also supports other industries."),
    ("transformation-alimentaire", "Food processing", "Food recruitment Quebec", "Food production: hygiene, operators and supervision. An example, not an exclusive specialty."),
    ("metallurgie", "Metals", "Metals and welding recruitment Quebec", "Welding, machining, metal fabrication. Other roles and industries are equally in scope."),
    ("plasturgie", "Plastics", "Plastics recruitment Quebec", "Injection, extrusion, press set-up and process technicians."),
    ("maintenance", "Maintenance", "Maintenance recruitment Quebec", "Technicians, mechanics and reliability leads — among a wide range of roles."),
]

ARTICLES_EN = [
    ("mauvaise-embauche", "What a bad hire really costs", "HR", "usine-equipe.jpg",
     "A poor fit is more than a salary. Training, overtime, lost productivity and turnover add up fast — in any industry."),
    ("machiniste-cnc", "Hiring a CNC machinist in Quebec in 2026", "Roles", "cnc-machiniste.jpg",
     "The CNC machinist remains a tight profile. Here is how to attract, assess and keep this talent — one example among many roles."),
    ("caristes-entrepot", "Forklift shortage: tactics for warehouses", "Logistics", "entrepot-logistique.jpg",
     "Distribution centres compete for experienced operators. Three practical levers, transferable to other scarce roles."),
    ("superviseur-production", "Production supervisor: the profile that steadies a team", "Production", "usine-equipe.jpg",
     "A strong supervisor stabilizes quality and climate. Here is the portrait we validate — applicable to other management roles."),
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
                <h5>Talendus. The intelligent recruiting platform for every company.</h5>
                <div class="space16"></div>
                <h1>Hire better, faster and more intelligently.</h1>
                <div class="space16"></div>
                <p>Looking for a job, or hiring? Talendus supports candidates and companies of every size, from SMEs to larger organizations, in every industry.</p>
                <p>From the first hiring need to identifying the best candidates, Talendus simplifies your recruiting process.</p>
            </div>
            <div class="tl-persona-cards">
              <a class="tl-persona-card is-talent" href="candidates.html" data-set-persona="talent">
                <span class="tl-kicker">Candidates</span>
                <h2>I'm looking for a job</h2>
                <p>Browse openings, create your profile, track applications. It's free. A consultant presents your file to employers.</p>
                <span class="tl-persona-go">Find a job <i class="fa-solid fa-arrow-right"></i></span>
              </a>
              <a class="tl-persona-card is-hire" href="employers.html" data-set-persona="entreprise">
                <span class="tl-kicker">Employers</span>
                <h2>I'm hiring</h2>
                <p>We send you the right talent, fast. A clear shortlist, not a stack of resumes to sort.</p>
                <span class="tl-persona-go">Find talent <i class="fa-solid fa-arrow-right"></i></span>
              </a>
            </div>
        </div>
  </div>
</div>
"""


def build_en(write, wrap, page_hero):
    write("en/index.html", wrap(
        "Talendus | Recruiting platform for every company",
        "Talendus is the intelligent recruiting platform for every company, from SMEs to larger organizations. Hire better, faster and more intelligently. Every industry.",
        "en/",
        INDEX_EN + homepage_after_hero("en"),
        solid=False,
        lang="en",
        alt="",
    ))

    write("en/about.html", wrap(
        "About Talendus | Recruiting platform for every company",
        "Talendus helps companies in every industry hire the right talent. History, mission and how we work.",
        "en/about.html",
        page_hero(
            "The firm",
            "Talendus is a recruiting platform for companies.",
            "We help companies in every industry hire the right talent. Industry, role and location are parameters — never brand limits.",
            actions='<a class="tl-btn" href="candidates.html" data-set-persona="talent">For talent</a><a class="tl-btn tl-btn-ghost" href="employers.html" data-set-persona="entreprise">For employers</a>',
        )
        + f"""
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <h2 class="tl-h2">Why we exist</h2>
    <p class="tl-lead">Too many companies lose weeks looking for the right people, sorting too many resumes, or letting a process drag. We built a platform that simplifies recruiting — for every company, not for one industry.</p>
    <h2 class="tl-h2">What we do</h2>
    <p>We connect employers with the talent they need: developers, accountants, welders, nurses, drivers, HR managers, and many others. A consultant presents the files. Candidates and employers stay on their own side.</p>
    <h2 class="tl-h2">Where we're headed</h2>
    <p>Hire better, faster and more intelligently with AI. Matching, resume analysis and ranking will come. They are not simulated today.</p>
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
      <div class="tl-card"><div class="body"><h3>Every industry</h3><p>Talendus is for every industry. Sector is a search filter, not the brand.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Rigour</h3><p>We assess the role, skills, experience and fit. Not a resume flood.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Word kept</h3><p>Timelines, files, guarantee: what is said is delivered. One consultant through to start date.</p></div></div>
    </div>
    </div></section>
    """
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
            ("technical-recruiting.html", "Trades", "Skilled roles", "Technicians, welders, developers, nurses, accountants — a wide range of profiles."),
            ("temporary-recruiting.html", "Urgent", "Urgent recruiting", "When a critical seat is uncovered. A filtered shortlist, not a resume flood."),
            ("executive-search.html", "Discreet", "Confidential mandates", "Manager replacements or reorganizations run without internal noise."),
            ("employers.html", "HR", "HR support", "Job descriptions, salary grids, joint interviews and onboarding."),
        ]
    )
    write("en/services.html", wrap(
        "Recruiting services | Talendus",
        "Permanent recruiting, search, managers and skilled roles for companies in every industry.",
        "en/services.html",
        page_hero(
            "Services",
            "From the first need to the hire: one contact.",
            "Permanent, temporary, search, leadership and skilled roles. For every company, not for one industry.",
            actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a>',
        )
        + f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    '''
        + ai_coming_soon("en"),
        lang="en",
        alt="services.html",
    ))

    write("en/employers.html", wrap(
        "Employers | Recruiting for every company — Talendus",
        "Hand a hire to Talendus. Post a job, find talent or talk to a recruiter. Every industry.",
        "en/employers.html",
        page_hero(
            "Employers",
            "Find the talent your company needs.",
            "Post a job, describe a need, or talk to a recruiter. Whatever your industry.",
            actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a><a class="tl-btn tl-btn-ghost" href="post-a-job.html">Post a job</a>',
            badges='<span class="tl-badge tl-badge-light">By appointment</span> <span class="tl-badge tl-badge-light">Every industry</span>',
        )
        + proof_stats("en")
        + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Focus</span><h3>Why Talendus</h3><p>We help companies in every industry hire the right talent. Not a firm stuck in one sector.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Timeline</span><h3>Timelines kept</h3><p>First files targeted in 7 days on an operations role. 3 to 8 weeks for supervisors, scarce trades and managers. We say so at the briefing.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Trust</span><h3>Guarantees</h3><p>Replacement included on permanent mandates. Terms confirmed when the file opens. One consultant through to start date.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">How it works</div>
        <h2 class="tl-h2">From the call to the first file</h2>
      </div>
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Call</h3><p>30 minutes to understand the role, industry, headcount and urgency.</p></div>
        <div class="tl-step"><span>02</span><h3>Targeting</h3><p>We activate the network by role, skills and location.</p></div>
        <div class="tl-step"><span>03</span><h3>Screen</h3><p>A Talendus interview before your team loses an hour.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>First files targeted in 7 days. Comparable files, a clear recommendation.</p></div>
        <div class="tl-step"><span>05</span><h3>Follow-up</h3><p>30/60/90 onboarding and replacement guarantee.</p></div>
      </div>
    </div></section>
    <section class="tl-section" id="calculator"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-5"><h2 class="tl-h2">What a bad hire really costs</h2>
        <p class="tl-lead">Estimate the impact of a poor fit: salary, training, overtime and lost productivity. A Talendus mandate almost always costs less than a seat left vacant too long.</p></div>
        <div class="col-lg-6 offset-lg-1">
          <div class="tl-calc">
            <label for="tl-salary">Annual salary for the role ($)</label>
            <input id="tl-salary" type="number" value="55000" min="0">
            <label for="tl-months">Months before the problem is visible</label>
            <input id="tl-months" type="number" value="4" min="1">
            <div class="tl-calc-result">Estimated cost<br><b id="tl-cost">—</b></div>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">What you can do here</div>
        <h2 class="tl-h2">Hire, post, search, support</h2>
      </div>
      <div class="tl-grid-4">
        <a class="tl-card" href="contact.html"><div class="body"><span class="tl-chip orange">Recruiter</span><h3>Talk to a recruiter</h3><p>Hand us the search. Industry, role, headcount, location.</p></div></a>
        <a class="tl-card" href="post-a-job.html"><div class="body"><span class="tl-chip orange">Mandate</span><h3>Post a job</h3><p>Describe the role, contract and urgency. We open sourcing.</p></div></a>
        <a class="tl-card" href="executive-search.html"><div class="body"><span class="tl-chip orange">Passive</span><h3>Find talent</h3><p>Discreet approach of people already in post, every industry.</p></div></a>
        <a class="tl-card" href="hr-solutions.html"><div class="body"><span class="tl-chip orange">HR</span><h3>HR solutions</h3><p>Job descriptions, salary grids, joint interviews and 30/60/90 onboarding.</p></div></a>
      </div>
    </div></section>
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
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker" id="faq">Employer FAQ</div>
        <h2 class="tl-h2">What HR and managers ask</h2>
      </div>
      {faq_html(FAQ_EMPLOYERS_EN)}
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Describe my hiring need</a>
      </div>
    </div></section>
    """,
        lang="en",
        alt="entreprises.html",
    ))

    write("en/candidates.html", wrap(
        "Candidates | Find a job in Quebec — Talendus",
        "Create your profile with Talendus. Openings in every industry: technology, healthcare, finance, manufacturing, retail and more.",
        "en/candidates.html",
        page_hero(
            "Candidates",
            "Find a job without a string of dead-end interviews.",
            "Create your profile. A consultant calls if a mandate fits. We don't blast you to fifteen employers.",
            actions='<a class="tl-btn" href="candidates.html#cv">Create my profile</a><a class="tl-btn tl-btn-ghost" href="jobs.html">Browse jobs</a>',
            badges='<span class="tl-badge tl-badge-light">Free for you</span> <span class="tl-badge tl-badge-light">Every industry</span>',
        )
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
      {faq_html(FAQ_CANDIDATES_EN)}
    </div></section>
    """,
        lang="en",
        alt="candidats.html",
    ))

    write("en/contact.html", wrap(
        "Contact | Talk to a recruiter — Talendus",
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
            <input type="hidden" name="profil" value="Candidate — I am looking for a role">
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
          <form class="tl-form" action="#" method="post" data-form="contact">
            <input type="hidden" name="profil" value="Employer — I am hiring">
            <label>Name</label><input required name="nom">
            <label>Company</label><input required name="entreprise">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Subject</label>
            <select name="objet">
              <option>Talk to a recruiter</option>
              <option>Post a job</option>
              <option>Describe my hiring need</option>
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

    cards = []
    for slug, title, city, cat, typ, sal, shift, req, sector, skills, exp in JOBS_EN:
        cards.append(f'''
    <article class="tl-job-card" data-job="{title} {city} {cat} {typ} {sal} {shift} {sector} {skills} {exp}" data-city="{city}" data-cat="{cat}" data-type="{typ}" data-shift="{shift}" data-salary="{sal}" data-sector="{sector}" data-skills="{skills}" data-exp="{exp}">
      <div class="body">
        <span class="tl-chip orange">{typ}</span><span class="tl-chip">{city}</span>
        <h3><a href="job-{slug}.html">{title}</a></h3>
        <p>{sal} · {shift}</p>
        <a class="tl-split-cta" href="job-{slug}.html" style="color:var(--tl-orange);margin-top:auto;padding-top:14px">View role →</a>
      </div>
    </article>''')
    write("en/jobs.html", wrap(
        "Job openings | Talendus",
        "Openings in every industry: developer, accountant, welder, nurse, driver, forklift operator and more. Filter by industry, role, skills, experience and location.",
        "en/jobs.html",
        page_hero(
            "Job openings", "Browse jobs. Every industry, every role.",
            "Filter by industry, role, skills, experience, location and job type, then apply. A Talendus consultant presents your file to the employer.",
            actions='<a class="tl-btn" href="candidates.html#cv">Create my profile</a>',
            badges='<span class="tl-badge tl-badge-light">Talent pool</span>',
        )
        + f"""
    <section class="tl-section"><div class="container">
      {job_search_filters("en")}
      <div class="tl-grid-3" id="job-list">{''.join(cards)}</div>
      <p class="tl-muted" id="job-empty" hidden>No roles match these filters. Create your profile — we'll contact you when a mandate fits.</p>
    </div></section>
    """,
        lang="en",
        alt="emplois.html",
    ))

    for slug, title, city, cat, typ, sal, shift, req, sector, skills, exp in JOBS_EN:
        write(f"en/job-{slug}.html", wrap(
            f"{title} in {city} | Job — Talendus",
            f"{title} role in {city}, Quebec. {typ}. Apply through Talendus, a recruiting platform for every company.",
            f"en/job-{slug}.html",
            page_hero(
                f"{city} · {typ}", title, f"{sal} · {shift} · Talendus recruiting",
                actions='<a class="tl-btn" href="#postuler">Apply</a>',
                badges='<span class="tl-badge tl-badge-light">Talendus opening</span>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <h2 class="tl-h2">The role</h2>
              <p class="tl-lead">Talendus is recruiting a {title.lower()} for an employer in {city}. Industry: {sector}. Skills: {skills}.</p>
              <h3>Profile</h3>
              <p>{req}</p>
              <h3>What we offer</h3>
              <ul><li>{typ} role</li><li>Pay: {sal}</li><li>Schedule: {shift}</li><li>Talendus support through to hire</li></ul>
              <p><a href="jobs.html">← All openings</a> · <a href="candidates.html">Talent space</a></p>
            </div>
            <div class="col-lg-4 offset-lg-1" id="postuler">
              <h3>Apply</h3>
              <form class="tl-form" data-form="apply" data-job-slug="{slug}"><label>Name</label><input name="name" required>
              <label>Email</label><input type="email" name="email" required>
              <label>Phone</label><input name="phone">
              <label>Resume link</label><input name="resume" placeholder="https://">
              <button class="tl-btn tl-btn-lg" type="submit">Apply</button>
              <div class="tl-success"></div></form>
            </div>
          </div>
        </div></section>
        """,
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
        "Every industry | Recruiting platform — Talendus",
        "Talendus is for every industry. Technology, construction, healthcare, finance, manufacturing, retail and many more.",
        "en/sectors.html",
        page_hero(
            "Every industry", "Talendus is built for every industry.",
            "These industries are examples of what the platform can do, not an exclusive list. Whatever your industry, Talendus helps you find the right talent.",
            actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a>',
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
                actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} This is not an exclusive specialty: Talendus recruits for every company.</p>
              <h2 class="tl-h2">Typical roles</h2>
              <p>Operations, skilled trades, supervision, management — and other profiles depending on the need.</p>
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
            actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a>',
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
          <p>We target profiles by role and skills, validate the fit and present a few files — each one we're ready to stand behind. AI will come later: matching and ranking are not simulated today.</p>
          <p><a href="sectors.html">Every industry</a> · <a href="jobs.html">Job openings</a></p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Talk to a recruiter</a>
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
        page_hero(
            "Candidates", "Your Talendus file.",
            "Profile, resume, applications, messages and interviews. Follow your job search.",
            badges='<span class="tl-badge tl-badge-light">Private space</span>',
        )
        + """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account"></div></div></section>""",
        lang="en",
        alt="espace.html",
        robots="noindex,nofollow",
    ))
    write("en/account-employer.html", wrap(
        "Employer portal | Talendus",
        "Sign in to manage job openings, applications, pipeline and Talendus invoices.",
        "en/account-employer.html",
        page_hero(
            "Employers", "Your hiring workspace.",
            "Jobs, presented files, pipeline and invoices. Follow your hires.",
            badges='<span class="tl-badge tl-badge-light">Private space</span>',
        )
        + """<section class="tl-section tl-portal-section"><div class="container"><div id="tl-account" data-space="employer"></div></div></section>""",
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
        "How it works | Talent path — Talendus",
        "Create your profile, apply, track applications and get contacted by Talendus — free for talent.",
        "en/how-it-works.html",
        page_hero(
            "Talent",
            "From resume to interview, we handle the introduction.",
            "Create your account, upload your resume, apply. Talendus talks to the employer for you. Your contact details never go out on their own.",
            actions='<a class="tl-btn" href="account.html" data-auth-open="register">Create my profile</a>',
        )
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Create your profile</h3><p>Role, skills, region, resume. Five minutes to join the network.</p></div>
        <div class="tl-step"><span>02</span><h3>Apply</h3><p>Open roles or a confidential mandate. We filter before we introduce you.</p></div>
        <div class="tl-step"><span>03</span><h3>Track applications</h3><p>A Talendus consultant is the bridge. No direct employer–candidate messages.</p></div>
        <div class="tl-step"><span>04</span><h3>Get contacted</h3><p>When the role, pay and environment match, we call you.</p></div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="comment-ca-fonctionne.html",
    ))
    write("en/post-a-job.html", wrap(
        "Post a job | Recruiting — Talendus",
        "Post a job opening. Talendus sources, screens and presents files. Every industry.",
        "en/post-a-job.html",
        page_hero(
            "Employers",
            "Describe the role. We start sourcing.",
            "Role, industry, contract, urgency: the clearer it is, the faster we send files. Briefing takes about half an hour.",
            actions='<a class="tl-btn" href="account-employer.html" data-auth-open="register">Post a job</a>',
        )
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Brief</h3><p>30 minutes: role, industry, skills, real pay.</p></div>
        <div class="tl-step"><span>02</span><h3>Framed posting</h3><p>Visible opening or confidential mandate, as you need.</p></div>
        <div class="tl-step"><span>03</span><h3>Talendus filter</h3><p>Applications go through our team. You see presented files.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>First files targeted in 7 days on operations roles.</p></div>
      </div>
    </div></section>
    """
        + human_hire_band("en"),
        lang="en",
        alt="publier-une-offre.html",
    ))
    write("en/hr-solutions.html", wrap(
        "HR solutions | Recruiting support — Talendus",
        "HR support: job descriptions, salary grids, joint interviews and 30/60/90 onboarding. Every industry.",
        "en/hr-solutions.html",
        page_hero(
            "Employers",
            "Build a hiring process, not just plug a hole.",
            "Job descriptions, pay grids, joint interviews and onboarding follow-up — for companies tired of winging it.",
            actions='<a class="tl-btn" href="contact.html">Talk to a recruiter</a>',
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
