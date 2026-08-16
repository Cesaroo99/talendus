"""Routes site : robots, sitemap, articles HTML, config tracking publique."""

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import AppError, ok
from app.services import blog as blog_svc
from app.services.seo import robots_txt, sitemap_xml, tracking_public_config

router = APIRouter(tags=["site"])


@router.get("/robots.txt", include_in_schema=False)
def robots():
    return PlainTextResponse(robots_txt(), media_type="text/plain; charset=utf-8")


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap(db: Session = Depends(get_db)):
    xml = sitemap_xml(db)
    return Response(
        content=xml,
        media_type="application/xml; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/api/tracking/config")
def tracking_config():
    return ok(tracking_public_config())


@router.get("/blog/{slug}", include_in_schema=False)
def blog_html(slug: str, db: Session = Depends(get_db)):
    try:
        post = blog_svc.get_public(db, slug)
    except AppError:
        raise
    html = blog_svc.render_post_html(post)
    return HTMLResponse(html)
