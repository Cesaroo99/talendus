"""Vague 10 : Lead Intelligence multi-sources — entreprises absentes des vagues 1–9.

Croisement Indeed / LinkedIn / Jobillico / site / ATS publics indexés.
Aucun scrap, aucun courriel inventé (NOT_FOUND → email vide).
"""

from __future__ import annotations

from app.data.lead_intelligence_new import NEW_LIS_SIGNALS
from app.services.lead_intelligence import compile_intelligence, to_catalog_lead

QUEBEC_EMPLOYER_LEADS_WAVE10 = tuple(
    to_catalog_lead(record) for record in compile_intelligence(NEW_LIS_SIGNALS)
)
