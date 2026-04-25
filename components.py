"""
Trust Labs Analytics — Reusable UI Components
Material Design 3 themed helpers for Streamlit + Plotly
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ───────────────────────────────────────────────────────────
# PLOTLY GOOGLE THEME
# ───────────────────────────────────────────────────────────

def google_theme(fig, height=350):
    """Apply Trust Labs / Google Material Design 3 styling to a Plotly figure."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="#dadce0",
            tickfont=dict(size=11, color="#5f6368", family="Roboto"),
            title_font=dict(size=11, color="#5f6368", family="Google Sans"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f3f4",
            showline=False,
            tickfont=dict(size=11, color="#5f6368", family="Roboto"),
            title_font=dict(size=11, color="#5f6368", family="Google Sans"),
        ),
        font=dict(family="Roboto, sans-serif", size=11, color="#202124"),
        margin=dict(t=20, b=30, l=40, r=20),
        height=height,
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=11,
            font_family="Roboto",
            bordercolor="#dadce0",
        ),
        legend=dict(
            font=dict(size=11, color="#5f6368"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    return fig


def google_donut(vals, names, colors, hole=0.6):
    """Create a Material Design donut chart."""
    fig = px.pie(
        values=vals,
        names=names,
        color=names,
        color_discrete_map=dict(zip(names, colors)),
    )
    fig.update_traces(
        hole=hole,
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(size=11, color="#202124"),
        marker=dict(line=dict(color="#ffffff", width=3)),
    )
    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Google Sans, sans-serif", size=11, color="#202124"),
    )
    return fig


def safe_vline(fig, x_datetime):
    """Add a vertical divider line + 'Forecast →' annotation."""
    xs = x_datetime.strftime("%Y-%m-%d")
    fig.add_shape(
        type="line",
        x0=xs,
        x1=xs,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="#9aa0a6", width=1.5, dash="solid"),
    )
    fig.add_annotation(
        x=xs,
        y=0.97,
        xref="x",
        yref="paper",
        text="Forecast →",
        showarrow=False,
        xanchor="left",
        font=dict(size=10, color="#5f6368"),
        bgcolor="rgba(255,255,255,0.85)",
        borderpad=3,
    )


# ───────────────────────────────────────────────────────────
# CHART SECTION CARD HELPERS
# ───────────────────────────────────────────────────────────

def sec_title(title, subtitle=""):
    """Render a section title with optional subtitle."""
    html = f'<div class="section-title">{title}</div>'
    if subtitle:
        html += f'<div class="section-subtitle">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)


def chart_start():
    """Open a chart-body container."""
    st.markdown('<div class="chart-body">', unsafe_allow_html=True)


def chart_end():
    """Close a chart-body container."""
    st.markdown("</div>", unsafe_allow_html=True)


def info_card_start(title):
    """Open an info-card with a title."""
    st.markdown(
        f'<div class="info-card"><div class="info-card-title">{title}</div>',
        unsafe_allow_html=True,
    )


def info_card_end():
    """Close an info-card container."""
    st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────
# KPI CARD HELPERS
# ───────────────────────────────────────────────────────────

def kpi_card(label, value, trend_text, trend_dir="neutral", icon="📊", accent="#1a73e8"):
    """Return HTML for a single KPI card."""
    cls = {"up": "up", "down": "down", "neutral": "neutral"}.get(trend_dir, "neutral")
    arrow = {"up": "↑", "down": "↓", "neutral": "→"}.get(trend_dir, "→")
    return f"""
<div class="kpi-card" style="--acc:{accent}">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <span class="kpi-trend {cls}">{arrow}&nbsp;{trend_text}</span>
</div>"""


def kpi_row(cards, cols=5):
    """Wrap a list of kpi_card HTML strings in a grid row."""
    return (
        f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
        + "".join(cards)
        + "</div>"
    )
