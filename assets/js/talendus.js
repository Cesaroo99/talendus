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
    if (file === "employeurs.html" || file === "secteurs.html" || file.indexOf("secteur-") === 0) return "employeurs";
    if (file === "candidats.html" || file === "emplois.html" || file.indexOf("emploi-") === 0) return "candidats";
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

    document.querySelectorAll(".tl-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var box = form.querySelector(".tl-success");
        if (box) {
          box.style.display = "block";
          box.textContent = "Merci. Réponse moyenne sous 30 minutes durant les heures d’ouverture. Un conseiller vous rejoint.";
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
      var q = ((search && search.value) || "").toLowerCase();
      var c = (cat && cat.value) || "";
      var v = (city && city.value) || "";
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
