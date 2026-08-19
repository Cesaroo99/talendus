"""Routes site : robots, sitemap, articles HTML, config tracking publique, portails."""

from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.errors import AppError, ok
from app.services import blog as blog_svc
from app.services.job_pages import render_job_html, static_job_path
from app.services.jobs import get_public_job
from app.services.seo import robots_txt, sitemap_xml, tracking_public_config

router = APIRouter(tags=["site"])
SITE_ROOT = Path(__file__).resolve().parents[3]
PORTAL_HEADERS = {"X-Robots-Tag": "noindex, nofollow", "Cache-Control": "no-store"}


def _portal_page(relative: str):
    path = SITE_ROOT / relative
    if not path.exists():
        raise AppError(404, "Page introuvable.", "NOT_FOUND")
    return FileResponse(path, media_type="text/html; charset=utf-8", headers=PORTAL_HEADERS)


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    for name in ("icon-192.png", "apple-touch-icon.png", "fav-logo1.png"):
        icon = SITE_ROOT / "assets" / "img" / "logo" / name
        if icon.exists():
            return FileResponse(icon, media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})
    raise AppError(404, "Page introuvable.", "NOT_FOUND")


@router.get("/manifest.webmanifest", include_in_schema=False)
def web_manifest():
    path = SITE_ROOT / "manifest.webmanifest"
    if not path.exists():
        raise AppError(404, "Page introuvable.", "NOT_FOUND")
    return FileResponse(
        path,
        media_type="application/manifest+json",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/sw.js", include_in_schema=False)
def service_worker():
    path = SITE_ROOT / "sw.js"
    if not path.exists():
        raise AppError(404, "Page introuvable.", "NOT_FOUND")
    return FileResponse(
        path,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"},
    )


def _install_file(name: str, media_type: str, download_name: str):
    path = SITE_ROOT / "assets" / "app" / name
    if not path.exists():
        raise AppError(404, "Fichier d'installation introuvable.", "NOT_FOUND")
    return FileResponse(
        path,
        media_type=media_type,
        filename=download_name,
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/download/talendus.apk", include_in_schema=False)
@router.get("/assets/app/talendus.apk", include_in_schema=False)
def android_app_package():
    return _install_file(
        "talendus.apk",
        "application/vnd.android.package-archive",
        "Talendus.apk",
    )


@router.get("/download/talendus.mobileconfig", include_in_schema=False)
@router.get("/assets/app/talendus.mobileconfig", include_in_schema=False)
def ios_home_screen_profile():
    return _install_file(
        "talendus.mobileconfig",
        "application/x-apple-aspen-config",
        "Talendus.mobileconfig",
    )


@router.get("/robots.txt", include_in_schema=False)
def robots():
    return PlainTextResponse(robots_txt(), media_type="text/plain; charset=utf-8")


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap(db: Session = Depends(get_db)):
    try:
        xml = sitemap_xml(db)
    except Exception:
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<url><loc>https://talendus.ca/</loc></url></urlset>"
        )
    return Response(
        content=xml,
        media_type="application/xml; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/google{token}.html", include_in_schema=False)
def google_site_verification(token: str):
    expected = (get_settings().google_site_verification or "").strip()
    if not expected or token != expected or not token.replace("_", "").replace("-", "").isalnum():
        raise AppError(404, "Page introuvable.", "NOT_FOUND")
    return PlainTextResponse(
        f"google-site-verification: {expected}\n",
        media_type="text/html; charset=utf-8",
        headers={"X-Robots-Tag": "noindex, nofollow", "Cache-Control": "public, max-age=300"},
    )


@router.get("/api/tracking/config")
def tracking_config():
    return ok(tracking_public_config())


@router.get("/candidate", include_in_schema=False)
@router.get("/candidate/{rest:path}", include_in_schema=False)
def candidate_portal(rest: str = ""):
    return _portal_page("espace.html")


@router.get("/employer", include_in_schema=False)
@router.get("/employer/{rest:path}", include_in_schema=False)
def employer_portal(rest: str = ""):
    return _portal_page("espace-employeur.html")


@router.get("/en/candidate", include_in_schema=False)
@router.get("/en/candidate/{rest:path}", include_in_schema=False)
def candidate_portal_en(rest: str = ""):
    return _portal_page("en/account.html")


@router.get("/en/employer", include_in_schema=False)
@router.get("/en/employer/{rest:path}", include_in_schema=False)
def employer_portal_en(rest: str = ""):
    return _portal_page("en/account-employer.html")


@router.get("/m.html", include_in_schema=False)
def mobile_app_fr():
    return _portal_page("m.html")


@router.get("/en/m.html", include_in_schema=False)
def mobile_app_en():
    return _portal_page("en/m.html")


@router.get("/blog/{slug}", include_in_schema=False)
def blog_html(slug: str, db: Session = Depends(get_db)):
    try:
        post = blog_svc.get_public(db, slug)
    except AppError:
        raise
    html = blog_svc.render_post_html(post)
    return HTMLResponse(html)


@router.get("/emploi-{slug}.html", include_in_schema=False)
def job_html_fr(slug: str, db: Session = Depends(get_db)):
    static = static_job_path(slug, "fr")
    if static.exists():
        return FileResponse(static, media_type="text/html; charset=utf-8")
    job = get_public_job(db, slug)
    return HTMLResponse(render_job_html(job, "fr"))


@router.get("/en/job-{slug}.html", include_in_schema=False)
def job_html_en(slug: str, db: Session = Depends(get_db)):
    static = static_job_path(slug, "en")
    if static.exists():
        return FileResponse(static, media_type="text/html; charset=utf-8")
    job = get_public_job(db, slug)
    return HTMLResponse(render_job_html(job, "en"))
