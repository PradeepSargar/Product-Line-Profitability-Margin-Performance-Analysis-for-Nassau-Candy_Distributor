"""
Header and title components for Nassau Candy Analytics Dashboard.
Styled with the Golden Ticket palette.
"""

from theme import PALETTE
from dashboard.utils.dashboard_utils import render_html


def render_app_header():
    """Render the top executive application header with status indicator."""
    header_html = """
        <div class="app-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <h1 class="app-title">Nassau Candy Distributor</h1>
                    <div class="app-subtitle">Product Line Profitability &amp; Margin Performance Analysis</div>
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
    render_html(header_html)


def render_page_header(title: str, subtitle: str = None, description: str = None):
    """Render a clean header for an individual dashboard page."""
    sub_html = f'<div class="app-subtitle" style="margin-top: 0.25rem;">{subtitle}</div>' if subtitle else ""
    desc_html = f'<div class="section-desc" style="margin-top: 0.3rem; margin-bottom: 0;">{description}</div>' if description else ""

    html = f"""
        <div class="page-header-block">
            <h2 style="font-size: 1.32rem; font-weight: 700; color: {PALETTE['wonka_purple']}; margin: 0; letter-spacing: -0.01em;">{title}</h2>
            {sub_html}
            {desc_html}
        </div>
    """
    render_html(html)


def render_section_title(title: str, description: str = None):
    """
    Render a standard section title and optional description.
    Uses consistent spacing system from design tokens:
    - Section title → divider: 10px
    - Divider → content: 18px
    """
    header_parts = [f'<div class="section-title">{title}</div>']
    if description:
        header_parts.append(f'<div class="section-desc">{description}</div>')

    html = f"""
        <div class="section-header">
            {''.join(header_parts)}
        </div>
    """
    render_html(html)
