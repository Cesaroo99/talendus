"""Rattache un compte employeur à la fiche admin déjà créée (veille / prospection)."""

from __future__ import annotations

import re
import unicodedata
from urllib.parse import urlparse

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Company, CompanyMembership, User
from app.models.enums import CompanyMemberRole, CompanyStatus
from app.models.prospect import Prospect

EARLY_STAGES = frozenset({"nouveau", "a-contacter", "contacte"})
PUBLIC_MAIL_DOMAINS = frozenset(
    {
        "gmail.com",
        "googlemail.com",
        "hotmail.com",
        "hotmail.ca",
        "outlook.com",
        "outlook.fr",
        "live.com",
        "live.ca",
        "msn.com",
        "yahoo.com",
        "yahoo.ca",
        "yahoo.fr",
        "icloud.com",
        "me.com",
        "mac.com",
        "proton.me",
        "protonmail.com",
        "bell.net",
        "videotron.ca",
        "sympatico.ca",
        "icloud.ca",
    }
)
_LEGAL_SUFFIXES = re.compile(
    r"\b("
    r"inc|incorporated|ltd|ltee|ltée|limited|limitee|limitée|"
    r"corp|corporation|cie|co|company|compagnie|"
    r"s\.?e\.?c\.?|s\.?e\.?n\.?c\.?|sencrl|senc|sec|"
    r"s\.?a\.?|sarl|llc"
    r")\b",
    re.IGNORECASE,
)


def normalize_company_name(name: str | None) -> str:
    text = unicodedata.normalize("NFKD", name or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = _LEGAL_SUFFIXES.sub(" ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _email_domain(email: str | None) -> str:
    value = (email or "").strip().lower()
    if "@" not in value:
        return ""
    return value.rsplit("@", 1)[-1]


def _host_from_website(website: str | None) -> str:
    raw = (website or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def company_domains(company: Company) -> set[str]:
    found = set()
    domain = _email_domain(company.email)
    if domain:
        found.add(domain)
    host = _host_from_website(company.website)
    if host:
        found.add(host)
    return {item for item in found if item and item not in PUBLIC_MAIL_DOMAINS}


def _is_unclaimed(company: Company | None) -> bool:
    return company is not None and not company.owner_user_id


def _name_keys(company: Company) -> set[str]:
    return {
        key
        for key in (
            normalize_company_name(company.name),
            normalize_company_name(company.legal_name),
            normalize_company_name(company.trade_name),
        )
        if key
    }


def find_unclaimed_employer_company(
    db: Session,
    *,
    email: str,
    company_name: str = "",
) -> Company | None:
    """Trouve la fiche veille à rattacher. Jamais une société déjà possédée."""
    email = (email or "").strip().lower()
    if email:
        by_email = db.scalar(
            select(Company).where(
                Company.owner_user_id.is_(None),
                func.lower(Company.email) == email,
            )
        )
        if by_email:
            return by_email
        prospect = db.scalar(select(Prospect).where(Prospect.side == "employer", Prospect.email == email))
        if prospect and prospect.company_id:
            linked = db.get(Company, prospect.company_id)
            if _is_unclaimed(linked):
                return linked

    wanted = normalize_company_name(company_name)
    if len(wanted) < 4:
        return None
    user_domain = _email_domain(email)
    unclaimed = list(db.scalars(select(Company).where(Company.owner_user_id.is_(None))).all())
    named = [row for row in unclaimed if wanted in _name_keys(row)]
    if not named:
        return None
    if user_domain and user_domain not in PUBLIC_MAIL_DOMAINS:
        domain_hits = [row for row in named if user_domain in company_domains(row)]
        if len(domain_hits) == 1:
            return domain_hits[0]
        if len(domain_hits) > 1:
            return None
    prospects = [row for row in named if row.status == CompanyStatus.PROSPECT]
    if len(prospects) == 1:
        return prospects[0]
    if len(named) == 1 and named[0].status == CompanyStatus.PROSPECT:
        return named[0]
    return None


def _ensure_owner_membership(db: Session, company: Company, user: User) -> None:
    already = db.scalar(
        select(CompanyMembership.id).where(
            CompanyMembership.company_id == company.id,
            CompanyMembership.user_id == user.id,
        )
    )
    if already:
        return
    db.add(CompanyMembership(company_id=company.id, user_id=user.id, member_role=CompanyMemberRole.OWNER))


def attach_user_to_company_prospects(db: Session, user: User, company: Company) -> None:
    rows = list(
        db.scalars(
            select(Prospect).where(
                Prospect.side == "employer",
                Prospect.company_id == company.id,
            )
        ).all()
    )
    by_email = db.scalar(select(Prospect).where(Prospect.side == "employer", Prospect.email == user.email))
    if by_email and by_email not in rows:
        rows.append(by_email)
    for row in rows:
        if not row.user_id:
            row.user_id = user.id
        if not row.company_id:
            row.company_id = company.id
        if row.stage in EARLY_STAGES:
            row.stage = "qualifie"
        if not (row.first_name or "").strip() and (user.first_name or "").strip():
            row.first_name = user.first_name.strip()[:80]
            row.last_name = (user.last_name or "").strip()[:80]


def claim_employer_company(db: Session, user: User, company: Company) -> Company:
    values = {"owner_user_id": user.id}
    if user.full_name:
        values["contact_name"] = user.full_name
    if not company.email:
        values["email"] = user.email
    if not company.phone and user.phone:
        values["phone"] = user.phone
    result = db.execute(
        update(Company)
        .where(Company.id == company.id, Company.owner_user_id.is_(None))
        .values(**values)
    )
    if int(result.rowcount or 0) != 1:
        raise AppError(409, "Cette fiche entreprise a déjà un titulaire.", "COMPANY_ALREADY_CLAIMED")
    db.refresh(company)
    _ensure_owner_membership(db, company, user)
    attach_user_to_company_prospects(db, user, company)
    from app.services.audit import audit

    audit(db, "company.claim", user, "company", company.id, metadata={"source": "inscription"})
    return company


def _create_employer_company(db: Session, user: User, company_name: str) -> Company:
    name = (company_name or "").strip() or f"{user.last_name} Inc."
    company = Company(
        name=name,
        legal_name=name,
        trade_name=name,
        owner_user_id=user.id,
        contact_name=user.full_name,
        email=user.email,
        province="Québec",
        country="Canada",
    )
    db.add(company)
    db.flush()
    _ensure_owner_membership(db, company, user)
    return company


def claim_or_create_employer_company(db: Session, user: User, company_name: str | None = "") -> Company:
    existing = db.scalar(select(Company).where(Company.owner_user_id == user.id))
    if existing:
        _ensure_owner_membership(db, existing, user)
        attach_user_to_company_prospects(db, user, existing)
        return existing
    offered = (company_name or "").strip()
    claimed = find_unclaimed_employer_company(db, email=user.email, company_name=offered)
    if claimed:
        try:
            return claim_employer_company(db, user, claimed)
        except AppError as exc:
            if getattr(exc, "code", "") != "COMPANY_ALREADY_CLAIMED":
                raise
    return _create_employer_company(db, user, offered)
