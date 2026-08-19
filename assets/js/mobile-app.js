(function () {
  var api = window.TalendusAPI;
  if (!api) return;
  var root = document.getElementById("tl-native-app");
  if (!root) return;

  var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  var t = isEn ? {
    home: "Home",
    jobs: "Jobs",
    hiring: "Hiring",
    messages: "Messages",
    me: "Account",
    hello: "Hello",
    guestTitle: "Talendus on your phone",
    guestLead: "Jobs, your file, and your consultant — without the website around it.",
    talent: "I am looking for work",
    employer: "I want to hire",
    recentJobs: "Open roles",
    call: "Call Talendus",
    wa: "WhatsApp",
    search: "Search a role",
    go: "Search",
    emptyJobs: "No roles to show yet.",
    apply: "Ask Talendus to present me",
    applied: "Request sent to Talendus.",
    login: "Sign in",
    register: "Create an account",
    logout: "Sign out",
    email: "Email",
    password: "Password",
    first: "First name",
    last: "Last name",
    company: "Company",
    submitLogin: "Sign in",
    submitRegister: "Create my account",
    needAccount: "No account yet?",
    haveAccount: "Already have an account?",
    guestMsgs: "Sign in to write to your Talendus consultant.",
    emptyMsgs: "No messages yet. Write to your consultant below.",
    write: "Write a message",
    send: "Send",
    loading: "Loading…",
    err: "Something went wrong.",
    apps: "My applications",
    emptyApps: "No applications yet.",
    profile: "My file",
    phone: "Phone",
    city: "City",
    title: "Job title",
    skills: "Skills",
    save: "Save",
    saved: "Saved.",
    cv: "Resume",
    upload: "Upload a PDF or Word file",
    completeness: "File completeness",
    statsApps: "Applications",
    statsProgress: "In progress",
    statsInterviews: "Interviews",
    hiringLead: "Hand Talendus a need. We search and present files. You keep the decision.",
    newNeed: "New hiring need",
    needTitle: "Role",
    location: "Location",
    seats: "Openings",
    notes: "What you need",
    sendNeed: "Send to Talendus",
    needSent: "Talendus has the need. A consultant will follow up.",
    emptyHiring: "No hiring request yet.",
    emptyThread: "Choose a conversation.",
    consultant: "Talendus consultant",
    back: "Back",
    salary: "Pay",
    sector: "Sector",
    contract: "Contract",
    notify: "Notifications",
    emptyNotify: "No notifications.",
    mediate: "Companies never get your email or phone. Contact always goes through Talendus."
  } : {
    home: "Accueil",
    jobs: "Offres",
    hiring: "Recrutements",
    messages: "Messages",
    me: "Compte",
    hello: "Bonjour",
    guestTitle: "Talendus dans votre poche",
    guestLead: "Les offres, votre dossier et votre conseiller — sans le site autour.",
    talent: "Je cherche un emploi",
    employer: "Je veux recruter",
    recentJobs: "Postes ouverts",
    call: "Appeler Talendus",
    wa: "WhatsApp",
    search: "Rechercher un poste",
    go: "Chercher",
    emptyJobs: "Aucune offre à afficher pour le moment.",
    apply: "Demander à Talendus de me présenter",
    applied: "Demande envoyée à Talendus.",
    login: "Connexion",
    register: "Créer un compte",
    logout: "Déconnexion",
    email: "Courriel",
    password: "Mot de passe",
    first: "Prénom",
    last: "Nom",
    company: "Entreprise",
    submitLogin: "Me connecter",
    submitRegister: "Créer mon compte",
    needAccount: "Pas encore de compte ?",
    haveAccount: "Déjà un compte ?",
    guestMsgs: "Connectez-vous pour écrire à votre conseiller Talendus.",
    emptyMsgs: "Aucun message pour le moment. Écrivez à votre conseiller.",
    write: "Votre message",
    send: "Envoyer",
    loading: "Chargement…",
    err: "Une erreur s’est produite.",
    apps: "Mes candidatures",
    emptyApps: "Aucune candidature pour le moment.",
    profile: "Mon dossier",
    phone: "Téléphone",
    city: "Ville",
    title: "Titre professionnel",
    skills: "Compétences",
    save: "Enregistrer",
    saved: "Enregistré.",
    cv: "CV",
    upload: "Téléverser un PDF ou un fichier Word",
    completeness: "Dossier complété",
    statsApps: "Candidatures",
    statsProgress: "En cours",
    statsInterviews: "Entretiens",
    hiringLead: "Confiez un besoin à Talendus. Nous recherchons et présentons les dossiers. Vous gardez la décision.",
    newNeed: "Nouveau besoin",
    needTitle: "Poste",
    location: "Lieu",
    seats: "Postes",
    notes: "Votre besoin",
    sendNeed: "Envoyer à Talendus",
    needSent: "Talendus a bien reçu le besoin. Un conseiller fait le suivi.",
    emptyHiring: "Aucun recrutement pour le moment.",
    emptyThread: "Choisissez une conversation.",
    consultant: "Conseiller Talendus",
    back: "Retour",
    salary: "Salaire",
    sector: "Secteur",
    contract: "Contrat",
    notify: "Notifications",
    emptyNotify: "Aucune notification.",
    mediate: "Les entreprises n’ont jamais votre courriel ni votre téléphone. Le contact passe toujours par Talendus."
  };

  var state = {
    user: api.currentUser(),
    contact: { phone_e164: "15145550199", phone_display: "514 555-0199", email: "info@talendus.ca" },
    jobs: [],
    job: null,
    dash: null,
    apps: [],
    threads: [],
    directory: [],
    conversation: [],
    hiring: [],
    notes: [],
    notice: "",
    error: "",
    busy: false
  };

  var icons = {
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/></svg>',
    jobs: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5h8v2"/></svg>',
    msg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 6h14v10H8l-3 3V6z"/></svg>',
    me: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.5"/><path d="M5 19c1.5-3.2 4-5 7-5s5.5 1.8 7 5"/></svg>',
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 3h3l1 4-2 1a12 12 0 006 6l1-2 4 1v3c0 1-1 2-2 2C10 18 6 14 6 7c0-1 1-2 1-4z"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3a9 9 0 00-7.8 13.5L3 21l4.7-1.2A9 9 0 1012 3zm4.7 12.6c-.2.6-1.1 1-1.8.7-1.5-.5-3.3-1.7-4.6-3.4S8 9.6 8 8.4c0-.7.4-1.3.8-1.5l.9-.2.7 1.7-.6.6c.5 1 1.5 2.1 2.4 2.6l.7-.5 1.6.8-.2.9z"/></svg>'
  };

  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function dataOf(json) { return json && json.data ? json.data : json; }
  function route() {
    var raw = (location.hash || "#/home").replace(/^#/, "");
    var parts = raw.replace(/^\//, "").split("/").filter(Boolean);
    return { name: parts[0] || "home", id: parts.slice(1).join("/") };
  }
  function go(hash) {
    if (location.hash === hash) render();
    else location.hash = hash;
  }
  function telHref() { return "tel:+" + String(state.contact.phone_e164 || "").replace(/\D/g, ""); }
  function waHref() {
    var n = String(state.contact.phone_e164 || "").replace(/\D/g, "");
    var msg = encodeURIComponent(isEn ? "Hello Talendus" : "Bonjour Talendus");
    return "https://wa.me/" + n + "?text=" + msg;
  }
  function isEmployer(user) {
    user = user || state.user;
    return user && (user.role === "EMPLOYER" || user.role === "RECRUITER" || user.role === "ADMIN" || user.role === "SUPER_ADMIN");
  }
  function isCandidate(user) {
    user = user || state.user;
    return user && user.role === "CANDIDATE";
  }
  function setNotice(msg, err) {
    state.notice = err ? "" : (msg || "");
    state.error = err ? (msg || t.err) : "";
  }
  function topBar() {
    return '<header class="tn-top"><div class="tn-brand"><img src="/assets/img/logo/icon-192.png" width="32" height="32" alt=""><span>Talendus</span></div>' +
      '<div class="tn-top-actions">' +
      '<a class="tn-icon-btn" href="' + telHref() + '" aria-label="' + esc(t.call) + '">' + icons.phone + "</a>" +
      '<a class="tn-icon-btn" href="' + waHref() + '" aria-label="' + esc(t.wa) + '">' + icons.wa + "</a>" +
      "</div></header>";
  }
  function tabs() {
    var r = route().name;
    var second = isEmployer() ? { href: "#/hiring", key: "hiring", label: t.hiring, icon: icons.jobs } :
      { href: "#/jobs", key: "jobs", label: t.jobs, icon: icons.jobs };
    var items = [
      { href: "#/home", key: "home", label: t.home, icon: icons.home },
      second,
      { href: "#/messages", key: "messages", label: t.messages, icon: icons.msg },
      { href: "#/me", key: "me", label: t.me, icon: icons.me }
    ];
    return '<nav class="tn-tabs">' + items.map(function (item) {
      var on = r === item.key || (item.key === "jobs" && r === "job") || (item.key === "hiring" && r === "need");
      return '<a href="' + item.href + '" class="' + (on ? "is-on" : "") + '">' + item.icon + "<span>" + esc(item.label) + "</span></a>";
    }).join("") + "</nav>";
  }
  function flash() {
    if (state.error) return '<p class="tn-error">' + esc(state.error) + "</p>";
    if (state.notice) return '<p class="tn-ok">' + esc(state.notice) + "</p>";
    return "";
  }
  function jobCard(job) {
    var href = "#/job/" + encodeURIComponent(job.slug || job.id);
    return '<a class="tn-job" href="' + href + '"><h3>' + esc(job.title) + "</h3>" +
      '<p class="tn-meta">' + esc([job.location, job.sector || job.employment_type, job.salary || job.salary_display].filter(Boolean).join(" · ")) + "</p></a>";
  }

  function homeView() {
    var user = state.user;
    if (!user) {
      return "<h1 class=\"tn-title\">" + esc(t.guestTitle) + "</h1><p class=\"tn-lead\">" + esc(t.guestLead) + "</p>" +
        '<div class="tn-choice"><a class="tn-primary" href="#/register/talent">' + esc(t.talent) + "</a>" +
        '<a class="tn-ghost" href="#/register/employer">' + esc(t.employer) + "</a></div>" +
        "<h2 class=\"tn-title\" style=\"font-size:1.1rem\">" + esc(t.recentJobs) + "</h2>" +
        '<div class="tn-grid">' + (state.jobs.slice(0, 5).map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>";
    }
    var name = user.first_name || "";
    var dash = state.dash || {};
    var stats = dash.stats || {};
    if (isEmployer()) {
      return "<h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
        '<p class="tn-lead">' + esc(dash.company_name || t.hiringLead) + "</p>" +
        '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.active_jobs || 0) + "</b><span>" + esc(t.hiring) + "</span></div>" +
        '<div class="tn-stat"><b>' + esc(stats.applications || 0) + "</b><span>" + esc(t.apps) + "</span></div></div>" +
        '<a class="tn-btn" href="#/hiring">' + esc(t.newNeed) + "</a>";
    }
    var pct = (dash.completeness && dash.completeness.percent) || 0;
    return "<h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
      '<p class="tn-note">' + esc(t.mediate) + "</p>" +
      '<p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p><div class=\"tn-progress\"><span style=\"width:" + pct + '%"></span></div>' +
      '<div class="tn-stats"><div class="tn-stat"><b>' + esc(stats.applications || 0) + "</b><span>" + esc(t.statsApps) + "</span></div>" +
      '<div class="tn-stat"><b>' + esc(stats.interviews || 0) + "</b><span>" + esc(t.statsInterviews) + "</span></div></div>" +
      '<div class="tn-grid">' + ((dash.matches || []).map(function (row) { return jobCard(row.job || row); }).join("") || state.jobs.slice(0, 4).map(jobCard).join("")) + "</div>";
  }

  function jobsView() {
    return '<form class="tn-search" data-search-jobs><input name="q" placeholder="' + esc(t.search) + '" value="' + esc(state.query || "") + '"><button type="submit">' + esc(t.go) + "</button></form>" +
      '<div class="tn-grid">' + (state.jobs.map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>";
  }

  function jobView() {
    var job = state.job;
    if (!job) return '<div class="tn-empty">' + esc(t.loading) + "</div>";
    var body = (job.description || "").slice(0, 900);
    return '<a class="tn-back" href="#/jobs">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(job.title) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, job.sector, job.contract_type, job.salary_display].filter(Boolean).join(" · ")) + "</p>" +
      '<div class="tn-card"><p>' + esc(body) + "</p></div>" + flash() +
      (isCandidate() ? '<p><button class="tn-btn" data-apply="' + esc(job.id) + '">' + esc(t.apply) + "</button></p>" :
        '<p><a class="tn-btn" href="#/login">' + esc(t.login) + "</a></p>");
  }

  function messagesView() {
    if (!state.user) {
      return '<div class="tn-empty"><p>' + esc(t.guestMsgs) + '</p><p><a class="tn-btn" href="#/login">' + esc(t.login) + "</a></p></div>";
    }
    var r = route();
    if (r.id) {
      var who = state.threads.concat(state.directory).find(function (p) { return (p.user_id || p.id) === r.id; }) || {};
      var name = ((who.first_name || "") + " " + (who.last_name || "")).trim() || t.consultant;
      return '<a class="tn-back" href="#/messages">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(name) + "</h1>" +
        '<div class="tn-msg-list">' + (state.conversation.map(function (m) {
          var mine = state.user && m.sender_id === state.user.id;
          return '<div class="tn-bubble' + (mine ? " mine" : "") + '">' + esc(m.body) + "</div>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyThread) + "</div>") + "</div>" +
        '<form class="tn-composer" data-send-msg data-to="' + esc(r.id) + '"><input name="body" required placeholder="' + esc(t.write) + '"><button class="tn-btn" type="submit">' + esc(t.send) + "</button></form>";
    }
    var list = state.threads.length ? state.threads : state.directory.map(function (p) {
      return { user_id: p.id, first_name: p.first_name, last_name: p.last_name, last_message: t.consultant, unread: 0 };
    });
    return "<h1 class=\"tn-title\">" + esc(t.messages) + "</h1><div class=\"tn-grid\">" +
      (list.map(function (th) {
        var label = ((th.first_name || "") + " " + (th.last_name || "")).trim() || t.consultant;
        return '<a class="tn-thread" href="#/messages/' + encodeURIComponent(th.user_id) + '"><strong>' + esc(label) + "</strong><p class=\"tn-meta\">" + esc(th.last_message || "") + "</p></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyMsgs) + "</div>") + "</div>";
  }

  function hiringView() {
    if (!state.user) return '<div class="tn-empty"><a class="tn-btn" href="#/login">' + esc(t.login) + "</a></div>";
    return "<h1 class=\"tn-title\">" + esc(t.hiring) + "</h1><p class=\"tn-lead\">" + esc(t.hiringLead) + "</p>" + flash() +
      '<form class="tn-form" data-hiring><label>' + esc(t.needTitle) + '</label><input name="title" required>' +
      "<label>" + esc(t.location) + '</label><input name="location">' +
      "<label>" + esc(t.notes) + '</label><textarea name="notes"></textarea>' +
      '<p><button class="tn-btn" type="submit">' + esc(t.sendNeed) + "</button></p></form>" +
      '<div class="tn-grid" style="margin-top:16px">' + (state.hiring.map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' + esc(row.location || "") + '</p><span class="tn-status">' + esc(row.status_label || row.status || "") + "</span></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyHiring) + "</div>") + "</div>";
  }

  function authView(kind, persona) {
    var employer = persona === "employer" || kind === "employer";
    if (kind === "login" || route().name === "login") {
      return "<h1 class=\"tn-title\">" + esc(t.login) + "</h1>" + flash() +
        '<form class="tn-form" data-login><label>' + esc(t.email) + '</label><input name="email" type="email" required>' +
        "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
        '<p><button class="tn-btn" type="submit">' + esc(t.submitLogin) + "</button></p></form>" +
        '<p class="tn-note">' + esc(t.needAccount) + ' <a href="#/register/talent">' + esc(t.register) + "</a></p>";
    }
    return "<h1 class=\"tn-title\">" + esc(employer ? t.employer : t.talent) + "</h1>" + flash() +
      '<form class="tn-form" data-register data-role="' + (employer ? "EMPLOYER" : "CANDIDATE") + '">' +
      "<label>" + esc(t.first) + '</label><input name="first_name" required>' +
      "<label>" + esc(t.last) + '</label><input name="last_name" required>' +
      "<label>" + esc(t.email) + '</label><input name="email" type="email" required>' +
      "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
      (employer ? "<label>" + esc(t.company) + '</label><input name="company_name" required>' : "") +
      '<p><button class="tn-btn" type="submit">' + esc(t.submitRegister) + "</button></p></form>" +
      '<p class="tn-note">' + esc(t.haveAccount) + ' <a href="#/login">' + esc(t.login) + "</a></p>";
  }

  function meView() {
    if (!state.user) return authView("login");
    var html = "<h1 class=\"tn-title\">" + esc((state.user.first_name || "") + " " + (state.user.last_name || "")) + "</h1>" +
      '<p class="tn-meta">' + esc(state.user.email || "") + "</p>" + flash();
    if (isCandidate()) {
      var p = state.profile || {};
      html += '<form class="tn-form" data-profile><label>' + esc(t.city) + '</label><input name="city" value="' + esc(p.city || "") + '">' +
        "<label>" + esc(t.title) + '</label><input name="title" value="' + esc(p.title || "") + '">' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(p.skills || "") + '">' +
        '<p><button class="tn-btn" type="submit">' + esc(t.save) + "</button></p></form>" +
        '<form class="tn-form" data-cv><label>' + esc(t.cv) + '</label><input type="file" name="file" accept=".pdf,.doc,.docx,application/pdf">' +
        '<p><button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.upload) + "</button></p></form>" +
        "<h2 class=\"tn-title\" style=\"font-size:1.1rem\">" + esc(t.apps) + "</h2><div class=\"tn-grid\">" +
        (state.apps.map(function (a) {
          var job = a.job || {};
          return '<div class="tn-job"><h3>' + esc(job.title || t.apps) + '</h3><span class="tn-status">' + esc(a.status || "") + "</span></div>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") + "</div>";
    }
    html += '<p style="margin-top:18px"><button class="tn-btn tn-btn-ghost" data-logout>' + esc(t.logout) + "</button></p>";
    return html;
  }

  function screenHtml() {
    var r = route();
    if (r.name === "jobs") return jobsView();
    if (r.name === "job") return jobView();
    if (r.name === "messages") return messagesView();
    if (r.name === "hiring" || r.name === "need") return hiringView();
    if (r.name === "login") return authView("login");
    if (r.name === "register") return authView("register", r.id);
    if (r.name === "me") return meView();
    return homeView();
  }

  function render() {
    root.innerHTML = topBar() + '<main id="tn-screen" class="tn-screen">' + screenHtml() + "</main>" + tabs();
  }

  function loadJobs(q) {
    state.query = q || "";
    return api.jobs({ q: q || "", page_size: 20, sort: "published_at" }).then(function (json) {
      state.jobs = dataOf(json) || [];
    }).catch(function () { state.jobs = []; });
  }

  function loadSessionData() {
    var user = api.currentUser();
    state.user = user;
    if (!user) {
      state.dash = null;
      return Promise.resolve();
    }
    var tasks = [
      api.request("/notifications/unread").then(function (json) { state.notes = dataOf(json) || []; }).catch(function () {}),
      api.request("/messages").then(function (json) { state.threads = dataOf(json) || []; }).catch(function () { state.threads = []; }),
      api.request("/messages/directory").then(function (json) { state.directory = dataOf(json) || []; }).catch(function () { state.directory = []; })
    ];
    if (isCandidate(user)) {
      tasks.push(api.request("/candidates/me/dashboard").then(function (json) { state.dash = dataOf(json); }).catch(function () {}));
      tasks.push(api.profile().then(function (json) { state.profile = dataOf(json); }).catch(function () {}));
      tasks.push(api.myApplications().then(function (json) { state.apps = dataOf(json) || []; }).catch(function () { state.apps = []; }));
    }
    if (isEmployer(user)) {
      tasks.push(api.request("/companies/me/dashboard").then(function (json) { state.dash = dataOf(json); }).catch(function () {}));
      tasks.push(api.request("/hiring-requests").then(function (json) { state.hiring = dataOf(json) || []; }).catch(function () { state.hiring = []; }));
    }
    return Promise.all(tasks);
  }

  function loadRoute() {
    var r = route();
    var pending = [loadSessionData()];
    if (r.name === "home" || r.name === "jobs") pending.push(loadJobs(state.query));
    if (r.name === "job" && r.id) {
      pending.push(api.request("/jobs/" + encodeURIComponent(r.id)).then(function (json) { state.job = dataOf(json); }).catch(function () { state.job = null; }));
    }
    if (r.name === "messages" && r.id) {
      pending.push(api.request("/messages/" + encodeURIComponent(r.id)).then(function (json) { state.conversation = dataOf(json) || []; }).catch(function () { state.conversation = []; }));
    }
    return Promise.all(pending).then(render);
  }

  root.addEventListener("submit", function (e) {
    var form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.matches("[data-search-jobs]")) {
      e.preventDefault();
      loadJobs(new FormData(form).get("q")).then(function () { go("#/jobs"); render(); });
    } else if (form.matches("[data-login]")) {
      e.preventDefault();
      var fd = new FormData(form);
      api.login(fd.get("email"), fd.get("password")).then(function () {
        state.user = api.currentUser();
        setNotice("");
        go("#/home");
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-register]")) {
      e.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      data.role = form.getAttribute("data-role") || "CANDIDATE";
      api.register(data).then(function () {
        state.user = api.currentUser();
        setNotice("");
        go("#/home");
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-send-msg]")) {
      e.preventDefault();
      var body = new FormData(form).get("body");
      api.request("/messages", { method: "POST", body: { recipient_id: form.getAttribute("data-to"), body: body } }).then(function () {
        form.reset();
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-hiring]")) {
      e.preventDefault();
      var need = Object.fromEntries(new FormData(form).entries());
      api.request("/hiring-requests", { method: "POST", body: need }).then(function () {
        setNotice(t.needSent);
        form.reset();
        loadRoute();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-profile]")) {
      e.preventDefault();
      var profile = Object.fromEntries(new FormData(form).entries());
      api.updateProfile(profile).then(function () { setNotice(t.saved); loadRoute(); })
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    } else if (form.matches("[data-cv]")) {
      e.preventDefault();
      var file = form.file && form.file.files && form.file.files[0];
      if (!file) return;
      var payload = new FormData();
      payload.append("file", file);
      api.uploadResume(payload).then(function () { setNotice(t.saved); loadRoute(); })
        .catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    }
  });

  root.addEventListener("click", function (e) {
    var applyBtn = e.target.closest("[data-apply]");
    if (applyBtn) {
      e.preventDefault();
      api.apply({ job_id: applyBtn.getAttribute("data-apply") }).then(function () {
        setNotice(t.applied);
        render();
      }).catch(function (err) { setNotice((err && err.message) || t.err, true); render(); });
    }
    if (e.target.closest("[data-logout]")) {
      e.preventDefault();
      api.logout().then(function () {
        state.user = null;
        go("#/home");
        loadRoute();
      });
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
