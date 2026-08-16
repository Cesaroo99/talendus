(function (global) {
  var KEY = "talendus-consent-v1";
  var EVENT = "talendus:consent";

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data || typeof data !== "object") return null;
      return {
        essential: true,
        analytics: !!data.analytics,
        marketing: !!data.marketing,
        updatedAt: data.updatedAt || null
      };
    } catch (e) {
      return null;
    }
  }

  function write(analytics, marketing) {
    var data = {
      essential: true,
      analytics: !!analytics,
      marketing: !!marketing,
      updatedAt: new Date().toISOString()
    };
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {}
    global.dispatchEvent(new CustomEvent(EVENT, { detail: data }));
    return data;
  }

  function isEn() {
    return (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  }

  function copy() {
    if (isEn()) {
      return {
        title: "Cookies on talendus.ca",
        text: "Essential cookies keep the site working. Analytics and marketing cookies load only if you accept them. You can change this later.",
        accept: "Accept all",
        reject: "Essential only",
        privacy: "Privacy policy",
        privacyHref: "privacy.html"
      };
    }
    return {
      title: "Cookies sur talendus.ca",
      text: "Les cookies essentiels font fonctionner le site. Les cookies d’analyse et de marketing ne sont chargés que si vous les acceptez. Vous pourrez modifier ce choix plus tard.",
      accept: "Tout accepter",
      reject: "Essentiels seulement",
      privacy: "Confidentialité",
      privacyHref: "confidentialite.html"
    };
  }

  function prefix() {
    var path = global.location.pathname || "";
    if (path.indexOf("/en/") === 0 || path.indexOf("/blog/") === 0) {
      if (path.indexOf("/en/") === 0) return "";
      return "/";
    }
    return "";
  }

  function privacyUrl(href) {
    var path = global.location.pathname || "";
    if (path.indexOf("/en/") === 0) return href;
    if (path.indexOf("/blog/") === 0) return "/" + (isEn() ? "en/privacy.html" : "confidentialite.html");
    return href;
  }

  function hide(box) {
    if (box && box.parentNode) box.parentNode.removeChild(box);
  }

  function renderBanner() {
    if (read() || document.getElementById("tl-consent")) return;
    var t = copy();
    var box = document.createElement("div");
    box.id = "tl-consent";
    box.className = "tl-consent";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-labelledby", "tl-consent-title");
    box.innerHTML =
      '<div class="tl-consent-inner">' +
      '<div><p id="tl-consent-title" class="tl-consent-title">' + t.title + "</p>" +
      '<p class="tl-consent-text">' + t.text + ' <a href="' + privacyUrl(t.privacyHref) + '">' + t.privacy + "</a>.</p></div>" +
      '<div class="tl-consent-actions">' +
      '<button type="button" class="tl-btn" data-consent="all">' + t.accept + "</button>" +
      '<button type="button" class="tl-btn tl-btn-ghost" data-consent="essential">' + t.reject + "</button>" +
      "</div></div>";
    document.body.appendChild(box);
    box.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-consent]");
      if (!btn) return;
      var all = btn.getAttribute("data-consent") === "all";
      write(all, all);
      hide(box);
    });
  }

  function openPrefs() {
    try { localStorage.removeItem(KEY); } catch (e) {}
    var existing = document.getElementById("tl-consent");
    hide(existing);
    renderBanner();
  }

  global.TalendusConsent = {
    read: read,
    write: write,
    open: openPrefs,
    eventName: EVENT
  };

  document.addEventListener("DOMContentLoaded", renderBanner);
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-consent-open]")) {
      e.preventDefault();
      openPrefs();
    }
  });
})(window);
