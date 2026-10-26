"""
Executive Themed Tables & Interactive Grids for Nassau Candy Analytics Dashboard.
Styled strictly with the Golden Ticket design system:
- Deep Wonka Purple header with Gold accent line
- Alternating clean rows with subtle gold hover
- Status badges for Segments (Core Driver, Volume Driver, Niche Gem, Underperformer)
- Risk pills (Investigate, Monitor, Stable)
- Right-aligned monospaced financial metrics
"""

import streamlit as st
import pandas as pd
from dashboard.utils.dashboard_utils import (
    format_currency,
    format_percent,
    format_integer,
    render_html,
)


def _get_segment_badge(segment_str: str) -> str:
    """Return styled HTML pill for strategic segments."""
    seg = str(segment_str).strip()
    if "Core" in seg:
        return '<span class="tbl-badge tbl-badge-gold">⭐ Core Driver</span>'
    elif "Volume" in seg:
        return '<span class="tbl-badge tbl-badge-purple">📦 Volume Driver</span>'
    elif "Niche" in seg:
        return '<span class="tbl-badge tbl-badge-pink">💎 Niche Gem</span>'
    elif "Underperformer" in seg:
        return '<span class="tbl-badge tbl-badge-risk">⚠️ Underperformer</span>'
    return f'<span class="tbl-badge tbl-badge-gold">{seg}</span>'


def _get_risk_badge(risk_str: str) -> str:
    """Return styled HTML pill for risk status."""
    risk = str(risk_str).strip()
    if "Investigate" in risk or "At Risk" in risk or "Flagged" in risk:
        return '<span class="tbl-badge tbl-badge-risk">🚨 Investigate</span>'
    elif "Monitor" in risk:
        return '<span class="tbl-badge tbl-badge-amber">🔍 Monitor</span>'
    return '<span class="tbl-badge tbl-badge-green">✓ Stable</span>'


def _format_gap_cell(gap_val: float) -> str:
    """Format profit vs revenue gap percentage points with color indicator."""
    if gap_val is None or pd.isna(gap_val):
        return "0.00 pp"
    if gap_val > 0.05:
        return f'<span style="color: #15803D; font-weight: 600;">+{gap_val:.2f} pp</span>'
    elif gap_val < -0.05:
        return f'<span style="color: #DC2626; font-weight: 600;">{gap_val:.2f} pp</span>'
    return f'<span style="color: #7A6C8A;">{gap_val:+.2f} pp</span>'


