"""
Reusable insight components, findings cards, and strategic implications.
"""

import streamlit as st
import pandas as pd
from dashboard.utils.dashboard_utils import format_currency, format_percent

# ── Golden Ticket palette aliases (avoids circular import from theme.py) ──
_PURPLE  = "#4B1E78"
_GOLD    = "#F2B01E"
_PINK    = "#E6427A"
_DARK    = "#2A1B3D"
_MUTED   = "#7A6C8A"
_WARNING = "#DC2626"


def render_insight_card(title: str, body: str, implication: str = None, border_color: str = None):
    """
    Render a single styled business insight card with optional implication.
    border_color defaults to Wonka Purple if not supplied.
    """
    _border = border_color if border_color else _PURPLE
    html = f"""
    <div class="insight-card" style="border-left-color: {_border};">
        <h4>{title}</h4>
        <p>{body}</p>
        {f'<p style="margin-top: 0.35rem; font-size: 0.79rem; color: {_MUTED};"><b>Business Implication:</b> {implication}</p>' if implication else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_executive_findings(kpis: dict, top5_info: dict, div_df: pd.DataFrame, reg_range: dict, risk_summary: dict):
    """
    Render dynamic executive findings and strategic implications grid.
    """
    if not div_df.empty:
        top_div = div_df.iloc[0]
        top_div_name = top_div['Division']
        top_div_gp_pct = top_div['Profit Contribution %']
        top_div_sales_pct = top_div['Revenue Contribution %']
    else:
        top_div_name, top_div_gp_pct, top_div_sales_pct = "N/A", 0.0, 0.0

    top_sku = top5_info['top_profit_products'][0] if top5_info['top_profit_products'] else "N/A"

    col1, col2 = st.columns(2)

    with col1:
        render_insight_card(
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
        )

        render_insight_card(
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
        )

    with col2:
        margin_spread = reg_range.get('margin_range_pp', 0.0)
        min_reg = reg_range.get('min_region', 'N/A')
        max_reg = reg_range.get('max_region', 'N/A')
        min_m = reg_range.get('min_margin', 0.0)
        max_m = reg_range.get('max_margin', 0.0)

        render_insight_card(
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
        )

        render_insight_card(
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
        )


def render_strategic_definitions():
    """Render 4-quadrant strategic definition cards using the Golden Ticket palette."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid rgba(242,176,30,0.35); border-top: 4px solid {_GOLD}; border-radius: 6px; padding: 0.8rem; height: 100%;">
                <b style="color: {_PURPLE};">Core Drivers</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">High Profit / High Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Key portfolio pillars driving healthy margins. Protect supply continuity, prevent stockouts, and prioritize shelf placement.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid rgba(75,30,120,0.18); border-top: 4px solid {_PURPLE}; border-radius: 6px; padding: 0.8rem; height: 100%;">
                <b style="color: {_PURPLE};">Volume Drivers</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">High Profit / Low Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Substantial transaction volume generates strong gross profit despite below-median margin rates. Audit freight and packaging to capture margin points.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid rgba(230,66,122,0.2); border-top: 4px solid {_PINK}; border-radius: 6px; padding: 0.8rem; height: 100%;">
                <b style="color: {_PURPLE};">Niche Gems</b><br>
                <span style="font-size: 0.76rem; color: {_MUTED};">Low Profit / High Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Strong unit-level economics constrained by limited customer reach. Prime candidates for targeted distribution and marketing pushes.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div style="background-color: #FEF2F2; border: 1px solid rgba(220,38,38,0.22); border-top: 4px solid {_WARNING}; border-radius: 6px; padding: 0.8rem; height: 100%;">
                <b style="color: {_WARNING};">Underperformers</b><br>
                <span style="font-size: 0.76rem; color: {_WARNING};">Low Profit / Low Margin</span>
                <p style="font-size: 0.79rem; color: {_DARK}; margin-top: 0.35rem; line-height: 1.35;">
                    Deliver below-median profit and margin. Note: Classification is an analytical screening indicator, not an immediate discontinuation order.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
