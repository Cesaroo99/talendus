"""Index Deep Contact Finder — catalogue existant uniquement."""

from __future__ import annotations

from app.data.contact_finder_apply import _finds_index
from app.data.quebec_employer_leads import QUEBEC_EMPLOYER_LEADS
from app.services.contact_finder import compile_contact_finder, finder_report
from app.services.contact_finder_providers import provider_catalog

CONTACT_FINDER = compile_contact_finder(QUEBEC_EMPLOYER_LEADS, _finds_index())
CONTACT_FINDER_REPORT = finder_report(CONTACT_FINDER)
CONTACT_FINDER_REPORT["providers"] = provider_catalog()
