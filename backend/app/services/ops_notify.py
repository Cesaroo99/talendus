"""Notifications internes : e-mail, in-app et message, sans prestataire externe."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Company, CompanyMembership, User
from app.models.enums import EmailType, NotificationType, UserRole
from app.rbac import ADMINS
from app.services.email import send_email
from app.services.notifications import notify, portal_href


def frontend() -> str:
    return (get_settings().frontend_url or "https://talendus.ca").rstrip("/")


def absolute_link(user: User | None, section: str, item_id: str | None = None) -> str:
    return f"{frontend()}{portal_href(user, section, item_id)}"


def company_users(db: Session, company_id: str) -> list[User]:
    company = db.get(Company, company_id)
    ids: set[str] = set()
    if company and company.owner_user_id:
        ids.add(company.owner_user_id)
    ids.update(
        db.scalars(select(CompanyMembership.user_id).where(CompanyMembership.company_id == company_id)).all()
    )
    users: list[User] = []
    seen: set[str] = set()
    for uid in ids:
        user = db.get(User, uid)
        if user and user.email and user.email not in seen:
            seen.add(user.email)
            users.append(user)
    if company and company.email and company.email.lower() not in {u.email.lower() for u in users}:
        # Destinataire société sans compte : e-mail seulement via un User factice n'est pas possible.
        pass
    return users


def company_emails(db: Session, company_id: str) -> list[str]:
    emails: list[str] = []
    company = db.get(Company, company_id)
    if company and company.email:
        emails.append(company.email.lower())
    for user in company_users(db, company_id):
        if user.email and user.email.lower() not in emails:
            emails.append(user.email.lower())
    return emails


def first_staff(db: Session) -> User | None:
    return db.scalar(
        select(User)
        .where(User.role.in_({UserRole.RECRUITER, UserRole.FINANCE} | ADMINS), User.is_active.is_(True))
        .order_by(User.created_at.asc())
    )


def _as_users(recipients: User | list[User | None] | None) -> list[User]:
    if recipients is None:
        return []
    rows = recipients if isinstance(recipients, list) else [recipients]
    out: list[User] = []
    seen: set[str] = set()
    for user in rows:
        if user and user.id not in seen:
            seen.add(user.id)
            out.append(user)
    return out


def notify_people(
    db: Session,
    recipients: User | list[User | None] | None,
    *,
    actor: User | None,
    ntype: NotificationType,
    title: str,
    message: str,
    section: str,
    template: str,
    email_type: EmailType,
    ctx: dict[str, str] | None = None,
    item_id: str | None = None,
    application_id: str | None = None,
    thread: bool = True,
    already_notified: bool = False,
) -> None:
    """In-app + e-mail info@ + copie dans le fil avec l'interlocuteur."""
    from app.services.messages import post_thread_note

    users = _as_users(recipients)
    base_ctx = {key: "" if value is None else str(value) for key, value in (ctx or {}).items()}
    thread_sender = actor or first_staff(db)
    for user in users:
        href = portal_href(user, section, item_id)
        link = base_ctx.get("link") or f"{frontend()}{href}"
        if not already_notified:
            notify(db, user, ntype, title, message, href=href)
        if actor and user.id == actor.id:
            continue
        if user.email:
            payload = {"name": user.first_name or "", **base_ctx, "link": link}
            send_email(db, user.email, email_type, template, **payload)
        if thread and thread_sender and thread_sender.id != user.id:
            note = f"{title}\n\n{message}\n\nOuvrir : {link}"
            post_thread_note(db, thread_sender, user, note, application_id)


def notify_company(
    db: Session,
    company_id: str,
    *,
    title: str,
    message: str,
    section: str,
    template: str,
    ctx: dict[str, str],
    item_id: str | None = None,
) -> None:
    users = company_users(db, company_id)
    emails = company_emails(db, company_id)
    mailed: set[str] = set()
    for user in users:
        notify(
            db,
            user,
            NotificationType.ADMIN,
            title,
            message,
            href=portal_href(user, section, item_id),
        )
        if user.email:
            send_email(db, user.email, EmailType.ADMIN, template, **ctx)
            mailed.add(user.email.lower())
    for email in emails:
        if email not in mailed:
            send_email(db, email, EmailType.ADMIN, template, **ctx)


def message_company(db: Session, actor: User, company_id: str, body: str) -> None:
    from app.errors import AppError
    from app.services.messages import send_message

    owner_ids = {u.id for u in company_users(db, company_id) if u.id != actor.id and u.role == UserRole.EMPLOYER}
    for uid in owner_ids:
        try:
            send_message(db, actor, uid, body, None, None, email=False)
        except AppError:
            continue
