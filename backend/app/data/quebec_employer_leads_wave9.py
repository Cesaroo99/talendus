"""Vague 9 : veille Indeed QC — entreprises découvertes via des offres indexées.

Indeed est la source de découverte (offre → entreprise → volume → score).
Aucun scrap, aucun courriel inventé. Les agences de placement sont
conservées mais classées priorité faible (concurrents, pas clients types).
"""

from __future__ import annotations

from app.data.indeed_quebec_signals import INDEED_QUEBEC_SIGNALS
from app.services.indeed_prospecting import compile_indeed_leads

QUEBEC_EMPLOYER_LEADS_WAVE9 = compile_indeed_leads(INDEED_QUEBEC_SIGNALS)
