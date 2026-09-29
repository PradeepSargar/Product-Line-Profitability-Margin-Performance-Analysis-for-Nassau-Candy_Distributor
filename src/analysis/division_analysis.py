"""
Division-level profitability analysis.

Validated control values:
- Chocolate: 92.88% of revenue, 95.06% of profit, 67.45% margin
- Other: 6.82% of revenue, 4.64% of profit, 44.84% margin
- Sugar: 0.30% of revenue, 0.30% of profit, 66.61% margin
"""

import pandas as pd
import numpy as np


def compute_division_summary(df):
    """
    Compute division-level profitability summary.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    pd.DataFrame
        Division summary with Sales, Gross Profit, Cost, Units, Orders,
        Customers, Gross Margin %, Revenue Contribution %,
        Profit Contribution %, Profit vs Revenue Gap pp.
    """
    total_sales = df['Sales'].sum()
    total_gp = df['Gross Profit'].sum()

    div_df = df.groupby('Division').agg(
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        Cost=('Cost', 'sum'),
        Units=('Units', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique'),
        Products=('Product Name', 'nunique'),
    ).reset_index()

    div_df['Gross Margin %'] = np.where(
        div_df['Sales'] != 0,
        (div_df['Gross Profit'] / div_df['Sales']) * 100,
        0.0
    )

    div_df['Cost-to-Sales %'] = np.where(
        div_df['Sales'] != 0,
        (div_df['Cost'] / div_df['Sales']) * 100,
        0.0
    )

    div_df['Revenue Contribution %'] = np.where(
        total_sales != 0,
        (div_df['Sales'] / total_sales) * 100,
        0.0
    )

    div_df['Profit Contribution %'] = np.where(
        total_gp != 0,
        (div_df['Gross Profit'] / total_gp) * 100,
        0.0
    )

    div_df['Profit vs Revenue Gap pp'] = (
        div_df['Profit Contribution %'] - div_df['Revenue Contribution %']
    )

    # Sort by Gross Profit descending
    div_df = div_df.sort_values('Gross Profit', ascending=False).reset_index(drop=True)

    return div_df
