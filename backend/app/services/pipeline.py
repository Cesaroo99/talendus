"""Correspondance kanban admin ↔ statuts de candidature API."""

from app.models.enums import ApplicationStatus

STAGE_TO_STATUS: dict[str, ApplicationStatus] = {
    "nouveaux": ApplicationStatus.SUBMITTED,
    "preselection": ApplicationStatus.UNDER_REVIEW,
    "entretien-talendus": ApplicationStatus.INTERVIEW,
    "presentation": ApplicationStatus.SHORTLISTED,
    "entretien-client": ApplicationStatus.SECOND_INTERVIEW,
    "offre": ApplicationStatus.OFFER_SENT,
    "placement": ApplicationStatus.HIRED,
}

STATUS_TO_STAGE: dict[ApplicationStatus, str] = {
    ApplicationStatus.SUBMITTED: "nouveaux",
    ApplicationStatus.RECEIVED: "nouveaux",
    ApplicationStatus.UNDER_REVIEW: "preselection",
    ApplicationStatus.SHORTLISTED: "presentation",
    ApplicationStatus.INTERVIEW: "entretien-talendus",
    ApplicationStatus.SECOND_INTERVIEW: "entretien-client",
    ApplicationStatus.OFFER_SENT: "offre",
    ApplicationStatus.HIRED: "placement",
}

TRACK_STEPS = [
    ApplicationStatus.SUBMITTED,
    ApplicationStatus.UNDER_REVIEW,
    ApplicationStatus.INTERVIEW,
    ApplicationStatus.SHORTLISTED,
    ApplicationStatus.SECOND_INTERVIEW,
    ApplicationStatus.OFFER_SENT,
    ApplicationStatus.HIRED,
]

_RANK = {
    ApplicationStatus.SUBMITTED: 0,
    ApplicationStatus.RECEIVED: 1,
    ApplicationStatus.UNDER_REVIEW: 1,
    ApplicationStatus.INTERVIEW: 2,
    ApplicationStatus.SHORTLISTED: 3,
    ApplicationStatus.SECOND_INTERVIEW: 4,
    ApplicationStatus.OFFER_SENT: 5,
    ApplicationStatus.HIRED: 6,
}

VIVIER_FOR_STATUS = {
    ApplicationStatus.SUBMITTED: "nouveau",
    ApplicationStatus.RECEIVED: "nouveau",
    ApplicationStatus.UNDER_REVIEW: "qualifie",
    ApplicationStatus.INTERVIEW: "entretien",
    ApplicationStatus.SHORTLISTED: "presente",
    ApplicationStatus.SECOND_INTERVIEW: "entretien-client",
    ApplicationStatus.OFFER_SENT: "offre",
    ApplicationStatus.HIRED: "place",
    ApplicationStatus.REJECTED: "refuse",
    ApplicationStatus.WITHDRAWN: "inactif",
}


def stage_for(status: ApplicationStatus | None) -> str | None:
    if status is None:
        return None
    return STATUS_TO_STAGE.get(status)


def status_for_stage(stage: str) -> ApplicationStatus | None:
    return STAGE_TO_STATUS.get(stage)


def tracker_for(row) -> dict:
    history_at: dict[str, str | None] = {}
    progress = 0
    for item in row.history or []:
        raw = item.new_status or ""
        if raw == ApplicationStatus.RECEIVED.value:
            raw = ApplicationStatus.UNDER_REVIEW.value
        if raw not in history_at:
            history_at[raw] = item.created_at.isoformat() if item.created_at else None
        try:
            status = ApplicationStatus(item.new_status)
        except ValueError:
            continue
        if status not in {ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}:
            progress = max(progress, _RANK.get(status, 0))
    current = row.status
    outcome = None
    if current in {ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}:
        outcome = current.value
        rank = progress
    else:
        rank = _RANK.get(current, 0)
    steps = []
    for status in TRACK_STEPS:
        idx = _RANK[status]
        if outcome:
            state = "done" if idx <= rank else "todo"
        elif current is ApplicationStatus.HIRED:
            state = "done" if idx <= rank else "todo"
        elif idx < rank:
            state = "done"
        elif idx == rank:
            state = "current"
        else:
            state = "todo"
        at = history_at.get(status.value)
        if status is ApplicationStatus.UNDER_REVIEW and not at:
            at = history_at.get(ApplicationStatus.RECEIVED.value)
        if status is ApplicationStatus.SUBMITTED and not at:
            at = row.created_at.isoformat() if row.created_at else None
        steps.append({"key": status.value, "state": state, "at": at})
    return {"status": current.value if current else None, "outcome": outcome, "steps": steps}


def next_action_for(row, viewer=None) -> dict | None:
    """Prochaine action utile, selon qui consulte le dossier."""
    from app.models.enums import UserRole

    status = row.status
    role = getattr(viewer, "role", None) if viewer is not None else None
    if role == UserRole.EMPLOYER:
        mapping = {
            ApplicationStatus.SHORTLISTED: ("feedback", "Donnez une suite à Talendus"),
            ApplicationStatus.SECOND_INTERVIEW: ("wait", "Entretien client en cours"),
            ApplicationStatus.OFFER_SENT: ("wait", "Offre en cours"),
            ApplicationStatus.HIRED: ("done", "Placement confirmé"),
            ApplicationStatus.REJECTED: ("done", "Dossier non retenu"),
        }
        item = mapping.get(status)
        return {"key": item[0], "label": item[1]} if item else None
    from app.rbac import ADMINS

    if role in {UserRole.RECRUITER} | ADMINS:
        mapping = {
            ApplicationStatus.SUBMITTED: ("review", "Passer en présélection Talendus"),
            ApplicationStatus.RECEIVED: ("review", "Passer en présélection Talendus"),
            ApplicationStatus.UNDER_REVIEW: ("interview", "Planifier l’entretien Talendus"),
            ApplicationStatus.INTERVIEW: ("present", "Présenter le dossier à l’employeur"),
            ApplicationStatus.SHORTLISTED: ("client", "Relancer l’employeur ou planifier l’entretien client"),
            ApplicationStatus.SECOND_INTERVIEW: ("offer", "Préparer l’offre"),
            ApplicationStatus.OFFER_SENT: ("hire", "Confirmer le placement"),
            ApplicationStatus.HIRED: ("done", "Dossier placé"),
        }
        item = mapping.get(status)
        return {"key": item[0], "label": item[1]} if item else None
    return None


def client_feedback_from(row) -> str | None:
    for item in reversed(list(row.history or [])):
        text = (item.comment or "").strip()
        if text.startswith("Retour employeur"):
            return text
    return None
