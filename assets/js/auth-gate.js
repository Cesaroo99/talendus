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
      seek: "Candidate", hire: "Employer",
      company: "Company name", close: "Close", or: "or", google: "Continue with Google",
      linkedin: "Continue with LinkedIn",
      resetTitle: "Choose a new password", resetBtn: "Update password",
      verifyTitle: "Confirming your email…", verifyOk: "Email verified. You can sign in.",
      forgotTitle: "Reset your password", forgotOk: "If an account exists, we sent an email.",
      guestCta: "Sign in", dashboard: "Dashboard", logout: "Sign out",
      workspace: "My workspace", settings: "Settings", notifs: "Notifications",
      accountMenu: "Account menu",
      saveJob: "Save job", savedJob: "Saved", saveNeedCandidate: "Use a candidate account to save a job.",
      applyNeedCandidate: "Use a candidate account to apply.",
      jobClosed: "Applications are paused for this role.",
      saveFailed: "The job could not be saved.",
      applyTrack: "Create an account to track this application",
      needAccount: "Create an account to continue",
      err: "Something went wrong.",
      loginLead: "Access your Talendus workspace.",
      registerLead: "Free for talent. Takes a few minutes.",
      registerEmployerLead: "Create your company space and hand us a hiring need.",
      haveAccount: "Already have an account? Sign in",
      noAccount: "No account yet? Create one",
      googleFail: "Google Sign-In could not load. Use email instead.",
      signedIn: "You are already signed in.",
      goWorkspace: "Open my workspace"
    } : {
      login: "Connexion", register: "Créer un compte", email: "Courriel", password: "Mot de passe",
      first: "Prénom", last: "Nom", submitLogin: "Me connecter", submitRegister: "Créer mon compte",
      forgot: "Mot de passe oublié ?", sendReset: "Envoyer le lien", back: "Retour",
      seek: "Candidat", hire: "Entreprise",
      company: "Nom de l'entreprise", close: "Fermer", or: "ou", google: "Continuer avec Google",
      linkedin: "Continuer avec LinkedIn",
      resetTitle: "Choisissez un nouveau mot de passe", resetBtn: "Mettre à jour",
      verifyTitle: "Vérification du courriel…", verifyOk: "Courriel vérifié. Vous pouvez vous connecter.",
      forgotTitle: "Réinitialiser le mot de passe", forgotOk: "Si un compte existe, un courriel a été envoyé.",
      guestCta: "Connexion", dashboard: "Tableau de bord", logout: "Déconnexion",
      workspace: "Mon espace", settings: "Paramètres", notifs: "Notifications",
      accountMenu: "Menu du compte",
      saveJob: "Sauvegarder", savedJob: "Sauvegardée", saveNeedCandidate: "Utilisez un compte candidat pour sauvegarder une offre.",
      applyNeedCandidate: "Utilisez un compte candidat pour postuler.",
      jobClosed: "Les candidatures sont suspendues pour cette offre.",
      saveFailed: "L’offre n’a pas pu être sauvegardée.",
      applyTrack: "Créer un compte pour suivre cette candidature",
      needAccount: "Créez un compte pour continuer",
      err: "Une erreur s’est produite.",
      loginLead: "Accédez à votre espace Talendus.",
      registerLead: "Gratuit pour les talents. Quelques minutes suffisent.",
      registerEmployerLead: "Créez l'espace de votre entreprise et confiez-nous un besoin.",
      haveAccount: "Déjà un compte ? Connexion",
      noAccount: "Pas encore de compte ? Créer un compte",
      googleFail: "La connexion Google n'a pas pu s'afficher. Utilisez le courriel.",
      signedIn: "Vous êtes déjà connecté.",
      goWorkspace: "Ouvrir mon espace"
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    function wireAuthLabels() {
      if (!overlay) return;
      overlay.querySelectorAll("label").forEach(function (label, i) {
        if (label.htmlFor || label.querySelector("input, select, textarea")) return;
        var next = label.nextElementSibling;
        if (!next || !/^(INPUT|SELECT|TEXTAREA)$/.test(next.tagName)) return;
        if (!next.id) next.id = "tl-auth-field-" + (next.getAttribute("name") || i);
        label.setAttribute("for", next.id);
      });
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
    function homeHref() { return siteRoot() + "index.html"; }
    function isNativeApp() {
      var ua = navigator.userAgent || "";
      if (/TalendusApp/i.test(ua)) return true;
      if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return true;
      if (window.matchMedia && window.matchMedia("(display-mode: fullscreen)").matches) return true;
      if (window.navigator && window.navigator.standalone) return true;
      return /\/m\.html$/.test(location.pathname || "");
    }
    function portalHref(role, hash) {
      if (staffRole(role)) return "/admin/";
      var dest = role === "EMPLOYER"
        ? siteRoot() + (isEn ? "account-employer.html" : "espace-employeur.html")
        : siteRoot() + (isEn ? "account.html" : "espace.html");
      var destHash = hash || "#/dashboard";
      if (isNativeApp()) destHash = String(destHash).replace("#/home", "#/dashboard");
      return dest + destHash;
    }
    function roleLabel(role) {
      if (role === "EMPLOYER") return t.hire;
      if (staffRole(role)) return isEn ? "Team" : "Équipe";
      return t.seek;
    }
    function initials(user) {
      var a = String((user && user.first_name) || "").trim().charAt(0);
      var b = String((user && user.last_name) || "").trim().charAt(0);
      var fallback = String((user && user.email) || "?").charAt(0);
      return ((a + b) || fallback).toUpperCase();
    }
    function displayName(user) {
      return (((user && user.first_name) || "") + " " + ((user && user.last_name) || "")).trim() || (user && user.email) || "";
    }
    function avatarHtml(user, cls) {
      var url = window.__tlAvatarUrl;
      if (url) {
        return '<span class="tl-avatar ' + (cls || "") + '"><img src="' + esc(url) + '" alt=""></span>';
      }
      return '<span class="tl-avatar ' + (cls || "") + '" aria-hidden="true">' + esc(initials(user)) + "</span>";
    }
    function parseAuthHash() {
      var raw = (location.hash || "").replace(/^#\/?/, "");
      if (!raw) return null;
      var qIndex = raw.indexOf("?");
      var path = qIndex >= 0 ? raw.slice(0, qIndex) : raw;
      var parts = path.split("/").filter(Boolean);
      var name = parts[0] || "";
      var query = {};
      var search = qIndex >= 0 ? raw.slice(qIndex + 1) : "";
      search.split("&").forEach(function (part) {
        var kv = part.split("=");
        if (kv[0]) query[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
      });
      if (!query.token && parts.length > 1) {
        try { query.token = decodeURIComponent(parts.slice(1).join("/")); } catch (e) { query.token = parts.slice(1).join("/"); }
      }
      if (["login", "register", "forgot", "reset", "verify"].indexOf(name) === -1) return null;
      return { name: name, query: query };
    }
    function samePath(href) {
      try {
        var dest = new URL(href, location.origin);
        var here = location.pathname.replace(/\/$/, "") || "/";
        var there = dest.pathname.replace(/\/$/, "") || "/";
        return here === there;
      } catch (e) { return false; }
    }
    function goToWorkspace(user) {
      var dest = portalHref((user || {}).role);
      closeOverlay();
      if (samePath(dest) && document.getElementById("tl-account")) {
        if ((location.hash || "") !== "#/dashboard") location.hash = "#/dashboard";
        window.dispatchEvent(new CustomEvent("talendus:auth", { detail: user }));
        return;
      }
      location.href = dest;
    }
    function defaultRole() {
      var root = document.getElementById("tl-account");
      if (root && root.getAttribute("data-space") === "employer") return "EMPLOYER";
      return "CANDIDATE";
    }
    function isLiveUser() {
      return !!api.currentUser();
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
    var authRole = "";
    var providers = { password: true, google: false, linkedin: false, google_client_id: "" };
    var providersReady = api.providers().then(function (json) {
      providers = Object.assign(providers, json.data || {});
      return providers;
    }).catch(function () { return providers; });
    var googleSdk = null;

    function closeOverlay() {
      overlay.hidden = true;
      overlay.innerHTML = "";
      document.body.classList.remove("tl-auth-open");
      authRole = "";
      if (pending && pending.type === "save") pending = null;
    }

    function flashBox(sel, msg, ok) {
      var el = overlay.querySelector(sel || ".tl-success");
      if (!el) return;
      el.style.display = "block";
      el.textContent = msg;
      el.className = ok === false ? "tl-success tl-error" : "tl-success";
    }

    function hintSave(msg) {
      var btn = document.querySelector("[data-save-job]");
      var host = (btn && btn.parentNode) || document.querySelector(".tl-job-save-row") || document.querySelector(".tl-job-apply-card");
      if (!host) return;
      var hint = host.querySelector(".tl-save-hint") || document.querySelector(".tl-save-hint");
      if (!hint) {
        hint = document.createElement("p");
        hint.className = "tl-save-hint";
        host.appendChild(hint);
      }
      hint.hidden = false;
      hint.textContent = msg || t.saveFailed;
    }

    function shell(bodyHtml, kicker) {
      overlay.setAttribute("aria-label", kicker || t.login);
      return '<div class="tl-auth-shell">' +
        '<button type="button" class="tl-auth-close" data-auth-close aria-label="' + esc(t.close) + '"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>' +
        '<div class="tl-auth-panel">' +
          '<a class="tl-auth-logo" href="' + esc(homeHref()) + '"><img src="' + esc(logoUrl()) + '" width="186" height="36" alt="Talendus"></a>' +
          bodyHtml +
        "</div></div>";
    }

    function oauthBlock() {
      var bits = [];
      if (providers.google && providers.google_client_id) {
        bits.push(
          '<div class="tl-google-slot" id="auth-google-slot">' +
            '<button type="button" class="tl-oauth-btn tl-oauth-google" disabled>' +
              '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/><path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/><path fill="#FBBC05" d="M3.964 10.707A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z"/><path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z"/></svg>' +
              "<span>" + esc(t.google) + "</span></button></div>"
        );
      }
      if (!bits.length) return "";
      return '<p class="tl-auth-or"><span>' + esc(t.or) + "</span></p><div class=\"tl-oauth-row\">" + bits.join("") + "</div>";
    }

    function loadGoogleSdk() {
      if (googleSdk) return googleSdk;
      googleSdk = new Promise(function (resolve, reject) {
        if (window.google && window.google.accounts && window.google.accounts.id) {
          resolve();
          return;
        }
        var s = document.createElement("script");
        s.src = "https://accounts.google.com/gsi/client";
        s.async = true;
        s.defer = true;
        s.onload = function () { resolve(); };
        s.onerror = function () { googleSdk = null; reject(new Error("google")); };
        document.head.appendChild(s);
      });
      return googleSdk;
    }

    function currentAuthRole() {
      var active = overlay.querySelector("[data-auth-role].is-active");
      return (active && active.getAttribute("data-auth-role")) || authRole || "CANDIDATE";
    }

    function mountGoogleButton() {
      var slot = overlay.querySelector("#auth-google-slot");
      if (!slot || !providers.google || !providers.google_client_id) return;
      loadGoogleSdk().then(function () {
        if (!overlay.querySelector("#auth-google-slot")) return;
        window.google.accounts.id.initialize({
          client_id: providers.google_client_id,
          callback: function (response) {
            var company = overlay.querySelector("[name=company_name]");
            api.oauthGoogle({
              id_token: response.credential,
              role: currentAuthRole(),
              company_name: company ? company.value : null
            }).then(function (json) {
              afterAuth(json.data && json.data.user);
            }).catch(function (err) {
              flashBox(".tl-success", (err && err.message) || t.err, false);
            });
          },
          ux_mode: "popup",
          auto_select: false,
          cancel_on_tap_outside: true
        });
        slot.innerHTML = "";
        var width = Math.max(240, Math.min(400, Math.floor(slot.getBoundingClientRect().width || 320)));
        window.google.accounts.id.renderButton(slot, {
          type: "standard",
          theme: "outline",
          size: "large",
          text: "continue_with",
          shape: "rectangular",
          logo_alignment: "left",
          width: width,
          locale: isEn ? "en" : "fr"
        });
      }).catch(function () {
        if (slot) slot.innerHTML = '<p class="tl-oauth-fallback">' + esc(t.googleFail) + "</p>";
      });
    }

    function afterAuth(user) {
      paintSession();
      paintSaveButtons();
      window.dispatchEvent(new CustomEvent("talendus:auth", { detail: user }));
      if (pending && pending.type === "save") {
        if (user && user.role === "CANDIDATE") {
          var jobId = pending.jobId;
          pending = null;
          closeOverlay();
          api.saveJob(jobId).then(function () { paintSaveButtons(); }).catch(function (err) {
            hintSave((err && err.message) || t.saveFailed);
          });
          return;
        }
        flashBox(".tl-success", t.saveNeedCandidate, false);
        return;
      }
      closeOverlay();
      if (pending && pending.type === "portal") {
        pending = null;
        goToWorkspace(user);
        return;
      }
      pending = null;
    }

    function bindAuthForm(mode, role) {
      overlay.querySelectorAll("[data-auth-goto]").forEach(function (btn) {
        btn.onclick = function () { openAuth(btn.getAttribute("data-auth-goto"), { role: role }); };
      });
      overlay.querySelectorAll("[data-auth-role]").forEach(function (btn) {
        btn.onclick = function () {
          openAuth("register", { role: btn.getAttribute("data-auth-role") });
        };
      });
      var closeBtn = overlay.querySelector("[data-auth-close]");
      if (closeBtn) closeBtn.onclick = closeOverlay;
      function busy(form, on) {
        var submit = form && form.querySelector("[type=submit]");
        if (submit) submit.disabled = !!on;
      }
      var login = overlay.querySelector("#tl-auth-login");
      if (login) login.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(login).entries());
        busy(login, true);
        api.login(d.email, d.password).then(function (json) {
          afterAuth(json.data && json.data.user);
        }).catch(function (err) {
          busy(login, false);
          flashBox(".tl-success", (err && err.message) || t.err, false);
        });
      });
      var register = overlay.querySelector("#tl-auth-register");
      if (register) register.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(register).entries());
        busy(register, true);
        api.register({
          email: d.email, password: d.password, first_name: d.first_name, last_name: d.last_name,
          role: role || "CANDIDATE", company_name: d.company_name || null, website_url: d.website_url || ""
        }).then(function (json) {
          afterAuth(json.data && json.data.user);
        }).catch(function (err) {
          busy(register, false);
          flashBox(".tl-success", (err && err.message) || t.err, false);
        });
      });
      var forgot = overlay.querySelector("#tl-auth-forgot");
      if (forgot) forgot.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(forgot).entries());
        busy(forgot, true);
        api.forgotPassword(d.email).then(function () {
          busy(forgot, false);
          flashBox(".tl-success", t.forgotOk, true);
        }).catch(function (err) {
          busy(forgot, false);
          flashBox(".tl-success", (err && err.message) || t.err, false);
        });
      });
      var reset = overlay.querySelector("#tl-auth-reset");
      if (reset) reset.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(reset).entries());
        busy(reset, true);
        api.resetPassword(d.token, d.password).then(function () {
          flashBox(".tl-success", isEn ? "Password updated." : "Mot de passe mis à jour.", true);
          setTimeout(function () { openAuth("login"); }, 800);
        }).catch(function (err) {
          busy(reset, false);
          flashBox(".tl-success", (err && err.message) || t.err, false);
        });
      });
      mountGoogleButton();
    }

    function openAuth(mode, opts) {
      opts = opts || {};
      var role = (opts.role || authRole || defaultRole()).toUpperCase();
      if (pending && pending.type === "save") role = "CANDIDATE";
      if (role !== "EMPLOYER") role = "CANDIDATE";
      authRole = role;
      var token = opts.token || "";
      var user = api.currentUser();
      var savingJob = pending && pending.type === "save";
      if (user && !savingJob && ["login", "register", "choose"].indexOf(mode) !== -1) {
        goToWorkspace(user);
        return;
      }
      if (user && savingJob && user.role === "CANDIDATE") {
        var jobId = pending.jobId;
        pending = null;
        api.saveJob(jobId).then(function () { paintSaveButtons(); }).catch(function (err) {
          hintSave((err && err.message) || t.saveFailed);
        });
        return;
      }
      overlay.hidden = false;
      document.body.classList.add("tl-auth-open");
      function draw() {
        var inner = "";
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
          wireAuthLabels();
          bindAuthForm(mode, role);
          api.verifyEmail(token).then(function () {
            flashBox(".tl-success", t.verifyOk, true);
          }).catch(function (err) { flashBox(".tl-success", (err && err.message) || t.err, false); });
          return;
        } else if (mode === "register" || mode === "choose") {
          var isHire = role === "EMPLOYER";
          inner = shell(
            "<h2>" + esc(t.register) + "</h2>" +
            '<p class="tl-auth-lead">' + esc(savingJob ? t.saveNeedCandidate : (isHire ? t.registerEmployerLead : t.registerLead)) + "</p>" +
            (savingJob ? "" : ('<div class="tl-auth-tabs" role="tablist">' +
              '<button type="button" role="tab" class="' + (isHire ? "" : "is-active") + '" data-auth-role="CANDIDATE" aria-selected="' + (isHire ? "false" : "true") + '">' + esc(t.seek) + "</button>" +
              '<button type="button" role="tab" class="' + (isHire ? "is-active" : "") + '" data-auth-role="EMPLOYER" aria-selected="' + (isHire ? "true" : "false") + '">' + esc(t.hire) + "</button>" +
            "</div>")) +
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
              '<div class="tl-success"></div></form>' + oauthBlock() +
            '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="login">' + esc(t.haveAccount) + "</button></p>",
            t.register
          );
        } else {
          inner = shell(
            "<h2>" + esc(t.login) + "</h2>" +
            '<p class="tl-auth-lead">' + esc(savingJob ? t.saveNeedCandidate : t.loginLead) + "</p>" +
            '<form class="tl-form tl-auth-form" id="tl-auth-login">' +
              "<label>" + esc(t.email) + '</label><input name="email" type="email" required autocomplete="username">' +
              "<label>" + esc(t.password) + '</label><input name="password" type="password" required minlength="8" autocomplete="current-password">' +
              '<p class="tl-auth-forgot"><button type="button" class="tl-text-btn" data-auth-goto="forgot">' + esc(t.forgot) + "</button></p>" +
              '<button class="tl-btn tl-btn-lg" type="submit">' + esc(t.submitLogin) + "</button>" +
              '<div class="tl-success"></div></form>' + oauthBlock() +
            '<p class="tl-auth-switch"><button type="button" class="tl-text-btn" data-auth-goto="register">' + esc(t.noAccount) + "</button></p>",
            t.login
          );
        }
        overlay.innerHTML = inner;
        wireAuthLabels();
        bindAuthForm(mode, role);
        var first = overlay.querySelector("input:not(.tl-hp), button.tl-btn");
        if (first && first.focus) first.focus();
      }
      if (mode === "login" || mode === "register" || mode === "choose") {
        providersReady.then(draw);
      } else {
        draw();
      }
    }

    window.TalendusAuth = {
      open: function (mode, opts) { openAuth(mode || "login", opts || {}); },
      paint: function () { paintSession(); },
      requireCandidate: function (intent) {
        var user = api.currentUser();
        if (user && user.role === "CANDIDATE") return Promise.resolve(user);
        pending = intent || { type: "portal" };
        openAuth(user ? "login" : "register", { role: "CANDIDATE" });
        return Promise.reject(new Error("auth"));
      },
      requireEmployer: function (intent) {
        var user = api.currentUser();
        if (user && user.role === "EMPLOYER") return Promise.resolve(user);
        pending = intent || { type: "portal" };
        openAuth("login", { role: "EMPLOYER" });
        return Promise.reject(new Error("auth"));
      }
    };

    function isEmployerPage() {
      var file = (location.pathname.split("/").pop() || "").toLowerCase();
      var path = (location.pathname || "").toLowerCase();
      return file === "espace-employeur.html" || file === "account-employer.html" || path.indexOf("/employer") !== -1;
    }
    function isHirePersona() {
      return (document.body.getAttribute("data-persona") || "") === "entreprise";
    }
    function guestSpaceHref() {
      if (isEmployerPage() || isHirePersona()) {
        return siteRoot() + (isEn ? "account-employer.html" : "espace-employeur.html");
      }
      return siteRoot() + (isEn ? "account.html" : "espace.html");
    }
    function guestRoleAttr() {
      return (isEmployerPage() || isHirePersona()) ? ' data-auth-role="EMPLOYER"' : "";
    }

    function guestMarkup(kind) {
      var space = guestSpaceHref();
      var roleAttr = guestRoleAttr();
      if (kind === "mobile") {
        return '<a href="' + esc(space) + '" class="tl-session-icon-btn" data-auth-open="login"' + roleAttr + ' aria-label="' + esc(t.login) + '">' +
          '<i class="fa-regular fa-user" aria-hidden="true"></i></a>';
      }
      if (kind === "offcanvas") {
        return '<a href="' + esc(space) + '" class="tl-btn tl-btn-ghost" data-auth-open="login"' + roleAttr + '>' + esc(t.login) + "</a>" +
          '<a href="' + esc(space) + '" class="tl-btn" data-auth-open="register"' + roleAttr + '>' + esc(t.register) + "</a>";
      }
      return '<a href="' + esc(space) + '" class="tl-session-login" data-auth-open="login"' + roleAttr + '>' +
        '<i class="fa-regular fa-user" aria-hidden="true"></i><span>' + esc(t.login) + "</span></a>" +
        '<a href="' + esc(space) + '" class="tl-btn tl-session-cta" data-auth-open="register"' + roleAttr + '>' + esc(t.register) + "</a>";
    }

    function authedMarkup(user, unread, kind) {
      var space = portalHref(user.role);
      var badge = unread ? '<span class="tl-session-badge">' + (unread > 9 ? "9+" : unread) + "</span>" : "";
      var menu =
        '<div class="tl-session-menu" role="menu">' +
          '<div class="tl-session-menu-id">' + avatarHtml(user, "is-lg") +
            "<div><strong>" + esc(displayName(user)) + "</strong><span>" + esc(roleLabel(user.role)) + "</span></div></div>" +
          '<a role="menuitem" href="' + esc(space) + '"><i class="fa-solid fa-table-columns" aria-hidden="true"></i>' + esc(t.workspace) + "</a>" +
          '<a role="menuitem" href="' + esc(portalHref(user.role, "#/settings")) + '"><i class="fa-solid fa-gear" aria-hidden="true"></i>' + esc(t.settings) + "</a>" +
          '<button type="button" role="menuitem" data-auth-logout><i class="fa-solid fa-arrow-right-from-bracket" aria-hidden="true"></i>' + esc(t.logout) + "</button>" +
        "</div>";
      if (kind === "offcanvas") {
        return '<div class="tl-session-offcanvas-user">' + avatarHtml(user, "is-lg") +
          "<div><strong>" + esc(displayName(user)) + "</strong><span>" + esc(roleLabel(user.role)) + "</span></div></div>" +
          '<a class="tl-btn" href="' + esc(space) + '">' + esc(t.workspace) + "</a>" +
          '<a class="tl-btn tl-btn-ghost" href="' + esc(portalHref(user.role, "#/settings")) + '">' + esc(t.settings) + "</a>" +
          '<button type="button" class="tl-btn tl-btn-ghost" data-auth-logout>' + esc(t.logout) + "</button>";
      }
      var trigger = '<button type="button" class="tl-session-user" data-session-menu aria-expanded="false" aria-haspopup="true" aria-label="' + esc(t.accountMenu) + '">' +
        avatarHtml(user) + '<span class="tl-session-name">' + esc(user.first_name || t.workspace) + '</span><i class="fa-solid fa-angle-down tl-session-caret" aria-hidden="true"></i></button>';
      if (kind === "mobile") {
        return trigger + menu;
      }
      var bell = '<a class="tl-session-bell" href="' + esc(portalHref(user.role, "#/notifs")) + '" aria-label="' + esc(t.notifs) + '">' +
        '<i class="fa-regular fa-bell" aria-hidden="true"></i>' + badge + "</a>";
      return '<div class="tl-session-cluster">' + bell + trigger + "</div>" + menu;
    }

    function fillSessions(user, unread) {
      document.body.classList.toggle("tl-is-authed", !!user);
      document.querySelectorAll("[data-session]").forEach(function (slot) {
        var kind = slot.getAttribute("data-session") || "desktop";
        slot.classList.remove("is-open");
        slot.innerHTML = user ? authedMarkup(user, unread, kind) : guestMarkup(kind);
      });
    }

    function loadAvatarThen(user, done) {
      if (!user || !user.avatar_path) { done(); return; }
      if (window.__tlAvatarUrl) { done(); return; }
      var token = "";
      try { token = localStorage.getItem("talendus_access_token") || ""; } catch (e) {}
      fetch("/api/users/me/avatar", { headers: token ? { Authorization: "Bearer " + token } : {} })
        .then(function (res) { return res.ok ? res.blob() : Promise.reject(); })
        .then(function (blob) {
          if (blob && blob.type && blob.type.indexOf("image") === 0) {
            window.__tlAvatarUrl = URL.createObjectURL(blob);
          }
        })
        .catch(function () {})
        .then(done);
    }

    function paintSession() {
      var user = api.currentUser();
      if (!user) {
        window.__tlAvatarUrl = "";
        fillSessions(null, 0);
        paintSaveButtons();
        return;
      }
      fillSessions(user, window.__tlUnread || 0);
      function withUser(next) {
        loadAvatarThen(next, function () {
          fillSessions(next, window.__tlUnread || 0);
          api.request("/notifications/unread").then(function (json) {
            var count = (json.meta && json.meta.count) || (json.data || []).length || 0;
            window.__tlUnread = count;
            fillSessions(next, count);
          }).catch(function () {});
        });
      }
      api.me().then(function (json) {
        if (json && json.data) {
          try { localStorage.setItem("talendus_user", JSON.stringify(json.data)); } catch (e) {}
          withUser(json.data);
        } else withUser(user);
      }).catch(function () {
        if (!api.currentUser()) {
          window.__tlAvatarUrl = "";
          window.__tlUnread = 0;
          fillSessions(null, 0);
          paintSaveButtons();
          return;
        }
        withUser(user);
      });
      paintSaveButtons();
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
      var menuBtn = e.target.closest("[data-session-menu]");
      if (menuBtn) {
        e.preventDefault();
        var wrap = menuBtn.closest(".tl-session");
        var open = wrap && !wrap.classList.contains("is-open");
        document.querySelectorAll(".tl-session.is-open").forEach(function (el) {
          el.classList.remove("is-open");
          var b = el.querySelector("[data-session-menu]");
          if (b) b.setAttribute("aria-expanded", "false");
        });
        if (wrap && open) {
          wrap.classList.add("is-open");
          menuBtn.setAttribute("aria-expanded", "true");
        }
        return;
      }
      if (!e.target.closest(".tl-session")) {
        document.querySelectorAll(".tl-session.is-open").forEach(function (el) {
          el.classList.remove("is-open");
          var b = el.querySelector("[data-session-menu]");
          if (b) b.setAttribute("aria-expanded", "false");
        });
      }
      var logout = e.target.closest("[data-auth-logout]");
      if (logout) {
        e.preventDefault();
        api.logout().then(function () {
          window.__tlAvatarUrl = "";
          window.__tlUnread = 0;
          closeOverlay();
          paintSession();
          window.dispatchEvent(new CustomEvent("talendus:auth", { detail: null }));
        });
        return;
      }
      var open = e.target.closest("[data-auth-open]");
      if (open) {
        e.preventDefault();
        if (isLiveUser()) {
          goToWorkspace(api.currentUser());
          return;
        }
        var mode = open.getAttribute("data-auth-open") || "login";
        var role = open.getAttribute("data-auth-role") || (isEmployerPage() || isHirePersona() ? "EMPLOYER" : "");
        if (mode === "register" || mode === "choose") openAuth("register", role ? { role: role } : {});
        else openAuth(mode, role ? { role: role } : {});
        return;
      }
      var save = e.target.closest("[data-save-job]");
      if (save) {
        e.preventDefault();
        e.stopPropagation();
        var jobId = save.getAttribute("data-save-job");
        if (!jobId) return;
        var user = api.currentUser();
        if (user && user.role !== "CANDIDATE") {
          hintSave(t.saveNeedCandidate);
          return;
        }
        if (user && user.role === "CANDIDATE") {
          var method = save.classList.contains("is-saved") ? "DELETE" : "POST";
          api.request("/jobs/" + jobId + "/save", { method: method }).then(function () {
            paintSaveButtons();
            var hint = document.querySelector(".tl-save-hint");
            if (hint) hint.hidden = true;
          }).catch(function (err) {
            if (err && (err.status === 401 || err.status === 403)) {
              pending = { type: "save", jobId: jobId };
              openAuth("login", { role: "CANDIDATE" });
              return;
            }
            hintSave((err && err.message) || t.saveFailed);
          });
          return;
        }
        pending = { type: "save", jobId: jobId };
        openAuth("register", { role: "CANDIDATE" });
      }
    });

    window.addEventListener("talendus:session-cleared", function () {
      window.__tlAvatarUrl = "";
      window.__tlUnread = 0;
      fillSessions(null, 0);
      paintSaveButtons();
    });

    var hash = parseAuthHash();
    if (hash) {
      if (api.currentUser() && ["login", "register"].indexOf(hash.name) !== -1) {
        history.replaceState(null, "", location.pathname + location.search);
        goToWorkspace(api.currentUser());
      } else {
        var token = hash.query.token || "";
        if ((hash.name === "reset" || hash.name === "verify") && token) {
          try { sessionStorage.setItem("tl-auth-" + hash.name, token); } catch (e) {}
          try { history.replaceState(null, "", location.pathname + location.search + "#/" + hash.name); } catch (e) {}
        } else if (hash.name === "reset" || hash.name === "verify") {
          try { token = sessionStorage.getItem("tl-auth-" + hash.name) || ""; } catch (e) { token = ""; }
        }
        openAuth(hash.name, { token: token, role: hash.query.role, email: hash.query.email });
      }
    }

    paintSession();

    var pageFile = (location.pathname.split("/").pop() || "").toLowerCase();
    var jobSlug = "";
    if (pageFile.indexOf("emploi-") === 0) jobSlug = pageFile.slice("emploi-".length).replace(/\.html$/, "");
    if (pageFile.indexOf("job-") === 0) jobSlug = pageFile.slice("job-".length).replace(/\.html$/, "");
    if (jobSlug) {
      api.request("/jobs/" + encodeURIComponent(jobSlug)).then(function (payload) {
        var job = payload && payload.data;
        if (!job) return;
        if (job.status && job.status !== "PUBLISHED") {
          var applyForm = document.querySelector('[data-form="apply"]') || document.querySelector("#postuler form") || document.querySelector(".tl-job-apply-card form");
          if (applyForm) {
            applyForm.querySelectorAll("input, textarea, select, button").forEach(function (el) { el.disabled = true; });
            var note = document.createElement("p");
            note.className = "tl-save-hint";
            note.textContent = t.jobClosed;
            applyForm.appendChild(note);
          }
        }
        var card = document.querySelector(".tl-job-apply-card");
        var host = card || document.querySelector("#postuler") || document.querySelector(".tl-page-hero .container") || document.querySelector(".tl-section .container");
        if (!host || document.querySelector("[data-save-job]")) return;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tl-btn tl-btn-ghost tl-save-job";
        btn.setAttribute("data-save-job", job.id);
        btn.textContent = t.saveJob;
        var row = document.createElement("p");
        row.className = "tl-job-save-row";
        row.appendChild(btn);
        if (card && card.parentNode) card.parentNode.insertBefore(row, card.nextSibling);
        else host.appendChild(row);
        if (job.saved) {
          btn.textContent = t.savedJob;
          btn.classList.add("is-saved");
        }
        paintSaveButtons();
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

    window.addEventListener("talendus:persona", function () {
      paintSession();
    });
  });
})();
