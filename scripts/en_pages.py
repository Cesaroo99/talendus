"""English pages for Talendus — native copy, not machine-translated chrome."""

from parts import speed_strip, cta_band, faq_html, FAQ_HOME_EN, FAQ_EMPLOYERS_EN, FAQ_CANDIDATES_EN

A = "../assets/"
SPEED = speed_strip("en")
CTA = cta_band("en")
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
<div class="hero2-arrow-hero">
    <div class="hero-main-slider">
      <div class="hero2-slider-area">
        <div class="img1"><img src="{img('usine-equipe.jpg')}" alt="Production team on a Quebec plant floor"></div>
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="hero2-heading tl-hero-lock">
                        <h5>The talent that keeps industry moving.</h5>
                        <div class="space16"></div>
                        <h1>Qualified candidates from day 7.</h1>
                        <div class="space16"></div>
                        <p>A recruiting partner for Quebec operations — production, maintenance, logistics, supervision and business continuity.</p>
                        <div class="space32"></div>
                        <div class="btn-area1">
                            <a href="contact.html" class="vl-btn2">Start a hire <span><i class="fa-solid fa-arrow-right"></i></span></a>
                            <a href="candidates.html#cv" class="vl-btn2 btn2">Submit my resume <span><i class="fa-solid fa-arrow-right"></i></span></a>
                        </div>
                        <div class="tl-hero-badges">
                          <span class="tl-badge tl-badge-light">Operations · Quebec</span>
                          <span class="tl-badge tl-badge-light">Consultation by appointment</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="hero2-slider-area">
        <div class="img1"><img src="{img('entrepot-logistique.jpg')}" alt="Logistics warehouse and forklift operators in Quebec"></div>
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="hero2-heading tl-hero-lock">
                        <h5>Industrial jobs · Quebec</h5>
                        <div class="space16"></div>
                        <h1>Find plant work in Quebec, presented to the right employers.</h1>
                        <div class="space16"></div>
                        <p>Operator, forklift, welder, CNC, maintenance, supervision: we introduce you to operations that are actually hiring.</p>
                        <div class="space32"></div>
                        <div class="btn-area1">
                            <a href="jobs.html" class="vl-btn2">Browse jobs <span><i class="fa-solid fa-arrow-right"></i></span></a>
                            <a href="candidates.html#cv" class="vl-btn2 btn2">Submit my resume <span><i class="fa-solid fa-arrow-right"></i></span></a>
                        </div>
                        <div class="tl-hero-badges">
                          <span class="tl-badge tl-badge-light">Free for candidates</span>
                          <span class="tl-badge tl-badge-light">Real plant mandates</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    <div class="testimonial-arrow">
     <div class="prev-arrow-hero">
        <button type="button" aria-label="Next slide"><i class="fa-solid fa-arrow-right"></i></button>
        </div>
        <div class="next-arrow-hero">
        <button type="button" aria-label="Previous slide"><i class="fa-solid fa-arrow-left"></i></button>
        </div>
    </div>
</div>
<section class="tl-section-sm">
  <div class="container">
    <div class="tl-split">
      <a class="employeurs" href="employers.html">
        <div class="tl-kicker" style="color:#ffb37a">Employers</div>
        <h3>Need talent who can hold production, logistics or maintenance?</h3>
        <p>Free consultation, by appointment. Screening built around your shift — not 80 resumes to sort at the end of the day.</p>
        <span class="tl-split-cta">Start a hire →</span>
      </a>
      <a class="candidats" href="candidates.html">
        <div class="tl-kicker" style="color:#cfe0ff">Candidates</div>
        <h3>A role in production, logistics or maintenance?</h3>
        <p>Submit your resume. We introduce you to operational employers in Quebec — not catch-all mandates.</p>
        <span class="tl-split-cta">Submit my resume →</span>
      </a>
    </div>
  </div>
