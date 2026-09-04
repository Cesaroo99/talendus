/* Talendus Admin — application SPA */
(function () {
  const S = () => TLStore.get();
  const U = TLUI;
  const $ = TLUI.$;
  const app = document.getElementById("app");
  let page = 1, sortKey = "lastActivity", sortDir = "desc", selected = new Set();
  let filters = {};
  let period = "mois";
  let analyticsRecruiter = "";
  let analyticsSector = "";
  let contentTab = "pages";
  let financeTab = "factures";
  let detailTab = "profil";

  const CAND_STATUS_TO_APP = {
    nouveau: "SUBMITTED",
    "a-contacter": "UNDER_REVIEW",
    qualifie: "SHORTLISTED",
    entretien: "INTERVIEW",
    presente: "SHORTLISTED",
    "entretien-client": "SECOND_INTERVIEW",
    offre: "OFFER_SENT",
    place: "HIRED",
    refuse: "REJECTED",
    inactif: "WITHDRAWN"
  };
  const HIRING_STATUSES = [
    ["REQUEST_SUBMITTED", "Besoin transmis"],
    ["UNDER_REVIEW", "Analyse en cours"],
    ["CLIENT_CONTACTED", "Échange avec l’entreprise"],
    ["NEEDS_CONFIRMED", "Profil défini"],
    ["JOB_BEING_PREPARED", "Offre en préparation"],
    ["CLIENT_VALIDATION", "Validation demandée"],
    ["JOB_PUBLISHED", "Recherche lancée"],
    ["SOURCING", "Recherche en cours"],
    ["SCREENING", "Présélection"],
    ["INTERVIEWS", "Entretiens Talendus"],
    ["SHORTLIST", "Shortlist"],
    ["CLIENT_REVIEW", "Profils à consulter"],
    ["HIRING", "Décision en cours"],
    ["CLOSED", "Recrutement terminé"]
  ];
  const JOB_ACT_API = { publiee: "publish", suspendue: "pause", archivee: "archive" };
  const JOB_CONTRACTS = ["Permanent", "Temporaire", "Contractuel", "Saisonnier", "Stage"];
  const JOB_HOURS = ["Temps plein", "Temps partiel", "Sur appel", "4 jours / 3"];
  const JOB_SHIFTS = ["Quart de jour", "Quart de soir", "Quart de nuit", "Quarts rotatifs", "Fin de semaine", "Quarts brisés"];

  function jobSelect(label, name, values, selected) {
    return U.field(label, name, { options: values, selected: selected || values[0] }, "select");
  }

  function jobVocabFields(job) {
    job = job || {};
    return jobSelect("Type de contrat", "contract_type", JOB_CONTRACTS, job.contract_type || job.type) +
      jobSelect("Horaire", "schedule", JOB_HOURS, job.schedule) +
      jobSelect("Quart", "shift", JOB_SHIFTS, job.shift);
  }

  function live() {
    return !!(window.TalendusAPI && TLStore.isLive && TLStore.isLive());
  }

  function api() {
    return window.TalendusAPI;
  }

  function invoiceApiId(i) {
    return (i && (i.apiId || i.id)) || "";
  }

  function firstId(list) {
    return list && list.length ? list[0].id : "";
  }

  function candLangs(c) {
    return Array.isArray(c && c.languages) ? c.languages : [];
  }

  async function setCandidateStatus(cand, next) {
    if (!cand) return;
    if (live()) {
      if (cand.applicationId && CAND_STATUS_TO_APP[next]) {
        await api().request("/applications/" + cand.applicationId + "/status", { method: "POST", body: { status: CAND_STATUS_TO_APP[next] } });
      } else {
        await api().request("/admin/candidates/" + cand.id, { method: "PATCH", body: { pipeline_status: next } });
      }
      await refreshLive();
      return;
    }
    TLStore.update(function (st) {
      var row = st.candidates.find(function (c) { return c.id === cand.id; });
      if (row) row.status = next;
    });
  }

  async function refreshLive() {
    if (TLStore.hydrateFromApi) await TLStore.hydrateFromApi();
  }

  function callButtons(i) {
    if (!i || !i.in_app_call) return "";
    var html = '<span class="int-call-help">1. Lancez l’audio ou la visio — 2. Le candidat voit alors Rejoindre — 3. Raccrochez pour refermer la salle.</span>';
    if (!i.host_in_call) {
      html += ' <button type="button" class="btn btn-ghost btn-sm" data-open-call="' + U.esc(i.id) + '">Prévenir le candidat</button>';
    }
    html += ' <button type="button" class="btn btn-ghost btn-sm" data-join-call="' + U.esc(i.id) + '" data-video="0">Lancer audio</button>';
    if (i.call_video !== false) {
      html += ' <button type="button" class="btn btn-sm btn-orange" data-join-call="' + U.esc(i.id) + '" data-video="1">Lancer visio</button>';
    }
    html += i.candidate_can_start
      ? ' <button type="button" class="btn btn-ghost btn-sm" data-call-perm="' + U.esc(i.id) + '" data-allow="0">Candidat : lancer retiré</button>'
      : ' <button type="button" class="btn btn-ghost btn-sm" data-call-perm="' + U.esc(i.id) + '" data-allow="1">Autoriser le candidat à lancer</button>';
    html += ' <button type="button" class="btn btn-ghost btn-sm" data-int-close="' + U.esc(i.id) + '" data-status="COMPLETED">Terminé</button>';
    html += ' <button type="button" class="btn btn-ghost btn-sm" data-int-close="' + U.esc(i.id) + '" data-status="NO_SHOW">Absent</button>';
    html += ' <button type="button" class="btn btn-ghost btn-sm" data-int-close="' + U.esc(i.id) + '" data-status="CANCELLED">Annulé</button>';
    return html;
  }

  function adminHash(href) {
    if (!href) return "#/notifications";
    var i = String(href).indexOf("#");
    if (i >= 0) return href.slice(i);
    if (String(href).charAt(0) === "#") return href;
    return "#/notifications";
  }

  const NAV = [
    ["Ops", [
      ["dashboard", "Tableau de bord", "fa-solid fa-grip"],
      ["hiring", "Besoins", "fa-solid fa-clipboard-list"],
      ["candidates", "Candidats", "fa-solid fa-users"],
      ["clients", "Clients", "fa-solid fa-industry"],
      ["jobs", "Offres d’emploi", "fa-solid fa-briefcase"],
      ["missions", "Missions", "fa-solid fa-diagram-project"],
      ["interviews", "Entretiens", "fa-solid fa-video"],
      ["messages", "Messages", "fa-solid fa-comments"]
    ]],
    ["Pilotage", [
      ["content", "Contenu", "fa-solid fa-pen-nib"],
      ["finance", "Finance", "fa-solid fa-file-invoice-dollar"],
      ["analytics", "Statistiques", "fa-solid fa-chart-line"],
      ["services", "Services", "fa-solid fa-plug"],
      ["notifications", "Notifications", "fa-solid fa-bell"]
    ]],
    ["Compte", [
      ["settings", "Paramètres", "fa-solid fa-gear"],
      ["profile", "Profil", "fa-solid fa-user"]
    ]]
  ];

  function route() {
    var h = (location.hash || "#/dashboard").replace(/^#\/?/, "");
    var parts = h.split("/").filter(Boolean);
    return { name: parts[0] || "dashboard", id: parts[1] || "" };
  }

  function go(hash) { location.hash = hash; }

  function allowedNav() {
    return NAV.map(function (g) {
      return [g[0], g[1].filter(function (i) { return TLStore.can(i[0]); })];
    }).filter(function (g) { return g[1].length; });
  }

  function firstModule() {
    var g = allowedNav()[0];
    return g ? g[1][0][0] : "profile";
  }

  /* ---------- Auth ---------- */
  function renderLogin() {
    var production = TLStore.apiEnv === "production";
    var emailPrefill = "";
    document.body.classList.add("login-open");
    app.innerHTML = `
      <div class="login">
        <section class="login-brand">
          <div>
            <img src="../assets/img/logo/logo1.png" alt="Talendus">
            <div style="margin-top:28px"><span class="login-kicker">Back-office</span></div>
            <h1>Talendus — équipe interne.</h1>
            <p>Dossiers, mandats, entretiens, factures et messages. Connexion réservée au personnel.</p>
          </div>
          <div class="login-meta">
            <div><b>QC</b>Placement au Québec</div>
            <div><b>ATS</b>Candidats &amp; clients</div>
            <div><b>CAD</b>Facturation TPS/TVQ</div>
          </div>
        </section>
        <section class="login-panel">
          <div class="login-card">
            <h2>Connexion</h2>
            <p class="sub">${production ? "Serveur de production — compte staff uniquement (ADMIN_EMAIL sur Render)." : "Espace privé — accès réservé à l’équipe Talendus."}</p>
            <p class="sub" style="margin-top:8px">Après connexion : entretiens, messages, factures QC, statistiques et onglet Équipe.</p>
            <form id="login-form" class="form-grid" style="grid-template-columns:1fr">
              ${U.field("Courriel", "email", emailPrefill, "email")}
              ${U.field("Mot de passe", "password", "", "password")}
              <button class="btn btn-orange" type="submit">Entrer dans le back-office</button>
            </form>
          </div>
        </section>
      </div>`;
    $("#login-form").onsubmit = async function (e) {
      e.preventDefault();
      var d = U.formData(e.target);
      var u = await TLStore.login(d.email, d.password);
      if (!u) {
        var err = TLStore.lastError;
        if (err === "not-staff") U.toast("Ce compte n’a pas accès au back-office. Utilisez le compte administrateur de production.", "err");
        else if (err === "account-disabled") U.toast("Ce compte est désactivé.", "err");
        else if (err === "email-not-verified") U.toast("Vérifiez votre courriel avant de vous connecter.", "err");
        else if (err === "locked") U.toast("Trop de tentatives. Réessayez dans quelques minutes.", "err");
        else if (err === "invalid-credentials") U.toast("Identifiants incorrects. Vérifiez le courriel et le mot de passe.", "err");
        else if (err === "api") U.toast("Connexion au serveur impossible. Vérifiez votre connexion, puis réessayez.", "err");
        else U.toast("Identifiants incorrects.", "err");
        return;
      }
      if (TLStore.lastError === "hydrate") {
        U.toast("Connecté. Le chargement des dossiers a échoué — rafraîchissez la page.", "warn");
      } else {
        U.toast("Bienvenue " + u.firstName + ".", "ok");
      }
      go("#/" + firstModule());
      render();
    };
  }

  /* ---------- Shell ---------- */
  function unread() {
    return S().notifications.filter(function (n) { return !n.read; }).length;
  }

  function shell(inner) {
    document.body.classList.remove("login-open");
    var me = TLStore.me();
    var r = route();
    var nav = allowedNav().map(function (g) {
      return '<div class="nav-group"><div class="nav-label">' + g[0] + "</div>" + g[1].map(function (i) {
        var active = r.name === i[0] ? " is-active" : "";
        var count = "";
        if (i[0] === "notifications" && unread()) count = '<span class="count">' + unread() + "</span>";
        if (i[0] === "messages" && (S().unreadMessages || 0)) count = '<span class="count">' + S().unreadMessages + "</span>";
        if (i[0] === "hiring") {
          var pending = (S().hiringRequests || S().missions || []).filter(function (m) {
            var key = m.status || m.statusKey || "";
            return ["besoin-transmis", "en-analyse", "REQUEST_SUBMITTED", "UNDER_REVIEW"].indexOf(key) !== -1;
          }).length;
          if (pending) count = '<span class="count">' + pending + "</span>";
        }
        return '<a class="nav-item' + active + '" href="#/' + i[0] + '"><i class="' + i[2] + '"></i>' + i[1] + count + "</a>";
      }).join("") + "</div>";
    }).join("");

    app.innerHTML = `
      <div class="shell">
        <aside class="sidebar" id="sidebar">
          <a class="sidebar-logo" href="#/${firstModule()}">
            <img src="../assets/img/logo/logo1.png" alt="">
            <div>Talendus<small>Back-office</small></div>
          </a>
          ${nav}
          <div class="live-flag ${live() ? "is-live" : "is-demo"}">${live() ? "Lié à l’application" : "Mode démo local"}</div>
          <div class="sidebar-foot">
            <a class="user-chip" href="#/profile">${U.avatar(me)}<div><b>${U.esc(me.firstName + " " + me.lastName)}</b><span>${U.esc(roleLabel(me.role))}</span></div></a>
            <button class="logout-btn" id="logout"><i class="fa-solid fa-right-from-bracket"></i> Déconnexion</button>
          </div>
        </aside>
        <div class="main">
          <header class="topbar">
            <button class="menu-toggle icon-btn" id="menu"><i class="fa-solid fa-bars"></i></button>
            <div class="search-wrap">
              <i class="fa-solid fa-magnifying-glass"></i>
              <input id="q" placeholder="Rechercher un candidat, un client, une offre, une mission, une facture…">
              <span class="kbd">⌘K</span>
            </div>
            <div class="top-actions">
              <div class="quick">
                <button class="btn btn-orange btn-sm" id="quick">+ Créer</button>
                <div class="dropdown" id="quick-menu" hidden>
                  <a class="n-item" href="#" data-create="candidate">Nouveau candidat</a>
                  <a class="n-item" href="#" data-create="client">Nouveau client</a>
                  <a class="n-item" href="#" data-create="job">Nouvelle offre</a>
                  <a class="n-item" href="#" data-create="mission">Nouvelle mission</a>
                  <a class="n-item" href="#" data-create="interview">Nouvel entretien</a>
                  <a class="n-item" href="#" data-create="invoice">Nouvelle facture</a>
                </div>
              </div>
              <button class="icon-btn" id="bell" title="Notifications">${unread() ? '<span class="dot"></span>' : ""}<i class="fa-regular fa-bell"></i></button>
              <a class="icon-btn" href="#/profile" title="Profil">${U.avatar(me, "sm")}</a>
            </div>
          </header>
          <div class="content" id="view">${inner}</div>
        </div>
      </div>`;

    $("#logout").onclick = function () {
      TLStore.logout();
      go("#/login");
      render();
    };
    $("#menu").onclick = function () { $("#sidebar").classList.toggle("open"); };
    $("#q").onfocus = openPalette;
    $("#q").onclick = openPalette;
    $("#bell").onclick = toggleNotifs;
    $("#quick").onclick = function (e) {
      e.stopPropagation();
      var m = $("#quick-menu");
      m.hidden = !m.hidden;
    };
    document.addEventListener("click", hidePop, { once: true });
    U.$$("[data-create]").forEach(function (a) {
      a.onclick = function (e) { e.preventDefault(); hidePop(); openCreate(a.getAttribute("data-create")); };
    });
  }

  function hidePop() {
    var m = document.getElementById("quick-menu");
    var d = document.getElementById("notif-drop");
    if (m) m.hidden = true;
    if (d) d.remove();
  }

  function roleLabel(r) {
    return { admin: "Administrateur", recruiter: "Recruteur", finance: "Finance", editor: "Éditeur" }[r] || r;
  }

  function toggleNotifs(e) {
    e.stopPropagation();
    if ($("#notif-drop")) { $("#notif-drop").remove(); return; }
    var items = S().notifications.slice(0, 8).map(function (n) {
      return '<div class="n-item ' + (n.read ? "" : "unread") + '" data-n="' + n.id + '" data-href="' + U.esc(n.href) + '"><b>' + U.esc(n.text) + '</b><div style="color:var(--steel);font-size:12px">' + U.esc(n.at) + "</div></div>";
    }).join("");
    var drop = document.createElement("div");
    drop.className = "dropdown";
    drop.id = "notif-drop";
    drop.innerHTML = "<header>Notifications</header>" + items + '<a class="n-item" href="#/notifications">Tout voir</a>';
    e.currentTarget.parentElement.style.position = "relative";
    e.currentTarget.parentElement.appendChild(drop);
    drop.onclick = function (ev) {
      var row = ev.target.closest("[data-n]");
      if (!row) return;
      var nid = row.getAttribute("data-n");
      var href = adminHash(row.getAttribute("data-href"));
      TLStore.update(function (st) {
        var n = st.notifications.find(function (x) { return x.id === nid; });
        if (n) n.read = true;
      });
      if (live()) {
        window.TalendusAPI.request("/notifications/" + nid + "/read", { method: "POST" }).catch(function () {});
      }
      go(href);
    };
  }

  /* ---------- Search palette ---------- */
  function openPalette() {
    if ($(".palette-back")) return;
    var back = document.createElement("div");
    back.className = "palette-back";
    back.innerHTML = '<div class="palette"><input id="pal-q" placeholder="Recherche globale — candidats, clients, offres, missions, factures, documents"><div id="pal-res"></div></div>';
    document.body.appendChild(back);
    var input = $("#pal-q");
    input.focus();
    function run() { $("#pal-res").innerHTML = searchHTML(input.value); }
    input.oninput = run;
    run();
    back.onclick = function (e) { if (e.target === back) back.remove(); };
    input.onkeydown = function (e) { if (e.key === "Escape") back.remove(); };
    $("#pal-res").onclick = function (e) {
      var a = e.target.closest("[data-go]");
      if (!a) return;
      back.remove();
      go(a.getAttribute("data-go"));
    };
  }

  function searchHTML(q) {
    q = (q || "").toLowerCase().trim();
    var groups = [
      ["Candidats", S().candidates.map(function (c) { return { t: c.firstName + " " + c.lastName + " · " + c.title, s: c.city, h: "#/candidates/" + c.id, hay: (c.firstName + c.lastName + c.title + c.city + c.sector).toLowerCase() }; })],
      ["Clients", S().clients.map(function (c) { return { t: c.name, s: c.city, h: "#/clients/" + c.id, hay: (c.name + c.city + c.sector + c.contact).toLowerCase() }; })],
      ["Offres", S().jobs.map(function (j) { return { t: j.title, s: j.city, h: "#/jobs/" + j.id, hay: (j.title + j.city + j.sector).toLowerCase() }; })],
      ["Missions", S().missions.map(function (m) { return { t: m.title, s: U.dateFr(m.due), h: "#/missions/" + m.id, hay: m.title.toLowerCase() }; })],
      ["Besoins", hiringList().map(function (h) { return { t: h.title, s: h.company_name || "", h: "#/hiring/" + h.id, hay: (h.title + " " + (h.company_name || "")).toLowerCase() }; })],
      ["Factures", S().invoices.map(function (i) { return { t: i.id, s: U.money(i.amount), h: "#/finance", hay: (i.id + String(i.amount)).toLowerCase() }; })],
      ["Documents", S().documents.map(function (d) { return { t: d.name, s: d.size, h: "#/candidates/" + (d.entityId || ""), hay: d.name.toLowerCase() }; })]
    ];
    return groups.map(function (g) {
      var hits = g[1].filter(function (x) { return !q || x.hay.indexOf(q) !== -1; }).slice(0, 5);
      if (!hits.length) return "";
      return '<div class="palette-group"><h5>' + g[0] + "</h5>" + hits.map(function (x) {
        return '<div class="palette-item" data-go="' + x.h + '"><span>' + U.esc(x.t) + "</span><span>" + U.esc(x.s) + "</span></div>";
      }).join("") + "</div>";
    }).join("") || '<div class="empty">Aucun résultat</div>';
  }

  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (TLStore.me()) openPalette();
    }
  });

  /* ---------- Dashboard ---------- */
  function viewDashboard() {
    var st = S();
    var today = new Date().toISOString().slice(0, 10);
    var monthStart = today.slice(0, 7) + "-01";
    var placed = st.candidates.filter(function (c) { return c.status === "place"; }).length;
    var activeJobs = st.jobs.filter(function (j) { return j.status === "publiee"; }).length;
    var activeClients = st.clients.filter(function (c) { return c.status === "Actif"; }).length;
    var openM = st.missions.filter(function (m) {
      return ["termine", "pourvue", "annulee", "CLOSED", "FILLED", "CANCELLED"].indexOf(m.status) === -1;
    }).length;
    var unpaid = st.invoices.filter(function (i) { return i.status === "en-attente" || i.status === "en-retard" || i.status === "envoyee"; });
    var revenue = st.invoices.filter(function (i) { return i.status === "payee"; }).reduce(function (s, i) { return s + i.amount; }, 0);
    var rate = Math.round((placed / Math.max(1, st.candidates.length)) * 100);
    var newbie = st.candidates.filter(function (c) { return (c.createdAt || "") >= monthStart; }).length;
    var bySector = {};
    st.candidates.forEach(function (c) { bySector[c.sector || "Autre"] = (bySector[c.sector || "Autre"] || 0) + 1; });
    var byStatus = {};
    st.candidates.forEach(function (c) { byStatus[c.status] = (byStatus[c.status] || 0) + 1; });
    var recPerf = st.users.filter(function (u) { return u.role === "recruiter" || u.role === "admin"; }).slice(0, 6).map(function (u, i) {
      var n = st.candidates.filter(function (c) { return c.recruiterId === u.id && c.status === "place"; }).length;
      return { l: u.firstName, v: n, c: ["#1e6bff", "#ff6b00", "#0b1f3a"][i % 3] };
    });
    if (!recPerf.length) recPerf = [{ l: "—", v: 0, c: "#1e6bff" }];
    var needs = (st.hiringRequests || []).filter(function (h) {
      return ["REQUEST_SUBMITTED", "UNDER_REVIEW", "CLIENT_CONTACTED"].indexOf(h.status) !== -1;
    }).length;

    return `
      <div class="page-head"><div><h1>Tableau de bord</h1><p>${live() ? "Données du jour." : "Vue locale."} ${U.dateFr(today)}</p></div>
        <div class="actions"><button class="btn btn-ghost btn-sm" data-export-dash>Exporter CSV</button></div></div>
      <div class="grid grid-6" style="margin-bottom:16px">
        ${kpi("Candidats", st.candidates.length, "+ " + newbie + " ce mois")}
        ${kpi("Nouveaux", newbie, "depuis le 1er du mois")}
        ${kpi("Clients actifs", activeClients, st.clients.length + " au total")}
        ${kpi("Offres actives", activeJobs, st.jobs.length + " au catalogue")}
        ${kpi("Besoins ouverts", needs || openM, placed + " placements")}
        ${kpi("Taux de placement", rate + " %", U.money(revenue) + " encaissés")}
      </div>
      <div class="grid grid-3" style="margin-bottom:16px">
        ${kpi("Placements réalisés", placed, "pipeline actif")}
        ${kpi("Revenus générés", U.money(revenue), "factures payées")}
        ${kpi("Factures impayées", U.money(unpaid.reduce(function (s, i) { return s + i.amount; }, 0)), unpaid.length + " pièces")}
      </div>
      <div class="grid grid-2" style="margin-bottom:16px">
        <div class="card card-pad"><div class="card-head"><h3>Évolution des candidatures</h3></div>${U.lineChart(st.monthly.applications, "#1e6bff")}<div class="legend">${st.monthly.months.join(" · ")}</div></div>
        <div class="card card-pad"><div class="card-head"><h3>Évolution des placements</h3></div>${U.lineChart(st.monthly.placements, "#ff6b00")}<div class="legend">${st.monthly.months.join(" · ")}</div></div>
      </div>
      <div class="grid grid-2" style="margin-bottom:16px">
        <div class="card card-pad"><div class="card-head"><h3>Revenus mensuels</h3></div>${U.barChart(st.monthly.months, st.monthly.revenue, "#0b1f3a")}</div>
        <div class="card card-pad"><div class="card-head"><h3>Performance des recruteurs</h3></div>${U.barChart(recPerf.map(function (r) { return r.l; }), recPerf.map(function (r) { return r.v; }), "#1e6bff")}</div>
      </div>
      <div class="grid grid-2">
        <div class="card card-pad"><div class="card-head"><h3>Candidats par secteur</h3></div>${U.donut(Object.keys(bySector).map(function (k, i) { return { l: k, v: bySector[k], c: ["#1e6bff","#ff6b00","#0b1f3a","#3d82ff","#0b7a38","#b45309"][i % 6] }; }))}</div>
        <div class="card card-pad"><div class="card-head"><h3>Candidats par statut</h3></div>${U.donut(Object.keys(byStatus).map(function (k, i) { return { l: (U.STATUS[k] || [k])[0], v: byStatus[k], c: ["#1e6bff","#ff6b00","#0b7a38","#b45309","#c0352b","#8b95a1"][i % 6] }; }))}</div>
      </div>
      <div class="card card-pad" style="margin-top:16px">
        <div class="card-head"><h3>Activité récente</h3></div>
        <div class="activity">${st.activities.map(function (a) { return '<div class="act"><span class="dot"></span><div><div>' + U.esc(a.text) + "</div><time>" + U.esc(a.at) + "</time></div></div>"; }).join("")}</div>
      </div>`;
  }

  function kpi(label, value, hint) {
    return '<div class="card kpi"><span>' + U.esc(label) + "</span><b>" + value + "</b><em class=\"up\">" + U.esc(hint || "") + "</em></div>";
  }

  /* ---------- Candidates ---------- */
  function filteredCandidates() {
    var list = S().candidates.slice();
    var f = filters;
    list = list.filter(function (c) {
      var hay = (c.firstName + " " + c.lastName).toLowerCase();
      if (f.q && hay.indexOf(f.q.toLowerCase()) === -1) return false;
      if (f.city && c.city !== f.city) return false;
      if (f.sector && c.sector !== f.sector) return false;
      if (f.title && c.title !== f.title) return false;
      if (f.level && c.level !== f.level) return false;
      if (f.availability && c.availability !== f.availability) return false;
      if (f.status && c.status !== f.status) return false;
      if (f.lang && candLangs(c).join(" ").indexOf(f.lang) === -1) return false;
      if (f.from && c.createdAt < f.from) return false;
      if (f.recruiter && c.recruiterId !== f.recruiter) return false;
      return true;
    });
    return U.sortBy(list, sortKey, sortDir);
  }

  function unique(arr, key) {
    return Array.from(new Set(arr.map(function (x) { return x[key]; }))).filter(Boolean);
  }

  function viewCandidates() {
    var list = filteredCandidates();
    var pg = U.paginate(list, page, 8);
    var rows = pg.items.map(function (c) {
      return `<tr data-go="#/candidates/${c.id}">
        <td class="check" onclick="event.stopPropagation()"><input type="checkbox" data-sel="${c.id}" ${selected.has(c.id) ? "checked" : ""}></td>
        <td><div class="person">${U.avatar({ firstName: c.firstName, lastName: c.lastName, userId: c.userId })}<div><b>${U.esc(c.firstName + " " + c.lastName)}</b><span>${U.esc(c.email)}</span></div></div></td>
        <td>${U.esc(c.title)}</td>
        <td>${U.esc(c.city)}</td>
        <td>${U.esc(c.sector)}</td>
        <td>${c.experience} ans · ${U.esc(c.level)}</td>
        <td>${U.badge(c.status)}</td>
        <td>${U.dateFr(c.createdAt)}</td>
        <td>${U.dateFr(c.lastActivity)}</td>
        <td>${U.esc(TLStore.name(c.recruiterId))}</td>
        <td onclick="event.stopPropagation()">
          <button class="btn btn-ghost btn-sm" data-note="${c.id}">Note</button>
        </td>
      </tr>`;
    }).join("");
    var sel = function (name, opts, val) {
      return '<select data-f="' + name + '"><option value="">' + opts[0] + "</option>" + opts.slice(1).map(function (o) {
        return "<option" + (val === o ? " selected" : "") + ">" + o + "</option>";
      }).join("") + "</select>";
    };
    return `
      <div class="page-head"><div><h1>Candidats</h1><p>${list.length} profils dans le vivier industriel</p></div>
        <div class="actions">
          <button class="btn btn-ghost" data-export-cand>Exporter CSV</button>
          <button class="btn btn-orange" data-create="candidate">Nouveau candidat</button>
        </div></div>
      <div class="filters">
        <input data-f="q" placeholder="Nom" value="${U.esc(filters.q || "")}">
        ${sel("city", ["Ville"].concat(unique(S().candidates, "city")), filters.city)}
        ${sel("sector", ["Secteur"].concat(unique(S().candidates, "sector")), filters.sector)}
        ${sel("title", ["Métier"].concat(unique(S().candidates, "title")), filters.title)}
        ${sel("level", ["Expérience", "Junior", "Intermédiaire", "Senior", "Cadre"], filters.level)}
        ${sel("availability", ["Disponibilité", "Immédiat", "2 semaines", "3 semaines", "1 mois", "2 mois"], filters.availability)}
        <select data-f="status"><option value="">Statut</option>${Object.keys(U.STATUS).filter(function (k) { return ["nouveau","a-contacter","qualifie","entretien","presente","entretien-client","offre","place","refuse","inactif"].indexOf(k) >= 0; }).map(function (k) { return "<option value=\"" + k + "\"" + (filters.status === k ? " selected" : "") + ">" + U.STATUS[k][0] + "</option>"; }).join("")}</select>
        ${sel("lang", ["Langue", "Français", "Anglais"], filters.lang)}
        <input data-f="from" type="date" value="${filters.from || ""}">
        <select data-f="recruiter"><option value="">Recruteur</option>${S().users.filter(function (u) { return u.role === "recruiter" || u.role === "admin"; }).map(function (u) { return "<option value=\"" + u.id + "\"" + (filters.recruiter === u.id ? " selected" : "") + ">" + u.firstName + " " + u.lastName + "</option>"; }).join("")}</select>
      </div>
      <div class="bulkbar ${selected.size ? "is-on" : ""}">${selected.size} sélectionné(s)
        <button class="btn btn-sm btn-ghost" data-bulk="qualifie">Marquer qualifié</button>
        <button class="btn btn-sm btn-ghost" data-bulk="inactif">Inactif</button>
      </div>
      <div class="card"><div class="table-wrap"><table class="data">
        <thead><tr>
          <th class="check"></th>
          ${[["lastName","Nom"],["title","Poste recherché"],["city","Localisation"],["sector","Secteur"],["experience","Expérience"],["status","Statut"],["createdAt","Inscription"],["lastActivity","Dernière activité"],["recruiterId","Recruteur"],["", "Actions"]].map(function (c) { return "<th data-sort=\"" + c[0] + "\">" + c[1] + "</th>"; }).join("")}
        </tr></thead>
        <tbody>${rows || '<tr><td colspan="11">' + U.empty("Aucun candidat", "Ajustez les filtres ou créez un profil.") + "</td></tr>"}</tbody>
      </table></div>
      <div class="pager"><span>${pg.total} résultats</span><div class="pages">${Array.from({ length: pg.pages }, function (_, i) { return '<button class="btn btn-ghost btn-sm' + (pg.page === i + 1 ? " btn-orange" : "") + '" data-page="' + (i + 1) + '">' + (i + 1) + "</button>"; }).join("")}</div></div>
      </div>`;
  }

  function viewCandidate(id) {
    var c = TLStore.candidate(id);
    if (!c) return U.empty("Introuvable", "Ce candidat n’existe pas.");
    var notes = S().notes.filter(function (n) { return n.entity === "candidate" && n.entityId === id; });
    var ints = S().interviews.filter(function (i) { return i.candidateId === id; });
    var docs = S().documents.filter(function (d) { return d.entity === "candidate" && d.entityId === id; });
    var client = TLStore.client(c.clientId);
    var tabs = { profil: "Profil", cv: "CV & documents", histo: "Candidatures", entretiens: "Entretiens", notes: "Notes internes", interactions: "Historique" };
    var body = "";
    if (detailTab === "profil") {
      body = `<div class="form-grid">
        <div class="card card-pad"><h3>Informations personnelles</h3>
          <div class="row"><span>Nom</span><b>${U.esc(c.firstName + " " + c.lastName)}</b></div>
          <div class="row"><span>Ville</span><b>${U.esc(c.city)}</b></div>
          <div class="row"><span>Langues</span><b>${U.esc(candLangs(c).join(", "))}</b></div>
        </div>
        <div class="card card-pad"><h3>Coordonnées</h3>
          <div class="row"><span>Courriel</span><b>${U.esc(c.email)}</b></div>
          <div class="row"><span>Téléphone</span><b>${U.esc(c.phone)}</b></div>
        </div>
        <div class="card card-pad full"><h3>Profil professionnel</h3><p>${U.esc(c.bio)}</p>
          <p><b>Compétences :</b> ${c.skills.map(function (s) { return '<span class="badge">' + U.esc(s) + "</span>"; }).join(" ")}</p>
          <p><b>Disponibilité :</b> ${U.esc(c.availability)} · <b>Quart :</b> ${U.esc(c.shift)}</p>
          <p><b>Préférences :</b> ${U.esc(c.sector)} · ${typeof c.salaryMin === "number" && c.salaryMin < 1000 ? c.salaryMin + "–" + c.salaryMax + " $/h" : U.money(c.salaryMin) + " – " + U.money(c.salaryMax)}</p>
        </div>
        <div class="card card-pad"><h3>Expériences</h3>${c.experiences.map(function (e) { return "<p><b>" + U.esc(e.role) + "</b> — " + U.esc(e.company) + "<br><span style='color:var(--steel)'>" + U.esc(e.years) + "</span></p>"; }).join("") || "<p>—</p>"}</div>
        <div class="card card-pad"><h3>Formations</h3>${c.education.map(function (e) { return "<p><b>" + U.esc(e.diploma) + "</b> — " + U.esc(e.school) + " (" + e.year + ")</p>"; }).join("") || "<p>—</p>"}</div>
      </div>`;
    } else if (detailTab === "cv") {
      var docRows = docs.map(function (d) {
        var href = d.url || "";
        return "<p><i class='fa-regular fa-file'></i> " + U.esc(d.name) + " · " + U.esc(d.size || "") +
          (href ? " <button class='btn btn-ghost btn-sm' data-dl-doc='" + U.esc(href) + "' data-dl-name='" + U.esc(d.name) + "'>Télécharger</button>" : "") +
          "</p>";
      }).join("");
      body = '<div class="card card-pad"><h3>Documents</h3>' +
        (docRows || "<p>Aucun document dans le dossier.</p>") +
        '<form id="cand-upload" style="margin-top:12px"><input type="file" name="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/jpeg,image/png,image/webp" required> ' +
        '<button class="btn btn-orange" type="submit">Ajouter un document</button></form></div>';
    } else if (detailTab === "histo") {
      var apps = c.applications || [];
      body = `<div class="card card-pad"><h3>Historique des candidatures</h3>
        ${apps.length ? apps.map(function (a) {
          var job = TLStore.job(a.jobId) || {};
          return "<p><a href=\"#/jobs/" + a.jobId + "\">" + U.esc(a.jobTitle || job.title || "Offre") + "</a> — " + U.badge(a.status) + " · " + U.dateFr(a.createdAt) + "</p>";
        }).join("") : "<p>Offre liée : <a href=\"#/jobs/" + c.jobId + "\">" + U.esc((TLStore.job(c.jobId) || {}).title || "—") + "</a></p>"}
        <h3>Entreprises auxquelles il a été présenté</h3>
        <p>${client ? '<a href="#/clients/' + client.id + '">' + U.esc(client.name) + "</a> — " + U.badge(c.status) : "Pas encore présenté."}</p></div>`;
    } else if (detailTab === "entretiens") {
      body = '<div class="card card-pad"><h3>Entretiens</h3>' + (ints.map(function (i) {
        return "<p><b>" + U.esc(i.type) + "</b> — " + U.esc(i.at) + " · " + U.esc(i.location) + callButtons(i) + "</p>";
      }).join("") || "<p>Aucun entretien.</p>") + '<button class="btn btn-orange" data-add-int="' + id + '">Planifier</button></div>';
    } else if (detailTab === "notes") {
      body = '<div class="card card-pad"><h3>Notes internes</h3>' + notes.map(function (n) {
        return '<div class="note"><div class="meta">' + U.esc(TLStore.name(n.authorId)) + " · " + U.esc(n.at) + "</div>" + U.esc(n.text) + "</div>";
      }).join("") + '<form id="note-form">' + U.field("Nouvelle note", "text", "", "textarea", "full") + '<button class="btn btn-orange" type="submit">Enregistrer la note</button></form></div>';
    } else {
      body = '<div class="card card-pad timeline">' + S().activities.filter(function (a) { return a.text.toLowerCase().indexOf(c.lastName.toLowerCase()) >= 0 || a.text.toLowerCase().indexOf(c.firstName.toLowerCase()) >= 0; }).concat([{ text: "Profil créé", at: c.createdAt }]).map(function (a) {
        return '<div class="tl-item"><b>' + U.esc(a.text) + "</b><div style='color:var(--steel);font-size:12px'>" + U.esc(a.at) + "</div></div>";
      }).join("") + "</div>";
    }

    return `
      <div class="crumbs"><a href="#/candidates">Candidats</a> / ${U.esc(c.firstName)} ${U.esc(c.lastName)}</div>
      <div class="page-head"><div><h1>${U.esc(c.firstName + " " + c.lastName)}</h1><p>${U.esc(c.title)} · ${U.esc(c.city)} · ${U.badge(c.status)}</p></div>
        <div class="actions">
          <select data-status-cand="${c.id}">${["nouveau","a-contacter","qualifie","entretien","presente","entretien-client","offre","place","refuse","inactif"].map(function (s) { return "<option value=\"" + s + "\"" + (c.status === s ? " selected" : "") + ">" + U.STATUS[s][0] + "</option>"; }).join("")}</select>
          <button class="btn btn-ghost" data-edit-cand="${c.id}">Modifier</button>
        </div></div>
      <div class="detail-grid">
        <div class="card card-pad side-card">
          ${U.avatar({ firstName: c.firstName, lastName: c.lastName, userId: c.userId }, "lg")}
          <p><b>${U.esc(c.email)}</b><br>${U.esc(c.phone)}</p>
          <div class="row"><span>Recruteur</span><b>${U.esc(TLStore.name(c.recruiterId))}</b></div>
          <div class="row"><span>Inscription</span><b>${U.dateFr(c.createdAt)}</b></div>
          <div class="row"><span>Dernière activité</span><b>${U.dateFr(c.lastActivity)}</b></div>
          <div class="row"><span>CV</span><b>${docs.length ? docs[0].name : "Non déposé"}</b></div>
        </div>
        <div>
          <div class="tabs">${Object.keys(tabs).map(function (k) { return '<button class="tab' + (detailTab === k ? " is-on" : "") + '" data-dtab="' + k + '">' + tabs[k] + "</button>"; }).join("")}</div>
          ${body}
        </div>
      </div>`;
  }

  /* ---------- Clients ---------- */
  function viewClients() {
    var list = S().clients.filter(function (c) {
      if (filters.q && (c.name + c.city).toLowerCase().indexOf((filters.q || "").toLowerCase()) === -1) return false;
      if (filters.sector && c.sector !== filters.sector) return false;
      if (filters.status && c.status !== filters.status) return false;
      return true;
    });
    var rows = list.map(function (c) {
      var missions = S().missions.filter(function (m) { return m.clientId === c.id; }).length;
      var placed = S().candidates.filter(function (x) { return x.clientId === c.id && x.status === "place"; }).length;
      return `<tr data-go="#/clients/${c.id}"><td><b>${U.esc(c.name)}</b></td><td>${U.esc(c.sector)}</td><td>${U.esc(c.city)}</td><td>${U.esc(c.contact)}</td><td>${missions}</td><td>${placed}</td><td>${U.badge(c.status)}</td><td>${U.esc(TLStore.name(c.recruiterId))}</td></tr>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Clients</h1><p>Entreprises opérationnelles du Québec</p></div>
        <div class="actions"><button class="btn btn-ghost" data-export-cli>Exporter</button><button class="btn btn-orange" data-create="client">Nouveau client</button></div></div>
      <div class="filters">
        <input data-f="q" placeholder="Nom ou ville" value="${U.esc(filters.q || "")}">
        <select data-f="sector"><option value="">Secteur</option>${unique(S().clients, "sector").map(function (s) { return "<option" + (filters.sector === s ? " selected" : "") + ">" + s + "</option>"; }).join("")}</select>
        <select data-f="status"><option value="">Statut</option><option>Actif</option><option>Prospect</option></select>
      </div>
      <div class="card"><div class="table-wrap"><table class="data">
        <thead><tr><th>Entreprise</th><th>Secteur</th><th>Localisation</th><th>Contact principal</th><th>Missions</th><th>Recrutements</th><th>Statut</th><th>Recruteur</th></tr></thead>
        <tbody>${rows || '<tr><td colspan="8">' + U.empty("Aucun client", "Créez une entreprise ou attendez qu’un employeur ouvre un espace.") + "</td></tr>"}</tbody></table></div></div>`;
  }

  function clientStatusLabel(ct) {
    if (ct.clientSigned || ct.clientStatus === "signed") return "Signé";
    if (ct.openedAt || ct.clientStatus === "opened") return "Ouvert";
    if (ct.sentAt || ct.clientStatus === "received") return "Reçu";
    return "Non envoyé";
  }

  function contractCard(ct) {
    var agency = ct.talendusSigned
      ? U.badge("Signé Talendus")
      : U.badge("À signer");
    var client = U.badge(clientStatusLabel(ct));
    var actions = '<div class="mandate-actions"><button class="btn btn-ghost btn-sm" data-read-contract="' + ct.id + '">Lire le mandat</button>';
    if (ct.pdfPath) {
      actions += ' <button class="btn btn-ghost btn-sm" data-open-pdf="' + ct.id + '">Lire le PDF</button>';
    }
    if (!ct.talendusSigned) {
      actions += ' <button class="btn btn-orange btn-sm" data-sign-talendus="' + ct.id + '">Signer pour Talendus</button>';
    }
    if (ct.talendusSigned && !ct.sentAt && !ct.clientSigned) {
      actions += ' <button class="btn btn-orange btn-sm" data-send-contract="' + ct.id + '">Envoyer au client</button>';
    }
    if (ct.sentAt && !ct.clientSigned) {
      actions += ' <button class="btn btn-ghost btn-sm" data-send-contract="' + ct.id + '">Relancer le client</button>';
      actions += ' <button class="btn btn-ghost btn-sm" data-sign-contract="' + ct.id + '">Enregistrer la signature du client</button>';
    }
    actions += "</div>";
    var trace = "";
    if (ct.talendusSigner || ct.talendusSignedAt) {
      trace += "<p style='color:var(--steel);font-size:12px'>Talendus : " + U.esc(ct.talendusSigner || "signé") + (ct.talendusSignedAt ? " · " + U.esc(ct.talendusSignedAt) : "") + "</p>";
    }
    if (ct.clientSigned) {
      trace += "<p style='color:var(--steel);font-size:12px'>Client : " + U.esc(ct.signerName || "") + (ct.signedAt ? " · " + U.esc(ct.signedAt) : "") + (ct.documentHash ? "<br>Hash " + U.esc(String(ct.documentHash).slice(0, 12)) + "…" : "") + "</p>";
    } else if (ct.openedAt) {
      trace += "<p style='color:var(--steel);font-size:12px'>Ouvert par le client le " + U.esc(ct.openedAt) + "</p>";
    } else if (ct.sentAt) {
      trace += "<p style='color:var(--steel);font-size:12px'>Reçu le " + U.esc(ct.sentAt) + (ct.reminderCount ? " · relancé " + ct.reminderCount + " fois" : "") + "</p>";
    }
    if ((ct.canEdit !== false) && !ct.talendusSigned && !ct.sentAt && !ct.clientSigned) {
      actions += ' <button class="btn btn-ghost btn-sm" data-edit-contract="' + ct.id + '">Modifier</button>';
    }
    if (ct.talendusSigned && ct.clientSigned) {
      client += " " + U.badge("Complet");
    }
    var duration = ct.durationDays ? (" · " + ct.durationDays + " jours") : "";
    return "<div class='mandate-card'><p><b>" + U.esc(ct.type) + "</b> · " + agency + " " + client +
      "<br>Commission " + ct.commission + " % · " + U.dateFr(ct.start) + " → " + U.dateFr(ct.end) + duration +
      "</p>" + trace + actions + "</div>";
  }

  function mandatePayload(d) {
    var percent = parseInt(d.commission_percent, 10);
    if (!(percent >= 0 && percent <= 100)) percent = 16;
    var type = (d.type || "").trim();
    if (type.length > 120) type = type.slice(0, 120);
    return {
      template: d.template || "succes",
      type: type || undefined,
      role: (d.role || "").trim() || null,
      start_date: d.start_date || null,
      end_date: d.end_date || null,
      commission_percent: percent
    };
  }

  function openMandateModal(companyId, existing) {
    existing = existing || {};
    var isEdit = !!existing.id;
    var today = new Date().toISOString().slice(0, 10);
    U.modal({
      wide: true,
      title: isEdit ? "Modifier le brouillon" : "Préparer le mandat",
      body: '<form id="ct-form" class="form-grid">' +
        U.field("Modèle", "template", { options: [{ v: "succes", l: "Recrutement au succès" }, { v: "temporaire", l: "Placement temporaire" }], selected: existing.template || "succes" }, "select") +
        U.field("Type", "type", existing.type || "Mandat de recrutement au succès") +
        U.field("Poste visé", "role", existing.role || "") +
        U.field("Début", "start_date", existing.start || today, "date") +
        U.field("Fin", "end_date", existing.end || "", "date") +
        U.field("Commission (%)", "commission_percent", existing.commission != null ? String(existing.commission) : "16", "number") +
        '<p class="mandate-duration full" id="ct-duration">Durée : —</p>' +
        '<div class="full"><label>Texte du mandat</label><article id="ct-read" class="mandate-read">Chargement du mandat…</article>' +
        '<textarea name="terms" id="ct-terms" class="sr-only" hidden></textarea></div>' +
        "</form>",
      footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer le brouillon</button>',
      onMount: function (box, close) {
        var form = box.querySelector("#ct-form");
        var reader = box.querySelector("#ct-read");
        var durationEl = box.querySelector("#ct-duration");
        var userTouchedEnd = !!(existing.end);
        var previewTimer = null;
        function setDuration(days, start, end) {
          if (!durationEl) return;
          var label = days ? (days + " jour" + (days > 1 ? "s" : "")) : "—";
          durationEl.textContent = "Durée du mandat : " + label +
            (start && end ? " (" + start + " → " + end + ")" : "");
        }
        async function fillPreview() {
          if (!live()) {
            var localStart = form.start_date.value;
            var localEnd = form.end_date.value;
            if (localStart && localEnd) {
              var a = new Date(localStart);
              var b = new Date(localEnd);
              var days = Math.max(1, Math.round((b - a) / 86400000));
              setDuration(days, localStart, localEnd);
            }
            return;
          }
          try {
            var q = "?company_id=" + encodeURIComponent(companyId) +
              "&template=" + encodeURIComponent(form.template.value || "succes") +
              "&commission_percent=" + encodeURIComponent(form.commission_percent.value || "16") +
              (form.role.value ? "&role=" + encodeURIComponent(form.role.value) : "") +
              (form.start_date.value ? "&start_date=" + encodeURIComponent(form.start_date.value) : "") +
              (form.end_date.value ? "&end_date=" + encodeURIComponent(form.end_date.value) : "");
            var prev = await window.TalendusAPI.previewContract(q);
            var data = (prev && prev.data) || prev || {};
            if (data.type) form.type.value = data.type;
            if (data.start_date && !form.start_date.value) form.start_date.value = data.start_date;
            if (data.end_date && (!form.end_date.value || !userTouchedEnd)) form.end_date.value = data.end_date;
            if (data.commission_percent != null && !form.commission_percent.value) form.commission_percent.value = data.commission_percent;
            if (data.duration_days != null) setDuration(data.duration_days, data.start_date || form.start_date.value, data.end_date || form.end_date.value);
            if (data.terms) {
              form.terms.value = data.terms;
              reader.textContent = data.terms;
            }
          } catch (err) {
            reader.textContent = "Le mandat se remplit à l’enregistrement.";
          }
        }
        function schedulePreview() {
          if (previewTimer) clearTimeout(previewTimer);
          previewTimer = setTimeout(fillPreview, 180);
        }
        fillPreview();
        ["template", "commission_percent", "role", "start_date", "end_date"].forEach(function (name) {
          form[name].addEventListener("change", function () {
            if (name === "end_date") userTouchedEnd = !!form.end_date.value;
            if (name === "template") {
              userTouchedEnd = false;
              form.end_date.value = "";
            }
            if (name === "start_date" && !userTouchedEnd) form.end_date.value = "";
            schedulePreview();
          });
          form[name].addEventListener("input", function () {
            if (name === "end_date") userTouchedEnd = !!form.end_date.value;
            if (name === "start_date" && !userTouchedEnd) form.end_date.value = "";
            schedulePreview();
          });
        });
        box.querySelector("#save").onclick = async function () {
          var d = U.formData(form);
          var payload = mandatePayload(d);
          try {
            if (live()) {
              if (!companyId) throw new Error("Choisissez une entreprise avant d’enregistrer le mandat.");
              if (isEdit) {
                await api().updateContract(existing.id, payload);
              } else {
                payload.company_id = companyId;
                try {
                  await api().createContract(payload);
                } catch (first) {
                  await api().createContract({
                    company_id: companyId,
                    template: payload.template || "succes",
                    start_date: payload.start_date || null,
                    end_date: payload.end_date || null,
                    commission_percent: payload.commission_percent,
                    role: payload.role || null
                  });
                }
              }
              await refreshLive();
            } else {
              TLStore.update(function (st) {
                var row = {
                  id: existing.id || TLStore.nid("ct"),
                  clientId: companyId,
                  type: payload.type || "Mandat de recrutement au succès",
                  start: payload.start_date,
                  end: payload.end_date,
                  commission: payload.commission_percent,
                  terms: (form.terms && form.terms.value) || (reader && reader.textContent) || "",
                  status: "Brouillon",
                  document: "",
                  talendusSigned: false,
                  clientSigned: false,
                  clientStatus: "not_sent",
                  canEdit: true,
                  durationDays: existing.durationDays || ""
                };
                if (isEdit) {
                  var found = st.contracts.find(function (x) { return x.id === existing.id; });
                  if (found) Object.assign(found, row, { id: existing.id });
                  else st.contracts.push(row);
                } else {
                  st.contracts.push(row);
                }
              });
            }
            close();
            U.toast(isEdit ? "Brouillon mis à jour." : "Brouillon enregistré. Lisez-le, signez pour Talendus, puis envoyez-le au client.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Enregistrement impossible.", "err");
          }
        };
      }
    });
  }

  function viewClient(id) {
    var c = TLStore.client(id);
    if (!c) return U.empty("Introuvable", "Client introuvable.");
    var contracts = S().contracts.filter(function (x) { return x.clientId === id; });
    var missions = S().missions.filter(function (m) { return m.clientId === id; });
    var jobs = S().jobs.filter(function (j) { return j.clientId === id; });
    var cands = S().candidates.filter(function (x) { return x.clientId === id; });
    var inv = S().invoices.filter(function (i) { return i.clientId === id; });
    var notes = S().notes.filter(function (n) { return n.entity === "client" && n.entityId === id; });
    return `
      <div class="crumbs"><a href="#/clients">Clients</a> / ${U.esc(c.name)}</div>
      <div class="page-head"><div><h1>${U.esc(c.name)}</h1><p>${U.esc(c.sector)} · ${U.esc(c.city)} · ${U.badge(c.status)}</p></div>
        <div class="actions">
          <button class="btn btn-ghost" data-edit-client="${id}">Modifier</button>
          <button class="btn btn-orange" data-add-contract="${id}">Préparer le mandat</button>
        </div></div>
      <div class="grid grid-2">
        <div class="card card-pad"><h3>Informations générales</h3>
          <div class="row"><span>Employés</span><b>${c.employees}</b></div>
          <div class="row"><span>Client depuis</span><b>${U.dateFr(c.since)}</b></div>
          <div class="row"><span>Site</span><b>${U.esc(c.website)}</b></div>
          <h3 style="margin-top:16px">Contacts</h3>
          <p><b>${U.esc(c.contact)}</b><br>${U.esc(c.email)}<br>${U.esc(c.phone)}</p>
        </div>
        <div class="card card-pad"><h3>Contrats</h3>${contracts.map(contractCard).join("") || "<p>Aucun mandat. Préparez-le, lisez-le, signez pour Talendus, puis envoyez-le au client. Vous suivrez ensuite reçu, ouvert et signé.</p>"}</div>
      </div>
      <div class="grid grid-2" style="margin-top:16px">
        <div class="card card-pad"><h3>Missions</h3>${missions.map(function (m) { return '<p><a href="#/missions/' + m.id + '">' + U.esc(m.title) + "</a> " + U.badge(m.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
        <div class="card card-pad"><h3>Offres d’emploi</h3>${jobs.map(function (j) { return '<p><a href="#/jobs/' + j.id + '">' + U.esc(j.title) + "</a> " + U.badge(j.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
      </div>
      <div class="grid grid-2" style="margin-top:16px">
        <div class="card card-pad"><h3>Candidats présentés / placements</h3>${cands.map(function (x) { return '<p><a href="#/candidates/' + x.id + '">' + U.esc(x.firstName + " " + x.lastName) + "</a> " + U.badge(x.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
        <div class="card card-pad"><h3>Factures & paiements</h3>${inv.map(function (i) { return "<p>" + U.esc(i.id) + " · " + U.money(i.amount) + " " + U.badge(i.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
      </div>
      <div class="card card-pad" style="margin-top:16px"><h3>Notes internes</h3>${notes.map(function (n) { return '<div class="note">' + U.esc(n.text) + " <span class='meta'>· " + U.esc(n.at) + "</span></div>"; }).join("") || "<p>Aucune note.</p>"}
        <form id="client-note-form" style="margin-top:12px">${U.field("Nouvelle note", "text", "", "textarea", "full")}<button class="btn btn-orange" type="submit">Enregistrer la note</button></form>
      </div>`;
  }

  /* ---------- Jobs ---------- */
  function viewJobs() {
    var list = S().jobs.filter(function (j) {
      if (filters.q && j.title.toLowerCase().indexOf((filters.q || "").toLowerCase()) === -1) return false;
      if (filters.status && j.status !== filters.status) return false;
      return true;
    });
    var rows = list.map(function (j) {
      var cl = TLStore.client(j.clientId);
      return `<article class="offer-card" data-go="#/jobs/${j.id}">
        <div class="offer-card-banner"><span>${U.esc(j.sector || "Talendus")}</span>${U.badge(j.status)}</div>
        <div class="offer-card-body">
          <h3>${U.esc(j.title)}</h3>
          <p class="muted">${U.esc(cl ? cl.name : "—")}</p>
          <ul class="offer-pills">
            ${j.city ? "<li>" + U.esc(j.city) + "</li>" : ""}
            ${j.salary ? '<li class="is-pay">' + U.esc(j.salary) + "</li>" : ""}
            ${j.type ? "<li>" + U.esc(j.type) + "</li>" : ""}
            <li>${j.applications || 0} candidature${(j.applications || 0) > 1 ? "s" : ""}</li>
          </ul>
          <p onclick="event.stopPropagation()"><button class="btn btn-ghost btn-sm" data-job-act="dup:${j.id}">Dupliquer</button></p>
        </div>
      </article>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Offres d’emploi</h1><p>Publication vers le site public Talendus</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="job">Créer une offre</button></div></div>
      <div class="filters">
        <input data-f="q" placeholder="Titre" value="${U.esc(filters.q || "")}">
        <select data-f="status"><option value="">Statut</option>${["brouillon","publiee","suspendue","expiree","archivee"].map(function (s) { return "<option value=\"" + s + "\"" + (filters.status === s ? " selected" : "") + ">" + U.STATUS[s][0] + "</option>"; }).join("")}</select>
      </div>
      <div class="offer-grid">${rows || '<div class="card card-pad">' + U.empty("Aucune offre", "Créez une offre, puis publiez-la pour qu’elle apparaisse sur le site.") + "</div>"}</div>`;
  }

  function viewJob(id) {
    var j = TLStore.job(id);
    if (!j) return U.empty("Introuvable", "Offre introuvable.");
    var cl = TLStore.client(j.clientId);
    return `
      <div class="crumbs"><a href="#/jobs">Offres</a> / ${U.esc(j.title)}</div>
      <div class="page-head"><div><h1>${U.esc(j.title)}</h1><p>${U.esc(cl ? cl.name : "")} · ${U.esc(j.city)} · ${U.badge(j.status)}</p></div>
        <div class="actions">
          <button class="btn btn-ghost" data-job-act="edit:${j.id}">Modifier</button>
          <button class="btn btn-electric" data-job-act="publiee:${j.id}">Publier</button>
          <button class="btn btn-ghost" data-job-act="suspendue:${j.id}">Dépublier</button>
          <button class="btn btn-ghost" data-job-act="archivee:${j.id}">Archiver</button>
          <button class="btn btn-ghost" data-job-act="dup:${j.id}">Dupliquer</button>
          ${j.slug ? '<a class="btn btn-ghost" href="' + U.esc(j.url || ("/emploi-" + j.slug + ".html")) + '" target="_blank" rel="noopener">Voir sur le site</a>' : ""}
        </div></div>
      <div class="grid grid-2">
        <div class="card card-pad">
          <h3>Description</h3><p>${U.esc(j.description)}</p>
          <h3>Responsabilités</h3><p>${U.esc(j.responsibilities)}</p>
          <h3>Qualifications</h3><p>${U.esc(j.qualifications)}</p>
        </div>
        <div class="card card-pad">
          <div class="row"><span>Salaire</span><b>${U.esc(j.salary)}</b></div>
          <div class="row"><span>Type de contrat</span><b>${U.esc(j.contract_type || j.type)}</b></div>
          <div class="row"><span>Horaire</span><b>${U.esc(j.schedule || "—")}</b></div>
          <div class="row"><span>Quart</span><b>${U.esc(j.shift)}</b></div>
          <div class="row"><span>Expérience</span><b>${U.esc(j.experience)}</b></div>
          <div class="row"><span>Compétences</span><b>${U.esc(j.skills)}</b></div>
          <div class="row"><span>Avantages</span><b>${U.esc(j.benefits)}</b></div>
          <div class="row"><span>Publication</span><b>${U.dateFr(j.publishedAt)}</b></div>
          <div class="row"><span>Expiration</span><b>${U.dateFr(j.expiresAt)}</b></div>
          <div class="row"><span>Candidatures</span><b>${j.applications}</b></div>
        </div>
      </div>
      <div class="card card-pad" style="margin-top:16px"><h3>Candidats correspondants (score déterministe)</h3>
        ${(S().jobMatches || []).filter(function (m) { return m.jobId === id; }).map(function (m) {
          var c = TLStore.candidate(m.candidateId);
          if (!c) return "";
          return '<p><a href="#/candidates/' + c.id + '">' + U.esc(c.firstName + " " + c.lastName) + "</a> — " + m.score + " % · " + U.esc((m.reasons || []).slice(0, 2).join(" · ")) + "</p>";
        }).join("") || "<p>Aucun profil au-dessus du seuil pour le moment.</p>"}
      </div>`;
  }

  /* ---------- Missions / pipeline ---------- */
  function viewMissions() {
    var list = S().missions;
    var rows = list.map(function (m) {
      var cl = TLStore.client(m.clientId);
      var job = TLStore.job(m.jobId);
      var n = Object.keys(m.stageMap || {}).length;
      return `<tr data-go="#/missions/${m.id}"><td><b>${U.esc(m.title)}</b></td><td>${U.esc(cl ? cl.name : "—")}</td><td>${U.esc(job ? job.title : "—")}</td><td>${m.seats}</td><td>${U.esc(TLStore.name(m.recruiterId))}</td><td>${U.dateFr(m.start)}</td><td>${U.dateFr(m.due)}</td><td>${U.badge(m.status)}</td><td>${n}</td><td><div style="background:#eef2f6;border-radius:99px;height:8px;width:80px"><div style="width:${m.progress}%;background:var(--orange);height:8px;border-radius:99px"></div></div> ${m.progress}%</td><td>${U.money(m.value)}</td><td>${U.money(m.commission)}</td></tr>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Missions</h1><p>Mandats en cours, kanban et commissions.</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="mission">Nouvelle mission</button></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Mission</th><th>Client</th><th>Poste</th><th>Postes</th><th>Recruteur</th><th>Début</th><th>Échéance</th><th>Statut</th><th>Candidats</th><th>Progression</th><th>Valeur</th><th>Commission</th></tr></thead><tbody>${rows || '<tr><td colspan="12">' + U.empty("Aucune mission", "Créez un mandat ou convertissez un besoin d’entreprise.") + "</td></tr>"}</tbody></table></div></div>`;
  }

  function viewMission(id) {
    var m = TLStore.mission(id);
    if (!m) return U.empty("Introuvable", "Mission introuvable.");
    function itemsForStage(stage) {
      var pipe = m.pipeline || [];
      if (pipe.length) return pipe.filter(function (p) { return p.stage === stage; });
      return Object.keys(m.stageMap || {}).filter(function (cid) { return m.stageMap[cid] === stage; }).map(function (cid) {
        return { candidateId: cid, applicationId: "", stage: stage };
      });
    }
    var cols = U.STAGES.map(function (st) {
      var items = itemsForStage(st[0]);
      var cards = items.map(function (p) {
        var c = TLStore.candidate(p.candidateId);
        if (!c) return "";
        return '<div class="kanban-card" draggable="true" data-cid="' + p.candidateId + '" data-app-id="' + (p.applicationId || "") + '"><b>' + U.esc(c.firstName + " " + c.lastName) + "</b><span>" + U.esc(c.title) + "</span></div>";
      }).join("");
      var n = items.length;
      return '<div class="kanban-col" data-stage="' + st[0] + '"><h4>' + st[1] + " <span class='badge'>" + n + "</span></h4>" + (cards || '<p style="color:var(--steel);font-size:12px">Déposez un candidat</p>') + "</div>";
    }).join("");
    return `
      <div class="crumbs"><a href="#/missions">Missions</a> / ${U.esc(m.title)}</div>
      <div class="page-head"><div><h1>${U.esc(m.title)}</h1><p>${U.esc((TLStore.client(m.clientId) || {}).name || "—")} · ${m.seats} poste(s) · échéance ${U.dateFr(m.due)} · ${U.badge(m.status)}</p></div>
        <div class="actions"><span class="badge orange">Valeur ${U.money(m.value)}</span><span class="badge info">Commission ${U.money(m.commission)}</span></div></div>
      <div class="kanban" data-mission="${m.id}">${cols}</div>
      <p style="color:var(--steel);margin-top:12px">Glissez les candidats d’une colonne à l’autre. Le statut est enregistré tout de suite.</p>`;
  }

  function hiringList() {
    return S().hiringRequests && S().hiringRequests.length ? S().hiringRequests : (S().missions || []).map(function (m) {
      return {
        id: m.id,
        title: m.title,
        seats: m.seats,
        status: m.statusKey || m.status,
        status_label: m.statusLabel || "",
        location: m.location,
        sector: m.sector,
        job_id: m.jobId,
        company_id: m.clientId,
        company_name: (TLStore.client(m.clientId) || {}).name,
        notes: m.notes,
        skills: m.skills,
        salary_display: m.salary
      };
    });
  }

  function viewHiring() {
    var list = hiringList();
    var rows = list.map(function (h) {
      var job = h.job_id ? TLStore.job(h.job_id) : null;
      return `<tr data-go="#/hiring/${h.id}"><td><b>${U.esc(h.title)}</b></td><td>${U.esc(h.company_name || (TLStore.client(h.company_id) || {}).name || "—")}</td><td>${U.esc(h.location || "")}</td><td>${h.seats || 1}</td><td>${U.badge(h.status)}</td><td>${job ? '<a href="#/jobs/' + job.id + '">' + U.esc(job.title) + "</a> " + U.badge(job.status) : "Pas encore d’offre"}</td></tr>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Besoins de recrutement</h1><p>Demandes reçues des entreprises, à convertir en offre.</p></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Besoin</th><th>Entreprise</th><th>Lieu</th><th>Postes</th><th>Statut</th><th>Offre Talendus</th></tr></thead><tbody>${rows || '<tr><td colspan="6">' + U.empty("Aucun besoin", "Les demandes envoyées depuis l’espace entreprise apparaissent ici.") + "</td></tr>"}</tbody></table></div></div>`;
  }

  function viewHiringDetail(id) {
    var list = hiringList();
    var h = list.find(function (x) { return x.id === id; });
    if (!h) return U.empty("Introuvable", "Ce besoin n’existe pas.");
    var job = h.job_id ? TLStore.job(h.job_id) : null;
    var statusOpts = HIRING_STATUSES.map(function (s) {
      return "<option value=\"" + s[0] + "\"" + (h.status === s[0] ? " selected" : "") + ">" + s[1] + "</option>";
    }).join("");
    return `
      <div class="crumbs"><a href="#/hiring">Besoins</a> / ${U.esc(h.title)}</div>
      <div class="page-head"><div><h1>${U.esc(h.title)}</h1><p>${U.esc(h.company_name || "")} · ${U.esc(h.location || "")} · ${U.badge(h.status)}</p></div>
        <div class="actions">
          ${h.company_id ? '<button class="btn btn-ghost" data-add-contract="' + h.company_id + '" data-role="' + U.esc(h.title || "") + '">Envoyer le mandat à signer</button>' : ""}
          ${h.job_id ? "" : '<button class="btn btn-orange" data-hire-convert="' + h.id + '">Créer l’offre (brouillon)</button>'}
          ${job && job.status !== "publiee" && job.id ? '<button class="btn btn-electric" data-job-act="publiee:' + job.id + '" data-hire-id="' + h.id + '">Publier sur le site</button>' : ""}
          ${job && job.slug ? '<a class="btn btn-ghost" href="' + U.esc(job.url || ("/emploi-" + job.slug + ".html")) + '" target="_blank" rel="noopener">Voir sur le site</a>' : ""}
        </div></div>
      <div class="grid grid-2">
        <div class="card card-pad">
          <h3>Brief entreprise</h3>
          <div class="row"><span>Secteur</span><b>${U.esc(h.sector || "—")}</b></div>
          <div class="row"><span>Compétences</span><b>${U.esc(h.skills || "—")}</b></div>
          <div class="row"><span>Rémunération</span><b>${U.esc(h.salary_display || "—")}</b></div>
          <p>${U.esc(h.notes || h.status_message || "")}</p>
        </div>
        <div class="card card-pad">
          <h3>Statut vu par l’entreprise</h3>
          <p>${U.esc(h.status_label || h.statusMessage || "")}</p>
          <label>Mettre à jour le statut</label>
          <select data-hire-status="${h.id}">${statusOpts}</select>
          <p style="margin-top:12px">Offre liée : ${job ? '<a href="#/jobs/' + job.id + '">' + U.esc(job.title) + "</a> " + U.badge(job.status) : "Aucune — créez l’offre, puis publiez-la pour qu’elle apparaisse sur emplois.html."}</p>
        </div>
      </div>`;
  }

  function viewMessages() {
    return `
      <div class="page-head"><div><h1>Messages</h1><p>Conversations avec les candidats et les entreprises.</p></div></div>
      <div id="msg-root" class="inbox"><div class="inbox-empty"><p>Chargement…</p></div></div>`;
  }

  function personaLabel(role) {
    var r = String(role || "").toUpperCase();
    if (r === "CANDIDATE") return "Candidat";
    if (r === "EMPLOYER") return "Entreprise";
    if (r === "FINANCE") return "Finance";
    if (r === "EDITOR") return "Éditeur";
    if (r === "RECRUITER") return "Recruteur";
    if (r === "ADMIN" || r === "SUPER_ADMIN") return "Admin";
    return role || "";
  }

  async function hydrateMessages() {
    var root = document.getElementById("msg-root");
    if (!root || !window.TalendusAPI) return;
    try {
      var threads = await window.TalendusAPI.request("/messages");
      var directory = await window.TalendusAPI.request("/messages/directory");
      var list = threads.data || [];
      var people = directory.data || [];
      var activeId = root.getAttribute("data-active") || (list[0] && list[0].user_id) || (people[0] && people[0].id) || "";
      function person(id) {
        return people.find(function (p) { return p.id === id; }) || list.find(function (t) { return t.user_id === id; }) || {};
      }
      function threadItem(th) {
        var on = th.user_id === activeId ? " is-on" : "";
        var unread = th.unread ? " is-unread" : "";
        var name = ((th.first_name || "") + " " + (th.last_name || "")).trim() || "Sans nom";
        return '<button type="button" class="inbox-thread' + on + unread + '" data-open-thread="' + U.esc(th.user_id) + '">' +
          U.avatar({ firstName: th.first_name || "?", lastName: th.last_name || "" }, "sm") +
          '<div class="who"><b>' + U.esc(name) + "</b><span>" + U.esc(th.last_message || personaLabel(th.role)) + "</span></div></button>";
      }
      var threadHtml = list.map(threadItem).join("");
      if (!threadHtml) {
        threadHtml = people.slice(0, 12).map(function (p) {
          return threadItem({ user_id: p.id, first_name: p.first_name, last_name: p.last_name, last_message: personaLabel(p.role), unread: false, role: p.role });
        }).join("") || '<p class="sub" style="padding:16px">L’annuaire est vide pour l’instant.</p>';
      }
      var current = person(activeId);
      var title = ((current.first_name || "") + " " + (current.last_name || "")).trim() || "Conversation";
      root.setAttribute("data-active", activeId);
      root.innerHTML =
        '<div class="inbox-list"><header><h3>Boîte de réception</h3><p class="sub" style="margin:0">' + list.length + " fil(s)</p></header>" +
        '<div class="inbox-threads">' + threadHtml + "</div></div>" +
        '<div class="inbox-pane"><header><div><h3>' + U.esc(title) + "</h3><span class='badge'>" + U.esc(personaLabel(current.role)) + "</span></div></header>" +
        '<div class="inbox-log" id="msg-thread"><div class="inbox-empty"><p>Ouvrez un fil pour lire les messages.</p></div></div>' +
        '<form class="inbox-compose" id="msg-form">' +
        '<input type="hidden" name="recipient_id" value="' + U.esc(activeId) + '">' +
        '<textarea name="body" required placeholder="Écrire un message…" rows="2"></textarea>' +
        '<button class="btn btn-orange" type="submit">Envoyer</button></form></div>';
      function loadThread(id) {
        var hidden = root.querySelector("[name=recipient_id]");
        if (hidden) hidden.value = id;
        root.setAttribute("data-active", id);
        root.querySelectorAll("[data-open-thread]").forEach(function (btn) {
          btn.classList.toggle("is-on", btn.getAttribute("data-open-thread") === id);
        });
        var head = root.querySelector(".inbox-pane header h3");
        var p = person(id);
        if (head) head.textContent = ((p.first_name || "") + " " + (p.last_name || "")).trim() || "Conversation";
        window.TalendusAPI.request("/messages/" + id).then(function (json) {
          var me = TLStore.me();
          var log = document.getElementById("msg-thread");
          var rows = json.data || [];
          if (!log) return;
          if (!rows.length) {
            log.innerHTML = '<div class="inbox-empty"><h3>Aucun message</h3><p>Écrivez le premier ci-dessous.</p></div>';
            return;
          }
          log.innerHTML = rows.map(function (m) {
            var mine = me && m.sender_id === me.id;
            return '<div class="bubble ' + (mine ? "is-mine" : "is-theirs") + '"><div class="meta">' +
              U.esc(m.sender_name || (mine ? "Vous" : "")) + "</div>" + U.esc(m.body) + "</div>";
          }).join("");
          log.scrollTop = log.scrollHeight;
        });
      }
      var form = document.getElementById("msg-form");
      if (form) form.onsubmit = function (e) {
        e.preventDefault();
        var d = U.formData(form);
        if (!d.recipient_id || !d.body) return;
        window.TalendusAPI.request("/messages", { method: "POST", body: { recipient_id: d.recipient_id, body: d.body } }).then(function () {
          U.toast("Envoyé.", "ok");
          hydrateMessages();
        }).catch(function (err) { U.toast((err && err.message) || "Envoi impossible.", "err"); });
      };
      root.querySelectorAll("[data-open-thread]").forEach(function (btn) {
        btn.onclick = function () { loadThread(btn.getAttribute("data-open-thread")); };
      });
      if (activeId) loadThread(activeId);
    } catch (err) {
      root.innerHTML = "<div class='inbox-empty'><p>Impossible de charger les messages.</p></div>";
    }
  }

  /* ---------- Content ---------- */
  function viewContent() {
    var labels = { pages: "Pages du site", blog: "Blog", temoignages: "Témoignages", faq: "FAQ", seo: "Contenu SEO" };
    var items = contentTab === "pages" ? (S().pages || []) : contentTab === "temoignages" ? (S().testimonials || []) : contentTab === "faq" ? (S().faqs || []) : [];
    var rows = "";
    if (contentTab === "pages") {
      rows = items.map(function (it) {
        return "<tr><td><b>" + U.esc(it.title) + "</b></td><td>" + U.esc(it.slug) + "</td><td>" + U.badge(it.status || "publie") + "</td><td>Site public</td>" +
          '<td><a class="btn btn-ghost btn-sm" href="' + U.esc(it.slug) + '" target="_blank" rel="noopener">Ouvrir</a></td></tr>';
      }).join("");
    } else if (contentTab === "seo") {
      rows = '<tr><td colspan="5">Le SEO des articles se gère dans l’onglet Blog. Les pages ci-contre sont le site déployé — pas un éditeur de HTML.</td></tr>';
    } else if (contentTab !== "blog") {
      rows = items.map(function (it) {
        return `<tr><td><b>${U.esc(it.title || it.q || it.author)}</b></td><td>${U.esc(it.slug || it.seo || it.role || "")}</td><td>${U.badge(it.status)}</td><td>${U.esc(it.updatedAt || "—")}</td>
        <td><button class="btn btn-ghost btn-sm" data-cms="edit:${contentTab}:${it.id}">Modifier</button>
            <button class="btn btn-ghost btn-sm" data-cms="toggle:${contentTab}:${it.id}">${it.status === "publie" || it.status === "publiee" ? "Dépublier" : "Publier"}</button>
            <button class="btn btn-ghost btn-sm" data-cms="arch:${contentTab}:${it.id}">Archiver</button></td></tr>`;
      }).join("") || '<tr><td colspan="5">Aucun élément. Utilisez « Créer » pour en ajouter un.</td></tr>';
    }
    if (contentTab === "blog") {
      rows = '<tr><td colspan="5">Chargement des articles…</td></tr>';
    }
    var canCreate = contentTab === "blog" || contentTab === "temoignages" || contentTab === "faq";
    return `
      <div class="page-head"><div><h1>Contenu</h1><p>${contentTab === "pages" ? "Pages du site public — le HTML est déployé avec le site. Témoignages, FAQ et blog s’enregistrent ici." : "CMS du site public — blog, témoignages et FAQ sont enregistrés dans l’API."}</p></div>
        <div class="actions">${canCreate ? '<button class="btn btn-orange" data-cms="new:' + contentTab + '">Créer</button>' : ""}</div></div>
      <div class="tabs">${Object.keys(labels).map(function (k) { return '<button class="tab' + (contentTab === k ? " is-on" : "") + '" data-ctab="' + k + '">' + labels[k] + "</button>"; }).join("")}</div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Titre</th><th>Slug / SEO</th><th>Statut</th><th>MAJ</th><th>Actions</th></tr></thead><tbody id="cms-rows">${rows}</tbody></table></div></div>`;
  }

  function blogStatusLabel(status) {
    var map = { DRAFT: "brouillon", PUBLISHED: "publie", SCHEDULED: "planifie", ARCHIVED: "archive" };
    return map[status] || (status || "").toLowerCase();
  }

  async function hydrateBlogCms() {
    var tbody = document.getElementById("cms-rows");
    if (!tbody || contentTab !== "blog" || !window.TalendusAPI) return;
    try {
      var json = await window.TalendusAPI.request("/admin/blog");
      var items = json.data || [];
      tbody.innerHTML = items.map(function (it) {
        return "<tr><td><b>" + U.esc(it.title) + "</b></td><td>" + U.esc(it.slug) + "</td><td>" + U.badge(blogStatusLabel(it.status)) + "</td><td>" + U.esc((it.updated_at || "").slice(0, 10)) + "</td>" +
          '<td><button class="btn btn-ghost btn-sm" data-cms="edit:blog:' + it.id + '">Modifier</button>' +
          '<button class="btn btn-ghost btn-sm" data-cms="prev:blog:' + it.slug + '">Prévisualiser</button>' +
          '<button class="btn btn-ghost btn-sm" data-cms="toggle:blog:' + it.id + '" data-status="' + it.status + '">' + (it.status === "PUBLISHED" ? "Dépublier" : "Publier") + "</button>" +
          '<button class="btn btn-ghost btn-sm" data-cms="arch:blog:' + it.id + '">Archiver</button></td></tr>';
      }).join("") || '<tr><td colspan="5">Aucun article. Créez le premier depuis « Créer ».</td></tr>';
    } catch (err) {
      tbody.innerHTML = "<tr><td colspan='5'>Impossible de charger le blog API. Vérifiez la connexion.</td></tr>";
    }
  }

  /* ---------- Finance ---------- */
  function viewFinance() {
    var inv = S().invoices;
    var pay = S().payments;
    var byStatus = function (s) { return inv.filter(function (i) { return i.status === s; }); };
    var tabs = { factures: "Factures", paiements: "Paiements", commissions: "Commissions" };
    var body = "";
    if (financeTab === "factures") {
      body = `<div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>N°</th><th>Client</th><th>Mission</th><th>Montant</th><th>Date</th><th>Échéance</th><th>Statut</th><th></th></tr></thead><tbody>${inv.map(function (i) {
        var cl = TLStore.client(i.clientId); var m = TLStore.mission(i.missionId);
        var iid = invoiceApiId(i);
        var send = (i.status === "brouillon") ? '<button class="btn btn-ghost btn-sm" data-inv-send="' + iid + '">Envoyer</button>' : "";
        var editInv = (i.status === "brouillon" || i.status === "envoyee") ? '<button class="btn btn-ghost btn-sm" data-inv-edit="' + iid + '">Modifier</button>' : "";
        var payBtn = (i.status === "envoyee" || i.status === "en-attente" || i.status === "en-retard") ? '<button class="btn btn-orange btn-sm" data-inv-pay="' + iid + '" data-inv-amount="' + i.amount + '">Encaisser</button>' : "";
        var pdf = iid ? '<button class="btn btn-ghost btn-sm" data-dl-doc="/api/invoices/' + iid + '/pdf" data-dl-name="' + U.esc(i.id) + '.pdf">PDF</button>' : "";
        return "<tr><td>" + U.esc(i.id) + "</td><td>" + U.esc(cl ? cl.name : "—") + "</td><td>" + U.esc(m ? m.title : "—") + "</td><td>" + U.money(i.amount) + "</td><td>" + U.dateFr(i.date) + "</td><td>" + U.dateFr(i.due) + "</td><td>" + U.badge(i.status) + "</td><td>" + pdf + editInv + send + payBtn + "</td></tr>";
      }).join("") || '<tr><td colspan="8">' + U.empty("Aucune facture", "Créez une facture depuis le bouton ci-dessus.") + "</td></tr>"}</tbody></table></div></div>`;
    } else if (financeTab === "paiements") {
      var pending = byStatus("en-attente").concat(byStatus("envoyee"));
      var late = byStatus("en-retard");
      body = `<div class="grid grid-3" style="margin-bottom:16px">${kpi("Reçus", U.money(pay.reduce(function (s, p) { return s + p.amount; }, 0)))}${kpi("En attente", U.money(pending.reduce(function (s, i) { return s + i.amount; }, 0)))}${kpi("En retard", U.money(late.reduce(function (s, i) { return s + i.amount; }, 0)))}</div>
        <div class="card card-pad"><h3>Historique des paiements</h3>${pay.map(function (p) { return "<p>" + U.dateFr(p.date) + " · " + p.invoiceId + " · " + U.money(p.amount) + " · " + p.method + "</p>"; }).join("")}</div>`;
    } else {
      var rows = S().missions.map(function (m) {
        var recu = S().invoices.filter(function (i) { return i.missionId === m.id && i.status === "payee"; }).reduce(function (s, i) { return s + i.amount; }, 0);
        return "<tr><td>" + U.esc(m.title) + "</td><td>" + U.esc((TLStore.client(m.clientId) || {}).name || "—") + "</td><td>" + U.esc(TLStore.name(m.recruiterId)) + "</td><td>" + U.money(m.commission) + "</td><td>" + U.money(recu) + "</td></tr>";
      }).join("");
      body = `<div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Mission</th><th>Client</th><th>Recruteur</th><th>Commission prévue</th><th>Commission reçue</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
    }
    return `
      <div class="page-head"><div><h1>Finance</h1><p>Factures CAD, TPS/TVQ, paiements et commissions.</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="invoice">Nouvelle facture</button><button class="btn btn-ghost" data-export-fin>Exporter</button></div></div>
      <div class="grid grid-4" style="margin-bottom:16px">
        ${kpi("Payées", byStatus("payee").length)}
        ${kpi("En attente", byStatus("en-attente").length + byStatus("envoyee").length)}
        ${kpi("En retard", byStatus("en-retard").length)}
        ${kpi("Brouillons", byStatus("brouillon").length)}
      </div>
      <div class="tabs">${Object.keys(tabs).map(function (k) { return '<button class="tab' + (financeTab === k ? " is-on" : "") + '" data-ftab="' + k + '">' + tabs[k] + "</button>"; }).join("")}</div>
      ${body}`;
  }

  function interviewTypeLabel(i) {
    return i.type || i.typeKey || "Talendus";
  }

  function interviewStatusKey(i) {
    return (i.status || "SCHEDULED").toUpperCase();
  }

  function viewInterviews() {
    var list = S().interviews || [];
    var cols = [
      ["SCHEDULED", "Planifiés"],
      ["CONFIRMED", "Confirmés"],
      ["COMPLETED", "Terminés"],
      ["CANCELLED", "Annulés / absents"]
    ];
    var board = cols.map(function (col) {
      var items = list.filter(function (i) {
        var st = interviewStatusKey(i);
        if (col[0] === "CANCELLED") return st === "CANCELLED" || st === "NO_SHOW";
        return st === col[0];
      });
      var cards = items.map(function (i) {
        var c = TLStore.candidate(i.candidateId);
        var name = i.candidateName || (c ? (c.firstName + " " + c.lastName) : "Candidat");
        var when = i.at || "";
        var join = callButtons(i);
        var meet = i.meetingUrl ? ' <a class="btn btn-ghost btn-sm" href="' + U.esc(i.meetingUrl) + '" target="_blank" rel="noopener">Lien visio</a>' : "";
        var face = U.avatar({ firstName: name.split(" ")[0], lastName: name.split(" ").slice(1).join(" "), userId: i.candidateUserId });
        return '<div class="int-card">' + face + "<div><b>" + U.esc(name) + "</b><span>" + U.esc(interviewTypeLabel(i)) + " · " + U.esc(when) + "</span><span>" + U.esc(i.location || "") + "</span></div>" +
          '<div class="int-actions">' + join + meet + "</div></div>";
      }).join("") || '<p style="color:var(--steel);font-size:12px">Aucun entretien.</p>';
      return '<div class="int-col"><h4>' + col[1] + ' <span class="badge">' + items.length + "</span></h4>" + cards + "</div>";
    }).join("");
    return `
      <div class="page-head"><div><h1>Entretiens</h1><p>Lancez l’appel depuis la carte. Le candidat ne voit Rejoindre que lorsque vous êtes dans la salle.</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="interview">Planifier</button></div></div>
      <div class="int-board">${board}</div>`;
  }

  /* ---------- Analytics ---------- */
  function viewAnalytics() {
    var st = S();
    var cands = st.candidates.filter(function (c) {
      if (analyticsRecruiter && c.recruiterId !== analyticsRecruiter) return false;
      if (analyticsSector && c.sector !== analyticsSector) return false;
      return true;
    });
    var placed = cands.filter(function (c) { return c.status === "place"; }).length;
    var interviews = st.interviews.length;
    var apps = st.jobs.reduce(function (s, j) { return s + j.applications; }, 0);
    var revenue = st.invoices.filter(function (i) { return i.status === "payee"; }).reduce(function (s, i) { return s + i.amount; }, 0);
    return `
      <div class="page-head"><div><h1>Statistiques</h1><p>Visites du site, interactions et activité interne.</p></div>
        <div class="actions"><button class="btn btn-ghost" data-export-an>Exporter CSV</button></div></div>
      <div class="filters">
        ${["jour","semaine","mois","trimestre","annee"].map(function (p) { return '<button class="btn btn-sm ' + (period === p ? "btn-orange" : "btn-ghost") + '" data-period="' + p + '">' + p + "</button>"; }).join("")}
        <select id="an-rec"><option value="">Recruteur</option>${st.users.filter(function (u) { return u.role !== "editor"; }).map(function (u) { return "<option value=\"" + u.id + "\"" + (analyticsRecruiter === u.id ? " selected" : "") + ">" + u.firstName + " " + u.lastName + "</option>"; }).join("")}</select>
        <select id="an-sec"><option value="">Secteur</option>${unique(st.candidates, "sector").map(function (s) { return "<option" + (analyticsSector === s ? " selected" : "") + ">" + s + "</option>"; }).join("")}</select>
      </div>
      <div class="grid grid-4" id="an-traffic" style="margin-bottom:16px">
        ${kpi("Visites", "…")}
        ${kpi("Interactions", "…")}
        ${kpi("Candidatures site", "…")}
        ${kpi("Messages", "…")}
      </div>
      <div class="grid grid-4" style="margin-bottom:16px">
        ${kpi("Candidats", cands.length)}
        ${kpi("Clients", st.clients.length)}
        ${kpi("Offres", st.jobs.length, apps + " candidatures")}
        ${kpi("Entretiens", interviews, placed + " placements")}
      </div>
      <div class="grid grid-4" style="margin-bottom:16px">
        ${kpi("Taux de placement", Math.round(placed / Math.max(1, cands.length) * 100) + " %")}
        ${kpi("Revenus encaissés", U.money(revenue))}
        ${kpi("Contacts (site)", "…", "formulaire / appel")}
        ${kpi("Recherches", "…")}
      </div>
      <div class="grid grid-2">
        <div class="card card-pad"><h3>Revenus (interne)</h3>${U.barChart(st.monthly.months, st.monthly.revenue, "#ff6b00")}</div>
        <div class="card card-pad" id="an-pages"><h3>Pages les plus vues</h3><p class="sub">Chargement…</p></div>
      </div>
      <div class="card card-pad" style="margin-top:16px"><h3>Placements par recruteur</h3>
        <table class="data"><thead><tr><th>Recruteur</th><th>Placements</th><th>Commission reçue</th></tr></thead><tbody>
        ${st.users.filter(function (u) { return u.role === "recruiter" || u.role === "admin"; }).map(function (u) {
          var n = st.candidates.filter(function (c) { return c.recruiterId === u.id && c.status === "place"; }).length;
          var recu = st.missions.filter(function (m) { return m.recruiterId === u.id; }).reduce(function (s, m) {
            return s + st.invoices.filter(function (i) { return i.missionId === m.id && i.status === "payee"; }).reduce(function (a, i) { return a + i.amount; }, 0);
          }, 0);
          return "<tr><td>" + U.esc(u.firstName + " " + u.lastName) + "</td><td>" + n + "</td><td>" + U.money(recu) + "</td></tr>";
        }).join("")}
        </tbody></table>
      </div>`;
  }

  async function hydrateAnalytics() {
    var box = document.getElementById("an-traffic");
    if (!box || !live()) return;
    try {
      var json = await api().request("/admin/analytics?period=" + encodeURIComponent(period));
      var d = json.data || {};
      var kpis = box.parentElement ? box : box;
      box.innerHTML = kpi("Visites", d.visits || 0, "période " + period) +
        kpi("Interactions", d.interactions || 0) +
        kpi("Candidatures", d.applies || 0, (d.new_applications || 0) + " dossiers") +
        kpi("Messages", d.messages || 0);
      var extras = document.querySelectorAll(".grid.grid-4")[2];
      if (extras) {
        var cells = extras.querySelectorAll(".kpi");
        if (cells[2]) cells[2].outerHTML = kpi("Contacts (site)", d.contacts || 0);
        if (cells[3]) cells[3].outerHTML = kpi("Recherches", d.searches || 0);
      }
      var pages = document.getElementById("an-pages");
      if (pages) {
        var rows = (d.top_pages || []).map(function (p) {
          return "<tr><td>" + U.esc(p.path) + "</td><td>" + p.views + "</td></tr>";
        }).join("") || "<tr><td colspan='2'>Pas encore de visites enregistrées.</td></tr>";
        pages.innerHTML = "<h3>Pages les plus vues</h3><table class='data'><thead><tr><th>Page</th><th>Vues</th></tr></thead><tbody>" + rows + "</tbody></table>";
      }
    } catch (err) {
      box.innerHTML = kpi("Visites", "—") + kpi("Interactions", "—") + kpi("Candidatures", "—") + kpi("Messages", "—");
    }
  }

  function staffRoleLabel(role) {
    return ({ RECRUITER: "Recruteur", FINANCE: "Finance", EDITOR: "Éditeur", ADMIN: "Admin", SUPER_ADMIN: "Super-admin" })[role] || role;
  }

  async function hydrateTeam() {
    var list = document.getElementById("adm-team-list");
    var form = document.getElementById("adm-team-form");
    if (form && api()) {
      form.onsubmit = function (e) {
        e.preventDefault();
        var d = U.formData(form);
        api().request("/admin/users", {
          method: "POST",
          body: {
            email: d.email,
            first_name: d.first_name,
            last_name: d.last_name,
            password: d.password,
            role: d.role,
            title: d.title || null
          }
        }).then(function () {
          U.toast("Accès créé.", "ok");
          form.reset();
          hydrateTeam();
        }).catch(function (err) { U.toast((err && err.message) || "Création impossible.", "err"); });
      };
    }
    if (!list || !api()) return;
    try {
      var json = await api().request("/admin/users");
      var rows = json.data || [];
      var staff = rows.filter(function (u) {
        return ["RECRUITER", "FINANCE", "EDITOR", "ADMIN", "SUPER_ADMIN"].indexOf(u.role) !== -1;
      });
      list.innerHTML = '<div class="card-head"><h3>Comptes internes</h3></div>' + staff.map(function (u) {
        var roleCtl = u.role === "SUPER_ADMIN"
          ? '<span class="badge">Super-admin</span>'
          : '<select data-team-role="' + U.esc(u.id) + '">' +
            [["RECRUITER", "Recruteur"], ["FINANCE", "Finance"], ["EDITOR", "Éditeur"], ["ADMIN", "Admin"]].map(function (opt) {
              return "<option value=\"" + opt[0] + "\"" + (u.role === opt[0] ? " selected" : "") + ">" + opt[1] + "</option>";
            }).join("") + "</select>";
        return '<div class="team-row"><div><b>' + U.esc((u.first_name || "") + " " + (u.last_name || "")) + "</b><div class='sub'>" +
          U.esc(u.email) + " · " + U.esc(staffRoleLabel(u.role)) + (u.is_active ? "" : " · désactivé") +
          "</div></div><div>" + roleCtl + " " +
          (u.role === "SUPER_ADMIN" ? "" : '<button type="button" class="btn btn-ghost btn-sm" data-team-active="' + U.esc(u.id) + '" data-on="' + (u.is_active ? "0" : "1") + '">' +
          (u.is_active ? "Désactiver" : "Activer") + "</button>") + "</div></div>";
      }).join("") || "<p class='sub'>Aucun compte interne.</p>";
      list.querySelectorAll("[data-team-role]").forEach(function (sel) {
        sel.onchange = function () {
          api().request("/admin/users/" + sel.getAttribute("data-team-role") + "/role", { method: "POST", body: { role: sel.value } })
            .then(function () { U.toast("Niveau mis à jour.", "ok"); hydrateTeam(); })
            .catch(function (err) { U.toast((err && err.message) || "Changement impossible.", "err"); hydrateTeam(); });
        };
      });
      list.querySelectorAll("[data-team-active]").forEach(function (btn) {
        btn.onclick = function () {
          api().request("/admin/users/" + btn.getAttribute("data-team-active"), {
            method: "PATCH",
            body: { is_active: btn.getAttribute("data-on") === "1" }
          }).then(function () { U.toast("Compte mis à jour.", "ok"); hydrateTeam(); })
            .catch(function (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); });
        };
      });
    } catch (err) {
      list.innerHTML = "<p class='sub'>Impossible de charger l’équipe.</p>";
    }
  }

  function viewServices() {
    return `
      <div class="page-head"><div><h1>Services</h1><p>État des branchements : courriel, paiement, Google, etc.</p></div></div>
      <div id="svc-todos"></div>
      <div id="svc-grid" class="svc-grid"><p class="sub">Chargement…</p></div>`;
  }

  function svcStateLabel(state) {
    return { active: "En service", configured: "Clés présentes, pas encore allumé", prepared: "Pas encore branché" }[state] || state;
  }

  async function hydrateServices() {
    var grid = document.getElementById("svc-grid");
    var todos = document.getElementById("svc-todos");
    if (!grid) return;
    if (!live()) {
      grid.innerHTML = U.empty("Hors ligne", "Connectez-vous au serveur pour voir l’état réel des services.");
      return;
    }
    try {
      var json = await api().request("/integrations/overview");
      var data = json.data || {};
      if (todos) {
        todos.innerHTML = (data.todos || []).map(function (item) {
          return '<article class="svc-todo"><h3>' + U.esc(item.title) + "</h3><p>" + U.esc(item.detail) + "</p></article>";
        }).join("") || '<article class="svc-todo is-ok"><h3>Rien d’urgent</h3><p>Les services essentiels tournent.</p></article>';
      }
      grid.innerHTML = (data.providers || []).map(function (row) {
        return '<article class="svc-card is-' + U.esc(row.state) + '">' +
          "<header><h3>" + U.esc(row.label) + '</h3><span class="svc-pill">' + U.esc(svcStateLabel(row.state)) + "</span></header>" +
          "<p>" + U.esc(row.next_step || row.message || "") + "</p></article>";
      }).join("");
    } catch (err) {
      grid.innerHTML = "<p>Impossible de lire les services. Réessayez.</p>";
    }
  }

  function viewNotifications() {
    return `<div class="page-head"><div><h1>Notifications</h1><p>Centre d’alertes opérationnelles</p></div>
      <div class="actions"><button class="btn btn-ghost" id="mark-all">Tout marquer lu</button></div></div>
      <div class="card">${S().notifications.length ? S().notifications.map(function (n) {
        return '<div class="n-item ' + (n.read ? "" : "unread") + '"><a href="' + U.esc(n.href || "#") + '"><b>' + U.esc(n.text) + "</b></a><div style='color:var(--steel);font-size:12px'>" + U.esc(n.at) + " · " + U.esc(n.type) + "</div></div>";
      }).join("") : U.empty("Aucune notification", "Les alertes opérationnelles apparaissent ici.")}</div>`;
  }

  function viewSettings() {
    var me = TLStore.me();
    var admin = me.role === "admin";
    var access = [
      ["Tableau de bord", true, true, false, true],
      ["Candidats, clients, offres, besoins, missions, messages", true, false, false, true],
      ["Finance et factures", false, true, false, true],
      ["Contenu du site", false, false, true, true],
      ["Statistiques", false, true, false, true],
      ["Services (courriel, paiement, Google…)", false, true, false, true],
      ["Notifications internes", true, true, true, true],
      ["Paramètres du compte", true, true, true, true],
      ["Paramètres de la plateforme", false, false, false, true]
    ];
    var marks = function (row) {
      return row.slice(1).map(function (on) {
        return "<td>" + (on ? "Oui" : "—") + "</td>";
      }).join("");
    };
    var personaLead = {
      admin: "Configuration, équipe et accès.",
      recruiter: "Mandats, candidats et clients.",
      finance: "Facturation et statistiques.",
      editor: "Contenu public du site."
    };
    return `
      <div class="page-head"><div><h1>Paramètres</h1><p>${U.esc(personaLead[me.role] || personaLead.recruiter)}</p></div></div>
      <div class="settings-tabs" role="tablist">
        <button type="button" class="settings-tab is-active" data-stab="account">Compte</button>
        <button type="button" class="settings-tab" data-stab="security">Sécurité</button>
        <button type="button" class="settings-tab" data-stab="access">Niveaux d’accès</button>
        ${admin ? '<button type="button" class="settings-tab" data-stab="team">Équipe</button>' : ""}
        ${admin ? '<button type="button" class="settings-tab" data-stab="email">Courriel</button>' : ""}
        ${admin ? '<button type="button" class="settings-tab" data-stab="platform">Plateforme</button>' : ""}
      </div>
      <div class="settings-panel" data-spanel="account">
        <div class="card card-pad">
          <div class="card-head"><h3>Votre compte</h3></div>
          <p class="sub">${U.esc(me.email)} · ${roleLabel(me.role)}</p>
          <form id="adm-prefs" class="form-grid" style="grid-template-columns:1fr">
            <label class="check"><input type="checkbox" name="notify_email" checked> Courriel</label>
            <label class="check"><input type="checkbox" name="notify_in_app" checked> Dans l’application</label>
            <label class="check"><input type="checkbox" name="notify_application" checked> Nouvelles candidatures</label>
            <label class="check"><input type="checkbox" name="notify_message" checked> Messages</label>
            <label class="check"><input type="checkbox" name="notify_interview" checked> Entretiens</label>
            <button class="btn btn-orange" type="submit">Enregistrer</button>
          </form>
        </div>
      </div>
      <div class="settings-panel" data-spanel="security" hidden>
        <div class="card card-pad">
          <div class="card-head"><h3>Mot de passe</h3></div>
          <form id="adm-pass" class="form-grid" style="grid-template-columns:1fr">
            ${U.field("Mot de passe actuel", "current_password", "", "password")}
            ${U.field("Nouveau mot de passe", "new_password", "", "password")}
            <button class="btn btn-orange" type="submit">Mettre à jour</button>
          </form>
        </div>
        <div class="card card-pad" id="adm-sessions" style="margin-top:16px"><p class="sub">Sessions…</p></div>
      </div>
      <div class="settings-panel" data-spanel="access" hidden>
        <div class="card">
          <div class="card-pad"><p>Chaque rôle n’ouvre que les menus nécessaires.</p></div>
          <div class="table-wrap"><table class="data"><thead><tr><th>Zone</th><th>Recruteur</th><th>Finance</th><th>Éditeur</th><th>Admin</th></tr></thead><tbody>
          ${access.map(function (row) { return "<tr><td>" + U.esc(row[0]) + "</td>" + marks(row) + "</tr>"; }).join("")}
          </tbody></table></div>
        </div>
      </div>
      ${admin ? `<div class="settings-panel" data-spanel="team" hidden>
        <div class="card card-pad">
          <div class="card-head"><h3>Créer un accès</h3></div>
          <form id="adm-team-form" class="form-grid">
            ${U.field("Prénom", "first_name")}
            ${U.field("Nom", "last_name")}
            ${U.field("Courriel", "email", "", "email")}
            ${U.field("Mot de passe initial", "password", "", "password")}
            ${U.field("Niveau", "role", { options: [
              { v: "RECRUITER", l: "Recruteur" },
              { v: "FINANCE", l: "Finance" },
              { v: "EDITOR", l: "Éditeur" },
              { v: "ADMIN", l: "Admin" }
            ], selected: "RECRUITER" }, "select")}
            ${U.field("Titre", "title", "Recruteur")}
            <button class="btn btn-orange" type="submit">Créer l’accès</button>
          </form>
        </div>
        <div class="card card-pad" id="adm-team-list" style="margin-top:16px"><p class="sub">Chargement de l’équipe…</p></div>
      </div>` : ""}
      ${admin ? `<div class="settings-panel" data-spanel="email" hidden>
        <div class="card card-pad smtp-guide">
          <div class="card-head"><h3>Courriel opérationnel</h3></div>
          <p class="sub">Tous les e-mails destinés aux recruteurs et aux candidats partent de <b>info@talendus.ca</b> et apparaissent aussi dans le fil de messages. Un clic admin ou recruteur suffit : le message est rédigé automatiquement, avec le lien vers l’action.</p>
          <h4>Google Workspace (Google Pro) — à faire une seule fois</h4>
          <p class="sub">Talendus envoie via SMTP de la boîte <b>info@talendus.ca</b>. On utilise un <b>mot de passe d’application</b>, jamais le mot de passe de connexion Google.</p>
          <ol>
            <li>Vérifiez que le domaine <code>talendus.ca</code> est bien dans Google Workspace et que la boîte <code>info@talendus.ca</code> existe (console d’admin → Annuaire → Utilisateurs).</li>
            <li>Connectez-vous à la console d’admin Google (<code>admin.google.com</code>) avec un super-admin.</li>
            <li>Sécurité → Authentification → <b>Validation en 2 étapes</b> : autorisez les utilisateurs à l’activer (si ce n’est pas déjà fait).</li>
            <li>Sécurité → Authentification → <b>Mots de passe d’application</b> : autorisez les utilisateurs à en créer.</li>
            <li>Ouvrez Gmail avec <code>info@talendus.ca</code> → Paramètres (engrenage) → Voir tous les paramètres → <b>Transfert et POP/IMAP</b> → activez <b>IMAP</b> → Enregistrer.</li>
            <li>Toujours connecté en <code>info@talendus.ca</code>, allez sur <code>myaccount.google.com/security</code> → activez la <b>validation en 2 étapes</b> si elle n’est pas déjà active.</li>
            <li>Puis <code>myaccount.google.com/apppasswords</code> → créer un mot de passe d’application nommé <b>Talendus</b>. Google affiche 16 lettres. Copiez-les (sans espaces).</li>
            <li>Dans le formulaire ci-dessous, collez exactement :
              <ul>
                <li>Activer l’envoi : <b>Oui — envoyer vraiment</b></li>
                <li>Serveur : <code>smtp.gmail.com</code></li>
                <li>Port : <code>587</code></li>
                <li>Identifiant : <code>info@talendus.ca</code></li>
                <li>Mot de passe : les 16 lettres du mot de passe d’application</li>
                <li>Expéditeur : <code>Talendus &lt;info@talendus.ca&gt;</code></li>
                <li>TLS : <b>oui</b></li>
              </ul>
            </li>
            <li>Cliquez <b>Enregistrer le courriel</b>, puis <b>Envoyer un test</b>.</li>
            <li>Ouvrez Gmail <code>info@talendus.ca</code> (et les spams). Le journal sous le formulaire doit passer à « SENT ». Les réponses des candidats arriveront dans cette même boîte.</li>
          </ol>
          <p class="sub">Si « Mots de passe d’application » n’apparaît pas : la validation en 2 étapes n’est pas encore active sur info@, ou l’admin Workspace ne l’a pas autorisée. Les deux doivent être ouvertes avant de réessayer le lien <code>myaccount.google.com/apppasswords</code>.</p>
          <p class="sub">Variante serveur (Render) : les mêmes valeurs existent en variables <code>EMAIL_*</code>. Un champ rempli ici prime sur la variable.</p>
        </div>
        <div class="card card-pad" style="margin-top:16px">
          <div class="card-head"><h3>Réglages SMTP</h3></div>
          <div id="adm-smtp"><p class="sub">Chargement…</p></div>
        </div>
        <div class="card card-pad" style="margin-top:16px">
          <div class="card-head"><h3>Journal des e-mails</h3></div>
          <div id="adm-email-log" class="smtp-log"><p class="sub">Chargement…</p></div>
        </div>
      </div>` : ""}
      ${admin ? `<div class="settings-panel" data-spanel="platform" hidden>
        <div class="card card-pad">
          <div class="card-head"><h3>Plateforme</h3></div>
          <p class="sub">Raison sociale, NEQ, n° TPS/TVQ et autres réglages de facturation.</p>
          <div id="adm-platform"><p class="sub">Chargement…</p></div>
          ${TLStore.isLive() ? "" : '<p style="margin-top:16px"><button class="btn btn-danger" id="reset-demo">Réinitialiser les données démo</button></p>'}
        </div>
      </div>` : ""}`;
  }

  function viewProfile() {
    var me = TLStore.me();
    var mine = S().candidates.filter(function (c) { return c.recruiterId === me.id; });
    return `
      <div class="page-head"><div><h1>Profil</h1><p>${U.esc(me.title)}</p></div></div>
      <div class="grid grid-2">
        <div class="card card-pad">${U.avatar(me, "lg")}<h3>${U.esc(me.firstName + " " + me.lastName)}</h3>
          <p>${U.esc(me.email)}<br>${roleLabel(me.role)}</p>
          <form id="adm-profile" class="form-grid" style="grid-template-columns:1fr">
            ${U.field("Prénom", "first_name", me.firstName)}
            ${U.field("Nom", "last_name", me.lastName)}
            ${U.field("Titre", "title", me.title || "")}
            ${U.field("Téléphone", "phone", me.phone || "")}
            <button class="btn btn-orange" type="submit">Enregistrer</button>
          </form>
        </div>
        <div class="card card-pad"><h3>Statistiques personnelles</h3>
          ${kpi("Candidats suivis", mine.length)}
          ${kpi("Placements", mine.filter(function (c) { return c.status === "place"; }).length)}
        </div>
      </div>`;
  }

  /* ---------- Creates / edits ---------- */
  function openCreate(type) {
    var me = TLStore.me();
    if (type === "candidate" && !TLStore.can("candidates")) return deny();
    if (type === "client" && !TLStore.can("clients")) return deny();
    if (type === "job" && !TLStore.can("jobs")) return deny();
    if (type === "mission" && !TLStore.can("missions")) return deny();
    if (type === "invoice" && !TLStore.can("finance")) return deny();
    if (type === "interview" && !TLStore.can("interviews") && !TLStore.can("candidates")) return deny();

    var body = "";
    if (type === "candidate") {
      body = '<form id="cf" class="form-grid">' + U.field("Prénom", "firstName") + U.field("Nom", "lastName") + U.field("Courriel", "email", "", "email") + U.field("Téléphone", "phone") + U.field("Ville", "city") + U.field("Poste recherché", "title") + U.field("Secteur", "sector", { options: unique(S().candidates, "sector").concat(["Production", "Entrepôt", "Maintenance"]), selected: "" }, "select") + U.field("Statut", "status", { options: ["nouveau","a-contacter","qualifie"].map(function (s) { return { v: s, l: U.STATUS[s][0] }; }), selected: "nouveau" }, "select") + "</form>";
    } else if (type === "client") {
      body = '<form id="cf" class="form-grid">' + U.field("Entreprise", "name") + U.field("Raison sociale", "legal_name") + U.field("Adresse", "address", "", "text", "full") + U.field("Ville", "city") + U.field("Province", "province", "Québec") + U.field("Secteur", "sector") + U.field("Contact", "contact") + U.field("Courriel", "email") + U.field("Téléphone", "phone") + "</form>";
    } else if (type === "job") {
      if (!S().clients.length) { U.toast("Créez d’abord une entreprise cliente.", "err"); return; }
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Entreprise", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: firstId(S().clients) }, "select") + U.field("Ville", "city") + U.field("Salaire", "salary") + jobVocabFields() + U.field("Description", "description", "", "textarea", "full") + "</form>";
    } else if (type === "mission") {
      if (!S().clients.length) { U.toast("Créez d’abord une entreprise cliente.", "err"); return; }
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: firstId(S().clients) }, "select") + U.field("Offre", "jobId", { options: [{ v: "", l: "Sans offre liée" }].concat(S().jobs.map(function (j) { return { v: j.id, l: j.title }; })), selected: firstId(S().jobs) }, "select") + U.field("Nombre de postes", "seats", "1", "number") + "</form>";
    } else if (type === "interview") {
      if (!S().candidates.length) { U.toast("Aucun candidat à convier.", "err"); return; }
      var now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      body = '<form id="cf" class="form-grid">' +
        U.field("Candidat", "candidate_id", { options: S().candidates.map(function (c) { return { v: c.id, l: c.firstName + " " + c.lastName }; }), selected: firstId(S().candidates) }, "select") +
        U.field("Date et heure", "scheduled_at", now.toISOString().slice(0, 16), "datetime-local") +
        U.field("Type", "type", { options: [{ v: "TALENDUS", l: "Visio Talendus" }, { v: "VIDEO", l: "Visio" }, { v: "PHONE", l: "Téléphone" }, { v: "CLIENT", l: "Chez le client" }, { v: "ONSITE", l: "Sur place" }], selected: "TALENDUS" }, "select") +
        U.field("Lieu / précisions", "location", "Visio Talendus") +
        '<label class="check" style="grid-column:1/-1"><input type="checkbox" name="candidate_can_start"> Autoriser le candidat à lancer l’appel</label>' +
        "<p class=\"sub\" style=\"grid-column:1/-1\">Sans cette case, le candidat peut seulement rejoindre une fois que vous avez ouvert la salle.</p>" +
        "</form>";
    } else {
      if (!S().clients.length) { U.toast("Créez d’abord une entreprise cliente.", "err"); return; }
      var today = new Date().toISOString().slice(0, 10);
      var due = new Date();
      due.setDate(due.getDate() + 30);
      body = '<form id="cf" class="form-grid">' +
        U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: firstId(S().clients) }, "select") +
        U.field("Mission", "missionId", { options: [{ v: "", l: "Sans mission" }].concat(S().missions.map(function (m) { return { v: m.id, l: m.title }; })), selected: "" }, "select") +
        U.field("Montant avant taxes (CAD)", "amount", "5000", "number") +
        U.field("Taxes", "tax_rate_bp", { options: [{ v: "14975", l: "TPS 5 % + TVQ 9,975 % (Québec)" }, { v: "0", l: "Sans taxes" }], selected: "14975" }, "select") +
        U.field("Date de facture", "issued_at", today, "date") +
        U.field("Échéance", "due_date", due.toISOString().slice(0, 10), "date") +
        U.field("Intitulé / notes (sur la facture)", "notes", "Honoraires de recrutement", "textarea", "full") +
        "</form>";
    }

    U.modal({
      title: "Créer",
      body: body,
      footer: '<button class="btn btn-ghost" data-close>Annuler</button>' + (type === "job" ? '<button class="btn btn-ghost" id="save">Brouillon</button><button class="btn btn-orange" id="save-pub">Créer et publier</button>' : '<button class="btn btn-orange" id="save">Enregistrer</button>'),
      onMount: function (box, close) {
        async function persistCreate(publish) {
          var d = U.formData(box.querySelector("#cf"));
          try {
            if (type === "candidate" && window.TalendusAPI) {
              await window.TalendusAPI.createCandidate({
                email: d.email,
                first_name: d.firstName,
                last_name: d.lastName,
                phone: d.phone,
                city: d.city,
                title: d.title,
                sector: d.sector
              });
              if (d.status && d.status !== "nouveau") {
                await refreshLive();
                var fresh = S().candidates.find(function (c) { return c.email === d.email; });
                if (fresh) await setCandidateStatus(fresh, d.status);
              } else {
                await refreshLive();
              }
              close();
              U.toast("Candidat créé — visible dans l’espace talent une fois connecté.", "ok");
              render();
              return;
            }
            if (type === "job" && window.TalendusAPI && d.clientId) {
              var created = await window.TalendusAPI.request("/jobs", {
                method: "POST",
                body: { title: d.title, company_id: d.clientId, location: d.city, salary_display: d.salary, description: d.description, contract_type: d.contract_type, schedule: d.schedule, shift: d.shift }
              });
              var job = created && created.data;
              if (publish && job && job.id) {
                await window.TalendusAPI.request("/jobs/" + job.id + "/publish", { method: "POST" });
              }
              await refreshLive();
              close();
              U.toast(publish ? "Offre publiée — elle apparaît sur le site public." : "Offre créée (brouillon).", "ok");
              render();
              return;
            }
            if (type === "client" && window.TalendusAPI) {
              await window.TalendusAPI.request("/companies", {
                method: "POST",
                body: { name: d.name, legal_name: d.legal_name || d.name, address: d.address, city: d.city, province: d.province || "Québec", sector: d.sector, contact_name: d.contact, email: d.email, phone: d.phone }
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Entreprise créée.", "ok");
              render();
              return;
            }
            if (type === "mission" && window.TalendusAPI) {
              await window.TalendusAPI.request("/recruiters/missions", {
                method: "POST",
                body: { title: d.title, company_id: d.clientId, job_id: d.jobId || null, seats: Number(d.seats) || 1 }
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Mission créée.", "ok");
              render();
              return;
            }
            if (type === "interview" && window.TalendusAPI) {
              await window.TalendusAPI.createInterview({
                candidate_id: d.candidate_id,
                scheduled_at: d.scheduled_at,
                location: d.location,
                type: d.type,
                candidate_can_start: !!(box.querySelector("[name=candidate_can_start]") && box.querySelector("[name=candidate_can_start]").checked)
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Entretien planifié.", "ok");
              render();
              return;
            }
            if (type === "invoice" && window.TalendusAPI) {
              await window.TalendusAPI.createInvoice({
                company_id: d.clientId,
                mission_id: d.missionId || null,
                amount: Number(d.amount) || 0,
                tax_rate_bp: Number(d.tax_rate_bp),
                issued_at: d.issued_at || null,
                due_date: d.due_date || null,
                notes: (d.notes || "").trim() || null
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Facture créée (TPS/TVQ selon le choix).", "ok");
              render();
              return;
            }
          } catch (err) {
            U.toast((err && err.message) || "Enregistrement impossible.", "err");
            if (live()) return;
          }
          if (live()) return;
          TLStore.update(function (st) {
            if (type === "candidate") {
              st.candidates.unshift({ id: TLStore.nid("c"), firstName: d.firstName, lastName: d.lastName, email: d.email, phone: d.phone, city: d.city, title: d.title, sector: d.sector, experience: 0, level: "Junior", availability: "Immédiat", status: d.status || "nouveau", languages: ["Français"], recruiterId: me.id, createdAt: new Date().toISOString().slice(0, 10), lastActivity: new Date().toISOString().slice(0, 10), skills: [], salaryMin: 20, salaryMax: 24, shift: "Jour", education: [], experiences: [], bio: "", jobId: "", clientId: "" });
              st.activities.unshift({ id: TLStore.nid("a"), text: "Nouveau candidat inscrit — " + d.firstName + " " + d.lastName, at: new Date().toISOString().slice(0, 16).replace("T", " ") });
            } else if (type === "client") {
              st.clients.unshift({ id: TLStore.nid("cl"), name: d.name, sector: d.sector, city: d.city, contact: d.contact, email: d.email, phone: d.phone, status: "Prospect", recruiterId: me.id, employees: 0, website: "", since: new Date().toISOString().slice(0, 10) });
            } else if (type === "job") {
              st.jobs.unshift({ id: TLStore.nid("j"), title: d.title, clientId: d.clientId, city: d.city, sector: "Production", type: d.contract_type || "Permanent", contract_type: d.contract_type || "Permanent", salary: d.salary, schedule: d.schedule || "Temps plein", shift: d.shift || "Quart de jour", status: publish ? "publiee" : "brouillon", publishedAt: publish ? new Date().toISOString().slice(0, 10) : "", expiresAt: "", applications: 0, experience: "—", skills: "", benefits: "", description: d.description, responsibilities: "", qualifications: "" });
            } else if (type === "mission") {
              st.missions.unshift({ id: TLStore.nid("m"), clientId: d.clientId, jobId: d.jobId, title: d.title, seats: Number(d.seats) || 1, recruiterId: me.id, start: new Date().toISOString().slice(0, 10), due: "", status: "en-cours", value: 40000, commission: 6400, progress: 5, stageMap: {} });
            } else {
              st.invoices.unshift({ id: "F-2026-" + Math.floor(100 + Math.random() * 80), clientId: d.clientId, missionId: d.missionId, amount: Number(d.amount) || 0, date: new Date().toISOString().slice(0, 10), due: "", status: "brouillon" });
            }
          });
          close();
          U.toast("Enregistré en local (mode démo).", "ok");
          render();
        }
        var save = box.querySelector("#save");
        if (save) save.onclick = function () { persistCreate(false); };
        var pub = box.querySelector("#save-pub");
        if (pub) pub.onclick = function () { persistCreate(true); };
      }
    });
  }

  function deny() { U.toast("Votre rôle n’autorise pas cette action.", "err"); }

  function bindKanban() {
    var board = $(".kanban");
    if (!board) return;
    var mid = board.getAttribute("data-mission");
    var dragId = null;
    var dragAppId = null;
    var STAGE_TO_STATUS = {
      nouveaux: "SUBMITTED",
      preselection: "UNDER_REVIEW",
      "entretien-talendus": "INTERVIEW",
      presentation: "SHORTLISTED",
      "entretien-client": "SECOND_INTERVIEW",
      offre: "OFFER_SENT",
      placement: "HIRED"
    };
    board.querySelectorAll(".kanban-card").forEach(function (card) {
      card.ondragstart = function () {
        dragId = card.getAttribute("data-cid");
        dragAppId = card.getAttribute("data-app-id") || "";
      };
    });
    board.querySelectorAll(".kanban-col").forEach(function (col) {
      col.ondragover = function (e) { e.preventDefault(); col.classList.add("drag-over"); };
      col.ondragleave = function () { col.classList.remove("drag-over"); };
      col.ondrop = async function (e) {
        e.preventDefault();
        col.classList.remove("drag-over");
        if (!dragId) return;
        var stage = col.getAttribute("data-stage");
        var status = STAGE_TO_STATUS[stage];
        var appId = dragAppId;
        TLStore.update(function (st) {
          var m = st.missions.find(function (x) { return x.id === mid; });
          if (m) {
            m.stageMap = m.stageMap || {};
            m.stageMap[dragId] = stage;
            if (m.pipeline && appId) {
              m.pipeline.forEach(function (p) {
                if (p.applicationId === appId || p.candidateId === dragId) {
                  p.stage = stage;
                  p.status = status || p.status;
                }
              });
            }
          }
          var c = st.candidates.find(function (x) { return x.id === dragId; });
          var map = { nouveaux: "nouveau", preselection: "a-contacter", "entretien-talendus": "entretien", presentation: "presente", "entretien-client": "entretien-client", offre: "offre", placement: "place" };
          if (c && map[stage]) c.status = map[stage];
        });
        if (appId && status && window.TalendusAPI) {
          try {
            await window.TalendusAPI.request("/applications/" + appId + "/status", { method: "POST", body: { status: status } });
            if (TLStore.hydrateFromApi) await TLStore.hydrateFromApi();
          } catch (err) {
            U.toast((err && err.message) || "Statut enregistré localement (API indisponible).", "err");
            render();
            return;
          }
        } else if (live() && dragId) {
          try {
            var map = { nouveaux: "nouveau", preselection: "a-contacter", "entretien-talendus": "entretien", presentation: "presente", "entretien-client": "entretien-client", offre: "offre", placement: "place" };
            await api().request("/admin/candidates/" + dragId, { method: "PATCH", body: { pipeline_status: map[stage] || "nouveau" } });
            await refreshLive();
          } catch (err) {
            U.toast((err && err.message) || "Déplacement non enregistré.", "err");
            render();
            return;
          }
        }
        U.toast("Candidat déplacé.", "ok");
        render();
      };
    });
  }

  /* ---------- Events ---------- */
  function bindView() {
    var view = $("#view");
    if (!view) return;
    view.onclick = function (e) {
      var t = e.target;
      var joinCall = t.closest("[data-join-call]");
      if (joinCall) {
        if (!window.TalendusCall) {
          U.toast("L’appel n’est pas chargé. Rechargez la page.", "err");
          return;
        }
        window.TalendusCall.start({
          interviewId: joinCall.getAttribute("data-join-call"),
          video: joinCall.getAttribute("data-video") !== "0",
          canWrap: true,
          onHangup: function () { refreshLive().then(render); },
          onWrapped: function () { refreshLive().then(render); }
        });
        return;
      }
      var closeInt = t.closest("[data-int-close]");
      if (closeInt) {
        (async function () {
          try {
            await window.TalendusAPI.request("/interviews/" + closeInt.getAttribute("data-int-close") + "/status", {
              method: "POST",
              body: { status: closeInt.getAttribute("data-status") }
            });
            await refreshLive();
            U.toast("Statut envoyé au candidat.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Mise à jour impossible.", "err");
          }
        })();
        return;
      }
      var openCall = t.closest("[data-open-call]");
      if (openCall) {
        (async function () {
          try {
            await window.TalendusAPI.request("/calls/" + openCall.getAttribute("data-open-call") + "/open", { method: "POST" });
            await refreshLive();
            U.toast("Le candidat est prévenu. Lancez l’appel pour qu’il puisse rejoindre.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Ouverture impossible.", "err");
          }
        })();
        return;
      }
      var perm = t.closest("[data-call-perm]");
      if (perm) {
        (async function () {
          try {
            await window.TalendusAPI.request("/interviews/" + perm.getAttribute("data-call-perm"), {
              method: "PATCH",
              body: { candidate_can_start: perm.getAttribute("data-allow") === "1" }
            });
            await refreshLive();
            U.toast(perm.getAttribute("data-allow") === "1" ? "Le candidat peut lancer l’appel." : "Le candidat ne peut plus que rejoindre.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Mise à jour impossible.", "err");
          }
        })();
        return;
      }
      var goEl = t.closest("[data-go]");
      if (goEl) { go(goEl.getAttribute("data-go")); return; }
      var sort = t.closest("[data-sort]");
      if (sort && sort.getAttribute("data-sort")) {
        var k = sort.getAttribute("data-sort");
        if (sortKey === k) sortDir = sortDir === "asc" ? "desc" : "asc";
        else { sortKey = k; sortDir = "asc"; }
        render(); return;
      }
      var pg = t.closest("[data-page]");
      if (pg) { page = Number(pg.getAttribute("data-page")); render(); return; }
      var cr = t.closest("[data-create]");
      if (cr) { openCreate(cr.getAttribute("data-create")); return; }
      var dtab = t.closest("[data-dtab]");
      if (dtab) { detailTab = dtab.getAttribute("data-dtab"); render(); return; }
      var ctab = t.closest("[data-ctab]");
      if (ctab) { contentTab = ctab.getAttribute("data-ctab"); render(); return; }
      var ftab = t.closest("[data-ftab]");
      if (ftab) { financeTab = ftab.getAttribute("data-ftab"); render(); return; }
      var per = t.closest("[data-period]");
      if (per) { period = per.getAttribute("data-period"); render(); return; }
      if (t.closest("[data-export-cand]")) {
        U.csv("candidats-talendus.csv", [["Nom","Poste","Ville","Statut"]].concat(filteredCandidates().map(function (c) { return [c.firstName + " " + c.lastName, c.title, c.city, c.status]; })));
        U.toast("Export CSV prêt.", "ok");
      }
      if (t.closest("[data-export-cli]")) {
        U.csv("clients-talendus.csv", [["Nom","Secteur","Ville"]].concat(S().clients.map(function (c) { return [c.name, c.sector, c.city]; })));
        U.toast("Export CSV prêt.", "ok");
      }
      if (t.closest("[data-export-fin]") || t.closest("[data-export-an]") || t.closest("[data-export-dash]")) {
        U.csv("talendus-export.csv", [["Indicateur","Valeur"],["Candidats", S().candidates.length],["Clients", S().clients.length],["Offres", S().jobs.length]]);
        U.toast("Export CSV prêt.", "ok");
      }
      var bulk = t.closest("[data-bulk]");
      if (bulk) {
        var stt = bulk.getAttribute("data-bulk");
        var ids = Array.from(selected);
        (async function () {
          if (live()) {
            try {
              for (var i = 0; i < ids.length; i++) {
                var cand = TLStore.candidate(ids[i]);
                await setCandidateStatus(cand, stt);
              }
            } catch (err) {
              U.toast((err && err.message) || "Statuts API impossibles.", "err");
              return;
            }
          } else {
            TLStore.update(function (st) {
              st.candidates.forEach(function (c) { if (selected.has(c.id)) c.status = stt; });
            });
          }
          selected.clear();
          U.toast("Statuts mis à jour.", "ok");
          render();
        })();
        return;
      }
      var note = t.closest("[data-note]");
      if (note) {
        U.modal({
          title: "Note interne",
          body: '<form id="nf">' + U.field("Note privée", "text", "", "textarea", "full") + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Ajouter</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var text = box.querySelector("[name=text]").value;
              var entityId = note.getAttribute("data-note");
              try {
                if (live()) {
                  await window.TalendusAPI.request("/recruiters/notes", { method: "POST", body: { entity_type: "candidate", entity_id: entityId, text: text } });
                  await refreshLive();
                  close(); U.toast("Note interne enregistrée (invisible pour le candidat).", "ok"); render();
                  return;
                }
              } catch (err) {
                U.toast((err && err.message) || "Note non enregistrée.", "err");
                if (live()) return;
              }
              TLStore.update(function (st) {
                st.notes.unshift({ id: TLStore.nid("n"), entity: "candidate", entityId: entityId, authorId: TLStore.me().id, text: text, at: new Date().toISOString().slice(0, 16).replace("T", " ") });
              });
              close(); U.toast("Note enregistrée.", "ok"); render();
            };
          }
        });
        return;
      }
      var jobAct = t.closest("[data-job-act]");
      if (jobAct) {
        var parts = jobAct.getAttribute("data-job-act").split(":");
        var act = parts[0], jid = parts[1];
        var hireId = jobAct.getAttribute("data-hire-id") || "";
        if (act === "dup") {
          (async function () {
            if (live()) {
              try {
                await window.TalendusAPI.request("/jobs/" + jid + "/duplicate", { method: "POST" });
                await refreshLive();
                U.toast("Offre dupliquée (brouillon).", "ok");
                render();
              } catch (err) {
                U.toast((err && err.message) || "Duplication impossible.", "err");
              }
              return;
            }
            TLStore.update(function (st) {
              var j = st.jobs.find(function (x) { return x.id === jid; });
              var copy = JSON.parse(JSON.stringify(j));
              copy.id = TLStore.nid("j"); copy.title = j.title + " (copie)"; copy.status = "brouillon"; copy.applications = 0;
              st.jobs.unshift(copy);
            });
            U.toast("Offre dupliquée.", "ok"); render();
          })();
          return;
        } else if (act === "edit") {
          var j = TLStore.job(jid);
          U.modal({
            title: "Modifier l’offre",
            body: '<form id="jf" class="form-grid">' + U.field("Titre", "title", j.title) + U.field("Salaire", "salary", j.salary) + jobVocabFields(j) + U.field("Description", "description", j.description, "textarea", "full") + "</form>",
            footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
            onMount: function (box, close) {
              box.querySelector("#save").onclick = async function () {
                var d = U.formData(box.querySelector("#jf"));
                try {
                  if (live()) {
                    await window.TalendusAPI.request("/jobs/" + jid, { method: "PATCH", body: { title: d.title, salary_display: d.salary, description: d.description, contract_type: d.contract_type, schedule: d.schedule, shift: d.shift } });
                    await refreshLive();
                    close(); U.toast("Offre mise à jour — le site public suit cette fiche.", "ok"); render();
                    return;
                  }
                } catch (err) {
                  U.toast((err && err.message) || "Mise à jour impossible.", "err");
                  if (live()) return;
                }
                TLStore.update(function (st) {
                  var x = st.jobs.find(function (z) { return z.id === jid; });
                  Object.assign(x, d);
                });
                close(); U.toast("Offre mise à jour.", "ok"); render();
              };
            }
          });
          return;
        } else {
          U.confirm("Changer le statut de l’offre ? Cela se reflète sur le site public.").then(async function (ok) {
            if (!ok) return;
            var endpoint = JOB_ACT_API[act];
            if (live() && endpoint) {
              try {
                await window.TalendusAPI.request("/jobs/" + jid + "/" + endpoint, { method: "POST" });
                if (hireId && act === "publiee") {
                  await window.TalendusAPI.request("/hiring-requests/" + hireId + "/status", { method: "POST", body: { status: "JOB_PUBLISHED" } });
                }
                await refreshLive();
                U.toast(act === "publiee" ? "Offre publiée sur le site." : "Statut de l’offre mis à jour.", "ok");
                render();
              } catch (err) {
                U.toast((err && err.message) || "Action impossible.", "err");
              }
              return;
            }
            TLStore.update(function (st) {
              var x = st.jobs.find(function (z) { return z.id === jid; });
              if (x) {
                x.status = act;
                if (act === "publiee") x.publishedAt = new Date().toISOString().slice(0, 10);
              }
            });
            U.toast("Statut mis à jour.", "ok"); render();
          });
          return;
        }
      }
      var cms = t.closest("[data-cms]");
      if (cms) {
        var p = cms.getAttribute("data-cms").split(":");
        var action = p[0], tab = p[1], cid = p[2];
        if (tab === "blog" && window.TalendusAPI) {
          if (action === "prev") {
            window.open("/blog/" + encodeURIComponent(cid), "_blank");
            return;
          }
          if (action === "toggle" || action === "arch") {
            var next = action === "arch" ? "ARCHIVED" : (cms.getAttribute("data-status") === "PUBLISHED" ? "DRAFT" : "PUBLISHED");
            window.TalendusAPI.request("/admin/blog/" + cid, { method: "PATCH", body: { status: next } }).then(function () {
              U.toast("Statut article mis à jour.", "ok");
              hydrateBlogCms();
            }).catch(function (err) { U.toast((err && err.message) || "Erreur", "err"); });
            return;
          }
          var load = cid ? window.TalendusAPI.request("/admin/blog/" + cid).then(function (j) { return j.data; }) : Promise.resolve({});
          load.then(function (item) {
            U.modal({
              title: action === "new" ? "Nouvel article" : "Éditer l’article",
              body: '<form id="ef" class="form-grid">' +
                U.field("Titre", "title", item.title || "") +
                U.field("Slug SEO", "slug", item.slug || "") +
                U.field("Title SEO", "seo_title", item.seo_title || "") +
                U.field("Meta description", "seo_description", item.seo_description || "", "textarea", "full") +
                U.field("Extrait", "excerpt", item.excerpt || "", "textarea", "full") +
                U.field("Corps", "body", item.body || "", "textarea", "full") +
                U.field("Catégorie", "category", item.category || "") +
                U.field("Tags", "tags", Array.isArray(item.tags) ? item.tags.join(", ") : (item.tags || "")) +
                U.field("Auteur", "author_name", item.author_name || "") +
                U.field("Image principale", "cover_image", item.cover_image || "") +
                U.field("Statut", "status", { options: [{ v: "DRAFT", l: "Brouillon" }, { v: "PUBLISHED", l: "Publié" }, { v: "SCHEDULED", l: "Programmé" }, { v: "ARCHIVED", l: "Archivé" }], selected: item.status || "DRAFT" }, "select") +
                U.field("Publication programmée", "scheduled_at", (item.scheduled_at || "").slice(0, 16), "datetime-local") +
                "</form>",
              footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
              onMount: function (box, close) {
                box.querySelector("#save").onclick = async function () {
                  var d = U.formData(box.querySelector("#ef"));
                  if (d.scheduled_at) d.scheduled_at = new Date(d.scheduled_at).toISOString();
                  else d.scheduled_at = null;
                  try {
                    if (action === "new") await window.TalendusAPI.request("/admin/blog", { method: "POST", body: d });
                    else await window.TalendusAPI.request("/admin/blog/" + cid, { method: "PATCH", body: d });
                    close(); U.toast("Article enregistré.", "ok"); hydrateBlogCms();
                  } catch (err) { U.toast((err && err.message) || "Erreur", "err"); }
                };
              }
            });
          });
          return;
        }
        var col = { pages: "pages", blog: "posts", temoignages: "testimonials", faq: "faqs", seo: "posts" }[tab];
        var cmsKey = tab === "temoignages" ? "testimonials" : tab === "faq" ? "faq" : "";
        if (tab === "pages" || tab === "seo") {
          U.toast("Ces pages sont le site déployé. Éditez le blog, les témoignages ou la FAQ.", "ok");
          return;
        }
        if (action === "new" || action === "edit") {
          var item = cid ? (S()[col] || []).find(function (x) { return x.id === cid; }) : { title: "", q: "", seo: "" };
          U.modal({
            title: action === "new" ? "Nouveau contenu" : "Éditeur",
            body: '<form id="ef">' + U.field("Titre / question / auteur", "title", item.title || item.q || item.author || "") + U.field("Contenu", "body", item.a || item.quote || item.seo || "", "textarea", "full") + "</form>",
            footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
            onMount: function (box, close) {
              box.querySelector("#save").onclick = async function () {
                var d = U.formData(box.querySelector("#ef"));
                var list = (S()[col] || []).slice();
                if (action === "new") {
                  list.unshift({ id: TLStore.nid("x"), title: d.title, q: d.title, author: d.title, quote: d.body, a: d.body, seo: d.body, slug: "", status: "publie", updatedAt: new Date().toISOString().slice(0, 10), role: "", authorId: TLStore.me().id });
                } else {
                  list = list.map(function (it) {
                    if (it.id !== cid) return it;
                    return Object.assign({}, it, { title: d.title, q: d.title, author: d.title, a: d.body, quote: d.body, updatedAt: new Date().toISOString().slice(0, 10) });
                  });
                }
                try {
                  if (live() && cmsKey) {
                    await api().request("/admin/site-content/" + cmsKey, { method: "PUT", body: { items: list } });
                    await refreshLive();
                  } else {
                    TLStore.update(function (st) { st[col] = list; });
                  }
                  close(); U.toast("Contenu enregistré.", "ok"); render();
                } catch (err) { U.toast((err && err.message) || "Enregistrement impossible.", "err"); }
              };
            }
          });
        } else if (action === "toggle" || action === "arch") {
          var nextList = (S()[col] || []).map(function (it) {
            if (it.id !== cid) return it;
            var copy = Object.assign({}, it);
            if (action === "arch") copy.status = "archive";
            else copy.status = (it.status === "publie" || it.status === "publiee") ? "brouillon" : "publie";
            return copy;
          });
          (async function () {
            try {
              if (live() && cmsKey) {
                await api().request("/admin/site-content/" + cmsKey, { method: "PUT", body: { items: nextList } });
                await refreshLive();
              } else {
                TLStore.update(function (st) { st[col] = nextList; });
              }
              U.toast("Statut contenu mis à jour.", "ok"); render();
            } catch (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); }
          })();
        }
        return;
      }
      var dl = t.closest("[data-dl-doc]");
      if (dl && api()) {
        api().download(dl.getAttribute("data-dl-doc").replace(/^\/api/, ""), dl.getAttribute("data-dl-name") || "document").catch(function (err) {
          U.toast((err && err.message) || "Téléchargement impossible.", "err");
        });
        return;
      }
      var invEdit = t.closest("[data-inv-edit]");
      if (invEdit) {
        var editId = invEdit.getAttribute("data-inv-edit");
        var invRow = S().invoices.find(function (x) { return invoiceApiId(x) === editId; });
        if (!invRow) return;
        U.modal({
          title: "Modifier la facture " + (invRow.id || ""),
          body: '<form id="inv-edit" class="form-grid">' +
            U.field("Date de facture", "issued_at", invRow.date || "", "date") +
            U.field("Échéance", "due_date", invRow.due || "", "date") +
            U.field("Intitulé / notes (sur la facture)", "notes", invRow.notes || "", "textarea", "full") +
            "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#inv-edit"));
              try {
                await api().request("/invoices/" + editId, { method: "PATCH", body: { issued_at: d.issued_at || null, due_date: d.due_date || null, notes: (d.notes || "").trim() || null } });
                await refreshLive();
                close();
                U.toast("Facture mise à jour.", "ok");
                render();
              } catch (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); }
            };
          }
        });
        return;
      }
      var invSend = t.closest("[data-inv-send]");
      if (invSend) {
        (async function () {
          try {
            await api().request("/invoices/" + invSend.getAttribute("data-inv-send") + "/send", { method: "POST" });
            await refreshLive();
            U.toast("Facture envoyée.", "ok");
            render();
          } catch (err) { U.toast((err && err.message) || "Envoi impossible.", "err"); }
        })();
        return;
      }
      var invPay = t.closest("[data-inv-pay]");
      if (invPay) {
        var payId = invPay.getAttribute("data-inv-pay");
        var amt = invPay.getAttribute("data-inv-amount") || "";
        U.modal({
          title: "Encaisser un paiement",
          body: '<form id="pay-form" class="form-grid">' + U.field("Montant", "amount", amt, "number") + U.field("Méthode", "method", { options: [{ v: "TRANSFER", l: "Virement" }, { v: "CHEQUE", l: "Chèque" }, { v: "CARD", l: "Carte" }, { v: "OTHER", l: "Autre" }], selected: "TRANSFER" }, "select") + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#pay-form"));
              try {
                await api().request("/invoices/" + payId + "/payments", { method: "POST", body: { amount: Number(d.amount) || 0, method: d.method } });
                await refreshLive();
                close(); U.toast("Paiement enregistré.", "ok"); render();
              } catch (err) { U.toast((err && err.message) || "Paiement impossible.", "err"); }
            };
          }
        });
        return;
      }
      var editCli = t.closest("[data-edit-client]");
      if (editCli) {
        var cl = TLStore.client(editCli.getAttribute("data-edit-client"));
        if (!cl) return;
        U.modal({
          title: "Modifier l’entreprise",
          body: '<form id="cl-form" class="form-grid">' + U.field("Entreprise", "name", cl.name) + U.field("Raison sociale", "legal_name", cl.legalName || cl.legal_name || "") + U.field("Adresse", "address", cl.address || "", "text", "full") + U.field("Ville", "city", cl.city) + U.field("Province", "province", cl.province || "Québec") + U.field("Secteur", "sector", cl.sector) + U.field("Contact", "contact", cl.contact) + U.field("Courriel", "email", cl.email) + U.field("Téléphone", "phone", cl.phone) + U.field("Site", "website", cl.website || "") + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#cl-form"));
              try {
                if (live()) {
                  await api().request("/companies/" + cl.id, { method: "PATCH", body: { name: d.name, legal_name: d.legal_name || d.name, address: d.address, city: d.city, province: d.province || "Québec", sector: d.sector, contact_name: d.contact, email: d.email || null, phone: d.phone, website: d.website } });
                  await refreshLive();
                } else {
                  TLStore.update(function (st) { Object.assign(st.clients.find(function (x) { return x.id === cl.id; }), d); });
                }
                close(); U.toast("Entreprise mise à jour.", "ok"); render();
              } catch (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); }
            };
          }
        });
        return;
      }
      var hireConvert = t.closest("[data-hire-convert]");
      if (hireConvert) {
        var hid = hireConvert.getAttribute("data-hire-convert");
        (async function () {
          try {
            await window.TalendusAPI.request("/hiring-requests/" + hid + "/convert-to-job", { method: "POST" });
            await refreshLive();
            U.toast("Offre créée en brouillon. Publiez-la pour qu’elle apparaisse sur le site.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Conversion impossible.", "err");
          }
        })();
        return;
      }
      var addInt = t.closest("[data-add-int]");
      if (addInt) {
        var cid = addInt.getAttribute("data-add-int");
        U.modal({
          title: "Planifier un entretien",
          body: '<form id="int-form" class="form-grid">' +
            U.field("Date et heure", "scheduled_at", new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16), "datetime-local") +
            U.field("Lieu", "location", "Visio Talendus") +
            U.field("Type", "type", { options: [{ v: "TALENDUS", l: "Visio Talendus" }, { v: "VIDEO", l: "Visio" }, { v: "PHONE", l: "Téléphone" }, { v: "CLIENT", l: "Chez le client" }, { v: "ONSITE", l: "Sur place" }], selected: "TALENDUS" }, "select") +
            '<label class="check"><input type="checkbox" name="candidate_can_start"> Autoriser le candidat à lancer l’appel</label>' +
            "<p class=\"sub\">Sans cette case, le candidat rejoint seulement après que vous ayez ouvert la salle.</p>" +
            "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Planifier</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#int-form"));
              try {
                if (live()) {
                  await window.TalendusAPI.createInterview({
                    candidate_id: cid,
                    scheduled_at: d.scheduled_at,
                    location: d.location,
                    type: d.type,
                    candidate_can_start: !!(box.querySelector("[name=candidate_can_start]") && box.querySelector("[name=candidate_can_start]").checked)
                  });
                  await TLStore.hydrateFromApi();
                  close();
                  U.toast("Entretien enregistré.", "ok");
                  render();
                  return;
                }
              } catch (err) {
                U.toast((err && err.message) || "Planification impossible.", "err");
                if (live()) return;
              }
              TLStore.update(function (st) {
                st.interviews.push({ id: TLStore.nid("i"), candidateId: cid, clientId: "", type: "Talendus", at: d.scheduled_at || "2026-08-20 10:00", location: d.location || "Visio", recruiterId: TLStore.me().id });
              });
              close();
              U.toast("Entretien planifié.", "ok");
              render();
            };
          }
        });
        return;
      }
      var signAgency = t.closest("[data-sign-talendus]");
      if (signAgency) {
        var agencyId = signAgency.getAttribute("data-sign-talendus");
        U.modal({
          title: "Signer pour Talendus",
          body: '<form id="sg-form">' + U.field("Nom du signataire Talendus", "signer_name", TLStore.me().firstName + " " + TLStore.me().lastName) + "<p>Talendus signe en premier. Le client recevra ensuite le mandat pour le lire et le contresigner. Trace : nom, date, IP et empreinte SHA-256. Ce n’est pas DocuSign.</p></form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Signer pour Talendus</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#sg-form"));
              try {
                await window.TalendusAPI.signTalendus(agencyId, { signer_name: d.signer_name, accepted: true });
                await TLStore.hydrateFromApi();
                close();
                U.toast("Mandat signé pour Talendus. Vous pouvez l’envoyer au client.", "ok");
                render();
              } catch (err) {
                U.toast((err && err.message) || "Signature Talendus impossible.", "err");
              }
            };
          }
        });
        return;
      }
      var readCt = t.closest("[data-read-contract]");
      if (readCt) {
        var readId = readCt.getAttribute("data-read-contract");
        var found = S().contracts.find(function (x) { return x.id === readId; }) || {};
        U.modal({
          wide: true,
          title: found.type || "Mandat de recrutement",
          body: '<div class="mandate-meta">' + U.badge(found.talendusSigned ? "Signé Talendus" : "À signer") + " " + U.badge(clientStatusLabel(found)) +
            "</div><article class=\"mandate-read\">" + U.esc(found.terms || "Le texte du mandat n’est pas disponible.") + "</article>",
          footer: '<button class="btn btn-ghost" data-close>Fermer</button>' +
            (found.pdfPath ? '<button class="btn btn-orange" id="open-pdf">Lire le PDF</button>' : ""),
          onMount: function (box) {
            var pdfBtn = box.querySelector("#open-pdf");
            if (pdfBtn) {
              pdfBtn.onclick = async function () {
                try {
                  await window.TalendusAPI.openPdf("/contracts/" + readId + "/pdf");
                } catch (err) {
                  U.toast((err && err.message) || "Lecture PDF impossible.", "err");
                }
              };
            }
          }
        });
        return;
      }
      var pdfCt = t.closest("[data-open-pdf]");
      if (pdfCt) {
        (async function () {
          try {
            await window.TalendusAPI.openPdf("/contracts/" + pdfCt.getAttribute("data-open-pdf") + "/pdf");
          } catch (err) {
            U.toast((err && err.message) || "Lecture PDF impossible.", "err");
          }
        })();
        return;
      }
      var signCt = t.closest("[data-sign-contract]");
      if (signCt) {
        var contractId = signCt.getAttribute("data-sign-contract");
        U.modal({
          title: "Enregistrer la signature du client",
          body: '<form id="sg-form">' + U.field("Nom du signataire client", "signer_name", "") + "<p>À utiliser si le client a signé en votre présence. Sinon, envoyez le mandat : le client lit et signe dans son espace.</p></form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer la signature</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#sg-form"));
              try {
                await window.TalendusAPI.signContract(contractId, { signer_name: d.signer_name, accepted: true });
                await TLStore.hydrateFromApi();
                close();
                U.toast("Signature du client enregistrée.", "ok");
                render();
              } catch (err) {
                U.toast((err && err.message) || "Signature impossible.", "err");
              }
            };
          }
        });
        return;
      }
      var sendCt = t.closest("[data-send-contract]");
      if (sendCt) {
        var sendId = sendCt.getAttribute("data-send-contract");
        (async function () {
          try {
            if (live()) {
              await window.TalendusAPI.sendContract(sendId);
              await refreshLive();
            }
            U.toast("Mandat transmis dans l’espace employeur.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Envoi impossible.", "err");
          }
        })();
        return;
      }
      var addCt = t.closest("[data-add-contract]");
      if (addCt) {
        openMandateModal(addCt.getAttribute("data-add-contract"), { role: addCt.getAttribute("data-role") || "" });
        return;
      }
      var editCt = t.closest("[data-edit-contract]");
      if (editCt) {
        var editId = editCt.getAttribute("data-edit-contract");
        var foundCt = S().contracts.find(function (x) { return x.id === editId; });
        if (foundCt) openMandateModal(foundCt.clientId, foundCt);
        return;
      }
      var editC = t.closest("[data-edit-cand]");
      if (editC) {
        var c = TLStore.candidate(editC.getAttribute("data-edit-cand"));
        U.modal({
          title: "Modifier le candidat",
          body: '<form id="ec" class="form-grid">' + U.field("Ville", "city", c.city) + U.field("Poste", "title", c.title) + U.field("Disponibilité", "availability", c.availability) + U.field("Secteur", "sector", c.sector || "") + U.field("Téléphone", "phone", c.phone || "") + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#ec"));
              try {
                if (live()) {
                  await api().request("/admin/candidates/" + c.id, { method: "PATCH", body: { city: d.city, title: d.title, availability: d.availability, sector: d.sector, phone: d.phone } });
                  await refreshLive();
                } else {
                  TLStore.update(function (st) { Object.assign(st.candidates.find(function (x) { return x.id === c.id; }), d); });
                }
                close(); U.toast("Fiche mise à jour.", "ok"); render();
              } catch (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); }
            };
          }
        });
      }
    };
    view.onchange = function (e) {
      var t = e.target;
      if (t.hasAttribute("data-f")) {
        filters[t.getAttribute("data-f")] = t.value;
        page = 1;
        render();
      }
      if (t.hasAttribute("data-sel")) {
        if (t.checked) selected.add(t.getAttribute("data-sel"));
        else selected.delete(t.getAttribute("data-sel"));
        render();
      }
      if (t.hasAttribute("data-status-cand")) {
        var id = t.getAttribute("data-status-cand");
        var next = t.value;
        (async function () {
          var cand = TLStore.candidate(id);
          try {
            await setCandidateStatus(cand, next);
            U.toast(live() ? "Statut enregistré — le candidat le voit dans son espace." : "Statut candidat mis à jour.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Statut non enregistré.", "err");
          }
        })();
      }
      if (t.hasAttribute("data-hire-status")) {
        var hid = t.getAttribute("data-hire-status");
        var status = t.value;
        (async function () {
          try {
            await window.TalendusAPI.request("/hiring-requests/" + hid + "/status", { method: "POST", body: { status: status } });
            await refreshLive();
            U.toast("Statut mis à jour — l’entreprise le voit dans son espace.", "ok");
            render();
          } catch (err) {
            U.toast((err && err.message) || "Statut non enregistré.", "err");
          }
        })();
      }
      if (t.id === "an-rec") { analyticsRecruiter = t.value; render(); }
      if (t.id === "an-sec") { analyticsSector = t.value; render(); }
    };
    var nf = document.getElementById("note-form");
    if (nf) nf.onsubmit = async function (e) {
      e.preventDefault();
      var id = route().id;
      var text = U.formData(nf).text;
      try {
        if (live()) {
          await window.TalendusAPI.request("/recruiters/notes", { method: "POST", body: { entity_type: "candidate", entity_id: id, text: text } });
          await refreshLive();
          U.toast("Note interne enregistrée.", "ok");
          render();
          return;
        }
      } catch (err) {
        U.toast((err && err.message) || "Note non enregistrée.", "err");
        if (live()) return;
      }
      TLStore.update(function (st) {
        st.notes.unshift({ id: TLStore.nid("n"), entity: "candidate", entityId: id, authorId: TLStore.me().id, text: text, at: new Date().toISOString().slice(0, 16).replace("T", " ") });
      });
      U.toast("Note interne enregistrée.", "ok");
      render();
    };
    var cnf = document.getElementById("client-note-form");
    if (cnf) cnf.onsubmit = async function (e) {
      e.preventDefault();
      var id = route().id;
      var text = U.formData(cnf).text;
      try {
        if (live()) {
          await api().request("/recruiters/notes", { method: "POST", body: { entity_type: "client", entity_id: id, text: text } });
          await refreshLive();
        } else {
          TLStore.update(function (st) {
            st.notes.unshift({ id: TLStore.nid("n"), entity: "client", entityId: id, authorId: TLStore.me().id, text: text, at: new Date().toISOString().slice(0, 16).replace("T", " ") });
          });
        }
        U.toast("Note interne enregistrée.", "ok");
        render();
      } catch (err) { U.toast((err && err.message) || "Note non enregistrée.", "err"); }
    };
    var up = document.getElementById("cand-upload");
    if (up) up.onsubmit = async function (e) {
      e.preventDefault();
      var file = up.querySelector("[name=file]") && up.querySelector("[name=file]").files[0];
      if (!file) { U.toast("Choisissez un fichier.", "err"); return; }
      if (!live()) { U.toast("Connectez-vous à l’API pour déposer un document.", "err"); return; }
      var fd = new FormData();
      api().appendFile(fd, file, "cv.pdf");
      try {
        await api().request("/admin/candidates/" + route().id + "/resume", { method: "POST", body: fd });
        await refreshLive();
        detailTab = "cv";
        U.toast("Document enregistré dans le dossier.", "ok");
        render();
      } catch (err) { U.toast((err && err.message) || "Téléversement impossible.", "err"); }
    };
    var pfme = document.getElementById("adm-profile");
    if (pfme) pfme.onsubmit = async function (e) {
      e.preventDefault();
      var d = U.formData(pfme);
      try {
        if (live()) {
          await api().request("/users/me", { method: "PATCH", body: { first_name: d.first_name, last_name: d.last_name, phone: d.phone, title: d.title } });
          TLStore.update(function (st) {
            var me = st.users.find(function (u) { return u.id === TLStore.me().id; });
            if (me) { me.firstName = d.first_name; me.lastName = d.last_name; me.title = d.title; }
          });
        }
        U.toast("Profil mis à jour.", "ok");
        render();
      } catch (err) { U.toast((err && err.message) || "Mise à jour impossible.", "err"); }
    };
    var ma = document.getElementById("mark-all");
    if (ma) ma.onclick = async function () {
      if (live()) {
        try {
          await window.TalendusAPI.request("/notifications/read-all", { method: "POST" });
          await refreshLive();
        } catch (err) {
          U.toast((err && err.message) || "Impossible de marquer lu.", "err");
          return;
        }
      } else {
        TLStore.update(function (st) { st.notifications.forEach(function (n) { n.read = true; }); });
      }
      render();
    };
    var rst = document.getElementById("reset-demo");
    if (rst) rst.onclick = function () {
      U.confirm("Réinitialiser toutes les données de démonstration ?").then(async function (ok) {
        if (!ok) return;
        TLStore.reset();
        if (live()) await refreshLive();
        U.toast(live() ? "Données rechargées depuis l’API." : "Données réinitialisées.", "ok");
        render();
      });
    };
    view.querySelectorAll("[data-stab]").forEach(function (btn) {
      btn.onclick = function () {
        var name = btn.getAttribute("data-stab");
        view.querySelectorAll("[data-stab]").forEach(function (b) { b.classList.toggle("is-active", b === btn); });
        view.querySelectorAll("[data-spanel]").forEach(function (p) { p.hidden = p.getAttribute("data-spanel") !== name; });
      };
    });
    function api() { return window.TalendusAPI; }
    var prefForm = document.getElementById("adm-prefs");
    if (prefForm && api()) {
      api().request("/users/me/preferences").then(function (json) {
        var d = (json && json.data) || {};
        ["notify_email", "notify_in_app", "notify_application", "notify_message", "notify_interview"].forEach(function (k) {
          var el = prefForm.querySelector("[name=" + k + "]");
          if (el) el.checked = d[k] !== false;
        });
      }).catch(function () {});
      prefForm.onsubmit = function (e) {
        e.preventDefault();
        var body = {};
        ["notify_email", "notify_in_app", "notify_application", "notify_message", "notify_interview"].forEach(function (k) {
          var el = prefForm.querySelector("[name=" + k + "]");
          if (el) body[k] = !!el.checked;
        });
        api().request("/users/me/preferences", { method: "PATCH", body: body }).then(function () {
          U.toast("Préférences enregistrées.", "ok");
        }).catch(function (err) { U.toast((err && err.message) || "Impossible d’enregistrer.", "err"); });
      };
    }
    var passForm = document.getElementById("adm-pass");
    if (passForm && api()) {
      passForm.onsubmit = function (e) {
        e.preventDefault();
        var d = U.formData(passForm);
        api().request("/auth/change-password", { method: "POST", body: d }).then(function () {
          U.toast("Mot de passe mis à jour.", "ok");
          passForm.reset();
        }).catch(function (err) { U.toast((err && err.message) || "Impossible de changer le mot de passe.", "err"); });
      };
    }
    var sess = document.getElementById("adm-sessions");
    if (sess && api()) {
      api().request("/auth/sessions").then(function (json) {
        var rows = (json && json.data) || [];
        sess.innerHTML = '<div class="card-head"><h3>Sessions actives</h3></div>' + (rows.map(function (s) {
          return '<div class="n-item"><b>' + U.esc(s.created_at || "") + "</b> · " + (s.active ? "Active" : "Révoquée") + "</div>";
        }).join("") || "<p class='sub'>Aucune session listée.</p>") +
          '<p style="margin-top:12px"><button type="button" class="btn btn-ghost" id="adm-revoke-all">Déconnecter partout</button></p>';
        var all = document.getElementById("adm-revoke-all");
        if (all) all.onclick = function () {
          api().request("/auth/sessions/revoke-all", { method: "POST" }).then(function () {
            U.toast("Sessions révoquées.", "ok");
            render();
          });
        };
      }).catch(function () { sess.innerHTML = "<p class='sub'>Sessions indisponibles hors connexion API.</p>"; });
    }
    var platform = document.getElementById("adm-platform");
    if (platform && api()) {
      api().request("/admin/settings").then(function (json) {
        var rows = ((json && json.data) || []).filter(function (s) {
          return String(s.key || "").indexOf("smtp.") !== 0;
        });
        platform.innerHTML = '<form id="adm-platform-form">' + rows.map(function (s) {
          return '<label>' + U.esc(s.label || s.key) + '</label><input name="' + U.esc(s.key) + '" value="' + U.esc(s.value || "") + '">';
        }).join("") + (rows.length ? '<button class="btn btn-orange" type="submit">Enregistrer la plateforme</button>' : "<p class='sub'>Aucun réglage plateforme.</p>") + "</form>";
        var pf = document.getElementById("adm-platform-form");
        if (pf) pf.onsubmit = function (e) {
          e.preventDefault();
          var fd = U.formData(pf);
          var tasks = Object.keys(fd).map(function (key) {
            return api().request("/admin/settings", { method: "PATCH", body: { key: key, value: fd[key] } });
          });
          Promise.all(tasks).then(function () { U.toast("Plateforme enregistrée.", "ok"); })
            .catch(function (err) { U.toast((err && err.message) || "Impossible d’enregistrer.", "err"); });
        };
      }).catch(function () { platform.innerHTML = "<p class='sub'>Réservé aux administrateurs connectés à l’API.</p>"; });
    }
    var smtpBox = document.getElementById("adm-smtp");
    if (smtpBox && api()) {
      api().request("/admin/settings").then(function (json) {
        var all = (json && json.data) || [];
        var byKey = {};
        all.forEach(function (s) { byKey[s.key] = s; });
        var val = function (key, fallback) {
          return (byKey[key] && byKey[key].value) || fallback || "";
        };
        smtpBox.innerHTML =
          '<form id="adm-smtp-form">' +
          '<label>Activer l’envoi</label><select name="smtp.enabled">' +
          '<option value="">Utiliser le réglage serveur (EMAIL_ENABLED)</option>' +
          '<option value="oui"' + (val("smtp.enabled") === "oui" ? " selected" : "") + ">Oui — envoyer vraiment</option>" +
          '<option value="non"' + (val("smtp.enabled") === "non" ? " selected" : "") + ">Non — journaliser seulement</option>" +
          "</select>" +
          '<label>Serveur SMTP</label><input name="smtp.host" placeholder="smtp.gmail.com" value="' + U.esc(val("smtp.host")) + '">' +
          '<label>Port</label><input name="smtp.port" placeholder="587" value="' + U.esc(val("smtp.port", "587")) + '">' +
          '<label>Identifiant</label><input name="smtp.username" placeholder="info@talendus.ca" value="' + U.esc(val("smtp.username")) + '" autocomplete="off">' +
          '<label>Mot de passe SMTP</label><input name="smtp.password" type="password" value="' + U.esc(val("smtp.password")) + '" autocomplete="new-password" placeholder="Laisser vide pour conserver">' +
          '<label>Expéditeur (From)</label><input name="smtp.from" value="' + U.esc(val("smtp.from", "Talendus <info@talendus.ca>")) + '">' +
          '<label>TLS (STARTTLS)</label><select name="smtp.use_tls">' +
          '<option value="oui"' + (val("smtp.use_tls", "oui") !== "non" ? " selected" : "") + ">oui</option>" +
          '<option value="non"' + (val("smtp.use_tls") === "non" ? " selected" : "") + ">non</option>" +
          "</select>" +
          '<p style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">' +
          '<button class="btn btn-orange" type="submit">Enregistrer le courriel</button>' +
          '<button class="btn btn-ghost" type="button" id="adm-smtp-test">Envoyer un test</button>' +
          "</p></form>";
        var sf = document.getElementById("adm-smtp-form");
        if (sf) sf.onsubmit = function (e) {
          e.preventDefault();
          var fd = U.formData(sf);
          var tasks = Object.keys(fd).map(function (key) {
            return api().request("/admin/settings", { method: "PATCH", body: { key: key, value: fd[key] } });
          });
          Promise.all(tasks).then(function () { U.toast("Réglages courriel enregistrés.", "ok"); })
            .catch(function (err) { U.toast((err && err.message) || "Impossible d’enregistrer.", "err"); });
        };
        var testBtn = document.getElementById("adm-smtp-test");
        if (testBtn) testBtn.onclick = function () {
          api().request("/admin/settings/test-email", { method: "POST", body: {} }).then(function (json) {
            var to = json && json.data && json.data.to_email;
            U.toast(to ? "Test envoyé vers " + to + "." : "Test journalisé.", "ok");
            loadEmailLog();
          }).catch(function (err) { U.toast((err && err.message) || "Test impossible.", "err"); });
        };
      }).catch(function () { smtpBox.innerHTML = "<p class='sub'>Réservé aux administrateurs connectés à l’API.</p>"; });
    }
    function loadEmailLog() {
      var logBox = document.getElementById("adm-email-log");
      if (!logBox || !api()) return;
      api().request("/emails?limit=30").then(function (json) {
        var rows = (json && json.data) || [];
        if (!rows.length) {
          logBox.innerHTML = "<p class='sub'>Aucun e-mail pour l’instant. Les actions recruteur / candidat apparaîtront ici.</p>";
          return;
        }
        logBox.innerHTML = '<div class="table-wrap"><table class="data"><thead><tr><th>Date</th><th>Destinataire</th><th>Sujet</th><th>Statut</th></tr></thead><tbody>' +
          rows.map(function (r) {
            return "<tr><td>" + U.esc((r.created_at || "").replace("T", " ").slice(0, 16)) + "</td><td>" +
              U.esc(r.to_email || "") + "</td><td>" + U.esc(r.subject || "") + "</td><td>" + U.esc(r.status || "") + "</td></tr>";
          }).join("") + "</tbody></table></div>";
      }).catch(function () { logBox.innerHTML = "<p class='sub'>Journal indisponible.</p>"; });
    }
    if (document.getElementById("adm-email-log")) loadEmailLog();
    bindKanban();
  }

  var avatarCache = window.__tlAdminAvatars || (window.__tlAdminAvatars = {});
  function adminToken() {
    try {
      var raw = sessionStorage.getItem("talendus-admin-session");
      var s = raw ? JSON.parse(raw) : null;
      if (s && s.access_token) return s.access_token;
    } catch (e) {}
    try { return localStorage.getItem("talendus_access_token") || ""; } catch (e2) { return ""; }
  }
  function warmAvatars() {
    var token = adminToken();
    if (!token) return;
    var ids = [];
    var me = TLStore.me();
    if (me && me.id) ids.push(me.id);
    (S().candidates || []).forEach(function (c) { if (c.userId && c.hasAvatar) ids.push(c.userId); });
    (S().users || []).forEach(function (u) { if (u.id && u.hasAvatar) ids.push(u.id); });
    (S().interviews || []).forEach(function (i) { if (i.candidateUserId && i.candidateHasAvatar) ids.push(i.candidateUserId); });
    var changed = false;
    var left = 0;
    ids.forEach(function (id) {
      if (avatarCache[id]) return;
      avatarCache[id] = "pending";
      left += 1;
      fetch("/api/users/" + encodeURIComponent(id) + "/avatar", {
        headers: { Authorization: "Bearer " + token }
      }).then(function (res) { return res.ok ? res.blob() : Promise.reject(); })
        .then(function (blob) {
          if (!blob || !blob.size) throw new Error("empty");
          avatarCache[id] = URL.createObjectURL(blob);
          changed = true;
        })
        .catch(function () { avatarCache[id] = "none"; })
        .then(function () {
          left -= 1;
          if (left <= 0 && changed) render();
        });
    });
  }

  function render() {
    var me = TLStore.me();
    var r = route();
    if (!me || r.name === "login") {
      if (me && r.name === "login") { go("#/" + firstModule()); }
      if (!me) { renderLogin(); return; }
    }
    if (!TLStore.can(r.name) && r.name !== "profile") {
      go("#/" + firstModule());
      r = route();
    }
    var html = U.skeleton();
    shell(html);
    setTimeout(function () {
      var inner = "";
      try {
        if (r.name === "dashboard") inner = viewDashboard();
        else if (r.name === "candidates" && r.id) inner = viewCandidate(r.id);
        else if (r.name === "candidates") inner = viewCandidates();
        else if (r.name === "clients" && r.id) inner = viewClient(r.id);
        else if (r.name === "clients") inner = viewClients();
        else if (r.name === "jobs" && r.id) inner = viewJob(r.id);
        else if (r.name === "jobs") inner = viewJobs();
        else if (r.name === "missions" && r.id) inner = viewMission(r.id);
        else if (r.name === "missions") inner = viewMissions();
        else if (r.name === "hiring" && r.id) inner = viewHiringDetail(r.id);
        else if (r.name === "hiring") inner = viewHiring();
        else if (r.name === "interviews") inner = viewInterviews();
        else if (r.name === "messages") inner = viewMessages();
        else if (r.name === "content") inner = viewContent();
        else if (r.name === "finance") inner = viewFinance();
        else if (r.name === "analytics") inner = viewAnalytics();
        else if (r.name === "services") inner = viewServices();
        else if (r.name === "notifications") inner = viewNotifications();
        else if (r.name === "settings") inner = viewSettings();
        else if (r.name === "profile") inner = viewProfile();
        else inner = viewDashboard();
      } catch (err) {
        inner = "<div class='card card-pad'><p>Erreur de rendu.</p></div>";
        console.error(err);
      }
      var v = document.getElementById("view");
      if (v) { v.innerHTML = inner; bindView(); }
      warmAvatars();
      if (r.name === "content") hydrateBlogCms();
      if (r.name === "messages") hydrateMessages();
      if (r.name === "services") hydrateServices();
      if (r.name === "analytics") hydrateAnalytics();
      if (r.name === "settings") hydrateTeam();
    }, 180);
  }

  window.addEventListener("hashchange", function () {
    page = 1; selected = new Set(); detailTab = "profil"; filters = {};
    render();
  });
  (async function boot() {
    if (TLStore.detectEnv) await TLStore.detectEnv();
    if (TLStore.restoreFromPublic) TLStore.restoreFromPublic();
    if (TLStore.me() && window.TalendusAPI && TLStore.hydrateFromApi) {
      var ok = await TLStore.hydrateFromApi();
      if (!ok) TLStore.logout();
    } else if (TLStore.me() && !TLStore.isLive()) {
      TLStore.logout();
    }
    render();
  })();
})();