def render_division_table(div_df: pd.DataFrame):
    """Render formatted division performance summary table in Golden Ticket theme."""
    if div_df.empty:
        st.info("No division data available for current selection.")
        return

    rows_html = []
    for _, row in div_df.iterrows():
        div_name = row.get("Division", "")
        sales = format_currency(row.get("Sales", 0.0))
        cost = format_currency(row.get("Cost", 0.0))
        gp = format_currency(row.get("Gross Profit", 0.0))
        gm = format_percent(row.get("Gross Margin %", 0.0))
        cts = format_percent(row.get("Cost-to-Sales %", 0.0))
        units = format_integer(row.get("Units", 0))
        orders = format_integer(row.get("Orders", 0))
        rev_share = format_percent(row.get("Revenue Contribution %", 0.0))
        profit_share = format_percent(row.get("Profit Contribution %", 0.0))
        gap = _format_gap_cell(row.get("Profit vs Revenue Gap pp", 0.0))

        rows_html.append(f"""
            <tr>
                <td class="primary-cell"><b>{div_name}</b></td>
                <td class="num-col">{sales}</td>
                <td class="num-col">{cost}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{gp}</td>
                <td class="num-col" style="font-weight: 600;">{gm}</td>
                <td class="num-col">{cts}</td>
                <td class="num-col">{units}</td>
                <td class="num-col">{orders}</td>
                <td class="num-col">{rev_share}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{profit_share}</td>
                <td class="num-col">{gap}</td>
            </tr>
        """)

    table_html = f"""
        <div class="executive-table-container">
            <table class="executive-table">
                <thead>
                    <tr>
                        <th>Operating Division</th>
                        <th class="num-col">Total Sales</th>
                        <th class="num-col">Total Cost</th>
                        <th class="num-col">Gross Profit</th>
                        <th class="num-col">Gross Margin</th>
                        <th class="num-col">Cost Ratio</th>
                        <th class="num-col">Units Sold</th>
                        <th class="num-col">Orders</th>
                        <th class="num-col">Revenue Share</th>
                        <th class="num-col">Profit Share</th>
                        <th class="num-col">Profit Gap</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    render_html(table_html)


def render_regional_table(reg_df: pd.DataFrame):
    """Render formatted regional performance summary table in Golden Ticket theme."""
    if reg_df.empty:
        st.info("No regional data available for current selection.")
        return

    rows_html = []
    for _, row in reg_df.iterrows():
        reg_name = row.get("Region", "")
        sales = format_currency(row.get("Sales", 0.0))
        cost = format_currency(row.get("Cost", 0.0))
        gp = format_currency(row.get("Gross Profit", 0.0))
        gm = format_percent(row.get("Gross Margin %", 0.0))
        cts = format_percent(row.get("Cost-to-Sales %", 0.0))
        units = format_integer(row.get("Units", 0))
        orders = format_integer(row.get("Orders", 0))
        customers = format_integer(row.get("Customers", 0))
        rev_share = format_percent(row.get("Revenue Contribution %", 0.0))
        profit_share = format_percent(row.get("Profit Contribution %", 0.0))
        gap = _format_gap_cell(row.get("Profit vs Revenue Gap pp", 0.0))

        rows_html.append(f"""
            <tr>
                <td class="primary-cell"><b>{reg_name}</b></td>
                <td class="num-col">{sales}</td>
                <td class="num-col">{cost}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{gp}</td>
                <td class="num-col" style="font-weight: 600;">{gm}</td>
                <td class="num-col">{cts}</td>
                <td class="num-col">{units}</td>
                <td class="num-col">{orders}</td>
                <td class="num-col">{customers}</td>
                <td class="num-col">{rev_share}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{profit_share}</td>
                <td class="num-col">{gap}</td>
            </tr>
        """)

    table_html = f"""
        <div class="executive-table-container">
            <table class="executive-table">
                <thead>
                    <tr>
                        <th>Sales Region</th>
                        <th class="num-col">Total Sales</th>
                        <th class="num-col">Total Cost</th>
                        <th class="num-col">Gross Profit</th>
                        <th class="num-col">Gross Margin</th>
                        <th class="num-col">Cost Ratio</th>
                        <th class="num-col">Units Sold</th>
                        <th class="num-col">Orders</th>
                        <th class="num-col">Customers</th>
                        <th class="num-col">Revenue Share</th>
                        <th class="num-col">Profit Share</th>
                        <th class="num-col">Profit Gap</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    render_html(table_html)