</section>
<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Key figures</div>
      <h2 class="tl-h2">A firm built for the reality of Quebec operations</h2>
    </div>
    <div class="tl-stats">
      <div class="tl-stat"><b>7 d</b><p>Qualified candidates from day 7 on operations mandates</p></div>
      <div class="tl-stat"><b>92 %</b><p>Of placements still in post after the probation period</p></div>
      <div class="tl-stat"><b>100 %</b><p>Of our mandates in industry, logistics or operations</p></div>
      <div class="tl-stat"><b>1,200+</b><p>Industrial talents active in our Quebec network</p></div>
    </div>
  </div>
</section>
<section class="tl-section">
  <div class="container">
    <div class="row align-items-center g-4">
      <div class="col-lg-6">
        <div class="tl-kicker">Why Talendus</div>
        <h2 class="tl-h2">The talent-acquisition partner for Quebec industry</h2>
        <p class="tl-lead">When a line, a dock or a shift stops, the cost is not a vacant seat: it is lost production. We speak operations, maintenance, logistics and supervision — not generic HR language.</p>
        <div class="space24"></div>
        <ul class="tl-muted">
          <li>Focus: production, manufacturing, logistics, maintenance, transportation and supervision.</li>
          <li>Floor-level assessment: skills, shift, operational culture.</li>
          <li>Replacement guarantee on permanent mandates.</li>
        </ul>
        <div class="space32"></div>
        <div class="tl-actions">
          <a href="contact.html" class="tl-btn">Start a hire</a>
          <a href="about.html" class="tl-btn tl-btn-ghost-dark">Our approach</a>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="tl-hero-media" style="height:420px;border-radius:18px;overflow:hidden">
          <img src="{img('cnc-machiniste.jpg')}" alt="CNC machinist in a Quebec plant">
        </div>
      </div>
    </div>
  </div>
</section>
<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Industries we serve</div>
      <h2 class="tl-h2">We recruit where Quebec produces, processes, ships and maintains</h2>
    </div>
    <div class="tl-grid-4">
      <a class="tl-card" href="sector-manufacturier.html"><div class="body"><h3>Manufacturing</h3><p>Fabrication, assembly and industrial subcontracting plants.</p></div></a>
      <a class="tl-card" href="sector-production.html"><div class="body"><h3>Production</h3><p>Operations, methods, quality and line supervision.</p></div></a>
      <a class="tl-card" href="sector-entrepot.html"><div class="body"><h3>Warehousing</h3><p>Material handling, forklift operators, order picking and WMS.</p></div></a>
      <a class="tl-card" href="sector-logistique.html"><div class="body"><h3>Logistics</h3><p>Distribution, internal transport and the supply chain.</p></div></a>
      <a class="tl-card" href="sector-transformation-alimentaire.html"><div class="body"><h3>Food</h3><p>Processing, packaging and plant hygiene standards.</p></div></a>
      <a class="tl-card" href="sector-metallurgie.html"><div class="body"><h3>Metals</h3><p>Welding, machining, metal fabrication and boilermaking.</p></div></a>
      <a class="tl-card" href="sector-plasturgie.html"><div class="body"><h3>Plastics</h3><p>Injection, extrusion and press operation.</p></div></a>
      <a class="tl-card" href="sector-maintenance.html"><div class="body"><h3>Maintenance</h3><p>Electromechanics, industrial mechanics and reliability.</p></div></a>
    </div>
  </div>
</section>
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Roles we fill</div>
      <h2 class="tl-h2">From plant labourer to plant manager</h2>
    </div>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Production</span><h3>Plant roles</h3><p>Labourer, operator, assembler, packer, line attendant.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Skilled</span><h3>Technical trades</h3><p>Welder, CNC machinist, electromechanical technician, industrial mechanic.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Logistics</span><h3>Warehouse &amp; distribution</h3><p>Forklift operator, clerk, logistics coordinator, warehouse supervisor.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Supervision</span><h3>Front-line leadership</h3><p>Production supervisor, foreperson, shift team lead.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Managers</span><h3>Plant leadership</h3><p>Plant manager, production director, maintenance manager.</p></div></div>
      <div class="tl-card"><div class="body"><span class="tl-chip orange">Urgent</span><h3>Shift coverage</h3><p>Accelerated mandates when a critical shift must be filled — without diluting the technical filter.</p></div></div>
    </div>
    <div class="tl-center" style="margin-top:28px"><a class="tl-btn" href="jobs.html">Browse jobs</a></div>
  </div>
