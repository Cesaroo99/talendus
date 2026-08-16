(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    document.querySelectorAll(".tl-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var box = form.querySelector(".tl-success");
        if (box) {
          box.style.display = "block";
          box.textContent = "Merci. Un conseiller Talendus vous répondra sous 24 heures ouvrables.";
        }
        form.reset();
      });
    });

    var salary = document.getElementById("tl-salary");
    var months = document.getElementById("tl-months");
    var result = document.getElementById("tl-cost");
    function calc() {
      if (!salary || !months || !result) return;
      var s = Number(salary.value) || 0;
      var m = Number(months.value) || 0;
      var cost = s * (m / 12) + s * 0.35 + 18000;
      result.textContent = new Intl.NumberFormat("fr-CA", {
        style: "currency",
        currency: "CAD",
        maximumFractionDigits: 0
      }).format(cost);
    }
    if (salary && months) {
      salary.addEventListener("input", calc);
      months.addEventListener("input", calc);
      calc();
    }

    var search = document.getElementById("job-search");
    var cat = document.getElementById("job-cat");
    var city = document.getElementById("job-city");
    function filterJobs() {
      var q = (search && search.value || "").toLowerCase();
      var c = cat && cat.value || "";
      var v = city && city.value || "";
      document.querySelectorAll("[data-job]").forEach(function (card) {
        var hay = card.getAttribute("data-job").toLowerCase();
        var ok = (!q || hay.indexOf(q) !== -1) && (!c || hay.indexOf(c) !== -1) && (!v || hay.indexOf(v) !== -1);
        card.style.display = ok ? "" : "none";
      });
    }
    [search, cat, city].forEach(function (el) {
      if (el) el.addEventListener("input", filterJobs);
      if (el) el.addEventListener("change", filterJobs);
    });
  });
})();
