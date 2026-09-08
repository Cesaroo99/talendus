"""Compile le Lead Intelligence Talendus (Indeed + overlays + nouvelles sources).

Aucune requête réseau. Les volumes par board ne sont jamais additionnés.
"""

from __future__ import annotations

from app.data.indeed_quebec_signals import INDEED_QUEBEC_SIGNALS
from app.data.lead_intelligence_new import NEW_LIS_SIGNALS
from app.data.lead_intelligence_overlays import apply_overlays
from app.services.lead_intelligence import compile_intelligence, intelligence_report

LEAD_INTELLIGENCE = compile_intelligence(apply_overlays(list(INDEED_QUEBEC_SIGNALS)) + list(NEW_LIS_SIGNALS))
LEAD_INTELLIGENCE_REPORT = intelligence_report(LEAD_INTELLIGENCE)
