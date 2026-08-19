(function () {
  var api = window.TalendusAPI;
  if (!api) return;
  var root = document.getElementById("tl-native-app");
  if (!root) return;

  var PERSONA_KEY = "talendus_mobile_persona";
  var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  var t = isEn ? {
    home: "Home",
    jobs: "Jobs",
    hiring: "Needs",
    messages: "Messages",
    me: "Me",
    hello: "Hello",
    welcomeTitle: "How can Talendus help you?",
    welcomeLead: "Choose once. You will only see what matches that choice.",
    tagline: "Placement agency · Every industry",
    talent: "I am looking for work",
    talentHint: "A consultant follows you. Submit your resume — we call you when a real mandate fits.",
    employer: "I want to hire",
    employerHint: "Hand us a hiring need. We search, present files, and a consultant calls you back.",
    next: "Continue",
    haveAccount: "I already have an account",
    createAccount: "Create my account",
    login: "Sign in",
    register: "Create an account",
    logout: "Sign out",
    email: "Email",
    password: "Password",
    first: "First name",
    last: "Last name",
    company: "Company name",
    submitLogin: "Sign in",
    submitRegister: "Create my account",
    needAccount: "No account yet?",
    back: "Back",
    call: "Call Talendus",
    wa: "WhatsApp",
    search: "Search a role",
    go: "Search",
    emptyJobs: "No roles to show yet.",
    apply: "Ask Talendus to present me",
    applied: "Request sent to your consultant.",
    emptyMsgs: "Write to your consultant. They follow your file with you.",
    write: "Your message",
    send: "Send",
    loading: "Loading…",
    err: "Something went wrong.",
    apps: "My applications",
    emptyApps: "No applications yet. Open Jobs to ask Talendus to present you.",
    city: "City",
    title: "The role you want",
    skills: "Skills",
    save: "Save",
    saved: "Saved.",
    cv: "Resume",
    upload: "Add my resume",
    completeness: "Your file",
    completeFile: "Finish my file",
    statsApps: "Applications",
    statsInterviews: "Interviews",
    hiringLead: "Describe the role in a few lines. Talendus takes the search from there.",
    newNeed: "Hand over a hiring need",
    needTitle: "Role to fill",
    location: "City or area",
    notes: "What you need",
    sendNeed: "Send to Talendus",
    needSent: "Talendus has the need. A consultant will follow up.",
    emptyHiring: "No hiring request yet. Start with one role.",
    emptyThread: "No messages in this conversation yet.",
    consultant: "Your consultant",
    mediate: "A consultant studies your file and gets back to you. Call or write whenever you want to move forward.",
    mediateEmployer: "A consultant takes your hire. Describe the role — we call you back with a shortlist.",
    loginTalentLead: "Sign in to your talent space.",
    loginEmployerLead: "Sign in to your hiring space.",
    loginGenericLead: "Sign in. We open the space that matches your account.",
    registerTalentLead: "Two minutes. Then your consultant can consider you.",
    registerEmployerLead: "Two minutes. Then you can hand us a hiring need.",
    wrongPersonaTalent: "This account is a talent space. We opened that for you.",
    wrongPersonaEmployer: "This account is a company space. We opened that for you.",
    help: "Need help?",
    nextJob: "Roles that may fit",
    openJobs: "See roles",
    openApps: "Follow my applications",
    presented: "Presented files",
    switchPrompt: "Not the right space?",
    changeChoice: "Change",
    notifs: "Updates",
    emptyNotifs: "No updates yet.",
    markAll: "Mark all as read",
    interviews: "Interviews",
    emptyInterviews: "No interview scheduled.",
    savedJobs: "Saved roles",
    emptySaved: "No saved roles yet.",
    saveJob: "Save this role",
    unsaveJob: "Saved",
    alerts: "Job alerts",
    emptyAlerts: "No alert yet. Add a keyword, we watch for you.",
    alertKeywords: "Keywords",
    createAlert: "Create an alert",
    cover: "A line for your consultant (optional)",
    withdraw: "Withdraw",
    forgot: "Forgot password?",
    forgotSent: "If an account exists, we sent a reset email.",
    invoices: "Invoices",
    emptyInvoices: "No invoice yet.",
    downloadPdf: "Download PDF",
    contracts: "Mandates",
    emptyContracts: "No mandate to sign.",
    sign: "Sign",
    signed: "Signed",
    availability: "Availability",
    missing: "Still to complete",
    nextInterview: "Next interview",
    unsigned: "To sign",
    toPay: "To pay",
    deleteAlert: "Remove",
    pay: "Pay",
    confirmInterview: "Confirm",
    cancelInterview: "Cancel",
    interviewUpdated: "Interview updated.",
    settings: "Settings",
    currentPass: "Current password",
    newPass: "New password",
    changePass: "Update password",
    prefs: "Notifications",
    notifyApp: "In the app",
    notifyEmail: "By email",
    notifyApps: "Applications",
    notifyMsgs: "Messages",
    notifyMatch: "Matching roles",
    notifyInt: "Interviews",
    pipeline: "Pipeline",
    companyProfile: "Company",
    emptyPipeline: "No file presented yet.",
    appDetail: "Application",
    history: "Follow-up",
    space: "Your space"
  } : {
    home: "Accueil",
    jobs: "Offres",
    hiring: "Besoins",
    messages: "Messages",
    me: "Moi",
    hello: "Bonjour",
    welcomeTitle: "Comment Talendus peut vous aider ?",
    welcomeLead: "Choisissez une fois. Ensuite, vous ne voyez que ce qui correspond à votre situation.",
    tagline: "Agence de placement · Tous secteurs",
    talent: "Je cherche un emploi",
    talentHint: "Un conseiller vous suit. Déposez votre CV, on vous rappelle pour un vrai mandat.",
    employer: "Je recrute",
    employerHint: "Confiez-nous un besoin. On cherche, on vous présente des dossiers, un conseiller vous rappelle.",
    next: "Continuer",
    haveAccount: "J’ai déjà un compte",
    createAccount: "Créer mon compte",
    login: "Connexion",
    register: "Créer un compte",
    logout: "Déconnexion",
    email: "Courriel",
    password: "Mot de passe",
    first: "Prénom",
    last: "Nom",
    company: "Nom de l’entreprise",
    submitLogin: "Me connecter",
    submitRegister: "Créer mon compte",
    needAccount: "Pas encore de compte ?",
    back: "Retour",
    call: "Appeler Talendus",
    wa: "WhatsApp",
    search: "Rechercher un poste",
    go: "Chercher",
    emptyJobs: "Aucune offre à afficher pour le moment.",
    apply: "Demander à être présenté",
    applied: "Demande envoyée à votre conseiller.",
    emptyMsgs: "Écrivez à votre conseiller. Il suit votre dossier avec vous.",
    write: "Votre message",
    send: "Envoyer",
    loading: "Chargement…",
    err: "Une erreur s’est produite.",
    apps: "Mes candidatures",
    emptyApps: "Aucune candidature pour le moment. Ouvrez Offres pour demander à être présenté.",
    city: "Ville",
    title: "Le poste que vous visez",
    skills: "Compétences",
    save: "Enregistrer",
    saved: "Enregistré.",
    cv: "CV",
    upload: "Ajouter mon CV",
    completeness: "Votre dossier",
    completeFile: "Compléter mon dossier",
    statsApps: "Candidatures",
    statsInterviews: "Entretiens",
    hiringLead: "Décrivez le poste en quelques lignes. Talendus prend la recherche.",
    newNeed: "Confier un besoin",
    needTitle: "Poste à pourvoir",
    location: "Ville ou secteur",
    notes: "Votre besoin",
    sendNeed: "Envoyer à Talendus",
    needSent: "Talendus a bien reçu le besoin. Un conseiller fait le suivi.",
    emptyHiring: "Aucun besoin pour le moment. Commencez par un poste.",
    emptyThread: "Aucun message dans cette conversation.",
    consultant: "Votre conseiller",
    mediate: "Un conseiller étudie votre dossier et vous relance. Appelez-nous ou écrivez-nous dès que vous voulez avancer.",
    mediateEmployer: "Un conseiller prend votre recrutement. Décrivez le poste, on vous rappelle avec une shortlist.",
    loginTalentLead: "Entrez dans votre espace talent.",
    loginEmployerLead: "Entrez dans votre espace entreprise.",
    loginGenericLead: "Connectez-vous. On ouvre l’espace qui correspond à votre compte.",
    registerTalentLead: "Deux minutes. Ensuite, votre conseiller peut vous considérer.",
    registerEmployerLead: "Deux minutes. Ensuite, vous pouvez confier un besoin.",
    wrongPersonaTalent: "Ce compte est un espace talent. Nous l’avons ouvert pour vous.",
    wrongPersonaEmployer: "Ce compte est un espace entreprise. Nous l’avons ouvert pour vous.",
    help: "Besoin d’aide ?",
    nextJob: "Postes qui peuvent convenir",
    openJobs: "Voir les offres",
    openApps: "Suivre mes candidatures",
    presented: "Dossiers présentés",
    switchPrompt: "Ce n’est pas le bon espace ?",
    changeChoice: "Changer",
    notifs: "Suivi",
    emptyNotifs: "Aucune nouvelle pour le moment.",
    markAll: "Tout marquer comme lu",
    interviews: "Entretiens",
    emptyInterviews: "Aucun entretien planifié.",
    savedJobs: "Offres gardées",
    emptySaved: "Aucune offre gardée pour le moment.",
    saveJob: "Garder cette offre",
    unsaveJob: "Offre gardée",
    alerts: "Alertes emploi",
    emptyAlerts: "Aucune alerte. Ajoutez un mot-clé, on surveille pour vous.",
    alertKeywords: "Mots-clés",
    createAlert: "Créer une alerte",
    cover: "Un mot pour votre conseiller (facultatif)",
    withdraw: "Retirer",
    forgot: "Mot de passe oublié ?",
    forgotSent: "Si un compte existe, un courriel de réinitialisation part.",
    invoices: "Factures",
    emptyInvoices: "Aucune facture pour le moment.",
    downloadPdf: "Télécharger le PDF",
    contracts: "Mandats",
    emptyContracts: "Aucun mandat à signer.",
    sign: "Signer",
    signed: "Signé",
    availability: "Disponibilité",
    missing: "À compléter",
    nextInterview: "Prochain entretien",
    unsigned: "À signer",
    toPay: "À payer",
    deleteAlert: "Supprimer",
    pay: "Payer",
    confirmInterview: "Confirmer",
    cancelInterview: "Annuler",
    interviewUpdated: "Entretien mis à jour.",
    settings: "Paramètres",
    currentPass: "Mot de passe actuel",
    newPass: "Nouveau mot de passe",
    changePass: "Mettre à jour le mot de passe",
    prefs: "Notifications",
    notifyApp: "Dans l’appli",
    notifyEmail: "Par courriel",
    notifyApps: "Candidatures",
    notifyMsgs: "Messages",
    notifyMatch: "Offres qui correspondent",
    notifyInt: "Entretiens",
    pipeline: "Pipeline",
    companyProfile: "Entreprise",
    emptyPipeline: "Aucun dossier présenté pour le moment.",
    appDetail: "Candidature",
    history: "Suivi",
    space: "Votre espace"
  };

  var state = {
    user: api.currentUser(),
    contact: { phone_e164: "15145550199", phone_display: "514 555-0199", email: "info@talendus.ca" },
    jobs: [],
    job: null,
    dash: null,
    profile: null,
    apps: [],
    threads: [],
    directory: [],
    conversation: [],
    hiring: [],
    notifs: [],
    interviews: [],
    saved: [],
    alerts: [],
    inbox: [],
    invoices: [],
    contracts: [],
    prefs: null,
    company: null,
    application: null,
    query: "",
    notice: "",
    error: "",
    mismatch: ""
  };

  var icons = {
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/></svg>',
    jobs: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5h8v2"/></svg>',
    msg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 6h14v10H8l-3 3V6z"/></svg>',
    me: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.5"/><path d="M5 19c1.5-3.2 4-5 7-5s5.5 1.8 7 5"/></svg>',
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 3h3l1 4-2 1a12 12 0 006 6l1-2 4 1v3c0 1-1 2-2 2C10 18 6 14 6 7c0-1 1-2 1-4z"/></svg>',
    chevron: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 6l6 6-6 6"/></svg>',
    talent: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.2"/><path d="M5 19c1.4-3 3.8-4.6 7-4.6S17.6 16 19 19"/><path d="M17 4.5l2 2 3.2-3.2"/></svg>',
    hire: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6h8v2"/><path d="M12 12v4"/><path d="M10 14h4"/></svg>',
    bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9a6 6 0 1112 0c0 7 3 7 3 7H3s3 0 3-7"/><path d="M10 19a2 2 0 004 0"/></svg>'
  };
  var MARK = '<svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg"><path fill="#ffffff" fill-rule="evenodd" d="M18 1.5c9.113 0 16.5 7.387 16.5 16.5S27.113 34.5 18 34.5 1.5 27.113 1.5 18 8.887 1.5 18 1.5zm-7.25 9.75h14.5a1.75 1.75 0 1 1 0 3.5h-5.5v12.75a1.75 1.75 0 1 1-3.5 0V14.75h-5.5a1.75 1.75 0 1 1 0-3.5z"/></svg>';
  function brandOrbit(cls) {
    return '<div class="tn-orbit' + (cls ? " " + cls : "") + '" aria-hidden="true">' +
      '<span class="tn-ring tn-ring-a"></span><span class="tn-ring tn-ring-b"></span><span class="tn-ring tn-ring-c"></span>' +
      '<div class="tn-mark">' + MARK + "</div></div>";
  }

  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function dataOf(json) { return json && json.data ? json.data : json; }
  function getPersona() {
    try { return sessionStorage.getItem(PERSONA_KEY) || ""; } catch (e) { return ""; }
  }
  function setPersona(value) {
    try {
      if (value) sessionStorage.setItem(PERSONA_KEY, value);
      else sessionStorage.removeItem(PERSONA_KEY);
    } catch (e) {}
  }
  function staffRole(role) {
    return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
  }
  function isEmployer(user) {
    user = user || state.user;
    return !!(user && user.role === "EMPLOYER");
  }
  function isCandidate(user) {
    user = user || state.user;
    return !!(user && user.role === "CANDIDATE");
  }
  function canonicalize(name, id) {
    var aliases = {
      dashboard: "home", home: "home", profile: "me", documents: "me", cv: "me", resume: "me",
      settings: "settings", account: "settings", applications: "apps", candidatures: "apps",
      application: "app", apps: "apps", saved: "saved", sauvegardees: "saved", alerts: "alerts",
      alertes: "alerts", notifications: "notifs", notifs: "notifs", entretiens: "interviews",
      interviews: "interviews", pipeline: "pipeline", ats: "pipeline", company: "company",
      billing: "invoices", facturation: "invoices", invoices: "invoices", contrats: "contracts",
      mandats: "contracts", contracts: "contracts", hiring: "hiring", messages: "messages",
      me: "me", jobs: "jobs", job: "job", inbox: "inbox"
    };
    name = aliases[name] || name;
    if (isEmployer()) {
      if (name === "jobs" || name === "job" || name === "job-edit" || name === "job-new") name = "hiring";
      if (name === "apps" || name === "app") name = "inbox";
    }
    return { name: name, id: id || "" };
  }
  function route() {
    var raw = (location.hash || "").replace(/^#/, "");
    var parts = raw.replace(/^\//, "").split("/").filter(Boolean);
    var name = parts[0];
    var id = decodeURIComponent(parts.slice(1).join("/"));
    if (!name) name = state.user ? "home" : "welcome";
    return canonicalize(name, id);
  }
  function allowedRoute(name) {
    if (!state.user) return name === "welcome" || name === "login" || name === "register";
    if (isCandidate()) return ["home", "jobs", "job", "apps", "app", "messages", "me", "notifs", "alerts", "saved", "interviews", "settings"].indexOf(name) !== -1;
    if (isEmployer()) return ["home", "hiring", "messages", "me", "notifs", "interviews", "inbox", "invoices", "contracts", "pipeline", "company", "settings"].indexOf(name) !== -1;
    return name === "home" || name === "me" || name === "messages" || name === "settings";
  }
  function portalHash(href) {
    if (!href) return "#/home";
    var hash = "";
    try {
      var u = new URL(href, location.origin);
      hash = (u.hash || "").replace(/^#\/?/, "");
      var m = u.pathname.match(/\/(candidate|employer)(?:\/(.*))?$/);
      if (m && m[2]) hash = m[2];
    } catch (e) {
      var bits = String(href).split("#");
      hash = (bits[1] || "").replace(/^\//, "");
    }
    var parts = hash.split("/").filter(Boolean);
    var mapped = canonicalize(parts[0] || "home", parts.slice(1).join("/"));
    return "#/" + mapped.name + (mapped.id ? "/" + mapped.id : "");
  }
  function go(hash) {
    if ((location.hash || "") === hash) render();
    else location.hash = hash;
  }
  function telHref() { return "tel:+" + String(state.contact.phone_e164 || "").replace(/\D/g, ""); }
  function waHref() {
    var n = String(state.contact.phone_e164 || "").replace(/\D/g, "");
    var msg = encodeURIComponent(isEn ? "Hello Talendus" : "Bonjour Talendus");
    return "https://wa.me/" + n + "?text=" + msg;
  }
  function setNotice(msg, err) {
    state.notice = err ? "" : (msg || "");
    state.error = err ? (msg || t.err) : "";
  }
  function flash() {
    var bits = [];
    if (state.mismatch) bits.push('<p class="tn-ok">' + esc(state.mismatch) + "</p>");
    if (state.error) bits.push('<p class="tn-error">' + esc(state.error) + "</p>");
    if (state.notice) bits.push('<p class="tn-ok">' + esc(state.notice) + "</p>");
    return bits.join("");
  }
  function helpLine() {
    return '<p class="tn-help">' + esc(t.help) + ' <a href="' + telHref() + '">' + esc(state.contact.phone_display || t.call) + "</a></p>";
  }
  function when(iso) {
    if (!iso) return "";
    try { return new Date(iso).toLocaleString(isEn ? "en-CA" : "fr-CA", { dateStyle: "medium", timeStyle: "short" }); }
    catch (e) { return iso; }
  }
  function money(n) {
    var v = Number(n || 0);
    return v.toLocaleString(isEn ? "en-CA" : "fr-CA") + " $";
  }
  function unreadCount() {
    return (state.notifs || []).filter(function (n) { return !n.is_read; }).length;
  }
  function nextInterview() {
    var now = Date.now();
    return (state.interviews || []).filter(function (row) {
      return row.scheduled_at && new Date(row.scheduled_at).getTime() >= now && row.status !== "CANCELLED" && row.status !== "COMPLETED";
    }).sort(function (a, b) { return new Date(a.scheduled_at) - new Date(b.scheduled_at); })[0] || null;
  }
  function missingChips() {
    var missing = ((state.dash && state.dash.completeness && state.dash.completeness.missing) || []).slice(0, 4);
    var labels = {
      name: isEn ? "Name" : "Nom", phone: isEn ? "Phone" : "Téléphone", photo: isEn ? "Photo" : "Photo",
      city: t.city, title: t.title, skills: t.skills, resume: t.cv, bio: isEn ? "Summary" : "Résumé",
      experience: isEn ? "Experience" : "Expérience", availability: t.availability
    };
    if (!missing.length) return "";
    return "<p class=\"tn-meta\">" + esc(t.missing) + "</p><div class=\"tn-chips\">" +
      missing.map(function (key) { return '<span class="tn-chip">' + esc(labels[key] || key) + "</span>"; }).join("") + "</div>";
  }
  function interviewCard() {
    var row = nextInterview();
    if (!row) return "";
    return '<a class="tn-job" href="#/interviews"><h3>' + esc(t.nextInterview) + "</h3><p class=\"tn-meta\">" +
      esc(when(row.scheduled_at) + (row.location ? " · " + row.location : "") + (row.type_label ? " · " + row.type_label : "")) + "</p></a>";
  }

  function topBar() {
    var unread = unreadCount();
    return '<header class="tn-top"><div class="tn-brand">' + brandOrbit("is-sm") + "<span>Talendus</span></div>" +
      '<div class="tn-top-actions"><a class="tn-icon-btn" href="#/notifs" aria-label="' + esc(t.notifs) + '">' + icons.bell +
      (unread ? '<span class="tn-badge">' + unread + "</span>" : "") + "</a>" +
      '<a class="tn-icon-btn" href="' + telHref() + '" aria-label="' + esc(t.call) + '">' + icons.phone + "</a></div></header>";
  }
  function gateBar() {
    return "";
  }
  function tabs() {
    if (!state.user) return "";
    var r = route().name;
    var items = isEmployer() ? [
      { href: "#/home", key: "home", label: t.home, icon: icons.home },
      { href: "#/hiring", key: "hiring", label: t.hiring, icon: icons.hire },
      { href: "#/messages", key: "messages", label: t.messages, icon: icons.msg },
      { href: "#/me", key: "me", label: t.me, icon: icons.me }
    ] : [
      { href: "#/home", key: "home", label: t.home, icon: icons.home },
      { href: "#/jobs", key: "jobs", label: t.jobs, icon: icons.jobs },
      { href: "#/messages", key: "messages", label: t.messages, icon: icons.msg },
      { href: "#/me", key: "me", label: t.me, icon: icons.me }
    ];
    return '<nav class="tn-tabs" aria-label="Talendus">' + items.map(function (item) {
      var on = r === item.key || (item.key === "jobs" && r === "job") || (item.key === "hiring" && (r === "pipeline" || r === "inbox")) || (item.key === "me" && (r === "settings" || r === "company" || r === "apps" || r === "app"));
      return '<a href="' + item.href + '" class="' + (on ? "is-on" : "") + '">' + item.icon + "<span>" + esc(item.label) + "</span></a>";
    }).join("") + "</nav>";
  }

  function welcomeView() {
    return '<div class="tn-gate">' +
      brandOrbit() +
      '<p class="tn-word">Talendus</p>' +
      '<p class="tn-tag">' + esc(t.tagline) + "</p>" +
      "<h1 class=\"tn-title tn-title-light\">" + esc(t.welcomeTitle) + "</h1>" +
      '<p class="tn-lead tn-lead-light">' + esc(t.welcomeLead) + "</p>" +
      '<a class="tn-persona" href="#/register/talent" data-choose="talent">' +
        '<span class="tn-persona-icon" aria-hidden="true">' + icons.talent + "</span>" +
        "<span><strong>" + esc(t.talent) + "</strong><em>" + esc(t.talentHint) + "</em></span>" +
        '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>" +
      '<a class="tn-persona" href="#/register/employer" data-choose="employer">' +
        '<span class="tn-persona-icon" aria-hidden="true">' + icons.hire + "</span>" +
        "<span><strong>" + esc(t.employer) + "</strong><em>" + esc(t.employerHint) + "</em></span>" +
        '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>" +
      '<a class="tn-text-link" href="#/login">' + esc(t.haveAccount) + "</a>" +
      helpLine() + "</div>";
  }

  function authView() {
    var r = route();
    var persona = r.id === "employer" || getPersona() === "employer" ? "employer" : (r.id === "talent" || getPersona() === "talent" ? "talent" : "");
    var employer = persona === "employer";
    var login = r.name === "login";
    var back = '<a class="tn-back" href="#/welcome">' + esc(t.back) + "</a>";
    var lead = login
      ? (employer ? t.loginEmployerLead : persona === "talent" ? t.loginTalentLead : t.loginGenericLead)
      : (employer ? t.registerEmployerLead : t.registerTalentLead);
    var title = login ? t.login : (employer ? t.employer : t.talent);
    var head = '<div class="tn-gate">' + brandOrbit("is-md") + '<p class="tn-word">Talendus</p>';
    if (login) {
      return head + '<div class="tn-sheet">' + back + "<h1 class=\"tn-title\">" + esc(title) + "</h1><p class=\"tn-lead\">" + esc(lead) + "</p>" + flash() +
        '<form class="tn-form" data-login>' +
        "<label for=\"tn-email\">" + esc(t.email) + '</label><input id="tn-email" name="email" type="email" autocomplete="username" inputmode="email" required>' +
        "<label for=\"tn-pass\">" + esc(t.password) + '</label><input id="tn-pass" name="password" type="password" autocomplete="current-password" required minlength="8">' +
        '<button class="tn-btn" type="submit">' + esc(t.submitLogin) + "</button></form>" +
        '<form class="tn-forgot" data-forgot><input type="hidden" name="email" id="tn-forgot-email"><button type="submit" class="tn-text-link">' + esc(t.forgot) + "</button></form>" +
        '<p class="tn-note">' + esc(t.needAccount) + ' <a href="#/welcome">' + esc(t.changeChoice) + "</a></p>" +
        helpLine() + "</div></div>";
    }
    return head + '<div class="tn-sheet">' + back + "<h1 class=\"tn-title\">" + esc(title) + "</h1><p class=\"tn-lead\">" + esc(lead) + "</p>" + flash() +
      '<form class="tn-form" data-register data-role="' + (employer ? "EMPLOYER" : "CANDIDATE") + '">' +
      "<label>" + esc(t.first) + '</label><input name="first_name" autocomplete="given-name" required>' +
      "<label>" + esc(t.last) + '</label><input name="last_name" autocomplete="family-name" required>' +
      "<label>" + esc(t.email) + '</label><input name="email" type="email" autocomplete="email" inputmode="email" required>' +
      "<label>" + esc(t.password) + '</label><input name="password" type="password" autocomplete="new-password" required minlength="8">' +
      (employer ? "<label>" + esc(t.company) + '</label><input name="company_name" autocomplete="organization" required>' : "") +
      '<button class="tn-btn" type="submit">' + esc(t.submitRegister) + "</button></form>" +
      '<p class="tn-note">' + esc(t.haveAccount) + ' <a href="#/login">' + esc(t.login) + "</a></p>" +
      helpLine() + "</div></div>";
  }

  function jobCard(job) {
    if (!job) return "";
    return '<a class="tn-job" href="#/job/' + encodeURIComponent(job.slug || job.id) + '"><h3>' + esc(job.title) + "</h3>" +
      '<p class="tn-meta">' + esc([job.location, job.sector || job.employment_type, job.salary || job.salary_display].filter(Boolean).join(" · ")) + "</p></a>";
  }
  function quickLinks(items) {
    return '<div class="tn-quick">' + items.map(function (it) {
      return '<a href="' + it[0] + '">' + esc(it[1]) + "</a>";
    }).join("") + "</div>";
  }

  function homeView() {
    var name = (state.user && state.user.first_name) || "";
    var dash = state.dash || {};
    var stats = dash.stats || {};
    if (isEmployer()) {
      var unsigned = (state.contracts || []).filter(function (c) { return !c.signed; }).length;
      var due = (state.invoices || []).filter(function (inv) { return inv.status !== "PAID" && inv.status !== "CANCELLED"; }).length;
      return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
        '<p class="tn-lead">' + esc(t.mediateEmployer) + "</p>" + flash() +
        interviewCard() +
        '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.active_jobs || state.hiring.length || 0) + "</b><span>" + esc(t.hiring) + "</span></div>" +
        '<div class="tn-stat"><b>' + esc(state.inbox.length || stats.applications || 0) + "</b><span>" + esc(t.presented) + "</span></div>" +
        '<div class="tn-stat"><b>' + esc(due) + "</b><span>" + esc(t.toPay) + "</span></div>" +
        '<div class="tn-stat"><b>' + esc(unsigned) + "</b><span>" + esc(t.unsigned) + "</span></div></div>" +
        '<a class="tn-btn" href="#/hiring">' + esc(t.newNeed) + "</a>" +
        quickLinks([["#/inbox", t.presented], ["#/pipeline", t.pipeline], ["#/invoices", t.invoices], ["#/contracts", t.contracts]]) +
        dashNotifs();
    }
    var pct = (dash.completeness && dash.completeness.percent) || 0;
    var matches = (dash.matches || []).map(function (row) { return jobCard(row.job || row); }).join("");
    return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
      '<p class="tn-note">' + esc(t.mediate) + "</p>" + flash() +
      '<section class="tn-card tn-file-card"><p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
      '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
      missingChips() +
      '<a class="tn-btn tn-btn-ghost" href="#/me">' + esc(t.completeFile) + "</a></section>" +
      interviewCard() +
      '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.applications || 0) + "</b><span>" + esc(t.statsApps) + "</span></div>" +
      '<div class="tn-stat"><b>' + esc(stats.interviews || 0) + "</b><span>" + esc(t.statsInterviews) + "</span></div>" +
      '<div class="tn-stat"><b>' + esc(stats.saved_jobs || (state.saved || []).length) + "</b><span>" + esc(t.savedJobs) + "</span></div>" +
      '<div class="tn-stat"><b>' + esc(stats.unread_notifications || unreadCount()) + "</b><span>" + esc(t.notifs) + "</span></div></div>" +
      dashNotifs() +
      "<h2 class=\"tn-section\">" + esc(t.nextJob) + "</h2>" +
      '<div class="tn-grid">' + (matches || state.jobs.slice(0, 4).map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>" +
      '<a class="tn-text-link" href="#/jobs">' + esc(t.openJobs) + "</a>";
  }

  function dashNotifs() {
    var rows = ((state.dash && state.dash.notifications) || state.notifs || []).slice(0, 3);
    if (!rows.length) return "";
    return "<h2 class=\"tn-section\">" + esc(t.notifs) + "</h2><div class=\"tn-grid\">" + rows.map(function (n) {
      return '<button type="button" class="tn-job tn-notif' + (n.is_read ? "" : " is-unread") + '" data-open-notif="' +
        esc(n.id) + '" data-href="' + esc(n.href || "") + '"><h3>' + esc(n.title || t.notifs) +
        '</h3><p class="tn-meta">' + esc(n.message || when(n.created_at)) + "</p></button>";
    }).join("") + "</div>";
  }

  function jobsView() {
    return "<h1 class=\"tn-title\">" + esc(t.jobs) + "</h1>" +
      '<form class="tn-search" data-search-jobs><input name="q" placeholder="' + esc(t.search) + '" value="' + esc(state.query || "") + '" enterkeyhint="search"><button type="submit">' + esc(t.go) + "</button></form>" +
      '<div class="tn-grid">' + (state.jobs.map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>";
  }

  function jobView() {
    var job = state.job;
    if (!job) return '<div class="tn-empty">' + esc(t.loading) + "</div>";
    var body = (job.description || "").slice(0, 900);
    var saved = !!(job.saved || (state.saved || []).some(function (row) { return (row.id || (row.job && row.job.id)) === job.id; }));
    return '<a class="tn-back" href="#/jobs">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(job.title) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, job.sector, job.contract_type, job.salary_display].filter(Boolean).join(" · ")) + "</p>" +
      '<div class="tn-card"><p>' + esc(body) + "</p></div>" + flash() +
      '<form class="tn-form" data-apply-form data-job="' + esc(job.id) + '"><label>' + esc(t.cover) + '</label><textarea name="cover_note" maxlength="800"></textarea>' +
      '<button class="tn-btn" type="submit">' + esc(t.apply) + "</button></form>" +
      '<button type="button" class="tn-btn tn-btn-ghost" data-save-job="' + esc(job.id) + '">' + esc(saved ? t.unsaveJob : t.saveJob) + "</button>";
  }

  function messagesView() {
    var r = route();
    if (r.id) {
      var who = state.threads.concat(state.directory).find(function (p) { return String(p.user_id || p.id) === String(r.id); }) || {};
      var name = ((who.first_name || "") + " " + (who.last_name || "")).trim() || t.consultant;
      return '<a class="tn-back" href="#/messages">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(name) + "</h1>" +
        '<div class="tn-msg-list">' + (state.conversation.map(function (m) {
          var mine = state.user && m.sender_id === state.user.id;
          return '<div class="tn-bubble' + (mine ? " mine" : "") + '">' + esc(m.body) + "</div>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyThread) + "</div>") + "</div>" +
        '<form class="tn-composer" data-send-msg data-to="' + esc(r.id) + '"><input name="body" required placeholder="' + esc(t.write) + '" autocomplete="off"><button class="tn-btn" type="submit">' + esc(t.send) + "</button></form>";
    }
    var list = state.threads.length ? state.threads : state.directory.map(function (p) {
      return { user_id: p.id, first_name: p.first_name, last_name: p.last_name, last_message: t.consultant, unread: 0 };
    });
    return "<h1 class=\"tn-title\">" + esc(t.messages) + "</h1><p class=\"tn-lead\">" + esc(isEmployer() ? t.mediateEmployer : t.mediate) + "</p><div class=\"tn-grid\">" +
      (list.map(function (th) {
        var label = ((th.first_name || "") + " " + (th.last_name || "")).trim() || t.consultant;
        return '<a class="tn-thread" href="#/messages/' + encodeURIComponent(th.user_id) + '"><strong>' + esc(label) + "</strong><p class=\"tn-meta\">" + esc(th.last_message || "") + "</p></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyMsgs) + "</div>") + "</div>";
  }

  function hiringView() {
    return "<h1 class=\"tn-title\">" + esc(t.newNeed) + "</h1><p class=\"tn-lead\">" + esc(t.hiringLead) + "</p>" + flash() +
      '<form class="tn-form" data-hiring><label>' + esc(t.needTitle) + '</label><input name="title" required placeholder="' + esc(t.needTitle) + '">' +
      "<label>" + esc(t.location) + '</label><input name="location" autocomplete="address-level2">' +
      "<label>" + esc(t.notes) + '</label><textarea name="notes" placeholder="' + esc(t.notes) + '"></textarea>' +
      '<button class="tn-btn" type="submit">' + esc(t.sendNeed) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + (state.hiring.map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' + esc(row.location || "") + '</p><span class="tn-status">' + esc(row.status_label || row.status || "") + "</span></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyHiring) + "</div>") + "</div>";
  }

  function listBlock(title, empty, items) {
    return "<h1 class=\"tn-title\">" + esc(title) + "</h1>" + flash() + '<div class="tn-grid">' +
      (items && items.length ? items.join("") : '<div class="tn-empty">' + esc(empty) + "</div>") + "</div>";
  }
  function notifsView() {
    return "<h1 class=\"tn-title\">" + esc(t.notifs) + "</h1>" + flash() +
      ((state.notifs || []).length ? '<button type="button" class="tn-btn tn-btn-ghost" data-read-all>' + esc(t.markAll) + "</button>" : "") +
      '<div class="tn-grid">' + ((state.notifs || []).map(function (n) {
        return '<button type="button" class="tn-job tn-notif' + (n.is_read ? "" : " is-unread") + '" data-open-notif="' +
          esc(n.id) + '" data-href="' + esc(n.href || "") + '"><h3>' +
          esc(n.title || t.notifs) + '</h3><p class="tn-meta">' + esc(n.message || when(n.created_at)) + "</p></button>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyNotifs) + "</div>") + "</div>";
  }
  function interviewsView() {
    return listBlock(t.interviews, t.emptyInterviews, (state.interviews || []).map(function (row) {
      var actions = "";
      if (isCandidate() && (row.status === "SCHEDULED" || !row.status)) {
        actions = '<div class="tn-row-actions"><button type="button" class="tn-btn" data-int-status="CONFIRMED" data-int-id="' +
          esc(row.id) + '">' + esc(t.confirmInterview) + '</button><button type="button" class="tn-btn tn-btn-ghost" data-int-status="CANCELLED" data-int-id="' +
          esc(row.id) + '">' + esc(t.cancelInterview) + "</button></div>";
      }
      return '<div class="tn-job"><h3>' + esc(row.type_label || t.interviews) + "</h3><p class=\"tn-meta\">" +
        esc([when(row.scheduled_at), row.location, row.status].filter(Boolean).join(" · ")) + "</p>" + actions + "</div>";
    }));
  }
  function savedView() {
    return listBlock(t.savedJobs, t.emptySaved, (state.saved || []).map(function (row) {
      return jobCard(row.job || row);
    }));
  }
  function alertsView() {
    return "<h1 class=\"tn-title\">" + esc(t.alerts) + "</h1><p class=\"tn-lead\">" + esc(t.emptyAlerts) + "</p>" + flash() +
      '<form class="tn-form" data-alert><label>' + esc(t.alertKeywords) + '</label><input name="keywords" required>' +
      "<label>" + esc(t.city) + '</label><input name="city">' +
      '<button class="tn-btn" type="submit">' + esc(t.createAlert) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + ((state.alerts || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.keywords || row.city || t.alerts) + '</h3><p class="tn-meta">' +
          esc([row.city, row.sector, row.contract_type].filter(Boolean).join(" · ")) +
          '</p><button type="button" class="tn-btn tn-btn-ghost" data-del-alert="' + esc(row.id) + '">' + esc(t.deleteAlert) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyAlerts) + "</div>") + "</div>";
  }
  function inboxView() {
    return listBlock(t.presented, t.emptyApps, (state.inbox || []).map(function (a) {
      var job = a.job || {};
      var cand = a.candidate || {};
      var label = [cand.title, job.title || t.presented].filter(Boolean).join(" · ");
      return '<a class="tn-job" href="#/inbox"><h3>' + esc(label) + '</h3><span class="tn-status">' +
        esc(a.status || a.pipeline_stage || "") + "</span></a>";
    }));
  }
  function pipelineView() {
    var groups = {};
    (state.inbox || []).forEach(function (a) {
      var key = a.pipeline_stage || a.status || t.presented;
      (groups[key] = groups[key] || []).push(a);
    });
    var keys = Object.keys(groups);
    if (!keys.length) return listBlock(t.pipeline, t.emptyPipeline, []);
    return "<h1 class=\"tn-title\">" + esc(t.pipeline) + "</h1>" + flash() + keys.map(function (key) {
      return "<h2 class=\"tn-section\">" + esc(key) + "</h2><div class=\"tn-grid\">" + groups[key].map(function (a) {
        var job = a.job || {};
        return '<div class="tn-job"><h3>' + esc(job.title || t.presented) + '</h3><span class="tn-status">' +
          esc(a.status || "") + "</span></div>";
      }).join("") + "</div>";
    }).join("");
  }
  function appView() {
    var a = state.application;
    if (!a) return '<div class="tn-empty">' + esc(t.loading) + "</div>";
    var job = a.job || {};
    var hist = (a.history || []).map(function (h) {
      return '<p class="tn-meta">' + esc(when(h.created_at) + " · " + (h.new_status || "")) + "</p>";
    }).join("");
    return '<a class="tn-back" href="#/apps">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(job.title || t.appDetail) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, a.status].filter(Boolean).join(" · ")) + "</p>" + flash() +
      (a.cover_note ? '<div class="tn-card"><p>' + esc(a.cover_note) + "</p></div>" : "") +
      "<h2 class=\"tn-section\">" + esc(t.history) + "</h2>" + (hist || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") +
      (a.status === "WITHDRAWN" ? "" : '<button type="button" class="tn-btn tn-btn-ghost" data-withdraw="' + esc(a.id) + '">' + esc(t.withdraw) + "</button>");
  }
  function companyView() {
    var c = state.company || {};
    return "<h1 class=\"tn-title\">" + esc(t.companyProfile) + "</h1>" + flash() +
      '<form class="tn-form" data-company data-id="' + esc(c.id || "") + '"><label>' + esc(t.company) +
      '</label><input name="name" value="' + esc(c.name || "") + '" required>' +
      "<label>" + esc(t.city) + '</label><input name="city" value="' + esc(c.city || "") + '">' +
      "<label>" + esc(t.location) + '</label><input name="sector" value="' + esc(c.sector || "") + '">' +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>";
  }
  function settingsView() {
    var p = state.prefs || {};
    function check(name, label, on) {
      return '<label class="tn-check"><input type="checkbox" name="' + name + '"' + (on ? " checked" : "") + "> " + esc(label) + "</label>";
    }
    return "<h1 class=\"tn-title\">" + esc(t.settings) + "</h1>" + flash() +
      '<form class="tn-form" data-password><label>' + esc(t.currentPass) + '</label><input name="current_password" type="password" required autocomplete="current-password">' +
      "<label>" + esc(t.newPass) + '</label><input name="new_password" type="password" required minlength="8" autocomplete="new-password">' +
      '<button class="tn-btn" type="submit">' + esc(t.changePass) + "</button></form>" +
      '<form class="tn-form" data-prefs><p class="tn-meta">' + esc(t.prefs) + "</p>" +
      check("notify_in_app", t.notifyApp, p.notify_in_app !== false) +
      check("notify_email", t.notifyEmail, p.notify_email !== false) +
      check("notify_application", t.notifyApps, p.notify_application !== false) +
      check("notify_message", t.notifyMsgs, p.notify_message !== false) +
      (isCandidate() ? check("notify_match", t.notifyMatch, p.notify_match !== false) : "") +
      check("notify_interview", t.notifyInt, p.notify_interview !== false) +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>";
  }
  function invoicesView() {
    return listBlock(t.invoices, t.emptyInvoices, (state.invoices || []).map(function (inv) {
      var payable = inv.status === "SENT" || inv.status === "PENDING" || inv.status === "OVERDUE";
      return '<div class="tn-job"><h3>' + esc(inv.number || t.invoices) + "</h3><p class=\"tn-meta\">" +
        esc(money(inv.amount) + " · " + (inv.status || "")) + '</p><div class="tn-row-actions">' +
        (payable ? '<button type="button" class="tn-btn" data-pay="' + esc(inv.id) + '">' + esc(t.pay) + "</button>" : "") +
        '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="invoices" data-id="' +
        esc(inv.id) + '">' + esc(t.downloadPdf) + "</button></div></div>";
    }));
  }
  function contractsView() {
    return "<h1 class=\"tn-title\">" + esc(t.contracts) + "</h1>" + flash() + '<div class="tn-grid">' +
      ((state.contracts || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.document_name || row.type || t.contracts) + '</h3><p class="tn-meta">' +
          esc(row.signed ? t.signed : t.unsigned) + "</p>" +
          (row.signed ? "" : '<button type="button" class="tn-btn" data-sign="' + esc(row.id) + '">' + esc(t.sign) + "</button>") +
          '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="contracts" data-id="' + esc(row.id) + '">' + esc(t.downloadPdf) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyContracts) + "</div>") + "</div>";
  }

  function meView() {
    var html = "<h1 class=\"tn-title\">" + esc(((state.user.first_name || "") + " " + (state.user.last_name || "")).trim() || t.me) + "</h1>" +
      '<p class="tn-meta">' + esc(state.user.email || "") + "</p>" + flash();
    if (isCandidate()) {
      var p = state.profile || {};
      html += '<p class="tn-note">' + esc(t.mediate) + "</p>" +
        '<form class="tn-form" data-profile><label>' + esc(t.city) + '</label><input name="city" value="' + esc(p.city || "") + '" autocomplete="address-level2">' +
        "<label>" + esc(t.title) + '</label><input name="title" value="' + esc(p.title || "") + '">' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(p.skills || "") + '">' +
        "<label>" + esc(t.availability) + '</label><input name="availability" value="' + esc(p.availability || "") + '">' +
        '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>" +
        '<form class="tn-form" data-cv><label>' + esc(t.cv) + '</label><input type="file" name="file" accept=".pdf,.doc,.docx,application/pdf">' +
        '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.upload) + "</button></form>" +
        quickLinks([["#/apps", t.apps], ["#/saved", t.savedJobs], ["#/alerts", t.alerts], ["#/interviews", t.interviews], ["#/settings", t.settings]]) +
        "<h2 class=\"tn-section\">" + esc(t.apps) + "</h2><div class=\"tn-grid\">" +
        (state.apps.map(function (a) {
          var job = a.job || {};
          return '<a class="tn-job" href="#/app/' + encodeURIComponent(a.id) + '"><h3>' + esc(job.title || t.apps) + '</h3><span class="tn-status">' + esc(a.status || "") + "</span></a>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") + "</div>";
    } else {
      html += '<p class="tn-note">' + esc(t.mediateEmployer) + "</p>" +
        '<p class="tn-meta">' + esc((state.dash && state.dash.company_name) || "") + "</p>" +
        quickLinks([["#/inbox", t.presented], ["#/pipeline", t.pipeline], ["#/company", t.companyProfile], ["#/settings", t.settings]]) +
        '<a class="tn-btn" href="#/hiring">' + esc(t.newNeed) + "</a>";
    }
    html += '<button class="tn-btn tn-btn-ghost tn-logout" data-logout>' + esc(t.logout) + "</button>";
    return html;
  }

  function screenHtml() {
    var name = route().name;
    if (!state.user) {
      if (name === "login" || name === "register") return authView();
      return welcomeView();
    }
    if (isCandidate()) {
      if (name === "jobs") return jobsView();
      if (name === "job") return jobView();
      if (name === "messages") return messagesView();
      if (name === "notifs") return notifsView();
      if (name === "interviews") return interviewsView();
      if (name === "saved") return savedView();
      if (name === "alerts") return alertsView();
      if (name === "app") return appView();
      if (name === "settings") return settingsView();
      if (name === "me" || name === "apps") return meView();
      return homeView();
    }
    if (name === "hiring") return hiringView();
    if (name === "messages") return messagesView();
    if (name === "notifs") return notifsView();
    if (name === "interviews") return interviewsView();
    if (name === "inbox") return inboxView();
    if (name === "pipeline") return pipelineView();
    if (name === "invoices") return invoicesView();
    if (name === "contracts") return contractsView();
    if (name === "company") return companyView();
    if (name === "settings") return settingsView();
    if (name === "me") return meView();
    return homeView();
  }

  function render() {
    document.body.classList.toggle("tn-gated", !state.user);
    var chrome = state.user ? topBar() : gateBar();
    root.innerHTML = chrome + '<main id="tn-screen" class="tn-screen">' + screenHtml() + "</main>" + tabs();
  }

  var FRESH_MS = 25000;
  var fetchedAt = {};
  function isFresh(key) {
    return !!(fetchedAt[key] && (Date.now() - fetchedAt[key]) < FRESH_MS);
  }
  function stamp(key) {
    fetchedAt[key] = Date.now();
  }
  function bustCache(keys) {
    if (!keys) { fetchedAt = {}; return; }
    keys.forEach(function (k) { delete fetchedAt[k]; });
  }
  function pull(key, runner, field, asList) {
    if (isFresh(key) && state[field] != null) return Promise.resolve();
    return runner().then(function (json) {
      var value = dataOf(json);
      state[field] = asList ? (value || []) : value;
      stamp(key);
    }).catch(function () {
      if (state[field] == null) state[field] = asList ? [] : null;
    });
  }

  function loadJobs(q) {
    state.query = q || "";
    var key = "jobs:" + (q || "");
    if (isFresh(key) && state.jobs && state.jobs.length) return Promise.resolve();
    return api.jobs({ q: q || "", page_size: 20, sort: "published_at" }).then(function (json) {
      state.jobs = dataOf(json) || [];
      stamp(key);
    }).catch(function () { state.jobs = []; });
  }

  function loadSessionData() {
    state.user = api.currentUser();
    if (!state.user) {
      state.dash = null;
      bustCache();
      return Promise.resolve();
    }
    var name = route().name;
    var tasks = [];
    function need(key, runner, field, asList) {
      tasks.push(pull(key, runner, field, asList));
    }
    need("notifs", function () { return api.notifications(); }, "notifs", true);
    if (isCandidate()) {
      if (name === "home" || name === "me" || name === "apps") {
        need("candDash", function () { return api.request("/candidates/me/dashboard"); }, "dash", false);
      }
      if (name === "me") need("profile", function () { return api.profile(); }, "profile", false);
      if (name === "me" || name === "apps" || name === "app") {
        need("apps", function () { return api.myApplications(); }, "apps", true);
      }
      if (name === "saved" || name === "job") {
        need("saved", function () { return api.request("/jobs/saved"); }, "saved", true);
      }
      if (name === "alerts") need("alerts", function () { return api.request("/alerts"); }, "alerts", true);
      if (name === "interviews" || name === "home") {
        need("interviews", function () { return api.request("/interviews"); }, "interviews", true);
      }
    } else if (isEmployer()) {
      if (name === "home" || name === "me") {
        need("empDash", function () { return api.request("/companies/me/dashboard"); }, "dash", false);
      }
      if (name === "home" || name === "hiring") {
        need("hiring", function () { return api.request("/hiring-requests"); }, "hiring", true);
      }
      if (name === "home" || name === "inbox" || name === "pipeline") {
        need("inbox", function () { return api.request("/applications"); }, "inbox", true);
      }
      if (name === "home" || name === "invoices") {
        need("invoices", function () { return api.request("/invoices"); }, "invoices", true);
      }
      if (name === "home" || name === "contracts") {
        need("contracts", function () { return api.request("/contracts"); }, "contracts", true);
      }
      if (name === "company") need("company", function () { return api.request("/companies/me"); }, "company", false);
      if (name === "interviews" || name === "home") {
        need("interviews", function () { return api.request("/interviews"); }, "interviews", true);
      }
    }
    if (name === "messages") {
      need("threads", function () { return api.request("/messages"); }, "threads", true);
      need("directory", function () { return api.request("/messages/directory"); }, "directory", true);
    }
    return Promise.all(tasks);
  }

  function syncHash() {
    var r = route();
    if (!allowedRoute(r.name)) {
      var fallback = state.user ? "#/home" : "#/welcome";
      if ((location.hash || "") !== fallback) {
        location.replace(fallback);
        return false;
      }
      return true;
    }
    var wanted = "#/" + r.name + (r.id ? "/" + r.id : "");
    var raw = (location.hash || "").replace(/^#\/?/, "").split("/")[0];
    if (state.user && raw && raw !== r.name && raw !== "welcome") {
      location.replace(wanted);
      return false;
    }
    return true;
  }

  function loadRoute() {
    state.user = api.currentUser();
    if (!syncHash()) return Promise.resolve();
    render();
    var r = route();
    var pending = [loadSessionData()];
    if (state.user && isCandidate() && (r.name === "home" || r.name === "jobs")) {
      var haveMatches = !!(state.dash && (state.dash.matches || []).length);
      if (r.name === "jobs" || !haveMatches) pending.push(loadJobs(state.query));
    }
    if (state.user && isCandidate() && r.name === "job" && r.id) {
      pending.push(api.request("/jobs/" + encodeURIComponent(r.id)).then(function (json) { state.job = dataOf(json); }).catch(function () { state.job = null; }));
    }
    if (state.user && isCandidate() && r.name === "app" && r.id) {
      pending.push(api.request("/applications/" + encodeURIComponent(r.id)).then(function (json) { state.application = dataOf(json); }).catch(function () { state.application = null; }));
    }
    if (state.user && r.name === "settings") {
      pending.push(api.request("/users/me/preferences").then(function (json) { state.prefs = dataOf(json) || {}; }).catch(function () { state.prefs = {}; }));
    }
    if (state.user && isEmployer() && r.name === "company") {
      pending.push(api.request("/companies/me").then(function (json) { state.company = dataOf(json); }).catch(function () { state.company = null; }));
    }
    if (state.user && r.name === "messages" && r.id) {
      pending.push(api.request("/messages/" + encodeURIComponent(r.id)).then(function (json) { state.conversation = dataOf(json) || []; }).catch(function () { state.conversation = []; }));
    }
    return Promise.all(pending).then(function () {
      if (!syncHash()) return;
      render();
    }).catch(function () { render(); });
  }

  function afterAuth() {
    return hydrateSession().then(function () {
      var user = api.currentUser();
      var chosen = getPersona();
      state.mismatch = "";
      if (chosen === "talent" && isEmployer(user)) state.mismatch = t.wrongPersonaEmployer;
      if (chosen === "employer" && isCandidate(user)) state.mismatch = t.wrongPersonaTalent;
      if (user) setPersona(isEmployer(user) ? "employer" : "talent");
      setNotice("");
      go("#/home");
      return loadRoute();
    });
  }

  function hydrateSession() {
    if (!api.currentUser()) return Promise.resolve();
    return api.me().then(function (json) {
      var user = dataOf(json);
      if (!user) return;
      state.user = user;
      if (staffRole(user.role)) {
        location.replace("/admin/");
        return new Promise(function () {});
      }
      setPersona(user.role === "EMPLOYER" ? "employer" : "talent");
    }).catch(function () {});
  }

  function fail(err) {
    setNotice((err && err.message) || t.err, true);
    render();
  }
  function done(msg) {
    setNotice(msg || "");
    bustCache();
    return loadRoute();
  }

  root.addEventListener("click", function (e) {
    var choose = e.target.closest("[data-choose]");
    if (choose) setPersona(choose.getAttribute("data-choose"));
    var applyBtn = e.target.closest("[data-apply]");
    if (applyBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.apply({ job_id: applyBtn.getAttribute("data-apply") }).then(function () { done(t.applied); }).catch(fail);
    }
    var saveBtn = e.target.closest("[data-save-job]");
    if (saveBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      var jobId = saveBtn.getAttribute("data-save-job");
      var already = (state.saved || []).some(function (row) { return String(row.id || (row.job && row.job.id)) === String(jobId); });
      (already ? api.unsaveJob(jobId) : api.saveJob(jobId)).then(function () { done(t.saved); }).catch(fail);
    }
    var withdraw = e.target.closest("[data-withdraw]");
    if (withdraw) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/applications/" + withdraw.getAttribute("data-withdraw") + "/withdraw", { method: "POST" })
        .then(function () { done(t.saved); }).catch(fail);
    }
    var delAlert = e.target.closest("[data-del-alert]");
    if (delAlert) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/alerts/" + delAlert.getAttribute("data-del-alert"), { method: "DELETE" })
        .then(function () { done(t.saved); }).catch(fail);
    }
    var readOne = e.target.closest("[data-read-notif]");
    if (readOne) {
      e.preventDefault();
      api.request("/notifications/" + readOne.getAttribute("data-read-notif") + "/read", { method: "POST" })
        .then(function () { return loadRoute(); }).catch(fail);
    }
    var openNotif = e.target.closest("[data-open-notif]");
    if (openNotif) {
      e.preventDefault();
      var href = openNotif.getAttribute("data-href") || "";
      var dest = portalHash(href);
      var nid = openNotif.getAttribute("data-open-notif");
      var jump = function () { go(dest); loadRoute(); };
      if (nid) api.request("/notifications/" + nid + "/read", { method: "POST" }).then(jump).catch(jump);
      else jump();
    }
    if (e.target.closest("[data-read-all]")) {
      e.preventDefault();
      api.request("/notifications/read-all", { method: "POST" }).then(function () { return loadRoute(); }).catch(fail);
    }
    var intBtn = e.target.closest("[data-int-status]");
    if (intBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/interviews/" + intBtn.getAttribute("data-int-id") + "/status", {
        method: "POST",
        body: { status: intBtn.getAttribute("data-int-status") }
      }).then(function () { done(t.interviewUpdated); }).catch(fail);
    }
    var signBtn = e.target.closest("[data-sign]");
    if (signBtn) {
      e.preventDefault();
      if (!isEmployer()) return;
      var signer = ((state.user.first_name || "") + " " + (state.user.last_name || "")).trim();
      api.signContract(signBtn.getAttribute("data-sign"), { signer_name: signer, accepted: true })
        .then(function () { done(t.signed); }).catch(fail);
    }
    var pdfBtn = e.target.closest("[data-pdf]");
    if (pdfBtn) {
      e.preventDefault();
      var kind = pdfBtn.getAttribute("data-pdf");
      var id = pdfBtn.getAttribute("data-id");
      api.download("/" + kind + "/" + id + "/pdf", kind === "invoices" ? "facture.pdf" : "mandat.pdf").catch(fail);
    }
    var payBtn = e.target.closest("[data-pay]");
    if (payBtn) {
      e.preventDefault();
      if (!isEmployer()) return;
      api.request("/invoices/" + payBtn.getAttribute("data-pay") + "/checkout", { method: "POST" }).then(function (json) {
        var url = json && json.data && json.data.checkout_url;
        if (url) location.assign(url);
        else fail({ message: t.err });
      }).catch(fail);
    }
    if (e.target.closest("[data-logout]")) {
      e.preventDefault();
      api.logout().then(function () {
        state.user = null;
        state.mismatch = "";
        bustCache();
        setPersona("");
        setNotice("");
        go("#/welcome");
        loadRoute();
      });
    }
  });

  root.addEventListener("submit", function (e) {
    var form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.matches("[data-search-jobs]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      loadJobs(new FormData(form).get("q")).then(function () { go("#/jobs"); render(); });
    } else if (form.matches("[data-login]")) {
      e.preventDefault();
      var fd = new FormData(form);
      api.login(fd.get("email"), fd.get("password")).then(afterAuth)
        .catch(fail);
    } else if (form.matches("[data-forgot]")) {
      e.preventDefault();
      var emailEl = document.getElementById("tn-email");
      var email = ((emailEl && emailEl.value) || new FormData(form).get("email") || "").trim();
      if (!email) { fail({ message: t.err }); return; }
      api.forgotPassword(email).then(function () { setNotice(t.forgotSent); render(); }).catch(fail);
    } else if (form.matches("[data-apply-form]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var cover = (new FormData(form).get("cover_note") || "").trim();
      var payload = { job_id: form.getAttribute("data-job") };
      if (cover) payload.cover_note = cover;
      api.apply(payload).then(function () { done(t.applied); }).catch(fail);
    } else if (form.matches("[data-alert]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/alerts", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-register]")) {
      e.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      data.role = form.getAttribute("data-role") || (getPersona() === "employer" ? "EMPLOYER" : "CANDIDATE");
      api.register(data).then(afterAuth).catch(fail);
    } else if (form.matches("[data-send-msg]")) {
      e.preventDefault();
      if (!state.user) return;
      api.request("/messages", { method: "POST", body: { recipient_id: form.getAttribute("data-to"), body: new FormData(form).get("body") } }).then(function () {
        form.reset();
        loadRoute();
      }).catch(fail);
    } else if (form.matches("[data-hiring]")) {
      e.preventDefault();
      if (!isEmployer()) return;
      api.request("/hiring-requests", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) }).then(function () {
        form.reset();
        done(t.needSent);
      }).catch(fail);
    } else if (form.matches("[data-profile]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.updateProfile(Object.fromEntries(new FormData(form).entries())).then(function () { done(t.saved); }).catch(fail);
    } else if (form.matches("[data-cv]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var file = form.file && form.file.files && form.file.files[0];
      if (!file) return;
      var payload = new FormData();
      payload.append("file", file);
      api.uploadResume(payload).then(function () { done(t.saved); }).catch(fail);
    } else if (form.matches("[data-password]")) {
      e.preventDefault();
      api.request("/auth/change-password", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-prefs]")) {
      e.preventDefault();
      var prefs = {
        notify_in_app: !!(form.notify_in_app && form.notify_in_app.checked),
        notify_email: !!(form.notify_email && form.notify_email.checked),
        notify_application: !!(form.notify_application && form.notify_application.checked),
        notify_message: !!(form.notify_message && form.notify_message.checked),
        notify_interview: !!(form.notify_interview && form.notify_interview.checked)
      };
      if (form.notify_match) prefs.notify_match = !!form.notify_match.checked;
      api.request("/users/me/preferences", { method: "PATCH", body: prefs }).then(function () { done(t.saved); }).catch(fail);
    } else if (form.matches("[data-company]")) {
      e.preventDefault();
      if (!isEmployer()) return;
      var cid = form.getAttribute("data-id");
      if (!cid) return;
      api.request("/companies/" + cid, { method: "PATCH", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { done(t.saved); }).catch(fail);
    }
  });

  window.addEventListener("hashchange", loadRoute);
  function registerSw() {
    if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
    }
  }
  if (window.requestIdleCallback) window.requestIdleCallback(registerSw, { timeout: 2500 });
  else setTimeout(registerSw, 1200);
  api.services().then(function (json) {
    var data = dataOf(json) || {};
    if (data.contact) state.contact = data.contact;
  }).catch(function () {});
  hydrateSession().then(loadRoute).catch(function () { render(); });
  render();
})();
