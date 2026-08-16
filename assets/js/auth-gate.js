(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    if (!window.TalendusAPI) return;
    var api = window.TalendusAPI;
    var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    var t = isEn ? {
      login: "Sign in", register: "Create an account", email: "Email", password: "Password",
      first: "First name", last: "Last name", submitLogin: "Sign in", submitRegister: "Create my account",
      forgot: "Forgot password?", sendReset: "Send reset link", back: "Back",
      choose: "Who are you?", seek: "Candidate", hire: "Employer",
      company: "Company name", close: "Close", or: "or", google: "Continue with Google",
      linkedin: "Continue with LinkedIn", soon: "Coming soon",
      resetTitle: "Choose a new password", resetBtn: "Update password",
      verifyTitle: "Confirming your email…", verifyOk: "Email verified. You can sign in.",
      forgotTitle: "Reset your password", forgotOk: "If an account exists, we sent an email.",
      guestCta: "Sign in", dashboard: "Dashboard", logout: "Sign out",
      saveJob: "Save job", savedJob: "Saved", applyTrack: "Create an account to track this application",
      needAccount: "Create an account to continue",
      err: "Something went wrong.",
      brand: "We hire for Quebec plants.",
      point1: "A consultant presents the files.",
      point2: "Candidates and employers stay on their own side.",
      loginLead: "Enter your workspace.",
      registerLead: "Takes five minutes. Free for talent.",
      registerEmployerLead: "Open a mandate and follow the files we present.",
      chooseLead: "This decides what you see next.",
      seekHint: "I'm looking for plant work",
      hireHint: "I have a role to fill",
      haveAccount: "Already have an account? Sign in",
      noAccount: "No account yet? Create one",
      home: "Home"
    } : {
      login: "Connexion", register: "Créer un compte", email: "Courriel", password: "Mot de passe",
      first: "Prénom", last: "Nom", submitLogin: "Me connecter", submitRegister: "Créer mon compte",
      forgot: "Mot de passe oublié ?", sendReset: "Envoyer le lien", back: "Retour",
      choose: "Vous êtes", seek: "Candidat", hire: "Entreprise",
      company: "Nom de l'entreprise", close: "Fermer", or: "ou", google: "Continuer avec Google",
      linkedin: "Continuer avec LinkedIn", soon: "Bientôt disponible",
      resetTitle: "Choisissez un nouveau mot de passe", resetBtn: "Mettre à jour",
      verifyTitle: "Vérification du courriel…", verifyOk: "Courriel vérifié. Vous pouvez vous connecter.",
      forgotTitle: "Réinitialiser le mot de passe", forgotOk: "Si un compte existe, un courriel a été envoyé.",
      guestCta: "Connexion", dashboard: "Tableau de bord", logout: "Déconnexion",
      saveJob: "Sauvegarder", savedJob: "Sauvegardée", applyTrack: "Créer un compte pour suivre cette candidature",
      needAccount: "Créez un compte pour continuer",
      err: "Une erreur s’est produite.",
      brand: "On recrute pour les usines du Québec.",
      point1: "Un conseiller présente les dossiers.",
      point2: "Candidats et employeurs, chacun de son côté.",
      loginLead: "Entrez dans votre espace.",
      registerLead: "Cinq minutes. C'est gratuit pour les talents.",
      registerEmployerLead: "Ouvrez un mandat et suivez les dossiers présentés.",
      chooseLead: "Ça détermine ce que vous voyez ensuite.",
      seekHint: "Je cherche un emploi en usine",
      hireHint: "J'ai un poste à pourvoir",
      haveAccount: "Déjà un compte ? Connexion",
      noAccount: "Pas encore de compte ? Inscription",
      home: "Accueil"
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    function staffRole(role) {
      return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
    }
    function siteRoot() { return isEn ? "/en/" : "/"; }
    function assetPrefix() {
      var img = document.querySelector(".vl-logo img");
      var src = img && img.getAttribute("src");
      if (src) return src.replace(/assets\/img\/logo\/[^/?#]+$/, "");
      return isEn ? "../" : "";
    }
    function logoUrl() { return assetPrefix() + "assets/img/logo/logo1.png"; }
    function plantUrl() { return assetPrefix() + "assets/img/all-images/industry/usine-equipe.jpg"; }
    function homeHref() { return siteRoot() + "index.html"; }
    var MARK_SVG = '<svg viewBox="0 0 36 36" aria-hidden="true"><path fill="#ffffff" fill-rule="evenodd" d="M18 1.5c9.113 0 16.5 7.387 16.5 16.5S27.113 34.5 18 34.5 1.5 27.113 1.5 18 8.887 1.5 18 1.5zm-7.25 9.75h14.5a1.75 1.75 0 1 1 0 3.5h-5.5v12.75a1.75 1.75 0 1 1-3.5 0V14.75h-5.5a1.75 1.75 0 1 1 0-3.5z"/></svg>';

    function brandPanel() {
      return '<aside class="tl-auth-brand">' +
        '<img class="tl-auth-photo" src="' + esc(plantUrl()) + '" alt="" width="600" height="800">' +
        '<div class="tl-auth-brand-inner">' +
          '<div class="tl-auth-mark">' + MARK_SVG + "</div>" +
          '<p class="tl-auth-word">Talendus</p>' +
          '<p class="tl-auth-tagline">' + esc(t.brand) + "</p>" +
          '<ul class="tl-auth-points"><li>' + esc(t.point1) + "</li><li>" + esc(t.point2) + "</li></ul>" +
        "</div></aside>";
    }

    function shell(bodyHtml, kicker) {
      overlay.setAttribute("aria-label", kicker || t.login);
      return '<div class="tl-auth-shell">' +
        '<button type="button" class="tl-auth-close" data-auth-close aria-label="' + esc(t.close) + '"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>' +
        brandPanel() +
        '<div class="tl-auth-panel">' +
          '<a class="tl-auth-logo" href="' + esc(homeHref()) + '"><img src="' + esc(logoUrl()) + '" width="186" height="36" alt="Talendus"></a>' +
          bodyHtml +
        "</div></div>";
    }
    function portalHref(role) {
      if (staffRole(role)) return "/admin/";
      if (role === "EMPLOYER") return siteRoot() + (isEn ? "account-employer.html" : "espace-employeur.html") + "#/dashboard";
      return siteRoot() + (isEn ? "account.html" : "espace.html") + "#/dashboard";
    }
    function parseAuthHash() {
      var raw = (location.hash || "").replace(/^#\/?/, "");
      if (!raw) return null;
      var qIndex = raw.indexOf("?");
      var name = (qIndex >= 0 ? raw.slice(0, qIndex) : raw).split("/")[0];
      var query = {};
      var search = qIndex >= 0 ? raw.slice(qIndex + 1) : "";
      search.split("&").forEach(function (part) {
        var kv = part.split("=");
        if (kv[0]) query[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
      });
      if (["login", "register", "forgot", "reset", "verify"].indexOf(name) === -1) return null;
      return { name: name, query: query };
    }

    var overlay = document.createElement("div");
    overlay.className = "tl-auth-overlay";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", t.login);
    document.body.appendChild(overlay);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) closeOverlay(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !overlay.hidden) closeOverlay();
    });

    var pending = null;
    var providers = { password: true, google: false, linkedin: false };
    api.providers().then(function (json) { providers = json.data || providers; }).catch(function () {});

    function closeOverlay() {
      overlay.hidden = true;
      overlay.innerHTML = "";
      document.body.classList.remove("tl-auth-open");
    }

    function flashBox(sel, msg, ok) {
      var el = overlay.querySelector(sel || ".tl-success");
      if (!el) return;
      el.style.display = "block";
      el.textContent = msg;
      el.className = ok === false ? "tl-success tl-error" : "tl-success";
    }

    function oauthButtons() {
      function oauthBtn(id, icon, label) {
        var on = !!providers[id];
        return '<button type="button" class="tl-btn tl-btn-ghost-dark tl-oauth' + (on ? "" : " is-disabled") + '"' +
          (on ? ' data-oauth="' + id + '"' : " disabled") + ' title="' + esc(on ? label : t.soon) + '">' +
          '<i class="' + icon + '" aria-hidden="true"></i> ' + esc(label) +
          (on ? "" : " — " + esc(t.soon)) + "</button>";
      }
      return '<p class="tl-auth-or"><span>' + esc(t.or) + "</span></p><div class=\"tl-oauth-row\">" +
        oauthBtn("google", "fa-brands fa-google", t.google) +
        oauthBtn("linkedin", "fa-brands fa-linkedin-in", t.linkedin) +
        "</div>";
    }

    function afterAuth(user) {
      closeOverlay();
      paintHeader();
      window.dispatchEvent(new CustomEvent("talendus:auth", { detail: user }));
      if (pending && pending.type === "save" && user && user.role === "CANDIDATE") {
        var jobId = pending.jobId;
        pending = null;
        api.saveJob(jobId).then(function () { paintSaveButtons(); }).catch(function () {});
        return;
      }
      if (pending && pending.type === "portal") {
        pending = null;
        window.location.href = portalHref(user.role);
        return;
      }
      pending = null;
      var onPortal = document.getElementById("tl-account");
      if (!onPortal && (location.pathname.indexOf("espace") !== -1 || location.pathname.indexOf("account") !== -1)) {
        window.location.reload();
      }
    }

    function bindAuthForm(mode, role) {
      overlay.querySelectorAll("[data-auth-goto]").forEach(function (btn) {
        btn.onclick = function () { openAuth(btn.getAttribute("data-auth-goto"), { role: role }); };
      });
      overlay.querySelectorAll("[data-role]").forEach(function (btn) {
        btn.onclick = function () { openAuth("register", { role: btn.getAttribute("data-role") }); };
      });
      var closeBtn = overlay.querySelector("[data-auth-close]");
      if (closeBtn) closeBtn.onclick = closeOverlay;
      var login = overlay.querySelector("#tl-auth-login");
      if (login) login.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(login).entries());
        api.login(d.email, d.password).then(function (json) {
          afterAuth(json.data && json.data.user);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
      });
      var register = overlay.querySelector("#tl-auth-register");
      if (register) register.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(register).entries());
        api.register({
          email: d.email, password: d.password, first_name: d.first_name, last_name: d.last_name,
          role: role || "CANDIDATE", company_name: d.company_name || null, website_url: d.website_url || ""
        }).then(function (json) {
          afterAuth(json.data && json.data.user);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
      });
      var forgot = overlay.querySelector("#tl-auth-forgot");
      if (forgot) forgot.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(forgot).entries());
        api.forgotPassword(d.email).then(function () {
          flashBox(".tl-success", t.forgotOk, true);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
      });
      var reset = overlay.querySelector("#tl-auth-reset");
      if (reset) reset.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(reset).entries());
        api.resetPassword(d.token, d.password).then(function () {
          flashBox(".tl-success", isEn ? "Password updated." : "Mot de passe mis à jour.", true);
          setTimeout(function () { openAuth("login"); }, 800);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
      });
      overlay.querySelectorAll("[data-oauth]").forEach(function (btn) {
        btn.onclick = function () {
          flashBox(".tl-success", t.soon, false);
        };
      });
    }

    function openAuth(mode, opts) {
      opts = opts || {};
      var role = opts.role || "CANDIDATE";
      var token = opts.token || "";
      overlay.hidden = false;
      document.body.classList.add("tl-auth-open");
      var inner = "";
      if (mode === "choose" || (mode === "register" && !opts.role && !opts.skipChoose)) {
        inner = shell(
          '<p class="tl-kicker">' + esc(t.register) + "</p>" +
          "<h2>" + esc(t.choose) + "</h2>" +
          '<p class="tl-auth-lead">' + esc(t.chooseLead) + "</p>" +
          '<div class="tl-auth-roles">' +
            '<button type="button" class="tl-auth-role" data-role="CANDIDATE">' +
              '<span class="tl-auth-role-icon" aria-hidden="true"><i class="fa-solid fa-helmet-safety"></i></span>' +
              '<span class="tl-auth-role-copy"><strong>' + esc(t.seek) + "</strong><span>" + esc(t.seekHint) + "</span></span>" +
            "</button>" +
            '<button type="button" class="tl-auth-role" data-role="EMPLOYER">' +
              '<span class="tl-auth-role-icon" aria-hidden="true"><i class="fa-solid fa-industry"></i></span>' +
              '<span class="tl-auth-role-copy"><strong>' + esc(t.hire) + "</strong><span>" + esc(t.hireHint) + "</span></span>" +
            "</button>" +
          "</div>" +
          '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="login">' + esc(t.haveAccount) + "</button></p>",
          t.choose
        );
        overlay.innerHTML = inner;
        bindAuthForm(mode, role);
        var firstRole = overlay.querySelector(".tl-auth-role");
        if (firstRole) firstRole.focus();
        return;
      }
      if (mode === "forgot") {
        inner = shell(
          '<p class="tl-kicker">' + esc(t.login) + "</p>" +
          "<h2>" + esc(t.forgotTitle) + "</h2>" +
          '<form class="tl-form tl-auth-form" id="tl-auth-forgot">' +
            "<label>" + esc(t.email) + '</label><input name="email" type="email" required autocomplete="email">' +
            '<button class="tl-btn tl-btn-lg" type="submit">' + esc(t.sendReset) + "</button>" +
            '<div class="tl-success"></div></form>' +
          '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="login">' + esc(t.back) + "</button></p>",
          t.forgotTitle
        );
      } else if (mode === "reset") {
        inner = shell(
          '<p class="tl-kicker">' + esc(t.login) + "</p>" +
          "<h2>" + esc(t.resetTitle) + "</h2>" +
          '<form class="tl-form tl-auth-form" id="tl-auth-reset">' +
            '<input type="hidden" name="token" value="' + esc(token) + '">' +
            "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8" autocomplete="new-password">' +
            '<button class="tl-btn tl-btn-lg" type="submit">' + esc(t.resetBtn) + "</button>" +
            '<div class="tl-success"></div></form>',
          t.resetTitle
        );
      } else if (mode === "verify") {
        inner = shell(
          '<p class="tl-kicker">' + esc(t.login) + "</p>" +
          "<h2>" + esc(t.verifyTitle) + '</h2><p class="tl-success" style="display:block"></p>',
          t.verifyTitle
        );
        overlay.innerHTML = inner;
        bindAuthForm(mode, role);
        api.verifyEmail(token).then(function () {
          flashBox(".tl-success", t.verifyOk, true);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
        return;
      } else if (mode === "register") {
        var isHire = role === "EMPLOYER";
        inner = shell(
          '<p class="tl-kicker">' + esc(isHire ? t.hire : t.seek) + "</p>" +
          "<h2>" + esc(t.register) + "</h2>" +
          '<p class="tl-auth-lead">' + esc(isHire ? t.registerEmployerLead : t.registerLead) + "</p>" +
          '<form class="tl-form tl-auth-form" id="tl-auth-register">' +
            '<input class="tl-hp" name="website_url" tabindex="-1" autocomplete="off" aria-hidden="true">' +
            '<div class="tl-row-2">' +
              "<div><label>" + esc(t.first) + '</label><input name="first_name" required autocomplete="given-name"></div>' +
              "<div><label>" + esc(t.last) + '</label><input name="last_name" required autocomplete="family-name"></div>' +
            "</div>" +
            (isHire ? "<label>" + esc(t.company) + '</label><input name="company_name" required autocomplete="organization">' : "") +
            "<label>" + esc(t.email) + '</label><input name="email" type="email" required autocomplete="email" value="' + esc(opts.email || "") + '">' +
            "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8" autocomplete="new-password">' +
            '<button class="tl-btn tl-btn-lg" type="submit">' + esc(t.submitRegister) + "</button>" +
            '<div class="tl-success"></div></form>' + oauthButtons() +
          '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="login">' + esc(t.haveAccount) + "</button></p>",
          t.register
        );
      } else {
        inner = shell(
          '<p class="tl-kicker">Talendus</p>' +
          "<h2>" + esc(t.login) + "</h2>" +
          '<p class="tl-auth-lead">' + esc(t.loginLead) + "</p>" +
          '<form class="tl-form tl-auth-form" id="tl-auth-login">' +
            "<label>" + esc(t.email) + '</label><input name="email" type="email" required autocomplete="username">' +
            "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8" autocomplete="current-password">' +
            '<button class="tl-btn tl-btn-lg" type="submit">' + esc(t.submitLogin) + "</button>" +
            '<p class="tl-auth-forgot"><button type="button" class="tl-text-btn" data-auth-goto="forgot">' + esc(t.forgot) + "</button></p>" +
            '<div class="tl-success"></div></form>' + oauthButtons() +
          '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="choose">' + esc(t.noAccount) + "</button></p>",
          t.login
        );
      }
      overlay.innerHTML = inner;
      bindAuthForm(mode, role);
      var first = overlay.querySelector("input:not(.tl-hp), .tl-auth-role, button.tl-btn");
      if (first && first.focus) first.focus();
    }

    window.TalendusAuth = {
      open: function (mode, opts) { openAuth(mode || "login", opts || {}); },
      requireCandidate: function (intent) {
        var user = api.currentUser();
        if (user && user.role === "CANDIDATE") return Promise.resolve(user);
        pending = intent || { type: "portal" };
        openAuth(user ? "login" : "choose", { role: "CANDIDATE", skipChoose: false });
        return Promise.reject(new Error("auth"));
      },
      requireEmployer: function (intent) {
        var user = api.currentUser();
        if (user && user.role === "EMPLOYER") return Promise.resolve(user);
        pending = intent || { type: "portal" };
        openAuth("register", { role: "EMPLOYER" });
        return Promise.reject(new Error("auth"));
      }
    };

    function paintHeader() {
      var user = api.currentUser();
      document.querySelectorAll("[data-account-link]").forEach(function (el) {
        if (user && user.first_name) {
          el.textContent = user.first_name;
          el.setAttribute("href", portalHref(user.role));
          el.removeAttribute("data-auth-open");
        } else {
          el.textContent = t.guestCta;
          el.setAttribute("href", "#");
          el.setAttribute("data-auth-open", "login");
        }
      });
      document.querySelectorAll("[data-auth-logout]").forEach(function (el) {
        el.hidden = !user;
      });
    }

    function paintSaveButtons() {
      var user = api.currentUser();
      document.querySelectorAll("[data-save-job]").forEach(function (btn) {
        var id = btn.getAttribute("data-save-job");
        if (!id) return;
        if (!user || user.role !== "CANDIDATE") {
          btn.textContent = t.saveJob;
          btn.classList.remove("is-saved");
          return;
        }
        api.request("/jobs/" + encodeURIComponent(id)).then(function (json) {
          var saved = json.data && json.data.saved;
          btn.textContent = saved ? t.savedJob : t.saveJob;
          btn.classList.toggle("is-saved", !!saved);
        }).catch(function () {});
      });
    }

    document.addEventListener("click", function (e) {
      var open = e.target.closest("[data-auth-open]");
      if (open) {
        e.preventDefault();
        var mode = open.getAttribute("data-auth-open") || "login";
        if (mode === "register") openAuth("choose");
        else openAuth(mode);
        return;
      }
      var save = e.target.closest("[data-save-job]");
      if (save) {
        e.preventDefault();
        var jobId = save.getAttribute("data-save-job");
        var user = api.currentUser();
        if (!user || user.role !== "CANDIDATE") {
          pending = { type: "save", jobId: jobId };
          openAuth("choose");
          return;
        }
        var method = save.classList.contains("is-saved") ? "DELETE" : "POST";
        api.request("/jobs/" + jobId + "/save", { method: method }).then(function () { paintSaveButtons(); }).catch(function () {});
      }
    });

    var hash = parseAuthHash();
    if (hash) {
      openAuth(hash.name, { token: hash.query.token || "", role: hash.query.role, email: hash.query.email });
    }

    paintHeader();

    var pageFile = (location.pathname.split("/").pop() || "").toLowerCase();
    var jobSlug = "";
    if (pageFile.indexOf("emploi-") === 0) jobSlug = pageFile.slice("emploi-".length).replace(/\.html$/, "");
    if (pageFile.indexOf("job-") === 0) jobSlug = pageFile.slice("job-".length).replace(/\.html$/, "");
    if (jobSlug) {
      api.request("/jobs/" + encodeURIComponent(jobSlug)).then(function (payload) {
        var job = payload && payload.data;
        if (!job) return;
        var host = document.querySelector("#postuler") || document.querySelector(".tl-page-hero .container") || document.querySelector(".tl-section .container");
        if (!host || host.querySelector("[data-save-job]")) return;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tl-btn tl-btn-ghost tl-save-job";
        btn.setAttribute("data-save-job", job.id);
        btn.textContent = t.saveJob;
        host.appendChild(btn);
        if (job.saved) {
          btn.textContent = t.savedJob;
          btn.classList.add("is-saved");
        }
      }).catch(function () {});
    }

    document.querySelectorAll(".tl-form[data-form=apply], #postuler .tl-form").forEach(function (form) {
      form.addEventListener("talendus:applied", function () {
        var user = api.currentUser();
        if (user) return;
        var box = form.querySelector(".tl-success");
        if (!box) return;
        var extra = document.createElement("p");
        extra.className = "tl-auth-followup";
        extra.innerHTML = '<button type="button" class="tl-text-btn" data-auth-open="register">' + esc(t.applyTrack) + "</button>";
        box.appendChild(extra);
      });
    });
  });
})();
