"""
Nassau Candy Distributor — Professional "Golden Ticket" Theme.

Color Palette:
- wonka_purple: #4B1E78 (Primary 1: sidebar, headings, main chart color / revenue)
- golden_ticket: #F2B01E (Primary 2: accents, borders, KPI highlights, secondary chart color / profit)
- candy_pink: #E6427A (Selected / active: selected filters, active tab, slider handle, hover, highlighted SKU)
- cream: #FFF8EF (Background)
- cards: #FFFFFF (Cards background)
- body_text: #2A1B3D (Body text)
- muted_text: #7A6C8A (Muted text)
- warning: #DC2626 (Warning / margin-risk flags only)
"""

import streamlit as st
import streamlit.components.v1 as components
import textwrap

# ── 1. The Definitive Golden Ticket Palette ──────────────────────────
PALETTE = {
    "wonka_purple": "#4B1E78",     # Primary 1: sidebar, headings, revenue
    "golden_ticket": "#F2B01E",    # Primary 2: accents, borders, profit
    "candy_pink": "#E6427A",       # Selected / active: filters, hover, highlight
    "cream": "#FFF8EF",            # Background
    "cards": "#FFFFFF",            # Card background
    "body_text": "#2A1B3D",        # Body text (WCAG AAA on cream/white)
    "muted_text": "#7A6C8A",       # Muted text
    "warning": "#DC2626",          # Margin-risk / discontinuation-review flags
}

# ── 1b. Centralized Design Tokens (CSS Variables) ────────────────────
DESIGN_TOKENS = {
    "dashboard_max_width": "1450px",
    "dashboard_padding_x": "28px",
    "card_radius": "10px",
    "card_padding": "22px",
    "card_padding_x": "22px",
    "card_padding_y": "20px",
    "grid_gap": "18px",
    "grid_gap_x": "18px",
    "grid_gap_y": "18px",
    "section_gap": "36px",
    "section_title_to_divider": "10px",
    "divider_to_content": "18px",
    "kpi_card_min_height": "138px",
    "kpi_card_row_height": "138px",
    "insight_card_min_height": "240px",
    "border_color": "rgba(75, 30, 120, 0.08)",
    "shadow_card": "0 4px 12px rgba(75, 30, 120, 0.06)",
    "shadow_card_hover": "0 6px 16px rgba(75, 30, 120, 0.12)",
}


