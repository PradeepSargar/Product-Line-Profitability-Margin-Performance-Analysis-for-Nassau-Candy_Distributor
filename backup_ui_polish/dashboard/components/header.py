"""
Header and title components for Nassau Candy Analytics Dashboard.
Styled with the Golden Ticket palette.
"""

import streamlit as st
from theme import PALETTE


def render_app_header():
    """Render the top executive application header with status indicator."""
    header_html = f"""
    <div class="app-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <h1 class="app-title">Nassau Candy Distributor</h1>
                <div class="app-subtitle">Product Line Profitability & Margin Performance Analysis</div>
                <div class="app-tagline">
                    <span>Portfolio profitability • Product performance • Margin diagnostics</span>
                </div>
            </div>
            <div style="align-self: center;">
                <span class="status-badge-inline">✓ Data Status: Validated</span>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = None, description: str = None):
    """Render a clean header for an individual dashboard page."""
    html = f"""
    <div style="margin-bottom: 1.1rem;">
        <h2 style="font-size: 1.35rem; font-weight: 700; color: {PALETTE['wonka_purple']}; margin: 0; letter-spacing: -0.01em;">{title}</h2>
        {f'<div style="font-size: 0.95rem; font-weight: 600; color: {PALETTE["candy_pink"]}; margin-top: 0.2rem;">{subtitle}</div>' if subtitle else ''}
        {f'<div style="font-size: 0.85rem; color: {PALETTE["muted_text"]}; margin-top: 0.25rem; line-height: 1.4;">{description}</div>' if description else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_section_title(title: str, description: str = None):
    """Render a standard section title and optional description."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.markdown(f'<div class="section-desc">{description}</div>', unsafe_allow_html=True)
