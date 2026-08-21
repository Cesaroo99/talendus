"""Honeypot anti-spam partagé par les formulaires publics."""

from __future__ import annotations

from app.errors import AppError


def reject_honeypot(website_url: str | None) -> None:
    if str(website_url or "").strip():
        raise AppError(400, "Requête refusée.", "SPAM_REJECTED")
