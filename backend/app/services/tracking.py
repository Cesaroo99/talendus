from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Application, Candidate, Interview, Message, User
from app.models.analytics import SiteEvent
from app.models.enums import utcnow
from app.models.ops import Invoice

ALLOWED_KINDS = {
    "page_view",
    "interaction",
    "contact",
    "apply",
    "search",
    "view_content",
    "generate_lead",
}
KIND_ALIASES = {
    "submit_application": "apply",
    "pageview": "page_view",
    "lead": "generate_lead",
}

PERIOD_DAYS = {
    "jour": 1,
    "semaine": 7,
    "mois": 30,
    "trimestre": 90,
    "annee": 365,
}


def record_hit(db: Session, kind: str, path: str) -> None:
    key = (kind or "page_view").strip().lower().replace("-", "_")
    key = KIND_ALIASES.get(key, key)
    if key not in ALLOWED_KINDS:
        key = "interaction"
    raw_path = (path or "/").strip() or "/"
    if len(raw_path) > 180:
        raw_path = raw_path[:180]
    if not raw_path.startswith("/"):
        raw_path = "/" + raw_path
    db.add(SiteEvent(kind=key, path=raw_path))
    db.commit()


def _since(period: str):
    days = PERIOD_DAYS.get(period or "mois", 30)
    return utcnow() - timedelta(days=days)


def analytics_snapshot(db: Session, period: str = "mois") -> dict:
    if period not in PERIOD_DAYS:
        raise AppError(400, "Période invalide.", "VALIDATION_ERROR")
    since = _since(period)

    def count_since(model, column):
        return int(db.scalar(select(func.count()).select_from(model).where(column >= since)) or 0)

    visits = int(
        db.scalar(
            select(func.count()).select_from(SiteEvent).where(SiteEvent.kind == "page_view", SiteEvent.created_at >= since)
        )
        or 0
    )
    interactions = int(
        db.scalar(
            select(func.count())
            .select_from(SiteEvent)
            .where(SiteEvent.kind != "page_view", SiteEvent.created_at >= since)
        )
        or 0
    )
    by_kind_rows = db.execute(
        select(SiteEvent.kind, func.count())
        .where(SiteEvent.created_at >= since)
        .group_by(SiteEvent.kind)
    ).all()
    by_kind = {kind: int(n) for kind, n in by_kind_rows}
    top_pages = [
        {"path": path, "views": int(n)}
        for path, n in db.execute(
            select(SiteEvent.path, func.count())
            .where(SiteEvent.kind == "page_view", SiteEvent.created_at >= since)
            .group_by(SiteEvent.path)
            .order_by(func.count().desc())
            .limit(8)
        ).all()
    ]
    day_expr = func.date(SiteEvent.created_at)
    daily = [
        {"day": str(day), "visits": int(n)}
        for day, n in db.execute(
            select(day_expr, func.count())
            .where(SiteEvent.kind == "page_view", SiteEvent.created_at >= since)
            .group_by(day_expr)
            .order_by(day_expr.asc())
        ).all()
        if day
    ]
    paid = int(
        db.scalar(
            select(func.coalesce(func.sum(Invoice.amount), 0)).where(
                Invoice.paid_at.is_not(None),
                Invoice.paid_at >= since.date().isoformat(),
            )
        )
        or 0
    )
    return {
        "period": period,
        "since": since.isoformat(),
        "visits": visits,
        "interactions": interactions,
        "contacts": by_kind.get("contact", 0) + by_kind.get("generate_lead", 0),
        "applies": by_kind.get("apply", 0),
        "searches": by_kind.get("search", 0),
        "content_views": by_kind.get("view_content", 0),
        "by_kind": by_kind,
        "top_pages": top_pages,
        "daily": daily,
        "new_candidates": count_since(Candidate, Candidate.created_at),
        "new_applications": count_since(Application, Application.created_at),
        "interviews": count_since(Interview, Interview.created_at),
        "messages": count_since(Message, Message.created_at),
        "new_users": count_since(User, User.created_at),
        "revenue_paid": paid,
    }
