"""
Data cleaning and feature engineering for Nassau Candy Distributor.

Handles data quality checks, type conversions, and computes derived
analytical metrics matching the validated notebook definitions.
"""

import pandas as pd
import numpy as np


def clean_data(df):
    """
    Clean the dataset — handle duplicates and ensure correct types.

    The validated notebook confirms:
    - 0 null cells across all 18 columns
    - 0 exact duplicate rows
    - Financial identity: Gross Profit == Sales - Cost (max divergence 0.0000)

    Parameters
    ----------
    df : pd.DataFrame
        Raw or date-parsed DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with correct numeric types.
    """
    df = df.copy()

    # Drop exact duplicate rows (validated: 0 duplicates expected)
    df = df.drop_duplicates()

    # Ensure numeric columns are properly typed
    for col in ['Sales', 'Gross Profit', 'Cost']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Units'] = pd.to_numeric(df['Units'], errors='coerce').astype('Int64')

    return df


def engineer_features(df):
    """
    Add computed analytical features/metrics to the dataset.

    Engineered features (matching notebook definitions):
    - Gross Margin %: (Gross Profit / Sales) × 100
    - Cost-to-Sales %: (Cost / Sales) × 100
    - Profit per Unit: Gross Profit / Units
    - Order Year: Year extracted from Order Date
    - Order Month: Month number from Order Date
    - Order Month Name: Full month name
    - Order Quarter: Quarter string (e.g., '2024Q1')
    - Order Month-Year: Period string (e.g., '2024-01')

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame with datetime Order Date.

    Returns
    -------
    pd.DataFrame
        DataFrame with additional computed columns.
    """
    df = df.copy()

    # ── Margin & Efficiency Metrics ──────────────────────────────────
    df['Gross Margin %'] = np.where(
        df['Sales'] != 0,
        (df['Gross Profit'] / df['Sales']) * 100,
        0.0
    )

    df['Cost-to-Sales %'] = np.where(
        df['Sales'] != 0,
        (df['Cost'] / df['Sales']) * 100,
        0.0
    )

    df['Profit per Unit'] = np.where(
        df['Units'] != 0,
        df['Gross Profit'] / df['Units'],
        0.0
    )

    # ── Calendar & Period Features ───────────────────────────────────
    if pd.api.types.is_datetime64_any_dtype(df['Order Date']):
        df['Order Year'] = df['Order Date'].dt.year.astype(int)
        df['Order Month'] = df['Order Date'].dt.month
        df['Order Month Name'] = df['Order Date'].dt.month_name()
        df['Order Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
        df['Order Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)

    return df


def get_clean_dataset(filepath=None):
    """
    Full data pipeline: load → validate → parse dates → clean → engineer features.

    Convenience function that runs the complete data preparation pipeline.

    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. If None, uses the default project path.

    Returns
    -------
    pd.DataFrame
        Fully prepared dataset ready for analysis.
    """
    from .loader import load_raw_data, validate_schema, parse_dates

    df = load_raw_data(filepath)
    validate_schema(df)
    df = parse_dates(df)
    df = clean_data(df)
    df = engineer_features(df)

    return df
