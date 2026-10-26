"""
Centralized theme and design system for the Nassau Candy Analytics Dashboard.
Re-exports the Golden Ticket palette, CSS injector, and Plotly styling helper from theme.py.
"""

import sys
import os

# Ensure project root is available
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from theme import (
    PALETTE, DESIGN_TOKENS,
    apply_theme, style_fig, plot_chart, chart_divider,
)

# Explicit color aliases for convenience
PRIMARY = PALETTE["wonka_purple"]
SECONDARY = PALETTE["golden_ticket"]
ACCENT = PALETTE["candy_pink"]
WARNING = PALETTE["warning"]
RISK = PALETTE["warning"]
DARK = PALETTE["body_text"]
MUTED = PALETTE["muted_text"]
BORDER = "#EADBC8"
CARD_BG = PALETTE["cards"]
BACKGROUND = PALETTE["cream"]

# Layout design tokens (centralized spacing, radii, grid gaps)
MAX_WIDTH = DESIGN_TOKENS["dashboard_max_width"]
CARD_RADIUS = DESIGN_TOKENS["card_radius"]
CARD_PADDING = DESIGN_TOKENS["card_padding"]
GRID_GAP = DESIGN_TOKENS["grid_gap"]
SECTION_GAP = DESIGN_TOKENS["section_gap"]
KPI_CARD_MIN_HEIGHT = DESIGN_TOKENS["kpi_card_min_height"]
INSIGHT_CARD_MIN_HEIGHT = DESIGN_TOKENS["insight_card_min_height"]

__all__ = [
    "PALETTE", "DESIGN_TOKENS",
    "apply_theme", "style_fig", "plot_chart", "chart_divider",
    "PRIMARY", "SECONDARY", "ACCENT", "WARNING", "RISK",
    "DARK", "MUTED", "BORDER", "CARD_BG", "BACKGROUND",
    "MAX_WIDTH", "CARD_RADIUS", "CARD_PADDING", "GRID_GAP",
    "SECTION_GAP", "KPI_CARD_MIN_HEIGHT", "INSIGHT_CARD_MIN_HEIGHT",
]
