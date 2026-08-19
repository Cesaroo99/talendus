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
    space: "Your space",
    profile: "My profile",
    documents: "Resume",
    account: "Account",
    helpTitle: "Talk to Talendus",
    emailUs: "Email",
    phone: "Phone",
    bio: "Summary",
    experience: "Experience",
    languages: "Languages",
    sector: "Industry",
    contract: "Contract type",
    salary: "Desired pay",
    mobility: "Mobility",
    province: "Province",
    photo: "Photo",
    add: "Add",
    remove: "Remove",
    education: "Education",
    certs: "Certifications",
    school: "School",
    diploma: "Diploma",
    companyName: "Company",
    roleHeld: "Role",
    years: "Years",
    downloadCv: "Download",
    noCv: "No resume yet. Add one so a consultant can study your path.",
    cvReady: "Resume on file",
    groupFile: "Your file",
    groupFollow: "Follow-up",
    groupHire: "Hiring",
    groupCompany: "Company",
    groupAccount: "Account",
    seeAll: "See all",
    nextStep: "To do now",
    myNeeds: "Your hiring needs",
    addNeed: "New need",
    seats: "Openings",
    website: "Website",
    address: "Address",
    size: "Company size",
    description: "Description",
    candidate: "Candidate",
    presentedFile: "Presented file",
    jobCity: "City",
    jobSector: "Industry",
    moreFilters: "Narrow the search",
    contactUs: "A consultant answers. Call, write or send a WhatsApp.",
    photoHint: "A photo helps your consultant recognise you.",
    expHint: "Add roles you have held. It helps us match you.",
    inboxEmpty: "No file presented yet. Hand us a need, we come back with people.",
    appsHint: "Each application is followed by your consultant.",
    profileLead: "The clearer this is, the faster a consultant can call you for a real mandate.",
    companyLead: "Keep the company file up to date so we brief the right people.",
    needLead: "Describe the role. A consultant opens the search and calls you back.",
    country: "Country",
    birth: "Date of birth",
    startDate: "Start date",
    experienceLevel: "Experience level",
    editNeed: "Edit this need",
    legalName: "Legal name",
    linkedin: "LinkedIn"
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
    space: "Votre espace",
    profile: "Mon profil",
    documents: "CV",
    account: "Compte",
    helpTitle: "Parler à Talendus",
    emailUs: "Courriel",
    phone: "Téléphone",
    bio: "Résumé",
    experience: "Expérience",
    languages: "Langues",
    sector: "Secteur",
    contract: "Type de contrat",
    salary: "Salaire souhaité",
    mobility: "Mobilité",
    province: "Province",
    photo: "Photo",
    add: "Ajouter",
    remove: "Retirer",
    education: "Formations",
    certs: "Certifications",
    school: "École",
    diploma: "Diplôme",
    companyName: "Entreprise",
    roleHeld: "Poste",
    years: "Années",
    downloadCv: "Télécharger",
    noCv: "Aucun CV pour le moment. Ajoutez-en un pour qu’un conseiller étudie votre parcours.",
    cvReady: "CV au dossier",
    groupFile: "Votre dossier",
    groupFollow: "Suivi",
    groupHire: "Recrutement",
    groupCompany: "Entreprise",
    groupAccount: "Compte",
    seeAll: "Tout voir",
    nextStep: "À faire maintenant",
    myNeeds: "Vos besoins",
    addNeed: "Nouveau besoin",
    seats: "Postes",
    website: "Site web",
    address: "Adresse",
    size: "Taille",
    description: "Description",
    candidate: "Candidat",
    presentedFile: "Dossier présenté",
    jobCity: "Ville",
    jobSector: "Secteur",
    moreFilters: "Préciser la recherche",
    contactUs: "Un conseiller vous répond. Appelez, écrivez ou envoyez un WhatsApp.",
    photoHint: "Une photo aide votre conseiller à vous reconnaître.",
    expHint: "Ajoutez les postes que vous avez tenus. Ça nous aide à vous placer.",
    inboxEmpty: "Aucun dossier présenté pour le moment. Confiez un besoin, on revient avec des profils.",
    appsHint: "Chaque candidature est suivie par votre conseiller.",
    profileLead: "Plus c’est clair, plus vite un conseiller peut vous rappeler pour un vrai mandat.",
    companyLead: "Tenez la fiche à jour pour qu’on briefe les bonnes personnes.",
    needLead: "Décrivez le poste. Un conseiller ouvre la recherche et vous rappelle.",
    country: "Pays",
    birth: "Date de naissance",
    startDate: "Date de début",
    experienceLevel: "Niveau d’expérience",
    editNeed: "Modifier ce besoin",
    legalName: "Raison sociale",
    linkedin: "LinkedIn"
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
    jobCity: "",
    jobSector: "",
    jobContract: "",
    need: null,
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
      dashboard: "home", home: "home", profile: "profile", documents: "cv", cv: "cv", resume: "cv",
      settings: "settings", account: "settings", applications: "apps", candidatures: "apps",
      application: "app", apps: "apps", saved: "saved", sauvegardees: "saved", alerts: "alerts",
      alertes: "alerts", notifications: "notifs", notifs: "notifs", entretiens: "interviews",
      interviews: "interviews", pipeline: "pipeline", ats: "pipeline", company: "company",
      billing: "invoices", facturation: "invoices", invoices: "invoices", contrats: "contracts",
      mandats: "contracts", contracts: "contracts", hiring: "hiring", messages: "messages",
      me: "me", jobs: "jobs", job: "job", inbox: "inbox", help: "help", aide: "help",
      need: "need", "hiring-new": "need", "job-new": "need"
    };
    name = aliases[name] || name;
    if (isEmployer()) {
      if (name === "jobs" || name === "job" || name === "job-edit") name = "hiring";
      if (name === "apps" || name === "app") name = "inbox";
      if (name === "profile" || name === "cv") name = "company";
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
    if (isCandidate()) return ["home", "jobs", "job", "apps", "app", "messages", "me", "notifs", "alerts", "saved", "interviews", "settings", "profile", "cv", "help"].indexOf(name) !== -1;
    if (isEmployer()) return ["home", "hiring", "need", "messages", "me", "notifs", "interviews", "inbox", "invoices", "contracts", "pipeline", "company", "settings", "help"].indexOf(name) !== -1;
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
  function statusLabel(s) {
    var key = String(s || "").toUpperCase();
    var fr = {
      SENT: "Envoyée", SUBMITTED: "Envoyée", REVIEW: "À l’étude", UNDER_REVIEW: "À l’étude",
      SHORTLISTED: "Présélection", PRESELECT: "Présélection", INTERVIEW: "Entretien",
      SCHEDULED: "Planifié", CONFIRMED: "Confirmé", CANCELLED: "Annulé", COMPLETED: "Terminé",
      HIRED: "Embauché", REJECTED: "Non retenu", WITHDRAWN: "Retirée", PRESENTED: "Présenté",
      OPEN: "Ouvert", NEW: "Nouveau", IN_PROGRESS: "En cours", CLOSED: "Clos",
      PAID: "Payée", PENDING: "En attente", OVERDUE: "En retard", SENT_INV: "Envoyée",
      PUBLISHED: "Publié", DRAFT: "Brouillon"
    };
    var en = {
      SENT: "Sent", SUBMITTED: "Sent", REVIEW: "Under review", UNDER_REVIEW: "Under review",
      SHORTLISTED: "Shortlist", PRESELECT: "Shortlist", INTERVIEW: "Interview",
      SCHEDULED: "Scheduled", CONFIRMED: "Confirmed", CANCELLED: "Cancelled", COMPLETED: "Done",
      HIRED: "Hired", REJECTED: "Not retained", WITHDRAWN: "Withdrawn", PRESENTED: "Presented",
      OPEN: "Open", NEW: "New", IN_PROGRESS: "In progress", CLOSED: "Closed",
      PAID: "Paid", PENDING: "Pending", OVERDUE: "Overdue", PUBLISHED: "Published", DRAFT: "Draft"
    };
    return (isEn ? en : fr)[key] || s || "";
  }
  function personName(row) {
    return (((row && row.first_name) || "") + " " + ((row && row.last_name) || "")).trim();
  }
  function initialsOf(user) {
    user = user || state.user || {};
    var a = String(user.first_name || "").charAt(0);
    var b = String(user.last_name || "").charAt(0);
    return ((a + b) || String(user.email || "?").charAt(0)).toUpperCase();
  }
  function identityHead() {
    var u = state.user || {};
    var name = personName(u) || t.me;
    return '<div class="tn-identity"><div class="tn-avatar" aria-hidden="true">' + esc(initialsOf(u)) + "</div>" +
      "<div><h1 class=\"tn-title\">" + esc(name) + '</h1><p class="tn-meta">' + esc(u.email || "") + "</p></div></div>";
  }
  function menuGroup(title, items) {
    return "<h2 class=\"tn-section\">" + esc(title) + "</h2>" +
      '<nav class="tn-menu">' + items.map(function (it) {
        var badge = it[2] ? '<span class="tn-menu-badge">' + esc(it[2]) + "</span>" : "";
        return '<a href="' + it[0] + '"><span>' + esc(it[1]) + "</span>" + badge +
          '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>";
      }).join("") + "</nav>";
  }
  function backTo(href) {
    return '<a class="tn-back" href="' + href + '">' + esc(t.back) + "</a>";
  }
  function statLink(href, value, label) {
    return '<a class="tn-stat" href="' + href + '"><b>' + esc(value) + "</b><span>" + esc(label) + "</span></a>";
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
    return '<header class="tn-top"><a class="tn-brand" href="#/home">' + brandOrbit("is-sm") + "<span>Talendus</span></a>" +
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
    var msgUnread = ((state.dash && state.dash.stats && state.dash.stats.unread_messages) || 0);
    return '<nav class="tn-tabs" aria-label="Talendus">' + items.map(function (item) {
      var on = r === item.key;
      if (item.key === "jobs") on = on || r === "job";
      if (item.key === "hiring") on = on || r === "need" || r === "pipeline" || r === "inbox";
      if (item.key === "me") on = on || ["settings", "company", "apps", "app", "profile", "cv", "saved", "alerts", "interviews", "help", "invoices", "contracts"].indexOf(r) !== -1;
      var badge = (item.key === "messages" && msgUnread) ? '<span class="tn-badge">' + msgUnread + "</span>" : "";
      return '<a href="' + item.href + '" class="' + (on ? "is-on" : "") + '">' + item.icon + badge + "<span>" + esc(item.label) + "</span></a>";
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
      var needs = state.hiring || [];
      return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
        flash() +
        '<div class="tn-stats">' +
        statLink("#/hiring", stats.active_jobs || needs.length || 0, t.hiring) +
        statLink("#/inbox", stats.applications || 0, t.presented) +
        statLink("#/interviews", stats.interviews || 0, t.interviews) +
        statLink("#/notifs", stats.unread_notifications || unreadCount(), t.notifs) +
        "</div>" +
        '<a class="tn-btn" href="#/need">' + esc(t.addNeed) + "</a>" +
        interviewCard() +
        (needs.length ? "<h2 class=\"tn-section\">" + esc(t.myNeeds) + "</h2><div class=\"tn-grid\">" +
          needs.slice(0, 3).map(function (row) {
            return '<a class="tn-job" href="#/need/' + encodeURIComponent(row.id) + '"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' +
              esc([row.location, statusLabel(row.status_label || row.status)].filter(Boolean).join(" · ")) + "</p></a>";
          }).join("") + "</div>" : "") +
        dashNotifs();
    }
    var pct = (dash.completeness && dash.completeness.percent) || 0;
    var matches = (dash.matches || []).map(function (row) { return jobCard(row.job || row); }).join("");
    var next = "";
    if (pct < 80) {
      next = '<section class="tn-card tn-file-card"><p class="tn-kicker">' + esc(t.nextStep) + "</p>" +
        '<p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
        '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
        missingChips() +
        '<a class="tn-btn" href="#/profile">' + esc(t.completeFile) + "</a></section>";
    }
    return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
      flash() + next + interviewCard() +
      '<div class="tn-stats">' +
      statLink("#/apps", stats.applications || 0, t.statsApps) +
      statLink("#/interviews", stats.interviews || 0, t.statsInterviews) +
      statLink("#/saved", stats.saved_jobs || (state.saved || []).length, t.savedJobs) +
      statLink("#/notifs", stats.unread_notifications || unreadCount(), t.notifs) +
      "</div>" +
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
      '<form class="tn-search" data-search-jobs>' +
      '<input name="q" placeholder="' + esc(t.search) + '" value="' + esc(state.query || "") + '" enterkeyhint="search">' +
      '<button type="submit">' + esc(t.go) + "</button>" +
      '<div class="tn-filters">' +
      '<input name="location" placeholder="' + esc(t.jobCity) + '" value="' + esc(state.jobCity || "") + '">' +
      '<input name="sector" placeholder="' + esc(t.jobSector) + '" value="' + esc(state.jobSector || "") + '">' +
      '<input name="contract_type" placeholder="' + esc(t.contract) + '" value="' + esc(state.jobContract || "") + '">' +
      "</div></form>" +
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
    return "<h1 class=\"tn-title\">" + esc(t.myNeeds) + "</h1><p class=\"tn-lead\">" + esc(t.hiringLead) + "</p>" + flash() +
      '<a class="tn-btn" href="#/need">' + esc(t.addNeed) + "</a>" +
      '<div class="tn-grid tn-stack">' + (state.hiring.map(function (row) {
        return '<a class="tn-job" href="#/need/' + encodeURIComponent(row.id) + '"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' +
          esc([row.location, row.sector, row.seats ? (row.seats + " " + t.seats) : ""].filter(Boolean).join(" · ")) +
          '</p><span class="tn-status">' + esc(statusLabel(row.status_label || row.status)) + "</span></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyHiring) + "</div>") + "</div>";
  }
  function needView() {
    var r = route();
    var n = r.id ? (state.need || {}) : {};
    if (r.id && !state.need) return backTo("#/hiring") + '<div class="tn-empty">' + esc(t.loading) + "</div>";
    return backTo("#/hiring") + "<h1 class=\"tn-title\">" + esc(r.id ? t.editNeed : t.addNeed) + "</h1><p class=\"tn-lead\">" + esc(t.needLead) + "</p>" + flash() +
      '<form class="tn-form" data-hiring' + (r.id ? ' data-id="' + esc(r.id) + '"' : "") + '><label>' + esc(t.needTitle) +
      '</label><input name="title" required placeholder="' + esc(t.needTitle) + '" value="' + esc(n.title || "") + '">' +
      "<label>" + esc(t.location) + '</label><input name="location" autocomplete="address-level2" value="' + esc(n.location || "") + '">' +
      "<label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(n.sector || "") + '">' +
      "<label>" + esc(t.contract) + '</label><input name="contract_type" value="' + esc(n.contract_type || "") + '">' +
      "<label>" + esc(t.experienceLevel) + '</label><input name="experience_level" value="' + esc(n.experience_level || "") + '">' +
      "<label>" + esc(t.seats) + '</label><input name="seats" type="number" min="1" value="' + esc(n.seats || 1) + '">' +
      "<label>" + esc(t.startDate) + '</label><input name="start_date" type="date" value="' + esc(n.start_date || "") + '">' +
      "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(n.skills || "") + '">' +
      "<label>" + esc(t.languages) + '</label><input name="languages" value="' + esc(n.languages || "") + '">' +
      "<label>" + esc(t.salary) + '</label><input name="salary_display" value="' + esc(n.salary_display || "") + '">' +
      "<label>" + esc(t.notes) + '</label><textarea name="notes" placeholder="' + esc(t.notes) + '">' + esc(n.notes || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(r.id ? t.save : t.sendNeed) + "</button></form>";
  }

  function listBlock(title, empty, items, backHref) {
    return (backHref ? backTo(backHref) : "") + "<h1 class=\"tn-title\">" + esc(title) + "</h1>" + flash() + '<div class="tn-grid">' +
      (items && items.length ? items.join("") : '<div class="tn-empty">' + esc(empty) + "</div>") + "</div>";
  }
  function notifsView() {
    return backTo("#/home") + "<h1 class=\"tn-title\">" + esc(t.notifs) + "</h1>" + flash() +
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
      var job = row.job || {};
      return '<div class="tn-job"><h3>' + esc(job.title || row.type_label || t.interviews) + "</h3><p class=\"tn-meta\">" +
        esc([when(row.scheduled_at), row.location, statusLabel(row.status)].filter(Boolean).join(" · ")) + "</p>" + actions + "</div>";
    }), "#/me");
  }
  function savedView() {
    return listBlock(t.savedJobs, t.emptySaved, (state.saved || []).map(function (row) {
      return jobCard(row.job || row);
    }), "#/me");
  }
  function alertsView() {
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.alerts) + "</h1><p class=\"tn-lead\">" + esc(t.emptyAlerts) + "</p>" + flash() +
      '<form class="tn-form" data-alert><label>' + esc(t.alertKeywords) + '</label><input name="keywords" required>' +
      "<label>" + esc(t.city) + '</label><input name="city">' +
      "<label>" + esc(t.sector) + '</label><input name="sector">' +
      '<button class="tn-btn" type="submit">' + esc(t.createAlert) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + ((state.alerts || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.keywords || row.city || t.alerts) + '</h3><p class="tn-meta">' +
          esc([row.city, row.sector, row.contract_type].filter(Boolean).join(" · ")) +
          '</p><button type="button" class="tn-btn tn-btn-ghost" data-del-alert="' + esc(row.id) + '">' + esc(t.deleteAlert) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyAlerts) + "</div>") + "</div>";
  }
  function inboxView() {
    var r = route();
    if (r.id) return inboxDetail();
    return listBlock(t.presented, t.inboxEmpty, (state.inbox || []).map(function (a) {
      var job = a.job || {};
      var cand = a.candidate || {};
      var label = personName(cand) || cand.title || t.candidate;
      return '<a class="tn-job" href="#/inbox/' + encodeURIComponent(a.id) + '"><h3>' + esc(label) +
        '</h3><p class="tn-meta">' + esc([cand.title, job.title, cand.city].filter(Boolean).join(" · ")) +
        '</p><span class="tn-status">' + esc(statusLabel(a.status || a.pipeline_stage)) + "</span></a>";
    }), "#/hiring");
  }
  function inboxDetail() {
    var a = state.application;
    if (!a) return '<div class="tn-empty">' + esc(t.loading) + "</div>";
    var job = a.job || {};
    var cand = a.candidate || {};
    return backTo("#/inbox") + "<h1 class=\"tn-title\">" + esc(personName(cand) || t.presentedFile) + "</h1>" +
      '<p class="tn-meta">' + esc([cand.title, cand.city, job.title].filter(Boolean).join(" · ")) + "</p>" +
      '<span class="tn-status">' + esc(statusLabel(a.status)) + "</span>" + flash() +
      (cand.skills ? '<div class="tn-card"><p>' + esc(cand.skills) + "</p></div>" : "") +
      (a.cover_note ? '<div class="tn-card"><p>' + esc(a.cover_note) + "</p></div>" : "") +
      '<a class="tn-btn tn-btn-ghost" href="#/messages">' + esc(t.messages) + "</a>";
  }
  function pipelineView() {
    var groups = {};
    (state.inbox || []).forEach(function (a) {
      var key = a.pipeline_stage || a.status || t.presented;
      (groups[key] = groups[key] || []).push(a);
    });
    var keys = Object.keys(groups);
    if (!keys.length) return listBlock(t.pipeline, t.emptyPipeline, [], "#/hiring");
    return backTo("#/hiring") + "<h1 class=\"tn-title\">" + esc(t.pipeline) + "</h1>" + flash() + keys.map(function (key) {
      return "<h2 class=\"tn-section\">" + esc(statusLabel(key) || key) + "</h2><div class=\"tn-grid\">" + groups[key].map(function (a) {
        var job = a.job || {};
        var cand = a.candidate || {};
        var label = personName(cand) || job.title || t.presented;
        return '<a class="tn-job" href="#/inbox/' + encodeURIComponent(a.id) + '"><h3>' + esc(label) +
          '</h3><p class="tn-meta">' + esc([cand.title, job.title].filter(Boolean).join(" · ")) +
          '</p><span class="tn-status">' + esc(statusLabel(a.status || "")) + "</span></a>";
      }).join("") + "</div>";
    }).join("");
  }
  function appView() {
    var a = state.application;
    if (!a) return '<div class="tn-empty">' + esc(t.loading) + "</div>";
    var job = a.job || {};
    var hist = (a.history || []).map(function (h) {
      return '<p class="tn-meta">' + esc(when(h.created_at) + " · " + statusLabel(h.new_status || "")) + "</p>";
    }).join("");
    return backTo("#/apps") + "<h1 class=\"tn-title\">" + esc(job.title || t.appDetail) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, statusLabel(a.status)].filter(Boolean).join(" · ")) + "</p>" + flash() +
      (a.cover_note ? '<div class="tn-card"><p>' + esc(a.cover_note) + "</p></div>" : "") +
      "<h2 class=\"tn-section\">" + esc(t.history) + "</h2>" + (hist || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") +
      (a.status === "WITHDRAWN" ? "" : '<button type="button" class="tn-btn tn-btn-ghost" data-withdraw="' + esc(a.id) + '">' + esc(t.withdraw) + "</button>");
  }
  function companyView() {
    var c = state.company || {};
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.companyProfile) + "</h1><p class=\"tn-lead\">" + esc(t.companyLead) + "</p>" + flash() +
      '<form class="tn-form" data-company data-id="' + esc(c.id || "") + '"><label>' + esc(t.company) +
      '</label><input name="name" value="' + esc(c.name || "") + '" required>' +
      "<label>" + esc(t.city) + '</label><input name="city" value="' + esc(c.city || "") + '">' +
      "<label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(c.sector || "") + '">' +
      "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(c.address || "") + '">' +
      "<label>" + esc(t.country) + '</label><input name="country" value="' + esc(c.country || "Canada") + '">' +
      "<label>" + esc(t.website) + '</label><input name="website" value="' + esc(c.website || "") + '" inputmode="url">' +
      "<label>" + esc(t.email) + '</label><input name="email" type="email" value="' + esc(c.email || "") + '">' +
      "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(c.phone || "") + '" inputmode="tel">' +
      "<label>" + esc(t.size) + '</label><input name="size_label" value="' + esc(c.size_label || "") + '">' +
      "<label>" + esc(t.legalName) + '</label><input name="legal_name" value="' + esc(c.legal_name || "") + '">' +
      "<label>" + esc(t.linkedin) + '</label><input name="linkedin_url" value="' + esc(c.linkedin_url || "") + '">' +
      "<label>" + esc(t.description) + '</label><textarea name="description">' + esc(c.description || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>";
  }
  function settingsView() {
    var p = state.prefs || {};
    function check(name, label, on) {
      return '<label class="tn-check"><input type="checkbox" name="' + name + '"' + (on ? " checked" : "") + "> " + esc(label) + "</label>";
    }
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.settings) + "</h1>" + flash() +
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
        esc(money(inv.amount) + " · " + statusLabel(inv.status || "")) + '</p><div class="tn-row-actions">' +
        (payable ? '<button type="button" class="tn-btn" data-pay="' + esc(inv.id) + '">' + esc(t.pay) + "</button>" : "") +
        '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="invoices" data-id="' +
        esc(inv.id) + '">' + esc(t.downloadPdf) + "</button></div></div>";
    }), "#/me");
  }
  function contractsView() {
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.contracts) + "</h1>" + flash() + '<div class="tn-grid">' +
      ((state.contracts || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.document_name || row.type || t.contracts) + '</h3><p class="tn-meta">' +
          esc(row.signed ? t.signed : t.unsigned) + "</p>" +
          (row.signed ? "" : '<button type="button" class="tn-btn" data-sign="' + esc(row.id) + '">' + esc(t.sign) + "</button>") +
          '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="contracts" data-id="' + esc(row.id) + '">' + esc(t.downloadPdf) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyContracts) + "</div>") + "</div>";
  }

  function appsView() {
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.apps) + "</h1><p class=\"tn-lead\">" + esc(t.appsHint) + "</p>" + flash() +
      '<div class="tn-grid">' + (state.apps.map(function (a) {
        var job = a.job || {};
        return '<a class="tn-job" href="#/app/' + encodeURIComponent(a.id) + '"><h3>' + esc(job.title || t.apps) +
          '</h3><p class="tn-meta">' + esc(job.location || "") + '</p><span class="tn-status">' + esc(statusLabel(a.status)) + "</span></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") + "</div>";
  }
  function profileView() {
    var u = state.user || {};
    var p = state.profile || {};
    function listBlockMini(title, rows, emptyTxt, formAttrs, fields, delAttr) {
      var items = (rows || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.role || row.diploma || row.name || "") + "</h3><p class=\"tn-meta\">" +
          esc([row.company, row.school, row.issuer, row.years, row.year].filter(Boolean).join(" · ")) +
          '</p><button type="button" class="tn-btn tn-btn-ghost" ' + delAttr + '="' + esc(row.id) + '">' + esc(t.remove) + "</button></div>";
      }).join("");
      return "<h2 class=\"tn-section\">" + esc(title) + "</h2>" + (items || '<p class="tn-meta">' + esc(emptyTxt) + "</p>") +
        '<form class="tn-form" ' + formAttrs + ">" + fields + '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.add) + "</button></form>";
    }
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.profile) + "</h1><p class=\"tn-lead\">" + esc(t.profileLead) + "</p>" + flash() +
      '<form class="tn-form" data-avatar><label>' + esc(t.photo) + '</label><p class="tn-meta">' + esc(t.photoHint) + "</p>" +
      '<input type="file" name="file" accept="image/jpeg,image/png,image/webp">' +
      '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.save) + "</button></form>" +
      '<form class="tn-form" data-profile>' +
      "<label>" + esc(t.first) + '</label><input name="first_name" value="' + esc(u.first_name || "") + '" autocomplete="given-name">' +
      "<label>" + esc(t.last) + '</label><input name="last_name" value="' + esc(u.last_name || "") + '" autocomplete="family-name">' +
      "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(u.phone || p.phone || "") + '" inputmode="tel">' +
      "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(p.address || "") + '" autocomplete="street-address">' +
      "<label>" + esc(t.city) + '</label><input name="city" value="' + esc(p.city || "") + '" autocomplete="address-level2">' +
      "<label>" + esc(t.province) + '</label><input name="province" value="' + esc(p.province || "") + '">' +
      "<label>" + esc(t.country) + '</label><input name="country" value="' + esc(p.country || "Canada") + '">' +
      "<label>" + esc(t.birth) + '</label><input name="birth_date" type="date" value="' + esc(p.birth_date || "") + '">' +
      "<label>" + esc(t.title) + '</label><input name="title" value="' + esc(p.title || "") + '">' +
      "<label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(p.sector || "") + '">' +
      "<label>" + esc(t.experience) + '</label><input name="years_experience" type="number" min="0" value="' + esc(p.years_experience || "") + '">' +
      "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(p.skills || "") + '">' +
      "<label>" + esc(t.languages) + '</label><input name="languages" value="' + esc(p.languages || "") + '">' +
      "<label>" + esc(t.availability) + '</label><input name="availability" value="' + esc(p.availability || "") + '">' +
      "<label>" + esc(t.contract) + '</label><input name="contract_type" value="' + esc(p.contract_type || "") + '">' +
      "<label>" + esc(t.salary) + '</label><input name="desired_salary_min" type="number" value="' + esc(p.desired_salary_min || "") + '">' +
      "<label>" + esc(t.mobility) + '</label><input name="mobility" value="' + esc(p.mobility || "") + '">' +
      "<label>" + esc(t.bio) + '</label><textarea name="bio">' + esc(p.bio || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>" +
      listBlockMini(t.experience, p.experiences, t.expHint, "data-exp",
        "<label>" + esc(t.companyName) + '</label><input name="company" required>' +
        "<label>" + esc(t.roleHeld) + '</label><input name="role" required>' +
        "<label>" + esc(t.years) + '</label><input name="years">', "data-del-exp") +
      listBlockMini(t.education, p.education, "", "data-edu",
        "<label>" + esc(t.school) + '</label><input name="school" required>' +
        "<label>" + esc(t.diploma) + '</label><input name="diploma">', "data-del-edu") +
      listBlockMini(t.certs, p.certifications, "", "data-cert",
        "<label>" + esc(t.certs) + '</label><input name="name" required>', "data-del-cert");
  }
  function cvView() {
    var p = state.profile || {};
    var resumes = p.resumes || [];
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.documents) + "</h1>" + flash() +
      '<form class="tn-form" data-cv><label>' + esc(t.cv) + '</label><input type="file" name="file" accept=".pdf,.doc,.docx,application/pdf,image/png,image/jpeg" required>' +
      '<button class="tn-btn" type="submit">' + esc(t.upload) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + (resumes.map(function (r) {
        return '<div class="tn-job"><h3>' + esc(r.original_name || t.cv) + '</h3><p class="tn-meta">' +
          esc(r.is_primary ? t.cvReady : when(r.created_at)) + '</p><div class="tn-row-actions">' +
          '<button type="button" class="tn-btn" data-dl-cv="' + esc(r.id) + '">' + esc(t.downloadCv) + "</button>" +
          '<button type="button" class="tn-btn tn-btn-ghost" data-del-cv="' + esc(r.id) + '">' + esc(t.remove) + "</button></div></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.noCv) + "</div>") + "</div>";
  }
  function helpView() {
    var mail = (state.contact && state.contact.email) || "info@talendus.ca";
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.helpTitle) + "</h1><p class=\"tn-lead\">" + esc(t.contactUs) + "</p>" +
      '<div class="tn-help-actions">' +
      '<a class="tn-btn" href="' + telHref() + '">' + esc(t.call) + " · " + esc(state.contact.phone_display || "") + "</a>" +
      '<a class="tn-btn tn-btn-ghost" href="' + waHref() + '">' + esc(t.wa) + "</a>" +
      '<a class="tn-btn tn-btn-ghost" href="mailto:' + esc(mail) + '">' + esc(t.emailUs) + " · " + esc(mail) + "</a></div>";
  }
  function meView() {
    var html = identityHead() + flash();
    if (isCandidate()) {
      var pct = ((state.dash && state.dash.completeness && state.dash.completeness.percent) || 0);
      html += '<p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
        '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
        menuGroup(t.groupFile, [["#/profile", t.profile], ["#/cv", t.documents], ["#/apps", t.apps, state.apps.length || ""], ["#/saved", t.savedJobs], ["#/alerts", t.alerts]]) +
        menuGroup(t.groupFollow, [["#/interviews", t.interviews], ["#/notifs", t.notifs, unreadCount() || ""], ["#/messages", t.messages]]) +
        menuGroup(t.groupAccount, [["#/settings", t.settings], ["#/help", t.helpTitle]]);
    } else {
      var stats = (state.dash && state.dash.stats) || {};
      html += '<p class="tn-meta">' + esc((state.dash && state.dash.company_name) || "") + "</p>" +
        menuGroup(t.groupHire, [["#/need", t.addNeed], ["#/hiring", t.myNeeds, (state.hiring || []).length || ""], ["#/inbox", t.presented, stats.applications || ""], ["#/pipeline", t.pipeline], ["#/interviews", t.interviews]]) +
        menuGroup(t.groupCompany, [["#/company", t.companyProfile], ["#/contracts", t.contracts], ["#/invoices", t.invoices]]) +
        menuGroup(t.groupAccount, [["#/settings", t.settings], ["#/help", t.helpTitle]]);
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
      if (name === "apps") return appsView();
      if (name === "app") return appView();
      if (name === "profile") return profileView();
      if (name === "cv") return cvView();
      if (name === "help") return helpView();
      if (name === "settings") return settingsView();
      if (name === "me") return meView();
      return homeView();
    }
    if (name === "hiring") return hiringView();
    if (name === "need") return needView();
    if (name === "messages") return messagesView();
    if (name === "notifs") return notifsView();
    if (name === "interviews") return interviewsView();
    if (name === "inbox") return inboxView();
    if (name === "pipeline") return pipelineView();
    if (name === "invoices") return invoicesView();
    if (name === "contracts") return contractsView();
    if (name === "company") return companyView();
    if (name === "settings") return settingsView();
    if (name === "help") return helpView();
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
    var extra = arguments[1] || {};
    if (q != null) state.query = q || "";
    if (extra.location != null) state.jobCity = extra.location;
    if (extra.sector != null) state.jobSector = extra.sector;
    if (extra.contract_type != null) state.jobContract = extra.contract_type;
    var key = "jobs:" + (state.query || "") + ":" + (state.jobCity || "") + ":" + (state.jobSector || "") + ":" + (state.jobContract || "");
    if (isFresh(key) && state.jobs && state.jobs.length) return Promise.resolve();
    return api.jobs({
      q: state.query || "",
      location: state.jobCity || "",
      sector: state.jobSector || "",
      contract_type: state.jobContract || "",
      page_size: 20,
      sort: "published_at"
    }).then(function (json) {
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
      if (name === "me" || name === "profile" || name === "cv") {
        need("profile", function () { return api.profile(); }, "profile", false);
      }
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
      if (name === "home" || name === "hiring" || name === "need" || name === "me") {
        need("hiring", function () { return api.request("/hiring-requests"); }, "hiring", true);
      }
      if (name === "inbox" || name === "pipeline") {
        need("inbox", function () { return api.request("/applications"); }, "inbox", true);
      }
      if (name === "invoices") need("invoices", function () { return api.request("/invoices"); }, "invoices", true);
      if (name === "contracts") need("contracts", function () { return api.request("/contracts"); }, "contracts", true);
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
    if (state.user && isEmployer() && r.name === "inbox" && r.id) {
      pending.push(api.request("/applications/" + encodeURIComponent(r.id)).then(function (json) { state.application = dataOf(json); }).catch(function () { state.application = null; }));
    }
    if (state.user && isEmployer() && r.name === "need" && r.id) {
      pending.push(api.request("/hiring-requests/" + encodeURIComponent(r.id)).then(function (json) { state.need = dataOf(json); }).catch(function () { state.need = null; }));
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
    var delRow = e.target.closest("[data-del-exp], [data-del-edu], [data-del-cert]");
    if (delRow) {
      e.preventDefault();
      if (!isCandidate()) return;
      var kind = delRow.hasAttribute("data-del-exp") ? "experiences" : (delRow.hasAttribute("data-del-edu") ? "education" : "certifications");
      var rid = delRow.getAttribute("data-del-exp") || delRow.getAttribute("data-del-edu") || delRow.getAttribute("data-del-cert");
      api.request("/candidates/me/" + kind + "/" + rid, { method: "DELETE" }).then(function () { done(t.saved); }).catch(fail);
    }
    var delCv = e.target.closest("[data-del-cv]");
    if (delCv) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/resume/" + delCv.getAttribute("data-del-cv"), { method: "DELETE" }).then(function () { done(t.saved); }).catch(fail);
    }
    var dlCv = e.target.closest("[data-dl-cv]");
    if (dlCv) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.download("/candidates/resumes/" + dlCv.getAttribute("data-dl-cv") + "/file", "cv.pdf").catch(fail);
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
      var fd = new FormData(form);
      loadJobs(fd.get("q") != null ? fd.get("q") : state.query, {
        location: fd.get("location") != null ? fd.get("location") : state.jobCity,
        sector: fd.get("sector") != null ? fd.get("sector") : state.jobSector,
        contract_type: fd.get("contract_type") != null ? fd.get("contract_type") : state.jobContract
      }).then(function () { go("#/jobs"); render(); });
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
      var hire = Object.fromEntries(new FormData(form).entries());
      if (hire.seats) hire.seats = Number(hire.seats) || 1;
      var hid = form.getAttribute("data-id");
      var req = hid
        ? api.request("/hiring-requests/" + hid, { method: "PATCH", body: hire })
        : api.request("/hiring-requests", { method: "POST", body: hire });
      req.then(function () {
        setNotice(hid ? t.saved : t.needSent);
        bustCache();
        go("#/hiring");
        return loadRoute();
      }).catch(fail);
    } else if (form.matches("[data-profile]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var d = Object.fromEntries(new FormData(form).entries());
      Promise.all([
        api.request("/users/me", { method: "PATCH", body: { first_name: d.first_name, last_name: d.last_name, phone: d.phone } }),
        api.updateProfile({
          city: d.city, province: d.province, country: d.country, address: d.address, birth_date: d.birth_date,
          title: d.title, sector: d.sector, skills: d.skills,
          bio: d.bio, languages: d.languages, availability: d.availability, contract_type: d.contract_type,
          mobility: d.mobility,
          years_experience: d.years_experience ? Number(d.years_experience) : null,
          desired_salary_min: d.desired_salary_min ? Number(d.desired_salary_min) : null
        })
      ]).then(function () { return api.me(); }).then(function (json) {
        var user = dataOf(json);
        if (user) state.user = user;
        done(t.saved);
      }).catch(fail);
    } else if (form.matches("[data-avatar]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var photo = form.file && form.file.files && form.file.files[0];
      if (!photo) return;
      var av = new FormData();
      av.append("file", photo);
      api.request("/users/me/avatar", { method: "POST", body: av }).then(function () { done(t.saved); }).catch(fail);
    } else if (form.matches("[data-exp]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/experiences", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-edu]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/education", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-cert]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/certifications", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
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
      var body = Object.fromEntries(new FormData(form).entries());
      if (!body.email) delete body.email;
      api.request("/companies/" + cid, { method: "PATCH", body: body })
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
