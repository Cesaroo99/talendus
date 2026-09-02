from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import utcnow
from app.models.identity import uid


class SiteEvent(Base):
    """Hits anonymes du site public (visites et interactions, sans PII)."""

    __tablename__ = "site_events"
    __table_args__ = (
        Index("ix_site_events_created_at", "created_at"),
        Index("ix_site_events_kind_created", "kind", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    kind: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(180), default="/")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
