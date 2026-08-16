"""English pages for Talendus — native copy, not machine-translated chrome."""

from parts import speed_strip, cta_band, faq_html, proof_stats, FAQ_EMPLOYERS_EN, FAQ_CANDIDATES_EN
from seo_pages import write_en as write_seo_en

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
    ("cariste", "Forklift operator", "Laval", "entrepot", "Permanent", "$22 to $26/hr", "Day shift", "Forklift permit, 1 year warehouse experience, health & safety."),
    ("operateur-production", "Production operator", "Longueuil", "production", "Permanent", "$20 to $24/hr", "Rotating shifts", "Plant experience, ability to follow procedures, teamwork."),
    ("soudeur", "Welder-fitter", "Drummondville", "metallurgie", "Permanent", "$28 to $34/hr", "Day shift", "MIG/TIG welding, blueprint reading, competency cards an asset."),
    ("machiniste-cnc", "CNC machinist", "Saint-Jérôme", "manufacturier", "Permanent", "$30 to $38/hr", "Day shift", "Programming or set-up, drawing reading, 3 years of experience."),
    ("electromecanicien", "Electromechanical technician", "Montreal", "maintenance", "Permanent", "$32 to $40/hr", "Rotating shifts", "Troubleshooting, hydraulics, pneumatics, industrial electricity."),
    ("mecanicien-industriel", "Industrial mechanic", "Sherbrooke", "maintenance", "Permanent", "$30 to $36/hr", "Day shift", "Preventive maintenance, alignment, conveyors, reliability."),
    ("journalier-usine", "Plant labourer", "Boucherville", "production", "Permanent", "$18 to $21/hr", "Evening shift", "Physical fitness, punctuality, on-the-job training provided."),
    ("superviseur-production", "Production supervisor", "Trois-Rivières", "supervision", "Permanent", "$70,000 to $85,000", "Day shift", "Team leadership, KPIs, Lean, 5 years on the plant floor."),
    ("coordonnateur-logistique", "Logistics coordinator", "Anjou", "logistique", "Permanent", "$55,000 to $68,000", "Day shift", "WMS, planning, English an asset."),
    ("directeur-usine", "Plant manager", "Quebec City", "cadres", "Permanent", "$120,000 to $150,000", "Day shift", "P&L, Lean, managing a 100+ employee plant. Confidential mandate."),
]

SECTORS_EN = [
    ("manufacturier", "Manufacturing", "Manufacturing recruitment in Quebec", "Fabrication, assembly and industrial subcontracting plants. We place operators, trades and plant leaders."),
    ("production", "Production", "Production recruitment in Quebec", "Lines, methods, quality and supervision. People who can hold a shift and a standard."),
    ("entrepot", "Warehousing", "Warehouse recruitment Quebec", "Forklift operators, pickers, clerks and warehouse supervisors for distribution centres."),
    ("logistique", "Logistics", "Logistics recruitment Quebec", "Planning, internal transport, WMS and supply-chain coordination."),
    ("distribution", "Distribution", "Distribution recruitment Quebec", "Distribution centres, shipping, receiving and inventory management."),
    ("transport", "Transportation", "Transportation and logistics recruiting", "Transport coordination, plant shipping and industrial flow roles."),
    ("transformation-alimentaire", "Food processing", "Industrial food recruitment Quebec", "Food plants: hygiene, shifts, operators and production supervision."),
    ("metallurgie", "Metals", "Metals and welding recruitment Quebec", "Welding, machining, metal fabrication and boilermaking."),
    ("plasturgie", "Plastics", "Plastics recruitment Quebec", "Injection, extrusion, press set-up and process technicians."),
    ("maintenance", "Industrial maintenance", "Industrial maintenance recruitment Quebec", "Electromechanical technicians, industrial mechanics and reliability leads."),
]

