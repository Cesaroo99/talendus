(function (global) {
  var STYLE_ID = "tn-call-css";
  var CSS = "#tn-call-overlay{display:none;position:fixed;inset:0;z-index:240;background:radial-gradient(120% 80% at 50% 0%,#16365f 0%,#0b1f3a 46%,#06111f 100%);color:#fff;font-family:inherit}" +
    "#tn-call-overlay.is-on{display:flex;flex-direction:column}" +
    "#tn-call-overlay .tn-call-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 20px 8px;padding-top:calc(16px + env(safe-area-inset-top))}" +
    "#tn-call-overlay .tn-call-brand{display:flex;align-items:center;gap:10px;min-width:0}" +
    "#tn-call-overlay .tn-call-mark{width:36px;height:36px;border-radius:10px;background:#e87024;display:inline-flex;align-items:center;justify-content:center;font-weight:800}" +
    "#tn-call-overlay .tn-call-brand strong{display:block;font-size:15px}" +
    "#tn-call-overlay .tn-call-brand span{display:block;font-size:12px;opacity:.72}" +
    "#tn-call-overlay .tn-call-pill{border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 12px;font-size:12px;font-weight:700;letter-spacing:.02em;background:rgba(255,255,255,.08)}" +
    "#tn-call-overlay .tn-call-stage{flex:1;position:relative;margin:8px 16px 0;border-radius:24px;overflow:hidden;background:#04101c;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06)}" +
    "#tn-call-overlay video{object-fit:cover;background:#000}" +
    "#tn-call-overlay .tn-call-remote{width:100%;height:100%}" +
    "#tn-call-overlay .tn-call-local{position:absolute;right:14px;top:14px;width:28%;max-width:148px;aspect-ratio:3/4;border-radius:16px;border:2px solid rgba(255,255,255,.45);z-index:2;box-shadow:0 10px 24px rgba(0,0,0,.35)}" +
    "#tn-call-overlay.is-audio .tn-call-local{display:none}" +
    "#tn-call-overlay .tn-call-wait{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center;padding:24px;z-index:1}" +
    "#tn-call-overlay .tn-call-orb{width:112px;height:112px;border-radius:50%;background:linear-gradient(160deg,#e87024,#c45312);display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800;box-shadow:0 0 0 12px rgba(232,112,36,.18)}" +
    "#tn-call-overlay.is-live .tn-call-wait{display:none}" +
    "#tn-call-overlay .tn-call-status{margin:0;font-weight:700;font-size:18px}" +
    "#tn-call-overlay .tn-call-hint{margin:0;opacity:.72;font-size:14px;max-width:320px}" +
    "#tn-call-overlay .tn-call-bar{display:flex;gap:14px;justify-content:center;align-items:flex-end;padding:18px 16px calc(22px + env(safe-area-inset-bottom))}" +
    "#tn-call-overlay .tn-call-btn{width:58px;height:58px;border:0;border-radius:50%;color:#fff;font-weight:800;cursor:pointer;display:inline-flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:10px;letter-spacing:.02em}" +
    "#tn-call-overlay .tn-call-btn i{font-size:18px}" +
    "#tn-call-overlay .tn-call-btn.is-mute{background:#3d4f66}" +
    "#tn-call-overlay .tn-call-btn.is-cam{background:#16365f}" +
    "#tn-call-overlay .tn-call-btn.is-hang{background:#c62828;min-width:132px;border-radius:29px;width:auto;padding:0 22px;flex-direction:row;gap:8px;font-size:14px}" +
    "#tn-call-overlay .tn-call-btn.is-retry{background:#e87024}" +
    "#tn-call-overlay .tn-call-err{padding:48px 24px 12px;text-align:center;font-size:18px;font-weight:700;max-width:420px;margin:auto}";

  var live = null;

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

  function labels() {
    var en = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    return en ? {
      connecting: "Connecting…",
      waiting: "Waiting for the other person…",
      live: "Connected",
      ended: "Call ended",
      mute: "Mute",
      unmute: "Unmute",
      camera: "Camera",
      hangup: "Hang up",
      micDenied: "Allow the microphone (and camera for video) to join the interview.",
      unsupported: "This device cannot place an in-app call.",
      waitHost: "The consultant has not opened the room yet.",
      brand: "Talendus interview",
      audioHint: "Audio only. Stay on this screen — the consultant will join here.",
      unavailable: "This interview cannot be taken in the app.",
      forbidden: "You cannot join this call.",
      retry: "Try again"
    } : {
      connecting: "Connexion…",
      waiting: "En attente de l’autre personne…",
      live: "En ligne",
      ended: "Appel terminé",
      mute: "Muet",
      unmute: "Son",
      camera: "Caméra",
      hangup: "Raccrocher",
      micDenied: "Autorisez le micro (et la caméra en visio) pour rejoindre l’entretien.",
      unsupported: "Cet appareil ne peut pas passer d’appel dans l’appli.",
      waitHost: "Le conseiller n’a pas encore ouvert la salle.",
      brand: "Entretien Talendus",
      audioHint: "Audio seulement. Restez sur cet écran — le conseiller vous rejoint ici.",
      unavailable: "Cet entretien ne peut pas se faire dans l’appli.",
      forbidden: "Vous ne pouvez pas rejoindre cet appel.",
      retry: "Relancer"
    };
  }

  function setStatus(text) {
    if (!live) return;
    live.statusText = text;
    var el = overlay().querySelector(".tn-call-status");
    if (el) el.textContent = text;
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
    return state !== "failed" && state !== "closed" && state !== "disconnected";
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
      remote.play().catch(function () {});
    }
  }

  function queueIce(pc, candidate) {
    if (!candidate) return Promise.resolve();
    if (pc.remoteDescription) {
      return pc.addIceCandidate(candidate).catch(function () {});
    }
    live.pendingIce = live.pendingIce || [];
    live.pendingIce.push(candidate);
    return Promise.resolve();
  }

  function flushIce(pc) {
    var list = (live && live.pendingIce) || [];
    live.pendingIce = [];
    return Promise.all(list.map(function (c) { return pc.addIceCandidate(c).catch(function () {}); }));
  }

  function bindPc(pc) {
    pc.onicecandidate = function (ev) {
      if (ev.candidate) post("ice", ev.candidate.toJSON());
    };
    pc.ontrack = function (ev) {
      if (!live || live.pc !== pc) return;
      live.remoteStream = ev.streams[0] || (ev.track ? new MediaStream([ev.track]) : null);
      attachVideos();
      overlay().classList.add("is-live");
      setStatus(labels().live);
    };
    pc.onconnectionstatechange = function () {
      if (!live || live.pc !== pc) return;
      if (pc.connectionState === "connected") {
        if (live.dropTimer) { clearTimeout(live.dropTimer); live.dropTimer = null; }
        overlay().classList.add("is-live");
        setStatus(labels().live);
        return;
      }
      if (pc.connectionState === "failed" || pc.connectionState === "closed") {
        setStatus(labels().ended);
        live.failed = true;
        if (live.dropTimer) clearTimeout(live.dropTimer);
        live.dropTimer = setTimeout(function () {
          if (live && live.pc === pc) hangup(true);
        }, 1200);
      }
      if (pc.connectionState === "disconnected") {
        setStatus(labels().ended);
        if (live.dropTimer) clearTimeout(live.dropTimer);
        live.dropTimer = setTimeout(function () {
          if (live && live.pc === pc && pc.connectionState !== "connected") {
            live.failed = true;
            hangup(true);
          }
        }, 6000);
      }
    };
  }

  function makePc(iceServers) {
    var pc = new RTCPeerConnection({ iceServers: iceServers || [] });
    bindPc(pc);
    if (live.localStream) {
      live.localStream.getTracks().forEach(function (track) { pc.addTrack(track, live.localStream); });
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

  function maybeOffer(peers) {
    if (!live || !live.pc) return;
    var others = (peers || []).filter(function (p) { return p && !p.self; });
    var otherId = others.length ? String(others[0].user_id || "") : "";
    if (live.offerTo !== otherId) {
      live.offered = false;
      live.offerTo = otherId;
    }
    if (live.offered || !others.length) return;
    if (String(live.selfId) > otherId) return;
    live.offered = true;
    live.pc.createOffer({ offerToReceiveAudio: true, offerToReceiveVideo: !!live.video })
      .then(function (offer) { return live.pc.setLocalDescription(offer); })
      .then(function () {
        var desc = live.pc.localDescription;
        return post("offer", { type: desc.type, sdp: desc.sdp });
      })
      .catch(function () { live.offered = false; });
  }

  function signalIsStale(row) {
    if (!live || !row || !row.created_at) return false;
    var when = Date.parse(row.created_at);
    if (!when) return false;
    return when < (live.joinedAt - 1500);
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
      if (live.pc.signalingState === "closed" || live.pc.currentRemoteDescription) {
        replacePc();
      }
      return live.pc.setRemoteDescription(new RTCSessionDescription(payload))
        .then(function () { return flushIce(live.pc); })
        .then(function () { return live.pc.createAnswer(); })
        .then(function (answer) { return live.pc.setLocalDescription(answer); })
        .then(function () {
          var desc = live.pc.localDescription;
          return post("answer", { type: desc.type, sdp: desc.sdp });
        })
        .catch(function () { return replacePc(); });
    }
    if (kind === "answer") {
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
        var rows = data.signals || [];
        var chain = Promise.resolve();
        rows.forEach(function (row) {
          live.after = row.id;
          chain = chain.then(function () { return handleSignal(row); });
        });
        return chain.then(function () { maybeOffer(data.peers || []); });
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
      maybeOffer(data.peers || []);
    }).catch(function () {});
  }

  function renderShell(title) {
    injectCss();
    var el = overlay();
    var t = labels();
    var mode = live && live.video ? (t.camera) : "Audio";
    el.innerHTML =
      '<div class="tn-call-top">' +
        '<div class="tn-call-brand"><span class="tn-call-mark" aria-hidden="true">T</span><div><strong>' + t.brand + "</strong><span>" + mode + "</span></div></div>" +
        '<span class="tn-call-pill">' + (title || t.connecting) + "</span>" +
      "</div>" +
      '<div class="tn-call-stage">' +
        '<video class="tn-call-remote" autoplay playsinline></video>' +
        '<video class="tn-call-local" autoplay muted playsinline></video>' +
        '<div class="tn-call-wait">' +
          '<div class="tn-call-orb" aria-hidden="true">T</div>' +
          '<p class="tn-call-status">' + (title || t.connecting) + "</p>" +
          '<p class="tn-call-hint">' + (live && live.video ? t.waiting : t.audioHint) + "</p>" +
        "</div>" +
      "</div>" +
      '<div class="tn-call-bar">' +
        '<button type="button" class="tn-call-btn is-mute" data-call-mute><i class="fa-solid fa-microphone" aria-hidden="true"></i>' + t.mute + "</button>" +
        (live && live.video ? '<button type="button" class="tn-call-btn is-cam" data-call-cam><i class="fa-solid fa-video" aria-hidden="true"></i>' + t.camera + "</button>" : "") +
        '<button type="button" class="tn-call-btn is-hang" data-call-hang><i class="fa-solid fa-phone-slash" aria-hidden="true"></i>' + t.hangup + "</button>" +
      "</div>";
    el.classList.add("is-on");
    el.classList.remove("is-live");
    el.classList.toggle("is-audio", !(live && live.video));
    el.removeAttribute("hidden");
    el.querySelector("[data-call-mute]").onclick = function () {
      if (!live || !live.localStream) return;
      live.localStream.getAudioTracks().forEach(function (track) { track.enabled = !track.enabled; });
      var on = live.localStream.getAudioTracks().some(function (track) { return track.enabled; });
      el.querySelector("[data-call-mute]").innerHTML = '<i class="fa-solid ' + (on ? "fa-microphone" : "fa-microphone-slash") + '" aria-hidden="true"></i>' + (on ? t.mute : t.unmute);
    };
    var cam = el.querySelector("[data-call-cam]");
    if (cam) {
      cam.onclick = function () {
        if (!live || !live.localStream) return;
        live.localStream.getVideoTracks().forEach(function (track) { track.enabled = !track.enabled; });
      };
    }
    el.querySelector("[data-call-hang]").onclick = function () { hangup(true); };
  }

  function stopTracks(stream) {
    if (!stream) return;
    stream.getTracks().forEach(function (track) {
      try { track.stop(); } catch (e) {}
    });
  }

  function hangup(notifyRemote) {
    var session = live;
    live = null;
    if (session) {
      clearInterval(session.pollTimer);
      clearInterval(session.beatTimer);
      if (session.dropTimer) clearTimeout(session.dropTimer);
      try { if (session.pc) session.pc.close(); } catch (e) {}
      stopTracks(session.localStream);
      if (notifyRemote && session.interviewId) {
        request("/calls/" + encodeURIComponent(session.interviewId) + "/hangup", { method: "POST" }).catch(function () {});
      }
      if (typeof session.onHangup === "function") {
        try { session.onHangup(); } catch (e) {}
      }
    }
    var el = document.getElementById("tn-call-overlay");
    if (el) {
      el.classList.remove("is-on");
      el.setAttribute("hidden", "");
      el.innerHTML = "";
    }
    return Promise.resolve();
  }

  function getMedia(constraints, attempt) {
    attempt = attempt || 0;
    return navigator.mediaDevices.getUserMedia(constraints).catch(function (err) {
      var native = false;
      try { native = !!(global.TalendusNative && global.TalendusNative.requestMedia); } catch (e) {}
      if (!native || attempt >= 12) throw err;
      return new Promise(function (resolve, reject) {
        setTimeout(function () {
          getMedia(constraints, attempt + 1).then(resolve, reject);
        }, 350);
      });
    });
  }

  function showCallError(message, retryOpts) {
    var el = overlay();
    var t = labels();
    injectCss();
    el.classList.add("is-on");
    el.removeAttribute("hidden");
    el.innerHTML = '<p class="tn-call-err">' + message + '</p><div class="tn-call-bar">' +
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
    if (code === "CALL_WAITING_FOR_HOST" || /ouvert/.test(msg)) return t.waitHost;
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
    return hangup(notifyRemote).then(function () {
      nativeMedia();
      live = {
        interviewId: interviewId,
        video: !!opts.video,
        onHangup: opts.onHangup,
        after: "",
        pendingIce: [],
        offered: false,
        offerTo: "",
        failed: false,
        joinedAt: Date.now(),
        iceServers: []
      };
      renderShell(labels().connecting);
      var constraints = { audio: true, video: live.video ? { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } } : false };
      return getMedia(constraints).catch(function () {
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
        live.pc = makePc(live.iceServers);
        attachVideos();
        setStatus(labels().waiting);
        maybeOffer(data.peers || []);
        live.pollTimer = setInterval(poll, 1000);
        live.beatTimer = setInterval(heartbeat, 8000);
        poll();
        return true;
      }).catch(function (err) {
        var retry = { interviewId: interviewId, video: !!opts.video, onHangup: opts.onHangup };
        var message = joinErrorMessage(err) || labels().micDenied;
        var session = live;
        live = null;
        if (session) {
          clearInterval(session.pollTimer);
          clearInterval(session.beatTimer);
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