</section>
<section class="tl-section tl-dark">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Method</div>
      <h2 class="tl-h2">A five-step process aligned with your production clock</h2>
    </div>
    <div class="tl-steps">
      <div class="tl-step"><span>01</span><h3>Operations diagnostic</h3><p>Shift, skills, health &amp; safety, culture and the real urgency of the mandate.</p></div>
      <div class="tl-step"><span>02</span><h3>Industrial targeting</h3><p>Passive network, plant references and direct approach.</p></div>
      <div class="tl-step"><span>03</span><h3>Floor-level assessment</h3><p>Technical interviews, checks and skills tests.</p></div>
      <div class="tl-step"><span>04</span><h3>Presentation</h3><p>Comparable files, a clear recommendation. Qualified candidates from day 7.</p></div>
      <div class="tl-step"><span>05</span><h3>Onboarding</h3><p>30/60/90-day follow-up and replacement guarantee.</p></div>
    </div>
  </div>
</section>
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Case work</div>
      <h2 class="tl-h2">Industrial mandates taken through to start date</h2>
    </div>
    <div class="tl-grid-3">
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="{img('soudeur-atelier.jpg')}" alt="Welder recruiting mandate"></div>
        <div class="body">
          <span class="tl-chip">Metals · Drummondville</span>
          <h3>3 welder-fitters for a second shift</h3>
          <p>A growing SME had to open a shift without stopping the line. Technical screening, a controlled start.</p>
        </div>
      </article>
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="{img('entrepot-logistique.jpg')}" alt="Distribution centre recruiting"></div>
        <div class="body">
          <span class="tl-chip">Warehouse · Laval</span>
          <h3>Shift supervisor + 8 forklift operators</h3>
          <p>Seasonal peak absorbed in 4 weeks, with retention above the site average.</p>
        </div>
      </article>
      <article class="tl-case">
        <div class="tl-hero-media" style="height:200px"><img src="{img('maintenance-tech.jpg')}" alt="Plant manager recruiting"></div>
        <div class="body">
          <span class="tl-chip">Leadership · Montérégie</span>
          <h3>Confidential plant manager</h3>
          <p>Discreet search. Start date in 9 weeks, without internal disruption.</p>
        </div>
      </article>
    </div>
  </div>
</section>
<section class="tl-section tl-ice">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">Testimonials</div>
      <h2 class="tl-h2">What plants and candidates say</h2>
      <p class="tl-lead">Feedback from manufacturing employers and professionals placed in Quebec — not generic quotes.</p>
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
        <p>I was a night forklift operator. Talendus introduced me to a logistics coordinator role in Laval. Clear interview, clean terms.</p>
        <footer><strong>A.D.</strong><span>Candidate placed · Laval</span></footer>
      </blockquote>
    </div>
  </div>
</section>
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
      <div class="tl-kicker">FAQ</div>
      <h2 class="tl-h2">Before you open a mandate or submit a resume</h2>
      <p class="tl-lead">Questions from HR, operations directors and candidates — straight answers.</p>
    </div>
    {faq_html(FAQ_HOME_EN)}
  </div>
