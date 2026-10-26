"""
Pareto (concentration) analysis for revenue and profit.

Validated control values:
- Revenue Pareto: 5 products account for 92.88% of revenue
- Profit Pareto: 5 products account for 95.06% of gross profit

Important: Do not call this "80/20 exactly". The observed values are
5/15 products → 92.88% revenue and 95.06% profit.
"""

import pandas as pd


def compute_revenue_pareto(product_df):
    """
    Compute revenue Pareto analysis with cumulative contribution.

    Products are ranked by Sales descending, with cumulative
    revenue contribution percentage.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table with 'Sales' and 'Revenue Contribution %'.

    Returns
    -------
    pd.DataFrame
        Revenue Pareto table sorted by Sales descending.
        Columns include: Product Name, Sales, Revenue Contribution %,
                         Cumulative Revenue %, Pareto Group
    """
    pareto = product_df.sort_values('Sales', ascending=False).reset_index(drop=True)
    pareto['Cumulative Revenue %'] = pareto['Revenue Contribution %'].cumsum()

    # Label products as within or beyond the 80% threshold
    pareto['Pareto Group'] = pareto['Cumulative Revenue %'].apply(
        lambda x: 'Core (≤80%)' if x <= 80.01 else 'Tail (>80%)'
    )

    pareto.index = pareto.index + 1
    pareto.index.name = 'Rank'

    return pareto


def compute_profit_pareto(product_df):
    """
    Compute profit Pareto analysis with cumulative contribution.

    Products are ranked by Gross Profit descending, with cumulative
    profit contribution percentage.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table with 'Gross Profit' and 'Profit Contribution %'.

    Returns
    -------
    pd.DataFrame
        Profit Pareto table sorted by Gross Profit descending.
        Columns include: Product Name, Gross Profit, Profit Contribution %,
                         Cumulative Profit %, Pareto Group
    """
    pareto = product_df.sort_values('Gross Profit', ascending=False).reset_index(drop=True)
    pareto['Cumulative Profit %'] = pareto['Profit Contribution %'].cumsum()

    # Label products as within or beyond the 80% threshold
    pareto['Pareto Group'] = pareto['Cumulative Profit %'].apply(
        lambda x: 'Core (≤80%)' if x <= 80.01 else 'Tail (>80%)'
    )

    pareto.index = pareto.index + 1
    pareto.index.name = 'Rank'

    return pareto


def get_pareto_threshold_count(pareto_df, cumulative_col, threshold=80):
    """
    Return the number of products needed to reach a cumulative threshold.

    Parameters
    ----------
    pareto_df : pd.DataFrame
        Pareto table with a cumulative percentage column.
    cumulative_col : str
        Name of the cumulative percentage column.
    threshold : float
        Cumulative percentage threshold (default: 80%).

    Returns
    -------
    int
        Number of products needed to exceed the threshold.
    """
    if pareto_df.empty:
        return 0

    exceeds = pareto_df[pareto_df[cumulative_col] >= threshold]
    if exceeds.empty:
        return len(pareto_df)

    # Return the rank (1-based index) of the first product to exceed threshold
    return int(exceeds.index[0])


def compute_concentration_metrics(product_df):
    """
    Compute profit and revenue concentration metrics.

    Parameters
    ----------
    product_df : pd.DataFrame
        Product profitability table.

    Returns
    -------
    dict
        Summary of concentration metrics including Pareto counts and
        cumulative percentages at key thresholds.
    """
    rev_pareto = compute_revenue_pareto(product_df)
    prof_pareto = compute_profit_pareto(product_df)

    rev_80_count = get_pareto_threshold_count(rev_pareto, 'Cumulative Revenue %', 80)
    prof_80_count = get_pareto_threshold_count(prof_pareto, 'Cumulative Profit %', 80)

    # Get the cumulative % at the count of products that reach 80%
    rev_at_80 = round(rev_pareto.loc[rev_80_count, 'Cumulative Revenue %'], 2) if rev_80_count <= len(rev_pareto) else 100.0
    prof_at_80 = round(prof_pareto.loc[prof_80_count, 'Cumulative Profit %'], 2) if prof_80_count <= len(prof_pareto) else 100.0

    return {
        'total_products': len(product_df),
        'revenue_80_count': rev_80_count,
        'revenue_80_cumulative_pct': rev_at_80,
        'profit_80_count': prof_80_count,
        'profit_80_cumulative_pct': prof_at_80,
    }
