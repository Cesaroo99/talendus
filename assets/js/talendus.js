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
    var path = (window.location.pathname || "").toLowerCase();
    if (path.indexOf("/candidate") !== -1 || file === "espace.html" || file === "account.html") return "candidats";
    if (path.indexOf("/employer") !== -1 || file === "espace-employeur.html" || file === "account-employer.html") return "employeurs";
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
      file === "comment-ca-fonctionne.html" ||
      file === "how-it-works.html"
    ) return "candidats";
    if (file === "emplois.html" || file === "jobs.html" || file.indexOf("emploi-") === 0 || file.indexOf("job-") === 0) return "jobs";
    if (file === "services.html" || file === "service.html" || file === "publier-une-offre.html" || file === "post-a-job.html" || file === "solutions-rh.html" || file === "hr-solutions.html" || file.indexOf("recrutement-") === 0 || file.indexOf("industrial-recruiting") === 0 || file.indexOf("manufacturing-recruiting") === 0 || file.indexOf("technical-recruiting") === 0 || file.indexOf("permanent-recruiting") === 0 || file.indexOf("temporary-recruiting") === 0 || file.indexOf("executive-search") === 0 || file.indexOf("leadership-recruiting") === 0) return "employeurs";
    if (file === "a-propos.html" || file === "about.html") return "about";
    if (file === "blog.html" || file.indexOf("article-") === 0 || file === "blog-single.html" || (window.location.pathname || "").indexOf("/blog/") === 0) return "blog";
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
    var apiUser = window.TalendusAPI && window.TalendusAPI.currentUser && window.TalendusAPI.currentUser();
    if (apiUser && apiUser.first_name) {
      var isEnNav = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
      var root = isEnNav ? "/en/" : "/";
      var href = root + (isEnNav ? "account.html" : "espace.html") + "#/dashboard";
      if (apiUser.role === "EMPLOYER") href = root + (isEnNav ? "account-employer.html" : "espace-employeur.html") + "#/dashboard";
      else if (["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(apiUser.role) !== -1) {
        href = "/admin/";
      }
      document.querySelectorAll("[data-account-link]").forEach(function (el) {
        el.textContent = apiUser.first_name;
        el.setAttribute("href", href);
        el.removeAttribute("data-auth-open");
      });
      document.querySelectorAll("[data-auth-open='register']").forEach(function (el) {
        el.hidden = true;
      });
    }

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

    function escapeHtml(value) {
      return String(value == null ? "" : value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function formValue(form, names) {
      for (var i = 0; i < names.length; i++) {
        var el = form.querySelector("[name='" + names[i] + "']") || form.querySelector("#" + names[i]);
        if (el && String(el.value || "").trim()) return String(el.value).trim();
      }
      return "";
    }

    function jobSlugFromPage() {
      var file = fileName();
      if (file.indexOf("emploi-") === 0) return file.slice("emploi-".length).replace(/\.html$/, "");
      if (file.indexOf("job-") === 0) return file.slice("job-".length).replace(/\.html$/, "");
      return "";
    }

    var pageSlug = jobSlugFromPage();
    if (pageSlug && window.TalendusAPI) {
      window.TalendusAPI.request("/jobs/" + encodeURIComponent(pageSlug)).then(function (payload) {
        var job = payload && payload.data;
        var url = job && job.share && (isEn ? job.share.linkedin_en : job.share.linkedin);
        if (!url) return;
        var host = document.querySelector(".tl-page-hero .container") || document.querySelector(".tl-section .container");
        if (!host || host.querySelector(".tl-share-linkedin")) return;
        var a = document.createElement("a");
        a.className = "tl-share-linkedin";
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = isEn ? "Share this role on LinkedIn" : "Partager cette offre sur LinkedIn";
        host.appendChild(a);
      }).catch(function () {});
    }

    function splitName(raw) {
      var parts = String(raw || "").trim().split(/\s+/);
      return { first: parts[0] || "Candidat", last: parts.slice(1).join(" ") };
    }

    function showFormMessage(form, text, isError) {
      var box = form.querySelector(".tl-success");
      if (!box) return;
      box.style.display = "block";
      box.textContent = text;
      box.style.color = isError ? "#8a1f11" : "";
    }

    document.querySelectorAll(".tl-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var kind = form.getAttribute("data-form") || (form.closest("#postuler") ? "apply" : "contact");
        var fallback = isEn
          ? "Thank you. Average response under 30 minutes during business hours. A consultant will follow up."
          : "Merci. Réponse moyenne sous 30 minutes durant les heures d’ouverture. Un conseiller vous rejoint.";
        var api = window.TalendusAPI;
        if (!api) {
          showFormMessage(form, fallback, false);
          form.reset();
          return;
        }
        var btn = form.querySelector("button[type=submit]");
        if (btn) btn.disabled = true;
        var done = function () { if (btn) btn.disabled = false; };
        if (kind === "apply") {
          var person = splitName(formValue(form, ["nom", "name"]));
          var slug = form.getAttribute("data-job-slug") || jobSlugFromPage();
          var user = api.currentUser && api.currentUser();
          var send = (user && user.role === "CANDIDATE")
            ? api.apply({ job_slug: slug, cover_note: formValue(form, ["cv", "resume"]) || null })
            : api.applyPublic({
                job_slug: slug,
                first_name: person.first,
                last_name: person.last,
                email: formValue(form, ["courriel", "email"]),
                phone: formValue(form, ["tel", "telephone", "phone"]) || null,
                cv_url: formValue(form, ["cv", "resume"]) || null
              });
          send.then(function () {
            showFormMessage(form, fallback, false);
            form.reset();
            if (window.TalendusTrack) window.TalendusTrack.apply({ content_name: slug || "job" });
            if (user && user.role === "CANDIDATE") {
              window.location.href = (isEn ? "/en/account.html" : "/espace.html") + "#/apps";
            } else {
              form.dispatchEvent(new CustomEvent("talendus:applied", { bubbles: true }));
            }
          }).catch(function (err) {
            showFormMessage(form, (err && err.message) || fallback, true);
          }).then(done);
          return;
        }
        api.contact({
          name: formValue(form, ["nom", "name"]) || "Visiteur",
          email: formValue(form, ["courriel", "email"]) || "info@talendus.ca",
          phone: formValue(form, ["tel", "telephone", "phone"]) || null,
          company: formValue(form, ["entreprise", "company"]) || null,
          subject: formValue(form, ["objet", "profil", "metier", "subject"]) || null,
          message: formValue(form, ["message", "msg"]) || formValue(form, ["cv", "region"]) || "Message site Talendus"
        }).then(function () {
          showFormMessage(form, fallback, false);
          form.reset();
          if (window.TalendusTrack) {
            if (kind === "contact" || (form.getAttribute("data-form") === "contact")) window.TalendusTrack.contact({ content_name: "contact" });
            else window.TalendusTrack.lead({ content_name: kind || "form" });
          }
        }).catch(function () {
          showFormMessage(form, fallback, false);
          form.reset();
        }).then(done);
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
    var searchTimer = null;
    function filterJobsAndTrack() {
      filterJobs();
      var q = ((search && search.value) || "").trim();
      if (!q || !window.TalendusTrack) return;
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function () {
        window.TalendusTrack.search({ search_term: q, content_category: "jobs" });
      }, 600);
    }
    [search, cat, city, type, shift, sal].forEach(function (el) {
      if (el) el.addEventListener("input", filterJobsAndTrack);
      if (el) el.addEventListener("change", filterJobsAndTrack);
    });

    var jobList = document.getElementById("job-list");
    if (jobList && window.TalendusAPI) {
      window.TalendusAPI.jobs({ page_size: 24, sort: "relevance" }).then(function (payload) {
        var items = (payload && payload.data) || [];
        if (!items.length) return;
        var prefix = isEn ? "/en/job-" : "/emploi-";
        jobList.innerHTML = items.map(function (job) {
          var href = prefix + job.slug + ".html";
          var salary = job.salary_display || "";
          var shiftVal = job.shift || "";
          var hay = [job.title, job.location, job.sector, job.contract_type, salary, shiftVal, job.skills].join(" ");
          var share = (job.share && job.share.linkedin)
            ? '<a class="tl-share-linkedin" href="' + escapeHtml(job.share.linkedin) + '" target="_blank" rel="noopener noreferrer">' + (isEn ? "Share on LinkedIn" : "Partager sur LinkedIn") + "</a>"
            : "";
          return '<article class="tl-job-card" data-job="' + escapeHtml(hay) + '" data-city="' + escapeHtml(job.location || "") + '" data-cat="' + escapeHtml((job.sector || "").toLowerCase()) + '" data-type="' + escapeHtml(job.contract_type || "") + '" data-shift="' + escapeHtml(shiftVal) + '" data-salary="' + escapeHtml(salary) + '"><div class="body"><span class="tl-chip orange">' + escapeHtml(job.contract_type || "") + '</span><span class="tl-chip">' + escapeHtml(job.location || "") + '</span><h3><a href="' + href + '">' + escapeHtml(job.title) + '</a></h3><p>' + escapeHtml([salary, shiftVal].filter(Boolean).join(" · ")) + "</p>" + share + '<p class="tl-job-card-actions"><a class="tl-split-cta" href="' + href + '" style="color:var(--tl-orange)">' + (isEn ? "View role →" : "Voir le poste →") + '</a> <button type="button" class="tl-text-btn" data-save-job="' + escapeHtml(job.id) + '">' + (isEn ? "Save" : "Sauvegarder") + "</button></p></div></article>";
        }).join("");
        filterJobs();
      }).catch(function () {});
    }

    var blogList = document.getElementById("blog-list");
    if (blogList && window.TalendusAPI) {
      window.TalendusAPI.request("/blog" + (isEn ? "?lang=en" : "?lang=fr")).then(function (payload) {
        var items = (payload && payload.data) || [];
        if (!items.length) return;
        items.forEach(function (post) {
          if (blogList.querySelector('[data-slug="' + post.slug + '"]')) return;
          var a = document.createElement("a");
          a.className = "tl-card";
          a.setAttribute("data-slug", post.slug);
          a.href = "/blog/" + encodeURIComponent(post.slug);
          var imgSrc = post.cover_image || "/assets/img/all-images/industry/usine-equipe.jpg";
          a.innerHTML = '<div class="tl-hero-media" style="height:180px"><img src="' + escapeHtml(imgSrc) + '" alt="' + escapeHtml(post.title) + '" loading="lazy" decoding="async"></div><div class="body"><span class="tl-chip">' + escapeHtml(post.category || "Blog") + "</span><h3>" + escapeHtml(post.title) + "</h3><p>" + escapeHtml(post.excerpt || "") + "</p></div>";
          blogList.appendChild(a);
        });
      }).catch(function () {});
    }

    var DESKTOP_NAV = 1200;
    var toggleBtns = document.querySelectorAll(".vl-offcanvas-toggle");

    function setMenuOpen(open) {
      document.body.classList.toggle("tl-menu-open", open);
      toggleBtns.forEach(function (btn) {
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }

    function closeMenu() {
      var canvas = document.querySelector(".vl-offcanvas");
      var overlay = document.querySelector(".vl-offcanvas-overlay");
      if (canvas) canvas.classList.remove("vl-offcanvas-open");
      if (overlay) overlay.classList.remove("vl-offcanvas-overlay-open");
      setMenuOpen(false);
    }

    toggleBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        setMenuOpen(true);
      });
    });
    document.querySelectorAll(".vl-offcanvas-close-toggle, .vl-offcanvas-overlay").forEach(function (el) {
      el.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= DESKTOP_NAV) closeMenu();
    });
    document.querySelectorAll(".vl-offcanvas-menu").forEach(function (menu) {
      menu.addEventListener("click", function (e) {
        var link = e.target.closest("a");
        if (!link) return;
        var item = link.parentElement;
        if (item && item.classList.contains("has-dropdown")) return;
        closeMenu();
      });
    });
  });
})();
