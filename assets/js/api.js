(function (global) {
  var ACCESS = "talendus_access_token";
  var REFRESH = "talendus_refresh_token";
  var USER = "talendus_user";

  function apiRoot() {
    if (global.TALENDUS_API_URL) return String(global.TALENDUS_API_URL).replace(/\/$/, "");
    return "/api";
  }

  function getAccess() {
    try { return localStorage.getItem(ACCESS) || ""; } catch (e) { return ""; }
  }

  function setSession(data) {
    if (!data) return;
    try {
      if (data.access_token) localStorage.setItem(ACCESS, data.access_token);
      if (data.refresh_token) localStorage.setItem(REFRESH, data.refresh_token);
      if (data.user) localStorage.setItem(USER, JSON.stringify(data.user));
    } catch (e) {}
    try { window.dispatchEvent(new CustomEvent("talendus:session-set")); } catch (e) {}
  }

  function clearSession() {
    try {
      localStorage.removeItem(ACCESS);
      localStorage.removeItem(REFRESH);
      localStorage.removeItem(USER);
    } catch (e) {}
  }

  function currentUser() {
    try { return JSON.parse(localStorage.getItem(USER) || "null"); } catch (e) { return null; }
  }

  var refreshPromise = null;

  function getRefresh() {
    try { return localStorage.getItem(REFRESH) || ""; } catch (e) { return ""; }
  }

  function isPublicAuthPath(path) {
    return /\/auth\/(login|register|oauth|forgot-password|reset-password|verify-email|refresh)/.test(path);
  }

  function expireSession() {
    clearSession();
    try { window.dispatchEvent(new CustomEvent("talendus:session-cleared")); } catch (e) {}
  }

  function refreshAccess() {
    if (refreshPromise) return refreshPromise;
    var rt = getRefresh();
    if (!rt) return Promise.reject(new Error("no-refresh"));
    refreshPromise = fetch(apiRoot() + "/auth/refresh", {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: rt })
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (json) {
        if (!res.ok || json.success === false) {
          throw new Error((json && json.message) || sessionExpiredMsg());
        }
        setSession(json.data);
        return (json.data && json.data.access_token) || "";
      });
    });
    refreshPromise = refreshPromise.then(function (token) {
      refreshPromise = null;
      return token;
    }, function (err) {
      refreshPromise = null;
      throw err;
    });
    return refreshPromise;
  }

  function pageIsEn() {
    try {
      if ((document.documentElement.lang || "").toLowerCase().indexOf("en") === 0) return true;
      return /\/en(\/|$)/.test(location.pathname || "");
    } catch (e) { return false; }
  }
  function fallbackErr() {
    return pageIsEn() ? "Something went wrong." : "Une erreur s’est produite.";
  }
  function sessionExpiredMsg() {
    return pageIsEn() ? "Session expired. Sign in again." : "Session expirée";
  }

  function failPayload(res, json) {
    var err = new Error((json && json.message) || fallbackErr());
    err.code = json && json.code;
    err.status = res.status;
    err.payload = json;
    return err;
  }

  function request(path, opts) {
    opts = opts || {};
    var headers = Object.assign({ "Accept": "application/json" }, opts.headers || {});
    if (opts.body && !(opts.body instanceof FormData) && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }
    var token = opts.token || getAccess();
    if (token && !isPublicAuthPath(path)) headers.Authorization = "Bearer " + token;
    return fetch(apiRoot() + path, {
      method: opts.method || "GET",
      headers: headers,
      body: opts.body instanceof FormData ? opts.body : (opts.body ? JSON.stringify(opts.body) : undefined)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (json) {
        if (!res.ok || json.success === false) {
          var canRefresh = res.status === 401 && token && !isPublicAuthPath(path) && !opts._retried;
          if (canRefresh) {
            return refreshAccess().then(function (next) {
              return request(path, Object.assign({}, opts, { token: next, _retried: true }));
            }).catch(function () {
              expireSession();
              throw failPayload(res, json);
            });
          }
          if (res.status === 401 && token && !isPublicAuthPath(path)) expireSession();
          throw failPayload(res, json);
        }
        return json;
      });
    }).catch(function (err) {
      if (err && (err.status || err.code || err.payload)) throw err;
      var net = new Error(pageIsEn()
        ? "Cannot reach Talendus. Check your connection and try again."
        : "Impossible de joindre Talendus. Vérifiez la connexion, puis réessayez.");
      net.code = "NETWORK";
      throw net;
    });
  }

  function filePartName(file, fallback) {
    var name = String((file && file.name) || "").trim();
    var type = String((file && file.type) || "").toLowerCase();
    var ext = "";
    if (type.indexOf("png") !== -1) ext = ".png";
    else if (type === "image/jpeg" || type === "image/jpg") ext = ".jpg";
    else if (type.indexOf("webp") !== -1) ext = ".webp";
    else if (type.indexOf("pdf") !== -1) ext = ".pdf";
    else if (type.indexOf("wordprocessingml") !== -1) ext = ".docx";
    else if (type.indexOf("msword") !== -1) ext = ".doc";
    if (name && /\.[A-Za-z0-9]{2,8}$/.test(name)) return name;
    var fallbackName = String(fallback || "document");
    var fallbackExt = (fallbackName.match(/\.[A-Za-z0-9]{2,8}$/) || [".pdf"])[0];
    var base = (name.replace(/\.[^.]*$/, "") || fallbackName.replace(/\.[^.]+$/, "") || "document");
    return base + (ext || fallbackExt);
  }

  function appendFile(formData, file, fallback) {
    formData.append("file", file, filePartName(file, fallback || "document.pdf"));
    return formData;
  }

  global.TalendusAPI = {
    request: request,
    filePartName: filePartName,
    appendFile: appendFile,
    setSession: setSession,
    clearSession: clearSession,
    currentUser: currentUser,
    bootstrap: function () { return request("/admin/bootstrap"); },
    createCandidate: function (body) { return request("/admin/candidates", { method: "POST", body: body }); },
    profile: function () { return request("/candidates/me"); },
    updateProfile: function (body) { return request("/candidates/me", { method: "PATCH", body: body }); },
    uploadResume: function (formData) { return request("/candidates/me/resume", { method: "POST", body: formData }); },
    register: function (body) {
      body = Object.assign({}, body || {});
      if (body.email) body.email = String(body.email).trim().toLowerCase();
      return request("/auth/register", { method: "POST", body: body }).then(function (json) {
        setSession(json.data);
        return json;
      });
    },
    login: function (email, password) {
      return request("/auth/login", {
        method: "POST",
        body: { email: String(email || "").trim().toLowerCase(), password: String(password || "") }
      }).then(function (json) {
        setSession(json.data);
        return json;
      });
    },
    logout: function () {
      var refresh = "";
      try { refresh = localStorage.getItem(REFRESH) || ""; } catch (e) {}
      return request("/auth/logout", { method: "POST", body: refresh ? { refresh_token: refresh } : {} })
        .catch(function () { return null; })
        .then(function () { clearSession(); });
    },
    me: function () {
      return request("/users/me").then(function (json) {
        if (json && json.data) {
          try { localStorage.setItem(USER, JSON.stringify(json.data)); } catch (e) {}
        }
        return json;
      });
    },
    providers: function () { return request("/auth/providers"); },
    forgotPassword: function (email) { return request("/auth/forgot-password", { method: "POST", body: { email: String(email || "").trim().toLowerCase() } }); },
    resetPassword: function (token, password) {
      return request("/auth/reset-password", { method: "POST", body: { token: token, new_password: password } });
    },
    verifyEmail: function (token) { return request("/auth/verify-email", { method: "POST", body: { token: token } }); },
    oauthGoogle: function (body) {
      return request("/auth/oauth/google", { method: "POST", body: body }).then(function (json) {
        setSession(json.data);
        return json;
      });
    },
    oauthLinkedIn: function (body) {
      return request("/auth/oauth/linkedin", { method: "POST", body: body }).then(function (json) {
        setSession(json.data);
        return json;
      });
    },
    saveJob: function (jobId) { return request("/jobs/" + jobId + "/save", { method: "POST" }); },
    unsaveJob: function (jobId) { return request("/jobs/" + jobId + "/save", { method: "DELETE" }); },
    jobs: function (params) {
      var q = new URLSearchParams();
      Object.keys(params || {}).forEach(function (k) {
        if (params[k] !== undefined && params[k] !== null && params[k] !== "") q.set(k, params[k]);
      });
      var suffix = q.toString() ? ("?" + q.toString()) : "";
      return request("/jobs" + suffix);
    },
    apply: function (body) { return request("/applications", { method: "POST", body: body }); },
    applyPublic: function (body) { return request("/applications/public", { method: "POST", body: body }); },
    submitTalentProfile: function (body) { return request("/talent-profile", { method: "POST", body: body }); },
    myApplications: function () { return request("/applications/me"); },
    notifications: function (unread) { return request("/notifications" + (unread ? "?unread=true" : "")); },
    contact: function (body) { return request("/contact", { method: "POST", body: body }); },
    services: function () { return request("/services"); },
    createInvoice: function (body) { return request("/invoices", { method: "POST", body: body }); },
    createInterview: function (body) { return request("/interviews", { method: "POST", body: body }); },
    signContract: function (id, body) { return request("/contracts/" + id + "/sign", { method: "POST", body: body }); },
    createContract: function (body) { return request("/contracts", { method: "POST", body: body }); },
    previewContract: function (query) { return request("/contracts/preview" + (query || "")); },
    sendContract: function (id) { return request("/contracts/" + id + "/send", { method: "POST" }); },
    download: function (path, filename) {
      var token = getAccess();
      var abs = apiRoot() + path;
      if (abs.indexOf("http") !== 0) abs = (location.origin || "") + abs;
      if (window.TalendusNative && typeof window.TalendusNative.downloadUrl === "function") {
        try {
          window.TalendusNative.downloadUrl(abs, filename || "document", token || "");
          return Promise.resolve();
        } catch (err) {}
      }
      var headers = { "Accept": "*/*" };
      if (token) headers.Authorization = "Bearer " + token;
      return fetch(abs, { headers: headers, credentials: "same-origin" }).then(function (res) {
        if (!res.ok) throw new Error(pageIsEn() ? "Download failed." : "Téléchargement impossible.");
        return res.blob().then(function (blob) {
          var url = URL.createObjectURL(blob);
          var a = document.createElement("a");
          a.href = url;
          a.download = filename || "document";
          a.rel = "noopener";
          document.body.appendChild(a);
          a.click();
          a.remove();
          var ua = navigator.userAgent || "";
          if (/iphone|ipad|ipod/i.test(ua)) {
            var opened = null;
            try { opened = window.open(url, "_blank"); } catch (e) {}
            if (!opened) location.assign(url);
          }
          setTimeout(function () { URL.revokeObjectURL(url); }, 8000);
        });
      });
    }
  };
})(window);
