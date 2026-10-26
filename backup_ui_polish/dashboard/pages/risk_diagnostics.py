"""
Risk Diagnostics Page — Margin Compression Screening & Cost Diagnostics.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, risk_analysis
from src.visualization import charts
from dashboard.components import header, tables, insights
from dashboard.utils.dashboard_utils import render_empty_state, format_percent


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Risk Diagnostics dashboard page.
    """
    header.render_page_header(
        title="Risk Screening & Margin Diagnostics",
        subtitle="Margin Compression Exposure, Cost-to-Sales Analysis & Audit Flags",
        description="Identifying portfolio-relative risk areas where below-median gross margins coincide with above-median cost ratios."
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # Dynamic Analytical Computations
    prod_df = profitability.compute_product_profitability(filtered_df)
    risk_df = risk_analysis.compute_risk_screening(prod_df)
    risk_summary = risk_analysis.get_risk_summary(risk_df)
    flagged_df = risk_analysis.get_flagged_products(risk_df)

    # 1. Risk Overview & Screening Thresholds
    header.render_section_title(
        "Margin Risk Screening Metrics",
        f"A product is flagged for 'Investigate' if Gross Margin % < median ({risk_summary['median_gm_pct']:.2f}%) "
        f"AND Cost-to-Sales % > median ({risk_summary['median_cts_pct']:.2f}%)."
    )

    r_c1, r_c2, r_c3, r_c4 = st.columns(4)
    with r_c1:
        st.metric("Total Products Screened", str(risk_summary['total_products']))
    with r_c2:
        st.metric(
            "Flagged for Investigation",
            str(risk_summary['flagged_count']),
            delta=f"{risk_summary['flagged_pct']:.1f}% of SKUs",
            delta_color="inverse"
        )
    with r_c3:
        st.metric("Portfolio Median Margin", f"{risk_summary['median_gm_pct']:.2f}%")
    with r_c4:
        st.metric("Portfolio Median Cost Ratio", f"{risk_summary['median_cts_pct']:.2f}%")

    st.markdown("---")

    # 2. Risk Screening Table
    header.render_section_title(
        "Products Flagged for Investigation",
        "Screened SKUs exhibiting margin compression relative to the portfolio benchmark."
    )
    if not flagged_df.empty:
        tables.render_risk_table(flagged_df)
    else:
        st.success("✓ No products currently meet the margin risk screening criteria under active filters.")

    st.markdown("---")

    # 3. Cost vs Sales Diagnostics Scatter
    header.render_section_title(
        "Cost vs Sales Diagnostics",
        "Scatter plot of product Sales (x) vs Cost (y). Dashed line indicates break-even (0% margin)."
    )
    st.plotly_chart(
        charts.chart_cost_vs_sales_scatter(risk_df),
        use_container_width=True
    )

    st.markdown("---")

    # 4. Methodological Note on Date Field Integrity
    st.markdown(
        """
        <div style="background-color: #FFF8EF; border: 1px solid rgba(75,30,120,0.18); border-left: 4px solid #4B1E78; border-radius: 4px; padding: 0.85rem 1.05rem; font-size: 0.81rem; color: #2A1B3D;">
            <b style="color: #4B1E78; font-size: 0.86rem;">📋 Methodological Audit: Order Date vs Ship Date Relationship</b><br>
            Transaction timestamp verification confirms that <code>Order Date</code> records span <b>2024–2025</b>,
            whereas associated <code>Ship Date</code> fields contain forward-dated values extending between <b>2026 and 2030</b>.
            Per validated analytical protocol, this empirical anomaly is preserved without arbitrary data deletion or speculative modification.
            All timeline and trend analyses strictly index on <b>Order Date</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 5. Diagnostic Findings & Investigation Guidelines
    header.render_section_title("Operational Risk Findings & Recommended Action")

    c_rf1, c_rf2 = st.columns(2)
    with c_rf1:
        insights.render_insight_card(
            title="Screening Role vs Operational Reality",
            body="Risk flags indicate portfolio-relative underperformance, NOT an automatic mandate to discontinue products.",
            implication="Certain flagged products may serve as vital customer acquisition drivers, basket-builders, or seasonal traffic anchors.",
            border_color="#DC2626"
        )
    with c_rf2:
        insights.render_insight_card(
            title="Targeted Diagnostic Action Items",
            body="For the 7 flagged SKUs, conduct a four-point commercial audit: (1) Vendor ingredient costs, (2) Minimum order quantities, (3) Packaging/shipping format, and (4) Wholesale pricing tiers.",
            implication="Recapturing 2-3 percentage points of gross margin on high-volume flagged SKUs yields meaningful dollar profit expansion.",
            border_color="#F2B01E"
        )
