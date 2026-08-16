from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.errors import ok
from app.models import User
from app.models.enums import UserRole
from app.services import blog as blog_svc

router = APIRouter(tags=["blog"])
admin_router = APIRouter(prefix="/admin/blog", tags=["admin-blog"])


class BlogIn(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    slug: str | None = Field(default=None, max_length=160)
    lang: str = Field(default="fr", max_length=8)
    excerpt: str | None = Field(default=None, max_length=400)
    body: str = ""
    category: str | None = Field(default=None, max_length=80)
    tags: str | None = Field(default=None, max_length=255)
    author_name: str | None = Field(default=None, max_length=120)
    cover_image: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=180)
    seo_description: str | None = Field(default=None, max_length=320)
    status: str = "DRAFT"
    scheduled_at: datetime | None = None


class BlogPatch(BaseModel):
    title: str | None = Field(default=None, max_length=180)
    slug: str | None = Field(default=None, max_length=160)
    lang: str | None = Field(default=None, max_length=8)
    excerpt: str | None = Field(default=None, max_length=400)
    body: str | None = None
    category: str | None = Field(default=None, max_length=80)
    tags: str | None = Field(default=None, max_length=255)
    author_name: str | None = Field(default=None, max_length=120)
    cover_image: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=180)
    seo_description: str | None = Field(default=None, max_length=320)
    status: str | None = None
    scheduled_at: datetime | None = None


_editor = require_roles(UserRole.EDITOR, UserRole.ADMIN, UserRole.RECRUITER)


@router.get("/blog")
def public_list(lang: str | None = Query(default=None), db: Session = Depends(get_db)):
    posts = blog_svc.list_public(db, lang=lang)
    return ok([blog_svc.serialize(p) for p in posts])


@router.get("/blog/{slug}")
def public_detail(slug: str, db: Session = Depends(get_db)):
    post = blog_svc.get_public(db, slug)
    return ok(blog_svc.serialize(post))


@admin_router.get("")
def staff_list(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(_editor),
):
    posts = blog_svc.list_staff(db, status=status.upper() if status else None)
    return ok([blog_svc.serialize(p, public=False) for p in posts])


@admin_router.post("")
def staff_create(payload: BlogIn, db: Session = Depends(get_db), user: User = Depends(_editor)):
    post = blog_svc.create_post(db, user, payload)
    db.commit()
    db.refresh(post)
    return ok(blog_svc.serialize(post, public=False), message="Article enregistré.")


@admin_router.get("/{post_id}")
def staff_get(post_id: str, db: Session = Depends(get_db), _: User = Depends(_editor)):
    return ok(blog_svc.serialize(blog_svc.get_staff(db, post_id), public=False))


@admin_router.patch("/{post_id}")
def staff_update(
    post_id: str,
    payload: BlogPatch,
    db: Session = Depends(get_db),
    _: User = Depends(_editor),
):
    post = blog_svc.update_post(db, blog_svc.get_staff(db, post_id), payload)
    db.commit()
    db.refresh(post)
    return ok(blog_svc.serialize(post, public=False), message="Article mis à jour.")
