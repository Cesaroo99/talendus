"""Sitemap, robots, JSON-LD JobPosting et redirections 301."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import JobOffer
from app.models.cms import BlogPost
from app.models.enums import BlogStatus, JobStatus, utcnow

SITE_ROOT = Path(__file__).resolve().parents[3]

REDIRECTS = {
    "/index1.html": "/",
    "/index2.html": "/",
    "/index3.html": "/",
    "/index4.html": "/",
    "/index5.html": "/",
    "/index6.html": "/",
    "/index7.html": "/",
    "/index8.html": "/",
    "/index9.html": "/",
    "/index10.html": "/",
    "/projects.html": "/",
    "/projects-left.html": "/",
    "/projects-right.html": "/",
    "/projects-single.html": "/",
    "/team.html": "/",
    "/testimonial.html": "/",
    "/about.html": "/a-propos.html",
    "/service.html": "/services.html",
    "/service-left.html": "/services.html",
    "/service-right.html": "/services.html",
    "/employeurs.html": "/entreprises.html",
    "/blog-single.html": "/blog.html",
    "/service-single.html": "/services.html",
    "/blog-left.html": "/blog.html",
    "/blog-right.html": "/blog.html",
    "/publier-une-offre.html": "/besoin-de-recrutement.html",
    "/en/post-a-job.html": "/en/hiring-need.html",
}

PRIVATE_PATHS = {
    "/admin/",
    "/espace.html",
    "/espace-employeur.html",
    "/en/account.html",
    "/en/account-employer.html",
}

STATIC_PAIRS = [
    ("", "en/"),
    ("a-propos.html", "en/about.html"),
    ("services.html", "en/services.html"),
    ("entreprises.html", "en/employers.html"),
    ("candidats.html", "en/candidates.html"),
    ("emplois.html", "en/jobs.html"),
    ("secteurs.html", "en/sectors.html"),
    ("blog.html", "en/blog.html"),
    ("contact.html", "en/contact.html"),
    ("confidentialite.html", "en/privacy.html"),
    ("conditions.html", "en/terms.html"),
    ("recrutement-industriel.html", "en/industrial-recruiting.html"),
    ("recrutement-manufacturier.html", "en/manufacturing-recruiting.html"),
    ("recrutement-technique.html", "en/technical-recruiting.html"),
    ("recrutement-permanent.html", "en/permanent-recruiting.html"),
    ("recrutement-temporaire.html", "en/temporary-recruiting.html"),
    ("chasse-de-tetes.html", "en/executive-search.html"),
    ("recrutement-cadres.html", "en/leadership-recruiting.html"),
    ("recrutement-industriel-montreal.html", "en/industrial-recruiting-montreal.html"),
    ("recrutement-industriel-laval.html", "en/industrial-recruiting-laval.html"),
    ("recrutement-industriel-longueuil.html", "en/industrial-recruiting-longueuil.html"),
    ("recrutement-industriel-quebec.html", "en/industrial-recruiting-quebec.html"),
    ("comment-ca-fonctionne.html", "en/how-it-works.html"),
    ("besoin-de-recrutement.html", "en/hiring-need.html"),
    ("solutions-rh.html", "en/hr-solutions.html"),
]


def canonical_host() -> str:
    return (get_settings().seo_canonical_host or "https://talendus.ca").rstrip("/")


def job_posting_schema(job: JobOffer) -> dict:
    host = canonical_host()
    url = f"{host}/emploi-{job.slug}.html"
    payload: dict = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": job.title,
        "description": (job.description or job.title)[:8000],
        "identifier": {"@type": "PropertyValue", "name": "Talendus", "value": job.slug or job.id},
        "datePosted": job.published_at.date().isoformat() if job.published_at else None,
        "employmentType": "FULL_TIME" if (job.contract_type or "").lower().startswith("perm") else "OTHER",
        "hiringOrganization": {"@type": "EmploymentAgency", "name": "Talendus", "sameAs": host, "logo": f"{host}/assets/img/logo/logo1.png"},
        "jobLocation": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": job.location or "Québec",
                "addressRegion": "QC",
                "addressCountry": "CA",
            },
        },
        "url": url,
    }
    if job.expires_at:
        payload["validThrough"] = job.expires_at.date().isoformat()
    if job.company:
        payload["hiringOrganization"]["name"] = "Talendus"
        payload["industry"] = job.sector
    if job.salary_min and job.salary_max:
        payload["baseSalary"] = {
            "@type": "MonetaryAmount",
            "currency": job.currency or "CAD",
            "value": {"@type": "QuantitativeValue", "minValue": job.salary_min, "maxValue": job.salary_max, "unitText": "YEAR"},
        }
    elif job.salary_display:
        payload["baseSalary"] = {"@type": "MonetaryAmount", "currency": job.currency or "CAD", "value": job.salary_display}
    return {k: v for k, v in payload.items() if v is not None}


def article_schema(post: BlogPost) -> dict:
    host = canonical_host()
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post.seo_title or post.title,
        "description": post.seo_description or post.excerpt or "",
        "datePublished": post.published_at.isoformat() if post.published_at else None,
        "dateModified": post.updated_at.isoformat() if post.updated_at else None,
        "author": {"@type": "Person", "name": post.author_name or "Talendus"},
        "publisher": {"@type": "Organization", "name": "Talendus", "url": host},
        "mainEntityOfPage": f"{host}/blog/{post.slug}",
        "inLanguage": "fr-CA" if post.lang == "fr" else "en-CA",
        "image": post.cover_image or f"{host}/assets/img/all-images/industry/usine-equipe.jpg",
    }


def robots_txt() -> str:
    host = canonical_host()
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /espace.html",
        "Disallow: /espace-employeur.html",
        "Disallow: /en/account.html",
        "Disallow: /en/account-employer.html",
        "Disallow: /candidate",
        "Disallow: /employer",
        "Disallow: /en/candidate",
        "Disallow: /en/employer",
        "Disallow: /index1.html",
        "Disallow: /index2.html",
        "Disallow: /index3.html",
        "Disallow: /index4.html",
        "Disallow: /index5.html",
        "Disallow: /index6.html",
        "Disallow: /index7.html",
        "Disallow: /index8.html",
        "Disallow: /index9.html",
        "Disallow: /index10.html",
        "Disallow: /projects.html",
        "Disallow: /projects-left.html",
        "Disallow: /projects-right.html",
        "Disallow: /projects-single.html",
        "Disallow: /team.html",
        "Disallow: /testimonial.html",
        "Disallow: /service-left.html",
        "Disallow: /service-right.html",
        f"Sitemap: {host}/sitemap.xml",
        "",
    ]
    return "\n".join(lines)


def _url_entry(loc: str, alternates: list[tuple[str, str]]) -> str:
    links = "".join(
        f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>\n' for lang, href in alternates
    )
    return f"  <url>\n    <loc>{loc}</loc>\n{links}  </url>\n"


def sitemap_xml(db: Session) -> str:
    host = canonical_host()
    chunks = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n',
    ]
    seen_locs: set[str] = set()

    def add(loc: str, alternates: list[tuple[str, str]]) -> None:
        if loc in seen_locs:
            return
        seen_locs.add(loc)
        chunks.append(_url_entry(loc, alternates))

    extra_fr = []
    for name in SITE_ROOT.glob("emploi-*.html"):
        extra_fr.append((name.name, "en/job-" + name.name[len("emploi-") :]))
    for name in SITE_ROOT.glob("secteur-*.html"):
        extra_fr.append((name.name, "en/sector-" + name.name[len("secteur-") :]))
    for name in SITE_ROOT.glob("article-*.html"):
        extra_fr.append((name.name, "en/" + name.name))
    seen = set()
    pairs = list(STATIC_PAIRS) + extra_fr
    for fr, en in pairs:
        key = (fr, en)
        if key in seen:
            continue
        seen.add(key)
        loc_fr = f"{host}/{fr}" if fr else f"{host}/"
        loc_en = f"{host}/{en}" if en else f"{host}/en/"
        alts = [("fr-CA", loc_fr), ("en-CA", loc_en), ("x-default", loc_fr)]
        add(loc_fr, alts)
        add(loc_en, alts)
    posts = db.scalars(
        select(BlogPost).where(BlogPost.status == BlogStatus.PUBLISHED).order_by(BlogPost.published_at.desc())
    ).all()
    now = utcnow()
    for post in posts:
        if post.scheduled_at:
            scheduled = post.scheduled_at
            if scheduled.tzinfo is None:
                from datetime import timezone as _tz

                scheduled = scheduled.replace(tzinfo=_tz.utc)
            if scheduled > now:
                continue
        loc = f"{host}/blog/{post.slug}"
        add(loc, [("fr-CA" if post.lang == "fr" else "en-CA", loc), ("x-default", loc)])
    jobs = db.scalars(select(JobOffer).where(JobOffer.status == JobStatus.PUBLISHED)).all()
    for job in jobs:
        loc = f"{host}/emploi-{job.slug}.html"
        loc_en = f"{host}/en/job-{job.slug}.html"
        alts = [("fr-CA", loc), ("en-CA", loc_en), ("x-default", loc)]
        add(loc, alts)
        add(loc_en, alts)
    chunks.append("</urlset>\n")
    return "".join(chunks)


def tracking_public_config() -> dict:
    settings = get_settings()
    enabled = bool(settings.tracking_enabled) and settings.app_env != "test"
    ga = (settings.ga_measurement_id or "").strip()
    pixel = (settings.meta_pixel_id or "").strip()
    if not enabled:
        ga, pixel = "", ""
    return {
        "enabled": enabled and bool(ga or pixel),
        "environment": settings.app_env,
        "ga_measurement_id": ga,
        "meta_pixel_id": pixel,
        "consent_required": True,
        "conversions": [
            "generate_lead",
            "contact",
            "submit_application",
            "search",
            "view_content",
        ],
        "ga_notes": "Marquer ces événements comme conversions dans GA4 Admin → Événements.",
    }


def dumps(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
