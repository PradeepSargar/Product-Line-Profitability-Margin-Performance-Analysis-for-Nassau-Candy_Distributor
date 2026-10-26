"""
Plotly chart builders for Nassau Candy Distributor dashboard.

Applies the professional "Golden Ticket" color theme:
- Revenue = #4B1E78 (Wonka Purple)
- Profit = #F2B01E (Golden Ticket)
- Highlighted / Selected = #E6427A (Candy Pink)
- Margin-risk / Warnings = #DC2626
- Pareto: bars purple (#4B1E78), cumulative line gold (#F2B01E), 80% line pink (#E6427A)
- Pass every figure through style_fig() before rendering.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from theme import PALETTE, style_fig


# ── The Golden Ticket Theme Mappings ─────────────────────────────────
COLORS = {
    'primary': PALETTE['wonka_purple'],     # #4B1E78 (Wonka Purple: Revenue, headers)
    'secondary': PALETTE['golden_ticket'],  # #F2B01E (Golden Ticket: Profit, accents)
    'accent': PALETTE['candy_pink'],        # #E6427A (Candy Pink: selected / highlight)
    'warning': PALETTE['warning'],          # #DC2626 (Margin-risk / review flags)
    'neutral': PALETTE['muted_text'],       # #7A6C8A (Muted text / neutral)
    'highlight': PALETTE['golden_ticket'],  # #F2B01E (Gold highlights)
    'light': PALETTE['cream'],              # #FFF8EF (Background cream)
    'dark': PALETTE['body_text'],           # #2A1B3D (Dark body text)
}

# Multi-tone palette for product/category charts aligned with Wonka & Golden Ticket
PRODUCT_PALETTE = [
    PALETTE['wonka_purple'], PALETTE['golden_ticket'], PALETTE['candy_pink'],
    '#6B2D8C', '#F5C24E', '#ED6B97',
    '#341256', '#D4940B', '#B82357',
    '#7A6C8A', '#9B61B5', '#F8D47C',
    '#F294B3', '#534366', PALETTE['warning']
]

DIVISION_COLORS = {
    'Chocolate': PALETTE['wonka_purple'],   # Primary division: Wonka Purple (#4B1E78)
    'Sugar': PALETTE['golden_ticket'],      # Golden Ticket (#F2B01E)
    'Other': PALETTE['candy_pink'],         # Candy Pink (#E6427A)
}

REGION_COLORS = {
    'Pacific': PALETTE['wonka_purple'],     # #4B1E78
    'Atlantic': PALETTE['golden_ticket'],   # #F2B01E
    'Interior': PALETTE['candy_pink'],      # #E6427A
    'Gulf': PALETTE['muted_text'],          # #7A6C8A
}

SEGMENT_COLORS = {
    'Core Driver': PALETTE['golden_ticket'],   # High Profit / High Margin: Gold
    'Volume Driver': PALETTE['wonka_purple'],  # High Profit / Low Margin: Purple
    'Niche Gem': PALETTE['candy_pink'],        # Low Profit / High Margin: Pink
    'Underperformer': PALETTE['warning'],      # Low Profit / Low Margin: Warning Red
}


def _common_layout(fig, title, height=450):
    """Apply consistent Golden Ticket layout and styling to all charts."""
    # First apply the global style_fig helper
    fig = style_fig(fig)

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=15, color=PALETTE['wonka_purple'], family='Segoe UI, Inter, sans-serif')
        ),
        height=height,
        margin=dict(l=60, r=30, t=60, b=50),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════
# Executive Overview Charts
# ══════════════════════════════════════════════════════════════════════

def chart_revenue_vs_profit_by_product(product_df, top_n=None):
    """
    Grouped bar chart: Revenue vs Gross Profit by product.
    Revenue = Wonka Purple (#4B1E78), Profit = Golden Ticket (#F2B01E).
    """
    df = product_df.copy()
    if top_n:
        df = df.nlargest(top_n, 'Sales')
    df = df.sort_values('Sales', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['Product Name'], x=df['Sales'],
        name='Revenue', orientation='h',
        marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{y}<br>Revenue: $%{x:,.2f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=df['Product Name'], x=df['Gross Profit'],
        name='Gross Profit', orientation='h',
        marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{y}<br>Gross Profit: $%{x:,.2f}<extra></extra>',
    ))

    fig = _common_layout(fig, 'Revenue vs Gross Profit by Product', height=max(350, len(df) * 35))
    fig.update_layout(barmode='group', yaxis=dict(title=''))
    fig.update_xaxes(title_text='Amount ($)')
    return fig


def chart_profit_contribution_by_product(product_df, top_n=None):
    """
    Horizontal bar chart of profit contribution by product.
    Top contributors highlighted in Golden Ticket (#F2B01E) or Candy Pink (#E6427A).
    """
    df = product_df.copy()
    if top_n:
        df = df.nlargest(top_n, 'Profit Contribution %')
    df = df.sort_values('Profit Contribution %', ascending=True)

    colors = [
        PALETTE['golden_ticket'] if v >= 10 else PALETTE['wonka_purple']
        for v in df['Profit Contribution %']
    ]

    fig = go.Figure(go.Bar(
        y=df['Product Name'], x=df['Profit Contribution %'],
        orientation='h', marker_color=colors,
        hovertemplate='%{y}<br>Profit Contribution: %{x:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Profit Contribution by Product (%)', height=max(350, len(df) * 30))
    fig.update_xaxes(title_text='Contribution (%)')
    fig.update_yaxes(title_text='')
    return fig


def chart_division_revenue_contribution(div_df):
    """Pie chart of revenue contribution by division."""
    fig = px.pie(
        div_df, values='Sales', names='Division',
        color='Division',
        color_discrete_map=DIVISION_COLORS,
        hole=0.45,
    )
    fig.update_traces(
        textposition='inside', textinfo='label+percent',
        hovertemplate='%{label}<br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>',
    )
    fig = _common_layout(fig, 'Revenue Contribution by Division', height=380)
    return fig


def chart_division_profit_contribution(div_df):
    """Pie chart of profit contribution by division."""
    fig = px.pie(
        div_df, values='Gross Profit', names='Division',
        color='Division',
        color_discrete_map=DIVISION_COLORS,
        hole=0.45,
    )
    fig.update_traces(
        textposition='inside', textinfo='label+percent',
        hovertemplate='%{label}<br>Gross Profit: $%{value:,.2f}<br>Share: %{percent}<extra></extra>',
    )
    fig = _common_layout(fig, 'Profit Contribution by Division', height=380)
    return fig


# ══════════════════════════════════════════════════════════════════════
# Product Profitability Charts
# ══════════════════════════════════════════════════════════════════════

def chart_gross_profit_by_product(product_df):
    """
    Horizontal bar chart of gross profit by product.
    Profit = Golden Ticket (#F2B01E), top SKU highlighted in Candy Pink (#E6427A).
    """
    df = product_df.sort_values('Gross Profit', ascending=True)

    max_gp = df['Gross Profit'].max()
    colors = [
        PALETTE['candy_pink'] if gp == max_gp else PALETTE['golden_ticket']
        for gp in df['Gross Profit']
    ]

    fig = go.Figure(go.Bar(
        y=df['Product Name'], x=df['Gross Profit'],
        orientation='h',
        marker_color=colors,
        hovertemplate='%{y}<br>Gross Profit: $%{x:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Gross Profit by Product', height=max(400, len(df) * 30))
    fig.update_xaxes(title_text='Gross Profit ($)')
    fig.update_yaxes(title_text='')
    return fig


def chart_gross_margin_by_product(product_df):
    """
    Horizontal bar chart of gross margin % by product.
    High margin = Golden Ticket, Mid = Wonka Purple, Below 50% = Warning Red.
    Portfolio average line in Candy Pink.
    """
    df = product_df.sort_values('Gross Margin %', ascending=True)

    colors = []
    for gm in df['Gross Margin %']:
        if gm >= 65:
            colors.append(PALETTE['golden_ticket'])
        elif gm >= 50:
            colors.append(PALETTE['wonka_purple'])
        else:
            colors.append(PALETTE['warning'])

    fig = go.Figure(go.Bar(
        y=df['Product Name'], x=df['Gross Margin %'],
        orientation='h', marker_color=colors,
        hovertemplate='%{y}<br>Gross Margin: %{x:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Gross Margin % by Product', height=max(400, len(df) * 30))
    fig.update_xaxes(title_text='Gross Margin (%)', range=[0, 100])
    fig.update_yaxes(title_text='')

    # Portfolio average line in Candy Pink
    avg_gm = (product_df['Gross Profit'].sum() / product_df['Sales'].sum() * 100) if product_df['Sales'].sum() != 0 else 0
    fig.add_vline(
        x=avg_gm, line_dash='dash', line_color=PALETTE['candy_pink'], line_width=2,
        annotation_text=f'Portfolio Avg: {avg_gm:.1f}%',
        annotation_position='top right'
    )
    return fig


def chart_revenue_vs_profit_contribution(product_df):
    """
    Grouped bar chart comparing revenue contribution vs profit contribution.
    Revenue = Wonka Purple (#4B1E78), Profit = Golden Ticket (#F2B01E).
    """
    df = product_df.sort_values('Profit Contribution %', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['Product Name'], x=df['Revenue Contribution %'],
        name='Revenue Share', orientation='h',
        marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{y}<br>Revenue Share: %{x:.2f}%<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=df['Product Name'], x=df['Profit Contribution %'],
        name='Profit Share', orientation='h',
        marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{y}<br>Profit Share: %{x:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Revenue vs Profit Contribution (%)', height=max(400, len(df) * 30))
    fig.update_layout(barmode='group')
    fig.update_xaxes(title_text='Contribution (%)')
    fig.update_yaxes(title_text='')
    return fig


# ══════════════════════════════════════════════════════════════════════
# Division Charts
# ══════════════════════════════════════════════════════════════════════

def chart_division_revenue_vs_profit(div_df):
    """
    Grouped bar chart: Revenue vs Profit by division.
    Revenue = Wonka Purple (#4B1E78), Profit = Golden Ticket (#F2B01E).
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=div_df['Division'], y=div_df['Sales'],
        name='Revenue', marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{x}<br>Revenue: $%{y:,.2f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=div_df['Division'], y=div_df['Gross Profit'],
        name='Gross Profit', marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Revenue vs Gross Profit by Division')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text='Amount ($)')
    return fig


def chart_division_margin_comparison(div_df):
    """Bar chart of gross margin % by division."""
    colors = [DIVISION_COLORS.get(d, PALETTE['muted_text']) for d in div_df['Division']]

    fig = go.Figure(go.Bar(
        x=div_df['Division'], y=div_df['Gross Margin %'],
        marker_color=colors,
        hovertemplate='%{x}<br>Gross Margin: %{y:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Gross Margin % by Division')
    fig.update_yaxes(title_text='Gross Margin (%)', range=[0, 100])
    return fig


def chart_division_contribution_comparison(div_df):
    """Side-by-side revenue vs profit contribution by division."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=div_df['Division'], y=div_df['Revenue Contribution %'],
        name='Revenue Share', marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{x}<br>Revenue Share: %{y:.2f}%<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=div_df['Division'], y=div_df['Profit Contribution %'],
        name='Profit Share', marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{x}<br>Profit Share: %{y:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Revenue vs Profit Contribution by Division (%)')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text='Contribution (%)')
    return fig


# ══════════════════════════════════════════════════════════════════════
# Regional Charts
# ══════════════════════════════════════════════════════════════════════

def chart_regional_gross_profit(reg_df):
    """Bar chart of gross profit by region in Golden Ticket."""
    df = reg_df.sort_values('Gross Profit', ascending=False)
    colors = [REGION_COLORS.get(r, PALETTE['golden_ticket']) for r in df['Region']]

    fig = go.Figure(go.Bar(
        x=df['Region'], y=df['Gross Profit'],
        marker_color=colors,
        hovertemplate='%{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Gross Profit by Region')
    fig.update_yaxes(title_text='Gross Profit ($)')
    return fig


def chart_regional_gross_margin(reg_df):
    """Bar chart of gross margin % by region."""
    df = reg_df.sort_values('Gross Margin %', ascending=False)
    colors = [REGION_COLORS.get(r, PALETTE['wonka_purple']) for r in df['Region']]

    fig = go.Figure(go.Bar(
        x=df['Region'], y=df['Gross Margin %'],
        marker_color=colors,
        text=[f'{v:.2f}%' for v in df['Gross Margin %']],
        textposition='outside',
        hovertemplate='%{x}<br>Gross Margin: %{y:.2f}%<extra></extra>',
    ))
    min_val = df['Gross Margin %'].min()
    max_val = df['Gross Margin %'].max()
    fig = _common_layout(fig, 'Gross Margin % by Region')
    fig.update_yaxes(
        title_text='Gross Margin (%)',
        range=[max(0, min_val - 2), min(100, max_val + 2)],
    )
    fig.add_annotation(
        text=f'Note: Margin range is only {max_val - min_val:.2f} percentage points',
        xref='paper', yref='paper', x=0.5, y=-0.15,
        showarrow=False, font=dict(size=10, color=PALETTE['muted_text']),
    )
    return fig


def chart_regional_revenue_vs_profit(reg_df):
    """
    Grouped bar chart: Revenue vs Profit by region.
    Revenue = Wonka Purple, Profit = Golden Ticket.
    """
    df = reg_df.sort_values('Sales', ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Region'], y=df['Sales'],
        name='Revenue', marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{x}<br>Revenue: $%{y:,.2f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=df['Region'], y=df['Gross Profit'],
        name='Gross Profit', marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Revenue vs Gross Profit by Region')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text='Amount ($)')
    return fig


# ══════════════════════════════════════════════════════════════════════
# Cost & Margin Diagnostics Charts
# ══════════════════════════════════════════════════════════════════════

def chart_cost_vs_sales_scatter(product_df):
    """
    Scatter plot: Sales (x) vs Cost (y) with risk status coloring.
    Investigate = Warning Red (#DC2626), Monitor = Wonka Purple (#4B1E78).
    Break-even line = Muted text (#7A6C8A).
    """
    df = product_df.copy()
    if 'Risk Status' not in df.columns:
        from src.analysis.risk_analysis import compute_risk_screening
        df = compute_risk_screening(df)

    color_map = {
        'Monitor': PALETTE['wonka_purple'],
        'Investigate': PALETTE['warning'],
    }

    fig = px.scatter(
        df, x='Sales', y='Cost',
        color='Risk Status',
        color_discrete_map=color_map,
        size='Units',
        hover_name='Product Name',
        hover_data={
            'Sales': ':$,.2f',
            'Cost': ':$,.2f',
            'Gross Margin %': ':.2f',
            'Cost-to-Sales %': ':.2f',
            'Risk Status': True,
        },
    )
    fig = _common_layout(fig, 'Cost vs Sales Diagnostics')
    fig.update_xaxes(title_text='Sales ($)')
    fig.update_yaxes(title_text='Cost ($)')

    max_val = max(df['Sales'].max(), df['Cost'].max()) * 1.1
    fig.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode='lines', line=dict(dash='dash', color=PALETTE['muted_text']),
        name='Break-even (0% Margin)', showlegend=True,
    ))
    return fig


# ══════════════════════════════════════════════════════════════════════
# Pareto Charts
# ══════════════════════════════════════════════════════════════════════

def chart_pareto(pareto_df, value_col, cumulative_col, title, value_label):
    """
    Combined bar + line Pareto chart.
    Bars = Wonka Purple (#4B1E78),
    Cumulative line = Golden Ticket (#F2B01E),
    80% threshold line = Candy Pink (#E6427A).
    """
    df = pareto_df.reset_index()

    fig = go.Figure()

    # Bar chart for individual contributions in Wonka Purple
    fig.add_trace(go.Bar(
        x=df['Product Name'], y=df[value_col],
        name='Individual Contribution',
        marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{x}<br>Contribution: %{y:.2f}%<extra></extra>',
    ))

    # Line chart for cumulative in Golden Ticket
    fig.add_trace(go.Scatter(
        x=df['Product Name'], y=df[cumulative_col],
        name='Cumulative', mode='lines+markers',
        line=dict(color=PALETTE['golden_ticket'], width=2.8),
        marker=dict(size=7, color=PALETTE['golden_ticket']),
        yaxis='y2',
        hovertemplate='%{x}<br>Cumulative: %{y:.2f}%<extra></extra>',
    ))

    # 80% threshold line in Candy Pink
    fig.add_hline(
        y=80, line_dash='dash', line_color=PALETTE['candy_pink'], line_width=2,
        annotation_text='80% Threshold',
        annotation_position='top right',
        yref='y2'
    )

    fig = _common_layout(fig, title, height=480)
    fig.update_layout(
        yaxis=dict(title=value_label, side='left'),
        yaxis2=dict(title='Cumulative (%)', side='right', overlaying='y',
                    range=[0, 105], showgrid=False),
        xaxis=dict(tickangle=-45),
    )
    return fig


def chart_revenue_pareto(pareto_df):
    """Revenue Pareto chart with 80% threshold line."""
    return chart_pareto(
        pareto_df,
        value_col='Revenue Contribution %',
        cumulative_col='Cumulative Revenue %',
        title='Revenue Pareto Analysis',
        value_label='Revenue Contribution (%)',
    )


def chart_profit_pareto(pareto_df):
    """Profit Pareto chart with 80% threshold line."""
    return chart_pareto(
        pareto_df,
        value_col='Profit Contribution %',
        cumulative_col='Cumulative Profit %',
        title='Profit Pareto Analysis',
        value_label='Profit Contribution (%)',
    )


# ══════════════════════════════════════════════════════════════════════
# Time Performance Charts
# ══════════════════════════════════════════════════════════════════════

def chart_monthly_sales_profit(monthly_df):
    """
    Dual line chart: Monthly sales and gross profit trends.
    Sales = Wonka Purple (#4B1E78), Gross Profit = Golden Ticket (#F2B01E).
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df['Month-Year'], y=monthly_df['Sales'],
        name='Sales', mode='lines+markers',
        line=dict(color=PALETTE['wonka_purple'], width=2.5),
        marker=dict(size=6),
        hovertemplate='%{x}<br>Sales: $%{y:,.2f}<extra></extra>',
    ))
    fig.add_trace(go.Scatter(
        x=monthly_df['Month-Year'], y=monthly_df['Gross Profit'],
        name='Gross Profit', mode='lines+markers',
        line=dict(color=PALETTE['golden_ticket'], width=2.5),
        marker=dict(size=6),
        hovertemplate='%{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Monthly Sales & Gross Profit Trend')
    fig.update_xaxes(title_text='Month', tickangle=-45)
    fig.update_yaxes(title_text='Amount ($)')
    return fig


def chart_monthly_margin(monthly_df):
    """Line chart: Monthly gross margin % trend in Golden Ticket."""
    fig = go.Figure(go.Scatter(
        x=monthly_df['Month-Year'], y=monthly_df['Gross Margin %'],
        mode='lines+markers',
        line=dict(color=PALETTE['golden_ticket'], width=2.5),
        fill='tozeroy', fillcolor='rgba(242, 176, 30, 0.12)',
        hovertemplate='%{x}<br>Gross Margin: %{y:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Monthly Gross Margin % Trend')
    fig.update_xaxes(title_text='Month', tickangle=-45)

    min_val = monthly_df['Gross Margin %'].min()
    max_val = monthly_df['Gross Margin %'].max()
    fig.update_yaxes(
        title_text='Gross Margin (%)',
        range=[max(0, min_val - 2), min(100, max_val + 2)],
    )
    return fig


def chart_yearly_comparison(yearly_df):
    """
    Grouped bar chart: Yearly sales and gross profit.
    Sales = Wonka Purple (#4B1E78), Profit = Golden Ticket (#F2B01E).
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly_df['Year'].astype(str), y=yearly_df['Sales'],
        name='Sales', marker_color=PALETTE['wonka_purple'],
        hovertemplate='%{x}<br>Sales: $%{y:,.2f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=yearly_df['Year'].astype(str), y=yearly_df['Gross Profit'],
        name='Gross Profit', marker_color=PALETTE['golden_ticket'],
        hovertemplate='%{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>',
    ))
    fig = _common_layout(fig, 'Yearly Sales & Gross Profit')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text='Amount ($)')
    return fig


def chart_yearly_margin(yearly_df):
    """Bar chart: Yearly gross margin % in Golden Ticket."""
    fig = go.Figure(go.Bar(
        x=yearly_df['Year'].astype(str), y=yearly_df['Gross Margin %'],
        marker_color=PALETTE['golden_ticket'],
        text=[f'{v:.2f}%' for v in yearly_df['Gross Margin %']],
        textposition='outside',
        hovertemplate='%{x}<br>Gross Margin: %{y:.2f}%<extra></extra>',
    ))
    fig = _common_layout(fig, 'Yearly Gross Margin %')
    min_val = yearly_df['Gross Margin %'].min()
    max_val = yearly_df['Gross Margin %'].max()
    fig.update_yaxes(
        title_text='Gross Margin (%)',
        range=[max(0, min_val - 3), min(100, max_val + 3)],
    )
    fig.add_annotation(
        text=f'YoY margin change: +{max_val - min_val:.2f} pp (volume-driven growth, stable margins)',
        xref='paper', yref='paper', x=0.5, y=-0.15,
        showarrow=False, font=dict(size=10, color=PALETTE['muted_text']),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════
# Strategic Segmentation & Distribution Charts
# ══════════════════════════════════════════════════════════════════════

def chart_strategic_matrix(product_df):
    """
    2x2 Strategic Product Matrix: Gross Margin % (x) vs Gross Profit (y).
    Core Driver = Gold, Volume Driver = Purple, Niche Gem = Pink, Underperformer = Red.
    """
    df = product_df.copy()
    if 'Segment' not in df.columns:
        from src.analysis.segmentation import segment_products
        df = segment_products(df)

    med_gp = df['Gross Profit'].median()
    med_gm = df['Gross Margin %'].median()

    fig = px.scatter(
        df,
        x='Gross Margin %',
        y='Gross Profit',
        color='Segment',
        color_discrete_map=SEGMENT_COLORS,
        size='Sales',
        hover_name='Product Name',
        hover_data={
            'Division': True,
            'Sales': ':$,.2f',
            'Gross Profit': ':$,.2f',
            'Gross Margin %': ':.2f',
            'Units': ':,',
            'Segment': True,
        },
    )

    fig = _common_layout(fig, 'Strategic Product Portfolio Matrix (2×2)', height=520)

    # Median threshold reference lines in muted neutral
    fig.add_vline(
        x=med_gm, line_dash='dash', line_color=PALETTE['muted_text'], line_width=1.5,
        annotation_text=f'Median Margin: {med_gm:.1f}%',
        annotation_position='top left',
    )
    fig.add_hline(
        y=med_gp, line_dash='dash', line_color=PALETTE['muted_text'], line_width=1.5,
        annotation_text=f'Median GP: ${med_gp:,.0f}',
        annotation_position='bottom right',
    )

    # Quadrant annotations with semantic colors
    x_min = max(0, df['Gross Margin %'].min() - 5)
    x_max = min(100, df['Gross Margin %'].max() + 5)
    y_max = df['Gross Profit'].max() * 1.05

    fig.add_annotation(
        x=x_max, y=y_max, text='Core Drivers<br><b>High Profit / High Margin</b>',
        showarrow=False, font=dict(size=10, color=PALETTE['golden_ticket']),
        xanchor='right', yanchor='top', opacity=0.9,
    )
    fig.add_annotation(
        x=x_min, y=y_max, text='Volume Drivers<br><b>High Profit / Low Margin</b>',
        showarrow=False, font=dict(size=10, color=PALETTE['wonka_purple']),
        xanchor='left', yanchor='top', opacity=0.9,
    )
    fig.add_annotation(
        x=x_max, y=0, text='Niche Gems<br><b>Low Profit / High Margin</b>',
        showarrow=False, font=dict(size=10, color=PALETTE['candy_pink']),
        xanchor='right', yanchor='bottom', opacity=0.9,
    )
    fig.add_annotation(
        x=x_min, y=0, text='Underperformers<br><b>Low Profit / Low Margin</b>',
        showarrow=False, font=dict(size=10, color=PALETTE['warning']),
        xanchor='left', yanchor='bottom', opacity=0.9,
    )

    fig.update_xaxes(title_text='Gross Margin (%)', range=[x_min, x_max])
    fig.update_yaxes(title_text='Gross Profit ($)', range=[0, y_max])
    return fig


def chart_revenue_profit_contribution_scatter(product_df):
    """
    Scatter plot: Revenue Contribution % (x) vs Profit Contribution % (y).
    Includes a 45-degree parity reference line.
    """
    df = product_df.copy()

    fig = px.scatter(
        df,
        x='Revenue Contribution %',
        y='Profit Contribution %',
        color='Division',
        color_discrete_map=DIVISION_COLORS,
        size='Gross Profit',
        hover_name='Product Name',
        hover_data={
            'Sales': ':$,.2f',
            'Gross Profit': ':$,.2f',
            'Gross Margin %': ':.2f',
            'Profit vs Revenue Gap pp': ':.2f',
        },
    )

    max_val = max(df['Revenue Contribution %'].max(), df['Profit Contribution %'].max()) * 1.15
    fig = _common_layout(fig, 'Revenue vs Profit Contribution Disparity', height=480)

    fig.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode='lines',
        line=dict(dash='dot', color=PALETTE['muted_text'], width=1.5),
        name='Parity Line (1:1 Share)',
        showlegend=True,
    ))

    fig.update_xaxes(title_text='Revenue Contribution (%)', range=[0, max_val])
    fig.update_yaxes(title_text='Profit Contribution (%)', range=[0, max_val])
    return fig


def chart_margin_distribution(df, group_col='Division'):
    """
    Box plot showing transaction-level Gross Margin % distribution across groups.
    """
    palette = DIVISION_COLORS if group_col == 'Division' else REGION_COLORS

    fig = px.box(
        df,
        x=group_col,
        y='Gross Margin %',
        color=group_col,
        color_discrete_map=palette,
        points='outliers',
    )
    fig = _common_layout(fig, f'Gross Margin % Distribution by {group_col}', height=420)
    fig.update_xaxes(title_text=group_col)
    fig.update_yaxes(title_text='Gross Margin (%)', range=[0, 100])
    fig.update_layout(showlegend=False)
    return fig
