"""
Reusable executive KPI card and grid components.
Styled with the Golden Ticket palette: white card, 5px gold left border, rounded corners, soft shadow.
"""

import streamlit as st
from theme import PALETTE
from dashboard.utils.dashboard_utils import format_currency, format_percent, format_integer


def render_kpi_card(title: str, value: str, subtext: str = "", border_color: str = None):
    """
    Render a single HTML-styled executive KPI card.

    Parameters
    ----------
    title : str
        Metric uppercase label.
    value : str
        Prominently displayed formatted value.
    subtext : str
        Contextual subtitle or baseline comparison.
    border_color : str
        Accent left border color (defaults to Golden Ticket #F2B01E).
    """
    accent_border = border_color if border_color else PALETTE['golden_ticket']

    card_html = f"""
    <div class="kpi-card" style="border-left: 5px solid {accent_border} !important;">
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_kpi_grid(kpis: dict, top5_info: dict, risk_summary: dict):
    """
    Render the standard 8-card executive KPI snapshot grid.
    """
    # Row 1: Core Financials
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_kpi_card(
            title="Total Revenue",
            value=format_currency(kpis['total_sales']),
            subtext=f"From {format_integer(kpis['total_orders'])} orders",
            border_color=PALETTE['wonka_purple']
        )

    with c2:
        render_kpi_card(
            title="Gross Profit",
            value=format_currency(kpis['total_gross_profit']),
            subtext=f"Total cost: {format_currency(kpis['total_cost'])}",
            border_color=PALETTE['golden_ticket']
        )

    with c3:
        render_kpi_card(
            title="Gross Margin",
            value=format_percent(kpis['gross_margin_pct']),
            subtext=f"Cost ratio: {format_percent(kpis['cost_to_sales_pct'])}",
            border_color=PALETTE['candy_pink']
        )

    with c4:
        render_kpi_card(
            title="Total Volume",
            value=format_integer(kpis['total_units']),
            subtext=f"Across {format_integer(kpis['total_customers'])} customers",
            border_color=PALETTE['golden_ticket']
        )

    # Row 2: Portfolio Scope, Concentration, and Risk Flags
    c5, c6, c7, c8 = st.columns(4)

    with c5:
        render_kpi_card(
            title="Product Count",
            value=str(kpis['total_products']),
            subtext=f"Across {kpis['total_divisions']} operating divisions",
            border_color=PALETTE['wonka_purple']
        )

    with c6:
        render_kpi_card(
            title="Division Count",
            value=f"{kpis['total_divisions']} Divisions",
            subtext=f"Covering {kpis['total_regions']} sales regions",
            border_color=PALETTE['golden_ticket']
        )

    with c7:
        render_kpi_card(
            title="Top 5 Profit Share",
            value=format_percent(top5_info['top_n_profit_pct']),
            subtext=f"Revenue share: {format_percent(top5_info['top_n_revenue_pct'])}",
            border_color=PALETTE['candy_pink']
        )

    with c8:
        risk_color = PALETTE['warning'] if risk_summary['flagged_count'] > 0 else PALETTE['golden_ticket']
        render_kpi_card(
            title="Risk-Flagged SKUs",
            value=f"{risk_summary['flagged_count']} / {risk_summary['total_products']}",
            subtext=f"{risk_summary['flagged_pct']:.1f}% screened for investigation",
            border_color=risk_color
        )
