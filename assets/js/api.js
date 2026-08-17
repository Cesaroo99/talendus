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

  function request(path, opts) {
    opts = opts || {};
    var headers = Object.assign({ "Accept": "application/json" }, opts.headers || {});
    if (opts.body && !(opts.body instanceof FormData) && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }
    var token = opts.token || getAccess();
    if (token) headers.Authorization = "Bearer " + token;
    return fetch(apiRoot() + path, {
      method: opts.method || "GET",
      headers: headers,
      body: opts.body instanceof FormData ? opts.body : (opts.body ? JSON.stringify(opts.body) : undefined)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (json) {
        if (!res.ok || json.success === false) {
          var publicAuth = /\/auth\/(login|register|oauth|forgot-password|reset-password|verify-email)/.test(path);
          if (res.status === 401 && token && !publicAuth) {
            clearSession();
            try { window.dispatchEvent(new CustomEvent("talendus:session-cleared")); } catch (e) {}
          }
          var err = new Error((json && json.message) || "Erreur API");
          err.code = json && json.code;
          err.status = res.status;
          err.payload = json;
          throw err;
        }
        return json;
      });
    });
  }

  global.TalendusAPI = {
    request: request,
    setSession: setSession,
    clearSession: clearSession,
    currentUser: currentUser,
    bootstrap: function () { return request("/admin/bootstrap"); },
    createCandidate: function (body) { return request("/admin/candidates", { method: "POST", body: body }); },
    profile: function () { return request("/candidates/me"); },
    updateProfile: function (body) { return request("/candidates/me", { method: "PATCH", body: body }); },
    uploadResume: function (formData) { return request("/candidates/me/resume", { method: "POST", body: formData }); },
    register: function (body) {
      return request("/auth/register", { method: "POST", body: body }).then(function (json) {
        setSession(json.data);
        return json;
      });
    },
    login: function (email, password) {
      return request("/auth/login", { method: "POST", body: { email: email, password: password } }).then(function (json) {
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
    me: function () { return request("/users/me"); },
    providers: function () { return request("/auth/providers"); },
    forgotPassword: function (email) { return request("/auth/forgot-password", { method: "POST", body: { email: email } }); },
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
    myApplications: function () { return request("/applications/me"); },
    notifications: function (unread) { return request("/notifications" + (unread ? "?unread=true" : "")); },
    contact: function (body) { return request("/contact", { method: "POST", body: body }); },
    createInvoice: function (body) { return request("/invoices", { method: "POST", body: body }); },
    createInterview: function (body) { return request("/interviews", { method: "POST", body: body }); },
    signContract: function (id, body) { return request("/contracts/" + id + "/sign", { method: "POST", body: body }); }
  };
})(window);
