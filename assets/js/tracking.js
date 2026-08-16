(function (global) {
  var loaded = { ga: false, pixel: false };
  var config = null;
  var pageViewSent = false;

  function consent() {
    return global.TalendusConsent && global.TalendusConsent.read();
  }

  function allowed(kind) {
    var c = consent();
    if (!c) return false;
    if (kind === "analytics") return !!c.analytics;
    if (kind === "marketing") return !!c.marketing;
    return false;
  }

  function loadScript(src, id) {
    if (document.getElementById(id)) return;
    var s = document.createElement("script");
    s.id = id;
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  function bootGa(id) {
    if (loaded.ga || !id || !allowed("analytics")) return;
    loaded.ga = true;
    global.dataLayer = global.dataLayer || [];
    global.gtag = global.gtag || function () { global.dataLayer.push(arguments); };
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id), "tl-ga");
    global.gtag("js", new Date());
    global.gtag("consent", "update", { analytics_storage: "granted" });
    global.gtag("config", id, { anonymize_ip: true, send_page_view: false });
  }

  function bootPixel(id) {
    if (loaded.pixel || !id || !allowed("marketing")) return;
    loaded.pixel = true;
    if (!global.fbq) {
      var n = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      n.queue = [];
      n.loaded = true;
      n.version = "2.0";
      global.fbq = n;
      global._fbq = n;
    }
    loadScript("https://connect.facebook.net/en_US/fbevents.js", "tl-meta-pixel");
    global.fbq("consent", "grant");
    global.fbq("init", id);
  }

  function sendPageView() {
    if (pageViewSent) return;
    pageViewSent = true;
    if (loaded.ga && global.gtag) {
      global.gtag("event", "page_view", { page_location: location.href, page_title: document.title });
    }
    if (loaded.pixel && global.fbq) global.fbq("track", "PageView");
  }

  function track(name, params) {
    params = params || {};
    if (loaded.ga && global.gtag && allowed("analytics")) {
      global.gtag("event", name, params);
    }
    if (loaded.pixel && global.fbq && allowed("marketing")) {
      var map = {
        generate_lead: "Lead",
        contact: "Contact",
        submit_application: "SubmitApplication",
        search: "Search",
        view_content: "ViewContent",
        page_view: "PageView"
      };
      var pixelName = map[name] || name;
      global.fbq("track", pixelName, params);
    }
  }

  function applyConfig(data) {
    config = data || {};
    if (!config.enabled) return;
    if (allowed("analytics")) bootGa(config.ga_measurement_id);
    if (allowed("marketing")) bootPixel(config.meta_pixel_id);
    sendPageView();
    var file = (location.pathname.split("/").pop() || "").toLowerCase();
    if (file.indexOf("emploi-") === 0 || file.indexOf("job-") === 0) {
      track("view_content", { content_name: document.title, content_type: "job" });
    }
  }

  function fetchConfig() {
    var c = consent();
    if (!c || (!c.analytics && !c.marketing)) return;
    fetch("/api/tracking/config", { headers: { Accept: "application/json" } })
      .then(function (res) { return res.json(); })
      .then(function (json) { applyConfig(json && json.data); })
      .catch(function () {});
  }

  global.TalendusTrack = {
    event: track,
    lead: function (params) { track("generate_lead", params); },
    contact: function (params) { track("contact", params); },
    apply: function (params) { track("submit_application", params); },
    search: function (params) { track("search", params); },
    viewContent: function (params) { track("view_content", params); }
  };

  document.addEventListener("DOMContentLoaded", fetchConfig);
  global.addEventListener("talendus:consent", fetchConfig);
})(window);
