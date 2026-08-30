const CACHE = "talendus-app-v31";
const PRECACHE = [
  "/offline.html",
  "/en/offline.html",
  "/m.html",
  "/en/m.html",
  "/manifest.webmanifest",
  "/assets/css/mobile-app.css",
  "/assets/js/api.js",
  "/assets/js/talendus-call.js",
  "/assets/js/mobile-app.js",
  "/assets/img/logo/icon-192.png",
  "/assets/img/logo/apple-touch-icon.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(PRECACHE).catch(function () {});
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

function isEnPath(pathname) {
  return /\/en(\/|$)/.test(pathname || "");
}

function defaultNotifsHref(en) {
  return (en ? "/en/m.html" : "/m.html") + "#/notifs";
}

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (url.pathname.indexOf("/api/") === 0) return;
  if (url.pathname.indexOf("/download/") === 0) return;
  if (url.pathname.indexOf("/assets/app/") === 0) return;
  event.respondWith(
    fetch(req).then(function (res) {
      if (res && res.ok && req.destination !== "document") {
        var copy = res.clone();
        caches.open(CACHE).then(function (cache) { cache.put(req, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (cached) {
        if (cached) return cached;
        if (req.mode === "navigate") {
          var offline = isEnPath(url.pathname) ? "/en/offline.html" : "/offline.html";
          return caches.match(offline).then(function (page) { return page || caches.match("/offline.html"); });
        }
        return Response.error();
      });
    })
  );
});

self.addEventListener("push", function (event) {
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
      var en = false;
      for (var i = 0; i < list.length; i++) {
        if (list[i].url && list[i].url.indexOf("/en/m.html") !== -1) { en = true; break; }
      }
      var payload = {
        title: "Talendus",
        body: "",
        href: defaultNotifsHref(en),
        icon: "/assets/img/logo/icon-192.png"
      };
      try {
        if (event.data) payload = Object.assign(payload, event.data.json());
      } catch (e) {
        try { payload.body = event.data ? event.data.text() : ""; } catch (err) {}
      }
      if (!payload.href || payload.href === "/m.html#/notifs") payload.href = defaultNotifsHref(en);
      var tag = payload.tag || payload.id || [payload.title || "", payload.body || payload.message || ""].join("|") || "talendus";
      return self.registration.showNotification(payload.title || "Talendus", {
        body: payload.body || payload.message || "",
        icon: payload.icon || "/assets/img/logo/icon-192.png",
        badge: "/assets/img/logo/icon-192.png",
        data: { href: payload.href || defaultNotifsHref(en) },
        tag: tag,
        renotify: false
      });
    })
  );
});

self.addEventListener("notificationclick", function (event) {
  event.notification.close();
  var href = (event.notification.data && event.notification.data.href) || "/m.html#/notifs";
  if (href.indexOf("http") !== 0) {
    href = self.location.origin + (href.charAt(0) === "/" ? href : "/" + href);
  }
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
      for (var i = 0; i < list.length; i++) {
        var client = list[i];
        if (client.url && client.url.indexOf("/m.html") !== -1 && "focus" in client) {
          if (client.navigate) client.navigate(href);
          return client.focus();
        }
      }
      if (self.clients.openWindow) return self.clients.openWindow(href);
    })
  );
});
