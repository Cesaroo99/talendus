/* Talendus Admin — primitives UI */
(function (global) {
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const STATUS = {
    nouveau: ["Nouveau", "info"],
    "a-contacter": ["À contacter", "warn"],
    qualifie: ["Qualifié", "ok"],
    entretien: ["Entretien", "info"],
    presente: ["Présenté au client", "orange"],
    "entretien-client": ["Entretien client", "orange"],
    offre: ["Offre reçue", "ok"],
    place: ["Placé", "ok"],
    refuse: ["Refusé", "danger"],
    inactif: ["Inactif", "muted"],
    publiee: ["Publiée", "ok"],
    brouillon: ["Brouillon", "muted"],
    suspendue: ["Suspendue", "warn"],
    expiree: ["Expirée", "danger"],
    archivee: ["Archivée", "muted"],
    publie: ["Publié", "ok"],
    archive: ["Archivé", "muted"],
    "en-cours": ["En cours", "info"],
    pourvue: ["Pourvue", "ok"],
    "en-pause": ["En pause", "warn"],
    annulee: ["Annulée", "muted"],
    payee: ["Payée", "ok"],
    envoyee: ["Envoyée", "info"],
    "en-attente": ["En attente", "warn"],
    "en-retard": ["En retard", "danger"],
    Actif: ["Actif", "ok"],
    Prospect: ["Prospect", "warn"],
    "Expire bientôt": ["Expire bientôt", "warn"]
  };

  const STAGES = [
    ["nouveaux", "Nouveaux"],
    ["preselection", "Présélection"],
    ["entretien-talendus", "Entretien Talendus"],
    ["presentation", "Présentation client"],
    ["entretien-client", "Entretien client"],
    ["offre", "Offre"],
    ["placement", "Placement"]
  ];

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function money(n) {
    return new Intl.NumberFormat("fr-CA", { style: "currency", currency: "CAD", maximumFractionDigits: 0 }).format(Number(n) || 0);
  }

  function dateFr(iso) {
    if (!iso) return "—";
    var p = String(iso).slice(0, 10).split("-");
    if (p.length < 3) return iso;
    return p[2] + "/" + p[1] + "/" + p[0];
  }

  function badge(key) {
    var meta = STATUS[key] || [key, "muted"];
    return '<span class="badge ' + meta[1] + '">' + esc(meta[0]) + "</span>";
  }

  function avatar(person, size) {
    var initials = person.initials || ((person.firstName || "?")[0] + (person.lastName || "?")[0]);
    return '<div class="avatar ' + (size || "") + '">' + esc(initials) + "</div>";
  }

  function toast(msg, type) {
    var root = document.getElementById("toast-root");
    var el = document.createElement("div");
    el.className = "toast " + (type || "");
    el.textContent = msg;
    root.appendChild(el);
    setTimeout(function () { el.remove(); }, 3200);
  }

  function modal(opts) {
    var root = document.getElementById("modal-root");
    root.innerHTML = '<div class="modal-back"><div class="modal" role="dialog" aria-modal="true"><header><h3 style="margin:0">' + esc(opts.title || "") + '</h3><button class="icon-btn" data-close>×</button></header><div class="body">' + (opts.body || "") + '</div><footer>' + (opts.footer || '<button class="btn btn-ghost" data-close>Fermer</button>') + "</footer></div></div>";
    var back = root.firstElementChild;
    function close() { root.innerHTML = ""; if (opts.onClose) opts.onClose(); }
    back.addEventListener("click", function (e) {
      if (e.target === back || e.target.closest("[data-close]")) close();
    });
    if (opts.onMount) opts.onMount(back.querySelector(".modal"), close);
    return close;
  }

  function confirm(message) {
    return new Promise(function (resolve) {
      var done = false;
      function finish(v) { if (done) return; done = true; resolve(v); }
      modal({
        title: "Confirmation",
        body: "<p>" + esc(message) + "</p>",
        footer: '<button class="btn btn-ghost" data-close>Annuler</button><button class="btn btn-orange" id="ok">Confirmer</button>',
        onMount: function (box, close) {
          box.querySelector("#ok").onclick = function () { finish(true); close(); };
        },
        onClose: function () { finish(false); }
      });
    });
  }

  function csv(filename, rows) {
    var text = rows.map(function (r) {
      return r.map(function (c) {
        var v = String(c == null ? "" : c).replace(/"/g, '""');
        return /[",;\n]/.test(v) ? '"' + v + '"' : v;
      }).join(";");
    }).join("\n");
    var blob = new Blob(["\ufeff" + text], { type: "text/csv;charset=utf-8;" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
  }

  function paginate(list, page, per) {
    per = per || 8;
    var pages = Math.max(1, Math.ceil(list.length / per));
    page = Math.min(Math.max(1, page), pages);
    return { items: list.slice((page - 1) * per, page * per), page: page, pages: pages, total: list.length, per: per };
  }

  function sortBy(list, key, dir) {
    var copy = list.slice();
    copy.sort(function (a, b) {
      var va = a[key], vb = b[key];
      if (va == null) va = "";
      if (vb == null) vb = "";
      if (typeof va === "number" && typeof vb === "number") return dir === "desc" ? vb - va : va - vb;
      return dir === "desc" ? String(vb).localeCompare(String(va), "fr") : String(va).localeCompare(String(vb), "fr");
    });
    return copy;
  }

  function field(label, name, value, type, extra) {
    extra = extra || "";
    if (type === "textarea") return '<div class="field ' + extra + '"><label>' + esc(label) + '</label><textarea name="' + name + '">' + esc(value || "") + "</textarea></div>";
    if (type === "select") {
      var opts = (value && value.options || []).map(function (o) {
        var v = typeof o === "string" ? o : o.v;
        var l = typeof o === "string" ? o : o.l;
        var sel = (value.selected === v) ? " selected" : "";
        return "<option value=\"" + esc(v) + "\"" + sel + ">" + esc(l) + "</option>";
      }).join("");
      return '<div class="field ' + extra + '"><label>' + esc(label) + '</label><select name="' + name + '">' + opts + "</select></div>";
    }
    return '<div class="field ' + extra + '"><label>' + esc(label) + '</label><input name="' + name + '" type="' + (type || "text") + '" value="' + esc(value || "") + '"></div>';
  }

  function formData(form) {
    var o = {};
    Array.from(form.elements).forEach(function (el) {
      if (!el.name) return;
      o[el.name] = el.value;
    });
    return o;
  }

  function lineChart(data, color) {
    var w = 560, h = 200, p = 24;
    var max = Math.max.apply(null, data.concat([1]));
    var pts = data.map(function (v, i) {
      var x = p + (i * (w - p * 2)) / (data.length - 1);
      var y = h - p - (v / max) * (h - p * 2);
      return x + "," + y;
    });
    var area = pts[0].split(",")[0] + "," + (h - p) + " " + pts.join(" ") + " " + pts[pts.length - 1].split(",")[0] + "," + (h - p);
    return '<svg viewBox="0 0 ' + w + " " + h + '" class="chart"><polyline fill="none" stroke="' + color + '" stroke-width="3" points="' + pts.join(" ") + '"/><polygon fill="' + color + '" opacity=".12" points="' + area + '"/></svg>';
  }

  function barChart(labels, data, color) {
    var w = 560, h = 200, p = 28;
    var max = Math.max.apply(null, data.concat([1]));
    var bw = (w - p * 2) / data.length * 0.62;
    var gap = (w - p * 2) / data.length;
    var bars = data.map(function (v, i) {
      var bh = (v / max) * (h - p * 2);
      var x = p + i * gap + (gap - bw) / 2;
      var y = h - p - bh;
      return '<rect x="' + x + '" y="' + y + '" width="' + bw + '" height="' + bh + '" rx="4" fill="' + color + '"/><text x="' + (x + bw / 2) + '" y="' + (h - 8) + '" text-anchor="middle" font-size="10" fill="#5c6770">' + esc(labels[i]) + "</text>";
    }).join("");
    return '<svg viewBox="0 0 ' + w + " " + h + '">' + bars + "</svg>";
  }

  function donut(items) {
    var total = items.reduce(function (s, i) { return s + i.v; }, 0) || 1;
    var r = 54, c = 2 * Math.PI * r, acc = 0;
    var rings = items.map(function (it) {
      var len = (it.v / total) * c;
      var dash = '<circle cx="80" cy="80" r="' + r + '" fill="none" stroke="' + it.c + '" stroke-width="16" stroke-dasharray="' + len + " " + (c - len) + '" stroke-dashoffset="' + (-acc) + '" transform="rotate(-90 80 80)"/>';
      acc += len;
      return dash;
    }).join("");
    var legend = items.map(function (it) {
      return '<span><i style="background:' + it.c + '"></i>' + esc(it.l) + " (" + it.v + ")</span>";
    }).join("");
    return '<div><svg viewBox="0 0 160 160" width="160" height="160">' + rings + '</svg><div class="legend">' + legend + "</div></div>";
  }

  function empty(title, text, action) {
    return '<div class="empty card card-pad"><i class="fa-regular fa-folder-open" style="font-size:28px;color:var(--orange)"></i><h3>' + esc(title) + "</h3><p>" + esc(text) + "</p>" + (action || "") + "</div>";
  }

  function skeleton() {
    return '<div class="grid grid-4">' + [1,2,3,4].map(function () { return '<div class="card kpi"><div class="skel"></div><div class="skel" style="height:28px;margin-top:12px;width:50%"></div></div>'; }).join("") + "</div>";
  }

  global.TLUI = {
    $, $$, esc, money, dateFr, badge, avatar, toast, modal, confirm, csv,
    paginate, sortBy, field, formData, lineChart, barChart, donut, empty, skeleton,
    STATUS, STAGES
  };
})(window);
