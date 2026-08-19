(function (global) {
  var STYLE_ID = "tn-call-css";
  var CSS = "#tn-call-overlay{display:none;position:fixed;inset:0;z-index:80;background:#071422;color:#fff;font-family:inherit}" +
    "#tn-call-overlay.is-on{display:flex;flex-direction:column}" +
    "#tn-call-overlay .tn-call-stage{flex:1;position:relative;background:#04101c;overflow:hidden}" +
    "#tn-call-overlay video{object-fit:cover;background:#000}" +
    "#tn-call-overlay .tn-call-remote{width:100%;height:100%}" +
    "#tn-call-overlay .tn-call-local{position:absolute;right:14px;top:14px;width:28%;max-width:140px;aspect-ratio:3/4;border-radius:16px;border:2px solid rgba(255,255,255,.4);z-index:2}" +
    "#tn-call-overlay.is-audio .tn-call-local{display:none}" +
    "#tn-call-overlay .tn-call-status{position:absolute;left:16px;right:16px;bottom:18px;text-align:center;z-index:2;font-weight:700}" +
    "#tn-call-overlay .tn-call-bar{display:flex;gap:12px;justify-content:center;align-items:center;padding:18px 16px calc(18px + env(safe-area-inset-bottom));background:#0b1f3a}" +
    "#tn-call-overlay .tn-call-btn{width:56px;height:56px;border:0;border-radius:50%;color:#fff;font-weight:800;cursor:pointer}" +
    "#tn-call-overlay .tn-call-btn.is-mute{background:#3d4f66}" +
    "#tn-call-overlay .tn-call-btn.is-cam{background:#16365f}" +
    "#tn-call-overlay .tn-call-btn.is-hang{background:#c62828;min-width:120px;border-radius:28px;width:auto;padding:0 18px}" +
    "#tn-call-overlay .tn-call-err{padding:24px;text-align:center}";

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
      unsupported: "This device cannot place an in-app call."
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
      unsupported: "Cet appareil ne peut pas passer d’appel dans l’appli."
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

  function makePc(iceServers) {
    var pc = new RTCPeerConnection({ iceServers: iceServers || [] });
    pc.onicecandidate = function (ev) {
      if (ev.candidate) post("ice", ev.candidate.toJSON());
    };
    pc.ontrack = function (ev) {
      live.remoteStream = ev.streams[0] || (ev.track ? new MediaStream([ev.track]) : null);
      attachVideos();
      setStatus(labels().live);
    };
    pc.onconnectionstatechange = function () {
      if (!live) return;
      if (pc.connectionState === "connected") setStatus(labels().live);
      if (pc.connectionState === "disconnected" || pc.connectionState === "failed") setStatus(labels().ended);
    };
    if (live.localStream) {
      live.localStream.getTracks().forEach(function (track) { pc.addTrack(track, live.localStream); });
    }
    return pc;
  }

  function maybeOffer(peers) {
    if (!live || live.offered || !live.pc) return;
    var others = (peers || []).filter(function (p) { return p && !p.self; });
    if (!others.length) return;
    var otherId = others[0].user_id;
    if (String(live.selfId) > String(otherId)) return;
    live.offered = true;
    live.pc.createOffer({ offerToReceiveAudio: true, offerToReceiveVideo: !!live.video })
      .then(function (offer) { return live.pc.setLocalDescription(offer); })
      .then(function () {
        var desc = live.pc.localDescription;
        return post("offer", { type: desc.type, sdp: desc.sdp });
      })
      .catch(function () { live.offered = false; });
  }

  function handleSignal(row) {
    if (!live || !live.pc || !row) return Promise.resolve();
    var kind = row.kind;
    var payload = row.payload || {};
    if (kind === "hangup") {
      setStatus(labels().ended);
      return hangup(false);
    }
    if (kind === "offer") {
      return live.pc.setRemoteDescription(new RTCSessionDescription(payload))
        .then(function () { return flushIce(live.pc); })
        .then(function () { return live.pc.createAnswer(); })
        .then(function (answer) { return live.pc.setLocalDescription(answer); })
        .then(function () {
          var desc = live.pc.localDescription;
          return post("answer", { type: desc.type, sdp: desc.sdp });
        });
    }
    if (kind === "answer") {
      return live.pc.setRemoteDescription(new RTCSessionDescription(payload))
        .then(function () { return flushIce(live.pc); });
    }
    if (kind === "ice") {
      return queueIce(live.pc, payload);
    }
    return Promise.resolve();
  }

  function poll() {
    if (!live) return;
    request("/calls/" + encodeURIComponent(live.interviewId) + "/signals" + (live.after ? "?after=" + encodeURIComponent(live.after) : ""))
      .then(function (json) {
        if (!live) return;
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
    if (!live) return;
    request("/calls/" + encodeURIComponent(live.interviewId) + "/join", {
      method: "POST",
      body: { video: !!live.video }
    }).then(function (json) {
      if (!live) return;
      var data = dataOf(json) || {};
      maybeOffer(data.peers || []);
    }).catch(function () {});
  }

  function renderShell(title) {
    injectCss();
    var el = overlay();
    var t = labels();
    el.innerHTML =
      '<div class="tn-call-stage">' +
        '<video class="tn-call-remote" autoplay playsinline></video>' +
        '<video class="tn-call-local" autoplay muted playsinline></video>' +
        '<p class="tn-call-status">' + (title || t.connecting) + "</p>" +
      "</div>" +
      '<div class="tn-call-bar">' +
        '<button type="button" class="tn-call-btn is-mute" data-call-mute>' + t.mute + "</button>" +
        (live && live.video ? '<button type="button" class="tn-call-btn is-cam" data-call-cam>' + t.camera + "</button>" : "") +
        '<button type="button" class="tn-call-btn is-hang" data-call-hang>' + t.hangup + "</button>" +
      "</div>";
    el.classList.add("is-on");
    el.classList.toggle("is-audio", !(live && live.video));
    el.removeAttribute("hidden");
    el.querySelector("[data-call-mute]").onclick = function () {
      if (!live || !live.localStream) return;
      live.localStream.getAudioTracks().forEach(function (track) { track.enabled = !track.enabled; });
      var on = live.localStream.getAudioTracks().some(function (track) { return track.enabled; });
      el.querySelector("[data-call-mute]").textContent = on ? t.mute : t.unmute;
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
      try { if (session.pc) session.pc.close(); } catch (e) {}
      stopTracks(session.localStream);
      if (notifyRemote) {
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

  function mediaError() {
    var el = overlay();
    injectCss();
    el.classList.add("is-on");
    el.removeAttribute("hidden");
    el.innerHTML = '<p class="tn-call-err">' + labels().micDenied + '</p><div class="tn-call-bar"><button type="button" class="tn-call-btn is-hang" data-call-hang>' + labels().hangup + "</button></div>";
    el.querySelector("[data-call-hang]").onclick = function () { hangup(false); };
  }

  function start(opts) {
    opts = opts || {};
    if (!api() || typeof RTCPeerConnection === "undefined" || !navigator.mediaDevices) {
      injectCss();
      var el = overlay();
      el.classList.add("is-on");
      el.removeAttribute("hidden");
      el.innerHTML = '<p class="tn-call-err">' + labels().unsupported + "</p>";
      return Promise.resolve(false);
    }
    var interviewId = opts.interviewId;
    if (!interviewId) return Promise.resolve(false);
    if (live && live.interviewId === interviewId) return Promise.resolve(true);
    return hangup(false).then(function () {
      nativeMedia();
      live = {
        interviewId: interviewId,
        video: !!opts.video,
        onHangup: opts.onHangup,
        after: "",
        pendingIce: [],
        offered: false
      };
      renderShell(labels().connecting);
      var constraints = { audio: true, video: live.video ? { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } } : false };
      return getMedia(constraints).catch(function () {
        if (!live.video) throw new Error("media");
        live.video = false;
        overlay().classList.add("is-audio");
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
        live.pc = makePc(data.ice_servers);
        attachVideos();
        setStatus(labels().waiting);
        maybeOffer(data.peers || []);
        live.pollTimer = setInterval(poll, 1000);
        live.beatTimer = setInterval(heartbeat, 8000);
        poll();
        return true;
      }).catch(function () {
        mediaError();
        return false;
      });
    });
  }

  global.TalendusCall = {
    start: start,
    hangup: function () { return hangup(true); },
    isLive: function (interviewId) {
      return !!(live && (!interviewId || live.interviewId === interviewId));
    }
  };
})(window);
