(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var root = document.getElementById("tl-account");
    if (!root || !window.TalendusAPI) return;
    var api = window.TalendusAPI;
    var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    document.body.classList.add("tl-portal-active");

    var t = isEn ? {
      login: "Sign in", register: "Create an account", email: "Email", password: "Password",
      first: "First name", last: "Last name", submitLogin: "Sign in", submitRegister: "Create my account",
      logout: "Sign out", dashboard: "Dashboard", profile: "Profile", apps: "Applications",
      notifs: "Notifications", documents: "Documents", jobs: "Jobs", messages: "Messages",
      interviews: "Interviews", settings: "Settings", save: "Save", city: "City", title: "Job title",
      sector: "Sector", skills: "Skills", phone: "Phone", upload: "Upload a PDF, DOC or DOCX",
      emptyApps: "No applications yet.", emptyNotifs: "No notifications.", emptyJobs: "No matching roles yet.",
      emptyMsgs: "No messages yet.", emptyInts: "No interviews scheduled.", emptyDocs: "No documents yet.",
      emptySaved: "No saved jobs.", markAll: "Mark all as read", markRead: "Mark as read",
      welcome: "Your industrial workspace", guest: "Sign in to follow your applications.",
      err: "Something went wrong.", saved: "Saved.", uploaded: "File saved.", send: "Send",
      confirm: "Confirm", cancel: "Cancel", to: "To", write: "Your message", score: "Match",
      welcomeEmployer: "Your hiring workspace", guestEmployer: "Sign in to manage jobs and applications.",
      registerEmployer: "Create an employer account", company: "Company", inbox: "Applications",
      candidates: "Candidates", invoices: "Invoices", publish: "Publish", pause: "Pause",
      archive: "Archive", draft: "Draft", createJob: "Create a job", edit: "Edit", apply: "Apply",
      bookmark: "Save job", unbookmark: "Saved", search: "Search", filters: "Filters",
      completeness: "Profile completeness", quickSearch: "Search jobs", quickProfile: "Complete my profile",
      quickCv: "Download resume", quickApps: "View applications", inProgress: "In progress",
      upcoming: "Upcoming interviews", accepted: "Accepted", hello: "Hello", activeJobs: "Active jobs",
      shortlisted: "Shortlisted", hired: "Hires", recent: "Recent activity", loading: "Loading…",
      withdraw: "Withdraw", location: "Location", contract: "Contract type", salary: "Salary",
      experience: "Experience", sort: "Sort", bio: "Professional summary", availability: "Availability",
      mobility: "Geographic mobility", languages: "Languages", desiredSalary: "Desired salary",
      updated: "Last updated", photo: "Photo", add: "Add", remove: "Remove", replace: "Replace",
      download: "Download", personal: "Personal information", security: "Security",
      privacy: "Privacy", danger: "Delete account", newPass: "New password", currentPass: "Current password",
      confirmDanger: "This will deactivate your account. Continue?", members: "Users",
      permissions: "Role", invite: "Invite", legal: "Legal information", website: "Website",
      address: "Address", country: "Country", description: "Description", openings: "Openings",
      startDate: "Start date", deadline: "Deadline", responsibilities: "Responsibilities",
      extra: "Additional information", validate: "Jobs are reviewed before they go live.",
      schedule: "Schedule interview", when: "Date and time", type: "Type", place: "Location or link",
      comments: "Comments", cover: "Cover letter", certs: "Certifications", otherDocs: "Other documents",
      noResults: "No results for these filters.", retry: "Try again", success: "Done.",
      page: "Page", of: "of", prev: "Previous", next: "Next", jobDetail: "Job details",
      appDetail: "Application", sent: "Submitted", review: "Under review", preselect: "Shortlist",
      interview: "Interview", decision: "Decision", companyDocs: "Company documents",
      notifyPrefs: "Notification preferences", emailNotif: "Email", inApp: "In-app",
      sms: "SMS (coming soon)", wa: "WhatsApp (coming soon)", push: "Push (coming soon)",
      profilePublic: "Allow a public professional summary", changeEmail: "Email address is used to sign in.",
      emptyInbox: "No applications received.", emptyInvoices: "No invoices.",
      pay: "Pay by card", pipeline: "Pipeline"
    } : {
      login: "Connexion", register: "Créer un compte", email: "Courriel", password: "Mot de passe",
      first: "Prénom", last: "Nom", submitLogin: "Me connecter", submitRegister: "Créer mon compte",
      logout: "Déconnexion", dashboard: "Tableau de bord", profile: "Profil", apps: "Candidatures",
      notifs: "Notifications", documents: "Documents", jobs: "Offres", messages: "Messages",
      interviews: "Entretiens", settings: "Paramètres", save: "Enregistrer", city: "Ville", title: "Titre professionnel",
      sector: "Secteur", skills: "Compétences", phone: "Téléphone", upload: "Téléverser un PDF, DOC ou DOCX",
      emptyApps: "Aucune candidature pour le moment.", emptyNotifs: "Aucune notification.",
      emptyJobs: "Aucune offre ne correspond encore à votre recherche.", emptyMsgs: "Aucun message pour le moment.",
      emptyInts: "Aucun entretien planifié.", emptyDocs: "Aucun document pour le moment.",
      emptySaved: "Aucune offre sauvegardée.", markAll: "Tout marquer comme lu", markRead: "Marquer comme lu",
      welcome: "Votre espace candidat", guest: "Connectez-vous pour suivre vos candidatures.",
      err: "Une erreur s’est produite.", saved: "Enregistré.", uploaded: "Fichier enregistré.", send: "Envoyer",
      confirm: "Confirmer", cancel: "Annuler", to: "Destinataire", write: "Votre message", score: "Score",
      welcomeEmployer: "Votre espace employeur", guestEmployer: "Connectez-vous pour gérer vos offres et candidatures.",
      registerEmployer: "Créer un compte employeur", company: "Entreprise", inbox: "Candidatures",
      candidates: "Candidats", invoices: "Factures", publish: "Publier", pause: "Mettre en pause",
      archive: "Archiver", draft: "Brouillon", createJob: "Créer une offre", edit: "Modifier", apply: "Postuler",
      bookmark: "Sauvegarder", unbookmark: "Sauvegardée", search: "Rechercher", filters: "Filtres",
      completeness: "Complétude du profil", quickSearch: "Rechercher une offre", quickProfile: "Compléter mon profil",
      quickCv: "Télécharger mon CV", quickApps: "Voir mes candidatures", inProgress: "En cours",
      upcoming: "Entretiens à venir", accepted: "Acceptées", hello: "Bonjour", activeJobs: "Offres actives",
      shortlisted: "Présélectionnés", hired: "Recrutements", recent: "Activité récente", loading: "Chargement…",
      withdraw: "Retirer", location: "Localisation", contract: "Type de contrat", salary: "Salaire",
      experience: "Expérience", sort: "Trier", bio: "Résumé professionnel", availability: "Disponibilité",
      mobility: "Mobilité géographique", languages: "Langues", desiredSalary: "Salaire souhaité",
      updated: "Dernière mise à jour", photo: "Photo", add: "Ajouter", remove: "Supprimer", replace: "Remplacer",
      download: "Télécharger", personal: "Informations personnelles", security: "Sécurité",
      privacy: "Confidentialité", danger: "Supprimer le compte", newPass: "Nouveau mot de passe",
      currentPass: "Mot de passe actuel", confirmDanger: "Cette action désactivera votre compte. Continuer ?",
      members: "Utilisateurs", permissions: "Rôle", invite: "Inviter", legal: "Informations légales",
      website: "Site web", address: "Adresse", country: "Pays", description: "Description", openings: "Nombre de postes",
      startDate: "Date de début", deadline: "Date limite", responsibilities: "Responsabilités",
      extra: "Informations complémentaires", validate: "L’offre est enregistrée en brouillon. Publiez-la lorsque tout est prêt.",
      schedule: "Planifier un entretien", when: "Date et heure", type: "Type", place: "Lieu ou lien",
      comments: "Commentaires", cover: "Lettre de motivation", certs: "Certifications", otherDocs: "Documents complémentaires",
      noResults: "Aucun résultat pour ces filtres.", retry: "Réessayer", success: "Terminé.",
      page: "Page", of: "sur", prev: "Précédent", next: "Suivant", jobDetail: "Détail de l’offre",
      appDetail: "Candidature", sent: "Candidature envoyée", review: "Dossier examiné", preselect: "Présélection",
      interview: "Entretien", decision: "Décision", companyDocs: "Documents de l’entreprise",
      notifyPrefs: "Préférences de notification", emailNotif: "Courriel", inApp: "Dans l’application",
      sms: "SMS (prochainement)", wa: "WhatsApp (prochainement)", push: "Push (prochainement)",
      profilePublic: "Autoriser un résumé professionnel visible", changeEmail: "Le courriel sert à vous connecter.",
      emptyInbox: "Aucune candidature reçue.", emptyInvoices: "Aucune facture.",
      pay: "Payer par carte", pipeline: "Pipeline"
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    function statusLabel(s) {
      var map = {
        SUBMITTED: isEn ? "Submitted" : "Candidature envoyée",
        RECEIVED: isEn ? "Received" : "Reçue",
        UNDER_REVIEW: isEn ? "Under review" : "En cours d’analyse",
        SHORTLISTED: isEn ? "Shortlisted" : "Présélection",
        INTERVIEW: isEn ? "Interview" : "Entretien",
        SECOND_INTERVIEW: isEn ? "Second interview" : "Deuxième entretien",
        OFFER_SENT: isEn ? "Offer" : "Offre d’emploi",
        REJECTED: isEn ? "Declined" : "Refusée",
        HIRED: isEn ? "Hired" : "Acceptée",
        WITHDRAWN: isEn ? "Withdrawn" : "Retirée",
        DRAFT: isEn ? "Draft" : "Brouillon",
        PUBLISHED: isEn ? "Published" : "Publiée",
        PAUSED: isEn ? "Paused" : "En pause",
        ARCHIVED: isEn ? "Archived" : "Archivée",
        CLOSED: isEn ? "Closed" : "Fermée",
        SCHEDULED: isEn ? "Scheduled" : "Planifié",
        CONFIRMED: isEn ? "Confirmed" : "Confirmé",
        COMPLETED: isEn ? "Completed" : "Terminé",
        CANCELLED: isEn ? "Cancelled" : "Annulé",
        NO_SHOW: isEn ? "No-show" : "Absent",
        OWNER: isEn ? "Administrator" : "Administrateur",
        ADMIN: isEn ? "Administrator" : "Administrateur",
        HR: isEn ? "HR" : "RH",
        RECRUITER: isEn ? "Recruiter" : "Recruteur",
        MEMBER: isEn ? "Member" : "Membre",
        BILLING: isEn ? "Billing" : "Facturation",
        SENT: isEn ? "Sent" : "Envoyée",
        PENDING: isEn ? "Pending" : "En attente",
        PAID: isEn ? "Paid" : "Payée",
        OVERDUE: isEn ? "Overdue" : "En retard",
        REFUNDED: isEn ? "Refunded" : "Remboursée"
      };
      return map[s] || s;
    }
    function fmtDate(v) {
      if (!v) return "—";
      return String(v).replace("T", " ").slice(0, 16);
    }
    function authDownload(path, filename) {
      var token = "";
      try { token = localStorage.getItem("talendus_access_token") || ""; } catch (e) {}
      fetch(path, { headers: { Authorization: token ? ("Bearer " + token) : "", Accept: "*/*" } }).then(function (res) {
        if (!res.ok) throw new Error(t.err);
        return res.blob().then(function (blob) {
          var url = URL.createObjectURL(blob);
          var a = document.createElement("a");
          a.href = url;
          a.download = filename || "document";
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
        });
      }).catch(function () { window.alert(t.err); });
    }
    function isEmployerSpace() {
      return root.getAttribute("data-space") === "employer" || /\/employer(\/|$)/.test(location.pathname);
    }
    function staffRole(role) {
      return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
    }
    function siteRoot() {
      return isEn ? "/en/" : "/";
    }
    function accountHref(role) {
      if (staffRole(role)) return "/admin/";
      if (role === "EMPLOYER") return siteRoot() + (isEn ? "account-employer.html" : "espace-employeur.html") + "#/dashboard";
      return siteRoot() + (isEn ? "account.html" : "espace.html") + "#/dashboard";
    }
    function localizeHref(href) {
      if (!href) return "";
      if (!isEn) return href;
      return String(href)
        .replace("/espace-employeur.html", "/en/account-employer.html")
        .replace("/espace.html", "/en/account.html");
    }
    function pathMode() {
      return /\/(candidate|employer)(\/|$)/.test(location.pathname);
    }
    function normalizeRoute(name, id) {
      if (isEmployerSpace() && (name === "applications" || name === "apps" || name === "candidatures")) {
        return { name: "inbox", id: id || "" };
      }
      if (name === "applications" || name === "candidatures" || name === "apps") {
        return id ? { name: "application", id: id } : { name: "apps", id: "" };
      }
      if (name === "job" && !id) return { name: "jobs", id: "" };
      return { name: name || "dashboard", id: id || "" };
    }
    function currentRoute() {
      var parts = location.pathname.replace(/\/+$/, "").split("/").filter(Boolean);
      var key = isEmployerSpace() ? "employer" : "candidate";
      var idx = parts.lastIndexOf(key);
      var rest = idx >= 0 ? parts.slice(idx + 1) : [];
      if (!rest.length) {
        var hash = (location.hash || "").replace(/^#\/?/, "");
        rest = hash ? hash.split("/") : ["dashboard"];
      }
      return normalizeRoute(rest[0] || "dashboard", rest[1] || "");
    }
    function go(name, id) {
      var suffix = name + (id ? "/" + id : "");
      if (pathMode()) {
        var base = location.pathname.split("/").filter(Boolean);
        var key = isEmployerSpace() ? "employer" : "candidate";
        var idx = base.lastIndexOf(key);
        var prefix = idx >= 0 ? "/" + base.slice(0, idx + 1).join("/") : (isEn ? "/en/" : "/") + key;
        history.pushState({}, "", prefix + "/" + suffix);
      } else {
        location.hash = "#/" + suffix;
      }
      renderAuthed();
    }
    function flash(el, msg, ok) {
      if (!el) return;
      el.style.display = "block";
      el.textContent = msg;
      el.className = ok === false ? "tl-success tl-error" : "tl-success";
    }
    function empty(msg) { return '<div class="tl-empty"><p>' + esc(msg) + "</p></div>"; }
    function errBox(msg) { return '<div class="tl-error"><p>' + esc(msg || t.err) + '</p><p><button type="button" class="tl-btn tl-btn-ghost" data-retry>' + esc(t.retry) + "</button></p></div>"; }
    function skeleton() { return '<div class="tl-skeleton"></div><div class="tl-skeleton"></div><div class="tl-skeleton"></div>'; }
    function unwrap(p) { return p.then(function (j) { return j.data; }); }
    function navItems(unreadN, unreadM) {
      if (isEmployerSpace()) {
        return [
          ["dashboard", t.dashboard], ["company", t.company], ["jobs", t.jobs], ["inbox", t.inbox],
          ["pipeline", t.pipeline], ["candidates", t.candidates], ["interviews", t.interviews],
          ["messages", t.messages, unreadM], ["invoices", t.invoices], ["documents", t.documents],
          ["notifs", t.notifs, unreadN], ["settings", t.settings]
        ];
      }
      return [
        ["dashboard", t.dashboard], ["profile", t.profile], ["jobs", t.jobs], ["apps", t.apps],
        ["interviews", t.interviews], ["messages", t.messages, unreadM], ["documents", t.documents],
        ["notifs", t.notifs, unreadN], ["settings", t.settings]
      ];
    }
    function shell(user, content, unreadN, unreadM) {
      var route = currentRoute();
      var items = navItems(unreadN, unreadM).map(function (it) {
        return '<button type="button" data-go="' + it[0] + '" class="' + (route.name === it[0] ? "is-active" : "") + '">' +
          esc(it[1]) + (it[2] ? '<span class="tl-portal-badge">' + it[2] + "</span>" : "") + "</button>";
      }).join("");
      var mobile = '<div class="tl-mobile-nav"><select id="acc-mobile-nav">' + navItems(unreadN, unreadM).map(function (it) {
        return '<option value="' + it[0] + '"' + (route.name === it[0] ? " selected" : "") + ">" + esc(it[1]) + "</option>";
      }).join("") + "</select></div>";
      var name = ((user.first_name || "") + " " + (user.last_name || "")).trim() || user.email;
      root.innerHTML = '<div class="tl-account-head"><div><div class="tl-kicker">' + esc(user.email) + "</div>" +
        '<h2 class="tl-h2">' + esc(name) + '</h2></div><button class="tl-btn tl-btn-ghost" type="button" id="acc-logout">' + esc(t.logout) + "</button></div>" +
        mobile + '<div class="tl-portal"><nav class="tl-portal-nav" aria-label="Talendus">' + items + "</nav>" +
        '<div class="tl-portal-main">' + content + "</div></div>";
      document.getElementById("acc-logout").onclick = function () { api.logout().then(renderGuest); };
      root.querySelectorAll("[data-go]").forEach(function (btn) {
        btn.onclick = function () { go(btn.getAttribute("data-go")); };
      });
      var sel = document.getElementById("acc-mobile-nav");
      if (sel) sel.onchange = function () { go(sel.value); };
      root.querySelectorAll("[data-nav]").forEach(function (btn) {
        btn.onclick = function () { go(btn.getAttribute("data-nav"), btn.getAttribute("data-id") || ""); };
      });
    }

    function renderGuest() {
      var employer = isEmployerSpace();
      root.innerHTML = '<div class="tl-account-grid"><div><div class="tl-kicker">Talendus</div><h2 class="tl-h2">' +
        esc(employer ? t.welcomeEmployer : t.welcome) + '</h2><p class="tl-lead">' + esc(employer ? t.guestEmployer : t.guest) +
        "</p></div><div class=\"tl-account-cards\">" +
        '<form class="tl-form" id="acc-login"><h3>' + esc(t.login) + "</h3><label>" + esc(t.email) +
        '</label><input name="email" type="email" required><label>' + esc(t.password) +
        '</label><input name="password" type="password" required minlength="8"><button class="tl-btn" type="submit">' +
        esc(t.submitLogin) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-register"><h3>' + esc(employer ? t.registerEmployer : t.register) + "</h3><label>" +
        esc(t.first) + '</label><input name="first_name" required><label>' + esc(t.last) +
        '</label><input name="last_name" required><label>' + esc(t.email) +
        '</label><input name="email" type="email" required><label>' + esc(t.password) +
        '</label><input name="password" type="password" required minlength="8"><button class="tl-btn tl-btn-electric" type="submit">' +
        esc(t.submitRegister) + '</button><div class="tl-success"></div></form></div></div>';
      document.getElementById("acc-login").addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(e.target).entries());
        api.login(d.email, d.password).then(boot).catch(function (err) { flash(e.target.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      document.getElementById("acc-register").addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(e.target).entries());
        api.register({ email: d.email, password: d.password, first_name: d.first_name, last_name: d.last_name, role: employer ? "EMPLOYER" : "CANDIDATE" })
          .then(boot).catch(function (err) { flash(e.target.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
    }

    function jobCard(job, extra) {
      job = job || {};
      var href = (isEn ? "/en/job-" : "/emploi-") + (job.slug || "") + ".html";
      return '<article class="tl-list-card"><span class="tl-chip orange">' + esc(statusLabel(job.status || "PUBLISHED")) + "</span>" +
        (job.saved ? '<span class="tl-match-score">' + esc(t.unbookmark) + "</span>" : "") +
        "<h3>" + esc(job.title || "") + "</h3><p class=\"tl-meta\">" + esc(job.company_name || "") + " · " + esc(job.location || "") +
        (job.contract_type ? " · " + esc(job.contract_type) : "") + "</p>" + (extra || "") +
        '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="job" data-id="' + esc(job.slug || job.id) + '">' +
        esc(t.jobDetail) + "</button> " + (job.slug ? '<a class="tl-split-cta" href="' + href + '">' + (isEn ? "Public page →" : "Page publique →") + "</a>" : "") + "</p></article>";
    }

    function renderCandidateDashboard(user, dash, profile) {
      var c = (dash && dash.completeness) || (profile && profile.completeness) || { percent: 0 };
      var s = (dash && dash.stats) || {};
      var stats = [["applications", t.apps, s.applications], ["in_progress", t.inProgress, s.in_progress],
        ["interviews", t.upcoming, s.interviews], ["accepted", t.accepted, s.accepted]];
      var primary = ((profile && profile.resumes) || []).filter(function (r) { return r.is_primary; })[0];
      var html = "<p class=\"tl-lead\">" + esc(t.hello) + " " + esc(user.first_name || "") + "</p>" +
        "<p>" + esc(t.completeness) + " — <b>" + esc(c.percent || 0) + " %</b></p><div class=\"tl-progress\"><i style=\"width:" + (c.percent || 0) + "%\"></i></div>" +
        '<div class="tl-stat-grid">' + stats.map(function (row) {
          return '<div class="tl-stat-card"><b>' + esc(row[2] || 0) + "</b><span>" + esc(row[1]) + "</span></div>";
        }).join("") + "</div><div class=\"tl-quick-actions\">" +
        '<button type="button" class="tl-btn" data-nav="jobs">' + esc(t.quickSearch) + "</button>" +
        '<button type="button" class="tl-btn tl-btn-ghost" data-nav="profile">' + esc(t.quickProfile) + "</button>" +
        (primary ? '<button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(primary.download_path) + '" data-dl-name="' + esc(primary.original_name || "cv.pdf") + '">' + esc(t.quickCv) + "</button>" : "") +
        '<button type="button" class="tl-btn tl-btn-ghost" data-nav="apps">' + esc(t.quickApps) + "</button></div>";
      var notifs = (dash && dash.notifications) || [];
      html += "<h3>" + esc(t.notifs) + "</h3>" + (notifs.length ? notifs.map(function (n) {
        return '<div class="tl-account-notif' + (n.is_read ? "" : " is-unread") + '"><b>' + esc(n.title) + "</b><p>" + esc(n.message) + "</p></div>";
      }).join("") : empty(t.emptyNotifs));
      var matches = (dash && dash.matches) || [];
      html += "<h3>" + esc(t.jobs) + "</h3>" + (matches.length ? '<div class="tl-list-cards">' + matches.map(function (m) {
        return jobCard(m.job || m, '<span class="tl-match-score">' + esc((m.score || 0) + " %") + "</span>");
      }).join("") : empty(t.emptyJobs));
      return html;
    }

    function profileForm(user, profile) {
      profile = profile || {};
      var exp = (profile.experiences || []).map(function (e) {
        return "<li>" + esc(e.role) + " — " + esc(e.company) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-exp="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>—</li>";
      var edu = (profile.education || []).map(function (e) {
        return "<li>" + esc(e.diploma || "") + " — " + esc(e.school) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-edu="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>—</li>";
      var certs = (profile.certifications || []).map(function (e) {
        return "<li>" + esc(e.name) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-cert="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>—</li>";
      return '<p class="tl-meta">' + esc(t.updated) + " : " + esc(fmtDate(profile.updated_at)) + "</p>" +
        '<form class="tl-form" id="acc-avatar"><label>' + esc(t.photo) + '</label><input name="file" type="file" accept="image/jpeg,image/png,image/webp">' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-profile"><div class="tl-row-2"><div><label>' + esc(t.first) + '</label><input name="first_name" value="' + esc(user.first_name || "") + '"></div>' +
        "<div><label>" + esc(t.last) + '</label><input name="last_name" value="' + esc(user.last_name || "") + '"></div></div>' +
        "<label>" + esc(t.email) + '</label><input value="' + esc(user.email || "") + '" disabled class="tl-disabled">' +
        "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(user.phone || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.city) + '</label><input name="city" value="' + esc(profile.city || "") + '"></div>' +
        "<div><label>" + esc(t.title) + '</label><input name="title" value="' + esc(profile.title || "") + '"></div></div>' +
        "<label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(profile.sector || "") + '">' +
        "<label>" + esc(t.bio) + '</label><textarea name="bio" rows="4">' + esc(profile.bio || "") + "</textarea>" +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(profile.skills || "") + '">' +
        "<label>" + esc(t.languages) + '</label><input name="languages" value="' + esc(profile.languages || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.availability) + '</label><input name="availability" value="' + esc(profile.availability || "") + '"></div>' +
        "<div><label>" + esc(t.contract) + '</label><input name="contract_type" value="' + esc(profile.contract_type || "") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.desiredSalary) + '</label><input name="desired_salary_min" type="number" value="' + esc(profile.desired_salary_min || "") + '"></div>' +
        "<div><label>" + esc(t.mobility) + '</label><input name="mobility" value="' + esc(profile.mobility || "") + '"></div></div>' +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>' +
        "<h3>" + (isEn ? "Experience" : "Expériences") + "</h3><ul>" + exp + "</ul>" +
        '<form class="tl-form" id="acc-exp"><div class="tl-row-2"><input name="company" placeholder="' + esc(t.company) + '" required><input name="role" placeholder="' + esc(t.title) + '" required></div>' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>" +
        "<h3>" + (isEn ? "Education" : "Formations") + "</h3><ul>" + edu + "</ul>" +
        '<form class="tl-form" id="acc-edu"><div class="tl-row-2"><input name="school" required><input name="diploma"></div>' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>" +
        "<h3>" + esc(t.certs) + "</h3><ul>" + certs + "</ul>" +
        '<form class="tl-form" id="acc-cert"><input name="name" required><button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>";
    }

    function bindProfile(user) {
      var form = document.getElementById("acc-profile");
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(form).entries());
        Promise.all([
          api.request("/users/me", { method: "PATCH", body: { first_name: d.first_name, last_name: d.last_name, phone: d.phone } }),
          api.request("/candidates/me", { method: "PATCH", body: {
            city: d.city, title: d.title, sector: d.sector, skills: d.skills, bio: d.bio, languages: d.languages,
            availability: d.availability, contract_type: d.contract_type,
            desired_salary_min: d.desired_salary_min ? Number(d.desired_salary_min) : null, mobility: d.mobility
          } })
        ]).then(function () { flash(form.querySelector(".tl-success"), t.saved, true); }).catch(function (err) {
          flash(form.querySelector(".tl-success"), (err && err.message) || t.err, false);
        });
      });
      var av = document.getElementById("acc-avatar");
      if (av) av.addEventListener("submit", function (e) {
        e.preventDefault();
        var file = av.querySelector("[name=file]").files[0];
        if (!file) return;
        var fd = new FormData(); fd.append("file", file);
        api.request("/users/me/avatar", { method: "POST", body: fd }).then(function () { flash(av.querySelector(".tl-success"), t.uploaded, true); }).catch(function (err) {
          flash(av.querySelector(".tl-success"), (err && err.message) || t.err, false);
        });
      });
      function postList(id, path) {
        var f = document.getElementById(id);
        if (!f) return;
        f.addEventListener("submit", function (e) {
          e.preventDefault();
          api.request(path, { method: "POST", body: Object.fromEntries(new FormData(f).entries()) }).then(function () { go("profile"); }).catch(function () {});
        });
      }
      postList("acc-exp", "/candidates/me/experiences");
      postList("acc-edu", "/candidates/me/education");
      postList("acc-cert", "/candidates/me/certifications");
      root.querySelectorAll("[data-del-exp]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/experiences/" + b.getAttribute("data-del-exp"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
      root.querySelectorAll("[data-del-edu]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/education/" + b.getAttribute("data-del-edu"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
      root.querySelectorAll("[data-del-cert]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/certifications/" + b.getAttribute("data-del-cert"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
    }

    function renderJobsSearch(payload) {
      var items = (payload && payload.data) || payload || [];
      var meta = (payload && payload.meta) || {};
      var f = state.jobFilters || {};
      function fv(name) { return esc(f[name] || ""); }
      var sort = f.sort || "relevance";
      var html = '<form class="tl-filters" id="acc-job-filters">' +
        '<div><label>' + esc(t.search) + '</label><input name="q" value="' + fv("q") + '"></div>' +
        "<div><label>" + esc(t.location) + '</label><input name="location" value="' + fv("location") + '"></div>' +
        "<div><label>" + esc(t.sector) + '</label><input name="sector" value="' + fv("sector") + '"></div>' +
        "<div><label>" + esc(t.contract) + '</label><input name="contract_type" value="' + fv("contract_type") + '"></div>' +
        "<div><label>" + esc(t.salary) + '</label><input name="salary_min" type="number" value="' + fv("salary_min") + '"></div>' +
        "<div><label>" + esc(t.experience) + '</label><input name="experience" value="' + fv("experience") + '"></div>' +
        "<div><label>" + esc(t.sort) + '</label><select name="sort">' +
        [["relevance", isEn ? "Relevance" : "Pertinence"], ["published_at", isEn ? "Date" : "Date"], ["salary", isEn ? "Salary" : "Salaire"]].map(function (opt) {
          return '<option value="' + opt[0] + '"' + (sort === opt[0] ? " selected" : "") + ">" + esc(opt[1]) + "</option>";
        }).join("") + "</select></div>" +
        '<div><button class="tl-btn" type="submit">' + esc(t.search) + "</button></div></form>";
      if (!items.length) html += empty(t.noResults);
      else html += '<div class="tl-list-cards">' + items.map(function (j) { return jobCard(j); }).join("") + "</div>";
      if (meta.pages > 1) {
        html += '<div class="tl-pager"><button type="button" class="tl-btn tl-btn-ghost" data-page="' + Math.max(1, (meta.page || 1) - 1) + '">' + esc(t.prev) +
          "</button><span>" + esc(t.page) + " " + (meta.page || 1) + " " + esc(t.of) + " " + meta.pages + '</span><button type="button" class="tl-btn tl-btn-ghost" data-page="' +
          Math.min(meta.pages, (meta.page || 1) + 1) + '">' + esc(t.next) + "</button></div>";
      }
      html += "<h3>" + esc(t.unbookmark) + "</h3><div id=\"acc-saved-jobs\">" + skeleton() + "</div>";
      return html;
    }

    function bindJobsSearch() {
      var form = document.getElementById("acc-job-filters");
      if (!form && !document.getElementById("acc-saved-jobs")) return;
      function load(page) {
        var d = form ? Object.fromEntries(new FormData(form).entries()) : (state.jobFilters || {});
        var params = new URLSearchParams();
        ["q", "location", "sector", "contract_type", "experience", "salary_min", "sort"].forEach(function (k) {
          var v = d[k];
          if (v) params.set(k, v);
        });
        params.set("page", page || d.page || 1);
        state.jobFilters = Object.assign({}, d, { page: page || d.page || 1 });
        api.request("/jobs?" + params.toString()).then(function (json) {
          state.jobs = json;
          go("jobs");
        }).catch(function () {});
      }
      if (form) form.addEventListener("submit", function (e) { e.preventDefault(); load(1); });
      root.querySelectorAll("[data-page]").forEach(function (b) { b.onclick = function () { load(b.getAttribute("data-page")); }; });
      if (!document.getElementById("acc-saved-jobs")) return;
      api.request("/jobs/saved").then(function (json) {
        var box = document.getElementById("acc-saved-jobs");
        if (!box) return;
        var items = json.data || [];
        box.innerHTML = items.length ? '<div class="tl-list-cards">' + items.map(function (j) { return jobCard(j); }).join("") : empty(t.emptySaved);
        root.querySelectorAll("[data-nav]").forEach(function (btn) {
          btn.onclick = function () { go(btn.getAttribute("data-nav"), btn.getAttribute("data-id") || ""); };
        });
      }).catch(function () {});
    }

    function renderJobDetail(job) {
      if (!job) return empty(t.err);
      return '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="jobs">' + (isEn ? "Back" : "Retour") + "</button></p>" +
        '<span class="tl-chip orange">' + esc(job.contract_type || "") + "</span><h3>" + esc(job.title) + "</h3>" +
        '<p class="tl-meta">' + esc(job.company_name || "") + " · " + esc(job.location || "") + " · " + esc(job.salary_display || "") + "</p>" +
        "<p>" + esc(job.description || "") + "</p>" +
        (job.responsibilities ? "<h4>" + esc(t.responsibilities) + "</h4><p>" + esc(job.responsibilities) + "</p>" : "") +
        (job.skills ? "<h4>" + esc(t.skills) + "</h4><p>" + esc(job.skills) + "</p>" : "") +
        (job.experience_level ? "<p>" + esc(t.experience) + " : " + esc(job.experience_level) + "</p>" : "") +
        "<p>" + esc(t.updated) + " : " + esc(fmtDate(job.published_at)) + (job.expires_at ? " · " + esc(t.deadline) + " " + esc(fmtDate(job.expires_at)) : "") + "</p>" +
        '<p><button type="button" class="tl-btn" id="acc-apply">' + esc(t.apply) + "</button> " +
        '<button type="button" class="tl-btn tl-btn-ghost" id="acc-save-job">' + esc(job.saved ? t.unbookmark : t.bookmark) + "</button></p>" +
        '<div class="tl-success" id="acc-job-msg"></div>';
    }

    function timeline(app) {
      var steps = [
        ["SUBMITTED", t.sent], ["UNDER_REVIEW", t.review], ["SHORTLISTED", t.preselect],
        ["INTERVIEW", t.interview], ["HIRED", t.decision]
      ];
      var order = ["SUBMITTED", "RECEIVED", "UNDER_REVIEW", "SHORTLISTED", "INTERVIEW", "SECOND_INTERVIEW", "OFFER_SENT", "HIRED"];
      var cur = order.indexOf(app.status);
      if (app.status === "REJECTED" || app.status === "WITHDRAWN") cur = -1;
      return '<ol class="tl-timeline">' + steps.map(function (st, i) {
        var idx = order.indexOf(st[0]);
        var cls = cur >= idx ? "is-done" : "";
        if (app.status === st[0] || (st[0] === "UNDER_REVIEW" && app.status === "RECEIVED")) cls = "is-current";
        if (app.status === "HIRED" && st[0] === "HIRED") cls = "is-done";
        return '<li class="' + cls + '"><b>' + esc(st[1]) + "</b></li>";
      }).join("") + "</ol>";
    }

    function renderApps(apps) {
      if (!apps || !apps.length) return empty(t.emptyApps);
      return '<div class="tl-list-cards">' + apps.map(function (a) {
        var job = a.job || {};
        return '<article class="tl-list-card"><span class="tl-chip orange">' + esc(statusLabel(a.status)) + "</span>" +
          "<h3>" + esc(job.title || "") + "</h3><p class=\"tl-meta\">" + esc(job.company_name || "") + " · " + esc(fmtDate(a.created_at)) +
          " · " + esc(t.updated) + " " + esc(fmtDate(a.updated_at)) + "</p>" +
          '<button type="button" class="tl-btn tl-btn-ghost" data-nav="application" data-id="' + esc(a.id) + '">' + esc(t.appDetail) + "</button></article>";
      }).join("") + "</div>";
    }

    function renderAppDetail(a) {
      var job = (a && a.job) || {};
      var canWithdraw = a && ["SUBMITTED", "RECEIVED", "UNDER_REVIEW", "SHORTLISTED"].indexOf(a.status) >= 0;
      return '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="apps">' + (isEn ? "Back" : "Retour") + "</button></p>" +
        "<h3>" + esc(job.title || "") + "</h3><p class=\"tl-meta\">" + esc(job.company_name || "") + " · " + esc(statusLabel(a.status)) + "</p>" +
        timeline(a) + (canWithdraw ? '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-withdraw">' + esc(t.withdraw) + "</button></p>" : "");
    }

    function renderNotifs(notifs) {
      if (!notifs || !notifs.length) return empty(t.emptyNotifs);
      return '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-readall">' + esc(t.markAll) + "</button></p><div class=\"tl-account-notifs\">" +
        notifs.map(function (n) {
          var href = localizeHref(n.href);
          return '<div class="tl-account-notif' + (n.is_read ? "" : " is-unread") + (href ? " is-clickable" : "") + '" data-open-notif="' + esc(n.id) + '" data-href="' + esc(href) + '"><b>' + esc(n.title) + "</b><p>" + esc(n.message) +
            "</p><p class=\"tl-meta\">" + esc(fmtDate(n.created_at)) + (n.is_read ? "" : ' · <button type="button" class="tl-btn tl-btn-ghost" data-read="' + esc(n.id) + '">' + esc(t.markRead) + "</button>") + "</p></div>";
        }).join("") + "</div>";
    }

    function renderMessages(threads, directory, thread) {
      var opts = (directory || []).map(function (p) {
        return '<option value="' + esc(p.id) + '">' + esc((p.first_name || "") + " " + (p.last_name || "") + " — " + statusLabel(p.role || "")) + "</option>";
      }).join("");
      var list = (!threads || !threads.length) ? empty(t.emptyMsgs) : threads.map(function (th) {
        return '<button type="button" class="tl-account-notif' + (th.unread ? " is-unread" : "") + '" data-open-thread="' + esc(th.user_id) + '"><b>' +
          esc((th.first_name || "") + " " + (th.last_name || "")) + "</b><p>" + esc(th.last_message || "") + " · " + esc(fmtDate(th.last_at)) + "</p></button>";
      }).join("");
      var msgs = (thread || []).map(function (m) {
        var mine = state.user && m.sender_id === state.user.id;
        return '<div class="tl-msg-bubble' + (mine ? " is-mine" : "") + '"><b>' + esc(m.sender_name || "") + "</b><p>" + esc(m.body) +
          '</p><p class="tl-meta">' + esc(fmtDate(m.created_at)) + (m.is_read ? "" : " · " + (isEn ? "Unread" : "Non lu")) + "</p></div>";
      }).join("");
      return '<div class="tl-msg-layout"><div>' + list + "</div><form class=\"tl-form\" id=\"acc-msg\"><label>" + esc(t.to) +
        '</label><select name="recipient_id" required>' + opts + "</select><label>" + esc(t.write) +
        '</label><textarea name="body" rows="4" required maxlength="4000"></textarea><button class="tl-btn" type="submit">' +
        esc(t.send) + '</button><div class="tl-success"></div><div id="acc-thread">' + msgs + "</div></form></div>";
    }

    function bindMessages() {
      var form = document.getElementById("acc-msg");
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(form).entries());
        api.request("/messages", { method: "POST", body: { recipient_id: d.recipient_id, body: d.body } }).then(function () { go("messages"); })
          .catch(function (err) { flash(form.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      root.querySelectorAll("[data-open-thread]").forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute("data-open-thread");
          var select = root.querySelector("#acc-msg [name=recipient_id]");
          if (select) select.value = id;
          api.request("/messages/" + id).then(function (json) {
            state.thread = json.data || [];
            go("messages");
          });
        };
      });
    }

    function renderDocs(docs, resumes) {
      var list = (docs || []).map(function (d) {
        return "<li>" + esc(d.original_name) + " · " + esc(d.kind) + ' <button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(d.download_path) + '" data-dl-name="' + esc(d.original_name) + '">' + esc(t.download) +
          '</button> <button type="button" class="tl-btn tl-btn-ghost" data-del-doc="' + esc(d.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>—</li>";
      var cvs = (resumes || []).map(function (r) {
        return "<li>" + esc(r.original_name) + (r.is_primary ? " · CV" : "") +
          ' <button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(r.download_path) + '" data-dl-name="' + esc(r.original_name) + '">' + esc(t.download) + "</button>" +
          ' <button type="button" class="tl-btn tl-btn-ghost" data-del-cv="' + esc(r.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>—</li>";
      return "<h3>CV</h3><ul>" + cvs + '</ul><form class="tl-form" id="acc-cv"><label>' + esc(t.upload) +
        '</label><input name="file" type="file" accept=".pdf,.doc,.docx,application/pdf" required><button class="tl-btn" type="submit">' +
        esc(t.replace) + '</button><div class="tl-success"></div></form><h3>' + esc(t.otherDocs) + "</h3><ul>" + list +
        '</ul><form class="tl-form" id="acc-doc"><label>' + esc(t.upload) + '</label><input name="file" type="file" required>' +
        '<select name="kind"><option value="cover_letter">' + esc(t.cover) + '</option><option value="certification">' +
        esc(t.certs) + '</option><option value="other">' + esc(t.otherDocs) + "</option></select>" +
        '<button class="tl-btn" type="submit">' + esc(t.add) + '</button><div class="tl-success"></div></form>';
    }

    function bindDocs() {
      var cv = document.getElementById("acc-cv");
      if (cv) cv.addEventListener("submit", function (e) {
        e.preventDefault();
        var file = cv.querySelector("[name=file]").files[0];
        if (!file) return;
        var fd = new FormData(); fd.append("file", file);
        api.request("/candidates/me/resume", { method: "POST", body: fd }).then(function () { go("documents"); })
          .catch(function (err) { flash(cv.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var doc = document.getElementById("acc-doc");
      if (doc) doc.addEventListener("submit", function (e) {
        e.preventDefault();
        var file = doc.querySelector("[name=file]").files[0];
        if (!file) return;
        var fd = new FormData();
        fd.append("file", file);
        fd.append("kind", doc.querySelector("[name=kind]").value);
        api.request("/documents", { method: "POST", body: fd }).then(function () { go("documents"); })
          .catch(function (err) { flash(doc.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      root.querySelectorAll("[data-del-cv]").forEach(function (b) {
        b.onclick = function () { api.request("/candidates/me/resume/" + b.getAttribute("data-del-cv"), { method: "DELETE" }).then(function () { go("documents"); }); };
      });
      root.querySelectorAll("[data-del-doc]").forEach(function (b) {
        b.onclick = function () { api.request("/documents/" + b.getAttribute("data-del-doc"), { method: "DELETE" }).then(function () { go("documents"); }); };
      });
    }

    function renderSettings(prefs) {
      prefs = prefs || {};
      return '<form class="tl-form" id="acc-pass"><h3>' + esc(t.security) + "</h3><label>" + esc(t.currentPass) +
        '</label><input name="current_password" type="password" required><label>' + esc(t.newPass) +
        '</label><input name="new_password" type="password" required minlength="8"><button class="tl-btn" type="submit">' +
        esc(t.save) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-prefs"><h3>' + esc(t.notifyPrefs) + "</h3>" +
        '<label><input type="checkbox" name="notify_email"' + (prefs.notify_email !== false ? " checked" : "") + "> " + esc(t.emailNotif) + "</label>" +
        '<label><input type="checkbox" name="notify_in_app"' + (prefs.notify_in_app !== false ? " checked" : "") + "> " + esc(t.inApp) + "</label>" +
        '<label><input type="checkbox" name="notify_sms"' + (prefs.notify_sms ? " checked" : "") + "> " + esc(t.sms) + "</label>" +
        '<label><input type="checkbox" name="notify_whatsapp"' + (prefs.notify_whatsapp ? " checked" : "") + "> " + esc(t.wa) + "</label>" +
        '<label><input type="checkbox" name="notify_push"' + (prefs.notify_push ? " checked" : "") + "> " + esc(t.push) + "</label>" +
        '<h3>' + esc(t.privacy) + "</h3><label><input type=\"checkbox\" name=\"privacy_profile_public\"" + (prefs.privacy_profile_public ? " checked" : "") + "> " +
        esc(t.profilePublic) + '</label><button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-del"><h3>' + esc(t.danger) + '</h3><button class="tl-btn tl-btn-ghost" type="submit">' +
        esc(t.danger) + '</button><div class="tl-success"></div></form>';
    }

    function bindSettings() {
      var pass = document.getElementById("acc-pass");
      if (pass) pass.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(pass).entries());
        api.request("/auth/change-password", { method: "POST", body: d }).then(function () { flash(pass.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(pass.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var prefs = document.getElementById("acc-prefs");
      if (prefs) prefs.addEventListener("submit", function (e) {
        e.preventDefault();
        var body = {};
        ["notify_email", "notify_in_app", "notify_sms", "notify_whatsapp", "notify_push", "privacy_profile_public"].forEach(function (k) {
          body[k] = !!prefs.querySelector("[name=" + k + "]").checked;
        });
        api.request("/users/me/preferences", { method: "PATCH", body: body }).then(function () { flash(prefs.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(prefs.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var del = document.getElementById("acc-del");
      if (del) del.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!window.confirm(t.confirmDanger)) return;
        api.request("/users/me/deactivate", { method: "POST" }).then(function () { api.logout().then(renderGuest); });
      });
    }

    function employerDashboard(user, dash, company) {
      var s = (dash && dash.stats) || {};
      return "<p class=\"tl-lead\">" + esc(t.hello) + " " + esc((company && company.name) || dash.company_name || "") + "</p>" +
        '<div class="tl-stat-grid">' +
        [["active_jobs", t.activeJobs], ["applications", t.inbox], ["shortlisted", t.shortlisted], ["interviews", t.interviews], ["hired", t.hired]].map(function (row) {
          return '<div class="tl-stat-card"><b>' + esc(s[row[0]] || 0) + "</b><span>" + esc(row[1]) + "</span></div>";
        }).join("") + "</div><div class=\"tl-quick-actions\"><button type=\"button\" class=\"tl-btn\" data-nav=\"job-new\">" +
        esc(t.createJob) + "</button><button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-nav=\"inbox\">" + esc(t.inbox) +
        "</button><button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-nav=\"pipeline\">" + esc(t.pipeline) +
        "</button><button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-nav=\"invoices\">" + esc(t.invoices) + "</button></div>";
    }

    function companyForm(company) {
      company = company || {};
      return '<form class="tl-form" id="acc-company"><label>' + esc(t.company) + '</label><input name="name" required value="' + esc(company.name || "") + '">' +
        "<label>" + esc(t.description) + '</label><textarea name="description" rows="4">' + esc(company.description || "") + "</textarea>" +
        '<div class="tl-row-2"><div><label>' + esc(t.sector) + '</label><input name="sector" value="' + esc(company.sector || "") + '"></div>' +
        "<div><label>" + esc(t.website) + '</label><input name="website" value="' + esc(company.website || "") + '"></div></div>' +
        "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(company.address || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.city) + '</label><input name="city" value="' + esc(company.city || "") + '"></div>' +
        "<div><label>" + esc(t.country) + '</label><input name="country" value="' + esc(company.country || "Canada") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.email) + '</label><input name="email" value="' + esc(company.email || "") + '"></div>' +
        "<div><label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(company.phone || "") + '"></div></div>' +
        "<label>" + esc(t.legal) + '</label><input name="legal_name" value="' + esc(company.legal_name || "") + '">' +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>';
    }

    function renderEmployerJobs(jobs) {
      var list = (!jobs || !jobs.length) ? empty(t.emptyJobs) : '<div class="tl-list-cards">' + jobs.map(function (j) {
        var actions = "";
        if (j.status === "DRAFT" || j.status === "PAUSED") actions += '<button type="button" class="tl-btn tl-btn-ghost" data-job-pub="' + esc(j.id) + '">' + esc(t.publish) + "</button> ";
        if (j.status === "PUBLISHED") actions += '<button type="button" class="tl-btn tl-btn-ghost" data-job-pause="' + esc(j.id) + '">' + esc(t.pause) + "</button> ";
        actions += '<button type="button" class="tl-btn tl-btn-ghost" data-job-arch="' + esc(j.id) + '">' + esc(t.archive) + "</button> ";
        actions += '<button type="button" class="tl-btn tl-btn-ghost" data-nav="job-edit" data-id="' + esc(j.id) + '">' + esc(t.edit) + "</button>";
        return '<article class="tl-list-card"><span class="tl-chip orange">' + esc(statusLabel(j.status)) + "</span><h3>" + esc(j.title) +
          "</h3><p class=\"tl-meta\">" + esc(j.location || "") + "</p>" + actions + "</article>";
      }).join("") + "</div>";
      return '<p><button type="button" class="tl-btn" data-nav="job-new">' + esc(t.createJob) + "</button></p>" + list;
    }

    function jobForm(job) {
      job = job || {};
      return '<p>' + esc(t.validate) + '</p><form class="tl-form" id="acc-job-form">' +
        "<label>" + esc(t.title) + '</label><input name="title" required value="' + esc(job.title || "") + '">' +
        "<label>" + esc(t.description) + '</label><textarea name="description" rows="5">' + esc(job.description || "") + "</textarea>" +
        "<label>" + esc(t.responsibilities) + '</label><textarea name="responsibilities" rows="4">' + esc(job.responsibilities || "") + "</textarea>" +
        '<div class="tl-row-2"><div><label>' + esc(t.location) + '</label><input name="location" value="' + esc(job.location || "") + '"></div>' +
        "<div><label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(job.sector || "") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.contract) + '</label><input name="contract_type" value="' + esc(job.contract_type || "") + '"></div>' +
        "<div><label>" + esc(t.experience) + '</label><input name="experience_level" value="' + esc(job.experience_level || "") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.salary) + " min</label><input name=\"salary_min\" type=\"number\" value=\"" + esc(job.salary_min || "") + '"></div>' +
        "<div><label>" + esc(t.salary) + " max</label><input name=\"salary_max\" type=\"number\" value=\"" + esc(job.salary_max || "") + '"></div></div>' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(job.skills || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.openings) + '</label><input name="openings" type="number" min="1" value="' + esc(job.openings || 1) + '"></div>' +
        "<div><label>" + esc(t.startDate) + '</label><input name="start_date" type="date" value="' + esc(job.start_date || "") + '"></div></div>' +
        "<label>" + esc(t.deadline) + '</label><input name="expires_at" type="date" value="' + esc((job.expires_at || "").slice(0, 10)) + '">' +
        "<label>" + esc(t.extra) + '</label><textarea name="benefits" rows="3">' + esc(job.benefits || "") + "</textarea>" +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>';
    }

    function renderInbox(apps) {
      if (!apps || !apps.length) return empty(t.emptyInbox);
      var opts = ["SUBMITTED", "UNDER_REVIEW", "SHORTLISTED", "INTERVIEW", "SECOND_INTERVIEW", "OFFER_SENT", "HIRED", "REJECTED"];
      return '<div class="tl-table-wrap"><table class="tl-portal-table"><thead><tr><th>' + esc(t.first) + "</th><th>" + esc(t.title) +
        "</th><th>" + esc(t.apps) + "</th><th>" + esc(t.experience) + "</th><th></th></tr></thead><tbody>" + apps.map(function (a) {
        var c = a.candidate || {};
        var job = a.job || {};
        return "<tr><td data-label=\"" + esc(t.first) + "\">" + esc((c.first_name || "") + " " + (c.last_name || "")) +
          "</td><td data-label=\"" + esc(t.title) + "\">" + esc(c.title || job.title || "") + "</td><td data-label=\"" + esc(t.apps) + "\">" +
          '<select data-app-status="' + esc(a.id) + '">' + opts.map(function (s) {
            return '<option value="' + s + '"' + (a.status === s ? " selected" : "") + ">" + esc(statusLabel(s)) + "</option>";
          }).join("") + "</select></td><td data-label=\"" + esc(t.experience) + "\">" + esc(c.years_experience || "—") +
          '</td><td><button type="button" class="tl-btn tl-btn-ghost" data-nav="candidate" data-id="' + esc(c.id || "") + '">' +
          esc(t.candidates) + "</button></td></tr>";
      }).join("") + "</tbody></table></div>";
    }

    function money(amount) {
      var n = Number(amount) || 0;
      try {
        return new Intl.NumberFormat(isEn ? "en-CA" : "fr-CA", { style: "currency", currency: "CAD", maximumFractionDigits: 0 }).format(n);
      } catch (e) {
        return n + " $";
      }
    }

    function renderInvoices(rows) {
      if (!rows || !rows.length) return empty(t.emptyInvoices);
      var payable = { SENT: 1, PENDING: 1, OVERDUE: 1 };
      return '<div class="tl-table-wrap"><table class="tl-portal-table"><thead><tr><th>' + esc(t.invoices) + "</th><th>" + esc(t.salary) +
        "</th><th></th><th></th></tr></thead><tbody>" + rows.map(function (inv) {
        var pay = payable[inv.status] ? '<button type="button" class="tl-btn" data-pay="' + esc(inv.id) + '">' + esc(t.pay) + "</button>" : "";
        return "<tr><td data-label=\"" + esc(t.invoices) + "\">" + esc(inv.number || inv.id) +
          "</td><td data-label=\"" + esc(t.salary) + "\">" + esc(money(inv.amount_total || inv.amount)) +
          "</td><td><span class=\"tl-chip\">" + esc(statusLabel(inv.status)) + "</span></td><td>" + pay + "</td></tr>";
      }).join("") + "</tbody></table></div><div class=\"tl-success\" id=\"acc-inv-msg\"></div>";
    }

    function renderPipeline(apps) {
      var stages = [
        ["nouveaux", t.sent], ["preselection", t.review], ["presentation", t.preselect],
        ["entretien-talendus", t.interview], ["entretien-client", isEn ? "Client interview" : "Entretien client"],
        ["offre", isEn ? "Offer" : "Offre"], ["placement", t.hired]
      ];
      var opts = ["SUBMITTED", "UNDER_REVIEW", "SHORTLISTED", "INTERVIEW", "SECOND_INTERVIEW", "OFFER_SENT", "HIRED", "REJECTED"];
      var grouped = {};
      stages.forEach(function (st) { grouped[st[0]] = []; });
      (apps || []).forEach(function (a) {
        var key = a.pipeline_stage || "nouveaux";
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(a);
      });
      return '<div class="tl-pipeline">' + stages.map(function (st) {
        var cards = (grouped[st[0]] || []).map(function (a) {
          var c = a.candidate || {};
          var job = a.job || {};
          return '<article class="tl-pipe-card"><b>' + esc((c.first_name || "") + " " + (c.last_name || "")) +
            "</b><p class=\"tl-meta\">" + esc(job.title || "") + "</p>" +
            '<select data-app-status="' + esc(a.id) + '">' + opts.map(function (s) {
              return '<option value="' + s + '"' + (a.status === s ? " selected" : "") + ">" + esc(statusLabel(s)) + "</option>";
            }).join("") + "</select>" +
            (c.id ? '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="candidate" data-id="' + esc(c.id) + '">' + esc(t.candidates) + "</button></p>" : "") +
            "</article>";
        }).join("");
        return '<section class="tl-pipe-col"><h4>' + esc(st[1]) + " <span>" + (grouped[st[0]] || []).length + "</span></h4>" +
          (cards || '<p class="tl-meta">—</p>') + "</section>";
      }).join("") + "</div>";
    }

    function renderMembers(members) {
      var rows = (members || []).map(function (m) {
        return "<tr><td data-label=\"" + esc(t.first) + "\">" + esc((m.first_name || "") + " " + (m.last_name || "")) +
          "</td><td>" + esc(m.email || "") + "</td><td>" + esc(statusLabel(m.member_role)) + "</td></tr>";
      }).join("");
      return '<div class="tl-table-wrap"><table class="tl-portal-table"><tbody>' + (rows || "") + "</tbody></table></div>" +
        '<form class="tl-form" id="acc-invite"><h3>' + esc(t.invite) + "</h3><div class=\"tl-row-2\"><input name=\"first_name\" required placeholder=\"" +
        esc(t.first) + '"><input name="last_name" required placeholder="' + esc(t.last) + '"></div>' +
        '<input name="email" type="email" required><select name="member_role"><option value="HR">RH</option><option value="RECRUITER">' +
        (isEn ? "Recruiter" : "Recruteur") + '</option><option value="ADMIN">' + (isEn ? "Administrator" : "Administrateur") +
        '</option><option value="BILLING">Billing</option></select><button class="tl-btn" type="submit">' + esc(t.invite) +
        '</button><div class="tl-success"></div></form>';
    }

    var state = { user: null, unreadN: 0, unreadM: 0, jobFilters: {} };

    function bindCommon() {
      var mark = document.getElementById("acc-readall");
      if (mark) mark.onclick = function () { api.request("/notifications/read-all", { method: "POST" }).then(function () { go("notifs"); }); };
      root.querySelectorAll("[data-read]").forEach(function (b) {
        b.onclick = function (ev) {
          ev.stopPropagation();
          api.request("/notifications/" + b.getAttribute("data-read") + "/read", { method: "POST" }).then(function () { go("notifs"); });
        };
      });
      root.querySelectorAll("[data-job-pub]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-pub") + "/publish", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-pause]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-pause") + "/pause", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-arch]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-arch") + "/archive", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-app-status]").forEach(function (sel) {
        sel.onchange = function () {
          var dest = currentRoute().name === "pipeline" ? "pipeline" : "inbox";
          api.request("/applications/" + sel.getAttribute("data-app-status") + "/status", { method: "POST", body: { status: sel.value } }).then(function () { go(dest); });
        };
      });
      root.querySelectorAll("[data-open-notif]").forEach(function (el) {
        el.onclick = function (ev) {
          if (ev.target && ev.target.closest && ev.target.closest("[data-read]")) return;
          var href = el.getAttribute("data-href") || "";
          var id = el.getAttribute("data-open-notif");
          var open = function () {
            if (!href) return;
            var hash = href.split("#")[1] || "";
            var parts = hash.replace(/^\//, "").split("/");
            if (parts[0] && (href.indexOf("espace") !== -1 || href.indexOf("account") !== -1 || href.indexOf("/candidate") !== -1 || href.indexOf("/employer") !== -1)) {
              var mapped = normalizeRoute(parts[0], parts[1] || "");
              go(mapped.name, mapped.id);
              return;
            }
            window.location.href = href;
          };
          if (id) api.request("/notifications/" + id + "/read", { method: "POST" }).then(open).catch(open);
          else open();
        };
      });
      root.querySelectorAll("[data-pay]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/invoices/" + btn.getAttribute("data-pay") + "/checkout", { method: "POST" }).then(function (json) {
            var url = json && json.data && json.data.checkout_url;
            if (url) window.location.href = url;
            else flash(document.getElementById("acc-inv-msg"), t.success, true);
          }).catch(function (err) {
            flash(document.getElementById("acc-inv-msg"), (err && err.message) || t.err, false);
          });
        };
      });
      root.querySelectorAll("[data-int-status]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/interviews/" + btn.getAttribute("data-int-id") + "/status", { method: "POST", body: { status: btn.getAttribute("data-int-status") } }).then(function () { go("interviews"); });
        };
      });
      var apply = document.getElementById("acc-apply");
      if (apply && state.job) apply.onclick = function () {
        api.request("/applications", { method: "POST", body: { job_id: state.job.id, job_slug: state.job.slug } })
          .then(function () { go("apps"); })
          .catch(function (err) { flash(document.getElementById("acc-job-msg"), (err && err.message) || t.err, false); });
      };
      var saveBtn = document.getElementById("acc-save-job");
      if (saveBtn && state.job) saveBtn.onclick = function () {
        var method = state.job.saved ? "DELETE" : "POST";
        api.request("/jobs/" + state.job.id + "/save", { method: method }).then(function () { go("job", state.job.slug); });
      };
      var withdraw = document.getElementById("acc-withdraw");
      if (withdraw && state.application) withdraw.onclick = function () {
        api.request("/applications/" + state.application.id + "/withdraw", { method: "POST" }).then(function () { go("apps"); });
      };
      var company = document.getElementById("acc-company");
      if (company && state.company) company.addEventListener("submit", function (e) {
        e.preventDefault();
        api.request("/companies/" + state.company.id, { method: "PATCH", body: Object.fromEntries(new FormData(company).entries()) })
          .then(function () { flash(company.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(company.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var jobFormEl = document.getElementById("acc-job-form");
      if (jobFormEl) jobFormEl.addEventListener("submit", function (e) {
        e.preventDefault();
        var body = Object.fromEntries(new FormData(jobFormEl).entries());
        if (body.salary_min) body.salary_min = Number(body.salary_min);
        if (body.salary_max) body.salary_max = Number(body.salary_max);
        if (body.openings) body.openings = Number(body.openings);
        var req = state.editJob
          ? api.request("/jobs/" + state.editJob.id, { method: "PATCH", body: body })
          : api.request("/jobs", { method: "POST", body: body });
        req.then(function () { go("jobs"); }).catch(function (err) { flash(jobFormEl.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var invite = document.getElementById("acc-invite");
      if (invite) invite.addEventListener("submit", function (e) {
        e.preventDefault();
        api.request("/companies/me/members", { method: "POST", body: Object.fromEntries(new FormData(invite).entries()) })
          .then(function () { go("settings"); }).catch(function (err) { flash(invite.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var intForm = document.getElementById("acc-int");
      if (intForm) {
        var sel = intForm.querySelector("[name=candidate_id]");
        var appField = intForm.querySelector("[name=application_id]");
        function syncApp() {
          if (!sel || !appField) return;
          var opt = sel.options[sel.selectedIndex];
          appField.value = opt ? (opt.getAttribute("data-app") || "") : "";
        }
        if (sel) { sel.onchange = syncApp; syncApp(); }
        intForm.addEventListener("submit", function (e) {
          e.preventDefault();
          syncApp();
          api.request("/interviews", { method: "POST", body: Object.fromEntries(new FormData(intForm).entries()) })
            .then(function () { go("interviews"); }).catch(function (err) { flash(intForm.querySelector(".tl-success"), (err && err.message) || t.err, false); });
        });
      }
      bindMessages();
      bindDocs();
      bindSettings();
      bindProfile(state.user);
      bindJobsSearch();
      root.querySelectorAll("[data-dl]").forEach(function (b) {
        b.onclick = function () { authDownload(b.getAttribute("data-dl"), b.getAttribute("data-dl-name") || "document"); };
      });
    }

    function renderInterviews(items, apps) {
      var list = (!items || !items.length) ? empty(t.emptyInts) : items.map(function (i) {
        var actions = "";
        if (i.status === "SCHEDULED") {
          actions = '<p><button type="button" class="tl-btn tl-btn-ghost" data-int-status="CONFIRMED" data-int-id="' + esc(i.id) + '">' + esc(t.confirm) +
            '</button> <button type="button" class="tl-btn tl-btn-ghost" data-int-status="CANCELLED" data-int-id="' + esc(i.id) + '">' + esc(t.cancel) + "</button></p>";
        }
        return '<div class="tl-account-notif"><b>' + esc(i.type_label || i.type) + " · " + esc(statusLabel(i.status)) + "</b><p>" +
          esc(fmtDate(i.scheduled_at)) + " · " + esc(i.location || i.meeting_url || "") + (i.job_title ? " · " + esc(i.job_title) : "") +
          (i.candidate_name ? " · " + esc(i.candidate_name) : "") + "</p>" + actions + "</div>";
      }).join("");
      var form = "";
      if (isEmployerSpace() && apps && apps.length) {
        form = '<form class="tl-form" id="acc-int"><h3>' + esc(t.schedule) + "</h3><label>" + esc(t.candidates) +
          '</label><select name="candidate_id" required>' + apps.map(function (a) {
            var c = a.candidate || {};
            return '<option value="' + esc(c.id || "") + '" data-app="' + esc(a.id) + '">' + esc((c.first_name || "") + " " + (c.last_name || "") + " — " + ((a.job || {}).title || "")) + "</option>";
          }).join("") + '</select><input type="hidden" name="application_id"><label>' + esc(t.when) +
          '</label><input name="scheduled_at" type="datetime-local" required><label>' + esc(t.place) +
          '</label><input name="location"><label>' + esc(t.type) + '</label><select name="type"><option value="CLIENT">Client</option><option value="VIDEO">Visio</option><option value="PHONE">Téléphone</option><option value="ONSITE">Sur place</option></select>' +
          "<label>" + (isEn ? "Meeting link (optional)" : "Lien visio (optionnel)") + '</label><input name="meeting_url" placeholder="https://">' +
          '<button class="tl-btn" type="submit">' + esc(t.schedule) + '</button><div class="tl-success"></div></form>';
      }
      return list + form;
    }

    function countsThen(cb) {
      Promise.all([
        api.notifications().then(function (j) { return j; }).catch(function () { return { data: [], meta: {} }; }),
        api.request("/messages").then(function (j) { return j.data || []; }).catch(function () { return []; })
      ]).then(function (rows) {
        state.unreadN = (rows[0].meta && rows[0].meta.unread) || (rows[0].data || []).filter(function (n) { return !n.is_read; }).length;
        state.unreadM = (rows[1] || []).reduce(function (s, th) { return s + (th.unread || 0); }, 0);
        state.notifs = rows[0].data || [];
        state.threads = rows[1];
        cb();
      });
    }

    function renderAuthed() {
      var user = state.user;
      var route = currentRoute();
      countsThen(function () {
        shell(user, skeleton(), state.unreadN, state.unreadM);
        var p;
        if (isEmployerSpace()) {
          if (route.name === "dashboard") p = Promise.all([unwrap(api.request("/companies/me/dashboard")), unwrap(api.request("/companies/me"))]).then(function (r) {
            return employerDashboard(user, r[0], r[1]);
          });
          else if (route.name === "company") p = unwrap(api.request("/companies/me")).then(function (c) { state.company = c; return companyForm(c); });
          else if (route.name === "jobs") p = unwrap(api.request("/jobs/managed")).then(renderEmployerJobs);
          else if (route.name === "job-new") p = Promise.resolve(jobForm({}));
          else if (route.name === "job-edit") p = unwrap(api.request("/jobs/managed/" + route.id)).then(function (j) { state.editJob = j; return jobForm(j); });
          else if (route.name === "inbox" || route.name === "candidates") p = unwrap(api.request("/applications")).then(renderInbox);
          else if (route.name === "pipeline") p = unwrap(api.request("/applications")).then(renderPipeline);
          else if (route.name === "invoices") p = unwrap(api.request("/invoices")).then(renderInvoices);
          else if (route.name === "candidate") p = unwrap(api.request("/candidates/" + route.id)).then(function (c) {
            return "<h3>" + esc((c.first_name || "") + " " + (c.last_name || "")) + "</h3><p>" + esc(c.title || "") + " · " + esc(c.city || "") +
              "</p><p>" + esc(c.skills || "") + "</p>" + ((c.resumes || []).map(function (r) {
                return '<p><button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(r.download_path) + '" data-dl-name="' + esc(r.original_name || "cv.pdf") + '">' + esc(t.download) + " CV</button></p>";
              }).join("") || "");
          });
          else if (route.name === "interviews") p = Promise.all([unwrap(api.request("/interviews")), unwrap(api.request("/applications"))]).then(function (r) {
            return renderInterviews(r[0], r[1]);
          });
          else if (route.name === "messages") p = Promise.all([
            unwrap(api.request("/messages")), unwrap(api.request("/messages/directory"))
          ]).then(function (r) { return renderMessages(r[0], r[1], state.thread); });
          else if (route.name === "documents") p = unwrap(api.request("/documents?owner_type=company")).then(function (docs) { return renderDocs(docs, []); });
          else if (route.name === "notifs") p = Promise.resolve(renderNotifs(state.notifs));
          else if (route.name === "settings") p = Promise.all([
            unwrap(api.request("/users/me/preferences")), unwrap(api.request("/companies/me/members"))
          ]).then(function (r) { return renderSettings(r[0]) + "<h3>" + esc(t.members) + "</h3>" + renderMembers(r[1]); });
          else p = Promise.resolve(empty(t.err));
        } else {
          if (route.name === "dashboard") p = Promise.all([unwrap(api.request("/candidates/me/dashboard")), unwrap(api.request("/candidates/me"))]).then(function (r) {
            return renderCandidateDashboard(user, r[0], r[1]);
          });
          else if (route.name === "profile") p = unwrap(api.request("/candidates/me")).then(function (pr) { return profileForm(user, pr); });
          else if (route.name === "jobs") p = (state.jobs ? Promise.resolve(state.jobs) : api.request("/jobs")).then(renderJobsSearch);
          else if (route.name === "job") p = unwrap(api.request("/jobs/" + route.id)).then(function (j) { state.job = j; return renderJobDetail(j); });
          else if (route.name === "apps") p = unwrap(api.myApplications()).then(renderApps);
          else if (route.name === "application") p = unwrap(api.request("/applications/" + route.id)).then(function (a) { state.application = a; return renderAppDetail(a); });
          else if (route.name === "interviews") p = unwrap(api.request("/interviews")).then(function (rows) { return renderInterviews(rows); });
          else if (route.name === "messages") p = Promise.all([
            unwrap(api.request("/messages")), unwrap(api.request("/messages/directory"))
          ]).then(function (r) { return renderMessages(r[0], r[1], state.thread); });
          else if (route.name === "documents") p = Promise.all([
            unwrap(api.request("/documents")), unwrap(api.request("/candidates/me"))
          ]).then(function (r) { return renderDocs(r[0], (r[1] && r[1].resumes) || []); });
          else if (route.name === "notifs") p = Promise.resolve(renderNotifs(state.notifs));
          else if (route.name === "settings") p = unwrap(api.request("/users/me/preferences")).then(renderSettings);
          else p = Promise.resolve(empty(t.err));
        }
        p.then(function (html) {
          shell(user, html, state.unreadN, state.unreadM);
          bindCommon();
        }).catch(function (err) {
          shell(user, errBox((err && err.message) || t.err), state.unreadN, state.unreadM);
          var retry = root.querySelector("[data-retry]");
          if (retry) retry.onclick = renderAuthed;
        });
      });
    }

    function boot() {
      if (isEmployerSpace() && /[?&]paid=/.test(location.search || "")) {
        if (!(location.hash || "").replace("#", "")) location.hash = "#/invoices";
      }
      var user = api.currentUser();
      if (user && staffRole(user.role)) { window.location.replace(accountHref(user.role)); return; }
      if (user && user.role === "EMPLOYER" && !isEmployerSpace()) { window.location.replace(accountHref("EMPLOYER")); return; }
      if (user && user.role === "CANDIDATE" && isEmployerSpace()) { window.location.replace(accountHref("CANDIDATE")); return; }
      if (!user) { renderGuest(); return; }
      state.user = user;
      api.me().then(function (j) { state.user = j.data; renderAuthed(); }).catch(function () { renderGuest(); });
    }

    window.addEventListener("hashchange", function () { if (state.user) renderAuthed(); });
    window.addEventListener("popstate", function () { if (state.user) renderAuthed(); });
    boot();
  });
})();
