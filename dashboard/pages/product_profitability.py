"""
Product Profitability Page — SKU Economics, Contribution & Leaderboard.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, segmentation, risk_analysis
from src.visualization import charts
from dashboard.components import header, tables, insights
from dashboard.utils.dashboard_utils import render_empty_state, format_percent


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Product Profitability dashboard page.
    """
    header.render_page_header(
        title="Product Profitability & Contribution",
        subtitle="Individual SKU Performance, Margin Spreads & Contribution Gaps",
        description="Detailed product economics identifying top gross profit generators, margin outliers, and contribution disparities."
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # Dynamic Analytical Computations
    prod_df = profitability.compute_product_profitability(filtered_df)

    # Apply margin threshold filter if set
    min_margin = filter_config.get('min_margin', 0.0)
    if min_margin > 0.0:
        prod_df_thresh = prod_df[prod_df['Gross Margin %'] >= min_margin].copy()
        if not prod_df_thresh.empty:
            prod_df = prod_df_thresh
        else:
            st.warning(f"No products have a Gross Margin % >= {min_margin:.1f}%. Displaying all portfolio SKUs.")

    prod_df = segmentation.segment_products(prod_df)
    prod_df = risk_analysis.compute_risk_screening(prod_df)

    # 1. Product Profitability Leaderboard Table
    header.render_section_title(
        "Product Profitability Leaderboard",
        "Interactive portfolio table. Click column headers to sort. "
        "Profit Gap (pp) highlights SKUs whose profit contribution exceeds or lags their revenue contribution."
    )
    tables.render_product_leaderboard(prod_df)

    st.markdown("---")

    # 2. Product Rankings
    header.render_section_title(
        "Gross Profit & Margin Rankings",
        "Comparing absolute dollar profit against percentage margin efficiency."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            charts.chart_gross_profit_by_product(prod_df),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            charts.chart_gross_margin_by_product(prod_df),
            use_container_width=True
        )

    st.markdown("---")

    # 3. Revenue vs Profit Contribution Comparison
    header.render_section_title(
        "Revenue vs Profit Contribution Disparity",
        "Examines whether products contribute proportionally to both sales volume and gross earnings."
    )
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            charts.chart_revenue_vs_profit_contribution(prod_df),
            use_container_width=True
        )
    with col4:
        st.plotly_chart(
            charts.chart_revenue_profit_contribution_scatter(prod_df),
            use_container_width=True
        )

    st.markdown("---")

    # 4. Product Profitability Matrix
    header.render_section_title(
        "Product Profitability Matrix",
        "2×2 view mapping product Gross Margin % against Gross Profit ($)."
    )
    st.plotly_chart(
        charts.chart_strategic_matrix(prod_df),
        use_container_width=True
    )

    # 5. Product-Level Analytical Findings
    st.markdown("---")
    header.render_section_title("Product-Level Analytical Observations")

    top_gp_sku = prod_df.iloc[0] if not prod_df.empty else None
    max_margin_sku = prod_df.sort_values('Gross Margin %', ascending=False).iloc[0] if not prod_df.empty else None
    min_margin_sku = prod_df.sort_values('Gross Margin %', ascending=True).iloc[0] if not prod_df.empty else None

    c_obs1, c_obs2 = st.columns(2)
    with c_obs1:
        insights.render_insight_card(
            title="Lead Commercial Driver",
            body=(
                f"<b>{top_gp_sku['Product Name'] if top_gp_sku is not None else 'N/A'}</b> produces "
                f"<b>${top_gp_sku['Gross Profit']:,.2f}</b> ({format_percent(top_gp_sku['Profit Contribution %'])}) "
                f"of total gross profit at a <b>{format_percent(top_gp_sku['Gross Margin %'])}</b> margin."
            ),
            implication="Preserving distribution volume and price stability for this SKU is paramount to company profitability.",
            border_color="#F2B01E"
        )
    with c_obs2:
        insights.render_insight_card(
            title="Margin Range Across SKUs",
            body=(
                f"Gross margin across products spans from <b>{format_percent(min_margin_sku['Gross Margin %'] if min_margin_sku is not None else 0)}</b> "
                f"({min_margin_sku['Product Name'] if min_margin_sku is not None else 'N/A'}) to "
                f"<b>{format_percent(max_margin_sku['Gross Margin %'] if max_margin_sku is not None else 0)}</b> "
                f"({max_margin_sku['Product Name'] if max_margin_sku is not None else 'N/A'})."
            ),
            implication="Product-level margin dispersion is significant, underscoring that commercial mix rather than geography governs profitability.",
            border_color="#4B1E78"
        )