ARTICLES_EN = [
    ("mauvaise-embauche", "What a bad plant hire really costs", "HR", "usine-equipe.jpg",
     "A poor fit on the floor is more than a salary. Training, overtime, scrap and turnover add up fast."),
    ("machiniste-cnc", "Hiring a CNC machinist in Quebec in 2026", "Manufacturing", "cnc-machiniste.jpg",
     "The CNC machinist is one of the tightest profiles. Here is how to attract, assess and keep this scarce talent."),
    ("caristes-entrepot", "Forklift shortage: tactics for warehouses", "Logistics", "entrepot-logistique.jpg",
     "Distribution centres compete for experienced operators. Three practical levers to secure your shifts."),
    ("superviseur-production", "Production supervisor: the profile that steadies a plant", "Production", "usine-equipe.jpg",
     "A strong supervisor stabilizes the shift, quality and climate. Here is the portrait we validate on the floor."),
    ("roulement-manufacturier", "Cutting turnover in manufacturing recruiting", "Recruiting", "soudeur-atelier.jpg",
     "Turnover is not only a pay problem. Onboarding, shifts and cultural fit make the difference."),
]

TOPICS_EN = [
    "Welder pay in Quebec", "Urgent plant hiring", "Competency cards and health & safety",
    "Evening shift: how to hire", "Plant manager search", "WMS and warehouse profiles",
    "Lean manufacturing and recruiting", "30/60/90 onboarding on the floor", "Electromechanical talent scarcity",
    "Regional hiring vs Greater Montreal", "Manufacturing employer brand", "Technical tests in interviews",
    "Food production attendants", "Seasonal warehouse contracts", "Retaining skilled trades",
    "Cost of a vacant production seat", "Hiring newcomers in plants", "Automation and new trades",
    "Replacement guarantee FAQ", "Preparing a supervisor interview",
]


INDEX_EN = rf"""
<div class="hero2-arrow-hero tl-gateway-hero">
  <div class="hero2-slider-area">
        <div class="img1"><img src="{img('usine-equipe.jpg')}" alt="Production team on a Quebec plant floor" fetchpriority="high" decoding="async"></div>
        <div class="container">
            <div class="hero2-heading tl-hero-lock">
                <h5>Industrial recruiting in Quebec</h5>
                <div class="space16"></div>
                <h1>Looking for plant work, or someone to cover a shift?</h1>
                <div class="space16"></div>
                <p>Talendus hires for plants, warehouses and shop-floor trades. Tell us which side you're on — we'll take you to the right page.</p>
            </div>
            <div class="tl-persona-cards">
              <a class="tl-persona-card is-talent" href="candidates.html" data-set-persona="talent">
                <span class="tl-kicker">Candidate</span>
                <h2>I'm looking for a job</h2>
                <p>Browse openings, upload your resume, track applications. It's free. A consultant presents your file to employers.</p>
                <span class="tl-persona-go">See jobs <i class="fa-solid fa-arrow-right"></i></span>
              </a>
              <a class="tl-persona-card is-hire" href="employers.html" data-set-persona="entreprise">
                <span class="tl-kicker">Employer</span>
                <h2>I'm hiring</h2>
                <p>Tell us the role, the shift and the pay. We screen, we send files, we stay on it through start date.</p>
                <span class="tl-persona-go">Request a hire <i class="fa-solid fa-arrow-right"></i></span>
              </a>
            </div>
        </div>
  </div>
</div>
"""


