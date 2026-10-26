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
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {PALETTE['body_text']};
    }}

    .stApp {{
        background-color: {PALETTE['cream']};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
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
        margin-top: -0.35rem !important;
        margin-bottom: 0.35rem !important;
    }}

    .app-tagline, .section-desc, .main-desc {{
        color: {PALETTE['muted_text']} !important;
        font-size: 0.86rem !important;
    }}

    /* ── Metric Cards: White bg, 5px Gold Left Border, 10px Radius, Soft Purple Shadow ── */
    [data-testid="stMetric"], .kpi-card {{
        background-color: {PALETTE['cards']} !important;
        border: 1px solid rgba(75, 30, 120, 0.08) !important;
        border-left: 5px solid {PALETTE['golden_ticket']} !important;
        border-radius: 10px !important;
        padding: 0.95rem 1.15rem !important;
        box-shadow: 0 4px 12px rgba(75, 30, 120, 0.06) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        height: 100% !important;
    }}

    [data-testid="stMetric"]:hover, .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(75, 30, 120, 0.12) !important;
        border-left: 5px solid {PALETTE['candy_pink']} !important;
    }}

    .kpi-label, [data-testid="stMetricLabel"] {{
        color: {PALETTE['muted_text']} !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    .kpi-value, [data-testid="stMetricValue"] {{
        color: {PALETTE['wonka_purple']} !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }}

    .kpi-subtext {{
        color: {PALETTE['muted_text']} !important;
        font-size: 0.76rem !important;
        font-weight: 500 !important;
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

    /* ── Tables & DataFrames: Purple Header, White Text, Subtle Hover ── */
    [data-testid="stDataFrame"] {{
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid rgba(75, 30, 120, 0.12) !important;
    }}

    [data-testid="stDataFrame"] header {{
        background-color: {PALETTE['wonka_purple']} !important;
        color: #FFFFFF !important;
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

    .insight-card {{
        background-color: {PALETTE['cards']} !important;
        border: 1px solid rgba(75, 30, 120, 0.1) !important;
        border-left: 5px solid {PALETTE['golden_ticket']} !important;
        border-radius: 8px;
        padding: 0.85rem 1.05rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 6px rgba(75, 30, 120, 0.04);
    }}

    .insight-card h4 {{
        margin: 0 0 0.35rem 0;
        font-size: 0.92rem;
        font-weight: 600;
        color: {PALETTE['wonka_purple']} !important;
        border-bottom: none !important;
    }}

    .insight-card p {{
        margin: 0;
        font-size: 0.82rem;
        color: {PALETTE['body_text']};
        line-height: 1.45;
    }}

    .status-badge-inline {{
        background-color: rgba(242, 176, 30, 0.15);
        color: {PALETTE['wonka_purple']};
        border: 1px solid {PALETTE['golden_ticket']};
        border-radius: 4px;
        padding: 0.2rem 0.55rem;
        font-size: 0.76rem;
        font-weight: 600;
        display: inline-block;
    }}

    .app-footer {{
        border-top: 1px solid rgba(75, 30, 120, 0.15);
        padding-top: 1.25rem;
        margin-top: 2.5rem;
        font-size: 0.78rem;
        color: {PALETTE['muted_text']};
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ── 3. Plotly Figure Styling Helper ──────────────────────────────────
def style_fig(fig):
    """
    Apply the Golden Ticket theme to a Plotly figure:
    - Cream / transparent background
    - Wonka purple text & titles
    - Light warm grid lines
    - Consistent font family
    - Colorway: [#4B1E78, #F2B01E, #E6427A, #7A6C8A, #DC2626]
    """
    if fig is None:
        return fig

    fig.update_layout(
        font=dict(
            family="Segoe UI, Inter, sans-serif",
            size=12,
            color=PALETTE["body_text"],
        ),
        title_font=dict(
            family="Segoe UI, Inter, sans-serif",
            size=15,
            color=PALETTE["wonka_purple"],
        ),
        paper_bgcolor="rgba(255, 248, 239, 0)",
        plot_bgcolor="#FFFFFF",
        colorway=[
            PALETTE["wonka_purple"],   # Revenue / Primary
            PALETTE["golden_ticket"],  # Profit / Accents
            PALETTE["candy_pink"],     # Selected / Highlight
            PALETTE["muted_text"],     # Neutral
            PALETTE["warning"],        # Risk / Flags
        ],
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(75, 30, 120, 0.15)",
            borderwidth=1,
            font=dict(size=11, color=PALETTE["body_text"]),
        ),
        margin=dict(l=55, r=30, t=55, b=45),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#F3E8D9",
        gridwidth=1,
        zerolinecolor="#EADBC8",
        tickfont=dict(color=PALETTE["body_text"], size=11),
        title_font=dict(color=PALETTE["wonka_purple"], size=12),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F3E8D9",
        gridwidth=1,
        zerolinecolor="#EADBC8",
        tickfont=dict(color=PALETTE["body_text"], size=11),
        title_font=dict(color=PALETTE["wonka_purple"], size=12),
    )

    return fig
