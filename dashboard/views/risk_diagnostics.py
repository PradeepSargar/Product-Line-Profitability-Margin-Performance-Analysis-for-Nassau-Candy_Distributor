"""
Risk & Business Performance Page.

Merges former Risk Diagnostics + Business Performance pages.
Covers: margin risk screening, flagged SKUs, cost-vs-sales diagnostics,
division breakdown, regional breakdown, margin distribution, longitudinal trends.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, risk_analysis, division_analysis, regional_analysis
from src.visualization import charts
from dashboard.components import header, tables, insights, kpi_cards
from dashboard.styles import theme
from dashboard.utils.dashboard_utils import render_empty_state, format_percent, render_html


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Risk Screening & Business Performance page.
    """
    header.render_page_header(
        title="Risk Screening & Business Performance",
        subtitle="Margin Risk Diagnostics, Division Breakdown, Regional Stability & Longitudinal Trends",
        description=(
            "Unified operational health view: identifies margin-compressed SKUs, "
            "dissects business unit contributions, and tracks performance over time."
        )
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # ── Shared Computations ────────────────────────────────────────────────
    prod_df    = profitability.compute_product_profitability(filtered_df)
    risk_df    = risk_analysis.compute_risk_screening(prod_df)
    risk_summary = risk_analysis.get_risk_summary(risk_df)
    flagged_df = risk_analysis.get_flagged_products(risk_df)

    div_df  = division_analysis.compute_division_summary(filtered_df)
    reg_df  = regional_analysis.compute_regional_summary(filtered_df)
    reg_range = regional_analysis.compute_regional_margin_range(reg_df)

    monthly_df = profitability.compute_time_analysis_monthly(filtered_df)
    yearly_df  = profitability.compute_time_analysis_yearly(filtered_df)

    # ── Section 1: Risk Overview KPIs ─────────────────────────────────────
    header.render_section_title(
        "Margin Risk Screening Metrics",
        f"A product is flagged 'Investigate' if Gross Margin % < median "
        f"({risk_summary['median_gm_pct']:.2f}%) AND Cost-to-Sales % > median "
        f"({risk_summary['median_cts_pct']:.2f}%)."
    )
    kpi_cards.render_risk_screening_kpis(risk_summary)

    theme.chart_divider()

    # ── Section 2: Flagged Products Table ─────────────────────────────────
    header.render_section_title(
        "Products Flagged for Investigation",
        "SKUs exhibiting margin compression relative to the portfolio benchmark."
    )
    if not flagged_df.empty:
        tables.render_risk_table(flagged_df)
    else:
        st.success("✓ No products currently meet the margin risk screening criteria under active filters.")

    theme.chart_divider()

    # ── Section 3: Cost vs Sales Scatter ──────────────────────────────────
    header.render_section_title(
        "Cost vs Sales Diagnostics",
        "Scatter plot of product Sales (x) vs Cost (y). Dashed line indicates break-even (0% margin)."
    )
    theme.plot_chart(charts.chart_cost_vs_sales_scatter(risk_df))

    theme.chart_divider()

    # ── Section 4: Risk Findings ───────────────────────────────────────────
    header.render_section_title("Operational Risk Findings & Recommended Action")

    c_rf1, c_rf2 = st.columns(2)
    with c_rf1:
        insights.render_insight_card(
            title="Screening Role vs Operational Reality",
            body="Risk flags indicate portfolio-relative underperformance, NOT an automatic mandate to discontinue products.",
            implication=(
                "Certain flagged products may serve as vital customer acquisition drivers, "
                "basket-builders, or seasonal traffic anchors."
            ),
            border_color="#DC2626"
        )
    with c_rf2:
        insights.render_insight_card(
            title="Targeted Diagnostic Action Items",
            body=(
                "For the 7 flagged SKUs, conduct a four-point commercial audit: "
                "(1) Vendor ingredient costs, (2) Minimum order quantities, "
                "(3) Packaging/shipping format, and (4) Wholesale pricing tiers."
            ),
            implication=(
                "Recapturing 2–3 percentage points of gross margin on high-volume "
                "flagged SKUs yields meaningful dollar profit expansion."
            ),
            border_color="#F2B01E"
        )

    theme.chart_divider()

    # ── Section 5: Division Breakdown ─────────────────────────────────────
    header.render_section_title(
        "Operating Division Breakdown",
        "Performance summary across commercial operating divisions."
    )
    tables.render_division_table(div_df)

    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        theme.plot_chart(charts.chart_division_revenue_vs_profit(div_df))
    with col_d2:
        theme.plot_chart(charts.chart_division_margin_comparison(div_df))
    with col_d3:
        theme.plot_chart(charts.chart_division_profit_contribution(div_df))

    theme.chart_divider()

    # ── Section 6: Regional Breakdown ─────────────────────────────────────
    header.render_section_title(
        "Geographic Regional Performance",
        f"Commercial sales across territories. "
        f"Regional margin spread: {reg_range['margin_range_pp']:.2f} pp."
    )
    tables.render_regional_table(reg_df)

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        theme.plot_chart(charts.chart_regional_gross_profit(reg_df))
    with col_r2:
        theme.plot_chart(charts.chart_regional_gross_margin(reg_df))
    with col_r3:
        theme.plot_chart(charts.chart_regional_revenue_vs_profit(reg_df))

    theme.chart_divider()

    # ── Section 7: Margin Distribution (Transaction Level) ────────────────
    header.render_section_title(
        "Transaction-Level Gross Margin Dispersion",
        "Box plots displaying margin distributions at order level — reveals pricing consistency."
    )
    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        theme.plot_chart(charts.chart_margin_distribution(filtered_df, group_col='Division'))
    with col_dist2:
        theme.plot_chart(charts.chart_margin_distribution(filtered_df, group_col='Region'))

    theme.chart_divider()

    # ── Section 8: Longitudinal Performance Trends ────────────────────────
    header.render_section_title(
        "Longitudinal Timeline Performance",
        "Monthly trajectories and yearly growth comparisons."
    )
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        theme.plot_chart(charts.chart_monthly_sales_profit(monthly_df))
    with col_t2:
        theme.plot_chart(charts.chart_monthly_margin(monthly_df))

    theme.chart_divider()

    col_t3, col_t4 = st.columns(2)
    with col_t3:
        theme.plot_chart(charts.chart_yearly_comparison(yearly_df))
    with col_t4:
        theme.plot_chart(charts.chart_yearly_margin(yearly_df))

    theme.chart_divider()

    # ── Section 9: Business Comparison Findings ────────────────────────────
    header.render_section_title("Business Performance Observations")

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        insights.render_insight_card(
            title="Division Skew & Strategic Risk",
            body="Chocolate accounts for over 95% of gross profit. Sugar and Other carry narrower volume or compressed margins.",
            implication=(
                "Evaluating pricing power and supplier arrangements in secondary divisions "
                "could unlock incremental portfolio margin points."
            ),
            border_color="#4B1E78"
        )
    with c_b2:
        insights.render_insight_card(
            title="Uniform Pricing Execution Across Regions",
            body=f"Regional gross margins are exceptionally consistent (spread of {reg_range['margin_range_pp']:.2f} pp).",
            implication=(
                "National pricing discipline is well-maintained; regional teams do not "
                "exhibit detrimental localized discounting."
            ),
            border_color="#E6427A"
        )

    theme.chart_divider()

    # ── Methodological Audit Note ──────────────────────────────────────────
    render_html("""
        <div style="background-color: #FFF8EF; border: 1px solid rgba(75,30,120,0.18); border-left: 4px solid #4B1E78; border-radius: 4px; padding: 0.85rem 1.05rem; font-size: 0.81rem; color: #2A1B3D;">
            <b style="color: #4B1E78; font-size: 0.86rem;">📋 Methodological Audit: Order Date vs Ship Date Relationship</b><br>
            Transaction timestamp verification confirms that <code>Order Date</code> records span <b>2024–2025</b>,
            whereas associated <code>Ship Date</code> fields contain forward-dated values extending between <b>2026 and 2030</b>.
            Per validated analytical protocol, this empirical anomaly is preserved without arbitrary data deletion or speculative modification.
            All timeline and trend analyses strictly index on <b>Order Date</b>.
        </div>
    """)
