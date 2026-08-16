(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function fileName() {
    var file = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    return file || "index.html";
  }

  function navKey(file) {
    if (!file || file === "index.html") return "home";
    if (
      file === "employeurs.html" ||
      file === "entreprises.html" ||
      file === "employers.html" ||
      file === "secteurs.html" ||
      file === "sectors.html" ||
      file.indexOf("secteur-") === 0 ||
      file.indexOf("sector-") === 0
    ) return "employeurs";
    if (
      file === "candidats.html" ||
      file === "candidates.html" ||
      file === "emplois.html" ||
      file === "jobs.html" ||
      file.indexOf("emploi-") === 0 ||
      file.indexOf("job-") === 0
    ) return "candidats";
    if (file === "services.html" || file === "service.html") return "services";
    if (file === "a-propos.html" || file === "about.html") return "about";
    if (file === "blog.html" || file.indexOf("article-") === 0 || file === "blog-single.html") return "blog";
    if (file === "contact.html") return "contact";
    return "";
  }

  function markActiveNav() {
    var key = navKey(fileName());
    document.querySelectorAll("[data-nav]").forEach(function (el) {
      el.classList.toggle("is-active", key && el.getAttribute("data-nav") === key);
    });
  }

  ready(function () {
    markActiveNav();
    setTimeout(markActiveNav, 250);

    if (window.jQuery) {
      var $ = window.jQuery;
      $(window).off("load");
      $(window).on("load.talendus", function () {
        var minMs = 900;
        var start = window.performance && performance.now ? performance.now() : Date.now();
        function hide() {
          var elapsed = (window.performance && performance.now ? performance.now() : Date.now()) - start;
          var wait = Math.max(0, minMs - elapsed);
          setTimeout(function () {
            $(".preloader").addClass("is-done");
            setTimeout(function () {
              $(".preloader").remove();
            }, 480);
          }, wait);
        }
        hide();
      });
      if (document.readyState === "complete") {
        $(window).trigger("load.talendus");
      }

      var $slider = $(".hero-main-slider");
      if ($slider.length) {
        if ($slider.hasClass("slick-initialized")) {
          $slider.slick("unslick");
        }
        $slider.slick({
          autoplay: true,
          autoplaySpeed: 6500,
          speed: 700,
          slidesToShow: 1,
          slidesToScroll: 1,
          pauseOnHover: true,
          dots: false,
          arrows: true,
          fade: true,
          cssEase: "ease-in-out",
          adaptiveHeight: false,
          draggable: true,
          prevArrow: $(".next-arrow-hero"),
          nextArrow: $(".prev-arrow-hero")
        });
      }
    }

    var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;

    document.querySelectorAll(".tl-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var box = form.querySelector(".tl-success");
        if (box) {
          box.style.display = "block";
          box.textContent = isEn
            ? "Thank you. Average response under 30 minutes during business hours. A consultant will follow up."
            : "Merci. Réponse moyenne sous 30 minutes durant les heures d’ouverture. Un conseiller vous rejoint.";
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
      result.textContent = new Intl.NumberFormat(isEn ? "en-CA" : "fr-CA", {
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
    var type = document.getElementById("job-type");
    var shift = document.getElementById("job-shift");
    var sal = document.getElementById("job-sal");
    var empty = document.getElementById("job-empty");

    function salaryFloor(raw) {
      var compact = (raw || "").replace(/\u00a0/g, " ").replace(/\s/g, "");
      var nums = compact.match(/\d+/g);
      if (!nums) return 0;
      var n = parseInt(nums[0], 10);
      if (n >= 1000) return n;
      return n * 2080;
    }

    function filterJobs() {
      var q = ((search && search.value) || "").toLowerCase();
      var c = (cat && cat.value) || "";
      var v = (city && city.value) || "";
      var ty = (type && type.value) || "";
      var sh = (shift && shift.value) || "";
      var minSal = sal && sal.value ? Number(sal.value) : 0;
      var shown = 0;
      document.querySelectorAll("[data-job]").forEach(function (card) {
        var hay = (card.getAttribute("data-job") || "").toLowerCase();
        var ok = (!q || hay.indexOf(q.toLowerCase()) !== -1)
          && (!c || hay.indexOf(c.toLowerCase()) !== -1)
          && (!v || (card.getAttribute("data-city") || "").toLowerCase() === v.toLowerCase() || hay.indexOf(v.toLowerCase()) !== -1)
          && (!ty || (card.getAttribute("data-type") || "").toLowerCase() === ty.toLowerCase() || hay.indexOf(ty.toLowerCase()) !== -1)
          && (!sh || (card.getAttribute("data-shift") || "").indexOf(sh) !== -1 || hay.indexOf(sh.toLowerCase()) !== -1);
        if (ok && minSal) {
          var floor = salaryFloor(card.getAttribute("data-salary") || hay);
          if (minSal < 1000) {
            ok = floor >= minSal * 2080;
          } else {
            ok = floor >= minSal;
          }
        }
        card.style.display = ok ? "" : "none";
        if (ok) shown += 1;
      });
      if (empty) empty.hidden = shown !== 0;
    }
    [search, cat, city, type, shift, sal].forEach(function (el) {
      if (el) el.addEventListener("input", filterJobs);
      if (el) el.addEventListener("change", filterJobs);
    });
  });
})();
