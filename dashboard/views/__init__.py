"""
Dashboard view modules for Nassau Candy Distributor Analytics.
3-page structure (post consolidation):
  1. Executive Overview
  2. Product & Portfolio Intelligence  (merged: product_profitability + strategic_analysis)
  3. Risk & Business Performance       (merged: risk_diagnostics + business_performance)
"""

from . import executive_overview
from . import product_profitability
from . import risk_diagnostics

__all__ = [
    "executive_overview",
    "product_profitability",
    "risk_diagnostics",
]
