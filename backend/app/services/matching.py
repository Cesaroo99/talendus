"""Matching déterministe candidat ↔ offre (compétences, ville, secteur, expérience, salaire)."""

from __future__ import annotations

import re

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import AppError
from app.models import Candidate, JobOffer, User
from app.models.enums import OPEN_JOB_STATUSES, UserRole
from app.rbac import ADMINS
from app.services.access import user_belongs_to_company
from app.services.auth import ensure_candidate
from app.services.jobs import serialize_job

_SPLIT = re.compile(r"[,;/|]+")
_YEARS = re.compile(r"(\d+)")


def _tokens(value: str | None) -> set[str]:
    return {part.strip().lower() for part in _SPLIT.split(value or "") if part.strip()}


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def _years_required(job: JobOffer) -> int | None:
    text = job.experience_level or ""
    match = _YEARS.search(text)
    if not match:
        return None
    return int(match.group(1))


def score_pair(candidate: Candidate, job: JobOffer) -> tuple[int, list[str]]:
    reasons: list[str] = []
    total = 0

    c_skills = _tokens(candidate.skills)
    j_skills = _tokens(job.skills)
    if j_skills:
        overlap = {js for js in j_skills if any(js in cs or cs in js for cs in c_skills)}
        ratio = len(overlap) / len(j_skills)
        pts = round(40 * min(1.0, ratio))
        total += pts
        if overlap:
            reasons.append("Compétences : " + ", ".join(sorted(overlap)[:4]))
        else:
            reasons.append("Peu de compétences en commun")
    else:
        total += 16
        reasons.append("Offre sans compétences listées")

    city = _norm(candidate.city)
    loc = _norm(job.location)
    if city and loc and (city in loc or loc in city):
        total += 20
        reasons.append(f"Ville : {job.location}")
    elif city and loc and _norm(candidate.mobility) and city != loc:
        total += 10
        reasons.append("Mobilité possible")
    elif not city or not loc:
        total += 8
    else:
        reasons.append("Localisation différente")

    c_sec = _norm(candidate.sector)
    j_sec = _norm(job.sector)
    if c_sec and j_sec and (c_sec == j_sec or c_sec in j_sec or j_sec in c_sec):
        total += 20
        reasons.append(f"Secteur : {job.sector}")
    elif not c_sec or not j_sec:
        total += 8
    else:
        reasons.append("Secteur différent")

    needed = _years_required(job)
    years = candidate.years_experience or 0
    if needed is None:
        total += 6
    elif years >= needed:
        total += 10
        reasons.append(f"Expérience : {years} ans")
    elif years >= max(0, needed - 1):
        total += 6
        reasons.append("Expérience proche")
    else:
        reasons.append("Expérience insuffisante")

    cmin = candidate.desired_salary_min
    cmax = candidate.desired_salary_max
    jmin = job.salary_min
    jmax = job.salary_max
    if cmin and cmax and jmin and jmax:
        if cmax < 1000 and jmin > 200:
            # candidat en $/h, offre annuelle
            cmin, cmax = cmin * 2080, cmax * 2080
        if jmax < 1000 and cmin and cmin > 200:
            jmin, jmax = jmin * 2080, jmax * 2080
        if cmin <= jmax and cmax >= jmin:
            total += 10
            reasons.append("Salaire compatible")
        else:
            reasons.append("Écart salarial")
    else:
        total += 5

    return min(100, total), reasons


def jobs_for_candidate(db: Session, candidate: Candidate, limit: int = 20) -> list[dict]:
    jobs = list(
        db.scalars(
            select(JobOffer)
            .options(joinedload(JobOffer.company))
            .where(JobOffer.status.in_(OPEN_JOB_STATUSES))
            .order_by(JobOffer.published_at.desc())
        ).unique().all()
    )
    ranked: list[dict] = []
    for job in jobs:
        score, reasons = score_pair(candidate, job)
        ranked.append(
            {
                "score": score,
                "reasons": reasons,
                "job": serialize_job(job),
            }
        )
    ranked.sort(key=lambda row: row["score"], reverse=True)
    return ranked[:limit]


def candidates_for_job(db: Session, job: JobOffer, limit: int = 20) -> list[dict]:
    candidates = list(
        db.scalars(select(Candidate).options(joinedload(Candidate.user), selectinload(Candidate.experiences))).unique().all()
    )
    ranked: list[dict] = []
    for candidate in candidates:
        user = candidate.user
        score, reasons = score_pair(candidate, job)
        ranked.append(
            {
                "score": score,
                "reasons": reasons,
                "candidate": {
                    "id": candidate.id,
                    "user_id": candidate.user_id,
                    "first_name": user.first_name if user else "",
                    "last_name": user.last_name if user else "",
                    "email": user.email if user else "",
                    "city": candidate.city,
                    "title": candidate.title,
                    "sector": candidate.sector,
                    "skills": candidate.skills,
                    "years_experience": candidate.years_experience,
                },
            }
        )
    ranked.sort(key=lambda row: row["score"], reverse=True)
    return ranked[:limit]


def my_job_matches(db: Session, user: User, limit: int = 20) -> list[dict]:
    candidate = ensure_candidate(db, user)
    return jobs_for_candidate(db, candidate, limit)


def staff_job_candidates(db: Session, user: User, job_id: str, limit: int = 20) -> list[dict]:
    if user.role not in {UserRole.RECRUITER, UserRole.EMPLOYER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès au matching.", "FORBIDDEN")
    job = db.get(JobOffer, job_id)
    if not job:
        raise AppError(404, "Offre introuvable.", "JOB_NOT_FOUND")
    if user.role == UserRole.EMPLOYER and not user_belongs_to_company(db, user, job.company_id):
        raise AppError(403, "Vous n'avez pas accès à cette offre.", "FORBIDDEN")
    return candidates_for_job(db, job, limit)


def staff_candidate_jobs(db: Session, user: User, candidate_id: str, limit: int = 20) -> list[dict]:
    if user.role not in {UserRole.RECRUITER} | ADMINS:
        raise AppError(403, "Vous n'avez pas accès au matching.", "FORBIDDEN")
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise AppError(404, "Candidat introuvable.", "CANDIDATE_NOT_FOUND")
    return jobs_for_candidate(db, candidate, limit)


def notify_job_matches(db: Session, job: JobOffer, limit: int = 40) -> int:
    """Alerte les candidats actifs dont le score dépasse le seuil (appelé à la publication)."""
    from app.config import get_settings
    from app.models.enums import JobSearchStatus, NotificationType
    from app.services.notifications import notify

    min_score = get_settings().job_match_min_score or 50
    candidates = list(
        db.scalars(
            select(Candidate).options(joinedload(Candidate.user)).where(Candidate.job_search_status == JobSearchStatus.ACTIVE)
        ).unique().all()
    )
    ranked: list[tuple[int, Candidate, list[str]]] = []
    for candidate in candidates:
        if not candidate.user:
            continue
        score, reasons = score_pair(candidate, job)
        if score >= min_score:
            ranked.append((score, candidate, reasons))
    ranked.sort(key=lambda row: row[0], reverse=True)
    sent = 0
    href = f"/emploi-{job.slug}.html"
    where = job.location or "Québec"
    for score, candidate, reasons in ranked[:limit]:
        detail = " · ".join(reasons[:2])
        notify(
            db,
            candidate.user,
            NotificationType.JOB_MATCH,
            "Offre correspondant à votre profil",
            f"{job.title} ({where}) — score {score} %." + (f" {detail}" if detail else ""),
            href=href,
        )
        sent += 1
    return sent
