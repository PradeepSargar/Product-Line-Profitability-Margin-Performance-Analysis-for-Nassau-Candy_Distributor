"""
Data loading utilities for Nassau Candy Distributor dataset.

Handles CSV loading, schema validation, and date parsing.
The raw dataset is expected at: data/raw/Nassau Candy Distributor.csv
"""

import os
import pandas as pd


# Expected columns in the raw dataset (18 columns)
EXPECTED_COLUMNS = [
    'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
    'Customer ID', 'Country/Region', 'City', 'State/Province', 'Postal Code',
    'Division', 'Region', 'Product ID', 'Product Name',
    'Sales', 'Units', 'Gross Profit', 'Cost'
]

# Raw date format in the source CSV
DATE_FORMAT = '%d-%m-%Y'


def get_default_data_path():
    """
    Return the default path to the raw CSV dataset.

    Resolves relative to this file's location:
    src/data/loader.py -> src/data/ -> src/ -> project_root/ -> data/raw/
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'data', 'raw', 'Nassau Candy Distributor.csv')


def load_raw_data(filepath=None):
    """
    Load the raw CSV dataset into a DataFrame.

    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. If None, uses the default project path.

    Returns
    -------
    pd.DataFrame
        Raw dataset with 18 columns and 10,194 rows.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at the specified path.
    ValueError
        If the loaded dataset is empty.
    """
    if filepath is None:
        filepath = get_default_data_path()

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset not found at: {filepath}\n"
            f"Expected location: data/raw/Nassau Candy Distributor.csv"
        )

    df = pd.read_csv(filepath)

    if df.empty:
        raise ValueError("Dataset is empty — no rows loaded from CSV.")

    return df


def validate_schema(df):
    """
    Validate that the DataFrame contains all expected columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    Returns
    -------
    bool
        True if all expected columns are present.

    Raises
    ------
    ValueError
        If any expected columns are missing.
    """
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in dataset: {sorted(missing)}")
    return True


def parse_dates(df):
    """
    Convert Order Date and Ship Date columns to datetime.

    The raw CSV stores dates in DD-MM-YYYY format.
    Ship Date anomalies (2026-2030 range) are preserved as-is per the
    validated analytical decision — timeline analyses use Order Date only.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with string date columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime-typed date columns.
    """
    df = df.copy()
    df['Order Date'] = pd.to_datetime(df['Order Date'], format=DATE_FORMAT, errors='raise')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format=DATE_FORMAT, errors='raise')
    return df
