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

from theme import PALETTE, apply_theme, style_fig

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
