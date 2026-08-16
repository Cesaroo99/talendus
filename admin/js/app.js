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

  const NAV = [
    ["Ops", [
      ["dashboard", "Tableau de bord", "fa-solid fa-grip"],
      ["candidates", "Candidats", "fa-solid fa-users"],
      ["clients", "Clients", "fa-solid fa-industry"],
      ["jobs", "Offres d’emploi", "fa-solid fa-briefcase"],
      ["missions", "Missions", "fa-solid fa-diagram-project"]
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
    app.innerHTML = `
      <div class="login">
        <section class="login-brand">
          <div>
            <img src="../assets/img/logo/logo1.png" alt="Talendus">
            <div style="margin-top:28px"><span class="login-kicker">ATS / CRM interne</span></div>
            <h1>Le centre opérationnel de Talendus.</h1>
            <p>Candidats, clients, missions, offres, contenu et finance — une seule plateforme pour l’équipe de recrutement industriel.</p>
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
            <p class="sub">Espace privé — accès réservé à l’équipe Talendus.</p>
            <form id="login-form" class="form-grid" style="grid-template-columns:1fr">
              ${U.field("Courriel", "email", "sophie.admin@talendus.ca", "email")}
              ${U.field("Mot de passe", "password", "talendus", "password")}
              <button class="btn btn-orange" type="submit">Entrer dans le back-office</button>
            </form>
            <div class="demo-accounts">
              Démo · mot de passe <b>talendus</b><br>
              <button type="button" data-fill="sophie.admin@talendus.ca">Admin</button> ·
              <button type="button" data-fill="marc.recruiter@talendus.ca">Recruteur</button> ·
              <button type="button" data-fill="nathalie.finance@talendus.ca">Finance</button> ·
              <button type="button" data-fill="alex.editeur@talendus.ca">Éditeur</button>
            </div>
          </div>
        </section>
      </div>`;
    $("#login-form").onsubmit = function (e) {
      e.preventDefault();
      var d = U.formData(e.target);
      var u = TLStore.login(d.email, d.password);
      if (!u) { U.toast("Identifiants incorrects.", "err"); return; }
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
        var count = i[0] === "notifications" && unread() ? '<span class="count">' + unread() + "</span>" : "";
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
      TLStore.update(function (st) {
        var n = st.notifications.find(function (x) { return x.id === row.getAttribute("data-n"); });
        if (n) n.read = true;
      });
      go(row.getAttribute("data-href"));
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
    var placed = st.candidates.filter(function (c) { return c.status === "place"; }).length;
    var activeJobs = st.jobs.filter(function (j) { return j.status === "publiee"; }).length;
    var activeClients = st.clients.filter(function (c) { return c.status === "Actif"; }).length;
    var openM = st.missions.filter(function (m) { return m.status === "en-cours"; }).length;
    var unpaid = st.invoices.filter(function (i) { return i.status === "en-attente" || i.status === "en-retard" || i.status === "envoyee"; });
    var revenue = st.invoices.filter(function (i) { return i.status === "payee"; }).reduce(function (s, i) { return s + i.amount; }, 0);
    var rate = Math.round((placed / Math.max(1, st.candidates.length)) * 100);
    var newbie = st.candidates.filter(function (c) { return c.createdAt >= "2026-08-01"; }).length;
    var bySector = {};
    st.candidates.forEach(function (c) { bySector[c.sector] = (bySector[c.sector] || 0) + 1; });
    var byStatus = {};
    st.candidates.forEach(function (c) { byStatus[c.status] = (byStatus[c.status] || 0) + 1; });
    var recPerf = ["u-marc", "u-camille", "u-sophie"].map(function (id) {
      var n = st.candidates.filter(function (c) { return c.recruiterId === id && c.status === "place"; }).length;
      return { l: TLStore.name(id).split(" ")[0], v: n, c: id === "u-marc" ? "#1e6bff" : id === "u-camille" ? "#ff6b00" : "#0b1f3a" };
    });

    return `
      <div class="page-head"><div><h1>Tableau de bord</h1><p>Vue synthétique de l’activité Talendus — ${U.dateFr("2026-08-16")}</p></div>
        <div class="actions"><button class="btn btn-ghost btn-sm" data-export-dash>Exporter CSV</button></div></div>
      <div class="grid grid-6" style="margin-bottom:16px">
        ${kpi("Candidats", st.candidates.length, "+ " + newbie + " ce mois")}
        ${kpi("Nouveaux", newbie, "depuis le 1er août")}
        ${kpi("Clients actifs", activeClients, st.clients.length + " au total")}
        ${kpi("Offres actives", activeJobs, st.jobs.length + " au catalogue")}
        ${kpi("Missions en cours", openM, placed + " placements")}
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
      body = `<div class="card card-pad"><h3>Historique des candidatures</h3>
        <p>Offre liée : <a href="#/jobs/${c.jobId}">${U.esc((TLStore.job(c.jobId) || {}).title || "—")}</a></p>
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
        <div class="card card-pad"><h3>Contrats</h3>${contracts.map(function (ct) { return "<p><b>" + U.esc(ct.type) + "</b> · " + U.badge(ct.status) + "<br>Commission " + ct.commission + " % · " + U.dateFr(ct.start) + " → " + U.dateFr(ct.end) + "<br><span style='color:var(--steel)'>" + U.esc(ct.terms) + "</span></p>"; }).join("") || "<p>Aucun contrat.</p>"}</div>
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
      <div class="page-head"><div><h1>Missions</h1><p>Mandats clients et pipeline de recrutement</p></div>
        <div class="actions"><button class="btn btn-orange" data-create="mission">Nouvelle mission</button></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Mission</th><th>Client</th><th>Poste</th><th>Postes</th><th>Recruteur</th><th>Début</th><th>Échéance</th><th>Statut</th><th>Candidats</th><th>Progression</th><th>Valeur</th><th>Commission</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
  }

  function viewMission(id) {
    var m = TLStore.mission(id);
    if (!m) return U.empty("Introuvable", "Mission introuvable.");
    var cols = U.STAGES.map(function (st) {
      var cards = Object.keys(m.stageMap || {}).filter(function (cid) { return m.stageMap[cid] === st[0]; }).map(function (cid) {
        var c = TLStore.candidate(cid);
        if (!c) return "";
        return '<div class="kanban-card" draggable="true" data-cid="' + cid + '"><b>' + U.esc(c.firstName + " " + c.lastName) + "</b><span>" + U.esc(c.title) + "</span></div>";
      }).join("");
      var n = Object.keys(m.stageMap || {}).filter(function (cid) { return m.stageMap[cid] === st[0]; }).length;
      return '<div class="kanban-col" data-stage="' + st[0] + '"><h4>' + st[1] + " <span class='badge'>" + n + "</span></h4>" + (cards || '<p style="color:var(--steel);font-size:12px">Déposez un candidat</p>') + "</div>";
    }).join("");
    return `
      <div class="crumbs"><a href="#/missions">Missions</a> / ${U.esc(m.title)}</div>
      <div class="page-head"><div><h1>${U.esc(m.title)}</h1><p>${U.esc((TLStore.client(m.clientId) || {}).name || "—")} · ${m.seats} poste(s) · échéance ${U.dateFr(m.due)} · ${U.badge(m.status)}</p></div>
        <div class="actions"><span class="badge orange">Valeur ${U.money(m.value)}</span><span class="badge info">Commission ${U.money(m.commission)}</span></div></div>
      <div class="kanban" data-mission="${m.id}">${cols}</div>
      <p style="color:var(--steel);margin-top:12px">Glissez-déposez les candidats d’une étape à l’autre.</p>`;
  }

  /* ---------- Content ---------- */
  function viewContent() {
    var map = { pages: S().pages, blog: S().posts, temoignages: S().testimonials, faq: S().faqs, seo: S().posts };
    var labels = { pages: "Pages du site", blog: "Blog", temoignages: "Témoignages", faq: "FAQ", seo: "Contenu SEO" };
    var items = map[contentTab] || [];
    var rows = items.map(function (it) {
      return `<tr><td><b>${U.esc(it.title || it.q || it.author)}</b></td><td>${U.esc(it.slug || it.seo || it.role || "")}</td><td>${U.badge(it.status)}</td><td>${U.esc(it.updatedAt || "—")}</td>
        <td><button class="btn btn-ghost btn-sm" data-cms="edit:${contentTab}:${it.id}">Modifier</button>
            <button class="btn btn-ghost btn-sm" data-cms="prev:${contentTab}:${it.id}">Prévisualiser</button>
            <button class="btn btn-ghost btn-sm" data-cms="toggle:${contentTab}:${it.id}">${it.status === "publie" || it.status === "publiee" ? "Dépublier" : "Publier"}</button>
            <button class="btn btn-ghost btn-sm" data-cms="arch:${contentTab}:${it.id}">Archiver</button></td></tr>`;
    }).join("");
    return `
      <div class="page-head"><div><h1>Contenu</h1><p>CMS du site public talendus.ca</p></div>
        <div class="actions"><button class="btn btn-orange" data-cms="new:${contentTab}">Créer</button></div></div>
      <div class="tabs">${Object.keys(labels).map(function (k) { return '<button class="tab' + (contentTab === k ? " is-on" : "") + '" data-ctab="' + k + '">' + labels[k] + "</button>"; }).join("")}</div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Titre</th><th>Slug / SEO</th><th>Statut</th><th>MAJ</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
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
        ${["u-marc","u-camille","u-sophie"].map(function (id) {
          var n = st.candidates.filter(function (c) { return c.recruiterId === id && c.status === "place"; }).length;
          var recu = st.missions.filter(function (m) { return m.recruiterId === id; }).reduce(function (s, m) {
            return s + st.invoices.filter(function (i) { return i.missionId === m.id && i.status === "payee"; }).reduce(function (a, i) { return a + i.amount; }, 0);
          }, 0);
          return "<tr><td>" + TLStore.name(id) + "</td><td>" + n + "</td><td>" + U.money(recu) + "</td></tr>";
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
    if (me.role !== "admin") return U.empty("Accès restreint", "Les paramètres globaux sont réservés aux administrateurs.");
    return `
      <div class="page-head"><div><h1>Paramètres</h1><p>Rôles, équipe et données de démonstration</p></div></div>
      <div class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Utilisateur</th><th>Courriel</th><th>Rôle</th><th>Modules</th></tr></thead><tbody>
      ${S().users.map(function (u) {
        return "<tr><td>" + U.esc(u.firstName + " " + u.lastName) + "</td><td>" + u.email + "</td><td>" + roleLabel(u.role) + "</td><td>" + (TLStore.PERMS[u.role] || []).join(", ") + "</td></tr>";
      }).join("")}
      </tbody></table></div></div>
      <p style="margin-top:16px"><button class="btn btn-danger" id="reset-demo">Réinitialiser les données démo</button></p>
      <p style="color:var(--steel)">Architecture prête pour authentification, API, stockage CV et paiements réels.</p>`;
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
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Entreprise", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0].id }, "select") + U.field("Ville", "city") + U.field("Salaire", "salary") + U.field("Description", "description", "", "textarea", "full") + "</form>";
    } else if (type === "mission") {
      body = '<form id="cf" class="form-grid">' + U.field("Titre", "title") + U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0].id }, "select") + U.field("Offre", "jobId", { options: S().jobs.map(function (j) { return { v: j.id, l: j.title }; }), selected: S().jobs[0].id }, "select") + U.field("Nombre de postes", "seats", "1", "number") + "</form>";
    } else {
      body = '<form id="cf" class="form-grid">' + U.field("Client", "clientId", { options: S().clients.map(function (c) { return { v: c.id, l: c.name }; }), selected: S().clients[0].id }, "select") + U.field("Mission", "missionId", { options: S().missions.map(function (m) { return { v: m.id, l: m.title }; }), selected: S().missions[0].id }, "select") + U.field("Montant", "amount", "5000", "number") + "</form>";
    }

    U.modal({
      title: "Créer",
      body: body,
      footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
      onMount: function (box, close) {
        box.querySelector("#save").onclick = function () {
          var d = U.formData(box.querySelector("#cf"));
          TLStore.update(function (st) {
            if (type === "candidate") {
              st.candidates.unshift({ id: TLStore.nid("c"), firstName: d.firstName, lastName: d.lastName, email: d.email, phone: d.phone, city: d.city, title: d.title, sector: d.sector, experience: 0, level: "Junior", availability: "Immédiat", status: d.status || "nouveau", languages: ["Français"], recruiterId: me.id, createdAt: "2026-08-16", lastActivity: "2026-08-16", skills: [], salaryMin: 20, salaryMax: 24, shift: "Jour", education: [], experiences: [], bio: "", jobId: "", clientId: "" });
              st.activities.unshift({ id: TLStore.nid("a"), text: "Nouveau candidat inscrit — " + d.firstName + " " + d.lastName, at: "2026-08-16 12:00" });
            } else if (type === "client") {
              st.clients.unshift({ id: TLStore.nid("cl"), name: d.name, sector: d.sector, city: d.city, contact: d.contact, email: d.email, phone: d.phone, status: "Prospect", recruiterId: me.id, employees: 0, website: "", since: "2026-08-16" });
            } else if (type === "job") {
              st.jobs.unshift({ id: TLStore.nid("j"), title: d.title, clientId: d.clientId, city: d.city, sector: "Production", type: "Permanent", salary: d.salary, shift: "Quart de jour", status: "brouillon", publishedAt: "", expiresAt: "2026-10-01", applications: 0, experience: "—", skills: "", benefits: "", description: d.description, responsibilities: "", qualifications: "" });
            } else if (type === "mission") {
              st.missions.unshift({ id: TLStore.nid("m"), clientId: d.clientId, jobId: d.jobId, title: d.title, seats: Number(d.seats) || 1, recruiterId: me.id, start: "2026-08-16", due: "2026-09-30", status: "en-cours", value: 40000, commission: 6400, progress: 5, stageMap: {} });
            } else {
              st.invoices.unshift({ id: "F-2026-" + Math.floor(100 + Math.random() * 80), clientId: d.clientId, missionId: d.missionId, amount: Number(d.amount) || 0, date: "2026-08-16", due: "2026-09-15", status: "brouillon" });
            }
          });
          close();
          U.toast("Enregistré.", "ok");
          render();
        };
      }
    });
  }

  function deny() { U.toast("Votre rôle n’autorise pas cette action.", "err"); }

  function bindKanban() {
    var board = $(".kanban");
    if (!board) return;
    var mid = board.getAttribute("data-mission");
    var dragId = null;
    board.querySelectorAll(".kanban-card").forEach(function (card) {
      card.ondragstart = function () { dragId = card.getAttribute("data-cid"); };
    });
    board.querySelectorAll(".kanban-col").forEach(function (col) {
      col.ondragover = function (e) { e.preventDefault(); col.classList.add("drag-over"); };
      col.ondragleave = function () { col.classList.remove("drag-over"); };
      col.ondrop = function (e) {
        e.preventDefault();
        col.classList.remove("drag-over");
        if (!dragId) return;
        var stage = col.getAttribute("data-stage");
        TLStore.update(function (st) {
          var m = st.missions.find(function (x) { return x.id === mid; });
          if (m) m.stageMap[dragId] = stage;
          var c = st.candidates.find(function (x) { return x.id === dragId; });
          var map = { nouveaux: "nouveau", preselection: "a-contacter", "entretien-talendus": "entretien", presentation: "presente", "entretien-client": "entretien-client", offre: "offre", placement: "place" };
          if (c && map[stage]) c.status = map[stage];
        });
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
        TLStore.update(function (st) {
          st.candidates.forEach(function (c) { if (selected.has(c.id)) c.status = stt; });
        });
        selected.clear();
        U.toast("Statuts mis à jour.", "ok");
        render();
      }
      var note = t.closest("[data-note]");
      if (note) {
        U.modal({
          title: "Note interne",
          body: '<form id="nf">' + U.field("Note privée", "text", "", "textarea", "full") + "</form>",
          footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Ajouter</button>',
          onMount: function (box, close) {
            box.querySelector("#save").onclick = function () {
              var text = box.querySelector("[name=text]").value;
              TLStore.update(function (st) {
                st.notes.unshift({ id: TLStore.nid("n"), entity: "candidate", entityId: note.getAttribute("data-note"), authorId: TLStore.me().id, text: text, at: "2026-08-16 12:10" });
              });
              close(); U.toast("Note enregistrée.", "ok"); render();
            };
          }
        });
      }
      var jobAct = t.closest("[data-job-act]");
      if (jobAct) {
        var parts = jobAct.getAttribute("data-job-act").split(":");
        var act = parts[0], jid = parts[1];
        if (act === "dup") {
          TLStore.update(function (st) {
            var j = st.jobs.find(function (x) { return x.id === jid; });
            var copy = JSON.parse(JSON.stringify(j));
            copy.id = TLStore.nid("j"); copy.title = j.title + " (copie)"; copy.status = "brouillon"; copy.applications = 0;
            st.jobs.unshift(copy);
          });
          U.toast("Offre dupliquée.", "ok"); render();
        } else if (act === "edit") {
          var j = TLStore.job(jid);
          U.modal({
            title: "Modifier l’offre",
            body: '<form id="jf" class="form-grid">' + U.field("Titre", "title", j.title) + U.field("Salaire", "salary", j.salary) + U.field("Description", "description", j.description, "textarea", "full") + "</form>",
            footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="save">Enregistrer</button>',
            onMount: function (box, close) {
              box.querySelector("#save").onclick = function () {
                var d = U.formData(box.querySelector("#jf"));
                TLStore.update(function (st) {
                  var x = st.jobs.find(function (z) { return z.id === jid; });
                  Object.assign(x, d);
                });
                close(); U.toast("Offre mise à jour.", "ok"); render();
              };
            }
          });
        } else {
          U.confirm("Changer le statut de l’offre ?").then(function (ok) {
            if (!ok) return;
            TLStore.update(function (st) {
              var x = st.jobs.find(function (z) { return z.id === jid; });
              if (x) {
                x.status = act;
                if (act === "publiee") x.publishedAt = "2026-08-16";
              }
            });
            U.toast("Statut mis à jour.", "ok"); render();
          });
        }
      }
      var cms = t.closest("[data-cms]");
      if (cms) {
        var p = cms.getAttribute("data-cms").split(":");
        var action = p[0], tab = p[1], cid = p[2];
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
      var addInt = t.closest("[data-add-int]");
      if (addInt) {
        TLStore.update(function (st) {
          st.interviews.push({ id: TLStore.nid("i"), candidateId: addInt.getAttribute("data-add-int"), clientId: "", type: "Talendus", at: "2026-08-20 10:00", location: "Visio", recruiterId: TLStore.me().id });
        });
        U.toast("Entretien planifié.", "ok"); render();
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
        TLStore.update(function (st) { st.candidates.find(function (c) { return c.id === id; }).status = t.value; });
        U.toast("Statut candidat mis à jour.", "ok");
        render();
      }
      if (t.id === "an-rec") { analyticsRecruiter = t.value; render(); }
      if (t.id === "an-sec") { analyticsSector = t.value; render(); }
    };
    var nf = document.getElementById("note-form");
    if (nf) nf.onsubmit = function (e) {
      e.preventDefault();
      var id = route().id;
      TLStore.update(function (st) {
        st.notes.unshift({ id: TLStore.nid("n"), entity: "candidate", entityId: id, authorId: TLStore.me().id, text: U.formData(nf).text, at: "2026-08-16 12:20" });
      });
      U.toast("Note interne enregistrée.", "ok");
      render();
    };
    var ma = document.getElementById("mark-all");
    if (ma) ma.onclick = function () {
      TLStore.update(function (st) { st.notifications.forEach(function (n) { n.read = true; }); });
      render();
    };
    var rst = document.getElementById("reset-demo");
    if (rst) rst.onclick = function () {
      U.confirm("Réinitialiser toutes les données de démonstration ?").then(function (ok) {
        if (!ok) return;
        TLStore.reset();
        U.toast("Données réinitialisées.", "ok");
        render();
      });
    };
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
    }, 180);
  }

  window.addEventListener("hashchange", function () {
    page = 1; selected = new Set(); detailTab = "profil"; filters = {};
    render();
  });
  render();
})();
