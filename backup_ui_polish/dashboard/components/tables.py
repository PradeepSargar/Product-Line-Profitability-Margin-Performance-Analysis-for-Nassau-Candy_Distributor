"""
Formatted, sortable, interactive table components for Nassau Candy Dashboard.
"""

import streamlit as st
import pandas as pd


def render_product_leaderboard(product_df: pd.DataFrame, height: int = 500):
    """
    Render formatted interactive product profitability leaderboard table.
    """
    df = product_df.copy()

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


def render_division_table(div_df: pd.DataFrame):
    """Render formatted division performance summary table."""
    df = div_df.copy()

    column_config = {
        "Division": st.column_config.TextColumn("Division", width="medium"),
        "Sales": st.column_config.NumberColumn("Total Sales", format="$%.2f"),
        "Cost": st.column_config.NumberColumn("Total Cost", format="$%.2f"),
        "Gross Profit": st.column_config.NumberColumn("Gross Profit", format="$%.2f"),
        "Gross Margin %": st.column_config.NumberColumn("Gross Margin %", format="%.2f%%"),
        "Cost-to-Sales %": st.column_config.NumberColumn("Cost-to-Sales %", format="%.2f%%"),
        "Units": st.column_config.NumberColumn("Units", format="%d"),
        "Orders": st.column_config.NumberColumn("Orders", format="%d"),
        "Customers": st.column_config.NumberColumn("Customers", format="%d"),
        "Products": st.column_config.NumberColumn("SKU Count", format="%d"),
        "Revenue Contribution %": st.column_config.NumberColumn("Revenue Share", format="%.2f%%"),
        "Profit Contribution %": st.column_config.NumberColumn("Profit Share", format="%.2f%%"),
        "Profit vs Revenue Gap pp": st.column_config.NumberColumn("Profit Gap (pp)", format="%+.2f"),
    }

    st.dataframe(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
    )


def render_regional_table(reg_df: pd.DataFrame):
    """Render formatted regional performance summary table."""
    df = reg_df.copy()

    column_config = {
        "Region": st.column_config.TextColumn("Region", width="medium"),
        "Sales": st.column_config.NumberColumn("Total Sales", format="$%.2f"),
        "Cost": st.column_config.NumberColumn("Total Cost", format="$%.2f"),
        "Gross Profit": st.column_config.NumberColumn("Gross Profit", format="$%.2f"),
        "Gross Margin %": st.column_config.NumberColumn("Gross Margin %", format="%.2f%%"),
        "Cost-to-Sales %": st.column_config.NumberColumn("Cost-to-Sales %", format="%.2f%%"),
        "Units": st.column_config.NumberColumn("Units", format="%d"),
        "Orders": st.column_config.NumberColumn("Orders", format="%d"),
        "Customers": st.column_config.NumberColumn("Customers", format="%d"),
        "Revenue Contribution %": st.column_config.NumberColumn("Revenue Share", format="%.2f%%"),
        "Profit Contribution %": st.column_config.NumberColumn("Profit Share", format="%.2f%%"),
        "Profit vs Revenue Gap pp": st.column_config.NumberColumn("Profit Gap (pp)", format="%+.2f"),
    }

    st.dataframe(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
    )


def render_segment_table(seg_summary_df: pd.DataFrame):
    """Render formatted 4-quadrant strategic segment summary table."""
    df = seg_summary_df.copy()

    column_config = {
        "Segment": st.column_config.TextColumn("Strategic Segment", width="medium"),
        "Products": st.column_config.NumberColumn("Product Count", format="%d"),
        "Sales": st.column_config.NumberColumn("Total Sales", format="$%.2f"),
        "Gross Profit": st.column_config.NumberColumn("Gross Profit", format="$%.2f"),
        "Avg Gross Margin %": st.column_config.NumberColumn("Avg Gross Margin %", format="%.2f%%"),
        "Revenue Share %": st.column_config.NumberColumn("Revenue Share", format="%.2f%%"),
        "Profit Share %": st.column_config.NumberColumn("Profit Share", format="%.2f%%"),
    }

    st.dataframe(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
    )


def render_risk_table(risk_df: pd.DataFrame):
    """Render formatted table of risk-screened products."""
    df = risk_df.copy()

    column_config = {
        "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
        "Division": st.column_config.TextColumn("Division", width="small"),
        "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
        "Cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
        "Gross Profit": st.column_config.NumberColumn("Gross Profit", format="$%.2f"),
        "Gross Margin %": st.column_config.NumberColumn("Gross Margin %", format="%.2f%%"),
        "Cost-to-Sales %": st.column_config.NumberColumn("Cost-to-Sales %", format="%.2f%%"),
        "Units": st.column_config.NumberColumn("Units", format="%d"),
        "Risk Status": st.column_config.TextColumn("Risk Status", width="small"),
    }

    cols = [c for c in [
        "Product Name", "Division", "Sales", "Cost", "Gross Profit",
        "Gross Margin %", "Cost-to-Sales %", "Units", "Risk Status"
    ] if c in df.columns]

    st.dataframe(
        df[cols],
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
    )
