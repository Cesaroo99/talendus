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
    var t = isEn ? {
      login: "Sign in",
      register: "Create an account",
      email: "Email",
      password: "Password",
      first: "First name",
      last: "Last name",
      submitLogin: "Sign in",
      submitRegister: "Create my account",
      logout: "Sign out",
      profile: "Profile",
      apps: "Applications",
      notifs: "Notifications",
      cv: "Resume",
      save: "Save",
      city: "City",
      title: "Target role",
      sector: "Sector",
      skills: "Skills",
      phone: "Phone",
      upload: "Upload a PDF, DOC or DOCX",
      emptyApps: "No applications yet.",
      emptyNotifs: "No notifications.",
      markAll: "Mark all as read",
      welcome: "Your industrial file",
      guest: "Sign in to follow your applications.",
      err: "Something went wrong.",
      saved: "Profile updated.",
      uploaded: "Resume saved."
    } : {
      login: "Connexion",
      register: "Créer un compte",
      email: "Courriel",
      password: "Mot de passe",
      first: "Prénom",
      last: "Nom",
      submitLogin: "Me connecter",
      submitRegister: "Créer mon compte",
      logout: "Déconnexion",
      profile: "Profil",
      apps: "Candidatures",
      notifs: "Notifications",
      cv: "CV",
      save: "Enregistrer",
      city: "Ville",
      title: "Métier visé",
      sector: "Secteur",
      skills: "Compétences",
      phone: "Téléphone",
      upload: "Téléverser un PDF, DOC ou DOCX",
      emptyApps: "Aucune candidature pour le moment.",
      emptyNotifs: "Aucune notification.",
      markAll: "Tout marquer comme lu",
      welcome: "Votre dossier industriel",
      guest: "Connectez-vous pour suivre vos candidatures.",
      err: "Une erreur s’est produite.",
      saved: "Profil mis à jour.",
      uploaded: "CV enregistré."
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    function statusLabel(s) {
      var map = {
        SUBMITTED: isEn ? "Submitted" : "Envoyée",
        UNDER_REVIEW: isEn ? "Under review" : "En revue",
        SHORTLISTED: isEn ? "Shortlisted" : "Présélection",
        INTERVIEW: isEn ? "Interview" : "Entretien",
        REJECTED: isEn ? "Declined" : "Refusée",
        HIRED: isEn ? "Hired" : "Embauché",
        WITHDRAWN: isEn ? "Withdrawn" : "Retirée"
      };
      return map[s] || s;
    }

    function renderGuest() {
      root.innerHTML = '<div class="tl-account-grid">' +
        '<div><div class="tl-kicker">Talendus</div><h2 class="tl-h2">' + esc(t.welcome) + '</h2><p class="tl-lead">' + esc(t.guest) + "</p></div>" +
        '<div class="tl-account-cards">' +
        '<form class="tl-form" id="acc-login"><h3>' + esc(t.login) + "</h3>" +
        "<label>" + esc(t.email) + '</label><input name="email" type="email" required>' +
        "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
        '<button class="tl-btn" type="submit">' + esc(t.submitLogin) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-register"><h3>' + esc(t.register) + "</h3>" +
        "<label>" + esc(t.first) + '</label><input name="first_name" required>' +
        "<label>" + esc(t.last) + '</label><input name="last_name" required>' +
        "<label>" + esc(t.email) + '</label><input name="email" type="email" required>' +
        "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
        '<button class="tl-btn tl-btn-electric" type="submit">' + esc(t.submitRegister) + '</button><div class="tl-success"></div></form>' +
        "</div></div>";
      bindGuest();
    }

    function bindGuest() {
      var login = document.getElementById("acc-login");
      var reg = document.getElementById("acc-register");
      login.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(login).entries());
        api.login(d.email, d.password).then(boot).catch(function (err) {
          login.querySelector(".tl-success").style.display = "block";
          login.querySelector(".tl-success").textContent = (err && err.message) || t.err;
        });
      });
      reg.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(reg).entries());
        api.register({ email: d.email, password: d.password, first_name: d.first_name, last_name: d.last_name, role: "CANDIDATE" }).then(boot).catch(function (err) {
          reg.querySelector(".tl-success").style.display = "block";
          reg.querySelector(".tl-success").textContent = (err && err.message) || t.err;
        });
      });
    }

    function renderApp(user, profile, apps, notifs) {
      var unread = (notifs || []).filter(function (n) { return !n.is_read; }).length;
      root.innerHTML = '<div class="tl-account-head"><div><div class="tl-kicker">' + esc(user.email) + "</div>" +
        '<h2 class="tl-h2">' + esc((user.first_name || "") + " " + (user.last_name || "")) + "</h2></div>" +
        '<button class="tl-btn tl-btn-ghost" type="button" id="acc-logout">' + esc(t.logout) + "</button></div>" +
        '<div class="tl-account-tabs" role="tablist">' +
        '<button type="button" class="is-active" data-tab="profile">' + esc(t.profile) + "</button>" +
        '<button type="button" data-tab="apps">' + esc(t.apps) + " (" + (apps || []).length + ")</button>" +
        '<button type="button" data-tab="notifs">' + esc(t.notifs) + (unread ? " · " + unread : "") + "</button>" +
        '<button type="button" data-tab="cv">' + esc(t.cv) + "</button></div>" +
        '<div class="tl-account-panel" data-panel="profile">' +
        '<form class="tl-form" id="acc-profile">' +
        "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(user.phone || "") + '">' +
        "<label>" + esc(t.city) + '</label><input name="city" value="' + esc(profile.city || "") + '">' +
        "<label>" + esc(t.title) + '</label><input name="title" value="' + esc(profile.title || "") + '">' +
        "<label>" + esc(t.sector) + '</label><input name="sector" value="' + esc(profile.sector || "") + '">' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(profile.skills || "") + '">' +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form></div>' +
        '<div class="tl-account-panel" data-panel="apps" hidden>' + renderApps(apps) + "</div>" +
        '<div class="tl-account-panel" data-panel="notifs" hidden>' + renderNotifs(notifs) + "</div>" +
        '<div class="tl-account-panel" data-panel="cv" hidden><form class="tl-form" id="acc-cv">' +
        "<label>" + esc(t.upload) + '</label><input name="file" type="file" accept=".pdf,.doc,.docx,application/pdf" required>' +
        '<button class="tl-btn" type="submit">' + esc(t.cv) + '</button><div class="tl-success"></div>' +
        renderResumes(profile.resumes) + "</form></div>";
      document.getElementById("acc-logout").onclick = function () { api.logout().then(renderGuest); };
      root.querySelectorAll("[data-tab]").forEach(function (btn) {
        btn.onclick = function () {
          root.querySelectorAll("[data-tab]").forEach(function (b) { b.classList.toggle("is-active", b === btn); });
          root.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== btn.getAttribute("data-tab"); });
        };
      });
      document.getElementById("acc-profile").addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(e.target).entries());
        Promise.all([
          api.request("/users/me", { method: "PATCH", body: { phone: d.phone } }),
          api.request("/candidates/me", { method: "PATCH", body: { city: d.city, title: d.title, sector: d.sector, skills: d.skills } })
        ]).then(function () {
          var box = e.target.querySelector(".tl-success");
          box.style.display = "block";
          box.textContent = t.saved;
        }).catch(function (err) {
          var box = e.target.querySelector(".tl-success");
          box.style.display = "block";
          box.textContent = (err && err.message) || t.err;
        });
      });
      document.getElementById("acc-cv").addEventListener("submit", function (e) {
        e.preventDefault();
        var file = e.target.querySelector("[name=file]").files[0];
        if (!file) return;
        var fd = new FormData();
        fd.append("file", file);
        api.request("/candidates/me/resume", { method: "POST", body: fd }).then(function () {
          var box = e.target.querySelector(".tl-success");
          box.style.display = "block";
          box.textContent = t.uploaded;
          boot();
        }).catch(function (err) {
          var box = e.target.querySelector(".tl-success");
          box.style.display = "block";
          box.textContent = (err && err.message) || t.err;
        });
      });
      var mark = document.getElementById("acc-readall");
      if (mark) mark.onclick = function () { api.request("/notifications/read-all", { method: "POST" }).then(boot); };
    }

    function renderApps(apps) {
      if (!apps || !apps.length) return "<p>" + esc(t.emptyApps) + "</p>";
      return '<div class="tl-grid-2">' + apps.map(function (a) {
        var job = a.job || {};
        var href = (isEn ? "job-" : "emploi-") + (job.slug || "") + ".html";
        return '<article class="tl-job-card"><div class="body"><span class="tl-chip orange">' + esc(statusLabel(a.status)) + "</span>" +
          "<h3>" + esc(job.title || "") + "</h3><p>" + esc(job.company_name || "") + " · " + esc(job.location || "") + "</p>" +
          (job.slug ? '<a class="tl-split-cta" href="' + href + '" style="color:var(--tl-orange);margin-top:auto;padding-top:14px">' + (isEn ? "View role →" : "Voir le poste →") + "</a>" : "") +
          "</div></article>";
      }).join("") + "</div>";
    }

    function renderNotifs(notifs) {
      if (!notifs || !notifs.length) return "<p>" + esc(t.emptyNotifs) + "</p>";
      return '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-readall">' + esc(t.markAll) + "</button></p><div class="tl-account-notifs">' +
        notifs.map(function (n) {
          return '<div class="tl-account-notif' + (n.is_read ? "" : " is-unread") + '"><b>' + esc(n.title) + "</b><p>" + esc(n.message) + "</p></div>";
        }).join("") + "</div>";
    }

    function renderResumes(resumes) {
      if (!resumes || !resumes.length) return "";
      return "<ul>" + resumes.map(function (r) {
        return "<li>" + esc(r.original_name) + (r.is_primary ? " · CV" : "") + "</li>";
      }).join("") + "</ul>";
    }

    function boot() {
      var user = api.currentUser();
      if (!user) { renderGuest(); return; }
      Promise.all([
        api.me().then(function (j) { return j.data; }),
        api.request("/candidates/me").then(function (j) { return j.data; }).catch(function () { return {}; }),
        api.myApplications().then(function (j) { return j.data || []; }).catch(function () { return []; }),
        api.notifications().then(function (j) { return j.data || []; }).catch(function () { return []; })
      ]).then(function (rows) {
        renderApp(rows[0], rows[1] || {}, rows[2], rows[3]);
      }).catch(function () { renderGuest(); });
    }

    boot();
  });
})();
