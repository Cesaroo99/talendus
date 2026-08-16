from datetime import datetime

from sqlalchemy import DateTime, Enum, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import BlogStatus, utcnow
from app.models.identity import uid


class BlogPost(Base):
    __tablename__ = "blog_posts"
    __table_args__ = (Index("ix_blog_posts_lang_status", "lang", "status"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    lang: Mapped[str] = mapped_column(String(8), default="fr", index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(400))
    body: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str | None] = mapped_column(String(80))
    tags: Mapped[str | None] = mapped_column(String(255))
    author_name: Mapped[str | None] = mapped_column(String(120))
    cover_image: Mapped[str | None] = mapped_column(String(500))
    seo_title: Mapped[str | None] = mapped_column(String(180))
    seo_description: Mapped[str | None] = mapped_column(String(320))
    status: Mapped[BlogStatus] = mapped_column(Enum(BlogStatus), default=BlogStatus.DRAFT, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[str | None] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
