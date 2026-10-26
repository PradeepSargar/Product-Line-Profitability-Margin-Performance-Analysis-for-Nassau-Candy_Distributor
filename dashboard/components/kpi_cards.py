"""
Reusable executive KPI card and grid components.
Styled with the Golden Ticket palette: white card, 5px gold left border, rounded corners, soft shadow.

Layout guarantees:
- All KPI cards in a grid share IDENTICAL row height via CSS Grid `grid-auto-rows: 1fr`.
- Internal vertical structure is LOCKED: label (top) → value (center, flex-1) → subtext/badge (bottom).
- Text length never pushes a card taller than its row siblings.
- Grids are rendered as a single pure-HTML <div class="kpi-grid"> to bypass Streamlit column-height behavior.
"""

from theme import PALETTE
from dashboard.utils.dashboard_utils import (
    format_currency,
    format_percent,
    format_integer,
    render_html,
)


def _build_kpi_card_html(title: str, value: str, subtext: str = "",
                         border_color: str = None, badge: str = None) -> str:
    """
    Build the clean HTML string for a single KPI card without indentation
    to prevent Markdown parser code-block escaping.
    """
    accent_border = border_color if border_color else PALETTE['golden_ticket']
    subtext_html = f'<div class="kpi-subtext">{subtext}</div>' if subtext else ""
    badge_html = f'<span class="kpi-badge">{badge}</span>' if badge else ""

    return (
        f'<div class="kpi-card" style="border-left: 5px solid {accent_border} !important;">'
        f'<div class="kpi-label">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{subtext_html}'
        f'{badge_html}'
        f'</div>'
    )


def render_kpi_card(title: str, value: str, subtext: str = "",
                    border_color: str = None, badge: str = None):
    """Render a single standalone HTML-styled executive KPI card."""
    render_html(_build_kpi_card_html(title, value, subtext, border_color, badge))


def _emit_grid(card_htmls: list):
    """Emit a list of KPI card HTML strings wrapped in a single .kpi-grid CSS Grid container."""
    grid_inner = "".join(card_htmls)
    grid_html = f'<div class="kpi-grid">{grid_inner}</div>'
    render_html(grid_html)


def render_kpi_grid(kpis: dict, top5_info: dict, risk_summary: dict):
    """
    Render the standard 8-card executive KPI snapshot grid.

    Architecture (4×2, pure CSS Grid — no st.columns):
      Row 1: Core Financials    [Total Revenue | Gross Profit | Gross Margin | Total Volume]
      Row 2: Portfolio + Risk   [Product Count | Division Count | Top 5 Share | Risk-Flagged]
    """
    cards = []

    # ── Row 1: Core Financials ─────────────────────────────────────
    cards.append(_build_kpi_card_html(
        title="Total Revenue",
        value=format_currency(kpis['total_sales']),
        subtext=f"From {format_integer(kpis['total_orders'])} orders",
        border_color=PALETTE['wonka_purple']
    ))
    cards.append(_build_kpi_card_html(
        title="Gross Profit",
        value=format_currency(kpis['total_gross_profit']),
        subtext=f"Total cost: {format_currency(kpis['total_cost'])}",
        border_color=PALETTE['golden_ticket']
    ))
    cards.append(_build_kpi_card_html(
        title="Gross Margin",
        value=format_percent(kpis['gross_margin_pct']),
        subtext=f"Cost ratio: {format_percent(kpis['cost_to_sales_pct'])}",
        border_color=PALETTE['candy_pink']
    ))
    cards.append(_build_kpi_card_html(
        title="Total Volume",
        value=format_integer(kpis['total_units']),
        subtext=f"Across {format_integer(kpis['total_customers'])} customers",
        border_color=PALETTE['golden_ticket']
    ))

    # ── Row 2: Portfolio Scope, Concentration, and Risk Flags ──────
    cards.append(_build_kpi_card_html(
        title="Product Count",
        value=str(kpis['total_products']),
        subtext=f"Across {kpis['total_divisions']} operating divisions",
        border_color=PALETTE['wonka_purple']
    ))
    cards.append(_build_kpi_card_html(
        title="Division Count",
        value=f"{kpis['total_divisions']} Divisions",
        subtext=f"Covering {kpis['total_regions']} sales regions",
        border_color=PALETTE['golden_ticket']
    ))
    cards.append(_build_kpi_card_html(
        title="Top 5 Profit Share",
        value=format_percent(top5_info['top_n_profit_pct']),
        subtext=f"Revenue share: {format_percent(top5_info['top_n_revenue_pct'])}",
        border_color=PALETTE['candy_pink']
    ))
    risk_color = PALETTE['warning'] if risk_summary['flagged_count'] > 0 else PALETTE['golden_ticket']
    cards.append(_build_kpi_card_html(
        title="Risk-Flagged SKUs",
        value=f"{risk_summary['flagged_count']} / {risk_summary['total_products']}",
        subtext=f"{risk_summary['flagged_pct']:.1f}% screened for investigation",
        border_color=risk_color
    ))

    _emit_grid(cards)


def render_risk_screening_kpis(risk_summary: dict):
    """
    4-column CSS Grid for the Margin Risk Screening Metrics section.
    """
    cards = []

    cards.append(_build_kpi_card_html(
        title="Total Products Screened",
        value=str(risk_summary['total_products']),
        subtext="Portfolio-wide coverage",
        border_color=PALETTE['wonka_purple']
    ))
    flagged_badge = f"{risk_summary['flagged_pct']:.1f}% of SKUs"
    cards.append(_build_kpi_card_html(
        title="Flagged for Investigation",
        value=str(risk_summary['flagged_count']),
        subtext="Below-median margin & above-median cost ratio",
        border_color=PALETTE['warning'],
        badge=flagged_badge
    ))
    cards.append(_build_kpi_card_html(
        title="Portfolio Median Margin",
        value=f"{risk_summary['median_gm_pct']:.2f}%",
        subtext="Gross Margin % screening threshold",
        border_color=PALETTE['golden_ticket']
    ))
    cards.append(_build_kpi_card_html(
        title="Portfolio Median Cost Ratio",
        value=f"{risk_summary['median_cts_pct']:.2f}%",
        subtext="Cost-to-Sales % screening threshold",
        border_color=PALETTE['candy_pink']
    ))

    _emit_grid(cards)