def render_segment_table(seg_summary_df: pd.DataFrame):
    """Render formatted 4-quadrant strategic segment summary table with badges."""
    if seg_summary_df.empty:
        st.info("No strategic segment data available.")
        return

    rows_html = []
    for _, row in seg_summary_df.iterrows():
        segment_badge = _get_segment_badge(row.get("Segment", ""))
        products = format_integer(row.get("Products", 0))
        sales = format_currency(row.get("Sales", 0.0))
        gp = format_currency(row.get("Gross Profit", 0.0))
        avg_gm = format_percent(row.get("Avg Gross Margin %", 0.0))
        rev_share = format_percent(row.get("Revenue Share %", 0.0))
        profit_share = format_percent(row.get("Profit Share %", 0.0))

        rows_html.append(f"""
            <tr>
                <td>{segment_badge}</td>
                <td class="num-col" style="font-weight: 600;">{products} SKUs</td>
                <td class="num-col">{sales}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{gp}</td>
                <td class="num-col" style="font-weight: 600;">{avg_gm}</td>
                <td class="num-col">{rev_share}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{profit_share}</td>
            </tr>
        """)

    table_html = f"""
        <div class="executive-table-container">
            <table class="executive-table">
                <thead>
                    <tr>
                        <th>Strategic Segment</th>
                        <th class="num-col">Product Count</th>
                        <th class="num-col">Total Sales</th>
                        <th class="num-col">Gross Profit</th>
                        <th class="num-col">Avg Gross Margin</th>
                        <th class="num-col">Revenue Share</th>
                        <th class="num-col">Profit Share</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    render_html(table_html)


def render_risk_table(risk_df: pd.DataFrame):
    """Render formatted table of risk-screened products with risk badges."""
    df = risk_df.copy()
    if df.empty:
        st.success("✓ No products currently meet the margin risk screening criteria under active filters.")
        return

    rows_html = []
    for _, row in df.iterrows():
        prod_name = row.get("Product Name", "")
        div_name = row.get("Division", "")
        sales = format_currency(row.get("Sales", 0.0))
        cost = format_currency(row.get("Cost", 0.0))
        gp = format_currency(row.get("Gross Profit", 0.0))
        gm = format_percent(row.get("Gross Margin %", 0.0))
        cts = format_percent(row.get("Cost-to-Sales %", 0.0))
        units = format_integer(row.get("Units", 0))
        risk_badge = _get_risk_badge(row.get("Risk Status", "Investigate"))

        rows_html.append(f"""
            <tr>
                <td class="primary-cell"><b>{prod_name}</b></td>
                <td><span class="tbl-badge tbl-badge-purple">{div_name}</span></td>
                <td class="num-col">{sales}</td>
                <td class="num-col">{cost}</td>
                <td class="num-col" style="font-weight: 600; color: #4B1E78;">{gp}</td>
                <td class="num-col" style="font-weight: 600; color: #DC2626;">{gm}</td>
                <td class="num-col">{cts}</td>
                <td class="num-col">{units}</td>
                <td>{risk_badge}</td>
            </tr>
        """)

    table_html = f"""
        <div class="executive-table-container">
            <table class="executive-table">
                <thead>
                    <tr>
                        <th>Flagged Product SKU</th>
                        <th>Division</th>
                        <th class="num-col">Total Sales</th>
                        <th class="num-col">Total Cost</th>
                        <th class="num-col">Gross Profit</th>
                        <th class="num-col">Gross Margin</th>
                        <th class="num-col">Cost-to-Sales %</th>
                        <th class="num-col">Units Sold</th>
                        <th>Risk Screening Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    """
    render_html(table_html)


def render_product_leaderboard(product_df: pd.DataFrame, height: int = 500):
    """
    Render executive-styled dual-view product profitability leaderboard.
    - View 1: Top 10 Executive Leaderboard with Segment & Risk badges
    - View 2: Complete Interactive Data Explorer (all SKUs with sortable columns)
    """
    df = product_df.copy()
    if df.empty:
        st.info("No product data available for current selection.")
        return

    tab1, tab2 = st.tabs(["⭐ Executive Leaderboard (Top SKUs)", "🔍 Complete Portfolio Explorer (All SKUs)"])

    with tab1:
        top_n = min(10, len(df))
        top_df = df.head(top_n)

        rows_html = []
        for idx, row in top_df.iterrows():
            rank = len(rows_html) + 1
            prod_name = row.get("Product Name", "")
            div_name = row.get("Division", "")
            sales = format_currency(row.get("Sales", 0.0))
            gp = format_currency(row.get("Gross Profit", 0.0))
            gm = format_percent(row.get("Gross Margin %", 0.0))
            units = format_integer(row.get("Units", 0))
            profit_unit = format_currency(row.get("Profit per Unit", 0.0))
            rev_share = format_percent(row.get("Revenue Contribution %", 0.0))
            profit_share = format_percent(row.get("Profit Contribution %", 0.0))
            gap = _format_gap_cell(row.get("Profit vs Revenue Gap pp", 0.0))
            seg_badge = _get_segment_badge(row.get("Segment", ""))
            risk_badge = _get_risk_badge(row.get("Risk Status", ""))

            rows_html.append(f"""
                <tr>
                    <td style="font-weight: 700; color: #F2B01E; text-align: center;">#{rank}</td>
                    <td class="primary-cell"><b>{prod_name}</b></td>
                    <td><span class="tbl-badge tbl-badge-purple">{div_name}</span></td>
                    <td class="num-col">{sales}</td>
                    <td class="num-col" style="font-weight: 700; color: #4B1E78;">{gp}</td>
                    <td class="num-col" style="font-weight: 600;">{gm}</td>
                    <td class="num-col">{units}</td>
                    <td class="num-col">{profit_unit}</td>
                    <td class="num-col">{rev_share}</td>
                    <td class="num-col" style="font-weight: 700; color: #4B1E78;">{profit_share}</td>
                    <td class="num-col">{gap}</td>
                    <td>{seg_badge}</td>
                    <td>{risk_badge}</td>
                </tr>
            """)

        table_html = f"""
            <div class="executive-table-container">
                <table class="executive-table">
                    <thead>
                        <tr>
                            <th style="text-align: center;">Rank</th>
                            <th>Product Name</th>
                            <th>Division</th>
                            <th class="num-col">Total Sales</th>
                            <th class="num-col">Gross Profit</th>
                            <th class="num-col">Gross Margin</th>
                            <th class="num-col">Units</th>
                            <th class="num-col">Profit / Unit</th>
                            <th class="num-col">Revenue Share</th>
                            <th class="num-col">Profit Share</th>
                            <th class="num-col">Profit Gap</th>
                            <th>Strategic Segment</th>
                            <th>Risk Screening</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows_html)}
                    </tbody>
                </table>
            </div>
        """
        render_html(table_html)

    with tab2:
        column_config = {
            "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
            "Division": st.column_config.TextColumn("Division", width="small"),
            "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
            "Cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
            "Gross Profit": st.column_config.NumberColumn("Gross Profit", format="$%.2f"),
            "Gross Margin %": st.column_config.NumberColumn("Gross Margin %", format="%.2f%%"),
            "Cost-to-Sales %": st.column_config.NumberColumn("Cost-to-Sales %", format="%.2f%%"),
            "Units": st.column_config.NumberColumn("Units Sold", format="%d"),
            "Orders": st.column_config.NumberColumn("Orders", format="%d"),
            "Profit per Unit": st.column_config.NumberColumn("Profit / Unit", format="$%.2f"),
            "Revenue Contribution %": st.column_config.NumberColumn("Revenue Share", format="%.2f%%"),
            "Profit Contribution %": st.column_config.NumberColumn("Profit Share", format="%.2f%%"),
            "Profit vs Revenue Gap pp": st.column_config.NumberColumn("Profit Gap (pp)", format="%+.2f"),
            "Risk Status": st.column_config.TextColumn("Risk Status", width="small"),
            "Segment": st.column_config.TextColumn("Strategic Segment", width="small"),
        }

        display_cols = [c for c in [
            "Product Name", "Division", "Sales", "Cost", "Gross Profit",
            "Gross Margin %", "Units", "Profit per Unit",
            "Revenue Contribution %", "Profit Contribution %",
            "Profit vs Revenue Gap pp", "Risk Status", "Segment"
        ] if c in df.columns]

        st.dataframe(
            df[display_cols],
            column_config=column_config,
            use_container_width=True,
            height=height,
            hide_index=True,
        )