def build_en(write, wrap, page_hero):
    write("en/index.html", wrap(
        "Talendus | Industrial and manufacturing recruitment in Quebec",
        "Talendus hires for Quebec plants: production, maintenance, logistics and supervision. Candidates on one side, employers on the other. Call by appointment.",
        "en/",
        INDEX_EN,
        solid=False,
        lang="en",
        alt="",
    ))

    write("en/about.html", wrap(
        "About Talendus | Industrial recruiting firm in Quebec",
        "History, mission, vision and values of Talendus, a recruiting partner for operational companies in Quebec.",
        "en/about.html",
        page_hero(
            "The firm",
            "Talendus recruits for Quebec industry. That's it.",
            "We hire the people who keep production, maintenance, logistics and supervision running. Not office. Not IT.",
            actions='<a class="tl-btn" href="candidates.html" data-set-persona="talent">For talent</a><a class="tl-btn tl-btn-ghost" href="employers.html" data-set-persona="entreprise">For employers</a>',
        )
        + f"""
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <h2 class="tl-h2">Why we exist</h2>
    <p class="tl-lead">Too many plants lose weeks with generalist agencies that cannot tell a CNC set-up from a desk job. We built a firm that speaks shifts, health &amp; safety and line pace — and stops there.</p>
    <h2 class="tl-h2">What we do</h2>
    <p>We connect Quebec plant employers with operators, skilled trades, supervisors and plant leaders who can actually hold the floor.</p>
    <h2 class="tl-h2">Where we're headed</h2>
    <p>Become the first call when a plant needs to hire well. A network that stays industrial, not a catch-all catalogue.</p>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="{img('usine-equipe.jpg')}" alt="Talendus team on the plant floor">
      </div>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">How we work</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Specialization</h3><p>No mandates outside industry. That's the filter. It keeps a forklift operator from sitting next to an admin assistant.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Floor-level rigour</h3><p>We assess like a supervisor, not like an algorithm. Skills, shift, health &amp; safety, attitude.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Word kept</h3><p>Timelines, files, guarantee: what is said is delivered. One consultant through to start date.</p></div></div>
    </div>
    </div></section>
    """,
        lang="en",
        alt="a-propos.html",
    ))

    services_cards = "".join(
        f'<a class="tl-card" href="{href}"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></a>'
        for href, chip, t, p in [
            ("permanent-recruiting.html", "Permanent", "Permanent recruiting", "Stable roles in plants, warehouses and manufacturing leadership. Success fees, replacement guarantee."),
            ("executive-search.html", "Passive", "Search mandates", "Direct approach of passive candidates for scarce profiles: CNC, electromechanics, plant leaders."),
            ("leadership-recruiting.html", "Leadership", "Manager recruiting", "Plant, production, maintenance and logistics managers. Often confidential."),
            ("industrial-recruiting.html", "Shift", "Supervisor recruiting", "Forepersons and shift supervisors who can hold KPIs, health & safety and team climate."),
            ("technical-recruiting.html", "Trades", "Skilled trades", "Welders, machinists, industrial mechanics, electromechanical technicians, set-up, quality."),
            ("temporary-recruiting.html", "Urgent", "Urgent recruiting", "Accelerated process when a critical shift is uncovered. A filtered shortlist, not a resume flood."),
            ("executive-search.html", "Discreet", "Confidential mandates", "Manager replacements or reorganizations run without internal noise."),
            ("employers.html", "HR", "HR support", "Job descriptions, industrial salary grids, joint interviews and onboarding."),
        ]
    )
    write("en/services.html", wrap(
        "Industrial recruiting services | Talendus Quebec",
        "Permanent recruiting, search, managers, supervisors and skilled trades for Quebec operations.",
        "en/services.html",
        page_hero(
            "Services",
            "From labourer to plant manager: one firm.",
            "Permanent, temporary, search, leadership and trades. All of it for the floor, not for a head office.",
            actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
        )
        + f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    ''',
        lang="en",
        alt="services.html",
    ))

    write("en/employers.html", wrap(
        "Employers | Manufacturing and industrial recruiting in Quebec — Talendus",
        "Request a hire with Talendus. Industrial screening and a replacement guarantee for Quebec operations.",
        "en/employers.html",
        page_hero(
            "Employers",
            "Fill a shift with people who can hold the floor.",
            "Tell us the trade, real pay and how urgent it is. You get a screened shortlist — not a stack of resumes.",
            actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
            badges='<span class="tl-badge tl-badge-light">By appointment</span> <span class="tl-badge tl-badge-light">Plant firm</span>',
        )
        + proof_stats("en")
        + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Focus</span><h3>Why Talendus</h3><p>A firm built for plants. Network of people already in post, technical assessment and onboarding follow-up. Not an agency that also fills admin desks.</p></div></div>
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
        <div class="tl-step"><span>01</span><h3>Call</h3><p>30 minutes to understand the shift, real pay and urgency.</p></div>
        <div class="tl-step"><span>02</span><h3>Targeting</h3><p>We activate the network and plant references.</p></div>
        <div class="tl-step"><span>03</span><h3>Floor filter</h3><p>A Talendus interview before your supervisor loses an hour.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>First files targeted in 7 days. Comparable files, a clear recommendation.</p></div>
        <div class="tl-step"><span>05</span><h3>Follow-up</h3><p>30/60/90 onboarding and replacement guarantee.</p></div>
      </div>
    </div></section>
    <section class="tl-section" id="calculator"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-5"><h2 class="tl-h2">What a bad hire really costs</h2>
        <p class="tl-lead">Estimate the impact of a poor fit: salary, training, overtime and lost productivity. A Talendus mandate almost always costs less than an unstable shift.</p></div>
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
        <a class="tl-card" href="employers.html"><div class="body"><span class="tl-chip orange">Services</span><h3>Hire with Talendus</h3><p>Industrial screening, a short shortlist, replacement guarantee.</p></div></a>
        <a class="tl-card" href="post-a-job.html"><div class="body"><span class="tl-chip orange">Mandate</span><h3>Post a job</h3><p>Describe the shift, real pay and urgency. We open sourcing.</p></div></a>
        <a class="tl-card" href="executive-search.html"><div class="body"><span class="tl-chip orange">Passive</span><h3>Talent search</h3><p>Discreet approach of people already in post: CNC, electromechanics, leaders.</p></div></a>
        <a class="tl-card" href="hr-solutions.html"><div class="body"><span class="tl-chip orange">HR</span><h3>HR solutions</h3><p>Job descriptions, salary grids, joint interviews and 30/60/90 onboarding.</p></div></a>
      </div>
    </div></section>
    <section class="tl-section tl-ice" id="temoignages"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">Employer testimonials</div>
        <h2 class="tl-h2">What plants say</h2>
      </div>
      <div class="tl-grid-3 tl-quotes">
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>They understood our rotating shifts on the first call. The supervisor they presented already knew a comparable Lean environment.</p>
          <footer><strong>M.L.</strong><span>Director of operations · food plant, South Shore</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>Not an agency that sends 40 resumes. Three solid files, an electromechanical technician in post, and follow-up after the hire.</p>
          <footer><strong>J.R.</strong><span>Maintenance director · metals, Mauricie</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>A confidential plant-manager mandate run without internal noise. Start date aligned with our production calendar.</p>
          <footer><strong>S.B.</strong><span>VP operations · manufacturer, Montérégie</span></footer>
        </blockquote>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker" id="faq">Employer FAQ</div>
        <h2 class="tl-h2">What HR and operations directors ask</h2>
      </div>
      {faq_html(FAQ_EMPLOYERS_EN)}
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Request a hire</a>
      </div>
    </div></section>
    """,
        lang="en",
        alt="entreprises.html",
    ))

    write("en/candidates.html", wrap(
        "Candidates | Plant, warehouse and skilled-trade jobs in Quebec — Talendus",
        "Submit your resume to Talendus. Roles in plants, warehouses, logistics, maintenance and supervision in Quebec.",
        "en/candidates.html",
        page_hero(
            "Candidates",
            "Land a plant job without a string of dead-end interviews.",
            "Upload your resume. A consultant calls if a mandate fits. We don't blast you to fifteen employers.",
            actions='<a class="tl-btn" href="candidates.html#cv">Submit my resume</a>',
            badges='<span class="tl-badge tl-badge-light">Free for you</span> <span class="tl-badge tl-badge-light">Real plant mandates</span>',
        )
        + f"""
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Submit your resume</h2>
          <p class="tl-lead">Tell us your trade, possible shifts and region. A consultant calls if a mandate fits. We don't send you to fifteen interviews for nothing.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">On weekdays we usually reply within 30 minutes.</div>
          <p id="process"></p>
          <h3>How it works</h3>
          <ol>
            <li>Create your profile.</li>
            <li>Apply to openings or submit your resume.</li>
            <li>Track applications with a Talendus consultant.</li>
            <li>We contact you when the shift and pay match.</li>
          </ol>
        </div>
        <div class="col-lg-6 offset-lg-1">
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Name</label><input required name="nom">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Target trade</label>
            <select name="metier">
              <option>Forklift operator</option><option>Production operator</option><option>Welder</option>
              <option>CNC machinist</option><option>Electromechanical technician</option><option>Supervisor</option>
              <option>Other industrial trade</option>
            </select>
            <label>Region</label><input name="region" placeholder="Laval, Montérégie, Quebec City…">
            <label>Link to your resume (Drive, Dropbox…)</label><input name="cv" placeholder="https://">
            <button class="tl-btn tl-btn-lg" type="submit">Submit my resume</button>
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
          <p>Not fifteen useless interviews. A consultant understood my shifts, then introduced me to a plant actually hiring a welder-fitter.</p>
          <footer><strong>K.T.</strong><span>Welder placed · Drummondville</span></footer>
        </blockquote>
        <blockquote class="tl-quote">
          <div class="tl-quote-mark" aria-hidden="true">“</div>
          <p>I submitted my resume on a Tuesday. Friday I had an electromechanical interview in Montreal. Free, no pressure.</p>
          <footer><strong>R.M.</strong><span>Electromechanical technician · Montreal</span></footer>
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
        "Contact | Industrial recruiting call Quebec — Talendus",
        "Contact Talendus in Montreal. Calls by appointment. On weekdays we usually reply within 30 minutes. 514 555-0199 · info@talendus.ca",
        "en/contact.html",
        page_hero(
            "Contact",
            "Write to us. We'll call you back.",
            "Looking for a job, or filling a seat? Pick your door — the form follows.",
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
            <p>Submit your resume or ask about a plant role. It's free.</p>
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
          <p class="tl-lead">It's free. A consultant calls if a plant mandate matches.</p>
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
            <label>Message</label><textarea required name="message" placeholder="Trade, city, possible shifts"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Submit my resume</button>
            <div class="tl-success"></div>
          </form>
        </div>
        <div data-persona-only="entreprise">
          <div class="tl-kicker">Employers</div>
          <h2 class="tl-h2">Request a hire</h2>
          <p class="tl-lead">Describe the role, shift and urgency. Free call, by appointment.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <input type="hidden" name="profil" value="Employer — I am hiring">
            <label>Name</label><input required name="nom">
            <label>Company</label><input required name="entreprise">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Subject</label>
            <select name="objet">
              <option>Request a hire</option>
              <option>Post a job</option>
              <option>Book a call</option>
            </select>
            <label>Message</label><textarea required name="message" placeholder="Role, city, shift, urgency"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Request a hire</button>
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
    for slug, title, city, cat, typ, sal, shift, req in JOBS_EN:
        cards.append(f'''
    <article class="tl-job-card" data-job="{title} {city} {cat} {typ} {sal} {shift}" data-city="{city}" data-cat="{cat}" data-type="{typ}" data-shift="{shift}" data-salary="{sal}">
      <div class="body">
        <span class="tl-chip orange">{typ}</span><span class="tl-chip">{city}</span>
        <h3><a href="job-{slug}.html">{title}</a></h3>
        <p>{sal} · {shift}</p>
        <a class="tl-split-cta" href="job-{slug}.html" style="color:var(--tl-orange);margin-top:auto;padding-top:14px">View role →</a>
      </div>
    </article>''')
    write("en/jobs.html", wrap(
        "Plant and warehouse jobs in Quebec | Talendus",
        "Forklift, operator, welder, CNC machinist, electromechanical technician, supervisor and plant manager roles in Quebec.",
        "en/jobs.html",
        page_hero(
            "Job openings", "Openings in plants, maintenance and warehousing.",
            "Filter by trade and region, then apply. A Talendus consultant presents your file to the employer.",
            actions='<a class="tl-btn" href="candidates.html#cv">Submit my resume</a>',
            badges='<span class="tl-badge tl-badge-light">Talent pool</span>',
        )
        + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-filters">
        <input id="job-search" placeholder="Search a trade, a city…">
        <select id="job-cat">
          <option value="">All categories</option>
          <option value="production">Production</option>
          <option value="entrepot">Warehouse</option>
          <option value="logistique">Logistics</option>
          <option value="maintenance">Maintenance</option>
          <option value="metallurgie">Metals</option>
          <option value="supervision">Supervision</option>
          <option value="cadres">Leadership</option>
        </select>
        <select id="job-city">
          <option value="">All cities</option>
          <option>Laval</option><option>Longueuil</option><option>Montreal</option>
          <option>Drummondville</option><option>Saint-Jérôme</option>
          <option>Sherbrooke</option><option>Boucherville</option>
          <option>Anjou</option><option>Trois-Rivières</option><option>Quebec City</option>
        </select>
        <select id="job-type">
          <option value="">All types</option>
          <option value="Permanent">Permanent</option>
          <option value="Temporary">Temporary</option>
        </select>
        <select id="job-shift">
          <option value="">All shifts</option>
          <option value="Day shift">Day shift</option>
          <option value="Evening shift">Evening shift</option>
          <option value="Rotating shifts">Rotating shifts</option>
        </select>
        <select id="job-sal">
          <option value="">All salaries</option>
          <option value="18">$18/hr and up</option>
          <option value="25">$25/hr and up</option>
          <option value="30">$30/hr and up</option>
          <option value="50000">$50,000 and up</option>
        </select>
      </div>
      <div class="tl-grid-3" id="job-list">{''.join(cards)}</div>
      <p class="tl-muted" id="job-empty" hidden>No roles match these filters. Submit your resume — we'll contact you when a mandate fits.</p>
    </div></section>
    """,
        lang="en",
        alt="emplois.html",
    ))

    for slug, title, city, cat, typ, sal, shift, req in JOBS_EN:
        write(f"en/job-{slug}.html", wrap(
            f"{title} in {city} | Industrial job Quebec — Talendus",
            f"{title} role in {city}, Quebec. {typ}. Apply through Talendus, industrial recruiting firm.",
            f"en/job-{slug}.html",
            page_hero(
                f"{city} · {typ}", title, f"{sal} · {shift} · Talendus industrial recruiting",
                actions='<a class="tl-btn" href="#postuler">Apply</a>',
                badges='<span class="tl-badge tl-badge-light">Industrial role</span>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <h2 class="tl-h2">The role</h2>
              <p class="tl-lead">Talendus is recruiting a {title.lower()} for a plant or logistics employer in {city}. A real floor: health &amp; safety, production pace, shifts.</p>
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
        "Industries | Industrial recruiting Quebec — Talendus",
        "Talendus recruits in manufacturing, production, warehousing, logistics, food, metals, plastics and maintenance in Quebec.",
        "en/sectors.html",
        page_hero(
            "Industries", "Pick your type of plant.",
            "Manufacturing, warehousing, food, metals, maintenance: we already speak your language.",
            actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
        )
        + f'<section class="tl-section"><div class="container"><div class="tl-grid-3">{sec_cards}</div></div></section>',
        lang="en",
        alt="secteurs.html",
    ))
    for slug, name, title, desc in SECTORS_EN:
        write(f"en/sector-{slug}.html", wrap(
            f"{title} | Talendus",
            desc,
            f"en/sector-{slug}.html",
            page_hero(
                "Industry", name, desc,
                actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} We don't send desk profiles: only people who have already lived a plant floor or a receiving dock.</p>
              <h2 class="tl-h2">Typical roles</h2>
              <p>Operations, skilled trades, supervision and leadership depending on site size.</p>
              <div class="tl-actions" style="margin-top:24px">
                <a class="tl-btn" href="contact.html">Open a {name.lower()} mandate</a>
                <a class="tl-btn tl-btn-ghost-dark" href="sectors.html">All industries</a>
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
        "Industrial recruiting, HR and manufacturing blog Quebec | Talendus",
        "SEO articles on manufacturing recruiting, logistics, warehouses and skilled trades in Quebec.",
        "en/blog.html",
        page_hero(
            "Blog", "Recruiting, HR, plants, logistics and careers.",
            "Useful writing for plant employers and candidates. No filler.",
            actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
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
          <h2>What we see in Quebec</h2>
          <p>Plants and distribution centres do not hire like a services head office. Shifts, health &amp; safety, competency cards and floor culture weigh as much as the resume. A six-week vacancy often costs more than a well-scoped recruiting mandate.</p>
          <h2>Practical moves</h2>
          <ul>
            <li>Clarify the shift, real pay and bonuses before approaching the market.</li>
            <li>Assess know-how (demonstration, scenarios) rather than diplomas alone.</li>
            <li>Plan 30/60/90-day onboarding: that is where retention is won.</li>
          </ul>
          <h2>How Talendus steps in</h2>
          <p>We target industrial profiles, validate shift fit and present a few files — each one we're ready to stand behind.</p>
          <p><a href="industrial-recruiting.html">Industrial recruiting</a> · <a href="jobs.html">Job openings</a></p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Request a hire</a>
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
            "Profile, resume, applications, messages and interviews. Follow your plant job search.",
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
            "Jobs, presented files, pipeline and invoices. Follow your plant mandates.",
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
        <div class="tl-step"><span>01</span><h3>Create your profile</h3><p>Trade, shifts, region, resume. Five minutes to join the network.</p></div>
        <div class="tl-step"><span>02</span><h3>Apply</h3><p>Open roles or a confidential mandate. We filter before we introduce you.</p></div>
        <div class="tl-step"><span>03</span><h3>Track applications</h3><p>A Talendus consultant is the bridge. No direct employer–candidate messages.</p></div>
        <div class="tl-step"><span>04</span><h3>Get contacted</h3><p>When the shift, pay and plant match, we call you.</p></div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="comment-ca-fonctionne.html",
    ))
    write("en/post-a-job.html", wrap(
        "Post a job | Industrial recruiting — Talendus",
        "Post a plant or warehouse job in Quebec. Talendus sources, screens and presents files.",
        "en/post-a-job.html",
        page_hero(
            "Employers",
            "Describe the role. We start sourcing.",
            "Shift, pay, urgency: the clearer it is, the faster we send files. Briefing takes about half an hour.",
            actions='<a class="tl-btn" href="account-employer.html" data-auth-open="register">Post a job</a>',
        )
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Brief</h3><p>30 minutes: role, shift, health &amp; safety, real pay.</p></div>
        <div class="tl-step"><span>02</span><h3>Framed posting</h3><p>Visible opening or confidential mandate, as you need.</p></div>
        <div class="tl-step"><span>03</span><h3>Talendus filter</h3><p>Applications go through our team. You see presented files.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>First files targeted in 7 days on operations roles.</p></div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="publier-une-offre.html",
    ))
    write("en/hr-solutions.html", wrap(
        "HR solutions | Industrial recruiting support — Talendus",
        "HR support for Quebec plants: job descriptions, salary grids, joint interviews and 30/60/90 onboarding.",
        "en/hr-solutions.html",
        page_hero(
            "Employers",
            "Build a hiring process, not just plug a hole.",
            "Job descriptions, pay grids, joint interviews and onboarding follow-up — for plants tired of winging it.",
            actions='<a class="tl-btn" href="contact.html">Request a hire</a>',
        )
        + """
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><h3>Industrial descriptions</h3><p>A role written as a shift is lived: machines, health &amp; safety, pace, supervision.</p></div></div>
        <div class="tl-card"><div class="body"><h3>Salary grids</h3><p>Align the offer with Quebec plant pay, without underpaying a scarce trade.</p></div></div>
        <div class="tl-card"><div class="body"><h3>30/60/90 onboarding</h3><p>Follow-up after start date. Replacement guarantee on permanent mandates.</p></div></div>
      </div>
    </div></section>
    """,
        lang="en",
        alt="solutions-rh.html",
    ))
    write_seo_en(write, wrap, page_hero, CTA)
