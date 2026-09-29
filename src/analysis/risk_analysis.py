"""
Margin risk screening analysis.

Risk screening definition (validated):
A product is flagged for investigation if:
  Gross Margin % < portfolio median Gross Margin %
  AND
  Cost-to-Sales % > portfolio median Cost-to-Sales %

This is a SCREENING mechanism, not a final business decision.
Decisions to discontinue or reprice require additional business context.

Validated: 7 of 15 products meet the screening criteria.
Median thresholds: GM% = 62.31%, CTS% = 37.69%
"""

import pandas as pd


def get_median_thresholds(product_df):
    """
    Compute the portfolio median thresholds used for risk screening.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table with 'Gross Margin %' and 'Cost-to-Sales %'.

    Returns
    -------
    dict
        median_gm_pct: Median Gross Margin %
        median_cts_pct: Median Cost-to-Sales %
    """
    return {
        'median_gm_pct': round(product_df['Gross Margin %'].median(), 2),
        'median_cts_pct': round(product_df['Cost-to-Sales %'].median(), 2),
    }


def compute_risk_screening(product_df):
    """
    Apply margin risk screening to the product profitability table.

    Adds a 'Risk Status' column:
    - 'Investigate': Meets both screening criteria
    - 'Monitor': Does not meet both screening criteria

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table from compute_product_profitability().

    Returns
    -------
    pd.DataFrame
        Product table with 'Risk Status' column added.
    """
    df = product_df.copy()

    thresholds = get_median_thresholds(df)
    median_gm = thresholds['median_gm_pct']
    median_cts = thresholds['median_cts_pct']

    # Screening rule: below-median margin AND above-median cost ratio
    df['Risk Status'] = 'Monitor'
    risk_mask = (df['Gross Margin %'] < median_gm) & (df['Cost-to-Sales %'] > median_cts)
    df.loc[risk_mask, 'Risk Status'] = 'Investigate'

    return df


def get_flagged_products(product_df):
    """
    Return only the products flagged for investigation.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product table with 'Risk Status' column.

    Returns
    -------
    pd.DataFrame
        Filtered table with only 'Investigate' status products.
    """
    if 'Risk Status' not in product_df.columns:
        product_df = compute_risk_screening(product_df)

    return product_df[product_df['Risk Status'] == 'Investigate'].reset_index(drop=True)


def get_risk_summary(product_df):
    """
    Compute a summary of risk screening results.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product table with 'Risk Status' column.

    Returns
    -------
    dict
        total_products, flagged_count, monitor_count,
        flagged_pct, median_gm_pct, median_cts_pct
    """
    if 'Risk Status' not in product_df.columns:
        product_df = compute_risk_screening(product_df)

    thresholds = get_median_thresholds(product_df)
    flagged = product_df[product_df['Risk Status'] == 'Investigate']

    return {
        'total_products': len(product_df),
        'flagged_count': len(flagged),
        'monitor_count': len(product_df) - len(flagged),
        'flagged_pct': round(len(flagged) / len(product_df) * 100, 1) if len(product_df) > 0 else 0,
        'median_gm_pct': thresholds['median_gm_pct'],
        'median_cts_pct': thresholds['median_cts_pct'],
    }
