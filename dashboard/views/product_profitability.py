"""
Product Profitability & Portfolio Intelligence Page.

Merges former Product Profitability + Strategic Analysis pages.
Covers: SKU leaderboard, margin rankings, contribution disparity,
Pareto concentration, 2×2 strategic matrix, segment summary & definitions.
"""

import streamlit as st
import pandas as pd
from src.analysis import profitability, pareto, segmentation, risk_analysis
from src.visualization import charts
from dashboard.components import header, tables, insights
from dashboard.styles import theme
from dashboard.utils.dashboard_utils import render_empty_state, format_percent


def render(filtered_df: pd.DataFrame, full_df: pd.DataFrame, filter_config: dict):
    """
    Render the Product Profitability & Portfolio Intelligence page.
    """
    header.render_page_header(
        title="Product Profitability & Portfolio Intelligence",
        subtitle="SKU Economics, Contribution Gaps, Pareto Concentration & Strategic Segmentation",
        description=(
            "End-to-end product analytics: from individual SKU margin rankings to portfolio-wide "
            "Pareto concentration and strategic quadrant segmentation."
        )
    )

    if filtered_df.empty:
        render_empty_state()
        return

    # ── Shared Computations ────────────────────────────────────────────────
    prod_df = profitability.compute_product_profitability(filtered_df)

    # Apply margin threshold filter if set
    min_margin = filter_config.get('min_margin', 0.0)
    if min_margin > 0.0:
        prod_df_thresh = prod_df[prod_df['Gross Margin %'] >= min_margin].copy()
        if not prod_df_thresh.empty:
            prod_df = prod_df_thresh
        else:
            st.warning(
                f"No products have a Gross Margin % >= {min_margin:.1f}%. Displaying all portfolio SKUs."
            )

    prod_df = segmentation.segment_products(prod_df)
    prod_df = risk_analysis.compute_risk_screening(prod_df)

    revenue_pareto_df = pareto.compute_revenue_pareto(prod_df)
    profit_pareto_df  = pareto.compute_profit_pareto(prod_df)
    concentration     = pareto.compute_concentration_metrics(prod_df)
    seg_summary_df    = segmentation.get_segment_summary(prod_df)

    # ── Section 1: Product Profitability Leaderboard ───────────────────────
    header.render_section_title(
        "Product Profitability Leaderboard",
        "Interactive portfolio table. Profit Gap (pp) highlights SKUs whose profit contribution "
        "exceeds or lags their revenue share."
    )
    tables.render_product_leaderboard(prod_df)

    theme.chart_divider()

    # ── Section 2: Gross Profit & Margin Rankings ──────────────────────────
    header.render_section_title(
        "Gross Profit & Margin Rankings",
        "Absolute dollar profit vs percentage margin efficiency — two different views of product value."
    )
    col1, col2 = st.columns(2)
    with col1:
        theme.plot_chart(charts.chart_gross_profit_by_product(prod_df))
    with col2:
        theme.plot_chart(charts.chart_gross_margin_by_product(prod_df))

    theme.chart_divider()

    # ── Section 3: Revenue vs Profit Contribution Disparity ───────────────
    header.render_section_title(
        "Revenue vs Profit Contribution Disparity",
        "Examines whether products contribute proportionally to both sales volume and gross earnings."
    )
    col3, col4 = st.columns(2)
    with col3:
        theme.plot_chart(charts.chart_revenue_vs_profit_contribution(prod_df))
    with col4:
        theme.plot_chart(charts.chart_revenue_profit_contribution_scatter(prod_df))

    theme.chart_divider()

    # ── Section 4: Pareto Concentration Analysis ───────────────────────────
    header.render_section_title(
        "Pareto Concentration Analysis (80/20 Rule)",
        "Cumulative contribution curves — portfolio dependency and SKU concentration risk."
    )

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.info(
            f"**Revenue Concentration:** **{concentration['revenue_80_count']}** of "
            f"{concentration['total_products']} products account for "
            f"**{concentration['revenue_80_cumulative_pct']:.2f}%** of total sales."
        )
    with col_m2:
        st.info(
            f"**Profit Concentration:** **{concentration['profit_80_count']}** of "
            f"{concentration['total_products']} products account for "
            f"**{concentration['profit_80_cumulative_pct']:.2f}%** of total gross profit."
        )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        theme.plot_chart(charts.chart_revenue_pareto(revenue_pareto_df))
    with col_p2:
        theme.plot_chart(charts.chart_profit_pareto(profit_pareto_df))

    theme.chart_divider()

    # ── Section 5: 2×2 Strategic Matrix ───────────────────────────────────
    header.render_section_title(
        "2×2 Strategic Product Portfolio Matrix",
        "Products mapped by Gross Margin % (x) vs Gross Profit ($) (y). "
        "Dashed lines indicate portfolio medians. Bubble sizes reflect total sales."
    )
    theme.plot_chart(charts.chart_strategic_matrix(prod_df))

    theme.chart_divider()

    # ── Section 6: Segment Summary Table ──────────────────────────────────
    header.render_section_title("Strategic Segment Performance Summary")
    tables.render_segment_table(seg_summary_df)

    theme.chart_divider()

    # ── Section 7: Segment Definitions & Tactical Guidance ────────────────
    header.render_section_title(
        "Segment Definitions & Strategic Playbook",
        "How to act on each quadrant — protect, grow, audit, or review."
    )
    insights.render_strategic_definitions()

    theme.chart_divider()

    # ── Section 8: Product-Level Analytical Observations ──────────────────
    header.render_section_title("Product-Level Analytical Observations")

    top_gp_sku      = prod_df.iloc[0] if not prod_df.empty else None
    max_margin_sku  = prod_df.sort_values('Gross Margin %', ascending=False).iloc[0] if not prod_df.empty else None
    min_margin_sku  = prod_df.sort_values('Gross Margin %', ascending=True).iloc[0]  if not prod_df.empty else None

    c_obs1, c_obs2 = st.columns(2)
    with c_obs1:
        insights.render_insight_card(
            title="Lead Commercial Driver",
            body=(
                f"<b>{top_gp_sku['Product Name'] if top_gp_sku is not None else 'N/A'}</b> produces "
                f"<b>${top_gp_sku['Gross Profit']:,.2f}</b> "
                f"({format_percent(top_gp_sku['Profit Contribution %'])}) "
                f"of total gross profit at a <b>{format_percent(top_gp_sku['Gross Margin %'])}</b> margin."
            ),
            implication=(
                "Preserving distribution volume and price stability for this SKU is "
                "paramount to company profitability."
            ),
            border_color="#F2B01E"
        )
    with c_obs2:
        insights.render_insight_card(
            title="Portfolio Margin Spread",
            body=(
                f"Gross margin spans from "
                f"<b>{format_percent(min_margin_sku['Gross Margin %'] if min_margin_sku is not None else 0)}</b> "
                f"({min_margin_sku['Product Name'] if min_margin_sku is not None else 'N/A'}) to "
                f"<b>{format_percent(max_margin_sku['Gross Margin %'] if max_margin_sku is not None else 0)}</b> "
                f"({max_margin_sku['Product Name'] if max_margin_sku is not None else 'N/A'})."
            ),
            implication=(
                "Significant margin dispersion confirms that commercial mix — not geography — "
                "governs portfolio profitability."
            ),
            border_color="#4B1E78"
        )
