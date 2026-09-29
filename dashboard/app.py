"""
Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis
Executive Decision Support & Business Intelligence Dashboard

Application Shell & Navigation Router.
"""

import sys
import os
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dashboard.styles import theme
from dashboard.utils import dashboard_utils
from dashboard.components import header, filters
from dashboard.pages import (
    executive_overview,
    product_profitability,
    business_performance,
    strategic_analysis,
    risk_diagnostics,
)


def main():
    # 1. Streamlit Page Configuration
    st.set_page_config(
        page_title="Nassau Candy | Profitability Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Centralized Theme Injection
    theme.apply_theme()

    # 3. Top Executive Application Header
    header.render_app_header()

    # 4. Data Loading with Graceful Error Handling
    try:
        full_df = dashboard_utils.get_cached_data()
    except FileNotFoundError as fnf:
        st.error(f"❌ Dataset not found: {str(fnf)}")
        st.info("Expected location: data/raw/Nassau Candy Distributor.csv")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to load or prepare dataset: {str(e)}")
        st.stop()

    # 5. Global Sidebar Navigation
    st.sidebar.markdown("### 🧭 Navigation")
    pages = {
        "01 — Executive Overview": executive_overview,
        "02 — Product Profitability": product_profitability,
        "03 — Business Performance": business_performance,
        "04 — Strategic Analysis": strategic_analysis,
        "05 — Risk Diagnostics": risk_diagnostics,
    }

    selected_page_name = st.sidebar.radio(
        "Select View",
        options=list(pages.keys()),
        index=0,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # 6. Global Sidebar Filters
    filter_config = filters.render_sidebar_filters(full_df)
    filtered_df = filter_config['filtered_df']

    # 7. Page Routing & Execution
    active_page_module = pages[selected_page_name]
    try:
        active_page_module.render(filtered_df, full_df, filter_config)
    except Exception as e:
        st.error(f"❌ An error occurred while rendering '{selected_page_name}': {str(e)}")
        st.exception(e)

    # 8. Subtle Executive Footer
    dashboard_utils.render_footer()


if __name__ == "__main__":
    main()
