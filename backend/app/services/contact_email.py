"""Validation et filtres des courriels de contact (prospects / clients)."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
INVALID_MARKERS = (
    "example.",
    "test@",
    "noreply@",
    "no-reply@",
    "invalid@",
    "fake@",
    "xxx@",
    "@email.",
    "you@company.",
)
EMAIL_FILTERS = ("", "with", "without", "verified", "unverified", "found")
READY_FILTERS = ("", "ready")


def is_valid_public_email(email: str | None) -> bool:
    value = (email or "").strip().lower()
    if not value or not EMAIL_RE.match(value):
        return False
    return not any(marker in value for marker in INVALID_MARKERS)


def is_ready_to_contact(email: str | None, confidence: str | None = None) -> bool:
    if not is_valid_public_email(email):
        return False
    return (confidence or "").upper() != "INVALID"


@lru_cache(maxsize=1)
def _lead_email_index() -> dict[str, dict[str, Any]]:
    from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS

    index: dict[str, dict[str, Any]] = {}
    for lead in QUEBEC_EMPLOYER_LEADS:
        name = (lead.get("name") or "").strip().casefold()
        if name:
            index[name] = lead
        email = (lead.get("email") or "").strip().lower()
        if email:
            index[f"e:{email}"] = lead
    return index


def lead_email_meta(company_name: str | None = None, email: str | None = None) -> dict[str, Any]:
    index = _lead_email_index()
    lead = None
    if company_name:
        lead = index.get(company_name.strip().casefold())
    if lead is None and email:
        lead = index.get(f"e:{(email or '').strip().lower()}")
    if not lead:
        return {
            "email_verified": False,
            "email_confidence": None,
            "email_source": None,
            "email_verified_at": None,
            "ready_to_contact": is_ready_to_contact(email),
        }
    confidence = lead.get("email_confidence")
    verified = bool(lead.get("email_verified") or (confidence or "").startswith("VERIFIED"))
    verified_at = lead.get("email_verified_at") or lead.get("researched_at")
    return {
        "email_verified": verified,
        "email_confidence": confidence,
        "email_source": lead.get("email_source"),
        "email_verified_at": verified_at,
        "ready_to_contact": is_ready_to_contact(lead.get("email") or email, confidence),
    }


def matches_email_filter(
    email: str | None,
    *,
    wanted: str | None,
    verified: bool = False,
    ready: str | None = None,
    confidence: str | None = None,
    verified_at: str | None = None,
) -> bool:
    key = (wanted or "").strip().lower()
    ready_key = (ready or "").strip().lower()
    present = bool((email or "").strip())
    valid = is_valid_public_email(email)
    if key == "with" and not present:
        return False
    if key == "without" and present:
        return False
    if key == "verified" and not (valid and verified):
        return False
    if key == "unverified" and not (present and not verified):
        return False
    if key == "found" and not (valid and verified and (verified_at or "").strip()):
        return False
    if ready_key in {"1", "true", "ready"} and not is_ready_to_contact(email, confidence):
        return False
    return True
