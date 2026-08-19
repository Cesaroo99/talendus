"""Fiches d'emploi publiques pour les offres créées dans le back-office (sans HTML statique)."""

from __future__ import annotations

import html
import sys
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import JobOffer
from app.services.jobs import get_public_job
from app.services.seo import job_posting_schema

SITE_ROOT = Path(__file__).resolve().parents[3]


def _parts():
    scripts = str(SITE_ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from parts import page_hero, wrap  # noqa: WPS433

    return wrap, page_hero


def render_job_page(db: Session, slug: str, lang: str = "fr") -> str:
    job = get_public_job(db, slug)
    return render_job_html(job, lang)


def render_job_html(job: JobOffer, lang: str = "fr") -> str:
    wrap, page_hero = _parts()
    is_en = lang == "en"
    title = job.title or ""
    loc = job.location or ("Quebec" if is_en else "Québec")
    salary = job.salary_display or ""
    contract = job.contract_type or ("Permanent" if is_en else "Permanent")
    shift = job.shift or ""
    skills = job.skills or ""
    sector = job.sector or ""
    experience = job.experience_level or ""
    slug = job.slug or job.id
    page_title = (
        f"{title} in {loc} | Job | Talendus" if is_en else f"{title} à {loc} | Emploi | Talendus"
    )
    desc = (
        f"{title} opening in {loc}, Quebec. Apply through Talendus — a consultant presents your file."
        if is_en
        else f"Poste de {title} à {loc}, Québec. Postulez via Talendus : un conseiller présente votre dossier."
    )
    slug_path = f"en/job-{slug}.html" if is_en else f"emploi-{slug}.html"
    alt = f"emploi-{slug}.html" if is_en else f"en/job-{slug}.html"

    def esc(value: str | None) -> str:
        return html.escape(value or "")

    def para(text: str | None) -> str:
        raw = (text or "").strip()
        if not raw:
            return ""
        return "".join(f"<p>{html.escape(block).replace(chr(10), '<br>')}</p>" for block in raw.split("\n\n") if block.strip())

    facts = []
    if loc:
        facts.append(f"<li>{'Location' if is_en else 'Lieu'} : {esc(loc)}</li>")
    if contract:
        facts.append(f"<li>{'Contract' if is_en else 'Contrat'} : {esc(contract)}</li>")
    if salary:
        facts.append(f"<li>{'Pay' if is_en else 'Rémunération'} : {esc(salary)}</li>")
    if job.schedule:
        facts.append(f"<li>{'Hours' if is_en else 'Horaire'} : {esc(job.schedule)}</li>")
    if shift:
        facts.append(f"<li>{'Shift' if is_en else 'Quart'} : {esc(shift)}</li>")
    if job.work_mode:
        facts.append(f"<li>{'Workplace' if is_en else 'Présence'} : {esc(job.work_mode)}</li>")
    if job.languages:
        facts.append(f"<li>{'Languages' if is_en else 'Langues'} : {esc(job.languages)}</li>")
    if job.overtime:
        facts.append(f"<li>{'Overtime' if is_en else 'Heures sup.'} : {esc(job.overtime)}</li>")
    if job.driver_license:
        facts.append(f"<li>{'Driver’s licence' if is_en else 'Permis'} : {esc(job.driver_license)}</li>")
    if job.unionized:
        facts.append(f"<li>{'Union' if is_en else 'Syndicat'} : {esc(job.unionized)}</li>")
    if job.travel:
        facts.append(f"<li>{'Travel' if is_en else 'Déplacements'} : {esc(job.travel)}</li>")
    if experience:
        facts.append(f"<li>{'Experience' if is_en else 'Expérience'} : {esc(experience)}</li>")
    if job.education_required:
        facts.append(f"<li>{'Education' if is_en else 'Formation'} : {esc(job.education_required)}</li>")
    if job.certifications:
        facts.append(f"<li>{'Certifications' if is_en else 'Certifications'} : {esc(job.certifications)}</li>")
    if job.start_date:
        facts.append(f"<li>{'Start date' if is_en else 'Entrée en poste'} : {esc(job.start_date)}</li>")
    if job.openings and job.openings > 1:
        facts.append(f"<li>{'Openings' if is_en else 'Postes'} : {job.openings}</li>")
    if sector:
        facts.append(f"<li>{'Sector' if is_en else 'Secteur'} : {esc(sector)}</li>")

    kicker = "Job opening" if is_en else "Offre d’emploi"
    lead = (
        "A Talendus consultant reviews your file and calls you when it matches the mandate. Apply here to move forward."
        if is_en
        else "Un conseiller Talendus étudie votre dossier et vous rappelle s’il correspond au mandat. Postulez ici pour avancer."
    )
    apply_title = "Send your file to Talendus" if is_en else "Envoyez votre dossier à Talendus"
    apply_lead = (
        "Upload your résumé. A consultant studies your file and gets back to you. Call us if you want to move faster."
        if is_en
        else "Téléversez votre CV. Un conseiller étudie votre dossier et vous relance. Appelez-nous si vous voulez aller plus vite."
    )
    submit = "Submit my application" if is_en else "Envoyer ma candidature"
    jobs_href = "/en/jobs.html" if is_en else "/emplois.html"
    talent_href = "/en/talent.html" if is_en else "/candidats.html"

    body = page_hero(kicker, esc(title), lead) + f"""
    <section class="tl-section tl-job-main"><div class="container tl-job-layout">
      <div>
        <ul class="tl-job-facts">{"".join(facts)}</ul>
        {f"<h2>{'The role' if is_en else 'Le poste'}</h2>{para(job.description)}" if job.description else ""}
        {f"<h2>{'Responsibilities' if is_en else 'Responsabilités'}</h2>{para(job.responsibilities)}" if job.responsibilities else ""}
        {f"<h2>{'What we look for' if is_en else 'Profil recherché'}</h2>{para(job.qualifications or skills)}" if (job.qualifications or skills) else ""}
        {f"<p><b>{'Benefits' if is_en else 'Avantages'} :</b> {esc(job.benefits)}</p>" if job.benefits else ""}
        <h2>{'How to apply' if is_en else 'Comment postuler'}</h2>
        <ol class="tl-job-steps">
          <li><span class="tl-job-step-n">1</span><div><strong>{'You apply here with your résumé.' if is_en else 'Vous postulez ici avec votre CV.'}</strong></div></li>
          <li><span class="tl-job-step-n">2</span><div><strong>{'A consultant reviews it.' if is_en else 'Un conseiller l’étudie.'}</strong></div></li>
          <li><span class="tl-job-step-n">3</span><div><strong>{'If it fits, we present you.' if is_en else 'Si ça colle, nous vous présentons.'}</strong></div></li>
          <li><span class="tl-job-step-n">4</span><div><strong>{'You follow up with us.' if is_en else 'Vous suivez la suite avec nous.'}</strong></div></li>
        </ol>
        <p class="tl-job-alt"><a href="{jobs_href}">{'See other openings' if is_en else 'Voir les autres offres'}</a> · <a href="{talent_href}">{'Create a talent profile' if is_en else 'Créer un profil talent'}</a></p>
      </div>
      <aside class="tl-job-aside">
        <div class="tl-job-apply-card" id="postuler">
          <p class="tl-job-apply-kicker">{'Application' if is_en else 'Candidature'}</p>
          <h2>{apply_title}</h2>
          <p>{apply_lead}</p>
          <form class="tl-form" data-form="apply" data-job-slug="{esc(slug)}" enctype="multipart/form-data">
            <label>{'Name' if is_en else 'Nom'}</label><input name="nom" required autocomplete="name">
            <label>{'Email' if is_en else 'Courriel'}</label><input type="email" name="courriel" required autocomplete="email">
            <label>{'Phone' if is_en else 'Téléphone'}</label><input name="tel" autocomplete="tel">
            <label class="tl-file">
              <span>{'Your résumé' if is_en else 'Votre CV'}</span>
              <input type="file" name="cvfile" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg" required>
            </label>
            <label>{'Note for Talendus' if is_en else 'Note pour Talendus'} <span class="tl-optional">({('optional' if is_en else 'facultatif')})</span></label>
            <textarea name="message" rows="3" maxlength="800"></textarea>
            <button class="tl-btn tl-btn-lg" type="submit">{submit}</button>
            <div class="tl-success"></div>
          </form>
        </div>
      </aside>
    </div></section>
    """
    schema = job_posting_schema(job)
    if is_en:
        schema["url"] = schema.get("url", "").replace("/emploi-", "/en/job-")
    return wrap(
        page_title,
        desc,
        slug_path,
        body,
        lang="en" if is_en else "fr",
        alt=alt,
        robots="index,follow",
        extra_json_ld=schema,
        og_type="article",
        persona="talent",
    )


def static_job_path(slug: str, lang: str = "fr") -> Path:
    if lang == "en":
        return SITE_ROOT / "en" / f"job-{slug}.html"
    return SITE_ROOT / f"emploi-{slug}.html"
