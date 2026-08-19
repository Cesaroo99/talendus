(function (global) {
  var isEn = ((document.documentElement.lang || "").toLowerCase().indexOf("en") === 0);

  var CITIES = isEn
    ? ["Montreal", "Laval", "Longueuil", "Brossard", "Terrebonne", "Repentigny", "Saint-Jérôme", "Boucherville", "Anjou", "Drummondville", "Sherbrooke", "Trois-Rivières", "Quebec City", "Lévis", "Gatineau", "Saint-Hyacinthe", "Granby", "Saint-Jean-sur-Richelieu", "Blainville", "Mirabel", "Remote / hybrid"]
    : ["Montréal", "Laval", "Longueuil", "Brossard", "Terrebonne", "Repentigny", "Saint-Jérôme", "Boucherville", "Anjou", "Drummondville", "Sherbrooke", "Trois-Rivières", "Québec", "Lévis", "Gatineau", "Saint-Hyacinthe", "Granby", "Saint-Jean-sur-Richelieu", "Blainville", "Mirabel", "Télétravail / hybride"];

  var SECTORS = isEn
    ? ["Manufacturing", "Warehouse", "Logistics", "Maintenance", "Production", "Transportation", "Construction", "Food processing", "Metals", "Plastics", "Technology", "Healthcare", "Administration", "Engineering"]
    : ["Manufacturier", "Entrepôt", "Logistique", "Maintenance", "Production", "Transport", "Construction", "Transformation alimentaire", "Métallurgie", "Plasturgie", "Technologie", "Santé", "Administration", "Ingénierie"];

  var CONTRACTS = isEn
    ? ["Permanent / full-time", "Temporary", "Part-time", "Day shift", "Evening shift", "Night shift", "Weekend", "Contract"]
    : ["Permanent / temps plein", "Temporaire", "Temps partiel", "Quart de jour", "Quart de soir", "Quart de nuit", "Fin de semaine", "Contractuel"];

  var TITLES = isEn
    ? ["Forklift operator", "Welder", "CNC machinist", "Production operator", "Industrial mechanic", "Electromechanical technician", "Warehouse supervisor", "Truck driver", "Shipper / receiver", "Production supervisor", "Accountant", "Developer", "Industrial engineer"]
    : ["Cariste", "Soudeur", "Machiniste CNC", "Opérateur de production", "Mécanicien industriel", "Électromécanicien", "Superviseur d’entrepôt", "Chauffeur", "Magasinier / réception", "Superviseur de production", "Comptable", "Développeur", "Ingénieur industriel"];

  var SKILLS = isEn
    ? ["Forklift class I–V", "Overhead crane", "Welding (SMAW/GMAW)", "CNC readout", "SAP / Excel", "ASP Construction", "Class 5 licence", "Class 1 licence", "Food safety", "Lockout / tagout"]
    : ["Cariste classe 1 à 5", "Pont roulant", "Soudure (SMAW/GMAW)", "Lecture de plans CNC", "SAP / Excel", "ASP Construction", "Permis classe 5", "Permis classe 1", "Salubrité alimentaire", "Cadenassage"];

  var LANGUAGES = isEn
    ? ["French", "French, English", "French, English, Spanish"]
    : ["Français", "Français, anglais", "Français, anglais, espagnol"];

  var SCHOOLS = isEn
    ? ["Cégep de Saint-Laurent", "Cégep de Maisonneuve", "École des métiers de l’aérospatiale", "Centre de formation professionnelle", "ÉTS", "Polytechnique Montréal"]
    : ["Cégep de Saint-Laurent", "Cégep de Maisonneuve", "École des métiers de l’aérospatiale", "Centre de formation professionnelle", "ÉTS", "Polytechnique Montréal"];

  var DIPLOMAS = isEn
    ? ["DVS / DEP", "DCS / DEC", "ASP Construction", "Bachelor's", "AEC"]
    : ["DEP", "DEC", "ASP Construction", "Baccalauréat", "AEC"];

  var CERTS = isEn
    ? ["ASP Construction", "Forklift class I–V", "Overhead crane", "First aid / CNESST", "WHMIS / SIMDUT", "Food handler"]
    : ["ASP Construction", "Cariste classe 1 à 5", "Pont roulant", "Secourisme / CNESST", "SIMDUT", "Manipulateur d’aliments"];

  var HINTS = {
    city: {
      list: CITIES,
      ph: isEn ? "Montreal, Laval, Longueuil, South Shore…" : "Montréal, Laval, Longueuil, Rive-Sud…",
      def: ""
    },
    province: {
      list: isEn ? ["Quebec"] : ["Québec"],
      ph: isEn ? "Quebec" : "Québec",
      def: isEn ? "Quebec" : "Québec"
    },
    country: {
      list: ["Canada"],
      ph: "Canada",
      def: "Canada"
    },
    sector: {
      list: SECTORS,
      ph: isEn ? "Manufacturing, warehouse, logistics…" : "Manufacturier, entrepôt, logistique…",
      def: ""
    },
    contract: {
      list: CONTRACTS,
      ph: isEn ? "Permanent, day shift, 40 h/week" : "Permanent, quart de jour, 40 h/semaine",
      def: ""
    },
    title: {
      list: TITLES,
      ph: isEn ? "e.g. forklift operator, welder, CNC machinist" : "ex. cariste, soudeur, machiniste CNC",
      def: ""
    },
    skills: {
      list: SKILLS,
      ph: isEn ? "Forklift, lockout, Excel, class 5 licence…" : "Cariste, cadenassage, Excel, permis classe 5…",
      def: ""
    },
    languages: {
      list: LANGUAGES,
      ph: isEn ? "French, English" : "Français, anglais",
      def: ""
    },
    phone: {
      list: [],
      ph: "514 555-0123",
      def: ""
    },
    address: {
      list: [],
      ph: isEn ? "1234 Notre-Dame St W, suite 200" : "1234, rue Notre-Dame Ouest, bureau 200",
      def: ""
    },
    salary: {
      list: isEn
        ? ["22 $/h", "24–28 $/h", "55 000 $/year", "70 000 $/year"]
        : ["22 $/h", "24–28 $/h", "55 000 $/an", "70 000 $/an"],
      ph: isEn ? "24–28 $/h or 55 000 $/year (CAD)" : "24–28 $/h ou 55 000 $/an (CAD)",
      def: ""
    },
    salaryNum: {
      list: [],
      ph: isEn ? "55000 (CAD / year)" : "55000 (CAD / an)",
      def: ""
    },
    availability: {
      list: isEn
        ? ["Immediate", "2 weeks notice", "Day shift", "Evening shift"]
        : ["Immédiatement", "Préavis 2 semaines", "Quart de jour", "Quart de soir"],
      ph: isEn ? "Immediate, 2 weeks, day shift…" : "Immédiatement, 2 semaines, quart de jour…",
      def: ""
    },
    mobility: {
      list: isEn
        ? ["Greater Montreal", "North Shore", "South Shore", "Willing to relocate in Quebec"]
        : ["Grand Montréal", "Rive-Nord", "Rive-Sud", "Prêt à se déplacer au Québec"],
      ph: isEn ? "Greater Montreal, North Shore, South Shore…" : "Grand Montréal, Rive-Nord, Rive-Sud…",
      def: ""
    },
    experience: {
      list: isEn
        ? ["Entry-level", "1–2 years", "3–5 years", "5 years and up", "Supervisor"]
        : ["Débutant", "1–2 ans", "3 à 5 ans", "5 ans et plus", "Supervision"],
      ph: isEn ? "e.g. 3–5 years, supervisor" : "ex. 3 à 5 ans, supervision",
      def: ""
    },
    years: {
      list: [],
      ph: isEn ? "5" : "5",
      def: ""
    },
    size: {
      list: isEn ? ["10–49", "50–199", "200–499", "500+"] : ["10–49", "50–199", "200–499", "500+"],
      ph: isEn ? "e.g. 50–200 employees" : "ex. 50–200 employés",
      def: ""
    },
    school: {
      list: SCHOOLS,
      ph: isEn ? "e.g. Cégep de Saint-Laurent" : "ex. Cégep de Saint-Laurent",
      def: ""
    },
    diploma: {
      list: DIPLOMAS,
      ph: isEn ? "DVS, DCS, ASP Construction…" : "DEP, DEC, ASP Construction…",
      def: ""
    },
    cert: {
      list: CERTS,
      ph: isEn ? "ASP Construction, forklift class I–V…" : "ASP Construction, cariste classe 1 à 5…",
      def: ""
    },
    company: {
      list: [],
      ph: isEn ? "e.g. plant in Laval, warehouse in Longueuil" : "ex. usine à Laval, entrepôt à Longueuil",
      def: ""
    },
    role: {
      list: TITLES,
      ph: isEn ? "e.g. production operator" : "ex. opérateur de production",
      def: ""
    },
    roleHr: {
      list: isEn ? ["HR", "Operations", "Plant manager", "Owner"] : ["RH", "Opérations", "Direction d’usine", "Propriétaire"],
      ph: isEn ? "HR, operations, owner…" : "RH, opérations, direction…",
      def: ""
    },
    cover: {
      list: [],
      ph: isEn ? "Available Monday, class 5 licence, 4 years on forklift." : "Disponible lundi, permis classe 5, 4 ans sur chariot élévateur.",
      def: ""
    },
    message: {
      list: [],
      ph: isEn ? "Day shift, 40 h, ASP required, plant in Laval…" : "Quart de jour, 40 h, ASP requise, usine à Laval…",
      def: ""
    },
    notes: {
      list: [],
      ph: isEn ? "Day shift 6 a.m.–2 p.m., steel-toe boots, bilingual an asset." : "Quart 6 h–14 h, bottes d’acier, bilingue un atout.",
      def: ""
    },
    bio: {
      list: [],
      ph: isEn ? "Production operator, 5 years in a North Shore plant." : "Opérateur de production, 5 ans en usine sur la Rive-Nord.",
      def: ""
    },
    description: {
      list: [],
      ph: isEn ? "Manufacturing SME in Laval, about 80 employees." : "PME manufacturière à Laval, environ 80 employés.",
      def: ""
    },
    keywords: {
      list: TITLES,
      ph: isEn ? "Forklift, welder, CNC machinist" : "Cariste, soudeur, machiniste CNC",
      def: ""
    },
    website: {
      list: [],
      ph: "https://",
      def: ""
    },
    legal: {
      list: [],
      ph: isEn ? "Legal name Inc. or L.P." : "Raison sociale Inc. ou S.E.N.C.",
      def: ""
    },
    email: {
      list: [],
      ph: isEn ? "name@company.ca" : "prenom.nom@entreprise.ca",
      def: ""
    },
    linkedin: {
      list: [],
      ph: "https://www.linkedin.com/company/…",
      def: ""
    }
  };

  var NAME_MAP = {
    city: "city",
    location: "city",
    localisation: "city",
    region: "city",
    jobcity: "city",
    province: "province",
    country: "country",
    sector: "sector",
    secteur: "sector",
    contract_type: "contract",
    contrat: "contract",
    contract: "contract",
    title: "title",
    poste: "title",
    metier: "title",
    needtitle: "title",
    skills: "skills",
    competences: "skills",
    languages: "languages",
    phone: "phone",
    tel: "phone",
    address: "address",
    salary: "salary",
    salary_display: "salary",
    desired_salary_min: "salaryNum",
    salary_min: "salaryNum",
    availability: "availability",
    mobility: "mobility",
    experience: "experience",
    experience_level: "experience",
    years_experience: "years",
    years: "years",
    size_label: "size",
    taille: "size",
    school: "school",
    diploma: "diploma",
    company: "company",
    company_name: "company",
    entreprise: "company",
    role: "role",
    fonction: "roleHr",
    cover_note: "cover",
    message: "message",
    notes: "notes",
    bio: "bio",
    description: "description",
    keywords: "keywords",
    website: "website",
    legal_name: "legal",
    linkedin_url: "linkedin",
    facebook_url: "website",
    email: "email",
    courriel: "email"
  };

  var SKIP_TYPES = { password: 1, file: 1, hidden: 1, checkbox: 1, radio: 1, submit: 1, button: 1, reset: 1, range: 1, color: 1 };
  var SKIP_NAMES = {
    password: 1, current_password: 1, new_password: 1, token: 1, website_url: 1,
    first_name: 1, last_name: 1, nom: 1, recipient_id: 1, signer_name: 1,
    firstName: 1, lastName: 1, contact: 1, body: 1
  };

  function hintFor(el) {
    var name = (el.getAttribute("name") || el.id || "").trim();
    if (!name || SKIP_NAMES[name]) return null;
    if (el.id === "job-search") return HINTS.title;
    if (el.id === "job-city") return HINTS.city;
    if (name === "q") {
      var form = el.form || el.closest("form");
      if (form && (form.hasAttribute("data-search-jobs") || form.id === "acc-job-filters" || /job|alert/.test(form.id || ""))) return HINTS.title;
      if (el.id === "job-search") return HINTS.title;
      return null;
    }
    if (name === "name") {
      if (el.closest("[data-cert], #acc-cert")) return HINTS.cert;
      if (el.closest("[data-company], #acc-company")) return HINTS.company;
      return null;
    }
    if (name === "email" || name === "courriel") {
      if (el.closest("[data-login], [data-register], [data-forgot], [data-password]")) return null;
      if ((el.getAttribute("autocomplete") || "") === "username") return null;
      if (el.disabled) return null;
      if (el.closest("[data-company], #acc-company, [data-form='hiring-need']")) return HINTS.email;
      return null;
    }
    return HINTS[NAME_MAP[name]] || null;
  }

  function ensureLists() {
    var host = document.getElementById("tl-qc-hints");
    if (host) return host;
    host = document.createElement("div");
    host.id = "tl-qc-hints";
    host.hidden = true;
    var html = "";
    Object.keys(HINTS).forEach(function (key) {
      var items = HINTS[key].list || [];
      if (!items.length) return;
      html += '<datalist id="tl-hint-' + key + '">' + items.map(function (v) {
        return "<option value=\"" + String(v).replace(/"/g, "&quot;") + "\">";
      }).join("") + "</datalist>";
    });
    host.innerHTML = html;
    document.body.appendChild(host);
    return host;
  }

  function decorate(el) {
    if (!el || el.nodeType !== 1) return;
    if (el.getAttribute("data-qc-hint") === "1") return;
    var type = (el.getAttribute("type") || "text").toLowerCase();
    if (SKIP_TYPES[type]) return;
    if (el.tagName !== "INPUT" && el.tagName !== "TEXTAREA") return;
    var hint = hintFor(el);
    if (!hint) return;
    el.setAttribute("data-qc-hint", "1");
    if (hint.ph) el.setAttribute("placeholder", hint.ph);
    if (hint.def && !String(el.value || "").trim()) {
      if (el.name === "province" || el.name === "country") el.value = hint.def;
    }
    if (hint.list && hint.list.length && el.tagName === "INPUT" && type !== "number" && type !== "date" && type !== "email") {
      var key = null;
      Object.keys(HINTS).some(function (k) { if (HINTS[k] === hint) { key = k; return true; } return false; });
      if (key) el.setAttribute("list", "tl-hint-" + key);
    }
    if (el.name === "phone" || el.name === "tel") el.setAttribute("inputmode", el.getAttribute("inputmode") || "tel");
  }

  function apply(root) {
    if (!document.body) return;
    ensureLists();
    var scope = root && root.querySelectorAll ? root : document;
    var nodes = scope.querySelectorAll("input, textarea");
    for (var i = 0; i < nodes.length; i++) decorate(nodes[i]);
    if (root && (root.tagName === "INPUT" || root.tagName === "TEXTAREA")) decorate(root);
  }

  var scheduled = null;
  function schedule(root) {
    if (scheduled) return;
    scheduled = setTimeout(function () {
      scheduled = null;
      apply(root || document);
    }, 40);
  }

  function boot() {
    apply(document);
    if (typeof MutationObserver === "undefined") return;
    var obs = new MutationObserver(function (muts) {
      for (var i = 0; i < muts.length; i++) {
        if (muts[i].addedNodes && muts[i].addedNodes.length) {
          schedule(document);
          return;
        }
      }
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  global.TalendusHints = { apply: apply, cities: CITIES, sectors: SECTORS, titles: TITLES };
})(window);
