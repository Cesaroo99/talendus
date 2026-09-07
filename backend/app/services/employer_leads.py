"""Importe les employeurs québécois recherchés : fiche client + prospect CRM."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from urllib.parse import urlparse

from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.models import Company, InternalNote, User
from app.models.enums import CompanyStatus, UserRole
from app.models.prospect import Prospect
from app.services.employer_claim import normalize_company_name
from app.services.prospects import person_name_parts, sanitize_generic_person, upsert_prospect

logger = logging.getLogger("talendus.employer_leads")

LEAD_NOTE_MARK = "Veille Talendus — employeur à démarcher"


def _size_label(employees: int | None) -> str | None:
    if not employees:
        return None
    return "PME" if employees < 200 else "Grande entreprise"


def _staff_user(db: Session) -> User | None:
    return db.scalar(
        select(User).where(
            User.is_active.is_(True),
            User.role.in_([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.RECRUITER]),
        ).order_by(User.created_at.asc())
    )


def _recruiters(db: Session) -> list[User]:
    rows = list(
        db.scalars(
            select(User).where(
                User.is_active.is_(True),
                User.role == UserRole.RECRUITER,
            ).order_by(User.created_at.asc())
        ).all()
    )
    if rows:
        return rows
    staff = _staff_user(db)
    return [staff] if staff else []


def _host_of(url: str | None) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def _company_name_index(db: Session) -> dict[str, Company]:
    index: dict[str, Company] = {}
    for row in db.scalars(select(Company)).all():
        raw = (row.name or "").strip()
        if raw:
            index[raw] = row
            index[raw.casefold()] = row
            key = normalize_company_name(raw)
            if key:
                index[f"n:{key}"] = row
        legal = normalize_company_name(row.legal_name)
        if legal:
            index[f"n:{legal}"] = row
        trade = normalize_company_name(row.trade_name)
        if trade:
            index[f"n:{trade}"] = row
        host = _host_of(row.website)
        if host:
            index[f"h:{host}"] = row
    return index


def _index_company(index: dict[str, Company], company: Company) -> None:
    raw = (company.name or "").strip()
    if raw:
        index[raw] = company
        index[raw.casefold()] = company
        key = normalize_company_name(raw)
        if key:
            index[f"n:{key}"] = company
    host = _host_of(company.website)
    if host:
        index[f"h:{host}"] = company


def _names_similar(left: str | None, right: str | None) -> bool:
    a = normalize_company_name(left)
    b = normalize_company_name(right)
    if not a or not b:
        return False
    if a == b:
        return True
    # Sous-chaîne seulement si le nom est assez long : « ad » ⊂ « admin »
    # fusionnerait la fiche d’inscription « Admin Inc. » avec un lead.
    if min(len(a), len(b)) >= 8 and (a in b or b in a):
        return True
    ta, tb = set(a.split()), set(b.split())
    return bool(ta and tb) and len(ta & tb) / len(ta | tb) >= 0.75


def _forget_session_prospects(db: Session) -> None:
    """Oublie les Prospect déjà dans la session (souvent issus d’une autre requête).

    Un flush global tenterait un UPDATE de ces lignes ; avec SQLite StaticPool
    + sessions HTTP mélangées, la ligne peut ne plus matcher (StaleDataError).
    """
    for obj in list(db.identity_map.values()) + list(db.new):
        if isinstance(obj, Prospect):
            db.expunge(obj)


def _same_company(lead: dict[str, Any], company: Company) -> bool:
    return _names_similar(lead.get("name"), company.name) or _names_similar(
        lead.get("legal_name"), company.legal_name or company.name
    )


def _owned_company_is_this_lead(company: Company, lead: dict[str, Any]) -> bool:
    """Une société déjà titulaire ne fusionne qu’avec le lead du même nom normalisé."""
    if not company.owner_user_id:
        return True
    wanted = normalize_company_name(lead.get("name"))
    legal = normalize_company_name(lead.get("legal_name") or lead.get("name"))
    return wanted in {
        normalize_company_name(company.name),
        normalize_company_name(company.legal_name),
        normalize_company_name(company.trade_name),
    } or legal in {
        normalize_company_name(company.name),
        normalize_company_name(company.legal_name),
        normalize_company_name(company.trade_name),
    }


def _find_company(db: Session, lead: dict[str, Any], index: dict[str, Company] | None = None) -> Company | None:
    name = (lead.get("name") or "").strip()
    if not name:
        return None
    if index is not None:
        found = index.get(name) or index.get(name.casefold())
        if found:
            return found
        key = normalize_company_name(name)
        if key and index.get(f"n:{key}"):
            return index[f"n:{key}"]
        legal = normalize_company_name(lead.get("legal_name"))
        if legal and index.get(f"n:{legal}"):
            return index[f"n:{legal}"]
        host = _host_of(lead.get("website"))
        candidate = index.get(f"h:{host}") if host else None
        if candidate and _same_company(lead, candidate):
            return candidate
        return None
    exact = db.scalar(select(Company).where(Company.name == name))
    if exact:
        return exact
    wanted = normalize_company_name(name)
    host = _host_of(lead.get("website"))
    for row in db.scalars(select(Company)).all():
        if normalize_company_name(row.name) == wanted:
            return row
        if host and _host_of(row.website) == host and _same_company(lead, row):
            return row
    return None


def _fill_empty(company: Company, **values: Any) -> None:
    for key, value in values.items():
        if value in (None, ""):
            continue
        current = getattr(company, key)
        if current in (None, "", 0):
            setattr(company, key, value)


def _note_text(lead: dict[str, Any]) -> str:
    jobs = lead.get("hiring") or ""
    careers = lead.get("careers_url") or lead.get("website") or ""
    score = lead.get("lead_score")
    priority = lead.get("lead_priority")
    source = lead.get("source") or "veille publique"
    score_line = f"Score : {score} ({priority}).\n" if score else ""
    email_src = lead.get("email_source")
    confidence = lead.get("email_confidence")
    if lead.get("email"):
        email_line = f"Courriel public : {lead.get('email')} — source {email_src}"
        if confidence:
            email_line += f" ({confidence})"
        if lead.get("email_source_url"):
            email_line += f" {lead.get('email_source_url')}"
        email_line += ".\n"
    else:
        email_line = "Courriel : non publié (laissé vide).\n"
    return (
        f"{LEAD_NOTE_MARK}.\n"
        f"{score_line}"
        f"Signal : {jobs}\n"
        f"Carrières : {careers}\n"
        f"Source : {source}\n"
        f"{email_line}"
        "Critères : établissement québécois, une seule fiche par groupe, "
        "aucune donnée inventée (courriel uniquement s’il est publié)."
    )


def _ensure_note(db: Session, company: Company, author: User | None, lead: dict[str, Any]) -> None:
    if not author:
        return
    existing = db.scalar(
        select(InternalNote).where(
            InternalNote.entity_type == "company",
            InternalNote.entity_id == company.id,
            InternalNote.text.like(f"{LEAD_NOTE_MARK}%"),
        )
    )
    text = _note_text(lead)[:4000]
    if existing is None:
        db.add(
            InternalNote(
                entity_type="company",
                entity_id=company.id,
                author_id=author.id,
                text=text,
            )
        )
        return
    previous = existing.text or ""
    email = (lead.get("email") or "").strip()
    if email and "Courriel : non publié" in previous and email not in previous:
        journal = (
            f"\nJournal 2026-09-07 : courriel ajouté {email} "
            f"(avant vide, source {lead.get('email_source') or 'recherche publique'})."
        )
        existing.text = (text + journal)[:4000]


def _ensure_prospect(db: Session, company: Company, lead: dict[str, Any], recruiter: User | None) -> None:
    email = (lead.get("email") or "").strip()
    if not email or "@" not in email:
        return
    first, last = person_name_parts(lead.get("contact_name") or "")
    hiring = (lead.get("hiring") or "")[:5000]
    detail = (lead.get("hiring") or lead.get("careers_url") or "")[:240]
    existing = db.scalar(select(Prospect.id).where(Prospect.side == "employer", Prospect.email == email.lower()))
    row = upsert_prospect(
        db,
        side="employer",
        email=email,
        source="prospection",
        first_name=first,
        last_name=last,
        phone=lead.get("phone") or "",
        company_name=company.name,
        title=lead.get("contact_title") or "Ressources humaines",
        city=company.city or "",
        sector=company.sector or "",
        source_detail=detail,
        message=hiring,
        company_id=company.id,
        assigned_recruiter_id=recruiter.id if recruiter else None,
        stage="a-contacter" if existing is None else None,
    )
    if row is not None:
        sanitize_generic_person(row)
        db.flush()
        db.expunge(row)


def catalog_emails() -> set[str]:
    return {
        (lead.get("email") or "").strip().lower()
        for lead in QUEBEC_EMPLOYER_LEADS
        if (lead.get("email") or "").strip() and "@" in (lead.get("email") or "")
    }


def catalog_stats(db: Session) -> dict[str, int]:
    emails = catalog_emails()
    company_emails = {
        (value or "").strip().lower()
        for value in db.scalars(select(Company.email)).all()
        if (value or "").strip()
    }
    prospect_emails = {
        (value or "").strip().lower()
        for value in db.scalars(select(Prospect.email).where(Prospect.side == "employer")).all()
        if (value or "").strip()
    }
    return {
        "catalog": len(QUEBEC_EMPLOYER_LEADS),
        "catalog_with_email": len(emails),
        "companies": int(db.scalar(select(func.count()).select_from(Company)) or 0),
        "companies_with_catalog_email": len(emails & company_emails),
        "prospects_with_catalog_email": len(emails & prospect_emails),
        "missing_company_emails": len(emails - company_emails),
        "missing_prospects": len(emails - prospect_emails),
    }


def refresh_employer_directory(db: Session, *, force: bool = False) -> dict[str, int | bool]:
    """Crée les fiches manquantes et recopie les courriels publics. Idempotent."""
    stats = catalog_stats(db)
    need = force or stats["missing_prospects"] > 5 or stats["missing_company_emails"] > 5
    if need:
        ensure_quebec_employer_leads(db)
    else:
        sync_catalog_emails_to_crm(db)
    out: dict[str, int | bool] = dict(catalog_stats(db))
    out["imported"] = need
    return out


def sync_catalog_emails_to_crm(db: Session) -> int:
    """Recopie les courriels publics du catalogue sur les fiches déjà en base.

    Ne crée aucune entreprise. N’écrase jamais un courriel déjà présent.
    Crée le prospect employeur dès qu’un courriel public est disponible.
    """
    _forget_session_prospects(db)
    recruiters = _recruiters(db)
    staff = recruiters[0] if recruiters else _staff_user(db)
    names = _company_name_index(db)
    known_emails = {
        (value or "").strip().lower()
        for value in db.scalars(select(Prospect.email).where(Prospect.side == "employer")).all()
        if value
    }
    filled = 0
    for index, lead in enumerate(QUEBEC_EMPLOYER_LEADS):
        email = (lead.get("email") or "").strip()
        if not email or "@" not in email:
            continue
        company = _find_company(db, lead, names)
        if company is None:
            continue
        if company.owner_user_id and not _owned_company_is_this_lead(company, lead):
            continue
        before = (company.email or "").strip()
        if not before:
            _fill_empty(
                company,
                email=email,
                phone=lead.get("phone"),
                contact_name=lead.get("contact_name") or None,
            )
            filled += 1
        current = (company.email or "").strip().lower()
        if current != email.lower():
            continue
        recruiter = recruiters[index % len(recruiters)] if recruiters else None
        email_key = email.lower()
        if email_key not in known_emails:
            _ensure_note(db, company, staff, lead)
            _ensure_prospect(db, company, lead, recruiter)
            known_emails.add(email_key)
    if filled:
        logger.info("%s courriels publics recopiés sur des fiches existantes.", filled)
    return filled


def ensure_quebec_employer_leads(db: Session) -> int:
    """Crée ou complète les fiches de veille. Idempotent. Aucun compte employeur."""
    _forget_session_prospects(db)
    db.expire_all()
    recruiters = _recruiters(db)
    staff = recruiters[0] if recruiters else _staff_user(db)
    names = _company_name_index(db)
    created = 0
    for index, lead in enumerate(QUEBEC_EMPLOYER_LEADS):
        name = (lead.get("name") or "").strip()
        if not name:
            continue
        recruiter = recruiters[index % len(recruiters)] if recruiters else None
        employees = lead.get("employees")
        company = _find_company(db, lead, names)
        if company is not None and not _owned_company_is_this_lead(company, lead):
            company = None
        if company is None:
            company = Company(
                name=name,
                legal_name=lead.get("legal_name") or name,
                trade_name=name,
                description=lead.get("hiring") or "",
                sector=lead.get("sector"),
                city=lead.get("city"),
                address=lead.get("address"),
                province="Québec",
                country="Canada",
                contact_name=lead.get("contact_name") or None,
                email=lead.get("email"),
                phone=lead.get("phone"),
                website=lead.get("website"),
                linkedin_url=lead.get("linkedin_url"),
                employees=employees,
                size_label=_size_label(employees),
                status=CompanyStatus.PROSPECT,
                assigned_recruiter_id=recruiter.id if recruiter else None,
            )
            db.add(company)
            _forget_session_prospects(db)
            db.flush()
            _index_company(names, company)
            created += 1
        else:
            _fill_empty(
                company,
                legal_name=lead.get("legal_name"),
                trade_name=name,
                description=lead.get("hiring"),
                sector=lead.get("sector"),
                city=lead.get("city"),
                address=lead.get("address"),
                website=lead.get("website"),
                linkedin_url=lead.get("linkedin_url"),
                email=lead.get("email"),
                phone=lead.get("phone"),
                employees=employees,
                size_label=_size_label(employees),
                contact_name=lead.get("contact_name") or None,
            )
            if company.status is None:
                company.status = CompanyStatus.PROSPECT
            if not company.assigned_recruiter_id and recruiter:
                company.assigned_recruiter_id = recruiter.id
        _ensure_note(db, company, staff, lead)
        _ensure_prospect(db, company, lead, recruiter)
    if created:
        logger.info("%s fiches employeurs québécois ajoutées (veille).", created)
    return created
