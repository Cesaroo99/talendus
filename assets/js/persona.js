(function () {
  var KEY = "talendus_persona";

  function pagePersona() {
    var body = document.body;
    if (!body) return "gateway";
    if (body.classList.contains("tl-persona-talent")) return "talent";
    if (body.classList.contains("tl-persona-entreprise")) return "entreprise";
    return "gateway";
  }

  function storedPersona() {
    try {
      return localStorage.getItem(KEY) || "";
    } catch (err) {
      return "";
    }
  }

  function persist(persona) {
    if (persona !== "talent" && persona !== "entreprise") return;
    try {
      localStorage.setItem(KEY, persona);
    } catch (err) { /* ignore quota / private mode */ }
  }

  function userPersona() {
    var api = window.TalendusAPI;
    var user = api && api.currentUser && api.currentUser();
    if (!user) return "";
    if (user.role === "CANDIDATE") return "talent";
    if (user.role === "EMPLOYER") return "entreprise";
    return "";
  }

  function effective() {
    return userPersona() || storedPersona() || pagePersona();
  }

  function apply(persona) {
    var body = document.body;
    if (!body) return;
    body.classList.remove("tl-persona-talent", "tl-persona-entreprise", "tl-persona-gateway");
    body.classList.add("tl-persona-" + persona);
    body.setAttribute("data-persona", persona);
    try { window.dispatchEvent(new CustomEvent("talendus:persona", { detail: persona })); } catch (err) {}
  }

  function init() {
    var page = pagePersona();
    if (page !== "gateway" && !userPersona()) persist(page);
    apply(effective());

    document.addEventListener("click", function (event) {
      var trigger = event.target.closest("[data-set-persona]");
      if (!trigger) return;
      var persona = trigger.getAttribute("data-set-persona");
      if (persona !== "talent" && persona !== "entreprise") return;
      persist(persona);
      apply(persona);
    });
  }

  window.TalendusPersona = {
    apply: apply,
    persist: persist,
    current: effective
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