</section>
<section class="tl-section tl-ice" id="contact-rapide">
  <div class="container">
    <div class="row align-items-center g-4">
      <div class="col-lg-5">
        <div class="tl-kicker">Contact</div>
        <h2 class="tl-h2">Tell us about your mandate or your resume</h2>
        <p class="tl-lead">Consultations by appointment only. Average response under 30 minutes during business hours.</p>
        <div class="tl-notice">Mon–Fri, 8 a.m. to 5 p.m. · Meetings scheduled around your availability.</div>
        <p><a href="tel:+15145550199">514 555-0199</a><br><a href="mailto:info@talendus.ca">info@talendus.ca</a><br><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a></p>
        <div class="tl-actions" style="margin-top:18px">
          <a class="tl-btn" href="contact.html">Start a hire</a>
        </div>
      </div>
      <div class="col-lg-6 offset-lg-1">
        <form class="tl-form" action="#" method="post" data-form="contact">
          <label for="nom">Name</label>
          <input id="nom" name="nom" required placeholder="Your name">
          <label for="courriel">Email</label>
          <input id="courriel" type="email" name="courriel" required placeholder="name@company.ca">
          <label for="profil">You are</label>
          <select id="profil" name="profil">
            <option>Employer — I am hiring</option>
            <option>Candidate — I am looking for a role</option>
          </select>
          <label for="msg">Message</label>
          <textarea id="msg" name="message" placeholder="Role, city, urgency or trade"></textarea>
          <button class="tl-btn tl-btn-lg" type="submit">Start a hire</button>
          <div class="tl-success" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>
{CTA}
<section class="tl-section">
  <div class="container">
    <div class="tl-center" style="max-width:760px;margin:0 auto 36px">
      <div class="tl-kicker">Blog</div>
      <h2 class="tl-h2">Recruiting, HR and industry resources in Quebec</h2>
    </div>
    <div class="tl-grid-3">
      <a class="tl-card" href="article-mauvaise-embauche.html"><div class="tl-hero-media" style="height:180px"><img src="{img('usine-equipe.jpg')}" alt=""></div><div class="body"><span class="tl-chip">HR</span><h3>What a bad plant hire really costs</h3></div></a>
      <a class="tl-card" href="article-machiniste-cnc.html"><div class="tl-hero-media" style="height:180px"><img src="{img('cnc-machiniste.jpg')}" alt=""></div><div class="body"><span class="tl-chip">Manufacturing</span><h3>Hiring a CNC machinist in Quebec</h3></div></a>
      <a class="tl-card" href="article-caristes-entrepot.html"><div class="tl-hero-media" style="height:180px"><img src="{img('entrepot-logistique.jpg')}" alt=""></div><div class="body"><span class="tl-chip">Logistics</span><h3>Forklift shortage: warehouse tactics</h3></div></a>
    </div>
  </div>
