"""CMS blog : brouillons, publication, programmation, archivage."""

from __future__ import annotations

import html
import re
import unicodedata
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models.cms import BlogPost
from app.models.enums import BlogStatus, utcnow
from app.models.identity import User
from app.services.seo import article_schema

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    slug = _SLUG_RE.sub("-", normalized.lower()).strip("-")
    return (slug or "article")[:150]


def unique_slug(db: Session, base: str, ignore_id: str | None = None) -> str:
    slug = slugify(base)
    candidate = slug
    n = 2
    while True:
        q = select(BlogPost).where(BlogPost.slug == candidate)
        if ignore_id:
            q = q.where(BlogPost.id != ignore_id)
        if db.scalar(q) is None:
            return candidate
        candidate = f"{slug}-{n}"[:160]
        n += 1


def publish_due(db: Session) -> int:
    now = utcnow()
    rows = db.scalars(select(BlogPost).where(BlogPost.status == BlogStatus.SCHEDULED)).all()
    changed = 0
    for post in rows:
        scheduled = _aware(post.scheduled_at)
        if scheduled and scheduled <= now:
            post.status = BlogStatus.PUBLISHED
            post.published_at = post.published_at or now
            changed += 1
    return changed


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def is_public(post: BlogPost) -> bool:
    now = utcnow()
    scheduled = _aware(post.scheduled_at)
    if post.status == BlogStatus.PUBLISHED:
        if scheduled and scheduled > now:
            return False
        return True
    if post.status == BlogStatus.SCHEDULED and scheduled and scheduled <= now:
        return True
    return False


def serialize(post: BlogPost, *, public: bool = True) -> dict:
    payload = {
        "id": post.id,
        "slug": post.slug,
        "lang": post.lang,
        "title": post.title,
        "excerpt": post.excerpt,
        "body": post.body,
        "category": post.category,
        "tags": [t.strip() for t in (post.tags or "").split(",") if t.strip()],
        "author_name": post.author_name,
        "cover_image": post.cover_image,
        "seo_title": post.seo_title,
        "seo_description": post.seo_description,
        "status": post.status.value,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "scheduled_at": post.scheduled_at.isoformat() if post.scheduled_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "url": f"/blog/{post.slug}",
        "schema": article_schema(post),
    }
    if not public:
        payload["created_by"] = post.created_by
        payload["created_at"] = post.created_at.isoformat() if post.created_at else None
    return payload


def list_public(db: Session, lang: str | None = None) -> list[BlogPost]:
    publish_due(db)
    db.flush()
    stmt = select(BlogPost).where(
        or_(
            BlogPost.status == BlogStatus.PUBLISHED,
            BlogPost.status == BlogStatus.SCHEDULED,
        )
    )
    if lang:
        stmt = stmt.where(BlogPost.lang == lang)
    rows = db.scalars(stmt.order_by(BlogPost.published_at.desc(), BlogPost.created_at.desc())).all()
    return [p for p in rows if is_public(p)]


def get_public(db: Session, slug: str) -> BlogPost:
    publish_due(db)
    db.flush()
    post = db.scalar(select(BlogPost).where(BlogPost.slug == slug))
    if not post or not is_public(post):
        raise AppError(404, "Article introuvable.", "NOT_FOUND")
    return post


def list_staff(db: Session, status: str | None = None) -> list[BlogPost]:
    publish_due(db)
    db.flush()
    stmt = select(BlogPost).order_by(BlogPost.updated_at.desc())
    if status:
        stmt = stmt.where(BlogPost.status == BlogStatus(status))
    return list(db.scalars(stmt).all())


def _status(value: str | None, default: BlogStatus = BlogStatus.DRAFT) -> BlogStatus:
    if not value:
        return default
    try:
        return BlogStatus(value.upper())
    except ValueError as exc:
        raise AppError(422, "Statut d'article invalide.", "VALIDATION_ERROR") from exc


def create_post(db: Session, user: User, data) -> BlogPost:
    status = _status(getattr(data, "status", None))
    slug = unique_slug(db, getattr(data, "slug", None) or data.title)
    now = utcnow()
    post = BlogPost(
        slug=slug,
        lang=getattr(data, "lang", None) or "fr",
        title=data.title.strip(),
        excerpt=(getattr(data, "excerpt", None) or "")[:400] or None,
        body=getattr(data, "body", None) or "",
        category=getattr(data, "category", None),
        tags=getattr(data, "tags", None),
        author_name=getattr(data, "author_name", None) or f"{user.first_name} {user.last_name}".strip(),
        cover_image=getattr(data, "cover_image", None),
        seo_title=getattr(data, "seo_title", None),
        seo_description=getattr(data, "seo_description", None),
        status=status,
        scheduled_at=getattr(data, "scheduled_at", None),
        created_by=user.id,
    )
    if status == BlogStatus.PUBLISHED:
        post.published_at = getattr(data, "published_at", None) or now
    db.add(post)
    db.flush()
    return post


