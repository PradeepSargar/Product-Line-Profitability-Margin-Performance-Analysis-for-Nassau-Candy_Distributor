"""
Executive Overview Page — Portfolio Profitability Snapshot & Key Findings.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, product_analysis, pareto, division_analysis, regional_analysis, risk_analysis
from src.visualization import charts
from dashboard.components import header, kpi_cards, insights
from dashboard.utils.dashboard_utils import render_empty_state


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Executive Overview dashboard page.

    Parameters
    ----------
    filtered_df : pd.DataFrame
        DataFrame after global sidebar filters are applied.
    full_df : pd.DataFrame
        Full dataset before filtering.
    filter_config : dict
        Current active filter settings.
    """
    header.render_page_header(
        title="Executive Overview",
        subtitle="Portfolio Profitability Snapshot & Business Concentration",
        description="High-level commercial performance across sales volume, gross profit margin, product contribution, and risk screening."
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # Dynamic Analytical Computations
    kpis = profitability.compute_overall_kpis(filtered_df)
    prod_df = profitability.compute_product_profitability(filtered_df)
    top_n = min(5, len(prod_df))
    top5_info = product_analysis.compute_top_n_contribution(prod_df, n=top_n)

    risk_df = risk_analysis.compute_risk_screening(prod_df)
    risk_summary = risk_analysis.get_risk_summary(risk_df)

    div_df = division_analysis.compute_division_summary(filtered_df)
    reg_df = regional_analysis.compute_regional_summary(filtered_df)
    reg_range = regional_analysis.compute_regional_margin_range(reg_df)

    profit_pareto_df = pareto.compute_profit_pareto(prod_df)
    monthly_df = profitability.compute_time_analysis_monthly(filtered_df)

    # 1. Global KPI Snapshot
    header.render_section_title("Global Portfolio KPIs", "Core financial metrics reflecting the current filter scope.")
    kpi_cards.render_kpi_grid(kpis, top5_info, risk_summary)

    st.markdown("---")

    # 2. Executive Visualizations
    header.render_section_title("Portfolio Drivers & Dynamics", "Visual breakdown of profit generation, contribution balance, and timeline trend.")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            charts.chart_gross_profit_by_product(prod_df.head(8)),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            charts.chart_revenue_vs_profit_contribution(prod_df.head(8)),
            use_container_width=True
        )

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            charts.chart_profit_pareto(profit_pareto_df),
            use_container_width=True
        )
    with col4:
        st.plotly_chart(
            charts.chart_monthly_sales_profit(monthly_df),
            use_container_width=True
        )

    st.markdown("---")

    # 3. Dynamic Executive Insights
    insights.render_executive_findings(kpis, top5_info, div_df, reg_range, risk_summary)