</section>
"""


def build_en(write, wrap, page_hero):
    write("en/index.html", wrap(
        "Talendus | Industrial and manufacturing recruitment in Quebec",
        "Talendus recruits the talent that keeps Quebec industry moving: production, maintenance, logistics and supervision. Consultation by appointment.",
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
            "Talendus exists so Quebec operations keep moving.",
            "We recruit the people who keep production, maintenance, logistics and supervision running.",
            actions='<a class="tl-btn" href="contact.html">Start a hire</a><a class="tl-btn tl-btn-ghost" href="services.html">See services</a>',
        )
        + f"""
    <section class="tl-section"><div class="container">
    <div class="row g-4"><div class="col-lg-7">
    <h2 class="tl-h2">History</h2>
    <p class="tl-lead">Talendus was built on a simple observation: too many Quebec plants lose weeks with generalist agencies that cannot tell a CNC set-up from a desk job. We built a firm that speaks only operations, shifts, health &amp; safety and line performance.</p>
    <h2 class="tl-h2">Mission</h2>
    <p>Connect Quebec operational employers with the talent that keeps production moving — operators, skilled trades, supervisors and plant leaders.</p>
    <h2 class="tl-h2">Vision</h2>
    <p>Become the reference for industrial talent acquisition in Quebec: the first call when an operation must hire well, with a firm that does not dilute its pool.</p>
    </div>
    <div class="col-lg-4 offset-lg-1">
      <div class="tl-hero-media" style="height:360px;border-radius:16px;overflow:hidden;margin-bottom:18px">
        <img src="{img('usine-equipe.jpg')}" alt="Talendus team on the plant floor">
      </div>
      <a class="tl-btn tl-btn-lg" href="contact.html">Start a hire</a>
    </div></div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
    <h2 class="tl-h2">Values</h2>
    <div class="tl-grid-3">
      <div class="tl-card"><div class="body"><h3>Specialization</h3><p>No office, IT or sales mandates. That filter is your guarantee we will not dilute the pool.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Floor-level rigour</h3><p>We assess like a supervisor, not like an algorithm. Skills, shift, health &amp; safety, attitude.</p></div></div>
      <div class="tl-card"><div class="body"><h3>Word kept</h3><p>Timelines, files, guarantee: what is said is delivered. One contact through to start date.</p></div></div>
    </div>
    </div></section>
    """ + CTA,
        lang="en",
        alt="a-propos.html",
    ))

    services_cards = "".join(
        f'<div class="tl-card"><div class="body"><span class="tl-chip orange">{chip}</span><h3>{t}</h3><p>{p}</p></div></div>'
        for chip, t, p in [
            ("Permanent", "Permanent recruiting", "Stable roles in plants, warehouses and manufacturing leadership. Success fees, replacement guarantee."),
            ("Passive", "Search mandates", "Direct approach of passive candidates for scarce profiles: CNC, electromechanics, plant leaders."),
            ("Leadership", "Manager recruiting", "Plant, production, maintenance and logistics managers. Often confidential."),
            ("Shift", "Supervisor recruiting", "Forepersons and shift supervisors who can hold KPIs, health & safety and team climate."),
            ("Trades", "Skilled trades", "Welders, machinists, industrial mechanics, electromechanical technicians, set-up, quality."),
            ("Urgent", "Urgent recruiting", "Accelerated process when a critical shift is uncovered. A filtered shortlist, not a resume flood."),
            ("Discreet", "Confidential mandates", "Manager replacements or reorganizations run without internal noise."),
            ("HR", "HR support", "Job descriptions, industrial salary grids, joint interviews and onboarding."),
        ]
    )
    write("en/services.html", wrap(
        "Industrial recruiting services | Talendus Quebec",
        "Permanent recruiting, search, managers, supervisors and skilled trades for Quebec operations.",
        "en/services.html",
        page_hero(
            "Services",
            "Services designed for operations, not for a head office.",
            "From labourer to plant manager: one firm, focused on the people who keep industry moving.",
            actions='<a class="tl-btn" href="contact.html">Start a hire</a><a class="tl-btn tl-btn-ghost" href="employers.html">Employer space</a>',
        )
        + f'''
    <section class="tl-section"><div class="container">
      <div class="tl-grid-4">{services_cards}</div>
    </div></section>
    ''' + CTA,
        lang="en",
        alt="services.html",
    ))

    write("en/employers.html", wrap(
        "Employers | Manufacturing and industrial recruiting in Quebec — Talendus",
        "Start a hire with Talendus. Industrial screening and a replacement guarantee for Quebec operations.",
        "en/employers.html",
        page_hero(
            "Employers",
            "Your operation does not need 80 resumes. It needs the right talent, on the right shift.",
            "Free consultation, by appointment. Industrial screening. Replacement guarantee.",
            actions='<a class="tl-btn" href="contact.html">Start a hire</a><a class="tl-btn tl-btn-ghost" href="contact.html">Book a consultation</a>',
            badges='<span class="tl-badge tl-badge-light">By appointment</span> <span class="tl-badge tl-badge-light">Operations partner</span>',
        )
        + SPEED
        + f"""
    <section class="tl-section"><div class="container">
      <div class="tl-grid-3">
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Focus</span><h3>Why Talendus</h3><p>A firm dedicated to operational companies. Passive network, technical assessment and onboarding follow-up — not an agency that also fills admin desks.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Timeline</span><h3>Timelines kept</h3><p>Qualified candidates from day 7 on operations roles. 3 to 8 weeks for supervisors, scarce trades and managers — stated at the briefing.</p></div></div>
        <div class="tl-card"><div class="body"><span class="tl-chip orange">Trust</span><h3>Guarantees</h3><p>Replacement included on permanent mandates. Terms confirmed when the file opens. One contact through to start date.</p></div></div>
      </div>
    </div></section>
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 36px">
        <div class="tl-kicker">How it works</div>
        <h2 class="tl-h2">From the call to the first file, without friction</h2>
      </div>
      <div class="tl-steps">
        <div class="tl-step"><span>01</span><h3>Consultation</h3><p>30 minutes to understand the shift, real pay and urgency.</p></div>
        <div class="tl-step"><span>02</span><h3>Targeting</h3><p>We activate the passive network and operations references.</p></div>
        <div class="tl-step"><span>03</span><h3>Floor filter</h3><p>A Talendus interview before your supervisor loses an hour.</p></div>
        <div class="tl-step"><span>04</span><h3>Shortlist</h3><p>Qualified candidates from day 7. Comparable files, a clear recommendation.</p></div>
        <div class="tl-step"><span>05</span><h3>Follow-up</h3><p>30/60/90 onboarding and replacement guarantee.</p></div>
      </div>
    </div></section>
    <section class="tl-section" id="calculator"><div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-5"><h2 class="tl-h2">Calculator: cost of a bad hire</h2>
        <p class="tl-lead">Estimate the impact of a poor fit (salary, training, overtime and lost productivity). A Talendus mandate almost always costs less than an unstable shift.</p>
        <a class="tl-btn" href="contact.html">Start a hire</a></div>
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
    <section class="tl-section tl-ice"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">Employer FAQ</div>
        <h2 class="tl-h2">What HR and operations directors ask</h2>
      </div>
      {faq_html(FAQ_EMPLOYERS_EN)}
      <div class="tl-center" style="margin-top:32px">
        <a class="tl-btn tl-btn-lg" href="contact.html">Start a hire</a>
      </div>
    </div></section>
    """ + CTA,
        lang="en",
        alt="entreprises.html",
    ))

    write("en/candidates.html", wrap(
        "Candidates | Plant, warehouse and skilled-trade jobs in Quebec — Talendus",
        "Submit your resume to Talendus. Roles in plants, warehouses, logistics, maintenance and supervision in Quebec.",
        "en/candidates.html",
        page_hero(
            "Candidates",
            "Plant and warehouse roles, presented clearly.",
            "We work with operational employers in Quebec — not catch-all mandates. Support through to start date.",
            actions='<a class="tl-btn" href="candidates.html#cv">Submit my resume</a><a class="tl-btn tl-btn-ghost" href="jobs.html">Browse jobs</a>',
            badges='<span class="tl-badge tl-badge-light">Free for you</span> <span class="tl-badge tl-badge-light">Real plant mandates</span>',
        )
        + f"""
    <section class="tl-section" id="cv"><div class="container">
      <div class="row g-4">
        <div class="col-lg-5">
          <h2 class="tl-h2">Submit your resume</h2>
          <p class="tl-lead">Tell us your trade, possible shifts and region. A consultant reaches out if a mandate matches — without sending you to 15 useless interviews.</p>
          <div class="tl-notice" style="color:var(--tl-navy)">Average response under 30 minutes during business hours.</div>
          <p id="process"></p>
          <h3>Our candidate process</h3>
          <ol>
            <li>We receive and qualify your profile.</li>
            <li>Talendus interview (skills, shifts, mobility).</li>
            <li>Introduction to relevant industrial employers.</li>
            <li>Plant interview preparation.</li>
            <li>Follow-up through to start date.</li>
          </ol>
          <div class="tl-actions" style="margin-top:8px">
            <a class="tl-btn tl-btn-electric" href="jobs.html">Browse jobs</a>
          </div>
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
    <section class="tl-section"><div class="container">
      <div class="tl-center" style="max-width:720px;margin:0 auto 28px">
        <div class="tl-kicker">Candidate FAQ</div>
        <h2 class="tl-h2">Before you submit your resume</h2>
      </div>
      {faq_html(FAQ_CANDIDATES_EN)}
    </div></section>
    """ + CTA,
        lang="en",
        alt="candidats.html",
    ))

    write("en/contact.html", wrap(
        "Contact | Industrial recruiting consultation Quebec — Talendus",
        "Contact Talendus in Montreal. Consultations by appointment only. Average response under 30 minutes during business hours. 514 555-0199 · info@talendus.ca",
        "en/contact.html",
        page_hero(
            "Contact",
            "A free consultation for your next industrial mandate.",
            "Consultations by appointment only. Average response under 30 minutes during business hours.",
            actions=f'<a class="tl-btn" href="tel:+15145550199">Call a specialist</a><a class="tl-btn tl-btn-ghost" href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a>',
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
            <p>Average response under 30 minutes during business hours.</p>
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
            <p>Employers and candidates · replies during business hours.</p>
          </div>
        </div>
        <div class="tl-info-card">
          <div class="icon" aria-hidden="true"><i class="fa-solid fa-calendar-check"></i></div>
          <div>
            <h3>Meetings</h3>
            <p>Consultations by appointment only.</p>
            <p>Meetings scheduled around your availability.</p>
          </div>
        </div>
      </div>
    </div></section>
    <section class="tl-section" id="formulaire"><div class="container">
      <div class="tl-contact-grid">
        <div>
          <div class="tl-kicker">Form</div>
          <h2 class="tl-h2">Describe the role or your profile</h2>
          <p class="tl-lead">Employer: open a mandate. Candidate: submit your resume. An industrial consultant comes back — on average under 30 minutes during business hours.</p>
          <form class="tl-form" action="#" method="post" data-form="contact">
            <label>Name</label><input required name="nom">
            <label>Company (optional)</label><input name="entreprise">
            <label>Email</label><input type="email" required name="courriel">
            <label>Phone</label><input name="tel">
            <label>Subject</label>
            <select name="objet">
              <option>Start a hire</option>
              <option>Book a consultation</option>
              <option>Submit my resume</option>
              <option>Join the talent pool</option>
            </select>
            <label>Message</label><textarea required name="message" placeholder="Role, city, shift, urgency or target trade"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">Start a hire</button>
            <div class="tl-success"></div>
          </form>
        </div>
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
            "Job openings", "Industrial roles open in Quebec",
            "Search by trade, city, salary, job type and shift. Apply in one form.",
            actions='<a class="tl-btn" href="candidates.html#cv">Submit my resume</a><a class="tl-btn tl-btn-ghost" href="contact.html">Start a hire</a>',
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
      <p class="tl-muted" id="job-empty" hidden>No roles match these filters. Submit your resume to join the talent pool.</p>
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
                actions='<a class="tl-btn" href="#postuler">Submit my resume</a><a class="tl-btn tl-btn-ghost" href="jobs.html">Browse jobs</a>',
                badges='<span class="tl-badge tl-badge-light">Industrial role</span>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <h2 class="tl-h2">The role</h2>
              <p class="tl-lead">Talendus is recruiting a {title.lower()} for a manufacturing / logistics employer in {city}. A real plant environment, health &amp; safety requirements and production pace.</p>
              <h3>Profile</h3>
              <p>{req}</p>
              <h3>What we offer</h3>
              <ul><li>{typ} role</li><li>Pay: {sal}</li><li>Schedule: {shift}</li><li>Talendus support through to hire</li></ul>
              <p><a href="jobs.html">← All openings</a></p>
            </div>
            <div class="col-lg-4 offset-lg-1" id="postuler">
              <h3>Apply</h3>
              <form class="tl-form" data-form="apply" data-job-slug="{slug}"><label>Name</label><input name="name" required>
              <label>Email</label><input type="email" name="email" required>
              <label>Phone</label><input name="phone">
              <label>Resume link</label><input name="resume" placeholder="https://">
              <button class="tl-btn tl-btn-lg" type="submit">Submit my resume</button>
              <div class="tl-success"></div></form>
            </div>
          </div>
        </div></section>
        """,
            lang="en",
            alt=f"emploi-{slug}.html",
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
            "Industries", "Expertise by type of operation, not a generic speech.",
            "Choose your industry. We already speak your operational language.",
            actions='<a class="tl-btn" href="contact.html">Start a hire</a>',
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
                actions='<a class="tl-btn" href="contact.html">Start a hire</a><a class="tl-btn tl-btn-ghost" href="contact.html">Book a consultation</a>',
            )
            + f"""
        <section class="tl-section"><div class="container">
          <div class="row g-4">
            <div class="col-lg-7">
              <p class="tl-lead">{desc} Talendus does not send desk profiles: only people who have already lived a plant floor or a receiving dock.</p>
              <h2 class="tl-h2">Typical roles</h2>
              <p>Operations, skilled trades, supervision and leadership depending on site size. Profiles who have already lived a plant floor.</p>
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
        f'<a class="tl-card" href="article-{s}.html"><div class="tl-hero-media" style="height:180px"><img src="{img(im)}" alt=""></div><div class="body"><span class="tl-chip">{cat}</span><h3>{t}</h3><p>{lead}</p></div></a>'
        for s, t, cat, im, lead in ARTICLES_EN
    )
    topics = "".join(f'<li style="margin-bottom:8px">{t}</li>' for t in TOPICS_EN)
    write("en/blog.html", wrap(
        "Industrial recruiting, HR and manufacturing blog Quebec | Talendus",
        "SEO articles on manufacturing recruiting, logistics, warehouses and skilled trades in Quebec.",
        "en/blog.html",
        page_hero(
            "Blog", "Recruiting, HR, plants, logistics and careers.",
            "Useful writing for industrial employers and plant candidates — no filler.",
            actions='<a class="tl-btn" href="contact.html">Start a hire</a>',
            badges="",
        )
        + f'<section class="tl-section"><div class="container"><div class="tl-grid-3">{art_cards}</div><h2 class="tl-h2" style="margin-top:48px">Coming topics</h2><ul class="tl-muted">{topics}</ul></div></section>',
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
          <img src="{img(im)}" alt="" style="width:100%;border-radius:16px;margin-bottom:24px">
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
          <p>We target industrial profiles, validate shift fit and present few files — each one defensible.</p>
          <div class="tl-actions" style="margin-top:28px">
            <a class="tl-btn" href="contact.html">Start a hire</a>
            <a class="tl-btn tl-btn-ghost-dark" href="blog.html">Back to the blog</a>
          </div>
        </div></section>
        """,
            lang="en",
            alt=f"article-{slug}.html",
        ))

    write("en/404.html", wrap(
        "Page not found | Talendus",
        "The requested page does not exist. Return to the Talendus home page.",
        "en/404.html",
        page_hero("404", "This page does not exist.", "The mandate might still exist.",
                  actions='<a class="tl-btn" href="index.html">Back to home</a><a class="tl-btn tl-btn-ghost" href="contact.html">Book a consultation</a>',
                  badges=""),
        lang="en",
        alt="404.html",
    ))
    write("en/account.html", wrap(
        "My candidate account | Talendus",
        "Sign in to manage your profile, resume, applications and Talendus notifications.",
        "en/account.html",
        page_hero(
            "Candidates", "Your Talendus file.",
            "Profile, resume, applications, matches, messages and interviews — follow your industrial job search.",
            badges='<span class="tl-badge tl-badge-light">Private space</span>',
        )
        + """<section class="tl-section"><div class="container"><div id="tl-account"></div></div></section>""",
        lang="en",
        alt="espace.html",
    ))
    write("en/privacy.html", wrap(
        "Privacy policy | Talendus",
        "Talendus privacy policy, talendus.ca.",
        "en/privacy.html",
        page_hero("Legal", "Privacy policy", "Resumes and mandates are handled confidentially.", badges="")
        + """<section class="tl-section"><div class="container" style="max-width:800px"><p>Talendus collects information needed for recruiting (contact details, resumes, job descriptions). It is not sold to third parties. It is used only to assess applications, open mandates and communicate with you.</p><p>You may request access, correction or deletion by writing to info@talendus.ca. Data is kept as long as needed for recruiting and legal obligations in Quebec.</p></div></section>""",
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
