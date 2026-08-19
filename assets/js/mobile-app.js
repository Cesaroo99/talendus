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
    talent: "I am looking for work",
    talentHint: "A consultant presents you. Companies never get your email or phone.",
    employer: "I want to hire",
    employerHint: "Hand us a need. Talendus searches and presents the files.",
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
    emptyMsgs: "Write to your consultant. That is your only contact.",
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
    mediate: "Companies never receive your contact details.",
    mediateEmployer: "You do not contact candidates directly. Talendus presents the files.",
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
    changeChoice: "Change"
  } : {
    home: "Accueil",
    jobs: "Offres",
    hiring: "Besoins",
    messages: "Messages",
    me: "Moi",
    hello: "Bonjour",
    welcomeTitle: "Comment Talendus peut vous aider ?",
    welcomeLead: "Choisissez une fois. Ensuite, vous ne voyez que ce qui correspond à votre situation.",
    talent: "Je cherche un emploi",
    talentHint: "Un conseiller vous présente. Les entreprises n’ont jamais votre courriel ni votre téléphone.",
    employer: "Je recrute",
    employerHint: "Vous confiez un besoin. Talendus cherche et vous présente les dossiers.",
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
    emptyMsgs: "Écrivez à votre conseiller. C’est votre seul contact.",
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
    mediate: "Les entreprises n’ont jamais vos coordonnées.",
    mediateEmployer: "Vous n’écrivez pas aux candidats. Talendus présente les dossiers.",
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
    changeChoice: "Changer"
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
    hire: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6h8v2"/><path d="M12 12v4"/><path d="M10 14h4"/></svg>'
  };

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
  function isEmployer(user) {
    user = user || state.user;
    return !!(user && (user.role === "EMPLOYER" || user.role === "RECRUITER" || user.role === "ADMIN" || user.role === "SUPER_ADMIN"));
  }
  function isCandidate(user) {
    user = user || state.user;
    return !!(user && user.role === "CANDIDATE");
  }
  function route() {
    var raw = (location.hash || "").replace(/^#/, "");
    var parts = raw.replace(/^\//, "").split("/").filter(Boolean);
    var name = parts[0];
    if (!name) name = state.user ? "home" : "welcome";
    return { name: name, id: decodeURIComponent(parts.slice(1).join("/")) };
  }
  function allowedRoute(name) {
    if (!state.user) return name === "welcome" || name === "login" || name === "register";
    if (isCandidate()) return ["home", "jobs", "job", "apps", "messages", "me"].indexOf(name) !== -1;
    if (isEmployer()) return ["home", "hiring", "messages", "me"].indexOf(name) !== -1;
    return name === "home" || name === "me" || name === "messages";
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

  function topBar() {
    return '<header class="tn-top"><div class="tn-brand"><img src="/assets/img/logo/icon-192.png" width="32" height="32" alt=""><span>Talendus</span></div>' +
      '<a class="tn-icon-btn" href="' + telHref() + '" aria-label="' + esc(t.call) + '">' + icons.phone + "</a></header>";
  }
  function gateBar() {
    return '<header class="tn-top tn-top-gate"><div class="tn-brand"><img src="/assets/img/logo/icon-192.png" width="32" height="32" alt=""><span>Talendus</span></div></header>';
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
      var on = r === item.key || (item.key === "jobs" && r === "job");
      return '<a href="' + item.href + '" class="' + (on ? "is-on" : "") + '">' + item.icon + "<span>" + esc(item.label) + "</span></a>";
    }).join("") + "</nav>";
  }

  function welcomeView() {
    return '<div class="tn-gate">' +
      "<h1 class=\"tn-title\">" + esc(t.welcomeTitle) + "</h1>" +
      '<p class="tn-lead">' + esc(t.welcomeLead) + "</p>" +
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
    if (login) {
      return back + "<h1 class=\"tn-title\">" + esc(title) + "</h1><p class=\"tn-lead\">" + esc(lead) + "</p>" + flash() +
        '<form class="tn-form" data-login>' +
        "<label for=\"tn-email\">" + esc(t.email) + '</label><input id="tn-email" name="email" type="email" autocomplete="username" inputmode="email" required>' +
        "<label for=\"tn-pass\">" + esc(t.password) + '</label><input id="tn-pass" name="password" type="password" autocomplete="current-password" required minlength="8">' +
        '<button class="tn-btn" type="submit">' + esc(t.submitLogin) + "</button></form>" +
        '<p class="tn-note">' + esc(t.needAccount) + ' <a href="#/welcome">' + esc(t.changeChoice) + "</a></p>" +
        helpLine();
    }
    return back + "<h1 class=\"tn-title\">" + esc(title) + "</h1><p class=\"tn-lead\">" + esc(lead) + "</p>" + flash() +
      '<form class="tn-form" data-register data-role="' + (employer ? "EMPLOYER" : "CANDIDATE") + '">' +
      "<label>" + esc(t.first) + '</label><input name="first_name" autocomplete="given-name" required>' +
      "<label>" + esc(t.last) + '</label><input name="last_name" autocomplete="family-name" required>' +
      "<label>" + esc(t.email) + '</label><input name="email" type="email" autocomplete="email" inputmode="email" required>' +
      "<label>" + esc(t.password) + '</label><input name="password" type="password" autocomplete="new-password" required minlength="8">' +
      (employer ? "<label>" + esc(t.company) + '</label><input name="company_name" autocomplete="organization" required>' : "") +
      '<button class="tn-btn" type="submit">' + esc(t.submitRegister) + "</button></form>" +
      '<p class="tn-note">' + esc(t.haveAccount) + ' <a href="#/login">' + esc(t.login) + "</a></p>" +
      helpLine();
  }

  function jobCard(job) {
    if (!job) return "";
    return '<a class="tn-job" href="#/job/' + encodeURIComponent(job.slug || job.id) + '"><h3>' + esc(job.title) + "</h3>" +
      '<p class="tn-meta">' + esc([job.location, job.sector || job.employment_type, job.salary || job.salary_display].filter(Boolean).join(" · ")) + "</p></a>";
  }

  function homeView() {
    var name = (state.user && state.user.first_name) || "";
    var dash = state.dash || {};
    var stats = dash.stats || {};
    if (isEmployer()) {
      return "<h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
        '<p class="tn-lead">' + esc(t.mediateEmployer) + "</p>" + flash() +
        '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.active_jobs || state.hiring.length || 0) + "</b><span>" + esc(t.hiring) + "</span></div>" +
        '<div class="tn-stat"><b>' + esc(stats.applications || 0) + "</b><span>" + esc(t.presented) + "</span></div></div>" +
        '<a class="tn-btn" href="#/hiring">' + esc(t.newNeed) + "</a>";
    }
    var pct = (dash.completeness && dash.completeness.percent) || 0;
    var matches = (dash.matches || []).map(function (row) { return jobCard(row.job || row); }).join("");
    return "<h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
      '<p class="tn-note">' + esc(t.mediate) + "</p>" + flash() +
      '<section class="tn-card tn-file-card"><p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
      '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
      '<a class="tn-btn tn-btn-ghost" href="#/me">' + esc(t.completeFile) + "</a></section>" +
      '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.applications || 0) + "</b><span>" + esc(t.statsApps) + "</span></div>" +
      '<div class="tn-stat"><b>' + esc(stats.interviews || 0) + "</b><span>" + esc(t.statsInterviews) + "</span></div></div>" +
      "<h2 class=\"tn-section\">" + esc(t.nextJob) + "</h2>" +
      '<div class="tn-grid">' + (matches || state.jobs.slice(0, 4).map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>" +
      '<a class="tn-text-link" href="#/jobs">' + esc(t.openJobs) + "</a>";
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
    return '<a class="tn-back" href="#/jobs">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(job.title) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, job.sector, job.contract_type, job.salary_display].filter(Boolean).join(" · ")) + "</p>" +
      '<div class="tn-card"><p>' + esc(body) + "</p></div>" + flash() +
      '<button class="tn-btn" data-apply="' + esc(job.id) + '">' + esc(t.apply) + "</button>";
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

  function meView() {
    var html = "<h1 class=\"tn-title\">" + esc(((state.user.first_name || "") + " " + (state.user.last_name || "")).trim() || t.me) + "</h1>" +
      '<p class="tn-meta">' + esc(state.user.email || "") + "</p>" + flash();
    if (isCandidate()) {
      var p = state.profile || {};
      html += '<p class="tn-note">' + esc(t.mediate) + "</p>" +
        '<form class="tn-form" data-profile><label>' + esc(t.city) + '</label><input name="city" value="' + esc(p.city || "") + '" autocomplete="address-level2">' +
        "<label>" + esc(t.title) + '</label><input name="title" value="' + esc(p.title || "") + '">' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(p.skills || "") + '">' +
        '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>" +
        '<form class="tn-form" data-cv><label>' + esc(t.cv) + '</label><input type="file" name="file" accept=".pdf,.doc,.docx,application/pdf">' +
        '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.upload) + "</button></form>" +
        "<h2 class=\"tn-section\">" + esc(t.apps) + "</h2><div class=\"tn-grid\">" +
        (state.apps.map(function (a) {
          var job = a.job || {};
          return '<div class="tn-job"><h3>' + esc(job.title || t.apps) + '</h3><span class="tn-status">' + esc(a.status || "") + "</span></div>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") + "</div>";
    } else {
      html += '<p class="tn-note">' + esc(t.mediateEmployer) + "</p>" +
        '<p class="tn-meta">' + esc((state.dash && state.dash.company_name) || "") + "</p>" +
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
      if (name === "me" || name === "apps") return meView();
      return homeView();
    }
    if (name === "hiring") return hiringView();
    if (name === "messages") return messagesView();
    if (name === "me") return meView();
    return homeView();
  }

  function render() {
    document.body.classList.toggle("tn-gated", !state.user);
    var chrome = state.user ? topBar() : gateBar();
    root.innerHTML = chrome + '<main id="tn-screen" class="tn-screen">' + screenHtml() + "</main>" + tabs();
  }

  function loadJobs(q) {
    state.query = q || "";
    return api.jobs({ q: q || "", page_size: 20, sort: "published_at" }).then(function (json) {
      state.jobs = dataOf(json) || [];
    }).catch(function () { state.jobs = []; });
  }

  function loadSessionData() {
    state.user = api.currentUser();
    if (!state.user) {
      state.dash = null;
      state.jobs = [];
      return Promise.resolve();
    }
    var tasks = [
      api.request("/messages").then(function (json) { state.threads = dataOf(json) || []; }).catch(function () { state.threads = []; }),
      api.request("/messages/directory").then(function (json) { state.directory = dataOf(json) || []; }).catch(function () { state.directory = []; })
    ];
    if (isCandidate()) {
      tasks.push(api.request("/candidates/me/dashboard").then(function (json) { state.dash = dataOf(json); }).catch(function () {}));
      tasks.push(api.profile().then(function (json) { state.profile = dataOf(json); }).catch(function () {}));
      tasks.push(api.myApplications().then(function (json) { state.apps = dataOf(json) || []; }).catch(function () { state.apps = []; }));
    } else if (isEmployer()) {
      tasks.push(api.request("/companies/me/dashboard").then(function (json) { state.dash = dataOf(json); }).catch(function () {}));
      tasks.push(api.request("/hiring-requests").then(function (json) { state.hiring = dataOf(json) || []; }).catch(function () { state.hiring = []; }));
    }
    return Promise.all(tasks);
  }

  function syncHash() {
    var r = route();
    if (allowedRoute(r.name)) return true;
    var fallback = state.user ? "#/home" : "#/welcome";
    if ((location.hash || "") !== fallback) {
      location.replace(fallback);
      return false;
    }
    return true;
  }

  function loadRoute() {
    state.user = api.currentUser();
    if (!syncHash()) return Promise.resolve();
    var r = route();
    var pending = [loadSessionData()];
    if (state.user && isCandidate() && (r.name === "home" || r.name === "jobs")) pending.push(loadJobs(state.query));
    if (state.user && isCandidate() && r.name === "job" && r.id) {
      pending.push(api.request("/jobs/" + encodeURIComponent(r.id)).then(function (json) { state.job = dataOf(json); }).catch(function () { state.job = null; }));
    }
    if (state.user && r.name === "messages" && r.id) {
      pending.push(api.request("/messages/" + encodeURIComponent(r.id)).then(function (json) { state.conversation = dataOf(json) || []; }).catch(function () { state.conversation = []; }));
    }
    return Promise.all(pending).then(function () {
      if (!syncHash()) return;
      render();
    });
  }

  function afterAuth() {
    var user = api.currentUser();
    var chosen = getPersona();
    state.mismatch = "";
    if (chosen === "talent" && isEmployer(user)) state.mismatch = t.wrongPersonaEmployer;
    if (chosen === "employer" && isCandidate(user)) state.mismatch = t.wrongPersonaTalent;
    setNotice("");
    go("#/home");
    return loadRoute();
  }

  root.addEventListener("click", function (e) {
    var choose = e.target.closest("[data-choose]");
    if (choose) setPersona(choose.getAttribute("data-choose"));
    var applyBtn = e.target.closest("[data-apply]");
    if (applyBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.apply({ job_id: applyBtn.getAttribute("data-apply") }).then(function () {
        setNotice(t.applied);
        render();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    }
    if (e.target.closest("[data-logout]")) {
      e.preventDefault();
      api.logout().then(function () {
        state.user = null;
        state.mismatch = "";
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
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-register]")) {
      e.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      data.role = form.getAttribute("data-role") || (getPersona() === "employer" ? "EMPLOYER" : "CANDIDATE");
      api.register(data).then(afterAuth)
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-send-msg]")) {
      e.preventDefault();
      if (!state.user) return;
      api.request("/messages", { method: "POST", body: { recipient_id: form.getAttribute("data-to"), body: new FormData(form).get("body") } }).then(function () {
        form.reset();
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-hiring]")) {
      e.preventDefault();
      if (!isEmployer()) return;
      api.request("/hiring-requests", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) }).then(function () {
        setNotice(t.needSent);
        form.reset();
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-profile]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.updateProfile(Object.fromEntries(new FormData(form).entries())).then(function () { setNotice(t.saved); loadRoute(); })
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-cv]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var file = form.file && form.file.files && form.file.files[0];
      if (!file) return;
      var payload = new FormData();
      payload.append("file", file);
      api.uploadResume(payload).then(function () { setNotice(t.saved); loadRoute(); })
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    }
  });

  window.addEventListener("hashchange", loadRoute);
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
  }
  api.services().then(function (json) {
    var data = dataOf(json) || {};
    if (data.contact) state.contact = data.contact;
  }).catch(function () {}).then(loadRoute);
})();