def update_post(db: Session, post: BlogPost, data) -> BlogPost:
    fields = [
        "title",
        "excerpt",
        "body",
        "category",
        "tags",
        "author_name",
        "cover_image",
        "seo_title",
        "seo_description",
        "lang",
        "scheduled_at",
    ]
    for name in fields:
        if getattr(data, name, None) is not None:
            setattr(post, name, getattr(data, name))
    if getattr(data, "slug", None):
        post.slug = unique_slug(db, data.slug, ignore_id=post.id)
    if getattr(data, "status", None):
        status = _status(data.status, post.status)
        post.status = status
        if status == BlogStatus.PUBLISHED and not post.published_at:
            post.published_at = utcnow()
        if status == BlogStatus.ARCHIVED:
            pass
    post.updated_at = utcnow()
    db.flush()
    return post


def get_staff(db: Session, post_id: str) -> BlogPost:
    post = db.get(BlogPost, post_id)
    if not post:
        raise AppError(404, "Article introuvable.", "NOT_FOUND")
    return post


def body_to_html(text: str) -> str:
    raw = text or ""
    if "<p" in raw.lower() or "<h2" in raw.lower() or "<ul" in raw.lower():
        return raw
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    if not blocks:
        return ""
    return "".join(f"<p>{html.escape(b).replace(chr(10), '<br>')}</p>" for b in blocks)


def render_post_html(post: BlogPost) -> str:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    scripts = str(root / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from parts import wrap, page_hero  # noqa: WPS433

    title = post.seo_title or f"{post.title} | Blog Talendus"
    desc = post.seo_description or post.excerpt or post.title
    cover = post.cover_image or "assets/img/all-images/industry/usine-equipe.jpg"
    if cover.startswith("/"):
        cover = cover.lstrip("/")
    lang = "en" if post.lang == "en" else "fr"
    slug_path = f"blog/{post.slug}"
    img_html = (
        f'<img src="/{html.escape(cover)}" alt="{html.escape(post.title)}" '
        'style="width:100%;border-radius:16px;margin-bottom:24px" loading="lazy" decoding="async">'
    )
    tags = ", ".join(t.strip() for t in (post.tags or "").split(",") if t.strip())
    cta = (
        '<a class="tl-btn" href="/contact.html">Parler à un spécialiste</a>'
        '<a class="tl-btn tl-btn-ghost-dark" href="/blog.html">Retour au blog</a>'
        if lang == "fr"
        else '<a class="tl-btn" href="/en/contact.html">Talk to a specialist</a>'
        '<a class="tl-btn tl-btn-ghost-dark" href="/en/blog.html">Back to the blog</a>'
    )
    related = (
        '<p><a href="/secteurs.html">Tous les secteurs</a> · '
        '<a href="/emplois.html">Offres d’emploi</a> · '
        '<a href="/entreprises.html">Solutions entreprises</a></p>'
        if lang == "fr"
        else '<p><a href="/en/sectors.html">Every industry</a> · '
        '<a href="/en/jobs.html">Job openings</a> · '
        '<a href="/en/employers.html">Employer solutions</a></p>'
    )
    body = (
        page_hero(post.category or ("Blog" if lang == "fr" else "Insights"), post.title, post.excerpt or "")
        + f"""
        <section class="tl-section"><div class="container" style="max-width:800px">
          {img_html}
          <p class="tl-muted">{html.escape(post.author_name or "Talendus")}</p>
          {body_to_html(post.body)}
          {"<p class='tl-muted'>Tags : " + html.escape(tags) + "</p>" if tags else ""}
          {related}
          <div class="tl-actions" style="margin-top:28px">{cta}</div>
        </div></section>
        """
    )
    return wrap(
        title,
        desc,
        slug_path,
        body,
        lang=lang,
        alt="en/blog.html" if lang == "fr" else "blog.html",
        robots="index,follow",
        og_type="article",
        og_image=cover if cover.startswith("http") else f"/{cover}",
        extra_json_ld=article_schema(post),
    )