# ── 2. CSS Theme Injection ───────────────────────────────────────────
def apply_theme():
    """
    Inject custom CSS implementing the Golden Ticket theme across all Streamlit components:
    - Sidebar: Purple background (#4B1E78) with crisp white text & labels
    - Headings (h1/h2/h3): Purple text (#4B1E78) with a 3px gold bottom border (#F2B01E)
    - Metric cards: White background, 5px gold left border (#F2B01E), rounded corners (10px), soft purple shadow
    - Buttons: Purple background (#4B1E78) with white text, candy pink (#E6427A) on hover
    - Selected controls: Candy pink (#E6427A) for active tabs, radio, slider handle, multiselect tags
    - Tables / Dataframes: Purple header row (#4B1E78) with white text, subtle row hover
    - NEW: Centralized dashboard container with max-width, CSS Grid for KPI/insight rows, equal-height cards
    """
    css = textwrap.dedent(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ═══════════════════════════════════════════════════════════════
       DESIGN TOKENS — Centrally controlled variables
       ═══════════════════════════════════════════════════════════════ */
    :root {{
        --dashboard-max-width: {DESIGN_TOKENS["dashboard_max_width"]};
        --dashboard-padding-x: {DESIGN_TOKENS["dashboard_padding_x"]};
        --card-radius: {DESIGN_TOKENS["card_radius"]};
        --card-padding: {DESIGN_TOKENS["card_padding"]};
        --card-padding-x: {DESIGN_TOKENS["card_padding_x"]};
        --card-padding-y: {DESIGN_TOKENS["card_padding_y"]};
        --grid-gap: {DESIGN_TOKENS["grid_gap"]};
        --grid-gap-x: {DESIGN_TOKENS["grid_gap_x"]};
        --grid-gap-y: {DESIGN_TOKENS["grid_gap_y"]};
        --section-gap: {DESIGN_TOKENS["section_gap"]};
        --section-title-to-divider: {DESIGN_TOKENS["section_title_to_divider"]};
        --divider-to-content: {DESIGN_TOKENS["divider_to_content"]};
        --kpi-card-min-height: {DESIGN_TOKENS["kpi_card_min_height"]};
        --kpi-card-row-height: {DESIGN_TOKENS["kpi_card_row_height"]};
        --insight-card-min-height: {DESIGN_TOKENS["insight_card_min_height"]};
        --border-color: {DESIGN_TOKENS["border_color"]};
        --shadow-card: {DESIGN_TOKENS["shadow_card"]};
        --shadow-card-hover: {DESIGN_TOKENS["shadow_card_hover"]};
        --accent-gold: {PALETTE["golden_ticket"]};
        --accent-purple: {PALETTE["wonka_purple"]};
        --accent-pink: {PALETTE["candy_pink"]};
        --accent-warning: {PALETTE["warning"]};
        --card-bg: {PALETTE["cards"]};
        --text-body: {PALETTE["body_text"]};
        --text-muted: {PALETTE["muted_text"]};
    }}

    /* ═══════════════════════════════════════════════════════════════
       GLOBAL DASHBOARD CONTAINER — Centered, max-width, consistent padding
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stMainBlockContainer"] {{
        max-width: calc(var(--dashboard-max-width) + (2 * var(--dashboard-padding-x))) !important;
        padding-left: var(--dashboard-padding-x) !important;
        padding-right: var(--dashboard-padding-x) !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    .block-container {{
        max-width: calc(var(--dashboard-max-width) + (2 * var(--dashboard-padding-x))) !important;
        padding-left: var(--dashboard-padding-x) !important;
        padding-right: var(--dashboard-padding-x) !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* Every Streamlit section within main content must use same horizontal bounds */
    .dashboard-section {{
        width: 100% !important;
        max-width: 100% !important;
        margin-bottom: var(--section-gap) !important;
    }}
    .dashboard-section:last-child {{
        margin-bottom: 0 !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       COMPLETE SCROLLBAR / SLIDER REMOVAL — ALL ELEMENTS (v2, 100% coverage)
       ═══════════════════════════════════════════════════════════════ */
    *, *::before, *::after {{
        box-sizing: border-box !important;
    }}

    /* ── Firefox / Edge Legacy — hide scrollbar track & thumb on EVERY scroller ── */
    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .block-container,
    section[tabindex="-1"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"],
    [data-testid="stPlotlyChart"],
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    [data-testid="stTabs"],
    [data-testid="stExpander"],
    [data-testid="stChatMessage"],
    [data-testid="stForm"],
    [data-testid="stMetric"],
    [data-testid="stBaseButton-header"],
    [class*="stScrollbarContainer"],
    [class*="css-scrollbar"],
    [class*="st-emotion-cache"] > div[style*="overflow"],
    div[class*="scrollbar-container"],
    div[data-testid*="Scrollbar"],
    .main,
    section.main,
    [data-baseweb="data-table"] > div,
    [data-baseweb="data-table"] .dvn-scroller,
    [data-baseweb="data-table"] .dvn-scroll-inner,
    [data-baseweb="data-table"] .dvn-scroll,
    [data-baseweb="tab-panel"],
    [data-baseweb="tab-list"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] ul,
    [data-baseweb="popover"],
    [data-baseweb="popover"] ul,
    [data-baseweb="menu"],
    .js-plotly-plot,
    .plot-container,
    .plotly,
    .svg-container,
    .main-svg,
    iframe,
    div {{
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }}

    /* ── WebKit (Chrome / Edge / Safari) — STANDALONE rules.
          WebKit silently DROPS any pseudo-element rule grouped with
          non-matching selectors, so each ::-webkit-scrollbar variant
          MUST be in its own dedicated selector block.
       ────────────────────────────────────────────────────────────── */
    *::-webkit-scrollbar {{
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        background: transparent !important;
        -webkit-appearance: none !important;
    }}
    *::-webkit-scrollbar-track {{
        display: none !important;
        background: transparent !important;
        width: 0 !important;
        height: 0 !important;
    }}
    *::-webkit-scrollbar-track-piece {{
        display: none !important;
        background: transparent !important;
    }}
    *::-webkit-scrollbar-thumb {{
        display: none !important;
        background: transparent !important;
        width: 0 !important;
        height: 0 !important;
        border: none !important;
        box-shadow: none !important;
        -webkit-appearance: none !important;
    }}
    *::-webkit-scrollbar-thumb:hover {{
        display: none !important;
        background: transparent !important;
    }}
    *::-webkit-scrollbar-thumb:vertical,
    *::-webkit-scrollbar-thumb:horizontal {{
        display: none !important;
        background: transparent !important;
    }}
    *::-webkit-scrollbar-corner {{
        display: none !important;
        background: transparent !important;
    }}
    *::-webkit-resizer {{
        display: none !important;
        background: transparent !important;
    }}
    *::-webkit-scrollbar-button {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }}

    /* Dedicated per-container WebKit rules — belt-and-braces for each Streamlit scroller */
    html::-webkit-scrollbar,
    body::-webkit-scrollbar,
    .stApp::-webkit-scrollbar,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar,
    [data-testid="stMain"]::-webkit-scrollbar,
    [data-testid="stMainBlockContainer"]::-webkit-scrollbar,
    .block-container::-webkit-scrollbar,
    [data-testid="stSidebar"]::-webkit-scrollbar,
    [data-testid="stSidebarContent"]::-webkit-scrollbar,
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar,
    [data-testid="stVerticalBlock"]::-webkit-scrollbar,
    [data-testid="stHorizontalBlock"]::-webkit-scrollbar,
    [data-testid="column"]::-webkit-scrollbar,
    [data-testid="stPlotlyChart"]::-webkit-scrollbar,
    [data-testid="stVerticalBlockBorderWrapper"]::-webkit-scrollbar,
    [data-testid="stMarkdownContainer"]::-webkit-scrollbar,
    [data-testid="stDataFrame"]::-webkit-scrollbar,
    [data-testid="stTable"]::-webkit-scrollbar,
    [data-testid="stTabs"]::-webkit-scrollbar,
    [data-testid="stExpander"]::-webkit-scrollbar,
    [data-testid="stForm"]::-webkit-scrollbar,
    [data-baseweb="tab-panel"]::-webkit-scrollbar,
    [data-baseweb="tab-list"]::-webkit-scrollbar,
    [data-baseweb="data-table"]::-webkit-scrollbar,
    [data-baseweb="popover"]::-webkit-scrollbar,
    [data-baseweb="menu"]::-webkit-scrollbar,
    .js-plotly-plot::-webkit-scrollbar,
    .plot-container::-webkit-scrollbar,
    iframe::-webkit-scrollbar {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }}

    /* ── Lock horizontal overflow at app shell only (avoid clipping cards/charts/text) ── */
    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        overflow-x: clip !important;
        max-width: 100% !important;
    }}

    /* Content blocks must grow naturally — hidden overflow was cutting off labels & copy */
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMetric"],
    [data-testid="stExpanderDetails"],
    .app-header,
    .page-header-block,
    .kpi-card,
    .insight-card,
    .strategic-card,
    .flowchart-container,
    .empty-state-card {{
        overflow: visible !important;
        max-width: 100% !important;
    }}

    /* ── Every element with overflow-y (page scroll / sidebar scroll) keeps scrolling,
          but the visible thumb/track is zeroed out by the rules above. ── */
    .stApp,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    .block-container {{
        overflow-y: auto !important;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {PALETTE['body_text']};
        overflow-x: hidden !important;
    }}

    .stApp {{
        background: linear-gradient(
            180deg,
            {PALETTE['cream']} 0%,
            #FFFDF9 42%,
            {PALETTE['cream']} 100%
        ) !important;
    }}

    /* ── Streamlit chrome: cleaner executive canvas ── */
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stToolbar"] {{
        right: 0.75rem !important;
    }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; height: 0 !important; }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
        overflow-x: hidden !important;
    }}

    /* ── Sidebar: Wonka Purple with White Text & Labels ── */
    [data-testid="stSidebar"] {{
        background-color: {PALETTE['wonka_purple']} !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {{
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        border-bottom: none !important;
        margin-bottom: 0.35rem !important;
        padding-bottom: 0 !important;
    }}

    /* Sidebar divider line */
    [data-testid="stSidebar"] hr {{
        border-color: rgba(242, 176, 30, 0.35) !important;
    }}

    /* Sidebar input fields: ensure text inside inputs is dark on light background */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {{
        color: {PALETTE['body_text']} !important;
        background-color: #FFFFFF !important;
        border-radius: 6px !important;
    }}

    /* ── Headings (h1, h2, h3): Purple with 3px Gold Bottom Border ── */
    h1, h2, h3, .app-title, .main-title {{
        color: {PALETTE['wonka_purple']} !important;
        border-bottom: 3px solid {PALETTE['golden_ticket']} !important;
        padding-bottom: 0.35rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}

    h1 {{ font-size: 1.75rem !important; }}
    h2 {{ font-size: 1.35rem !important; }}
    h3 {{ font-size: 1.15rem !important; }}

    .app-subtitle, .main-subtitle {{
        color: {PALETTE['candy_pink']} !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.35rem !important;
        line-height: 1.35 !important;
    }}

    .app-tagline, .section-desc, .main-desc {{
        color: {PALETTE['muted_text']} !important;
        font-size: 0.86rem !important;
        line-height: 1.45 !important;
    }}

    /* ── Top application hero header ── */
    .app-header {{
        background: {PALETTE['cards']} !important;
        border: 1px solid rgba(75, 30, 120, 0.09) !important;
        border-top: 4px solid {PALETTE['golden_ticket']} !important;
        border-radius: 14px !important;
        padding: 1.15rem 1.35rem 1rem 1.35rem !important;
        margin-bottom: 1.35rem !important;
        box-shadow:
            0 1px 2px rgba(75, 30, 120, 0.04),
            0 8px 24px rgba(75, 30, 120, 0.06) !important;
    }}
    .app-header .app-title {{
        border-bottom: none !important;
        margin-bottom: 0.15rem !important;
        padding-bottom: 0 !important;
        font-size: 1.62rem !important;
    }}
    .app-header .app-subtitle {{
        border-bottom: none !important;
    }}

    /* ── Page & section headings (main content) ── */
    .page-header-block {{
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.8rem !important;
        border-bottom: 1px solid rgba(75, 30, 120, 0.08) !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }}
    .page-header-block h2 {{
        border-bottom: none !important;
        margin-bottom: 0.15rem !important;
        padding-bottom: 0 !important;
    }}
    .section-header {{
        width: 100% !important;
        margin-bottom: var(--divider-to-content) !important;
        box-sizing: border-box !important;
    }}
    .section-title {{
        color: var(--accent-purple) !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin: 0 0 var(--section-title-to-divider) 0 !important;
        padding-bottom: var(--section-title-to-divider) !important;
        border-bottom: 2px solid rgba(242, 176, 30, 0.42) !important;
        line-height: 1.3 !important;
    }}
    .section-desc {{
        color: var(--text-muted) !important;
        font-size: 0.84rem !important;
        line-height: 1.45 !important;
        margin: 0 !important;
    }}
    .section-body {{
        width: 100% !important;
        box-sizing: border-box !important;
    }}

    /* ── Sidebar brand & navigation ── */
    .sidebar-brand {{
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(242, 176, 30, 0.28) !important;
        border-radius: 10px !important;
        padding: 0.75rem 0.85rem !important;
        margin-bottom: 0.85rem !important;
    }}
    .sidebar-brand-title {{
        color: {PALETTE['golden_ticket']} !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.2rem !important;
    }}
    .sidebar-brand-sub {{
        color: rgba(255, 255, 255, 0.88) !important;
        font-size: 0.78rem !important;
        line-height: 1.35 !important;
    }}
    .sidebar-nav-caption {{
        color: rgba(255, 255, 255, 0.72) !important;
        font-size: 0.74rem !important;
        margin: 0.15rem 0 0.65rem 0 !important;
        line-height: 1.45 !important;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        gap: 0.45rem !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.65rem 0.55rem 0.55rem !important;
        align-items: flex-start !important;
        line-height: 1.4 !important;
        min-height: unset !important;
        height: auto !important;
        transition: background 0.15s ease, border-color 0.15s ease !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child {{
        margin-top: 0.12rem !important;
        flex-shrink: 0 !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:last-child {{
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        word-break: break-word !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(242, 176, 30, 0.35) !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: rgba(230, 66, 122, 0.18) !important;
        border-color: rgba(242, 176, 30, 0.45) !important;
    }}

    .portfolio-idle-indicator {{
        font-size: 0.78rem !important;
        color: rgba(255, 255, 255, 0.82) !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.75rem !important;
        margin-bottom: 0.75rem !important;
        line-height: 1.4 !important;
    }}
    .portfolio-idle-indicator b {{
        color: #FFFFFF !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       KPI GRID SYSTEM — 4-column CSS Grid, responsive, equal heights
       ═══════════════════════════════════════════════════════════════ */
    .kpi-grid {{
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: var(--grid-gap-y) var(--grid-gap-x) !important;
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    @media (max-width: 1024px) {{
        .kpi-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
    }}
    @media (max-width: 640px) {{
        .kpi-grid {{ grid-template-columns: 1fr !important; }}
    }}

    /* ── Metric Cards: White bg, 5px Gold Left Border, 10px Radius, Soft Purple Shadow, EQUAL HEIGHTS via flexbox ── */
    [data-testid="stMetric"] {{
        overflow: visible !important;
    }}
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
        white-space: normal !important;
        overflow: visible !important;
        word-break: break-word !important;
    }}

    [data-testid="stMetric"], .kpi-card {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-left: 5px solid var(--accent-gold) !important;
        border-radius: var(--card-radius) !important;
        padding: var(--card-padding-y) var(--card-padding-x) !important;
        box-shadow: var(--shadow-card) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        height: 100% !important;
        min-height: var(--kpi-card-min-height) !important;
        overflow: visible !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        margin: 0 !important;
    }}

    [data-testid="stMetric"]:hover, .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-card-hover) !important;
        border-left: 5px solid var(--accent-pink) !important;
    }}

    .kpi-label, [data-testid="stMetricLabel"] {{
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        line-height: 1.35 !important;
        margin: 0 0 10px 0 !important;
        flex-shrink: 0 !important;
        width: 100% !important;
    }}

    .kpi-value, [data-testid="stMetricValue"] {{
        color: var(--accent-purple) !important;
        font-size: clamp(1.25rem, 2.4vw, 1.85rem) !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        margin: 0 0 auto 0 !important;
        flex: 1 0 auto !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }}
    [data-testid="stMetricValue"] {{
        flex: 0 0 auto !important;
    }}

    .kpi-label, .kpi-subtext {{
        white-space: normal !important;
        overflow: visible !important;
    }}

    .kpi-subtext, [data-testid="stMetricDelta"] {{
        color: var(--text-muted) !important;
        font-size: 0.76rem !important;
        font-weight: 500 !important;
        line-height: 1.35 !important;
        margin: 10px 0 0 0 !important;
        flex-shrink: 0 !important;
        width: 100% !important;
    }}
    [data-testid="stMetricDelta"] {{
        margin-top: 6px !important;
    }}

    /* Equal-height enforcement inside st.columns() */
    .block-container [data-testid="stHorizontalBlock"] {{
        align-items: stretch !important;
        flex-wrap: wrap !important;
        gap: var(--grid-gap-y) 0 !important;
        width: 100% !important;
        margin: 0 !important;
    }}
    .block-container [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        padding-left: calc(var(--grid-gap-x) / 2) !important;
        padding-right: calc(var(--grid-gap-x) / 2) !important;
        overflow: visible !important;
        align-self: stretch !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    .block-container [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {{
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    .block-container [data-testid="stHorizontalBlock"] + .block-container [data-testid="stHorizontalBlock"] {{
        margin-top: var(--grid-gap-y) !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       HORIZONTAL OVERFLOW + SCROLLBAR PROTECTION — DataFrames / Tabs / Sidebar / Plots
       ═══════════════════════════════════════════════════════════════ */
    /* Hide BaseWeb / Glide data-table scrollbars */
    [data-baseweb="data-table"] > div,
    [data-baseweb="data-table"] [data-testid="stDataFrameResizable"],
    [data-baseweb="data-table"] .dvn-scroller,
    [data-baseweb="data-table"] .dvn-scroll-inner,
    [data-baseweb="select"] > div,
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [data-baseweb="tab-list"] {{
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        overflow-x: hidden !important;
    }}
    [data-baseweb="data-table"] > div::-webkit-scrollbar,
    [data-baseweb="data-table"] [data-testid="stDataFrameResizable"]::-webkit-scrollbar,
    [data-baseweb="data-table"] .dvn-scroller::-webkit-scrollbar,
    [data-baseweb="data-table"] .dvn-scroll-inner::-webkit-scrollbar,
    [data-baseweb="tab-panel"]::-webkit-scrollbar,
    [data-baseweb="select"] > div::-webkit-scrollbar,
    [data-baseweb="popover"]::-webkit-scrollbar,
    [data-baseweb="menu"]::-webkit-scrollbar,
    [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
    }}

    /* Multiselect / dropdown popup: no scrollbars visible */
    [data-baseweb="select"] ul,
    [data-baseweb="popover"] ul {{
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }}
    [data-baseweb="select"] ul::-webkit-scrollbar,
    [data-baseweb="popover"] ul::-webkit-scrollbar {{
        display: none !important;
    }}

    /* Plotly: allow titles, legends, and tick labels to render outside the SVG box */
    [data-testid="stPlotlyChart"],
    [data-testid="stPlotlyChart"] > div,
    .js-plotly-plot,
    .plot-container,
    .plotly,
    .svg-container,
    .main-svg {{
        overflow: visible !important;
        scrollbar-width: none !important;
    }}
    iframe {{
        overflow: hidden !important;
        scrollbar-width: none !important;
    }}
    .js-plotly-plot::-webkit-scrollbar,
    .plot-container::-webkit-scrollbar,
    .plotly::-webkit-scrollbar,
    .svg-container::-webkit-scrollbar,
    iframe::-webkit-scrollbar {{
        display: none !important;
    }}

    /* ── Buttons: Purple bg, White Text, Candy Pink on Hover ── */
    .stButton > button {{
        background-color: {PALETTE['wonka_purple']} !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: 1px solid {PALETTE['wonka_purple']} !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease-in-out !important;
    }}

    .stButton > button:hover {{
        background-color: {PALETTE['candy_pink']} !important;
        color: #FFFFFF !important;
        border-color: {PALETTE['candy_pink']} !important;
        box-shadow: 0 4px 10px rgba(230, 66, 122, 0.3) !important;
    }}

    /* ── Selected Controls (Radio, Tabs, Slider, Tags): Candy Pink (#E6427A) ── */
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px !important;
        border-bottom: 2px solid rgba(75, 30, 120, 0.15) !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
    }}
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {PALETTE['muted_text']} !important;
        font-weight: 600 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 16px !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {PALETTE['candy_pink']} !important;
        border-bottom: 3px solid {PALETTE['candy_pink']} !important;
    }}

    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {{
        border-color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] div:first-child,
    .stRadio div[role="radiogroup"] label[data-checked="true"] div:first-child {{
        background-color: {PALETTE['candy_pink']} !important;
        border-color: {PALETTE['candy_pink']} !important;
    }}

    /* Multiselect tags */
    [data-baseweb="tag"] {{
        background-color: {PALETTE['candy_pink']} !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
    }}

    [data-baseweb="tag"] span {{
        color: #FFFFFF !important;
    }}

    /* Slider track & thumb */
    [data-baseweb="slider"] div[role="slider"] {{
        background-color: {PALETTE['candy_pink']} !important;
        border-color: {PALETTE['candy_pink']} !important;
    }}

    /* ── Permanent Suppression of Duplicate Native Streamlit Sidebar Navigation ── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavSeparator"],
    [data-testid="stSidebarNavItems"],
    section[data-testid="stSidebar"] nav,
    .st-emotion-cache-16txtl3,
    ul[data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNav"] {{
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }}

    /* ── Tables & DataFrames: Golden Ticket Theme Alignment ── */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrameResizable"] {{
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid rgba(75, 30, 120, 0.12) !important;
        box-shadow: 0 4px 12px rgba(75, 30, 120, 0.05) !important;
        background: #FFFFFF !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }}

    /* ── Executive HTML Table Design System ── */
    .executive-table-container {{
        width: 100% !important;
        overflow-x: auto !important;
        border-radius: 10px !important;
        border: 1px solid rgba(75, 30, 120, 0.12) !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(75, 30, 120, 0.05) !important;
        margin-bottom: 1.5rem !important;
    }}

    .executive-table {{
        width: 100% !important;
        border-collapse: collapse !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 0.84rem !important;
        color: #2A1B3D !important;
        text-align: left !important;
        margin: 0 !important;
    }}

    .executive-table thead {{
        background: linear-gradient(135deg, #4B1E78 0%, #3B1560 100%) !important;
        border-bottom: 3px solid #F2B01E !important;
    }}

    .executive-table th {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.81rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.03em !important;
        padding: 12px 14px !important;
        white-space: nowrap !important;
        border: none !important;
    }}

    .executive-table th.num-col,
    .executive-table td.num-col {{
        text-align: right !important;
    }}

    .executive-table tbody tr {{
        border-bottom: 1px solid rgba(75, 30, 120, 0.06) !important;
        transition: background-color 0.15s ease !important;
    }}

    .executive-table tbody tr:nth-child(even) {{
        background-color: #FFFDF9 !important;
    }}

    .executive-table tbody tr:nth-child(odd) {{
        background-color: #FFFFFF !important;
    }}

    .executive-table tbody tr:hover {{
        background-color: rgba(242, 176, 30, 0.12) !important;
    }}

    .executive-table td {{
        padding: 10px 14px !important;
        vertical-align: middle !important;
        color: #2A1B3D !important;
        border: none !important;
    }}

    .executive-table td.primary-cell {{
        font-weight: 600 !important;
        color: #4B1E78 !important;
    }}

    .tbl-badge {{
        display: inline-block !important;
        padding: 2px 8px !important;
        border-radius: 4px !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        white-space: nowrap !important;
    }}

    .tbl-badge-gold {{
        background: #FEF9E7 !important;
        color: #8C5C00 !important;
        border: 1px solid #F2B01E !important;
    }}

    .tbl-badge-purple {{
        background: #F3EFF9 !important;
        color: #4B1E78 !important;
        border: 1px solid #4B1E78 !important;
    }}

    .tbl-badge-pink {{
        background: #FDF2F6 !important;
        color: #C2185B !important;
        border: 1px solid #E6427A !important;
    }}

    .tbl-badge-risk {{
        background: #FEF2F2 !important;
        color: #DC2626 !important;
        border: 1px solid #DC2626 !important;
    }}

    .tbl-badge-amber {{
        background: #FFFBEB !important;
        color: #B45309 !important;
        border: 1px solid #F59E0B !important;
    }}

    .tbl-badge-green {{
        background: #F0FDF4 !important;
        color: #15803D !important;
        border: 1px solid #22C55E !important;
    }}

    /* ── Custom Cards and Status Badges ── */
    .filter-indicator {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        border-left: 3px solid {PALETTE['golden_ticket']} !important;
        padding: 0.55rem 0.85rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.8rem;
        color: #FFFFFF !important;
        margin: 0.75rem 0;
    }}

    .filter-indicator b, .filter-indicator span {{
        color: #FFFFFF !important;
    }}

    .data-quality-box {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(242, 176, 30, 0.3) !important;
        border-radius: 8px;
        padding: 0.75rem 0.85rem;
        margin-top: 1rem;
        font-size: 0.77rem;
    }}

    .data-quality-box h5 {{
        color: {PALETTE['golden_ticket']} !important;
        margin: 0 0 0.5rem 0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .dq-item {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
        color: rgba(255, 255, 255, 0.8) !important;
    }}

    .dq-val {{
        font-weight: 600;
        color: #FFFFFF !important;
    }}

    .dq-pass {{
        color: {PALETTE['golden_ticket']} !important;
        font-weight: 600;
    }}

    /* ═══════════════════════════════════════════════════════════════
       INSIGHT GRID SYSTEM — 2×2 CSS Grid with EQUAL row heights
       ═══════════════════════════════════════════════════════════════ */
    .insight-grid {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: var(--grid-gap-y) var(--grid-gap-x) !important;
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        padding: 0 !important;
        grid-auto-rows: 1fr !important;
    }}
    .insight-grid-row {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0 var(--grid-gap-x) !important;
        grid-auto-rows: 1fr !important;
        margin-bottom: var(--grid-gap-y) !important;
    }}
    .insight-grid-row:last-child {{
        margin-bottom: 0 !important;
    }}
    @media (max-width: 768px) {{
        .insight-grid {{ grid-template-columns: 1fr !important; }}
        .insight-grid-row {{ grid-template-columns: 1fr !important; }}
    }}

    .insight-card {{
        background-color: var(--card-bg) !important;
        border: 1px solid rgba(75, 30, 120, 0.1) !important;
        border-left: 5px solid var(--accent-gold) !important;
        border-radius: var(--card-radius) !important;
        padding: 1.15rem 1.25rem !important;
        margin: 0 !important;
        box-shadow: 0 2px 6px rgba(75, 30, 120, 0.04) !important;
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease !important;
        height: 100% !important;
        min-height: var(--insight-card-min-height) !important;
        overflow: visible !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }}
    .insight-card:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(75, 30, 120, 0.08) !important;
        border-color: rgba(242, 176, 30, 0.28) !important;
    }}

    .strategic-card {{
        background-color: {PALETTE['cards']} !important;
        border-radius: 10px !important;
        padding: 0.85rem 0.95rem !important;
        height: 100% !important;
        box-shadow: 0 2px 8px rgba(75, 30, 120, 0.05) !important;
        transition: transform 0.16s ease, box-shadow 0.16s ease !important;
    }}
    .strategic-card:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(75, 30, 120, 0.09) !important;
    }}
    .strategic-card--gold {{ border: 1px solid rgba(242, 176, 30, 0.35) !important; border-top: 4px solid {PALETTE['golden_ticket']} !important; }}
    .strategic-card--purple {{ border: 1px solid rgba(75, 30, 120, 0.18) !important; border-top: 4px solid {PALETTE['wonka_purple']} !important; }}
    .strategic-card--pink {{ border: 1px solid rgba(230, 66, 122, 0.2) !important; border-top: 4px solid {PALETTE['candy_pink']} !important; }}
    .strategic-card--risk {{ background-color: #FEF2F2 !important; border: 1px solid rgba(220, 38, 38, 0.22) !important; border-top: 4px solid {PALETTE['warning']} !important; }}

    .empty-state-card {{
        background: {PALETTE['cards']} !important;
        border: 1px dashed rgba(75, 30, 120, 0.22) !important;
        border-radius: 12px !important;
        padding: 1.15rem 1.25rem !important;
        margin: 0.5rem 0 1rem 0 !important;
    }}
    .empty-state-title {{
        color: {PALETTE['wonka_purple']} !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.35rem !important;
    }}
    .empty-state-body {{
        color: {PALETTE['muted_text']} !important;
        font-size: 0.84rem !important;
        line-height: 1.45 !important;
        margin: 0 !important;
    }}

    .insight-card h4, .insight-card-title {{
        margin: 0 0 0.6rem 0 !important;
        font-size: 0.98rem !important;
        font-weight: 700 !important;
        color: var(--accent-purple) !important;
        border-bottom: none !important;
        line-height: 1.3 !important;
        flex-shrink: 0 !important;
    }}

    .insight-card p, .insight-card-body {{
        margin: 0 0 0.5rem 0 !important;
        font-size: 0.84rem !important;
        color: var(--text-body) !important;
        line-height: 1.55 !important;
        flex: 1 1 auto !important;
    }}
    .insight-card p:last-child, .insight-card-body:last-child {{
        margin-bottom: 0 !important;
    }}
    .insight-card-implication {{
        margin: 0.65rem 0 0 0 !important;
        padding: 0.6rem 0.75rem !important;
        background: rgba(75, 30, 120, 0.04) !important;
        border-left: 3px solid var(--accent-gold) !important;
        border-radius: 0 6px 6px 0 !important;
        font-size: 0.8rem !important;
        color: var(--text-body) !important;
        line-height: 1.45 !important;
        flex-shrink: 0 !important;
    }}
    .insight-card-implication b {{
        color: var(--accent-purple) !important;
        font-weight: 600 !important;
    }}

    .status-badge-inline {{
        background-color: rgba(242, 176, 30, 0.15);
        color: var(--accent-purple);
        border: 1px solid var(--accent-gold);
        border-radius: 4px;
        padding: 0.18rem 0.5rem;
        font-size: 0.72rem;
        font-weight: 600;
        display: inline-block;
        line-height: 1.25;
        flex-shrink: 0;
    }}
    .kpi-badge {{
        margin-top: 8px !important;
        background-color: rgba(230, 66, 122, 0.12) !important;
        color: var(--accent-pink) !important;
        border: 1px solid rgba(230, 66, 122, 0.3) !important;
        border-radius: 999px !important;
        padding: 0.15rem 0.55rem !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        display: inline-block !important;
        line-height: 1.25 !important;
        flex-shrink: 0 !important;
        white-space: nowrap !important;
    }}

    .app-footer {{
        border-top: 1px solid rgba(75, 30, 120, 0.12);
        padding-top: 1.15rem;
        margin-top: 2.5rem;
        font-size: 0.76rem;
        color: {PALETTE['muted_text']};
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem 1rem;
        justify-content: space-between;
        align-items: center;
    }}

    /* ── Expanders & alerts ── */
    [data-testid="stExpander"] {{
        background: {PALETTE['cards']} !important;
        border: 1px solid rgba(75, 30, 120, 0.1) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }}
    [data-testid="stAlert"] {{
        border-radius: 10px !important;
    }}



    /* ── Analytical pipeline flowchart ── */
    .flowchart-container {{
        background: {PALETTE['cards']} !important;
        border: 1px solid rgba(75, 30, 120, 0.1) !important;
        border-radius: 14px !important;
        padding: 1rem 1.1rem 1.05rem 1.1rem !important;
        margin: 0.5rem 0 1rem 0 !important;
        box-shadow: 0 4px 16px rgba(75, 30, 120, 0.06) !important;
    }}
    .flowchart-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.85rem;
        padding-bottom: 0.65rem;
        border-bottom: 1px solid rgba(75, 30, 120, 0.08);
    }}
    .flowchart-title {{
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 1rem;
        font-weight: 700;
        color: {PALETTE['wonka_purple']} !important;
    }}
    .flowchart-badge {{
        background: rgba(242, 176, 30, 0.14);
        color: {PALETTE['wonka_purple']};
        border: 1px solid rgba(242, 176, 30, 0.45);
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }}
    .flowchart-steps {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 0.65rem;
    }}
    .flowchart-step-card {{
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFCF7 100%);
        border: 1px solid rgba(75, 30, 120, 0.09);
        border-left: 4px solid {PALETTE['golden_ticket']};
        border-radius: 10px;
        padding: 0.75rem 0.8rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: unset;
        height: auto;
        transition: transform 0.16s ease, box-shadow 0.16s ease;
    }}
    .flowchart-step-card:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(75, 30, 120, 0.08);
    }}
    .flowchart-step-num {{
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {PALETTE['candy_pink']} !important;
        margin-bottom: 0.2rem;
    }}
    .flowchart-step-title {{
        font-size: 0.86rem;
        font-weight: 700;
        color: {PALETTE['wonka_purple']} !important;
        margin-bottom: 0.25rem;
        line-height: 1.25;
    }}
    .flowchart-step-desc {{
        font-size: 0.76rem;
        color: {PALETTE['muted_text']} !important;
        line-height: 1.4;
    }}
    .flowchart-step-status {{
        margin-top: 0.55rem;
        font-size: 0.72rem;
        font-weight: 700;
        color: {PALETTE['wonka_purple']} !important;
        background: rgba(242, 176, 30, 0.12);
        border-radius: 6px;
        padding: 0.25rem 0.45rem;
        align-self: flex-start;
    }}

    /* ═══════════════════════════════════════════════════════════════
       FINAL LAYER — FORCE-HIDE VERTICAL SCROLLBARS ON THE 9 EXACT
       STREAMLIT SCROLLERS REVEALED IN LIVE DOM AUDIT (2026-09-30)
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stMainBlockContainer"] {{
        overflow-y: scroll !important;    /* scrolling still works */
        overflow-x: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }}
    [data-testid="stMainBlockContainer"]::-webkit-scrollbar,
    [data-testid="stSidebarContent"]::-webkit-scrollbar,
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar,
    [data-testid="stMain"]::-webkit-scrollbar {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       GRAPH FIT — Every Plotly chart uses 100% of its card, with
       breathing room instead of hard borders. Responsive autosize
       is enforced via Plotly autosize=True + plot_chart(width='stretch')
       at render time (see plot_chart helper). These rules lock the
       card/container so inner SVG never overflows horizontally.
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stPlotlyChart"] {{
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        padding: 1rem 1rem 1.15rem 1rem !important;
        margin-bottom: 0.35rem !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        background: #FFFFFF !important;
        border: 1px solid rgba(75, 30, 120, 0.09) !important;
        border-radius: 16px !important;
        box-shadow:
            0 1px 2px rgba(75, 30, 120, 0.035),
            0 4px 14px rgba(75, 30, 120, 0.055) !important;
    }}
    [data-testid="stPlotlyChart"] > div,
    [data-testid="stPlotlyChart"] > div > div,
    [data-testid="stPlotlyChart"] > div > div > div,
    [data-testid="stPlotlyChart"] .js-plotly-plot,
    [data-testid="stPlotlyChart"] .plot-container,
    [data-testid="stPlotlyChart"] .svg-container,
    [data-testid="stPlotlyChart"] svg,
    [data-testid="stPlotlyChart"] .main-svg {{
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        padding: 1.1rem 1.25rem 0.6rem 1.25rem !important;
        margin-bottom: 0 !important;
        background: #FFFFFF !important;
        border: 1px solid rgba(75, 30, 120, 0.08) !important;
        border-radius: 14px !important;
        box-shadow: 0 3px 12px rgba(75, 30, 120, 0.05) !important;
        transition: box-shadow 0.18s ease, transform 0.18s ease, border-color 0.18s ease !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        box-shadow: 0 7px 22px rgba(75, 30, 120, 0.09) !important;
        border-color: rgba(242, 176, 30, 0.28) !important;
    }}
    /* Column-embedded charts: more compact but still professional */
    [data-testid="column"] [data-testid="stPlotlyChart"] {{
        padding: 0.85rem 0.75rem 1rem 0.75rem !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       GOLD-GRADIENT BREAKING LINE between every two different
       chart / insight rows. Applied via chart_divider() helper which
       emits <hr class="chart-tier-divider"> — a symmetrical
       purple→gold→purple gradient with rounded endcaps so the break
       looks clean and sectioned rather than a hard border.
       ═══════════════════════════════════════════════════════════════ */
    hr.chart-tier-divider,
    .chart-tier-divider,
    .chart-divider {{
        display: block !important;
        width: 100% !important;
        height: 3px !important;
        border: none !important;
        outline: none !important;
        margin: 2.2rem 0 1.9rem 0 !important;
        padding: 0 !important;
        background: linear-gradient(90deg,
          rgba(75, 30, 120, 0.00) 0%,
          rgba(75, 30, 120, 0.18) 14%,
          rgba(242, 176, 30, 0.72) 50%,
          rgba(75, 30, 120, 0.18) 86%,
          rgba(75, 30, 120, 0.00) 100%
        ) !important;
        border-radius: 3px !important;
        box-sizing: border-box !important;
        max-width: 100% !important;
        opacity: 0.94 !important;
    }}
    /* Extra spacing right before & after a divider on horizontal blocks */
    [data-testid="stHorizontalBlock"] + hr.chart-tier-divider,
    hr.chart-tier-divider + [data-testid="stHorizontalBlock"],
    hr.chart-tier-divider + [data-testid="stVerticalBlockBorderWrapper"] {{
        margin-top: 2rem !important;
    }}
    </style>
    """)
    st.markdown(css, unsafe_allow_html=True)

    # ── Runtime scrollbar eradicator (components.html allows <script>) ──
    # Streamlit strips <script> from st.markdown; components.html() preserves it.
    # This JS physically re-injects zero-width scrollbar CSS on every possible
    # scroller (html, main, sidebar, vertical blocks, Glide tables, iframes)
    # after render + on every Streamlit rerender/DOM mutation.
    _scrollbar_nuke_js = r"""
    <div style="display:none !important; visibility:hidden !important; width:0 !important; height:0 !important; overflow:hidden !important; pointer-events:none !important;">
    <script>
    (function(){
      function injectNoScrollbarStyle(root){
        try {
          if (!root || root.__noScrollbarInjected) return;
          var style = document.createElement('style');
          style.setAttribute('data-scrollbar-nuke','1');
          style.textContent = [
            '*::-webkit-scrollbar{display:none !important;width:0 !important;height:0 !important;}',
            '*::-webkit-scrollbar-track{display:none !important;background:transparent !important;}',
            '*::-webkit-scrollbar-track-piece{display:none !important;}',
            '*::-webkit-scrollbar-thumb{display:none !important;background:transparent !important;width:0 !important;height:0 !important;-webkit-appearance:none !important;}',
            '*::-webkit-scrollbar-thumb:vertical,*::-webkit-scrollbar-thumb:horizontal{display:none !important;}',
            '*::-webkit-scrollbar-corner,*::-webkit-scrollbar-button,*::-webkit-resizer{display:none !important;}',
            'html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"],.block-container,[data-testid="stSidebar"],[data-testid="stSidebarContent"],[data-testid="stSidebarUserContent"],[data-testid="stVerticalBlock"],[data-testid="stHorizontalBlock"],[data-testid="stPlotlyChart"],[data-testid="stVerticalBlockBorderWrapper"],[data-testid="stDataFrame"],[data-baseweb="data-table"] .dvn-scroller,[data-baseweb="data-table"] .dvn-scroll-inner,iframe,div{scrollbar-width:none !important;-ms-overflow-style:none !important;}'
          ].join('\n');
          if (root.head) {
            root.head.appendChild(style);
          } else if (root.appendChild) {
            root.appendChild(style);
          }
          root.__noScrollbarInjected = true;
        } catch(e) {}
      }
      function processIframes(){
        var fs = document.querySelectorAll('iframe');
        for (var i = 0; i < fs.length; i++) {
          var f = fs[i];
          try {
            var d = f.contentDocument || (f.contentWindow && f.contentWindow.document);
            if (d) injectNoScrollbarStyle(d);
          } catch(e) {}
        }
      }
      function nuke(){
        injectNoScrollbarStyle(document);
        processIframes();
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', nuke);
      } else {
        nuke();
      }
      window.addEventListener('load', function(){ nuke(); }, { once: true });
      [0, 400, 1100, 2200, 4000, 6500, 9500].forEach(function(t){ setTimeout(nuke, t); });
      try {
        var mo = new MutationObserver(function(muts){
          for (var i = 0; i < muts.length; i++) {
            if (muts[i].addedNodes && muts[i].addedNodes.length) {
              setTimeout(nuke, 40);
              break;
            }
          }
        });
        mo.observe(document.documentElement, { childList: true, subtree: true });
      } catch(e) {}
    })();
    </script>
    </div>
    """
    try:
        components.html(_scrollbar_nuke_js, height=0, width=0)
    except Exception:
        pass


# ── 3. Plotly Figure Styling Helper ──────────────────────────────────
def style_fig(fig, *, height: int | None = None,
              margin: dict | None = None,
              compact: bool = True):
    """
    Apply the Golden Ticket theme to a Plotly figure so it fits perfectly
    without any horizontal or vertical scrollbar inside its column card.

    Tuned to fit inside st.columns + use_container_width=True layout:
      - Ultra-compact margins (no wasted padding that forces scroll)
      - autosize=True + width=None + responsive: SVG reflows to 100%
      - Optional height override for "tall" charts vs "short" KPI cards
      - Legend docked inside bottom-left to avoid extra width
    """
    import textwrap

    if fig is None:
        return fig

    if margin is not None:
        base_margin = margin
    elif compact:
        base_margin = dict(l=62, r=28, t=68, b=92)
    else:
        base_margin = dict(l=72, r=32, t=78, b=100)

    fig.update_layout(
        font=dict(
            family="Segoe UI, Inter, sans-serif",
            size=13,
            color=PALETTE["body_text"],
        ),
        title_font=dict(
            family="Segoe UI, Inter, sans-serif",
            size=15.5,
            color=PALETTE["wonka_purple"],
        ),
        title_x=0.01,
        title_xanchor="left",
        paper_bgcolor="rgba(255, 248, 239, 0)",
        plot_bgcolor="#FFFFFF",
        colorway=[
            PALETTE["wonka_purple"],
            PALETTE["golden_ticket"],
            PALETTE["candy_pink"],
            PALETTE["muted_text"],
            PALETTE["warning"],
        ],
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="left",
            x=0,
            bgcolor="rgba(255, 255, 255, 0.97)",
            bordercolor="rgba(75, 30, 120, 0.15)",
            borderwidth=1,
            font=dict(size=11.5, color=PALETTE["body_text"]),
            itemwidth=32,
            traceorder="normal",
        ),
        margin=base_margin,
        autosize=True,
        width=None,
        height=height,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#F3E8D9",
        gridwidth=1,
        zerolinecolor="#EADBC8",
        tickfont=dict(color=PALETTE["body_text"], size=11.5),
        title_font=dict(color=PALETTE["wonka_purple"], size=12.5),
        automargin=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F3E8D9",
        gridwidth=1,
        zerolinecolor="#EADBC8",
        tickfont=dict(color=PALETTE["body_text"], size=11.5),
        title_font=dict(color=PALETTE["wonka_purple"], size=12.5),
        automargin=True,
    )

    fig.update_traces(
        marker_line_width=0.4,
        selector=dict(type="bar"),
    )
    fig.update_traces(
        marker=dict(line=dict(width=0.8, color="rgba(75,30,120,0.15)")),
        selector=dict(type="pie"),
    )

    config = {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d", "pan"],
        "responsive": True,
        "scrollZoom": False,
        "editable": False,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "nassau-candy-chart",
            "height": 600,
            "width": 1400,
            "scale": 2,
        },
    }
    try:
        fig._config = config
    except Exception:
        pass

    return fig


# ── 3b. Render helper — single call to style + fit any Plotly chart ──
def plot_chart(fig, *, height: int | None = None,
               use_container_width: bool = True,
               theme: bool = True,
               compact_margins: bool = True,
               margin: dict | None = None,
               card: bool = True,
               **st_kwargs):
    """
    Render a Plotly chart so it fits perfectly inside its column card.

    Pipeline:
      1. (optional) wrap in <div class="plotly-bento-card"> for professional
         fintech-style bento framing — white background, soft purple border,
         subtle lift shadow, hover gold accent.
      2. style_fig() → apply Golden Ticket palette + spacious margins
      3. fig layout → autosize=True + width=None (100% responsive)
      4. st.plotly_chart(width='stretch') → SVG fills 100% of column

    The chart never needs a horizontal or vertical scrollbar.
    """
    import textwrap

    if fig is None:
        return None
    if theme:
        fig = style_fig(fig, height=height, compact=compact_margins, margin=margin)
    try:
        fig.update_layout(
            autosize=True,
            width=None,
            height=height,
        )
    except Exception:
        pass

    # Chart framing is applied via CSS on [data-testid="stPlotlyChart"] (single DOM node).
    # Do not wrap with split open/close HTML blocks — Streamlit siblings break nesting and clip text.

    # Streamlit >= 1.57 API: width='stretch' replaces use_container_width=True
    try:
        import streamlit as _st_semver
        _st_v = tuple(int(x) for x in _st_semver.__version__.split(".")[:2])
        _use_width = _st_v >= (1, 57)
    except Exception:
        _use_width = False

    _render_kwargs = dict(
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d", "pan"],
            "responsive": True,
            "scrollZoom": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "nassau-candy-chart",
                "height": 600,
                "width": 1400,
                "scale": 2,
            },
        },
    )
    _render_kwargs.update(st_kwargs)
    if _use_width:
        if use_container_width:
            _render_kwargs["width"] = "stretch"
        elif "width" not in _render_kwargs:
            _render_kwargs["width"] = "content"
    else:
        _render_kwargs["use_container_width"] = use_container_width

    return st.plotly_chart(fig, **_render_kwargs)


# ── 3c. Gold-gradient breaking line between two different charts ─────
def chart_divider():
    """
    Emit a horizontal gold-gradient breaking line between chart tiers so
    two different chart rows look cleanly separated rather than merged.

    Uses <hr class="chart-tier-divider"> which is styled in apply_theme()
    to be a soft, symmetrical purple→gold→purple gradient line.
    """
    import textwrap

    html = textwrap.dedent(
        '<hr class="chart-tier-divider" aria-hidden="true">'
    )
    st.markdown(html, unsafe_allow_html=True)
