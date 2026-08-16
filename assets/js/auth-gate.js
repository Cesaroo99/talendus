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
      choose: "How can Talendus help you?", seek: "I'm looking for a job", hire: "I hire for a company",
      company: "Company name", close: "Close", or: "or", google: "Continue with Google",
      linkedin: "Continue with LinkedIn", soon: "Coming soon",
      resetTitle: "Choose a new password", resetBtn: "Update password",
      verifyTitle: "Confirming your email…", verifyOk: "Email verified. You can sign in.",
      forgotTitle: "Reset your password", forgotOk: "If an account exists, we sent an email.",
      guestCta: "Sign in", dashboard: "Dashboard", logout: "Sign out",
      saveJob: "Save job", savedJob: "Saved", applyTrack: "Create an account to track this application",
      needAccount: "Create an account to continue",
      err: "Something went wrong."
    } : {
      login: "Connexion", register: "Créer un compte", email: "Courriel", password: "Mot de passe",
      first: "Prénom", last: "Nom", submitLogin: "Me connecter", submitRegister: "Créer mon compte",
      forgot: "Mot de passe oublié ?", sendReset: "Envoyer le lien", back: "Retour",
      choose: "Que souhaitez-vous faire ?", seek: "Je cherche un emploi", hire: "Je recrute pour une entreprise",
      company: "Nom de l'entreprise", close: "Fermer", or: "ou", google: "Continuer avec Google",
      linkedin: "Continuer avec LinkedIn", soon: "Bientôt disponible",
      resetTitle: "Choisissez un nouveau mot de passe", resetBtn: "Mettre à jour",
      verifyTitle: "Vérification du courriel…", verifyOk: "Courriel vérifié. Vous pouvez vous connecter.",
      forgotTitle: "Réinitialiser le mot de passe", forgotOk: "Si un compte existe, un courriel a été envoyé.",
      guestCta: "Connexion", dashboard: "Tableau de bord", logout: "Déconnexion",
      saveJob: "Sauvegarder", savedJob: "Sauvegardée", applyTrack: "Créer un compte pour suivre cette candidature",
      needAccount: "Créez un compte pour continuer",
      err: "Une erreur s’est produite."
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    function staffRole(role) {
      return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
    }
    function siteRoot() { return isEn ? "/en/" : "/"; }
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

    function oauthButtons(role) {
      var g = providers.google
        ? '<button type="button" class="tl-btn tl-btn-ghost tl-oauth" data-oauth="google">' + esc(t.google) + "</button>"
        : '<button type="button" class="tl-btn tl-btn-ghost tl-oauth is-disabled" disabled title="' + esc(t.soon) + '">' + esc(t.google) + " — " + esc(t.soon) + "</button>";
      var l = providers.linkedin
        ? '<button type="button" class="tl-btn tl-btn-ghost tl-oauth" data-oauth="linkedin">' + esc(t.linkedin) + "</button>"
        : '<button type="button" class="tl-btn tl-btn-ghost tl-oauth is-disabled" disabled title="' + esc(t.soon) + '">' + esc(t.linkedin) + " — " + esc(t.soon) + "</button>";
      return '<p class="tl-auth-or">' + esc(t.or) + "</p><div class=\"tl-oauth-row\">" + g + l + "</div>";
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
      overlay.addEventListener("click", function (e) { if (e.target === overlay) closeOverlay(); });
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
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close aria-label="' + esc(t.close) + '">×</button>' +
          "<h2>" + esc(t.choose) + "</h2>" +
          '<div class="tl-auth-roles"><button type="button" class="tl-btn" data-role="CANDIDATE">' + esc(t.seek) +
          '</button><button type="button" class="tl-btn tl-btn-electric" data-role="EMPLOYER">' + esc(t.hire) +
          "</button></div><p><button type=\"button\" class=\"tl-text-btn\" data-auth-goto=\"login\">" + esc(t.login) + "</button></p></div>";
        overlay.innerHTML = inner;
        bindAuthForm(mode, role);
        return;
      }
      if (mode === "forgot") {
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close>×</button><h2>' +
          esc(t.forgotTitle) + '</h2><form class="tl-form" id="tl-auth-forgot"><label>' + esc(t.email) +
          '</label><input name="email" type="email" required><button class="tl-btn" type="submit">' + esc(t.sendReset) +
          '</button><div class="tl-success"></div></form><p><button type="button" class="tl-text-btn" data-auth-goto="login">' +
          esc(t.back) + "</button></p></div>";
      } else if (mode === "reset") {
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close>×</button><h2>' +
          esc(t.resetTitle) + '</h2><form class="tl-form" id="tl-auth-reset"><input type="hidden" name="token" value="' +
          esc(token) + '"><label>' + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
          '<button class="tl-btn" type="submit">' + esc(t.resetBtn) + '</button><div class="tl-success"></div></form></div>';
      } else if (mode === "verify") {
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close>×</button><h2>' +
          esc(t.verifyTitle) + '</h2><p class="tl-success" style="display:block"></p></div>';
        overlay.innerHTML = inner;
        bindAuthForm(mode, role);
        api.verifyEmail(token).then(function () {
          flashBox(".tl-success", t.verifyOk, true);
        }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
        return;
      } else if (mode === "register") {
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close>×</button><h2>' +
          esc(role === "EMPLOYER" ? t.hire : t.seek) + '</h2><form class="tl-form" id="tl-auth-register">' +
          '<input class="tl-hp" name="website_url" tabindex="-1" autocomplete="off" aria-hidden="true">' +
          "<label>" + esc(t.first) + '</label><input name="first_name" required><label>' + esc(t.last) +
          '</label><input name="last_name" required>' +
          (role === "EMPLOYER" ? "<label>" + esc(t.company) + '</label><input name="company_name" required>' : "") +
          "<label>" + esc(t.email) + '</label><input name="email" type="email" required value="' + esc(opts.email || "") +
          '"><label>' + esc(t.password) + '</label><input name="password" type="password" required minlength="8">' +
          '<button class="tl-btn tl-btn-electric" type="submit">' + esc(t.submitRegister) +
          '</button><div class="tl-success"></div></form>' + oauthButtons(role) +
          '<p><button type="button" class="tl-text-btn" data-auth-goto="login">' + esc(t.login) + "</button></p></div>";
      } else {
        inner = '<div class="tl-auth-card"><button type="button" class="tl-auth-close" data-auth-close>×</button><h2>' +
          esc(t.login) + '</h2><form class="tl-form" id="tl-auth-login"><label>' + esc(t.email) +
          '</label><input name="email" type="email" required><label>' + esc(t.password) +
          '</label><input name="password" type="password" required minlength="8"><button class="tl-btn" type="submit">' +
          esc(t.submitLogin) + '</button><p><button type="button" class="tl-text-btn" data-auth-goto="forgot">' +
          esc(t.forgot) + '</button></p><div class="tl-success"></div></form>' + oauthButtons("CANDIDATE") +
          '<p><button type="button" class="tl-text-btn" data-auth-goto="choose">' + esc(t.register) + "</button></p></div>";
      }
      overlay.innerHTML = inner;
      bindAuthForm(mode, role);
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
