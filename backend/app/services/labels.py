"""Libellés FR/EN pour les codes internes visibles par les utilisateurs."""

from __future__ import annotations

APPLICATION_STATUS = {
    "SUBMITTED": {"fr": "Candidature envoyée", "en": "Submitted"},
    "RECEIVED": {"fr": "Reçue", "en": "Received"},
    "UNDER_REVIEW": {"fr": "Présélection Talendus", "en": "Talendus screening"},
    "SHORTLISTED": {"fr": "Présenté à l’employeur", "en": "Presented to employer"},
    "INTERVIEW": {"fr": "Entretien Talendus", "en": "Talendus interview"},
    "SECOND_INTERVIEW": {"fr": "Entretien client", "en": "Client interview"},
    "OFFER_SENT": {"fr": "Offre d’emploi", "en": "Offer sent"},
    "REJECTED": {"fr": "Non retenue", "en": "Not retained"},
    "HIRED": {"fr": "Embauchée", "en": "Hired"},
    "WITHDRAWN": {"fr": "Retirée", "en": "Withdrawn"},
}

INTERVIEW_STATUS = {
    "SCHEDULED": {"fr": "Planifié", "en": "Scheduled"},
    "CONFIRMED": {"fr": "Confirmé", "en": "Confirmed"},
    "COMPLETED": {"fr": "Terminé", "en": "Completed"},
    "CANCELLED": {"fr": "Annulé", "en": "Cancelled"},
    "NO_SHOW": {"fr": "Absent", "en": "No-show"},
}

INTERVIEW_TYPE = {
    "TALENDUS": {"fr": "Talendus", "en": "Talendus"},
    "CLIENT": {"fr": "Client", "en": "Client"},
    "PHONE": {"fr": "Téléphone", "en": "Phone"},
    "VIDEO": {"fr": "Visio", "en": "Video"},
    "ONSITE": {"fr": "Sur place", "en": "On site"},
    "OFFER": {"fr": "Offre", "en": "Offer"},
}

INVOICE_STATUS = {
    "DRAFT": {"fr": "Brouillon", "en": "Draft"},
    "SENT": {"fr": "Envoyée", "en": "Sent"},
    "PENDING": {"fr": "En attente", "en": "Pending"},
    "PAID": {"fr": "Payée", "en": "Paid"},
    "OVERDUE": {"fr": "En retard", "en": "Overdue"},
    "CANCELLED": {"fr": "Annulée", "en": "Cancelled"},
    "REFUNDED": {"fr": "Remboursée", "en": "Refunded"},
}

JOB_STATUS = {
    "DRAFT": {"fr": "Brouillon", "en": "Draft"},
    "PENDING_VALIDATION": {"fr": "En validation", "en": "Pending validation"},
    "PUBLISHED": {"fr": "Publiée", "en": "Published"},
    "PAUSED": {"fr": "En pause", "en": "Paused"},
    "CLOSED": {"fr": "Fermée", "en": "Closed"},
    "ARCHIVED": {"fr": "Archivée", "en": "Archived"},
}


def lang_of(user=None, locale: str | None = None) -> str:
    raw = locale
    if raw is None and user is not None:
        prefs = getattr(user, "preferences", None)
        raw = getattr(prefs, "locale", None) if prefs else None
    text = str(raw or "fr-CA").strip().lower()
    return "en" if text.startswith("en") else "fr"


def label(table: dict[str, dict[str, str]], code, lang: str = "fr") -> str:
    key = str(getattr(code, "value", code) or "").upper().replace("-", "_")
    row = table.get(key) or {}
    return row.get(lang) or row.get("fr") or key


def application_status_label(code, user=None, locale: str | None = None) -> str:
    return label(APPLICATION_STATUS, code, lang_of(user, locale))


def interview_status_label(code, user=None, locale: str | None = None) -> str:
    return label(INTERVIEW_STATUS, code, lang_of(user, locale))


def interview_type_label(code, user=None, locale: str | None = None) -> str:
    return label(INTERVIEW_TYPE, code, lang_of(user, locale))
