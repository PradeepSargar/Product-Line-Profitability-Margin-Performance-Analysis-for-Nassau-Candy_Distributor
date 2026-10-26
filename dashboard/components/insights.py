"""
Reusable insight components, findings cards, and strategic implications.

Layout guarantees:
- render_executive_findings() → strict 2×2 grid (NOT masonry).
- Cards in the SAME row have IDENTICAL height via:
    .insight-grid-row { grid-auto-rows: 1fr } + .insight-card { height: 100%; display:flex; flex-direction:column }
- Long text in the left card stretches the row; the right card matches it.
- Internal flex order: title (shrink:0) → body (flex:1) → implication (shrink:0).
"""

import streamlit as st
import pandas as pd
from dashboard.utils.dashboard_utils import format_percent, render_html

# ── Golden Ticket palette aliases (avoids circular import from theme.py) ──
_PURPLE  = "#4B1E78"
_GOLD    = "#F2B01E"
_PINK    = "#E6427A"
_DARK    = "#2A1B3D"
_MUTED   = "#7A6C8A"
_WARNING = "#DC2626"


def _build_insight_card_html(title: str, body: str, implication: str = None,
                             border_color: str = None) -> str:
    """Build the clean HTML string for a single insight card (no indentation)."""
    _border = border_color if border_color else _PURPLE

    implication_html = ""
    if implication:
        implication_html = (
            f'<div class="insight-card-implication">'
            f'<b>Business Implication:</b> {implication}'
            f'</div>'
        )

    return (
        f'<div class="insight-card" style="border-left-color: {_border};">'
        f'<h4>{title}</h4>'
        f'<p>{body}</p>'
        f'{implication_html}'
        f'</div>'
    )


def render_insight_card(title: str, body: str, implication: str = None,
                        border_color: str = None):
    """
    Render a single styled business insight card with optional implication.
    """
    render_html(_build_insight_card_html(title, body, implication, border_color))


def render_executive_findings(kpis: dict, top5_info: dict, div_df: pd.DataFrame,
                              reg_range: dict, risk_summary: dict):
    """
    Render dynamic executive findings and strategic implications grid.
    Strict 2x2 CSS Grid wrapper.
    """
    if not div_df.empty:
        top_div = div_df.iloc[0]
        top_div_name = top_div['Division']
        top_div_gp_pct = top_div['Profit Contribution %']
        top_div_sales_pct = top_div['Revenue Contribution %']
    else:
        top_div_name, top_div_gp_pct, top_div_sales_pct = "N/A", 0.0, 0.0

    top_sku = top5_info['top_profit_products'][0] if top5_info['top_profit_products'] else "N/A"

    cards = []

    # ── Card 1: Extreme Profit Concentration (Row 1, Col 1) ───────
    cards.append(_build_insight_card_html(
        title="1. Extreme Profit Concentration",
        body=(
            f"The top 5 products generate <b>{format_percent(top5_info['top_n_profit_pct'])}</b> of portfolio Gross Profit "
            f"and <b>{format_percent(top5_info['top_n_revenue_pct'])}</b> of total Revenue. "
            f"The lead SKU (<b>{top_sku}</b>) represents a core commercial foundation of the distributor."
        ),
        implication=(
            "Cash flow is heavily dependent on a compact core. Supplier price hikes, stockouts, or retail friction "
            "on these top 5 SKUs represent the company's largest single financial exposure."
        ),
        border_color=_PURPLE
    ))

    # ── Card 3: Geographic Margin Uniformity (Row 1, Col 2) ────────
    margin_spread = reg_range.get('margin_range_pp', 0.0)
    min_reg = reg_range.get('min_region', 'N/A')
    max_reg = reg_range.get('max_region', 'N/A')
    min_m = reg_range.get('min_margin', 0.0)
    max_m = reg_range.get('max_margin', 0.0)
    cards.append(_build_insight_card_html(
        title="3. Geographic Margin Uniformity",
        body=(
            f"Across all four sales territories, Gross Margin % varies by only <b>{margin_spread:.2f} percentage points</b> "
            f"(ranging from {min_reg} at {min_m:.2f}% to {max_reg} at {max_m:.2f}%)."
        ),
        implication=(
            "Profitability is structurally driven by product mix and division rather than regional cost divergence. "
            "Regional sales initiatives can proceed under unified commercial pricing frameworks."
        ),
        border_color=_PINK
    ))

    # ── Card 2: Division Asymmetry (Row 2, Col 1) ──────────────────
    cards.append(_build_insight_card_html(
        title="2. Division Asymmetry",
        body=(
            f"The <b>{top_div_name}</b> division is the primary commercial engine, accounting for "
            f"<b>{format_percent(top_div_gp_pct)}</b> of Gross Profit and <b>{format_percent(top_div_sales_pct)}</b> of Revenue. "
            f"Non-chocolate categories operate with narrower margins or minor volume shares."
        ),
        implication=(
            "While chocolate drives near-term earnings, margin enhancement and category expansion in secondary "
            "divisions could help diversify portfolio risk."
        ),
        border_color=_GOLD
    ))

    # ── Card 4: Margin Screening & Cost Ratio Exposure (Row 2, Col 2)
    cards.append(_build_insight_card_html(
        title="4. Margin Screening & Cost Ratio Exposure",
        body=(
            f"<b>{risk_summary['flagged_count']}</b> of <b>{risk_summary['total_products']}</b> products "
            f"({risk_summary['flagged_pct']:.1f}%) meet portfolio-relative risk screening criteria "
            f"(Gross Margin < median {risk_summary['median_gm_pct']:.1f}% AND Cost-to-Sales > median {risk_summary['median_cts_pct']:.1f}%)."
        ),
        implication=(
            "Screened products warrant targeted reviews of wholesale price tiers, vendor contracts, freight allowances, "
            "and minimum order quantities rather than immediate discontinuation."
        ),
        border_color=_WARNING
    ))

    # ── Emit single 2×2 CSS Grid wrapper ────────────────────────────
    grid_inner = "".join(cards)
    grid_html = f'<div class="insight-grid">{grid_inner}</div>'
    render_html(grid_html)


def render_strategic_definitions():
    """Render 4-quadrant strategic definition cards using the Golden Ticket palette."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_html(f"""
            <div class="strategic-card strategic-card--gold">
                <b style="color: {_PURPLE};">Core Drivers</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">High Profit / High Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Key portfolio pillars driving healthy margins. Protect supply continuity, prevent stockouts, and prioritize shelf placement.
                </p>
            </div>
        """)

    with c2:
        render_html(f"""
            <div class="strategic-card strategic-card--purple">
                <b style="color: {_PURPLE};">Volume Drivers</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">High Profit / Low Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Substantial transaction volume generates strong gross profit despite below-median margin rates. Audit freight and packaging to capture margin points.
                </p>
            </div>
        """)

    with c3:
        render_html(f"""
            <div class="strategic-card strategic-card--pink">
                <b style="color: {_PURPLE};">Niche Gems</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">Low Profit / High Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Strong unit-level economics constrained by limited customer reach. Prime candidates for targeted distribution and marketing pushes.
                </p>
            </div>
        """)

    with c4:
        render_html(f"""
            <div class="strategic-card strategic-card--risk">
                <b style="color: {_WARNING};">Underperformers</b><br>
                <span style="font-size: 0.76rem; color: {_WARNING};">Low Profit / Low Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Deliver below-median profit and margin. Note: Classification is an analytical screening indicator, not an immediate discontinuation order.
                </p>
            </div>
        """)
