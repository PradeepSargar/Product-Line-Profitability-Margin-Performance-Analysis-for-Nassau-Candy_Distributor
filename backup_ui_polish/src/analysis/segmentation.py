"""
Product segmentation analysis.

Segments products using a 2×2 matrix based on portfolio median thresholds:
- Gross Profit median: threshold for high/low profit
- Gross Margin % median: threshold for high/low margin

Validated segment breakdown:
1. High Profit / High Margin (Core Drivers) — 6 products
2. High Profit / Low Margin (Volume Drivers) — 2 products
3. Low Profit / High Margin (Niche Gems) — 2 products
4. Low Profit / Low Margin (Underperformers) — 5 products
"""

import pandas as pd


def segment_products(product_df):
    """
    Classify products into strategic segments using a 2×2 matrix.

    Dimensions:
    - Gross Profit vs median Gross Profit (high/low profit)
    - Gross Margin % vs median Gross Margin % (high/low margin)

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table with 'Gross Profit' and 'Gross Margin %'.

    Returns
    -------
    pd.DataFrame
        Product table with 'Segment' and 'Segment Label' columns added.
    """
    df = product_df.copy()

    # Portfolio medians as thresholds
    median_gp = df['Gross Profit'].median()
    median_gm = df['Gross Margin %'].median()

    # Classification conditions
    high_profit = df['Gross Profit'] >= median_gp
    high_margin = df['Gross Margin %'] >= median_gm

    # Assign segments
    conditions = [
        high_profit & high_margin,
        high_profit & ~high_margin,
        ~high_profit & high_margin,
        ~high_profit & ~high_margin,
    ]
    labels = [
        'Core Driver',
        'Volume Driver',
        'Niche Gem',
        'Underperformer',
    ]
    descriptions = [
        'High Profit / High Margin',
        'High Profit / Low Margin',
        'Low Profit / High Margin',
        'Low Profit / Low Margin',
    ]

    # Use numpy select for clean assignment
    import numpy as np
    df['Segment'] = np.select(conditions, labels, default='Unclassified')
    df['Segment Label'] = np.select(conditions, descriptions, default='Unclassified')

    return df


def get_segment_summary(product_df):
    """
    Compute aggregate performance metrics per segment.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product table with 'Segment' column (from segment_products).

    Returns
    -------
    pd.DataFrame
        Summary with product count, total sales, total profit,
        average margin, revenue share, and profit share per segment.
    """
    if 'Segment' not in product_df.columns:
        product_df = segment_products(product_df)

    total_sales = product_df['Sales'].sum()
    total_gp = product_df['Gross Profit'].sum()

    summary = product_df.groupby('Segment').agg(
        Products=('Product Name', 'count'),
        Sales=('Sales', 'sum'),
        **{'Gross Profit': ('Gross Profit', 'sum')},
        **{'Avg Gross Margin %': ('Gross Margin %', 'mean')},
    ).reset_index()

    summary['Revenue Share %'] = (summary['Sales'] / total_sales * 100) if total_sales != 0 else 0
    summary['Profit Share %'] = (summary['Gross Profit'] / total_gp * 100) if total_gp != 0 else 0

    # Sort by Gross Profit descending
    summary = summary.sort_values('Gross Profit', ascending=False).reset_index(drop=True)

    return summary
