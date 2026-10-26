"""
Core profitability computations for Nassau Candy Distributor.

Provides overall KPIs, product-level profitability table,
and time-based profitability analysis.
"""

import pandas as pd
import numpy as np


def compute_overall_kpis(df):
    """
    Compute portfolio-wide business KPIs from the dataset.

    Validated control values (unfiltered):
    - Total Sales: $141,783.63
    - Total Gross Profit: $93,442.80
    - Overall Gross Margin: 65.91%
    - Total Products: 15
    - Total Divisions: 3
    - Total Regions: 4

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with all analytical columns.

    Returns
    -------
    dict
        Dictionary of KPI name-value pairs.
    """
    total_sales = df['Sales'].sum()
    total_gp = df['Gross Profit'].sum()
    total_cost = df['Cost'].sum()
    total_units = df['Units'].sum()

    # Guard against divide-by-zero
    gross_margin = (total_gp / total_sales * 100) if total_sales != 0 else 0.0
    cost_to_sales = (total_cost / total_sales * 100) if total_sales != 0 else 0.0

    return {
        'total_sales': round(total_sales, 2),
        'total_gross_profit': round(total_gp, 2),
        'total_cost': round(total_cost, 2),
        'gross_margin_pct': round(gross_margin, 2),
        'cost_to_sales_pct': round(cost_to_sales, 2),
        'total_units': int(total_units),
        'total_orders': df['Order ID'].nunique(),
        'total_customers': df['Customer ID'].nunique(),
        'total_products': df['Product Name'].nunique(),
        'total_divisions': df['Division'].nunique(),
        'total_regions': df['Region'].nunique(),
        'total_records': len(df),
    }


def compute_product_profitability(df):
    """
    Compute the full product-level profitability table.

    For each product, calculates:
    - Sales, Gross Profit, Cost, Units, Orders
    - Gross Margin %, Cost-to-Sales %
    - Profit per Unit
    - Revenue Contribution %, Profit Contribution %
    - Profit vs Revenue Gap (pp)

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    pd.DataFrame
        Product profitability table sorted by Gross Profit descending.
        Columns: Product Name, Division, Sales, Gross Profit, Cost, Units,
                 Orders, Gross Margin %, Cost-to-Sales %, Profit per Unit,
                 Revenue Contribution %, Profit Contribution %,
                 Profit vs Revenue Gap pp
    """
    total_sales = df['Sales'].sum()
    total_gp = df['Gross Profit'].sum()

    product_df = df.groupby('Product Name').agg(
        Division=('Division', 'first'),
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        Cost=('Cost', 'sum'),
        Units=('Units', 'sum'),
        Orders=('Order ID', 'nunique'),
    ).reset_index()

    # Derived metrics with zero-division guards
    product_df['Gross Margin %'] = np.where(
        product_df['Sales'] != 0,
        (product_df['Gross Profit'] / product_df['Sales']) * 100,
        0.0
    )

    product_df['Cost-to-Sales %'] = np.where(
        product_df['Sales'] != 0,
        (product_df['Cost'] / product_df['Sales']) * 100,
        0.0
    )

    product_df['Profit per Unit'] = np.where(
        product_df['Units'] != 0,
        product_df['Gross Profit'] / product_df['Units'],
        0.0
    )

    # Contribution percentages (relative to portfolio total)
    product_df['Revenue Contribution %'] = np.where(
        total_sales != 0,
        (product_df['Sales'] / total_sales) * 100,
        0.0
    )

    product_df['Profit Contribution %'] = np.where(
        total_gp != 0,
        (product_df['Gross Profit'] / total_gp) * 100,
        0.0
    )

    # Gap between profit contribution and revenue contribution
    product_df['Profit vs Revenue Gap pp'] = (
        product_df['Profit Contribution %'] - product_df['Revenue Contribution %']
    )

    # Sort by Gross Profit descending
    product_df = product_df.sort_values('Gross Profit', ascending=False).reset_index(drop=True)

    return product_df


def compute_time_analysis_monthly(df):
    """
    Compute monthly sales, profit, and margin trends.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Order Month-Year' column.

    Returns
    -------
    pd.DataFrame
        Monthly aggregates sorted chronologically.
        Columns: Month-Year, Sales, Gross Profit, Cost, Units, Orders,
                 Gross Margin %, Cost-to-Sales %
    """
    monthly = df.groupby('Order Month-Year').agg(
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        Cost=('Cost', 'sum'),
        Units=('Units', 'sum'),
        Orders=('Order ID', 'nunique'),
    ).reset_index()

    monthly = monthly.rename(columns={'Order Month-Year': 'Month-Year'})
    monthly = monthly.sort_values('Month-Year').reset_index(drop=True)

    monthly['Gross Margin %'] = np.where(
        monthly['Sales'] != 0,
        (monthly['Gross Profit'] / monthly['Sales']) * 100,
        0.0
    )

    monthly['Cost-to-Sales %'] = np.where(
        monthly['Sales'] != 0,
        (monthly['Cost'] / monthly['Sales']) * 100,
        0.0
    )

    return monthly


def compute_time_analysis_yearly(df):
    """
    Compute yearly sales, profit, and margin trends.

    Validated control values:
    - 2024: Margin 65.83%
    - 2025: Margin 65.96%

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Order Year' column.

    Returns
    -------
    pd.DataFrame
        Yearly aggregates sorted chronologically.
    """
    yearly = df.groupby('Order Year').agg(
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        Cost=('Cost', 'sum'),
        Units=('Units', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique'),
    ).reset_index()

    yearly = yearly.rename(columns={'Order Year': 'Year'})
    yearly = yearly.sort_values('Year').reset_index(drop=True)

    yearly['Gross Margin %'] = np.where(
        yearly['Sales'] != 0,
        (yearly['Gross Profit'] / yearly['Sales']) * 100,
        0.0
    )

    yearly['Cost-to-Sales %'] = np.where(
        yearly['Sales'] != 0,
        (yearly['Cost'] / yearly['Sales']) * 100,
        0.0
    )

    return yearly
