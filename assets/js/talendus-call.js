(function (global) {
  var STYLE_ID = "tn-call-css";
  var CSS = "" +
    "#tn-call-overlay{display:none;position:fixed;inset:0;z-index:240;color:#fff;font-family:inherit;" +
      "background:radial-gradient(120% 90% at 50% -10%,#1d4f86 0%,#102848 38%,#07111f 100%)}" +
    "#tn-call-overlay.is-on{display:flex;flex-direction:column}" +
    "#tn-call-overlay::before{content:'';position:absolute;inset:0;pointer-events:none;z-index:0;" +
      "background:radial-gradient(42% 36% at 12% 88%,rgba(232,112,36,.22),transparent 70%)," +
      "radial-gradient(38% 32% at 92% 12%,rgba(90,168,255,.16),transparent 68%)}" +
    "#tn-call-overlay .tn-call-top,#tn-call-overlay .tn-call-stage,#tn-call-overlay .tn-call-dock," +
      "#tn-call-overlay .tn-call-wrap{position:relative;z-index:1}" +
    "#tn-call-overlay .tn-call-top{display:flex;align-items:center;justify-content:space-between;gap:12px;" +
      "padding:14px 18px 10px;padding-top:calc(14px + env(safe-area-inset-top))}" +
    "#tn-call-overlay .tn-call-brand{display:flex;align-items:center;gap:10px;min-width:0}" +
    "#tn-call-overlay .tn-call-mark{width:38px;height:38px;border-radius:12px;background:linear-gradient(160deg,#ff8a3d,#e87024);" +
      "display:inline-flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 8px 20px rgba(232,112,36,.35)}" +
    "#tn-call-overlay .tn-call-brand strong{display:block;font-size:15px;letter-spacing:.01em}" +
    "#tn-call-overlay .tn-call-brand span{display:block;font-size:12px;opacity:.7}" +
    "#tn-call-overlay .tn-call-meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}" +
    "#tn-call-overlay .tn-call-pill{border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:6px 12px;" +
      "font-size:12px;font-weight:700;letter-spacing:.02em;background:rgba(7,17,31,.42);backdrop-filter:blur(14px)}" +
    "#tn-call-overlay .tn-call-pill.is-live{background:rgba(46,184,122,.18);border-color:rgba(46,184,122,.45);color:#b8f3d4}" +
    "#tn-call-overlay .tn-call-stage{flex:1;position:relative;margin:4px 14px 0;border-radius:28px;overflow:hidden;" +
      "background:linear-gradient(180deg,#0a1626,#050b14);box-shadow:0 24px 60px rgba(0,0,0,.35),inset 0 0 0 1px rgba(255,255,255,.06)}" +
    "#tn-call-overlay video{object-fit:cover;background:#000}" +
    "#tn-call-overlay .tn-call-remote{width:100%;height:100%}" +
    "#tn-call-overlay .tn-call-local{position:absolute;right:14px;bottom:14px;width:28%;max-width:164px;aspect-ratio:3/4;" +
      "border-radius:18px;border:2px solid rgba(255,255,255,.5);z-index:3;box-shadow:0 16px 32px rgba(0,0,0,.4);background:#0b1726}" +
    "#tn-call-overlay.is-audio .tn-call-local{display:none}" +
    "#tn-call-overlay .tn-call-chip{position:absolute;left:14px;bottom:14px;z-index:3;display:none;align-items:center;gap:8px;" +
      "padding:6px 10px;border-radius:999px;background:rgba(7,17,31,.55);backdrop-filter:blur(12px);font-size:12px;font-weight:700}" +
    "#tn-call-overlay.is-live .tn-call-chip{display:inline-flex}" +
    "#tn-call-overlay .tn-call-wait{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;" +
      "gap:16px;text-align:center;padding:28px;z-index:2;background:radial-gradient(70% 60% at 50% 42%,rgba(22,54,95,.35),transparent 72%)}" +
    "#tn-call-overlay .tn-call-orb-wrap{position:relative;width:132px;height:132px}" +
    "#tn-call-overlay .tn-call-ring{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(232,112,36,.28);animation:tnCallPulse 2.2s ease-out infinite}" +
    "#tn-call-overlay .tn-call-ring:nth-child(2){animation-delay:.7s}" +
    "#tn-call-overlay .tn-call-orb{position:absolute;inset:16px;border-radius:50%;overflow:hidden;" +
      "background:linear-gradient(160deg,#e87024,#c45312);display:flex;align-items:center;justify-content:center;" +
      "font-size:34px;font-weight:800;box-shadow:0 10px 28px rgba(232,112,36,.28)}" +
    "#tn-call-overlay .tn-call-orb img{width:100%;height:100%;object-fit:cover}" +
    "#tn-call-overlay.is-live .tn-call-wait{display:none}" +
    "#tn-call-overlay .tn-call-status{margin:0;font-weight:800;font-size:22px;letter-spacing:-.02em}" +
    "#tn-call-overlay .tn-call-hint{margin:0;opacity:.74;font-size:14px;max-width:340px;line-height:1.45}" +
    "#tn-call-overlay .tn-call-dock{display:flex;gap:16px;justify-content:center;align-items:flex-end;" +
      "padding:16px 16px calc(20px + env(safe-area-inset-bottom))}" +
    "#tn-call-overlay .tn-call-btn{min-width:64px;height:64px;border:0;border-radius:22px;color:#fff;font-weight:800;cursor:pointer;" +
      "display:inline-flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:10px;letter-spacing:.03em;" +
      "background:rgba(255,255,255,.1);backdrop-filter:blur(16px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}" +
    "#tn-call-overlay .tn-call-btn i{font-size:18px}" +
    "#tn-call-overlay .tn-call-btn.is-mute{background:rgba(61,79,102,.72)}" +
    "#tn-call-overlay .tn-call-btn.is-mute.is-off{background:#c62828}" +
    "#tn-call-overlay .tn-call-btn.is-cam{background:rgba(22,54,95,.78)}" +
    "#tn-call-overlay .tn-call-btn.is-cam.is-off{background:#3d4f66}" +
    "#tn-call-overlay .tn-call-btn.is-hang{background:linear-gradient(180deg,#e53935,#c62828);min-width:148px;border-radius:32px;" +
      "width:auto;padding:0 22px;flex-direction:row;gap:8px;font-size:14px;box-shadow:0 12px 24px rgba(198,40,40,.35)}" +
    "#tn-call-overlay .tn-call-btn.is-retry{background:linear-gradient(180deg,#ff8a3d,#e87024)}" +
    "#tn-call-overlay .tn-call-err{padding:48px 24px 12px;text-align:center;font-size:18px;font-weight:700;max-width:420px;margin:auto;position:relative;z-index:1}" +
    "#tn-call-overlay .tn-call-wrap{flex:1;display:flex;align-items:center;justify-content:center;padding:24px 16px}" +
    "#tn-call-overlay .tn-call-wrap-card{width:min(440px,100%);background:rgba(10,18,32,.78);border:1px solid rgba(255,255,255,.1);" +
      "border-radius:28px;padding:28px 22px;text-align:center;backdrop-filter:blur(22px);box-shadow:0 24px 60px rgba(0,0,0,.35)}" +
    "#tn-call-overlay .tn-call-wrap-card h2{margin:14px 0 8px;font-size:24px}" +
    "#tn-call-overlay .tn-call-wrap-card p{margin:0 0 18px;opacity:.74;line-height:1.45}" +
    "#tn-call-overlay .tn-call-wrap-actions{display:grid;gap:10px}" +
    "#tn-call-overlay .tn-call-wrap-actions button{border:0;border-radius:16px;padding:14px 16px;font-weight:800;cursor:pointer;font-size:15px}" +
    "#tn-call-overlay .tn-call-wrap-actions .is-done{background:#e87024;color:#fff}" +
    "#tn-call-overlay .tn-call-wrap-actions .is-miss{background:rgba(255,255,255,.1);color:#fff}" +
    "#tn-call-overlay .tn-call-wrap-actions .is-cancel{background:rgba(198,40,40,.2);color:#ffd4d4}" +
    "#tn-call-overlay .tn-call-wrap-skip{margin-top:12px;background:transparent;border:0;color:rgba(255,255,255,.7);font-weight:700;cursor:pointer}" +
    "@keyframes tnCallPulse{0%{transform:scale(.72);opacity:.7}100%{transform:scale(1.18);opacity:0}}" +
    "@media (max-width:720px){#tn-call-overlay .tn-call-stage{margin:0;border-radius:0;box-shadow:none}" +
      "#tn-call-overlay .tn-call-local{width:34%;max-width:128px;right:10px;bottom:10px}}";

  var live = null;
  var avatarCache = {};

  function injectCss() {
    if (document.getElementById(STYLE_ID)) return;
    var el = document.createElement("style");
    el.id = STYLE_ID;
    el.textContent = CSS;
    document.head.appendChild(el);
  }

  function overlay() {
    var el = document.getElementById("tn-call-overlay");
    if (!el) {
      el = document.createElement("div");
      el.id = "tn-call-overlay";
      el.setAttribute("hidden", "");
      document.body.appendChild(el);
    }
    return el;
  }

  function api() { return global.TalendusAPI; }

  function request(path, opts) {
    return api().request(path, opts);
  }

  function dataOf(json) {
    return json && json.data !== undefined ? json.data : json;
  }

  function authToken() {
    try { return localStorage.getItem("talendus_access_token") || ""; } catch (e) { return ""; }
  }

  function labels() {
    var en = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    return en ? {
      connecting: "Connecting…",
      waiting: "Waiting for the other person…",
      live: "Connected",
      ended: "Call ended",
      reconnecting: "Reconnecting…",
      mute: "Mute",
      unmute: "Unmute",
      camera: "Camera",
      hangup: "Hang up",
      micDenied: "Allow the microphone (and camera for video) to join the interview.",
      unsupported: "This device cannot place an in-app call.",
      waitHost: "The recruiter has not started the call yet.",
      brand: "Talendus interview",
      audioHint: "Audio only. Stay on this screen — the recruiter joins you here.",
      unavailable: "This interview cannot be taken in the app.",
      forbidden: "You cannot join this call.",
      retry: "Try again",
      you: "You",
      wrapTitle: "How did the interview go?",
      wrapHint: "This status is sent to the candidate right away.",
      wrapDone: "Completed",
      wrapMiss: "No-show",
      wrapCancel: "Cancelled",
      wrapSkip: "Close without changing the status",
      wrapSaved: "Status sent to the candidate."
    } : {
      connecting: "Connexion…",
      waiting: "En attente de l’autre personne…",
      live: "En ligne",
      ended: "Appel terminé",
      reconnecting: "Reconnexion…",
      mute: "Muet",
      unmute: "Son",
      camera: "Caméra",
      hangup: "Raccrocher",
      micDenied: "Autorisez le micro (et la caméra en visio) pour rejoindre l’entretien.",
      unsupported: "Cet appareil ne peut pas passer d’appel dans l’appli.",
      waitHost: "Le recruteur n’a pas encore lancé l’appel.",
      brand: "Entretien Talendus",
      audioHint: "Audio seulement. Restez sur cet écran — le recruteur vous rejoint ici.",
      unavailable: "Cet entretien ne peut pas se faire dans l’appli.",
      forbidden: "Vous ne pouvez pas rejoindre cet appel.",
      retry: "Relancer",
      you: "Vous",
      wrapTitle: "Comment s’est passé l’entretien ?",
      wrapHint: "Ce statut arrive tout de suite chez le candidat.",
      wrapDone: "Terminé",
      wrapMiss: "Absent",
      wrapCancel: "Annulé",
      wrapSkip: "Fermer sans changer le statut",
      wrapSaved: "Statut envoyé au candidat."
    };
  }

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function formatClock(ms) {
    var s = Math.max(0, Math.floor(ms / 1000));
    var m = Math.floor(s / 60);
    var h = Math.floor(m / 60);
    s = s % 60;
    m = m % 60;
    if (h) return h + ":" + String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
    return m + ":" + String(s).padStart(2, "0");
  }

  function setStatus(text) {
    if (!live) return;
    live.statusText = text;
    var el = overlay().querySelector(".tn-call-status");
    if (el) el.textContent = text;
    var pill = overlay().querySelector("[data-call-pill]");
    if (pill) {
      pill.textContent = text;
      pill.classList.toggle("is-live", text === labels().live);
    }
  }

  function remotePeer(peers) {
    peers = peers || (live && live.peers) || [];
    var i;
    for (i = 0; i < peers.length; i++) {
      if (peers[i] && !peers[i].self) return peers[i];
    }
    return null;
  }

  function blobLooksLikeImage(blob) {
    if (!blob || !blob.size) return false;
    var t = String(blob.type || "").toLowerCase();
    if (!t || t === "application/octet-stream" || t.indexOf("octet") >= 0) return true;
    return t.indexOf("image") === 0;
  }

  function fetchAvatar(userId) {
    if (!userId) return Promise.resolve("");
    if (avatarCache[userId]) return Promise.resolve(avatarCache[userId]);
    if (userId === (live && live.selfId) && global.__tlAvatarUrl) {
      avatarCache[userId] = global.__tlAvatarUrl;
      return Promise.resolve(avatarCache[userId]);
    }
    var token = authToken();
    return fetch("/api/users/" + encodeURIComponent(userId) + "/avatar", {
      headers: token ? { Authorization: "Bearer " + token } : {}
    }).then(function (res) {
      if (!res.ok) throw new Error("avatar");
      return res.blob();
    }).then(function (blob) {
      if (!blobLooksLikeImage(blob)) throw new Error("type");
      avatarCache[userId] = URL.createObjectURL(blob);
      return avatarCache[userId];
    }).catch(function () { return ""; });
  }

  function paintPeerFace(peer) {
    var orb = overlay().querySelector(".tn-call-orb");
    var hintName = overlay().querySelector("[data-call-peer]");
    var chip = overlay().querySelector(".tn-call-chip");
    var brandSub = overlay().querySelector("[data-call-sub]");
    if (peer) {
      if (hintName) hintName.textContent = peer.name || labels().waiting;
      if (chip) chip.textContent = peer.name || "";
      if (brandSub) brandSub.textContent = peer.name || (live && live.video ? labels().camera : "Audio");
      if (orb && !orb.querySelector("img")) orb.textContent = peer.initials || "T";
      if (peer.has_avatar && peer.user_id) {
        fetchAvatar(peer.user_id).then(function (url) {
          if (!url || !orb) return;
          orb.innerHTML = '<img src="' + esc(url) + '" alt="">';
        });
      }
    }
  }

  function nativeMedia() {
    try {
      if (global.TalendusNative && typeof global.TalendusNative.requestMedia === "function") {
        global.TalendusNative.requestMedia();
      }
    } catch (e) {}
  }

  function sessionIsUsable() {
    if (!live || live.failed) return false;
    var el = document.getElementById("tn-call-overlay");
    if (!el || !el.classList.contains("is-on") || el.hasAttribute("hidden")) return false;
    if (!live.pc) return true;
    var state = live.pc.connectionState || "";
    return state !== "failed" && state !== "closed";
  }

  function post(kind, payload) {
    if (!live) return Promise.resolve();
    return request("/calls/" + encodeURIComponent(live.interviewId) + "/signal", {
      method: "POST",
      body: { kind: kind, payload: payload || {} }
    }).catch(function () {});
  }

  function attachVideos() {
    if (!live) return;
    var root = overlay();
    var remote = root.querySelector(".tn-call-remote");
    var local = root.querySelector(".tn-call-local");
    if (local && live.localStream) {
      local.srcObject = live.localStream;
      local.muted = true;
      local.playsInline = true;
      local.play().catch(function () {});
    }
    if (remote && live.remoteStream) {
      remote.srcObject = live.remoteStream;
      remote.playsInline = true;
      remote.muted = false;
      remote.play().catch(function () {});
    }
  }

  function asIce(payload) {
    if (!payload) return null;
    try {
      return payload instanceof RTCIceCandidate ? payload : new RTCIceCandidate(payload);
    } catch (e) {
      return null;
    }
  }

  function queueIce(pc, candidate) {
    var ice = asIce(candidate);
    if (!ice) return Promise.resolve();
    if (pc.remoteDescription) {
      return pc.addIceCandidate(ice).catch(function () {});
    }
    live.pendingIce = live.pendingIce || [];
    live.pendingIce.push(ice);
    return Promise.resolve();
  }

  function flushIce(pc) {
    var list = (live && live.pendingIce) || [];
    live.pendingIce = [];
    return Promise.all(list.map(function (c) { return pc.addIceCandidate(c).catch(function () {}); }));
  }

  function markLive() {
    if (!live) return;
    overlay().classList.add("is-live");
    if (!live.connectedAt) live.connectedAt = Date.now();
    setStatus(labels().live);
  }

  function bindPc(pc) {
    pc.onicecandidate = function (ev) {
      if (ev.candidate) post("ice", ev.candidate.toJSON ? ev.candidate.toJSON() : ev.candidate);
    };
    pc.ontrack = function (ev) {
      if (!live || live.pc !== pc) return;
      if (!live.remoteStream) live.remoteStream = new MediaStream();
      if (ev.track && !live.remoteStream.getTracks().some(function (t) { return t.id === ev.track.id; })) {
        live.remoteStream.addTrack(ev.track);
      }
      attachVideos();
      markLive();
    };
    pc.onconnectionstatechange = function () {
      if (!live || live.pc !== pc) return;
      if (pc.connectionState === "connected") {
        if (live.dropTimer) { clearTimeout(live.dropTimer); live.dropTimer = null; }
        live.restarting = false;
        markLive();
        return;
      }
      if (pc.connectionState === "failed") {
        setStatus(labels().reconnecting);
        if (!live.restarting) {
          live.restarting = true;
          live.offered = false;
          try { pc.restartIce(); } catch (e) {}
          maybeOffer(live.peers || [], true);
          if (live.dropTimer) clearTimeout(live.dropTimer);
          live.dropTimer = setTimeout(function () {
            if (live && live.pc === pc && pc.connectionState !== "connected") {
              live.failed = true;
              hangup(true);
            }
          }, 8000);
        }
        return;
      }
      if (pc.connectionState === "closed") {
        setStatus(labels().ended);
        return;
      }
      if (pc.connectionState === "disconnected") {
        setStatus(labels().reconnecting);
        if (live.dropTimer) clearTimeout(live.dropTimer);
        live.dropTimer = setTimeout(function () {
          if (live && live.pc === pc && pc.connectionState !== "connected") {
            live.offered = false;
            try { pc.restartIce(); } catch (e) {}
            maybeOffer(live.peers || [], true);
          }
        }, 2500);
      }
    };
  }

  function makePc(iceServers) {
    var pc = new RTCPeerConnection({
      iceServers: iceServers || [],
      iceTransportPolicy: "all",
      bundlePolicy: "max-bundle",
      iceCandidatePoolSize: 4
    });
    bindPc(pc);
    if (live.localStream) {
      live.localStream.getTracks().forEach(function (track) { pc.addTrack(track, live.localStream); });
    } else {
      try { pc.addTransceiver("audio", { direction: "sendrecv" }); } catch (e) {}
      if (live.video) {
        try { pc.addTransceiver("video", { direction: "sendrecv" }); } catch (e) {}
      }
    }
    return pc;
  }

  function replacePc() {
    if (!live) return null;
    try { if (live.pc) live.pc.close(); } catch (e) {}
    live.pendingIce = [];
    live.offered = false;
    live.offerTo = "";
    live.remoteStream = null;
    live.pc = makePc(live.iceServers || []);
    overlay().classList.remove("is-live");
    return live.pc;
  }

  function maybeOffer(peers, iceRestart) {
    if (!live || !live.pc) return;
    live.peers = peers || live.peers || [];
    paintPeerFace(remotePeer(live.peers));
    var others = live.peers.filter(function (p) { return p && !p.self; });
    var otherId = others.length ? String(others[0].user_id || "") : "";
    if (live.offerTo !== otherId) {
      live.offered = false;
      live.offerTo = otherId;
    }
    if (!others.length) return;
    if (!iceRestart && live.offered) return;
    if (String(live.selfId) > otherId) return;
    if (!iceRestart && live.pc.signalingState !== "stable") return;
    live.offered = true;
    var opts = { offerToReceiveAudio: true, offerToReceiveVideo: !!live.video };
    if (iceRestart) opts.iceRestart = true;
    live.pc.createOffer(opts)
      .then(function (offer) { return live.pc.setLocalDescription(offer); })
      .then(function () {
        var desc = live.pc.localDescription;
        return post("offer", { type: desc.type, sdp: desc.sdp });
      })
      .catch(function () { live.offered = false; });
  }

  function signalIsStale(row) {
    if (!live || !row || row.kind !== "hangup" || !row.created_at) return false;
    var when = Date.parse(row.created_at);
    if (!when) return false;
    return when < (live.joinedAt - 4000);
  }

  function handleSignal(row) {
    if (!live || !live.pc || !row) return Promise.resolve();
    if (signalIsStale(row)) return Promise.resolve();
    var kind = row.kind;
    var payload = row.payload || {};
    if (kind === "hangup") {
      setStatus(labels().ended);
      live.failed = true;
      return hangup(false);
    }
    if (kind === "offer") {
      if (!payload.type || !payload.sdp) return Promise.resolve();
      if (!live.pc || live.pc.signalingState === "closed") replacePc();
      else if (live.pc.signalingState === "have-local-offer") {
        if (String(live.selfId) < String(row.sender_id || "")) return Promise.resolve();
        replacePc();
      } else if (live.pc.signalingState !== "stable" && live.pc.currentRemoteDescription) {
        return Promise.resolve();
      }
      return live.pc.setRemoteDescription(new RTCSessionDescription(payload))
        .then(function () { return flushIce(live.pc); })
        .then(function () { return live.pc.createAnswer(); })
        .then(function (answer) { return live.pc.setLocalDescription(answer); })
        .then(function () {
          var desc = live.pc.localDescription;
          return post("answer", { type: desc.type, sdp: desc.sdp });
        })
        .catch(function () {});
    }
    if (kind === "answer") {
      if (!payload.type || !payload.sdp) return Promise.resolve();
      if (live.pc.signalingState !== "have-local-offer") return Promise.resolve();
      return live.pc.setRemoteDescription(new RTCSessionDescription(payload))
        .then(function () { return flushIce(live.pc); })
        .catch(function () {});
    }
    if (kind === "ice") {
      return queueIce(live.pc, payload);
    }
    return Promise.resolve();
  }

  function poll() {
    if (!live || live.failed) return;
    request("/calls/" + encodeURIComponent(live.interviewId) + "/signals" + (live.after ? "?after=" + encodeURIComponent(live.after) : ""))
      .then(function (json) {
        if (!live || live.failed) return;
        var data = dataOf(json) || {};
        live.peers = data.peers || live.peers || [];
        paintPeerFace(remotePeer(live.peers));
        var rows = data.signals || [];
        var chain = Promise.resolve();
        rows.forEach(function (row) {
          live.after = row.id;
          chain = chain.then(function () { return handleSignal(row); });
        });
        return chain.then(function () { maybeOffer(live.peers); });
      })
      .catch(function () {});
  }

  function heartbeat() {
    if (!live || live.failed) return;
    request("/calls/" + encodeURIComponent(live.interviewId) + "/join", {
      method: "POST",
      body: { video: !!live.video }
    }).then(function (json) {
      if (!live || live.failed) return;
      var data = dataOf(json) || {};
      live.peers = data.peers || live.peers || [];
      maybeOffer(live.peers);
    }).catch(function () {});
  }

  function tickClock() {
    if (!live) return;
    var el = overlay().querySelector("[data-call-timer]");
    if (!el) return;
    var start = live.connectedAt || live.joinedAt;
    el.textContent = formatClock(Date.now() - start);
  }

  function renderShell(title) {
    injectCss();
    var el = overlay();
    var t = labels();
    var mode = live && live.video ? t.camera : "Audio";
    var peer = remotePeer();
    el.innerHTML =
      '<div class="tn-call-top">' +
        '<div class="tn-call-brand"><span class="tn-call-mark" aria-hidden="true">T</span><div><strong>' + t.brand +
          '</strong><span data-call-sub>' + esc((peer && peer.name) || mode) + "</span></div></div>" +
        '<div class="tn-call-meta"><span class="tn-call-pill" data-call-timer>0:00</span>' +
          '<span class="tn-call-pill" data-call-pill>' + (title || t.connecting) + "</span></div>" +
      "</div>" +
      '<div class="tn-call-stage">' +
        '<video class="tn-call-remote" autoplay playsinline></video>' +
        '<video class="tn-call-local" autoplay muted playsinline></video>' +
        '<span class="tn-call-chip">' + esc((peer && peer.name) || "") + "</span>" +
        '<div class="tn-call-wait">' +
          '<div class="tn-call-orb-wrap"><span class="tn-call-ring"></span><span class="tn-call-ring"></span>' +
            '<div class="tn-call-orb" aria-hidden="true">' + esc((peer && peer.initials) || "T") + "</div></div>" +
          '<p class="tn-call-status">' + (title || t.connecting) + "</p>" +
          '<p class="tn-call-hint" data-call-peer>' + (live && live.video ? t.waiting : t.audioHint) + "</p>" +
        "</div>" +
      "</div>" +
      '<div class="tn-call-dock">' +
        '<button type="button" class="tn-call-btn is-mute" data-call-mute><i class="fa-solid fa-microphone" aria-hidden="true"></i>' + t.mute + "</button>" +
        (live && live.video ? '<button type="button" class="tn-call-btn is-cam" data-call-cam><i class="fa-solid fa-video" aria-hidden="true"></i>' + t.camera + "</button>" : "") +
        '<button type="button" class="tn-call-btn is-hang" data-call-hang><i class="fa-solid fa-phone-slash" aria-hidden="true"></i>' + t.hangup + "</button>" +
      "</div>";
    el.classList.add("is-on");
    el.classList.remove("is-live", "is-wrap");
    el.classList.toggle("is-audio", !(live && live.video));
    el.removeAttribute("hidden");
    el.querySelector("[data-call-mute]").onclick = function () {
      if (!live || !live.localStream) return;
      live.localStream.getAudioTracks().forEach(function (track) { track.enabled = !track.enabled; });
      var on = live.localStream.getAudioTracks().some(function (track) { return track.enabled; });
      var btn = el.querySelector("[data-call-mute]");
      btn.classList.toggle("is-off", !on);
      btn.innerHTML = '<i class="fa-solid ' + (on ? "fa-microphone" : "fa-microphone-slash") + '" aria-hidden="true"></i>' + (on ? t.mute : t.unmute);
    };
    var cam = el.querySelector("[data-call-cam]");
    if (cam) {
      cam.onclick = function () {
        if (!live || !live.localStream) return;
        live.localStream.getVideoTracks().forEach(function (track) { track.enabled = !track.enabled; });
        var on = live.localStream.getVideoTracks().some(function (track) { return track.enabled; });
        cam.classList.toggle("is-off", !on);
        cam.innerHTML = '<i class="fa-solid ' + (on ? "fa-video" : "fa-video-slash") + '" aria-hidden="true"></i>' + t.camera;
      };
    }
    el.querySelector("[data-call-hang]").onclick = function () { hangup(true); };
    paintPeerFace(peer);
  }

  function hideOverlay() {
    var el = document.getElementById("tn-call-overlay");
    if (el) {
      el.classList.remove("is-on", "is-live", "is-wrap");
      el.setAttribute("hidden", "");
      el.innerHTML = "";
    }
  }

  function showWrap(session) {
    injectCss();
    var el = overlay();
    var t = labels();
    el.classList.add("is-on", "is-wrap");
    el.classList.remove("is-live");
    el.removeAttribute("hidden");
    el.innerHTML =
      '<div class="tn-call-wrap"><div class="tn-call-wrap-card">' +
        '<span class="tn-call-mark" aria-hidden="true">T</span>' +
        "<h2>" + t.wrapTitle + "</h2>" +
        "<p>" + t.wrapHint + "</p>" +
        '<div class="tn-call-wrap-actions">' +
          '<button type="button" class="is-done" data-wrap="COMPLETED">' + t.wrapDone + "</button>" +
          '<button type="button" class="is-miss" data-wrap="NO_SHOW">' + t.wrapMiss + "</button>" +
          '<button type="button" class="is-cancel" data-wrap="CANCELLED">' + t.wrapCancel + "</button>" +
        "</div>" +
        '<button type="button" class="tn-call-wrap-skip" data-wrap-skip>' + t.wrapSkip + "</button>" +
      "</div></div>";
    el.querySelectorAll("[data-wrap]").forEach(function (btn) {
      btn.onclick = function () {
        var status = btn.getAttribute("data-wrap");
        request("/interviews/" + encodeURIComponent(session.interviewId) + "/status", {
          method: "POST",
          body: { status: status }
        }).then(function () {
          hideOverlay();
          if (typeof session.onWrapped === "function") session.onWrapped(status);
        }).catch(function () {
          hideOverlay();
        });
      };
    });
    el.querySelector("[data-wrap-skip]").onclick = function () { hideOverlay(); };
  }

  function stopTracks(stream) {
    if (!stream) return;
    stream.getTracks().forEach(function (track) {
      try { track.stop(); } catch (e) {}
    });
  }

  function hangup(notifyRemote, opts) {
    opts = opts || {};
    var session = live;
    live = null;
    if (session) {
      clearInterval(session.pollTimer);
      clearInterval(session.beatTimer);
      clearInterval(session.clockTimer);
      if (session.dropTimer) clearTimeout(session.dropTimer);
      try { if (session.pc) session.pc.close(); } catch (e) {}
      stopTracks(session.localStream);
      if (notifyRemote && session.interviewId) {
        request("/calls/" + encodeURIComponent(session.interviewId) + "/hangup", { method: "POST" }).catch(function () {});
      }
      if (typeof session.onHangup === "function") {
        try { session.onHangup(); } catch (e) {}
      }
      if (session.canWrap && session.interviewId && !opts.silent) {
        showWrap(session);
        return Promise.resolve();
      }
    }
    hideOverlay();
    return Promise.resolve();
  }

  function getMedia(constraints, attempt) {
    attempt = attempt || 0;
    return navigator.mediaDevices.getUserMedia(constraints).catch(function (err) {
      var native = false;
      try { native = !!(global.TalendusNative && global.TalendusNative.requestMedia); } catch (e) {}
      var max = native ? 12 : 4;
      if (attempt >= max) throw err;
      return new Promise(function (resolve, reject) {
        setTimeout(function () {
          getMedia(constraints, attempt + 1).then(resolve, reject);
        }, native ? 350 : 220 * (attempt + 1));
      });
    });
  }

  function showCallError(message, retryOpts) {
    var el = overlay();
    var t = labels();
    injectCss();
    el.classList.add("is-on");
    el.removeAttribute("hidden");
    el.innerHTML = '<p class="tn-call-err">' + message + '</p><div class="tn-call-dock">' +
      (retryOpts ? '<button type="button" class="tn-call-btn is-retry" data-call-retry>' + t.retry + "</button>" : "") +
      '<button type="button" class="tn-call-btn is-hang" data-call-hang>' + t.hangup + "</button></div>";
    var retry = el.querySelector("[data-call-retry]");
    if (retry && retryOpts) {
      retry.onclick = function () { start(retryOpts); };
    }
    el.querySelector("[data-call-hang]").onclick = function () { hangup(false); };
  }

  function joinErrorMessage(err) {
    var t = labels();
    var code = (err && (err.code || err.error)) || "";
    var msg = (err && err.message) || "";
    if (code === "CALL_WAITING_FOR_HOST" || /ouvert|lancé|recruteur/i.test(msg)) return t.waitHost;
    if (code === "CALL_NOT_AVAILABLE") return t.unavailable;
    if (code === "CALL_CANNOT_START" || code === "FORBIDDEN") return t.forbidden;
    if (code === "NotAllowedError" || code === "NotFoundError" || /media|permission|NotAllowed|NotFound/i.test(msg)) return t.micDenied;
    if (err && err.status === 409) return msg || t.waitHost;
    if (err && (err.status === 403 || err.status === 404)) return t.forbidden;
    return "";
  }

  function start(opts) {
    opts = opts || {};
    if (!api() || typeof RTCPeerConnection === "undefined" || !navigator.mediaDevices) {
      showCallError(labels().unsupported);
      return Promise.resolve(false);
    }
    var interviewId = opts.interviewId;
    if (!interviewId) return Promise.resolve(false);
    if (live && live.interviewId === interviewId && sessionIsUsable()) {
      return Promise.resolve(true);
    }
    var notifyRemote = !!(live && live.interviewId);
    return hangup(notifyRemote, { silent: true }).then(function () {
      nativeMedia();
      live = {
        interviewId: interviewId,
        video: !!opts.video,
        onHangup: opts.onHangup,
        onWrapped: opts.onWrapped,
        canWrap: !!opts.canWrap,
        after: "",
        pendingIce: [],
        offered: false,
        offerTo: "",
        failed: false,
        restarting: false,
        joinedAt: Date.now(),
        iceServers: [],
        peers: []
      };
      renderShell(labels().connecting);
      var constraints = { audio: true, video: live.video ? { facingMode: "user", width: { ideal: 960 }, height: { ideal: 720 } } : false };
      return new Promise(function (resolve) { setTimeout(resolve, 180); }).then(function () {
        return getMedia(constraints);
      }).catch(function () {
        if (!live || !live.video) throw new Error("media");
        live.video = false;
        overlay().classList.add("is-audio");
        var hint = overlay().querySelector(".tn-call-hint");
        if (hint) hint.textContent = labels().audioHint;
        return getMedia({ audio: true, video: false });
      }).then(function (stream) {
        if (!live) {
          stopTracks(stream);
          return false;
        }
        live.localStream = stream;
        attachVideos();
        return request("/calls/" + encodeURIComponent(interviewId) + "/join", {
          method: "POST",
          body: { video: !!live.video }
        });
      }).then(function (json) {
        if (!live) return false;
        var data = dataOf(json) || {};
        live.selfId = data.self_id;
        live.iceServers = data.ice_servers || [];
        live.joinedAt = Date.now();
        live.peers = data.peers || [];
        live.pc = makePc(live.iceServers);
        attachVideos();
        setStatus(labels().waiting);
        paintPeerFace(remotePeer(live.peers));
        maybeOffer(live.peers);
        live.pollTimer = setInterval(poll, 450);
        live.beatTimer = setInterval(heartbeat, 6000);
        live.clockTimer = setInterval(tickClock, 1000);
        poll();
        return true;
      }).catch(function (err) {
        var retry = { interviewId: interviewId, video: !!opts.video, onHangup: opts.onHangup, onWrapped: opts.onWrapped, canWrap: !!opts.canWrap };
        var message = joinErrorMessage(err) || labels().micDenied;
        var session = live;
        live = null;
        if (session) {
          clearInterval(session.pollTimer);
          clearInterval(session.beatTimer);
          clearInterval(session.clockTimer);
          try { if (session.pc) session.pc.close(); } catch (e) {}
          stopTracks(session.localStream);
        }
        showCallError(message, retry);
        return false;
      });
    });
  }

  global.TalendusCall = {
    start: start,
    hangup: function () { return hangup(true); },
    isLive: function (interviewId) {
      return !!(live && sessionIsUsable() && (!interviewId || live.interviewId === interviewId));
    }
  };
})(window);
