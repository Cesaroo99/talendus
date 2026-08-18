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
    if (file === "services.html" || file === "service.html" || file === "besoin-de-recrutement.html" || file === "hiring-need.html" || file === "publier-une-offre.html" || file === "post-a-job.html" || file === "solutions-rh.html" || file === "hr-solutions.html" || file.indexOf("recrutement-") === 0 || file.indexOf("industrial-recruiting") === 0 || file.indexOf("manufacturing-recruiting") === 0 || file.indexOf("technical-recruiting") === 0 || file.indexOf("permanent-recruiting") === 0 || file.indexOf("temporary-recruiting") === 0 || file.indexOf("executive-search") === 0 || file.indexOf("leadership-recruiting") === 0) return "employeurs";
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
        var host = document.querySelector(".tl-job-main") || document.querySelector(".tl-page-hero .container") || document.querySelector(".tl-section .container");
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

    function cvFileFromForm(form) {
      var fileInput = form.querySelector('input[type=file][name=cvfile]');
      return fileInput && fileInput.files && fileInput.files[0];
    }

    function validateCvFile(form, file) {
      var allowed = /\.(pdf|doc|docx|png|jpe?g|webp)$/i;
      if (file && !allowed.test(file.name)) {
        showFormMessage(form, isEn ? "Use a PDF, Word or image file (PNG, JPG)." : "Utilisez un fichier PDF, Word ou image (PNG, JPG).", true);
        return false;
      }
      if (file && file.size > 5 * 1024 * 1024) {
        showFormMessage(form, isEn ? "The file must be 5 MB or less." : "Le fichier doit faire 5 Mo ou moins.", true);
        return false;
      }
      return true;
    }

    document.querySelectorAll(".tl-form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var kind = form.getAttribute("data-form") || (form.closest("#postuler") ? "apply" : "contact");
        var hiringOk = isEn
          ? "Your hiring need has been sent to Talendus. Our team will review the information and contact you to understand the role and define the profile together. Your recruiting starts with Talendus."
          : "Votre besoin a bien été transmis à Talendus. Notre équipe va analyser les informations communiquées et vous contacter afin de mieux comprendre votre besoin et de définir avec vous le profil recherché. Votre recrutement commence avec Talendus.";
        var fallback = isEn
          ? "Thanks. On weekdays we usually reply within 30 minutes. A consultant will follow up."
          : "Merci. En semaine, on répond en général en moins de 30 minutes. Un conseiller vous rappelle.";
        var api = window.TalendusAPI;
        if (!api) {
          showFormMessage(form, kind === "hiring-need" ? hiringOk : fallback, false);
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
          var file = cvFileFromForm(form);
          var cover = formValue(form, ["message", "note"]) || null;
          if (!validateCvFile(form, file)) {
            done();
            return;
          }
          if (user && user.role && user.role !== "CANDIDATE") {
            showFormMessage(form, isEn ? "Use a candidate account to apply." : "Utilisez un compte candidat pour postuler.", true);
            done();
            return;
          }
          var send;
          if (user && user.role === "CANDIDATE") {
            send = Promise.resolve(null);
            if (file) {
              var up = new FormData();
              up.append("file", file);
              send = api.uploadResume(up).then(function (json) {
                return json && json.data && json.data.id;
              });
            }
            send = send.then(function (resumeId) {
              var body = { job_slug: slug, cover_note: cover };
              if (resumeId) body.resume_id = resumeId;
              return api.apply(body);
            });
          } else {
            var fd = new FormData();
            fd.append("job_slug", slug);
            fd.append("first_name", person.first);
            fd.append("last_name", person.last || "");
            fd.append("email", formValue(form, ["courriel", "email"]));
            var phone = formValue(form, ["tel", "telephone", "phone"]);
            if (phone) fd.append("phone", phone);
            if (cover) fd.append("cover_note", cover);
            if (file) fd.append("file", file);
            send = api.request("/applications/public", { method: "POST", body: fd });
          }
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
        if (kind === "talent-cv") {
          var person = splitName(formValue(form, ["nom", "name"]));
          var file = cvFileFromForm(form);
          var user = api.currentUser && api.currentUser();
          if (!validateCvFile(form, file)) {
            done();
            return;
          }
          if (user && user.role && user.role !== "CANDIDATE") {
            showFormMessage(form, isEn ? "Use a candidate account to submit a resume." : "Utilisez un compte candidat pour déposer un CV.", true);
            done();
            return;
          }
          var fd = new FormData();
          fd.append("first_name", person.first);
          fd.append("last_name", person.last || "");
          fd.append("email", formValue(form, ["courriel", "email"]));
          var phone = formValue(form, ["tel", "telephone", "phone"]);
          if (phone) fd.append("phone", phone);
          var title = formValue(form, ["metier", "title"]);
          if (title) fd.append("title", title);
          var city = formValue(form, ["region", "city"]);
          if (city) fd.append("city", city);
          var cvUrl = formValue(form, ["cv"]);
          if (cvUrl) fd.append("cv_url", cvUrl);
          var message = formValue(form, ["message", "msg"]);
          if (message) fd.append("message", message);
          var subject = formValue(form, ["objet", "subject", "profil"]);
          if (subject) fd.append("subject", subject);
          if (file) fd.append("file", file);
          api.request("/talent-profile", { method: "POST", body: fd }).then(function () {
            showFormMessage(form, fallback, false);
            form.reset();
            if (window.TalendusTrack) window.TalendusTrack.lead({ content_name: "talent-cv" });
          }).catch(function (err) {
            showFormMessage(form, (err && err.message) || fallback, true);
          }).then(done);
          return;
        }
        var user = api.currentUser && api.currentUser();
        var isHiring = kind === "hiring-need" || !!formValue(form, ["poste", "entreprise"]);
        if (isHiring && user && user.role === "EMPLOYER") {
          var seats = parseInt(formValue(form, ["volume", "seats"]) || "1", 10);
          api.request("/hiring-requests", {
            method: "POST",
            body: {
              title: formValue(form, ["poste", "title"]) || formValue(form, ["objet"]) || "Besoin de recrutement",
              seats: seats > 0 ? seats : 1,
              location: formValue(form, ["localisation", "location"]) || null,
              sector: formValue(form, ["secteur", "sector"]) || null,
              contract_type: formValue(form, ["contrat", "contract"]) || null,
              experience_level: formValue(form, ["experience"]) || null,
              skills: formValue(form, ["competences", "skills"]) || null,
              notes: formValue(form, ["message", "msg"]) || null,
              contact_name: formValue(form, ["nom", "name"]) || null,
              contact_role: formValue(form, ["fonction", "role"]) || null,
              contact_email: formValue(form, ["courriel", "email"]) || null,
              contact_phone: formValue(form, ["tel", "telephone", "phone"]) || null,
              company_size: formValue(form, ["taille", "size"]) || null
            }
          }).then(function () {
            showFormMessage(form, hiringOk, false);
            form.reset();
            if (window.TalendusTrack) window.TalendusTrack.lead({ content_name: "hiring-need" });
          }).catch(function (err) {
            showFormMessage(form, (err && err.message) || hiringOk, true);
          }).then(done);
          return;
        }
        api.contact({
          name: formValue(form, ["nom", "name"]) || "Visiteur",
          email: formValue(form, ["courriel", "email"]) || "info@talendus.ca",
          phone: formValue(form, ["tel", "telephone", "phone"]) || null,
          company: formValue(form, ["entreprise", "company"]) || null,
          subject: formValue(form, ["objet", "profil", "metier", "subject"]) || null,
          message: formValue(form, ["message", "msg"]) || formValue(form, ["cv", "region"]) || "Message site Talendus",
          title: formValue(form, ["poste", "title"]) || null,
          sector: formValue(form, ["secteur", "sector"]) || null,
          location: formValue(form, ["localisation", "location"]) || null,
          contract_type: formValue(form, ["contrat", "contract"]) || null,
          seats: parseInt(formValue(form, ["volume", "seats"]) || "", 10) || null,
          experience_level: formValue(form, ["experience"]) || null,
          skills: formValue(form, ["competences", "skills"]) || null,
          contact_role: formValue(form, ["fonction", "role"]) || null,
          company_size: formValue(form, ["taille", "size"]) || null
        }).then(function () {
          showFormMessage(form, isHiring ? hiringOk : fallback, false);
          form.reset();
          if (window.TalendusTrack) {
            if (isHiring) window.TalendusTrack.lead({ content_name: "hiring-need" });
            else if (kind === "contact" || (form.getAttribute("data-form") === "contact")) window.TalendusTrack.contact({ content_name: "contact" });
            else window.TalendusTrack.lead({ content_name: kind || "form" });
          }
        }).catch(function () {
          showFormMessage(form, isHiring ? hiringOk : fallback, false);
          form.reset();
        }).then(done);
      });
    });

    document.querySelectorAll('form[data-form="apply"] input[name="cvfile"], form[data-form="talent-cv"] input[name="cvfile"]').forEach(function (input) {
      var user = window.TalendusAPI && window.TalendusAPI.currentUser && window.TalendusAPI.currentUser();
      if (user && user.role === "CANDIDATE") {
        input.required = false;
        var hint = input.parentElement && input.parentElement.querySelector(".tl-file-hint");
        if (hint) {
          hint.textContent = isEn
            ? "PDF, Word or image, 5 MB max. Leave empty to use the resume already on your profile."
            : "PDF, Word ou image, 5 Mo max. Laissez vide pour utiliser le CV déjà dans votre profil.";
        }
      }
    });

    function money(amount) {
      return new Intl.NumberFormat(isEn ? "en-CA" : "fr-CA", {
        style: "currency",
        currency: "CAD",
        maximumFractionDigits: 0
      }).format(amount);
    }
    function setMoney(id, amount) {
      var el = document.getElementById(id);
      if (el) el.textContent = money(amount);
    }
    var salary = document.getElementById("tl-salary");
    var months = document.getElementById("tl-months");
    var result = document.getElementById("tl-cost");
    function calc() {
      if (!salary || !months || !result) return;
      var s = Math.max(0, Number(salary.value) || 0);
      var m = Math.max(1, Number(months.value) || 0);
      var paid = s * (m / 12);
      var training = s * 0.35;
      var restart = 18000;
      setMoney("tl-cost-paid", paid);
      setMoney("tl-cost-training", training);
      setMoney("tl-cost-restart", restart);
      result.textContent = money(paid + training + restart);
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
    var sector = document.getElementById("job-sector");
    var exp = document.getElementById("job-exp");
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
      var sec = (sector && sector.value) || "";
      var ex = (exp && exp.value) || "";
      var minSal = sal && sal.value ? Number(sal.value) : 0;
      var shown = 0;
      var root = document.getElementById("job-list") || document;
      root.querySelectorAll("[data-job]").forEach(function (card) {
        var hay = (card.getAttribute("data-job") || "").toLowerCase();
        var ok = (!q || hay.indexOf(q.toLowerCase()) !== -1)
          && (!c || hay.indexOf(c.toLowerCase()) !== -1)
          && (!v || (card.getAttribute("data-city") || "").toLowerCase() === v.toLowerCase() || hay.indexOf(v.toLowerCase()) !== -1)
          && (!ty || (card.getAttribute("data-type") || "").toLowerCase() === ty.toLowerCase() || hay.indexOf(ty.toLowerCase()) !== -1)
          && (!sh || (card.getAttribute("data-shift") || "").indexOf(sh) !== -1 || hay.indexOf(sh.toLowerCase()) !== -1)
          && (!sec || (card.getAttribute("data-sector") || "").toLowerCase() === sec.toLowerCase() || hay.indexOf(sec.toLowerCase()) !== -1)
          && (!ex || (card.getAttribute("data-exp") || "").toLowerCase() === ex.toLowerCase() || hay.indexOf(ex.toLowerCase()) !== -1);
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
      var countEl = document.getElementById("job-count");
      if (countEl) {
        countEl.textContent = isEn
          ? (shown + " opening" + (shown === 1 ? "" : "s"))
          : (shown + " offre" + (shown > 1 ? "s" : ""));
      }
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
    [search, cat, city, type, shift, sal, sector, exp].forEach(function (el) {
      if (el) el.addEventListener("input", filterJobsAndTrack);
      if (el) el.addEventListener("change", filterJobsAndTrack);
    });
    if (document.getElementById("job-list")) filterJobs();

    var jobList = document.getElementById("job-list");
    if (jobList && window.TalendusAPI) {
      window.TalendusAPI.jobs({ page_size: 24, sort: "relevance" }).then(function (payload) {
        var items = (payload && payload.data) || [];
        if (!items.length) return;
        var prefix = isEn ? "/en/job-" : "/emploi-";
        var expLabel = {
          debutant: isEn ? "Entry-level" : "Débutant",
          intermediaire: isEn ? "Mid-level" : "Intermédiaire",
          senior: isEn ? "Senior" : "Senior"
        };
        var catLabel = {
          entrepot: isEn ? "Warehouse" : "Entrepôt",
          production: "Production",
          metallurgie: isEn ? "Metals" : "Métallurgie",
          manufacturier: isEn ? "Manufacturing" : "Manufacturier",
          maintenance: "Maintenance",
          supervision: "Supervision",
          logistique: isEn ? "Logistics" : "Logistique",
          cadres: isEn ? "Leadership" : "Cadres",
          technologie: isEn ? "Technology" : "Technologie",
          finance: "Finance",
          ingenierie: isEn ? "Engineering" : "Ingénierie",
          transport: isEn ? "Transportation" : "Transport",
          sante: isEn ? "Healthcare" : "Santé",
          commerce: isEn ? "Retail" : "Commerce",
          administration: "Administration",
          marketing: "Marketing"
        };
        var catIcon = {
          entrepot: "fa-warehouse",
          production: "fa-industry",
          metallurgie: "fa-fire",
          manufacturier: "fa-gears",
          maintenance: "fa-wrench",
          supervision: "fa-user-tie",
          logistique: "fa-boxes-stacked",
          cadres: "fa-briefcase",
          technologie: "fa-laptop-code",
          finance: "fa-calculator",
          ingenierie: "fa-compass-drafting",
          transport: "fa-truck",
          sante: "fa-heart-pulse",
          commerce: "fa-store",
          administration: "fa-building",
          marketing: "fa-bullhorn"
        };
        jobList.innerHTML = items.map(function (job) {
          var href = prefix + job.slug + ".html";
          var salary = job.salary_display || "";
          var shiftVal = job.shift || "";
          var loc = job.location || "";
          var typ = job.contract_type || "";
          var sector = job.sector || "";
          var skills = job.skills || "";
          var exp = job.experience_level || "";
          var cat = String(job.category || sector || "").toLowerCase();
          var hay = [job.title, loc, cat, sector, typ, salary, shiftVal, skills, exp].join(" ");
          var excerpt = job.summary || job.qualifications || job.description || skills || "";
          if (excerpt.length > 180) excerpt = excerpt.slice(0, 177) + "…";
          var shownCat = catLabel[cat] || job.category || sector || "";
          var cta = isEn ? "View opening and apply" : "Voir l'offre et postuler";
          var icon = catIcon[cat] || "fa-briefcase";
          var chips = String(skills).split(/[,;]/).map(function (s) { return s.trim(); }).filter(Boolean).slice(0, 6)
            .map(function (s) { return "<span>" + escapeHtml(s) + "</span>"; }).join("");
          var facts = "";
          if (loc) facts += "<div><dt>" + (isEn ? "Location" : "Lieu") + "</dt><dd>" + escapeHtml(loc) + "</dd></div>";
          if (salary) facts += "<div><dt>" + (isEn ? "Pay" : "Rémunération") + "</dt><dd>" + escapeHtml(salary) + "</dd></div>";
          if (shiftVal) facts += "<div><dt>" + (isEn ? "Schedule" : "Horaire") + "</dt><dd>" + escapeHtml(shiftVal) + "</dd></div>";
          return '<a class="tl-job-card" href="' + href + '" aria-label="' + escapeHtml(cta + " : " + job.title) + '" data-job="' + escapeHtml(hay) + '" data-city="' + escapeHtml(loc) + '" data-cat="' + escapeHtml(cat) + '" data-type="' + escapeHtml(typ) + '" data-shift="' + escapeHtml(shiftVal) + '" data-salary="' + escapeHtml(salary) + '" data-sector="' + escapeHtml(sector.toLowerCase()) + '" data-exp="' + escapeHtml(String(exp).toLowerCase()) + '">' +
            '<div class="tl-job-card-banner"><span class="tl-job-card-icon" aria-hidden="true"><i class="fa-solid ' + icon + '"></i></span><div class="tl-job-card-banner-text"><p class="tl-job-card-cat">' + escapeHtml(shownCat) + '</p><p class="tl-job-card-via">Via Talendus</p></div></div>' +
            '<div class="tl-job-card-body">' +
            '<div class="tl-job-card-top">' + (typ ? '<span class="tl-chip orange">' + escapeHtml(typ) + "</span>" : "") +
            (expLabel[exp] ? '<span class="tl-chip">' + escapeHtml(expLabel[exp]) + "</span>" : "") + "</div>" +
            "<h3>" + escapeHtml(job.title) + "</h3>" +
            (facts ? '<dl class="tl-job-facts-mini">' + facts + "</dl>" : "") +
            (excerpt ? '<p class="tl-job-excerpt-label">' + (isEn ? "Profile we look for" : "Profil recherché") + '</p><p class="tl-job-excerpt">' + escapeHtml(excerpt) + "</p>" : "") +
            (chips ? '<div class="tl-job-skills">' + chips + "</div>" : "") +
            '</div><span class="tl-job-card-cta">' + cta + "</span></a>";
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

    (function setupPwa() {
      var standalone = window.matchMedia && window.matchMedia("(display-mode: standalone)").matches;
      if (window.navigator && window.navigator.standalone) standalone = true;
      if (standalone) document.documentElement.classList.add("tl-standalone");
      if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
        navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
      }
      if (standalone || /\/admin\//.test(location.pathname)) return;
      var dismissed = false;
      try { dismissed = localStorage.getItem("talendus_install_dismissed") === "1"; } catch (e) {}
      var deferred = null;
      window.addEventListener("beforeinstallprompt", function (e) {
        e.preventDefault();
        deferred = e;
        showInstall(true);
      });
      function showInstall(canNative) {
        if (dismissed || document.querySelector(".tl-install-banner")) return;
        var box = document.createElement("div");
        box.className = "tl-install-banner is-on";
        box.setAttribute("role", "dialog");
        var appHref = isEn ? "app.html" : "app.html";
        if (location.pathname.indexOf("/en/") === 0) appHref = "/en/app.html";
        else appHref = "/app.html";
        box.innerHTML = "<p>" + (isEn
          ? "Install the Talendus app on your phone. Jobs, profile, messages and click-to-call — Android and iPhone."
          : "Installez l'appli Talendus sur votre téléphone. Offres, profil, messages et appel direct — Android et iPhone.") +
          "</p><div class=\"tl-actions\">" +
          (canNative ? "<button type=\"button\" class=\"tl-btn\" data-install-native>" + (isEn ? "Install" : "Installer") + "</button>" : "") +
          "<a class=\"tl-btn" + (canNative ? " tl-btn-ghost" : "") + "\" href=\"" + appHref + "\">" + (isEn ? "How to install" : "Comment installer") + "</a>" +
          "<button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-install-dismiss>" + (isEn ? "Later" : "Plus tard") + "</button></div>";
        document.body.appendChild(box);
        box.querySelector("[data-install-dismiss]").addEventListener("click", function () {
          box.remove();
          try { localStorage.setItem("talendus_install_dismissed", "1"); } catch (err) {}
        });
        var nativeBtn = box.querySelector("[data-install-native]");
        if (nativeBtn) nativeBtn.addEventListener("click", function () {
          if (!deferred) return;
          deferred.prompt();
          deferred.userChoice.finally(function () { deferred = null; box.remove(); });
        });
      }
      setTimeout(function () { showInstall(!!deferred); }, 9000);
    })();
  });
})();
