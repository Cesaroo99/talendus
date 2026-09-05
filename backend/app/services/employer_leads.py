"""Importe les 50 employeurs québécois recherchés : fiche client + prospect CRM."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.models import Company, InternalNote, User
from app.models.enums import CompanyStatus, UserRole
from app.models.prospect import Prospect
from app.services.prospects import upsert_prospect

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


def _find_company(db: Session, lead: dict[str, Any]) -> Company | None:
    name = (lead.get("name") or "").strip()
    if not name:
        return None
    return db.scalar(select(Company).where(func.lower(Company.name) == name.casefold()))


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
    return (
        f"{LEAD_NOTE_MARK}.\n"
        f"Signal : {jobs}\n"
        f"Carrières : {careers}\n"
        "Critères : plusieurs postes visibles (portail, Jobillico, Indeed ou LinkedIn), "
        "métiers usine / entrepôt / maintenance, établissement québécois, une seule fiche par groupe."
    )


def _ensure_note(db: Session, company: Company, author: User | None, lead: dict[str, Any]) -> None:
    if not author:
        return
    exists = db.scalar(
        select(InternalNote.id).where(
            InternalNote.entity_type == "company",
            InternalNote.entity_id == company.id,
            InternalNote.text.like(f"{LEAD_NOTE_MARK}%"),
        )
    )
    if exists:
        return
    db.add(
        InternalNote(
            entity_type="company",
            entity_id=company.id,
            author_id=author.id,
            text=_note_text(lead)[:4000],
        )
    )


def _ensure_prospect(db: Session, company: Company, lead: dict[str, Any], recruiter: User | None) -> None:
    email = (lead.get("email") or "").strip()
    if not email or "@" not in email:
        return
    contact = (lead.get("contact_name") or "Ressources humaines").strip()
    parts = contact.split(None, 1)
    first = parts[0] if parts and parts[0].casefold() != "ressources" else ""
    last = parts[1] if len(parts) > 1 and first else ""
    if not first:
        first = "Ressources"
        last = "humaines"
    hiring = (lead.get("hiring") or "")[:5000]
    detail = (lead.get("hiring") or lead.get("careers_url") or "")[:240]
    existing = db.scalar(select(Prospect.id).where(Prospect.side == "employer", Prospect.email == email.lower()))
    upsert_prospect(
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


def ensure_quebec_employer_leads(db: Session) -> int:
    """Crée ou complète les 50 fiches. Idempotent. Aucun compte employeur."""
    recruiters = _recruiters(db)
    staff = recruiters[0] if recruiters else _staff_user(db)
    created = 0
    for index, lead in enumerate(QUEBEC_EMPLOYER_LEADS):
        name = (lead.get("name") or "").strip()
        if not name:
            continue
        recruiter = recruiters[index % len(recruiters)] if recruiters else None
        employees = lead.get("employees")
        company = _find_company(db, lead)
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
                contact_name=lead.get("contact_name") or "Ressources humaines",
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
            db.flush()
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
                contact_name=lead.get("contact_name") or "Ressources humaines",
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
