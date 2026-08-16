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


def stage_for(status: ApplicationStatus | None) -> str | None:
    if status is None:
        return None
    return STATUS_TO_STAGE.get(status)


def status_for_stage(stage: str) -> ApplicationStatus | None:
    return STAGE_TO_STATUS.get(stage)
