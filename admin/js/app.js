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

  function live() {
    return !!(window.TalendusAPI && TLStore.isLive && TLStore.isLive());
  }

  async function refreshLive() {
    if (TLStore.hydrateFromApi) await TLStore.hydrateFromApi();
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
      ["messages", "Messages", "fa-solid fa-comments"]
    ]],
    ["Pilotage", [
      ["content", "Contenu", "fa-solid fa-pen-nib"],
      ["finance", "Finance", "fa-solid fa-file-invoice-dollar"],
      ["analytics", "Statistiques", "fa-solid fa-chart-line"],
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
    var emailPrefill = production ? "lea.super@talendus.ca" : "sophie.admin@talendus.ca";
    var passPrefill = production ? "" : "talendus";
    var demo = production ? "" : `<div class="demo-accounts">
              Démo locale · mot de passe <b>talendus</b><br>
              <button type="button" data-fill="sophie.admin@talendus.ca">Admin</button> ·
              <button type="button" data-fill="marc.recruiter@talendus.ca">Recruteur</button> ·
              <button type="button" data-fill="nathalie.finance@talendus.ca">Finance</button> ·
              <button type="button" data-fill="alex.editeur@talendus.ca">Éditeur</button>
            </div>`;
    app.innerHTML = `
      <div class="login">
        <section class="login-brand">
          <div>
            <img src="../assets/img/logo/logo1.png" alt="Talendus">
            <div style="margin-top:28px"><span class="login-kicker">ATS / CRM interne</span></div>
            <h1>Le centre opérationnel de Talendus.</h1>
            <p>Candidats, clients, missions, offres, besoins et messages — une seule plateforme, liée au site et aux espaces.</p>
          </div>
          <div class="login-meta">
            <div><b>1 200+</b>Talents en réseau</div>
            <div><b>7 j</b>Shortlist type</div>
            <div><b>92 %</b>Rétention post-essai</div>
          </div>
        </section>
        <section class="login-panel">
          <div class="login-card">
            <h2>Connexion</h2>
            <p class="sub">${production ? "Serveur de production — compte staff uniquement (ADMIN_EMAIL sur Render)." : "Espace privé — accès réservé à l’équipe Talendus."}</p>
            <form id="login-form" class="form-grid" style="grid-template-columns:1fr">
              ${U.field("Courriel", "email", emailPrefill, "email")}
              ${U.field("Mot de passe", "password", passPrefill, "password")}
              <button class="btn btn-orange" type="submit">Entrer dans le back-office</button>
            </form>
            ${demo}
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
        else U.toast("Identifiants incorrects.", "err");
        return;
      }
      U.toast("Bienvenue " + u.firstName + ".", "ok");
      go("#/" + firstModule());
      render();
    };
    U.$$("[data-fill]").forEach(function (b) {
      b.onclick = function () {
        $("input[name=email]").value = b.getAttribute("data-fill");
        $("input[name=password]").value = "talendus";
      };
    });
  }

  /* ---------- Shell ---------- */
  function unread() {
    return S().notifications.filter(function (n) { return !n.read; }).length;
  }

  function shell(inner) {
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
      <div class="page-head"><div><h1>Tableau de bord</h1><p>${live() ? "Données live — les mêmes que le site et les espaces candidat / entreprise." : "Vue démo locale."} — ${U.dateFr(today)}</p></div>
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
      if (f.lang && c.languages.join(" ").indexOf(f.lang) === -1) return false;
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
        <td><div class="person">${U.avatar({ firstName: c.firstName, lastName: c.lastName })}<div><b>${U.esc(c.firstName + " " + c.lastName)}</b><span>${U.esc(c.email)}</span></div></div></td>
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
          <div class="row"><span>Langues</span><b>${U.esc(c.languages.join(", "))}</b></div>
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
      body = '<div class="card card-pad"><h3>Documents</h3>' + (docs.map(function (d) { return "<p><i class='fa-regular fa-file'></i> " + U.esc(d.name) + " · " + d.size + "</p>"; }).join("") || "<p>Aucun document. Téléversement simulé.</p>") + '<button class="btn btn-ghost" data-fake-upload>Ajouter un document</button></div>';
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
      body = '<div class="card card-pad"><h3>Entretiens</h3>' + (ints.map(function (i) { return "<p><b>" + U.esc(i.type) + "</b> — " + U.esc(i.at) + " · " + U.esc(i.location) + "</p>"; }).join("") || "<p>Aucun entretien.</p>") + '<button class="btn btn-orange" data-add-int="' + id + '">Planifier</button></div>';
    } else if (detailTab === "notes") {
      body = '<div class="card card-pad"><h3>Notes internes (invisibles pour le candidat)</h3>' + notes.map(function (n) {
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
          ${U.avatar({ firstName: c.firstName, lastName: c.lastName }, "lg")}
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
        <tbody>${rows}</tbody></table></div></div>`;
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
        <div class="actions"><button class="btn btn-ghost" data-add-contract="${id}">Nouveau contrat</button></div></div>
      <div class="grid grid-2">
        <div class="card card-pad"><h3>Informations générales</h3>
          <div class="row"><span>Employés</span><b>${c.employees}</b></div>
          <div class="row"><span>Client depuis</span><b>${U.dateFr(c.since)}</b></div>
          <div class="row"><span>Site</span><b>${U.esc(c.website)}</b></div>
          <h3 style="margin-top:16px">Contacts</h3>
          <p><b>${U.esc(c.contact)}</b><br>${U.esc(c.email)}<br>${U.esc(c.phone)}</p>
        </div>
        <div class="card card-pad"><h3>Contrats</h3>${contracts.map(function (ct) {
          var signBtn = ct.signed
            ? "<p style='color:var(--steel);font-size:12px'>Signé " + U.esc(ct.signedAt || "") + " · " + U.esc(ct.signerName || "") + (ct.documentHash ? "<br>Hash " + U.esc(ct.documentHash.slice(0, 12)) + "…" : "") + "</p>"
            : '<button class="btn btn-ghost btn-sm" data-sign-contract="' + ct.id + '">Enregistrer la signature</button>';
          return "<p><b>" + U.esc(ct.type) + "</b> · " + U.badge(ct.status) + "<br>Commission " + ct.commission + " % · " + U.dateFr(ct.start) + " → " + U.dateFr(ct.end) + "<br><span style='color:var(--steel)'>" + U.esc(ct.terms) + "</span></p>" + signBtn;
        }).join("") || "<p>Aucun contrat.</p>"}</div>
      </div>
      <div class="grid grid-2" style="margin-top:16px">
        <div class="card card-pad"><h3>Missions</h3>${missions.map(function (m) { return '<p><a href="#/missions/' + m.id + '">' + U.esc(m.title) + "</a> " + U.badge(m.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
        <div class="card card-pad"><h3>Offres d’emploi</h3>${jobs.map(function (j) { return '<p><a href="#/jobs/' + j.id + '">' + U.esc(j.title) + "</a> " + U.badge(j.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
      </div>
      <div class="grid grid-2" style="margin-top:16px">
        <div class="card card-pad"><h3>Candidats présentés / placements</h3>${cands.map(function (x) { return '<p><a href="#/candidates/' + x.id + '">' + U.esc(x.firstName + " " + x.lastName) + "</a> " + U.badge(x.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
        <div class="card card-pad"><h3>Factures & paiements</h3>${inv.map(function (i) { return "<p>" + i.id + " · " + U.money(i.amount) + " " + U.badge(i.status) + "</p>"; }).join("") || "<p>—</p>"}</div>
      </div>
      <div class="card card-pad" style="margin-top:16px"><h3>Notes internes</h3>${notes.map(function (n) { return '<div class="note">' + U.esc(n.text) + " <span class='meta'>· " + U.esc(n.at) + "</span></div>"; }).join("") || "<p>Aucune note.</p>"}</div>`;
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
      return `<tr data-go="#/jobs/${j.id}"><td><b>${U.esc(j.title)}</b></td><td>${U.esc(cl ? cl.name : "—")}</td><td>${U.esc(j.city)}</td><td>${U.esc(j.sector)}</td><td>${U.esc(j.type)}</td><td>${U.esc(j.salary)}</td><td>${U.badge(j.status)}</td><td>${j.applications}</td>
        <td onclick="event.stopPropagation()">
          <button class="btn btn-ghost btn-sm" data-job-act="dup:${j.id}">Dupliquer</button>
        </td></tr>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Offres d’emploi</h1><p>Publication vers le site public Talendus</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="job">Créer une offre</button></div></div>
      <div class="filters">
        <input data-f="q" placeholder="Titre" value="${U.esc(filters.q || "")}">
        <select data-f="status"><option value="">Statut</option>${["brouillon","publiee","suspendue","expiree","archivee"].map(function (s) { return "<option value=\"" + s + "\"" + (filters.status === s ? " selected" : "") + ">" + U.STATUS[s][0] + "</option>"; }).join("")}</select>
      </div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Titre</th><th>Entreprise</th><th>Localisation</th><th>Secteur</th><th>Type</th><th>Salaire</th><th>Statut</th><th>Candidatures</th><th></th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
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
          <div class="row"><span>Type</span><b>${U.esc(j.type)}</b></div>
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
      <div class="page-head"><div><h1>Missions</h1><p>Mandats et pipeline — les statuts kanban s’enregistrent dans l’API et se voient dans les espaces.</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="mission">Nouvelle mission</button></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Mission</th><th>Client</th><th>Poste</th><th>Postes</th><th>Recruteur</th><th>Début</th><th>Échéance</th><th>Statut</th><th>Candidats</th><th>Progression</th><th>Valeur</th><th>Commission</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
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
      <p style="color:var(--steel);margin-top:12px">Glissez-déposez les candidats d’une étape à l’autre. Le statut est enregistré dans l’API et se reflète dans les espaces.</p>`;
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
      <div class="page-head"><div><h1>Besoins de recrutement</h1><p>Ce que les entreprises transmettent dans leur espace — Talendus convertit, publie, puis présente les profils.</p></div></div>
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
      <div class="page-head"><div><h1>Messages</h1><p>Fils avec les candidats et les entreprises — jamais d’échange direct entre eux.</p></div></div>
      <div class="grid grid-2" id="msg-root"><div class="card card-pad"><p class="sub">Chargement des conversations…</p></div></div>`;
  }

  async function hydrateMessages() {
    var root = document.getElementById("msg-root");
    if (!root || !window.TalendusAPI) return;
    try {
      var threads = await window.TalendusAPI.request("/messages");
      var directory = await window.TalendusAPI.request("/messages/directory");
      var list = threads.data || [];
      var people = directory.data || [];
      var opts = people.map(function (p) {
        return '<option value="' + U.esc(p.id) + '">' + U.esc((p.first_name || "") + " " + (p.last_name || "") + " · " + (p.role || "")) + "</option>";
      }).join("");
      var items = list.map(function (th) {
        return '<button type="button" class="n-item ' + (th.unread ? "unread" : "") + '" data-open-thread="' + U.esc(th.user_id) + '"><b>' +
          U.esc((th.first_name || "") + " " + (th.last_name || "")) + "</b><div style='color:var(--steel);font-size:12px'>" + U.esc(th.last_message || "") + "</div></button>";
      }).join("") || "<p class='sub'>Aucun message pour le moment.</p>";
      root.innerHTML =
        '<div class="card card-pad"><div class="card-head"><h3>Conversations</h3></div>' + items + "</div>" +
        '<div class="card card-pad"><form id="msg-form" class="form-grid" style="grid-template-columns:1fr">' +
        U.field("Destinataire", "recipient_id", { options: people.map(function (p) { return { v: p.id, l: (p.first_name || "") + " " + (p.last_name || "") + " · " + (p.role || "") }; }), selected: people[0] && people[0].id }, "select") +
        U.field("Message", "body", "", "textarea", "full") +
        '<button class="btn btn-orange" type="submit">Envoyer</button></form><div id="msg-thread"></div></div>';
      var form = document.getElementById("msg-form");
      if (form) form.onsubmit = function (e) {
        e.preventDefault();
        var d = U.formData(form);
        window.TalendusAPI.request("/messages", { method: "POST", body: { recipient_id: d.recipient_id, body: d.body } }).then(function () {
          U.toast("Message envoyé.", "ok");
          hydrateMessages();
        }).catch(function (err) { U.toast((err && err.message) || "Envoi impossible.", "err"); });
      };
      root.querySelectorAll("[data-open-thread]").forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute("data-open-thread");
          var select = form && form.querySelector("[name=recipient_id]");
          if (select) select.value = id;
          window.TalendusAPI.request("/messages/" + id).then(function (json) {
            var me = TLStore.me();
            document.getElementById("msg-thread").innerHTML = (json.data || []).map(function (m) {
              var mine = me && m.sender_id === me.id;
              return '<div class="note ' + (mine ? "is-mine" : "") + '"><div class="meta">' + U.esc(m.sender_name || "") + "</div>" + U.esc(m.body) + "</div>";
            }).join("");
          });
        };
      });
    } catch (err) {
      root.innerHTML = "<div class='card card-pad'><p>Impossible de charger les messages. Vérifiez la connexion API.</p></div>";
    }
  }

  /* ---------- Content ---------- */
  function viewContent() {
    var map = { pages: S().pages, blog: [], temoignages: S().testimonials, faq: S().faqs, seo: S().posts };
    var labels = { pages: "Pages du site", blog: "Blog", temoignages: "Témoignages", faq: "FAQ", seo: "Contenu SEO" };
    var items = map[contentTab] || [];
    var rows = items.map(function (it) {
      return `<tr><td><b>${U.esc(it.title || it.q || it.author)}</b></td><td>${U.esc(it.slug || it.seo || it.role || "")}</td><td>${U.badge(it.status)}</td><td>${U.esc(it.updatedAt || "—")}</td>
        <td><button class="btn btn-ghost btn-sm" data-cms="edit:${contentTab}:${it.id}">Modifier</button>
            <button class="btn btn-ghost btn-sm" data-cms="prev:${contentTab}:${it.id}">Prévisualiser</button>
            <button class="btn btn-ghost btn-sm" data-cms="toggle:${contentTab}:${it.id}">${it.status === "publie" || it.status === "publiee" ? "Dépublier" : "Publier"}</button>
            <button class="btn btn-ghost btn-sm" data-cms="arch:${contentTab}:${it.id}">Archiver</button></td></tr>`;
    }).join("");
    if (contentTab === "blog") {
      rows = '<tr><td colspan="5">Chargement des articles…</td></tr>';
    }
    return `
      <div class="page-head"><div><h1>Contenu</h1><p>CMS du site public talendus.ca — le blog est enregistré dans l’API (brouillon, publication, programmation).</p></div>
        <div class="actions"><button class="btn btn-orange" data-cms="new:${contentTab}">Créer</button></div></div>
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
      body = `<div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>N°</th><th>Client</th><th>Mission</th><th>Montant</th><th>Date</th><th>Échéance</th><th>Statut</th></tr></thead><tbody>${inv.map(function (i) {
        var cl = TLStore.client(i.clientId); var m = TLStore.mission(i.missionId);
        return "<tr><td>" + i.id + "</td><td>" + U.esc(cl ? cl.name : "—") + "</td><td>" + U.esc(m ? m.title : "—") + "</td><td>" + U.money(i.amount) + "</td><td>" + U.dateFr(i.date) + "</td><td>" + U.dateFr(i.due) + "</td><td>" + U.badge(i.status) + "</td></tr>";
      }).join("")}</tbody></table></div></div>`;
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
      <div class="page-head"><div><h1>Finance</h1><p>Factures, paiements et commissions</p></div>
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
    var avg = placed ? Math.round(revenue / placed) : 0;
    return `
      <div class="page-head"><div><h1>Statistiques</h1><p>Reporting Talendus · période ${period}</p></div>
        <div class="actions"><button class="btn btn-ghost" data-export-an>Exporter Excel/CSV</button></div></div>
      <div class="filters">
        ${["jour","semaine","mois","trimestre","annee"].map(function (p) { return '<button class="btn btn-sm ' + (period === p ? "btn-orange" : "btn-ghost") + '" data-period="' + p + '">' + p + "</button>"; }).join("")}
        <select id="an-rec"><option value="">Recruteur</option>${st.users.filter(function (u) { return u.role !== "editor"; }).map(function (u) { return "<option value=\"" + u.id + "\"" + (analyticsRecruiter === u.id ? " selected" : "") + ">" + u.firstName + " " + u.lastName + "</option>"; }).join("")}</select>
        <select id="an-sec"><option value="">Secteur</option>${unique(st.candidates, "sector").map(function (s) { return "<option" + (analyticsSector === s ? " selected" : "") + ">" + s + "</option>"; }).join("")}</select>
      </div>
      <div class="grid grid-4" style="margin-bottom:16px">
        ${kpi("Candidats", cands.length, "+" + cands.filter(function (c) { return c.createdAt >= "2026-08-01"; }).length + " nouveaux")}
        ${kpi("Clients", st.clients.length, "dont 1 prospect")}
        ${kpi("Offres", st.jobs.length, apps + " candidatures")}
        ${kpi("Entretiens", interviews, placed + " placements")}
      </div>
      <div class="grid grid-4" style="margin-bottom:16px">
        ${kpi("Taux de placement", Math.round(placed / Math.max(1, cands.length) * 100) + " %")}
        ${kpi("Délai moyen", "18 j")}
        ${kpi("Revenus", U.money(revenue))}
        ${kpi("Valeur moyenne", U.money(avg))}
      </div>
      <div class="grid grid-2">
        <div class="card card-pad"><h3>Revenus</h3>${U.barChart(st.monthly.months, st.monthly.revenue, "#ff6b00")}</div>
        <div class="card card-pad"><h3>Candidatures vs placements</h3>${U.lineChart(st.monthly.applications, "#1e6bff")}${U.lineChart(st.monthly.placements, "#ff6b00")}</div>
      </div>
      <div class="card card-pad" style="margin-top:16px"><h3>Revenus par recruteur</h3>
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

  function viewNotifications() {
    return `<div class="page-head"><div><h1>Notifications</h1><p>Centre d’alertes opérationnelles</p></div>
      <div class="actions"><button class="btn btn-ghost" id="mark-all">Tout marquer lu</button></div></div>
      <div class="card">${S().notifications.map(function (n) {
        return '<div class="n-item ' + (n.read ? "" : "unread") + '"><a href="' + n.href + '"><b>' + U.esc(n.text) + "</b></a><div style='color:var(--steel);font-size:12px'>" + U.esc(n.at) + " · " + n.type + "</div></div>";
      }).join("")}</div>`;
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
      admin: "Vous voyez tout le centre opérationnel, y compris la configuration de la plateforme.",
      recruiter: "Vous suivez les mandats, les candidats et les clients. La finance et le contenu du site restent hors de cet accès.",
      finance: "Vous suivez la facturation et les statistiques. Les dossiers candidats restent à l’équipe de recrutement.",
      editor: "Vous gérez le contenu public. Les mandats et la finance restent à l’équipe de recrutement."
    };
    return `
      <div class="page-head"><div><h1>Paramètres</h1><p>${U.esc(personaLead[me.role] || personaLead.recruiter)}</p></div></div>
      <div class="settings-tabs" role="tablist">
        <button type="button" class="settings-tab is-active" data-stab="account">Compte</button>
        <button type="button" class="settings-tab" data-stab="security">Sécurité</button>
        <button type="button" class="settings-tab" data-stab="access">Accès selon le rôle</button>
        ${admin ? '<button type="button" class="settings-tab" data-stab="platform">Plateforme</button>' : ""}
      </div>
      <div class="settings-panel" data-spanel="account">
        <div class="card card-pad">
          <div class="card-head"><h3>Votre compte Talendus</h3></div>
          <p class="sub">${U.esc(me.email)} · ${roleLabel(me.role)}</p>
          <p>Les entreprises et les candidats ne voient jamais cet espace. C’est l’outil interne de l’agence.</p>
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
          <div class="card-pad"><p>Chaque rôle du back-office ne voit que ce dont il a besoin. Les espaces candidat et entreprise restent séparés de cet outil.</p></div>
          <div class="table-wrap"><table class="data"><thead><tr><th>Zone</th><th>Recruteur</th><th>Finance</th><th>Éditeur</th><th>Admin</th></tr></thead><tbody>
          ${access.map(function (row) { return "<tr><td>" + U.esc(row[0]) + "</td>" + marks(row) + "</tr>"; }).join("")}
          </tbody></table></div>
        </div>
      </div>
      ${admin ? `<div class="settings-panel" data-spanel="platform" hidden>
        <div class="card card-pad">
          <div class="card-head"><h3>Plateforme</h3></div>
          <p class="sub">Réglages internes de l’agence — pas visibles sur le site public.</p>
          <div id="adm-platform"><p class="sub">Chargement…</p></div>
          <p style="margin-top:16px"><button class="btn btn-danger" id="reset-demo">Réinitialiser les données démo</button></p>
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
          <p>Modules : ${(TLStore.PERMS[me.role] || []).join(" · ")}</p>
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

    var body = "";
    if (type === "candidate") {
      body = '<form id="cf" class="form-grid">' + U.field("Prénom", "firstName") + U.field("Nom", "lastName") + U.field("Courriel", "email", "", "email") + U.field("Téléphone", "phone") + U.field("Ville", "city") + U.field("Poste recherché", "title") + U.field("Secteur", "sector", { options: unique(S().candidates, "sector"), selected: "" }, "select") + U.field("Statut", "status", { options: ["nouveau","a-contacter","qualifie"].map(function (s) { return { v: s, l: U.STATUS[s][0] }; }), selected: "nouveau" }, "select") + "</form>";
    } else if (type === "client") {
      body = '<form id="cf" class="form-grid">' + U.field("Entreprise", "name") + U.field("Secteur", "sector") + U.field("Ville", "city") + U.field("Contact", "contact") + U.field("Courriel", "email") + U.field("Téléphone", "phone") + "</form>";
    } else if (type === "job") {
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Entreprise", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0] && S().clients[0].id }, "select") + U.field("Ville", "city") + U.field("Salaire", "salary") + U.field("Description", "description", "", "textarea", "full") + "</form>";
    } else if (type === "mission") {
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0].id }, "select") + U.field("Offre", "jobId", { options: S().jobs.map(function (j) { return { v: j.id, l: j.title }; }), selected: S().jobs[0].id }, "select") + U.field("Nombre de postes", "seats", "1", "number") + "</form>";
    } else {
      body = '<form id="cf" class="form-grid">' + U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0].id }, "select") + U.field("Mission", "missionId", { options: S().missions.map(function (m) { return { v: m.id, l: m.title }; }), selected: S().missions[0].id }, "select") + U.field("Montant", "amount", "5000", "number") + "</form>";
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
              await refreshLive();
              close();
              U.toast("Candidat créé — visible dans l’espace talent une fois connecté.", "ok");
              render();
              return;
            }
            if (type === "job" && window.TalendusAPI && d.clientId) {
              var created = await window.TalendusAPI.request("/jobs", {
                method: "POST",
                body: { title: d.title, company_id: d.clientId, location: d.city, salary_display: d.salary, description: d.description }
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
                body: { name: d.name, sector: d.sector, city: d.city, contact_name: d.contact, email: d.email, phone: d.phone }
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
                body: { title: d.title, company_id: d.clientId, job_id: d.jobId, seats: Number(d.seats) || 1 }
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Mission créée.", "ok");
              render();
              return;
            }
            if (type === "invoice" && window.TalendusAPI) {
              await window.TalendusAPI.createInvoice({
                company_id: d.clientId,
                mission_id: d.missionId || null,
                amount: Number(d.amount) || 0
              });
              await TLStore.hydrateFromApi();
              close();
              U.toast("Facture créée dans l’API.", "ok");
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
              st.jobs.unshift({ id: TLStore.nid("j"), title: d.title, clientId: d.clientId, city: d.city, sector: "Production", type: "Permanent", salary: d.salary, shift: "Quart de jour", status: publish ? "publiee" : "brouillon", publishedAt: publish ? new Date().toISOString().slice(0, 10) : "", expiresAt: "", applications: 0, experience: "—", skills: "", benefits: "", description: d.description, responsibilities: "", qualifications: "" });
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
                var appId = cand && cand.applicationId;
                if (appId && CAND_STATUS_TO_APP[stt]) {
                  await window.TalendusAPI.request("/applications/" + appId + "/status", { method: "POST", body: { status: CAND_STATUS_TO_APP[stt] } });
                }
              }
              await refreshLive();
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
            body: '<form id="jf" class="form-grid">' + U.field("Titre", "title", j.title) + U.field("Salaire", "salary", j.salary) + U.field("Description", "description", j.description, "textarea", "full") + "</form>",
            footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
            onMount: function (box, close) {
              box.querySelector("#save").onclick = async function () {
                var d = U.formData(box.querySelector("#jf"));
                try {
                  if (live()) {
                    await window.TalendusAPI.request("/jobs/" + jid, { method: "PATCH", body: { title: d.title, salary_display: d.salary, description: d.description } });
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
        if (action === "new" || action === "edit") {
          var item = cid ? S()[col].find(function (x) { return x.id === cid; }) : { title: "", q: "", seo: "" };
          U.modal({
            title: action === "new" ? "Nouveau contenu" : "Éditeur",
            body: '<form id="ef">' + U.field("Titre / question", "title", item.title || item.q || item.author || "") + U.field("Contenu", "body", item.a || item.quote || item.seo || "", "textarea", "full") + "</form>",
            footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Publier</button>',
            onMount: function (box, close) {
              box.querySelector("#save").onclick = function () {
                var d = U.formData(box.querySelector("#ef"));
                TLStore.update(function (st) {
                  if (action === "new") {
                    st[col].unshift({ id: TLStore.nid("x"), title: d.title, q: d.title, author: d.title, quote: d.body, a: d.body, seo: d.body, slug: "/nouveau", status: "brouillon", updatedAt: "2026-08-16", authorId: TLStore.me().id });
                  } else {
                    var it = st[col].find(function (x) { return x.id === cid; });
                    if (it) { it.title = d.title; it.q = d.title; it.a = d.body; it.quote = d.body; it.updatedAt = "2026-08-16"; }
                  }
                });
                close(); U.toast("Contenu enregistré.", "ok"); render();
              };
            }
          });
        } else if (action === "prev") {
          U.modal({ title: "Prévisualisation", body: "<p>Aperçu du contenu destiné au site public.</p>", footer: '<button class="btn btn-ghost" data-close>Fermer</button>' });
        } else if (action === "toggle" || action === "arch") {
          TLStore.update(function (st) {
            var it = st[col].find(function (x) { return x.id === cid; });
            if (!it) return;
            if (action === "arch") it.status = "archive";
            else it.status = (it.status === "publie" || it.status === "publiee") ? "brouillon" : "publie";
          });
          U.toast("Statut contenu mis à jour.", "ok"); render();
        }
      }
      if (t.closest("[data-fake-upload]")) U.toast("Téléversement simulé — brancher le stockage fichiers ensuite.", "ok");
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
            U.field("Date et heure", "scheduled_at", "2026-08-20T10:00", "datetime-local") +
            U.field("Lieu", "location", "Visio") +
            U.field("Type", "type", { options: [{ v: "TALENDUS", l: "Talendus" }, { v: "CLIENT", l: "Client" }, { v: "VIDEO", l: "Visio" }, { v: "PHONE", l: "Téléphone" }, { v: "ONSITE", l: "Sur place" }], selected: "TALENDUS" }, "select") +
            "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Planifier</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#int-form"));
              try {
                if (window.TalendusAPI) {
                  await window.TalendusAPI.createInterview({
                    candidate_id: cid,
                    scheduled_at: d.scheduled_at,
                    location: d.location,
                    type: d.type
                  });
                  await TLStore.hydrateFromApi();
                  close();
                  U.toast("Entretien enregistré.", "ok");
                  render();
                  return;
                }
              } catch (err) {
                U.toast((err && err.message) || "API indisponible, repli local.", "err");
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
      var signCt = t.closest("[data-sign-contract]");
      if (signCt) {
        var contractId = signCt.getAttribute("data-sign-contract");
        U.modal({
          title: "Signature interne du mandat",
          body: '<form id="sg-form">' + U.field("Nom du signataire", "signer_name", TLStore.me().firstName + " " + TLStore.me().lastName) + "<p>Trace interne : nom, date, IP et empreinte du document. Ce n’est pas une signature notariale ni DocuSign.</p></form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Signer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = async function () {
              var d = U.formData(box.querySelector("#sg-form"));
              try {
                await window.TalendusAPI.signContract(contractId, { signer_name: d.signer_name, accepted: true });
                await TLStore.hydrateFromApi();
                close();
                U.toast("Signature enregistrée.", "ok");
                render();
              } catch (err) {
                U.toast((err && err.message) || "Signature impossible.", "err");
              }
            };
          }
        });
        return;
      }
      var addCt = t.closest("[data-add-contract]");
      if (addCt) {
        TLStore.update(function (st) {
          st.contracts.push({ id: TLStore.nid("ct"), clientId: addCt.getAttribute("data-add-contract"), type: "Succès", start: "2026-08-16", end: "2027-08-16", commission: 16, terms: "16 % au succès, garantie 90 jours.", status: "Actif", document: "nouveau-contrat.pdf" });
        });
        U.toast("Contrat ajouté.", "ok"); render();
      }
      var editC = t.closest("[data-edit-cand]");
      if (editC) {
        var c = TLStore.candidate(editC.getAttribute("data-edit-cand"));
        U.modal({
          title: "Modifier le candidat",
          body: '<form id="ec" class="form-grid">' + U.field("Ville", "city", c.city) + U.field("Poste", "title", c.title) + U.field("Disponibilité", "availability", c.availability) + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = function () {
              var d = U.formData(box.querySelector("#ec"));
              TLStore.update(function (st) { Object.assign(st.candidates.find(function (x) { return x.id === c.id; }), d); });
              close(); U.toast("Fiche mise à jour.", "ok"); render();
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
          if (live() && cand && cand.applicationId && CAND_STATUS_TO_APP[next]) {
            try {
              await window.TalendusAPI.request("/applications/" + cand.applicationId + "/status", { method: "POST", body: { status: CAND_STATUS_TO_APP[next] } });
              await refreshLive();
              U.toast("Statut enregistré — le candidat le voit dans son espace.", "ok");
              render();
              return;
            } catch (err) {
              U.toast((err && err.message) || "Statut non enregistré.", "err");
              return;
            }
          }
          TLStore.update(function (st) { st.candidates.find(function (c) { return c.id === id; }).status = next; });
          U.toast("Statut candidat mis à jour.", "ok");
          render();
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
          U.toast("Note interne enregistrée (invisible pour le candidat).", "ok");
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
        var rows = (json && json.data) || [];
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
    bindKanban();
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
        else if (r.name === "messages") inner = viewMessages();
        else if (r.name === "content") inner = viewContent();
        else if (r.name === "finance") inner = viewFinance();
        else if (r.name === "analytics") inner = viewAnalytics();
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
      if (r.name === "content") hydrateBlogCms();
      if (r.name === "messages") hydrateMessages();
    }, 180);
  }

  window.addEventListener("hashchange", function () {
    page = 1; selected = new Set(); detailTab = "profil"; filters = {};
    render();
  });
  (async function boot() {
    if (TLStore.detectEnv) await TLStore.detectEnv();
    if (TLStore.apiEnv === "production" && TLStore.me() && !TLStore.isLive()) {
      TLStore.logout();
    }
    if (TLStore.me() && window.TalendusAPI && TLStore.hydrateFromApi && TLStore.isLive()) {
      await TLStore.hydrateFromApi();
    }
    render();
  })();
})();
