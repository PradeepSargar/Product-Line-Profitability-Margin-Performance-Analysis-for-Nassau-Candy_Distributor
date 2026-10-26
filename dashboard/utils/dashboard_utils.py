"""
Shared dashboard utilities, formatting helpers, and cached data loader.
"""

import streamlit as st
import pandas as pd
from src.data.cleaning import get_clean_dataset


@st.cache_data(show_spinner="Loading portfolio dataset...")
def get_cached_data() -> pd.DataFrame:
    """
    Load, validate, clean, and feature-engineer dataset once.
    Reuses existing src/data/ cleaning pipeline as the single source of truth.
    """
    return get_clean_dataset()


def clean_html(html_str: str) -> str:
    """
    Strip all leading and trailing whitespace from every line in an HTML string.
    This guarantees that lines never begin with 4+ spaces or tabs, which would
    cause Markdown parsers to convert them into <pre><code> indented code blocks.
    """
    if not html_str:
        return ""
    lines = [line.strip() for line in html_str.splitlines()]
    return "\n".join(lines)


def render_html(html_str: str, sidebar: bool = False):
    """
    Safely render HTML in Streamlit without risk of Markdown code block escaping.
    Uses st.html / st.sidebar.html if supported (Streamlit 1.34+), or
    st.markdown / st.sidebar.markdown with zero-indented HTML.
    """
    cleaned = clean_html(html_str)
    target = st.sidebar if sidebar else st
    if hasattr(target, "html"):
        target.html(cleaned)
    else:
        target.markdown(cleaned, unsafe_allow_html=True)


def format_currency(val: float, compact: bool = False) -> str:
    """Format numeric value as currency ($#,##0.00 or $#,##0.0K)."""
    if val is None or pd.isna(val):
        return "$0.00"
    if compact:
        if abs(val) >= 1_000_000:
            return f"${val / 1_000_000:.1f}M"
        if abs(val) >= 1_000:
            return f"${val / 1_000:.1f}K"
    return f"${val:,.2f}"


def format_percent(val: float, decimals: int = 2) -> str:
    """Format numeric value as percentage (0.00%)."""
    if val is None or pd.isna(val):
        return f"{0.0:.{decimals}f}%"
    return f"{val:.{decimals}f}%"


def format_integer(val: int) -> str:
    """Format integer value with thousand separators (#,##0)."""
    if val is None or pd.isna(val):
        return "0"
    return f"{int(val):,}"


def render_empty_state(message: str = "No transactions match the current filter selection."):
    """Render a standardized executive empty state with reset option."""
    html = f"""
        <div class="empty-state-card">
            <div class="empty-state-title">No data for this selection</div>
            <p class="empty-state-body">{message}</p>
            <p class="empty-state-body" style="margin-top: 0.45rem;">
                Try broadening your date window, selecting additional divisions or regions,
                or clearing the product search query. Use <b>Reset All Filters</b> in the sidebar to restore the full portfolio.
            </p>
        </div>
    """
    render_html(html)


def render_footer():
    """Render a subtle, professional corporate footer."""
    footer_html = """
        <div class="app-footer">
            <div>
                <b>Nassau Candy Distributor</b> — Product Line Profitability &amp; Margin Performance Analysis
            </div>
            <div>
                Data Analytics Portfolio Project • Executive Decision Support System
            </div>
        </div>
    """
    render_html(footer_html)
