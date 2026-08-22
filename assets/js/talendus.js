(function () {
  function isNativeApp() {
    var ua = navigator.userAgent || "";
    if (/TalendusApp/i.test(ua)) return true;
    if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return true;
    if (window.matchMedia && window.matchMedia("(display-mode: fullscreen)").matches) return true;
    if (window.navigator && window.navigator.standalone) return true;
    if (/\/m\.html$/.test(location.pathname || "")) return true;
    return false;
  }

  if (isNativeApp()) {
    document.documentElement.classList.add("tl-standalone", "tl-native-app");
    var path = location.pathname || "/";
    if (!/\/m\.html$/.test(path) && path.indexOf("/download/") !== 0 && path.indexOf("/admin") !== 0 && path.indexOf("/api/") !== 0) {
      var hash = location.hash || "";
      var portal = path.match(/\/(candidate|employer)(?:\/(.*))?$/);
      if (portal) hash = "#/" + (portal[2] || "home");
      location.replace((path.indexOf("/en/") === 0 ? "/en/m.html" : "/m.html") + hash);
      return;
    }
  }

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

  function wireFormLabels() {
    document.querySelectorAll(".tl-form label").forEach(function (label, i) {
      if (label.htmlFor || label.querySelector("input, select, textarea")) return;
      var next = label.nextElementSibling;
      if (!next || !/^(INPUT|SELECT|TEXTAREA)$/.test(next.tagName)) return;
      if (!next.id) next.id = "tl-field-" + (next.getAttribute("name") || i);
      label.setAttribute("for", next.id);
    });
  }

  ready(function () {
    markActiveNav();
    setTimeout(markActiveNav, 250);
    wireFormLabels();

    if (window.jQuery) {
      var $ = window.jQuery;
      $(window).off("load");
      $(window).on("load.talendus", function () {
        var minMs = 180;
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

    var lastPublicContact = null;
    function applyPublicContact(data) {
      if (data) lastPublicContact = data;
      else data = lastPublicContact;
      var c = data && data.contact;
      if (!c) return;
      var email = c.email || "info@talendus.ca";
      if (c.demo) {
        document.querySelectorAll("a.tl-whatsapp, a[href*='wa.me/']").forEach(function (a) {
          a.hidden = true;
          a.setAttribute("href", "mailto:" + email);
        });
        document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
          a.setAttribute("href", "mailto:" + email);
          if (/514\s*555|whatsapp/i.test(a.textContent || "")) a.textContent = email;
        });
        document.querySelectorAll('script[type="application/ld+json"]').forEach(function (el) {
          try {
            var data = JSON.parse(el.textContent);
            var changed = false;
            function stripPhone(obj) {
              if (!obj || typeof obj !== "object") return;
              if (Array.isArray(obj)) { obj.forEach(stripPhone); return; }
              if (obj.telephone && /555/.test(String(obj.telephone))) {
                delete obj.telephone;
                changed = true;
              }
            }
            stripPhone(data);
            if (changed) el.textContent = JSON.stringify(data);
          } catch (err) {}
        });
        return;
      }
      var e164 = String(c.phone_e164 || "").replace(/\D/g, "");
      if (!e164) return;
      var tel = "tel:+" + e164;
      var waBase = "https://wa.me/" + e164;
      var display = c.phone_display || "";
      var persona = (document.body.getAttribute("data-persona") || "");
      var waMsg;
      if (isEn) {
        if (persona === "talent") waMsg = "?text=" + encodeURIComponent("Hello Talendus, I am looking for work.");
        else if (persona === "entreprise") waMsg = "?text=" + encodeURIComponent("Hello Talendus, I would like to talk about a hiring need.");
        else waMsg = "?text=" + encodeURIComponent("Hello Talendus, I would like to talk.");
      } else if (persona === "talent") {
        waMsg = "?text=" + encodeURIComponent("Bonjour Talendus, je cherche un emploi.");
      } else if (persona === "entreprise") {
        waMsg = "?text=" + encodeURIComponent("Bonjour Talendus, je souhaite discuter d'un besoin de recrutement.");
      } else {
        waMsg = "?text=" + encodeURIComponent("Bonjour Talendus, j'aimerais vous parler.");
      }
      document.querySelectorAll('a[href^="tel:"], a.tl-call').forEach(function (a) {
        a.hidden = false;
        a.setAttribute("href", tel);
        if (display && /514\s*555|info@talendus\.ca|263\s*558/i.test(a.textContent || "") && !a.querySelector("svg")) {
          a.textContent = display;
        }
      });
      document.querySelectorAll(".fa-phone").forEach(function (icon) {
        var a = icon.closest("a");
        if (!a) return;
        a.setAttribute("href", tel);
        if (display && /info@talendus\.ca|514\s*555|263\s*558/.test(a.textContent || "")) {
          a.innerHTML = icon.outerHTML + " " + display;
        }
      });
      document.querySelectorAll("a.tl-whatsapp, a[href*='wa.me/']").forEach(function (a) {
        a.hidden = false;
        a.setAttribute("href", waBase + waMsg);
      });
      document.querySelectorAll(".fa-whatsapp").forEach(function (icon) {
        var a = icon.closest("a");
        if (!a) return;
        a.hidden = false;
        a.setAttribute("href", waBase + waMsg);
      });
      document.querySelectorAll('script[type="application/ld+json"]').forEach(function (el) {
        try {
          var payload = JSON.parse(el.textContent);
          var changed = false;
          function setPhone(obj) {
            if (!obj || typeof obj !== "object") return;
            if (Array.isArray(obj)) { obj.forEach(setPhone); return; }
            if (obj["@type"] === "EmploymentAgency") {
              obj.telephone = "+" + e164;
              changed = true;
            }
          }
          setPhone(payload);
          if (changed) el.textContent = JSON.stringify(payload);
        } catch (err) {}
      });
      document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
        var href = a.getAttribute("href") || "";
        if (href.indexOf("info@talendus.ca") === -1) return;
        if (a.classList.contains("tl-call") || a.classList.contains("tl-whatsapp")) return;
        if (a.querySelector(".fa-phone, .fa-whatsapp")) return;
        a.setAttribute("href", "mailto:" + email);
        if ((a.textContent || "").indexOf("info@talendus.ca") !== -1) a.textContent = email;
      });
    }

    if (window.TalendusAPI && window.TalendusAPI.services) {
      window.TalendusAPI.services().then(function (json) {
        window.TalendusServices = json.data || {};
        applyPublicContact(json.data);
        try { window.dispatchEvent(new CustomEvent("talendus:services", { detail: json.data })); } catch (e) {}
      }).catch(function () {});
    }
    window.addEventListener("talendus:persona", function () {
      if (lastPublicContact) applyPublicContact(lastPublicContact);
    });

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
      box.classList.toggle("tl-error", !!isError);
      box.setAttribute("role", isError ? "alert" : "status");
    }

    function cvFileFromForm(form) {
      var fileInput = form.querySelector('input[type=file][name=cvfile]');
      return fileInput && fileInput.files && fileInput.files[0];
    }

    function validateCvFile(form, file) {
      if (!file) return true;
      var name = String(file.name || "");
      var type = String(file.type || "").toLowerCase();
      var namedOk = /\.(pdf|doc|docx|png|jpe?g|webp)$/i.test(name);
      var typedOk = /pdf|msword|wordprocessingml|image\/(jpeg|jpg|png|webp)/.test(type);
      if (file && !namedOk && !typedOk && /\.[A-Za-z0-9]+$/.test(name)) {
        showFormMessage(form, isEn ? "Use a PDF, Word or image file (PNG, JPG)." : "Utilisez un fichier PDF, Word ou image (PNG, JPG).", true);
        return false;
      }
      if (file && file.size > 5 * 1024 * 1024) {
        showFormMessage(form, isEn ? "The file must be 5 MB or less." : "Le fichier doit faire 5 Mo ou moins.", true);
        return false;
      }
      return true;
    }

    function injectHoneypot(form) {
      if (!form || form.querySelector('input[name="website_url"]')) return;
      var hp = document.createElement("input");
      hp.className = "tl-hp";
      hp.name = "website_url";
      hp.tabIndex = -1;
      hp.autocomplete = "off";
      hp.setAttribute("aria-hidden", "true");
      form.insertBefore(hp, form.firstChild);
    }

    document.querySelectorAll(".tl-form").forEach(function (form) {
      injectHoneypot(form);
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var kind = form.getAttribute("data-form") || (form.closest("#postuler") ? "apply" : "contact");
        var hiringOk = isEn
          ? "Your hiring need has been sent to Talendus. Our team will review the information and contact you to understand the role and define the profile together. Your recruiting starts with Talendus."
          : "Votre besoin a bien été transmis à Talendus. Notre équipe va analyser les informations communiquées et vous contacter afin de mieux comprendre votre besoin et de définir avec vous le profil recherché. Votre recrutement commence avec Talendus.";
        var fallback = isEn
          ? "Thanks. On weekdays we usually reply within 30 minutes. A consultant will follow up."
          : "Merci. En semaine, on répond en général en moins de 30 minutes. Un conseiller vous rappelle.";
        var sendFail = isEn
          ? "The message could not be sent. Check your connection and try again."
          : "L’envoi n’a pas abouti. Vérifiez votre connexion et réessayez.";
        var api = window.TalendusAPI;
        if (!api) {
          showFormMessage(form, sendFail, true);
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
              api.appendFile(up, file, "cv.pdf");
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
            fd.append("website_url", formValue(form, ["website_url"]));
            if (file) api.appendFile(fd, file, "cv.pdf");
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
            showFormMessage(form, (err && err.message) || sendFail, true);
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
          fd.append("website_url", formValue(form, ["website_url"]));
          if (file) api.appendFile(fd, file, "cv.pdf");
          api.request("/talent-profile", { method: "POST", body: fd }).then(function () {
            showFormMessage(form, fallback, false);
            form.reset();
            if (window.TalendusTrack) window.TalendusTrack.lead({ content_name: "talent-cv" });
          }).catch(function (err) {
            showFormMessage(form, (err && err.message) || sendFail, true);
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
            showFormMessage(form, (err && err.message) || sendFail, true);
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
          company_size: formValue(form, ["taille", "size"]) || null,
          website_url: formValue(form, ["website_url"]) || ""
        }).then(function () {
          showFormMessage(form, isHiring ? hiringOk : fallback, false);
          form.reset();
          if (window.TalendusTrack) {
            if (isHiring) window.TalendusTrack.lead({ content_name: "hiring-need" });
            else if (kind === "contact" || (form.getAttribute("data-form") === "contact")) window.TalendusTrack.contact({ content_name: "contact" });
            else window.TalendusTrack.lead({ content_name: kind || "form" });
          }
        }).catch(function (err) {
          showFormMessage(form, (err && err.message) || sendFail, true);
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
    var schedule = document.getElementById("job-schedule");
    var mode = document.getElementById("job-mode");
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
      var sch = (schedule && schedule.value) || "";
      var md = (mode && mode.value) || "";
      var sec = (sector && sector.value) || "";
      var ex = (exp && exp.value) || "";
      var minSal = sal && sal.value ? Number(sal.value) : 0;
      var shown = 0;
      var root = document.getElementById("job-list") || document;
      function hayOf(card) { return (card.getAttribute("data-job") || "").toLowerCase(); }
      function remoteLike(text) {
        return /remote|télétravail|teletravail|work from home|wfh/.test(String(text || "").toLowerCase());
      }
      function hybridLike(text) {
        return /hybride|hybrid/.test(String(text || "").toLowerCase());
      }
      function onsiteLike(text) {
        return /sur place|on-site|onsite|on site/.test(String(text || "").toLowerCase());
      }
      function cardMode(card) {
        return ((card.getAttribute("data-mode") || "") + " " + (card.getAttribute("data-city") || "") + " " + hayOf(card)).toLowerCase();
      }
      function cityOk(card) {
        if (!v) return true;
        if (v.toLowerCase() === "remote" || remoteLike(v)) return remoteLike(cardMode(card));
        var cityVal = (card.getAttribute("data-city") || "").toLowerCase();
        return cityVal === v.toLowerCase() || hayOf(card).indexOf(v.toLowerCase()) !== -1;
      }
      function modeOk(card) {
        if (!md) return true;
        var blob = cardMode(card);
        if (remoteLike(md)) return remoteLike(blob);
        if (hybridLike(md)) return hybridLike(blob);
        if (onsiteLike(md)) return onsiteLike(blob);
        return blob.indexOf(md.toLowerCase()) !== -1 || hayOf(card).indexOf(md.toLowerCase()) !== -1;
      }
      root.querySelectorAll("[data-job]").forEach(function (card) {
        var hay = hayOf(card);
        var ok = (!q || hay.indexOf(q.toLowerCase()) !== -1)
          && (!c || hay.indexOf(c.toLowerCase()) !== -1)
          && cityOk(card)
          && (!ty || (card.getAttribute("data-type") || "").toLowerCase() === ty.toLowerCase() || hay.indexOf(ty.toLowerCase()) !== -1)
          && (!sh || (card.getAttribute("data-shift") || "").indexOf(sh) !== -1 || hay.indexOf(sh.toLowerCase()) !== -1)
          && (!sch || (card.getAttribute("data-schedule") || "").indexOf(sch) !== -1 || hay.indexOf(sch.toLowerCase()) !== -1)
          && modeOk(card)
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
    [search, cat, city, type, shift, schedule, mode, sal, sector, exp].forEach(function (el) {
      if (el) el.addEventListener("input", filterJobsAndTrack);
      if (el) el.addEventListener("change", filterJobsAndTrack);
    });
    if (document.getElementById("job-list")) filterJobs();

    var filtersRoot = document.querySelector(".tl-filters-search");
    if (filtersRoot && !filtersRoot.querySelector(".tl-filters-toggle")) {
      var extra = filtersRoot.querySelectorAll(".tl-filter");
      if (extra.length > 4) {
        var toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "tl-text-btn tl-filters-toggle";
        toggle.textContent = isEn ? "More filters" : "Plus de filtres";
        toggle.addEventListener("click", function () {
          var open = filtersRoot.classList.toggle("is-open");
          toggle.textContent = open
            ? (isEn ? "Fewer filters" : "Moins de filtres")
            : (isEn ? "More filters" : "Plus de filtres");
        });
        filtersRoot.appendChild(toggle);
      }
    }

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
          var scheduleVal = job.schedule || "";
          var modeVal = job.work_mode || "";
          var loc = job.location || "";
          var typ = job.contract_type || "";
          var sector = job.sector || "";
          var skills = job.skills || "";
          var exp = job.experience_level || "";
          var cat = String(job.category || sector || "").toLowerCase();
          var hay = [job.title, loc, cat, sector, typ, salary, shiftVal, scheduleVal, modeVal, skills, exp].join(" ");
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
          if (scheduleVal) facts += "<div><dt>" + (isEn ? "Hours" : "Horaire") + "</dt><dd>" + escapeHtml(scheduleVal) + "</dd></div>";
          if (shiftVal) facts += "<div><dt>" + (isEn ? "Shift" : "Quart") + "</dt><dd>" + escapeHtml(shiftVal) + "</dd></div>";
          return '<a class="tl-job-card" href="' + href + '" aria-label="' + escapeHtml(cta + " : " + job.title) + '" data-job="' + escapeHtml(hay) + '" data-city="' + escapeHtml(loc) + '" data-cat="' + escapeHtml(cat) + '" data-type="' + escapeHtml(typ) + '" data-shift="' + escapeHtml(shiftVal) + '" data-schedule="' + escapeHtml(scheduleVal) + '" data-mode="' + escapeHtml(modeVal) + '" data-salary="' + escapeHtml(salary) + '" data-sector="' + escapeHtml(sector.toLowerCase()) + '" data-exp="' + escapeHtml(String(exp).toLowerCase()) + '">' +
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
      var DISMISS_KEY = "talendus_install_dismissed_at";
      var ASKED_KEY = "talendus_install_asked";
      var ua = (navigator.userAgent || "").toLowerCase();
      var isIos = /iphone|ipad|ipod/.test(ua);
      var isAndroid = /android/.test(ua);
      var isDesktopOs = (/windows nt|macintosh|cros/.test(ua) && !/iphone|ipad|ipod|android/.test(ua))
        || (/linux/.test(ua) && !/android|iphone|ipad/.test(ua))
        || (navigator.userAgentData && navigator.userAgentData.mobile === false);
      var isPhone = (isIos || isAndroid) && !isDesktopOs && window.innerWidth < 900;
      if (isDesktopOs) document.documentElement.classList.add("tl-desktop-os");
      var isChromeIos = isIos && /crios/.test(ua);
      var isSafariIos = isIos && /safari/.test(ua) && !/crios|fxios|edgios/.test(ua);
      var standalone = isNativeApp();
      if (standalone) document.documentElement.classList.add("tl-standalone", "tl-native-app");
      if (standalone) {
        try {
          localStorage.setItem(DISMISS_KEY, String(Date.now() + 365 * 24 * 60 * 60 * 1000));
          sessionStorage.setItem(ASKED_KEY, "1");
        } catch (e) {}
      }
      if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
        navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
      }

      var board = document.getElementById("tl-install-board");
      if (board) {
        if (standalone) {
          board.querySelectorAll("[data-install-already]").forEach(function (el) { el.hidden = false; });
        }
        if (isChromeIos || (isIos && !isSafariIos)) {
          board.querySelectorAll("[data-install-safari]").forEach(function (el) { el.hidden = false; });
        }
        if (isAndroid) {
          board.querySelectorAll("[data-install-ios]").forEach(function (el) { el.hidden = true; });
          board.querySelectorAll("[data-install-ios-file]").forEach(function (el) { el.hidden = true; });
        } else if (isIos) {
          board.querySelectorAll("[data-install-android]").forEach(function (el) { el.hidden = true; });
          board.querySelectorAll("[data-install-android-file]").forEach(function (el) { el.hidden = true; });
        }
      }

      var dismissed = false;
      try {
        var until = parseInt(localStorage.getItem(DISMISS_KEY) || "0", 10);
        dismissed = until > Date.now();
        if (localStorage.getItem("talendus_install_dismissed") === "1") dismissed = true;
      } catch (e) {}

      var APK_URL = "/download/talendus.apk";
      var IOS_URL = "/download/talendus.mobileconfig";
      var deferred = null;
      window.TalendusInstall = {
        prompt: function () { return runInstall(); }
      };

      function rememberDismiss(days) {
        try {
          localStorage.setItem(DISMISS_KEY, String(Date.now() + (days || 14) * 24 * 60 * 60 * 1000));
          sessionStorage.setItem(ASKED_KEY, "1");
        } catch (err) {}
        dismissed = true;
      }

      function askedThisVisit() {
        try { return sessionStorage.getItem(ASKED_KEY) === "1"; } catch (e) { return false; }
      }

      function hideBanner() {
        var box = document.querySelector(".tl-install-banner");
        if (box) box.remove();
      }

      function packageUrl() {
        return isIos ? IOS_URL : APK_URL;
      }

      function startPackageDownload(url) {
        window.location.assign(url || packageUrl());
      }

      function runInstall() {
        hideBanner();
        rememberDismiss(365);
        if (!isIos && deferred && typeof deferred.prompt === "function") {
          var ev = deferred;
          deferred = null;
          return ev.prompt().then(function () {
            return ev.userChoice;
          }).then(function (choice) {
            if (choice && choice.outcome === "accepted") {
              rememberDismiss(365);
              return;
            }
            startPackageDownload(APK_URL);
            showFollowUp("android");
          }).catch(function () {
            startPackageDownload(APK_URL);
            showFollowUp("android");
          });
        }
        startPackageDownload();
        showFollowUp(isIos ? "ios" : "android");
        return Promise.resolve();
      }

      function showFollowUp(kind) {
        rememberDismiss(365);
        if (document.querySelector(".tl-install-sheet")) return;
        var sheet = document.createElement("div");
        sheet.className = "tl-install-sheet is-on";
        sheet.setAttribute("role", "dialog");
        sheet.setAttribute("aria-modal", "true");
        var title = isEn ? "Install Talendus now" : "Installez Talendus maintenant";
        var body = kind === "ios"
          ? (isEn
            ? "<p>Allow the profile, then open <strong>Settings</strong>. At the top, tap <strong>Profile Downloaded</strong>, then tap <strong>Install</strong>.</p>"
            : "<p>Autorisez le profil, puis ouvrez <strong>Réglages</strong>. En haut, touchez <strong>Profil téléchargé</strong>, puis touchez <strong>Installer</strong>.</p>")
          : (isEn
            ? "<p>The file is at the bottom of the screen. Tap it once, then tap <strong>Install</strong>.</p>"
            : "<p>Le fichier est en bas de l'écran. Touchez-le une fois, puis touchez <strong>Installer</strong>.</p>");
        if (kind === "ios" && (isChromeIos || !isSafariIos)) {
          body += "<p class=\"tl-install-safari-note\">" + (isEn
            ? "If nothing happens, open this page in Safari (the blue compass icon) and tap Install again."
            : "Si rien ne se passe, ouvrez cette page avec Safari (l'icône boussole bleue) et touchez Installer encore une fois.") + "</p>";
        }
        sheet.innerHTML =
          "<div class=\"tl-install-sheet-card\">" +
            "<button type=\"button\" class=\"tl-auth-close\" data-install-close aria-label=\"" + (isEn ? "Close" : "Fermer") + "\"><i class=\"fa-solid fa-xmark\" aria-hidden=\"true\"></i></button>" +
            "<div class=\"tl-install-icon-preview\" aria-hidden=\"true\"><img src=\"/assets/img/logo/icon-192.png\" width=\"64\" height=\"64\" alt=\"\"><span>Talendus</span></div>" +
            "<h2>" + title + "</h2>" + body +
            "<p class=\"tl-install-sheet-actions\"><button type=\"button\" class=\"tl-btn\" data-install-close>" + (isEn ? "Done" : "C'est fait") + "</button></p>" +
          "</div>";
        document.body.appendChild(sheet);
        function close() { sheet.remove(); }
        sheet.querySelectorAll("[data-install-close]").forEach(function (el) {
          el.addEventListener("click", close);
        });
        sheet.addEventListener("click", function (e) { if (e.target === sheet) close(); });
      }

      document.querySelectorAll("[data-install-now]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          runInstall();
        });
      });
      document.querySelectorAll("[data-install-android-file]").forEach(function (link) {
        link.addEventListener("click", function () { showFollowUp("android"); });
      });
      document.querySelectorAll("[data-install-ios-file]").forEach(function (link) {
        link.addEventListener("click", function () { showFollowUp("ios"); });
      });

      window.addEventListener("beforeinstallprompt", function (e) {
        e.preventDefault();
        deferred = e;
        var nativeBtn = document.querySelector("[data-install-now]");
        if (nativeBtn) nativeBtn.classList.add("is-ready");
        maybeShowBanner();
      });
      window.addEventListener("appinstalled", function () {
        markInstalled();
        var sheet = document.querySelector(".tl-install-sheet");
        if (sheet) sheet.remove();
      });

      function showBanner() {
        if (document.querySelector(".tl-install-banner")) return;
        var box = document.createElement("div");
        box.className = "tl-install-banner is-on";
        box.setAttribute("role", "dialog");
        box.setAttribute("aria-label", isEn ? "Download Talendus" : "Télécharger Talendus");
        box.innerHTML = "<p>" + (isEn
          ? "Put Talendus on your phone. Jobs, messages and your consultant — one tap, like your other apps."
          : "Mettez Talendus sur votre téléphone. Offres, messages et votre conseiller, en un tap — comme vos autres applis.") +
          "</p><div class=\"tl-actions\">" +
          "<button type=\"button\" class=\"tl-btn\" data-install-native>" + (isEn ? "Download the app" : "Télécharger l'appli") + "</button>" +
          "<button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-install-dismiss>" + (isEn ? "Not now" : "Pas maintenant") + "</button></div>";
        document.body.appendChild(box);
        box.querySelector("[data-install-dismiss]").addEventListener("click", function () {
          hideBanner();
          rememberDismiss(14);
        });
        box.querySelector("[data-install-native]").addEventListener("click", function () {
          runInstall();
        });
      }

      function alreadyInstalled() {
        if (isNativeApp() || standalone) return true;
        try {
          if (window.matchMedia && (
            window.matchMedia("(display-mode: standalone)").matches
            || window.matchMedia("(display-mode: fullscreen)").matches
            || window.matchMedia("(display-mode: minimal-ui)").matches
          )) return true;
        } catch (e) {}
        return false;
      }

      function markInstalled() {
        document.documentElement.classList.add("tl-app-installed");
        rememberDismiss(365);
        hideBanner();
      }

      function maybeShowBanner() {
        if (isDesktopOs || !isPhone || alreadyInstalled() || dismissed || askedThisVisit()) return;
        if (/\/admin\//.test(location.pathname)) return;
        if (board) return;
        showBanner();
      }
      if (alreadyInstalled()) markInstalled();

      if (navigator.getInstalledRelatedApps) {
        try {
          navigator.getInstalledRelatedApps().then(function (apps) {
            if (apps && apps.length) markInstalled();
            maybeShowBanner();
          }).catch(function () { maybeShowBanner(); });
        } catch (e) {
          setTimeout(maybeShowBanner, 2500);
        }
      } else {
        setTimeout(maybeShowBanner, 2500);
      }
    })();
  });
})();
