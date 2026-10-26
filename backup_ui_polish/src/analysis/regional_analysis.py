"""
Regional profitability analysis.

Validated control values:
- Highest margin: Interior at 66.43%
- Lowest margin: Atlantic at 65.47%
- Regional margin range: 0.96 percentage points
- Key finding: Margins are virtually uniform across all four regions.
"""

import pandas as pd
import numpy as np


def compute_regional_summary(df):
    """
    Compute region-level profitability summary.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    pd.DataFrame
        Regional summary with Sales, Gross Profit, Cost, Units, Orders,
        Customers, Gross Margin %, Revenue/Profit Contribution %,
        Profit vs Revenue Gap pp.
    """
    total_sales = df['Sales'].sum()
    total_gp = df['Gross Profit'].sum()

    reg_df = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        Cost=('Cost', 'sum'),
        Units=('Units', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique'),
    ).reset_index()

    reg_df['Gross Margin %'] = np.where(
        reg_df['Sales'] != 0,
        (reg_df['Gross Profit'] / reg_df['Sales']) * 100,
        0.0
    )

    reg_df['Cost-to-Sales %'] = np.where(
        reg_df['Sales'] != 0,
        (reg_df['Cost'] / reg_df['Sales']) * 100,
        0.0
    )

    reg_df['Revenue Contribution %'] = np.where(
        total_sales != 0,
        (reg_df['Sales'] / total_sales) * 100,
        0.0
    )

    reg_df['Profit Contribution %'] = np.where(
        total_gp != 0,
        (reg_df['Gross Profit'] / total_gp) * 100,
        0.0
    )

    reg_df['Profit vs Revenue Gap pp'] = (
        reg_df['Profit Contribution %'] - reg_df['Revenue Contribution %']
    )

    # Sort by Gross Profit descending
    reg_df = reg_df.sort_values('Gross Profit', ascending=False).reset_index(drop=True)

    return reg_df


def compute_regional_margin_range(regional_df):
    """
    Compute the margin range across regions.

    Validated: Range = 0.96 percentage points (Interior 66.43% – Atlantic 65.47%).

    Parameters
    ----------
    regional_df : pd.DataFrame
        Output from compute_regional_summary().

    Returns
    -------
    dict
        Dictionary with max_margin, min_margin, margin_range,
        max_region, min_region.
    """
    max_idx = regional_df['Gross Margin %'].idxmax()
    min_idx = regional_df['Gross Margin %'].idxmin()

    max_margin = regional_df.loc[max_idx, 'Gross Margin %']
    min_margin = regional_df.loc[min_idx, 'Gross Margin %']

    return {
        'max_margin': round(max_margin, 2),
        'min_margin': round(min_margin, 2),
        'margin_range_pp': round(max_margin - min_margin, 2),
        'max_region': regional_df.loc[max_idx, 'Region'],
        'min_region': regional_df.loc[min_idx, 'Region'],
    }
