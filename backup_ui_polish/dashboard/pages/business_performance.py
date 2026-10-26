"""
Business Performance Page — Division, Regional & Longitudinal Timeline Performance.
"""

import streamlit as st
import pandas as pd
from src.analysis import division_analysis, regional_analysis, profitability
from src.visualization import charts
from dashboard.components import header, tables, insights
from dashboard.utils.dashboard_utils import render_empty_state, format_percent


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Business Performance dashboard page.
    """
    header.render_page_header(
        title="Business Performance",
        subtitle="Division Asymmetry, Regional Stability & Longitudinal Trends",
        description="Comprehensive evaluation of business unit contributions, territory margin consistency, and yearly/monthly performance."
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # Dynamic Analytical Computations
    div_df = division_analysis.compute_division_summary(filtered_df)
    reg_df = regional_analysis.compute_regional_summary(filtered_df)
    reg_range = regional_analysis.compute_regional_margin_range(reg_df)

    monthly_df = profitability.compute_time_analysis_monthly(filtered_df)
    yearly_df = profitability.compute_time_analysis_yearly(filtered_df)

    # 1. Division Performance
    header.render_section_title("Operating Division Breakdown", "Performance summary across commercial operating divisions.")
    tables.render_division_table(div_df)

    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.plotly_chart(
            charts.chart_division_revenue_vs_profit(div_df),
            use_container_width=True
        )
    with col_d2:
        st.plotly_chart(
            charts.chart_division_margin_comparison(div_df),
            use_container_width=True
        )
    with col_d3:
        st.plotly_chart(
            charts.chart_division_profit_contribution(div_df),
            use_container_width=True
        )

    st.markdown("---")

    # 2. Regional Performance
    header.render_section_title(
        "Geographic Regional Performance",
        f"Commercial sales across territories. Note: Regional margin spread is only {reg_range['margin_range_pp']:.2f} percentage points."
    )
    tables.render_regional_table(reg_df)

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.plotly_chart(
            charts.chart_regional_gross_profit(reg_df),
            use_container_width=True
        )
    with col_r2:
        st.plotly_chart(
            charts.chart_regional_gross_margin(reg_df),
            use_container_width=True
        )
    with col_r3:
        st.plotly_chart(
            charts.chart_regional_revenue_vs_profit(reg_df),
            use_container_width=True
        )

    st.markdown("---")

    # 3. Transaction-Level Margin Distribution
    header.render_section_title("Gross Margin Dispersion", "Box plots displaying transaction-level margin distributions.")
    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        st.plotly_chart(
            charts.chart_margin_distribution(filtered_df, group_col='Division'),
            use_container_width=True
        )
    with col_dist2:
        st.plotly_chart(
            charts.chart_margin_distribution(filtered_df, group_col='Region'),
            use_container_width=True
        )

    st.markdown("---")

    # 4. Longitudinal Performance Trends
    header.render_section_title("Longitudinal Timeline Performance", "Tracking monthly trajectories and yearly growth comparisons.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.plotly_chart(
            charts.chart_monthly_sales_profit(monthly_df),
            use_container_width=True
        )
    with col_t2:
        st.plotly_chart(
            charts.chart_monthly_margin(monthly_df),
            use_container_width=True
        )

    col_t3, col_t4 = st.columns(2)
    with col_t3:
        st.plotly_chart(
            charts.chart_yearly_comparison(yearly_df),
            use_container_width=True
        )
    with col_t4:
        st.plotly_chart(
            charts.chart_yearly_margin(yearly_df),
            use_container_width=True
        )

    # 5. Business Comparison Findings
    st.markdown("---")
    header.render_section_title("Business Comparison Observations")

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        insights.render_insight_card(
            title="Division Skew & Strategic Risk",
            body="Chocolate accounts for over 95% of gross profit. Other lines (Sugar and Other) carry narrower volume or compressed margins.",
            implication="Evaluating pricing power and supplier arrangements in the 'Other' division could unlock incremental portfolio margin points.",
            border_color="#4B1E78"
        )
    with c_b2:
        insights.render_insight_card(
            title="Uniform Pricing Execution Across Regions",
            body=f"Regional gross margins are exceptionally consistent (spread of {reg_range['margin_range_pp']:.2f} pp).",
            implication="National pricing discipline is well-maintained; regional teams do not exhibit detrimental localized discounting.",
            border_color="#E6427A"
        )
