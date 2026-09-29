"""
Strategic Analysis Page — Concentration (Pareto) & 2×2 Product Matrix.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, pareto, segmentation
from src.visualization import charts
from dashboard.components import header, tables, insights
from dashboard.utils.dashboard_utils import render_empty_state, format_percent


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Strategic Analysis dashboard page.
    """
    header.render_page_header(
        title="Strategic Portfolio Analysis",
        subtitle="Pareto Concentration (80/20) & 2×2 Strategic Matrix",
        description="Assessing portfolio concentration risk and categorizing SKUs into Core Drivers, Volume Drivers, Niche Gems, and Underperformers."
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # Dynamic Analytical Computations
    prod_df = profitability.compute_product_profitability(filtered_df)
    prod_df = segmentation.segment_products(prod_df)

    revenue_pareto_df = pareto.compute_revenue_pareto(prod_df)
    profit_pareto_df = pareto.compute_profit_pareto(prod_df)
    concentration_metrics = pareto.compute_concentration_metrics(prod_df)
    seg_summary_df = segmentation.get_segment_summary(prod_df)

    # 1. Concentration Metrics & Pareto Curves
    header.render_section_title(
        "Pareto Concentration Analysis",
        "Evaluating portfolio dependency: cumulative contribution curves highlighting the 80% threshold."
    )

    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.info(
            f"**Revenue Concentration:** **{concentration_metrics['revenue_80_count']}** of "
            f"{concentration_metrics['total_products']} products account for "
            f"**{concentration_metrics['revenue_80_cumulative_pct']:.2f}%** of total sales."
        )
    with col_meta2:
        st.info(
            f"**Profit Concentration:** **{concentration_metrics['profit_80_count']}** of "
            f"{concentration_metrics['total_products']} products account for "
            f"**{concentration_metrics['profit_80_cumulative_pct']:.2f}%** of total gross profit."
        )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.plotly_chart(
            charts.chart_revenue_pareto(revenue_pareto_df),
            use_container_width=True
        )
    with col_p2:
        st.plotly_chart(
            charts.chart_profit_pareto(profit_pareto_df),
            use_container_width=True
        )

    st.markdown("---")

    # 2. Strategic Product Portfolio Matrix (2x2)
    header.render_section_title(
        "2×2 Strategic Product Portfolio Matrix",
        "Products mapped by Gross Margin % (x) vs Gross Profit ($) (y). "
        "Dashed lines indicate portfolio medians. Bubble sizes reflect total sales."
    )
    st.plotly_chart(
        charts.chart_strategic_matrix(prod_df),
        use_container_width=True
    )

    # 3. Supporting Segment Summary Table
    header.render_section_title("Strategic Segment Performance Summary")
    tables.render_segment_table(seg_summary_df)

    st.markdown("---")

    # 4. Strategic Definitions & Tactical Guidance
    header.render_section_title("Segment Definitions & Strategic Recommendations")
    insights.render_strategic_definitions()
