import io
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="R-Cube Strategic Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #fdfcf9; color: #1a1c20; }

[data-testid="stSidebar"] { background: #f4f2ee !important; border-right: 1px solid #e2e2e0; }
[data-testid="stSidebar"] * { color: #4a4a48 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1a1c20 !important; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1a1c20 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.kpi-card {
    background: #ffffff; border: 1px solid #e8e8e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border-radius: 12px; padding: 1.5rem 1.75rem;
    position: relative; overflow: hidden;
}
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.kpi-card.relevance::before   { background: #d4af37; }
.kpi-card.reliability::before { background: #3a8fb5; }
.kpi-card.reputability::before { background: #9b5fcf; }
.kpi-card.growth::before      { background: #2e9c6e; }
.kpi-card.growth { text-align: center; }

.kpi-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #888880; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 5.2rem; font-weight: 900; line-height: 1; margin-bottom: 0.3rem; }
.kpi-value.relevance   { color: #b08d20; }
.kpi-value.reliability { color: #2a7a9e; }
.kpi-value.reputability { color: #7e46b0; }
.kpi-value.growth      { color: #1e7d54; }

.kpi-band { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-top: 0.25rem; }
.band-fragile    { background: #fff5f5; color: #e03131; }
.band-emerging   { background: #fff9db; color: #f08c00; }
.band-developing { background: #ebfbee; color: #2f9e44; }
.band-strong     { background: #e7f5ff; color: #1971c2; }
.band-benchmark  { background: #f8f0fc; color: #9c36b5; }

.stage-bar-wrap { background: #ffffff; border: 1px solid #e8e8e6; border-radius: 12px; padding: 1.5rem; }
.stage-profile-offset { margin-top: 44px; }
.stage-row { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.stage-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #666660; width: 130px; flex-shrink: 0; }
.stage-track { flex: 1; height: 8px; background: #f0f0ee; border-radius: 4px; overflow: hidden; }
.stage-fill  { height: 100%; border-radius: 4px; }
.stage-val   { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #4a4a48; }

.status-badge { display: inline-flex; align-items: center; gap: 0.6rem; padding: 0.7rem 1.45rem; border-radius: 10px; font-family: 'DM Mono', monospace; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
.badge-benchmark { background: #f8f0fc; border: 1px solid #9c36b5; color: #9c36b5; }
.badge-fragile   { background: #fff5f5; border: 1px solid #fa5252; color: #fa5252; }
.badge-efficient { background: #ebfbee; border: 1px solid #2f9e44; color: #2f9e44; }
.badge-legacy    { background: #e7f5ff; border: 1px solid #1971c2; color: #1971c2; }
.badge-default   { background: #f8f9fa; border: 1px solid #dee2e6; color: #495057; }
.badge-desc { font-size: 1.05rem; color: #000000; font-weight: 700; white-space: nowrap; }
.status-row { display: flex; align-items: center; flex-wrap: nowrap; gap: 0.8rem; margin-top: 1.25rem; white-space: nowrap; }

.section-header { border-bottom: 1px solid #e2e2e0; margin-bottom: 1.25rem; padding-bottom: 0.6rem; }
.section-number { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #a0a09a; letter-spacing: 0.15em; margin-right: 0.5rem; }
.section-title  { font-family: 'Playfair Display', serif; font-size: 1.15rem; color: #1a1c20; }

.explain-wrap { background: #ffffff; border: 1px solid #e8e8e6; border-radius: 14px; padding: 1.1rem 1.2rem; margin-bottom: 1rem; }
.explain-head { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 900; color: #1a1c20; line-height: 1.2; margin-bottom: 0.3rem; }
.explain-sub  { font-family: 'DM Mono', monospace; font-size: 0.66rem; letter-spacing: 0.14em; text-transform: uppercase; color: #7a8399; margin-bottom: 0.9rem; }
.explain-grid { display: grid; grid-template-columns: repeat(3, minmax(180px, 1fr)); gap: 0.8rem; }
.explain-card { background: #fcfcfb; border: 1px solid #ecebe8; border-radius: 10px; padding: 0.8rem 0.85rem; }
.explain-card h4 { margin: 0 0 0.45rem 0; font-family: 'DM Mono', monospace; letter-spacing: 0.08em; font-size: 0.72rem; text-transform: uppercase; }
.exp-rel h4  { color: #b08d20; }
.exp-reli h4 { color: #2a7a9e; }
.exp-repu h4 { color: #7e46b0; }
.explain-card ul { margin: 0; padding-left: 1rem; color: #4a4a48; font-size: 0.88rem; line-height: 1.5; }

.focus-wrap  { background: #ffffff; border: 1px solid #e8e8e6; border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 1rem; overflow-x: auto; }
.focus-title { font-family: 'Playfair Display', serif; font-size: 1.35rem; font-weight: 900; color: #1a1c20; margin-bottom: 0.65rem; }
.focus-table { width: 100%; border-collapse: collapse; min-width: 860px; }
.focus-table th, .focus-table td { border: 1px solid #d9d8d5; padding: 0.58rem 0.55rem; vertical-align: top; color: #3f403d; line-height: 1.35; }
.focus-table th { background: #f4f2ee; font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; }
.focus-stage { font-family: 'DM Mono', monospace; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; white-space: nowrap; background: #faf9f6; }

.alert-box   { border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; font-size: 0.85rem; line-height: 1.5; border-left: 3px solid; }
.alert-critical { background: #fff5f5; border-color: #fa5252; color: #c92a2a; }
.alert-warning  { background: #fff9db; border-color: #fab005; color: #e67700; }
.alert-info     { background: #e7f5ff; border-color: #339af0; color: #1864ab; }
.alert-success  { background: #ebfbee; border-color: #40c057; color: #2b8a3e; }
.alert-title { font-weight: 700; letter-spacing: 0.03em; margin-bottom: 0.2rem; }

.download-btn {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: #1a1c20; color: #ffffff;
    font-family: 'DM Mono', monospace; font-size: 0.8rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 0.75rem 1.5rem; border-radius: 8px;
    text-decoration: none; font-weight: 600;
    border: none; cursor: pointer; margin: 0.5rem 0;
}
hr { border-color: #e2e2e0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
RESPONSE_MAP = {
    "Completely disagree": 1, "Disagree": 2,
    "Don't Know, Can't Say": 3, "don't know ,can't say": 3,
    "Agree": 4, "Completely agree": 5, "Completely Agree": 5,
}

BAND_LABELS = {
    (0, 40):   ("Fragile",    "band-fragile"),
    (40, 60):  ("Emerging",   "band-emerging"),
    (60, 75):  ("Developing", "band-developing"),
    (75, 90):  ("Strong",     "band-strong"),
    (90, 101): ("Benchmark",  "band-benchmark"),
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#4a4a48", size=11),
    margin=dict(l=20, r=20, t=40, b=20),
)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_band(score):
    for (lo, hi), (label, css) in BAND_LABELS.items():
        if lo <= score < hi:
            return label, css
    return "Benchmark", "band-benchmark"

def score_to_color(score):
    if score < 40:  return "#ef4444"
    if score < 60:  return "#f59e0b"
    if score < 75:  return "#3b82f6"
    if score < 90:  return "#10b981"
    return "#a78bfa"

def get_strategic_profile(row):
    gi   = row['Growth_Index']
    rel  = row['Relevance']
    reli = row['Reliability_Adj']
    repu = row['Reputability_Adj']
    if gi >= 85:
        return "🏆 Benchmark Institution", "badge-benchmark", "Market leader and legacy institution setting the standard for peers."
    if rel > 70 and reli < 50:
        return "⚡ Fragile Starter", "badge-fragile", "Strong vision and relevance, but operational systems are failing to match ambition."
    if reli > 70 and rel < 50:
        return "⚙️ Efficient Machine", "badge-efficient", "Consistent delivery and strong systems, but at risk of becoming obsolete."
    if reli > 60 and repu > 60:
        return "📜 Legacy Builder", "badge-legacy", "Strong operational systems and actively building long-term market authority."
    if gi < 40:
        return "🛑 Fragile Foundation", "badge-fragile", "Immediate intervention required — core foundations are critically weak."
    return "🌱 Emerging", "badge-default", "Moving out of survival phase and stabilising core operations."


# ─────────────────────────────────────────────
#  SCORING ENGINE
# ─────────────────────────────────────────────
def calculate_metrics(df):
    df = df.copy()
    for i in [1, 2, 3, 4, 5]:
        df[f'S{i}'] = (5 - df[f'Q{i}']) * 25
    for i in range(6, 21):
        df[f'S{i}'] = (df[f'Q{i}'] - 1) * 25

    df['Relevance']      = df[['S1','S2','S5','S11','S13','S14']].mean(axis=1)
    df['Rel_Raw']        = df[['S3','S4','S6','S7','S8','S9','S10','S12','S14','S15']].mean(axis=1)
    df['Rep_Raw']        = df[['S16','S17','S18','S19','S20']].mean(axis=1)
    df['Reliability_Adj']  = df['Rel_Raw'] * (0.75 + 0.25 * df['Relevance'] / 100)
    min_floor              = df[['Relevance','Reliability_Adj']].min(axis=1)
    df['Reputability_Adj'] = df['Rep_Raw'] * (0.60 + 0.40 * min_floor / 100)
    df['Foundation']    = df[[f'Q{i}' for i in range(1, 6)]].mean(axis=1)
    df['Growth']        = df[[f'Q{i}' for i in range(6, 11)]].mean(axis=1)
    df['Acceleration']  = df[[f'Q{i}' for i in range(11, 16)]].mean(axis=1)
    df['Legacy']        = df[[f'Q{i}' for i in range(16, 21)]].mean(axis=1)
    df['Growth_Index']  = 0.35*df['Relevance'] + 0.40*df['Reliability_Adj'] + 0.25*df['Reputability_Adj']
    return df


# ─────────────────────────────────────────────
#  PLOTLY CHARTS (web UI)
# ─────────────────────────────────────────────
def radar_chart(row):
    cats = ['Foundation', 'Growth', 'Acceleration', 'Legacy']
    vals = [row[c] for c in cats]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]],
        fill='toself', fillcolor='rgba(60,100,160,0.10)',
        line=dict(color='#3a6eb5', width=2),
        hovertemplate='%{theta}: %{r:.2f}<extra></extra>',
    ))
    fig.add_trace(go.Scatterpolar(
        r=[4,4,4,4,4], theta=cats+[cats[0]],
        line=dict(color='rgba(0,0,0,0.15)', width=1, dash='dash'),
        mode='lines', hoverinfo='skip',
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor='rgba(250,250,248,0.9)',
            radialaxis=dict(visible=True, range=[0,5], gridcolor='#e8e8e6', tickfont=dict(size=9)),
            angularaxis=dict(color='#4a4a48', gridcolor='#e8e8e6'),
        ),
        showlegend=False, height=320,
    )
    return fig

def gauge_chart(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        number=dict(font=dict(family="Playfair Display", size=36, color=color), valueformat=".1f"),
        gauge=dict(
            axis=dict(range=[0,100], tickwidth=0, visible=False),
            bar=dict(color=color, thickness=0.65),
            bgcolor='rgba(0,0,0,0)', borderwidth=0,
            steps=[
                dict(range=[0,40],   color='rgba(239,68,68,0.12)'),
                dict(range=[40,60],  color='rgba(245,158,11,0.10)'),
                dict(range=[60,75],  color='rgba(59,130,246,0.10)'),
                dict(range=[75,90],  color='rgba(16,185,129,0.10)'),
                dict(range=[90,100], color='rgba(167,139,250,0.12)'),
            ],
        ),
    ))
    fig.update_layout(
        **PLOTLY_THEME, height=200,
        title=dict(text=title, font=dict(size=11, family='DM Mono', color='#888880'), x=0.5, y=0.95),
    )
    return fig

def sigmoid_position_chart(value):
    x = np.linspace(0, 100, 400)
    y = 1 / (1 + np.exp(-0.12*(x-50)))
    y_val = 1 / (1 + np.exp(-0.12*(value-50)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#9aa3b2', width=3), hoverinfo='skip'))
    fig.add_trace(go.Scatter(
        x=[value], y=[y_val], mode='markers',
        marker=dict(size=16, color='#1e7d54', line=dict(color='#ffffff', width=3)),
        hovertemplate="Growth Index: %{x:.1f}<extra></extra>",
    ))
    fig.add_annotation(
        x=value, y=y_val, text="<b>You are here</b>",
        showarrow=True, arrowhead=2, arrowcolor='#1e7d54',
        ax=65, ay=-35, font=dict(size=12, color='#1e7d54'),
        bgcolor='rgba(255,255,255,0.9)', bordercolor='#1e7d54', borderwidth=1,
    )
    theme = {k: v for k, v in PLOTLY_THEME.items() if k != 'margin'}
    fig.update_layout(
        **theme, height=238,
        margin=dict(l=30, r=10, t=12, b=28),
        xaxis=dict(range=[0,100], title='Growth Index', gridcolor='#f0f0ee', zeroline=False),
        yaxis=dict(range=[0,1], title='Maturity Momentum', gridcolor='#f4f4f2', zeroline=False),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────
#  HTML COMPONENTS (web)
# ─────────────────────────────────────────────
def kpi_card(label, value, card_cls, val_cls):
    band_label, band_css = get_band(value)
    return f"""<div class="kpi-card {card_cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {val_cls}">{value:.0f}</div>
        <span class="kpi-band {band_css}">{band_label}</span>
    </div>"""

def section_header(num, title):
    return f"""<div class="section-header">
        <span class="section-number">{num}</span>
        <span class="section-title">{title}</span>
    </div>"""

def stage_bar_html(row):
    stages = [
        ("Foundation Pressure",    row['Foundation'],   5, "#c2a24c"),
        ("Growth Stability",       row['Growth'],       5, "#3a8fb5"),
        ("Acceleration Readiness", row['Acceleration'], 5, "#9b5fcf"),
        ("Legacy Strength",        row['Legacy'],       5, "#2e9c6e"),
    ]
    bars = ""
    for label, val, max_val, color in stages:
        pct = (val / max_val) * 100
        bars += (f'<div class="stage-row">'
                 f'<span class="stage-label">{label}</span>'
                 f'<div class="stage-track"><div class="stage-fill" style="width:{pct:.1f}%;background:{color};"></div></div>'
                 f'<span class="stage-val">{val:.2f}</span></div>')
    return f'<div class="stage-bar-wrap stage-profile-offset">{bars}</div>'

def alert_html(cls, title, body):
    return f"""<div class="alert-box alert-{cls}"><div class="alert-title">{title}</div>{body}</div>"""

def score_explanation_html():
    return """<div class="explain-wrap">
    <div class="explain-head">How Your Scores Are Calculated</div>
    <div class="explain-sub">R-Cube Scoring Framework</div>
    <div class="explain-grid">
        <div class="explain-card exp-rel"><h4>Relevance</h4><ul>
            <li>The school meets the immediate needs of parents and students.</li>
            <li>Focus on curriculum alignment, compliance, visibility, and initial trust-building.</li>
            <li>Unique value proposition that differentiates from other schools.</li>
        </ul></div>
        <div class="explain-card exp-reli"><h4>Reliability</h4><ul>
            <li>Parents and the community trust consistent delivery year after year.</li>
            <li>Strong academic outcomes, defined SOPs, teacher stability, and structured parent engagement.</li>
            <li>Scaled by empowering middle leaders and embedding technology.</li>
        </ul></div>
        <div class="explain-card exp-repu"><h4>Reputability</h4><ul>
            <li>Recognized at state, national, or international levels.</li>
            <li>Legacy-building: research, publications, alumni networks, awards, and collaborations.</li>
            <li>Parents choose the school as a benchmark of excellence.</li>
        </ul></div>
    </div></div>"""

def growth_stage_focus_html():
    return """<div class="focus-wrap">
    <div class="focus-title">Growth Stages and Focus</div>
    <table class="focus-table"><thead><tr>
        <th></th><th>Management</th><th>School Leader</th><th>Faculty</th>
    </tr></thead><tbody>
    <tr><td class="focus-stage">Foundation</td>
        <td>Capital investment, brand positioning, community outreach, and long-term vision.</td>
        <td>Establish operational systems (admissions, timetable, discipline, communication).</td>
        <td>Adapt to school culture, set academic benchmarks, and engage parents directly.</td></tr>
    <tr><td class="focus-stage">Growth</td>
        <td>Shift from firefighting to governance — set clear policies, delegate authority, monitor performance.</td>
        <td>Drive academic quality, teacher mentoring, and parent engagement.</td>
        <td>Deliver consistent results; adopt professional development and modern pedagogy.</td></tr>
    <tr><td class="focus-stage">Acceleration</td>
        <td>Strategic investments for innovation; alliances with universities, corporates, international partners.</td>
        <td>Transformational leadership — culture, innovation, teacher empowerment, and visibility.</td>
        <td>Move from teaching to mentoring; collaborate on curriculum enrichment, research, and competitions.</td></tr>
    <tr><td class="focus-stage">Consolidation</td>
        <td>Sustainability, diversification, succession planning, and creating a legacy.</td>
        <td>Become ambassadors and thought leaders; groom next-line leaders.</td>
        <td>Advanced professional development, research, publications, and pedagogy innovation.</td></tr>
    </tbody></table></div>"""

def get_action_alerts(row):
    alerts = []
    rel, reli, repu = row['Relevance'], row['Reliability_Adj'], row['Reputability_Adj']
    fdn, grw, acc, leg = row['Foundation'], row['Growth'], row['Acceleration'], row['Legacy']
    if fdn > grw:
        alerts.append(("warning", "⚠ Friction Detected",
            "Foundation Pressure exceeds Growth Stability. Stabilise basic SOPs before investing in growth initiatives."))
    if acc > grw and grw < 3:
        alerts.append(("warning", "⚡ Stage Skip Risk",
            "Acceleration Readiness appears higher than Growth Stability. Build systems first."))
    mins = {"Relevance": rel, "Reliability": reli, "Reputability": repu}
    lowest_k = min(mins, key=mins.get)
    prescriptions = {
        "Relevance":    "Focus on curriculum innovation, competitive differentiation, and future-facing positioning.",
        "Reliability":  "Invest in operational systems, leadership depth, academic consistency, and parent processes.",
        "Reputability": "Activate alumni engagement, third-party recognition, and brand authority programmes.",
    }
    alerts.append(("critical", f"🎯 Priority 1 — {lowest_k} ({mins[lowest_k]:.0f})", prescriptions[lowest_k]))
    highest_k = max(mins, key=mins.get)
    alerts.append(("success", f"✅ Leverage Strength — {highest_k}",
        f"Your {highest_k.lower()} score is your strongest pillar ({mins[highest_k]:.0f}). Build strategic initiatives that amplify this advantage."))
    if leg > grw + 0.8:
        alerts.append(("info", "📜 Legacy Disconnect",
            "Legacy aspirations significantly outpace Growth Stability. External reputation is hard to sustain without mature internal systems."))
    return alerts


# ═══════════════════════════════════════════════════════
#  PDF GENERATION — MATPLOTLIB CHARTS + REPORTLAB LAYOUT
# ═══════════════════════════════════════════════════════

# Color palette for PDF
PDF_COLORS = {
    'gold':    '#B08D20',
    'blue':    '#2A7A9E',
    'purple':  '#7E46B0',
    'green':   '#1E7D54',
    'text':    '#1A1C20',
    'subtext': '#666660',
    'border':  '#E8E8E6',
    'bg':      '#FDFCF9',
    'light':   '#F4F2EE',
}

def mpl_fig_to_bytes(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    return buf

def make_gauge_mpl(value, title, color, size=(3.2, 2.0)):
    fig, ax = plt.subplots(figsize=size, facecolor='white')
    ax.set_aspect('equal')
    ax.axis('off')

    # Background arc
    theta_range = np.linspace(np.pi, 0, 200)
    ax.plot(np.cos(theta_range)*0.85, np.sin(theta_range)*0.85,
            lw=16, color='#F0F0EE', solid_capstyle='butt')

    # Band colouring
    bands = [(0,40,'#FFEAEA'), (40,60,'#FFF8E1'), (60,75,'#E8F4FD'), (75,90,'#E8F8EE'), (90,100,'#F3E8FF')]
    for lo, hi, bc in bands:
        t = np.linspace(np.pi*(1 - lo/100), np.pi*(1 - hi/100), 60)
        ax.plot(np.cos(t)*0.85, np.sin(t)*0.85, lw=14, color=bc, solid_capstyle='butt')

    # Value arc
    t_val = np.linspace(np.pi, np.pi*(1 - value/100), 200)
    ax.plot(np.cos(t_val)*0.85, np.sin(t_val)*0.85, lw=14, color=color, solid_capstyle='butt')

    # Needle
    angle = np.pi*(1 - value/100)
    ax.plot([0, 0.65*np.cos(angle)], [0, 0.65*np.sin(angle)], color=color, lw=2.5)
    ax.scatter([0], [0], s=40, color=color, zorder=5)

    ax.text(0, -0.15, f"{value:.0f}", ha='center', va='center',
            fontsize=22, fontweight='bold', color=color, fontfamily='serif')
    ax.text(0, -0.38, title, ha='center', va='center',
            fontsize=7, color='#888880', fontfamily='monospace')

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.55, 1.1)
    fig.tight_layout(pad=0.1)
    return fig

def make_radar_mpl(row, size=(3.8, 3.2)):
    cats  = ['Foundation', 'Growth', 'Acceleration', 'Legacy']
    vals  = [row[c] for c in cats]
    N     = len(cats)
    angles = [n/N*2*np.pi for n in range(N)] + [0]
    vals_plot = vals + [vals[0]]

    fig, ax = plt.subplots(figsize=size, subplot_kw=dict(polar=True), facecolor='white')
    ax.set_facecolor('#FAFAF8')

    # Grid and benchmark
    for level in [1,2,3,4,5]:
        ax.plot(angles, [level]*N+[level], color='#E8E8E6', lw=0.8, zorder=1)
    ax.plot(angles, [4]*N+[4], color='#CCCCCC', lw=1, ls='--', zorder=2, label='Benchmark (4)')

    # Data
    ax.fill(angles, vals_plot, color='#3A6EB5', alpha=0.12, zorder=3)
    ax.plot(angles, vals_plot, color='#3A6EB5', lw=2, zorder=4)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=8, color='#4A4A48', fontfamily='monospace')
    ax.set_ylim(0, 5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(['1','2','3','4','5'], fontsize=6, color='#AAAAAA')
    ax.spines['polar'].set_color('#E8E8E6')
    ax.grid(False)
    fig.tight_layout(pad=0.3)
    return fig

def make_stage_bars_mpl(row, size=(4.5, 2.6)):
    stages = [
        ("Foundation Pressure",    row['Foundation'],   "#C2A24C"),
        ("Growth Stability",       row['Growth'],       "#3A8FB5"),
        ("Acceleration Readiness", row['Acceleration'], "#9B5FCF"),
        ("Legacy Strength",        row['Legacy'],       "#2E9C6E"),
    ]
    fig, ax = plt.subplots(figsize=size, facecolor='white')
    ax.set_facecolor('white')
    ax.axis('off')

    y_positions = [0.78, 0.54, 0.30, 0.06]
    bar_height  = 0.14
    for (label, val, color), y in zip(stages, y_positions):
        pct = val / 5.0
        # Track
        ax.barh(y, 1.0, height=bar_height, left=0, color='#F0F0EE',
                align='center', zorder=1)
        # Fill
        ax.barh(y, pct, height=bar_height, left=0, color=color,
                align='center', zorder=2)
        # Label
        ax.text(-0.02, y, label, ha='right', va='center',
                fontsize=7.5, color='#666660', fontfamily='monospace',
                fontweight='bold')
        # Value
        ax.text(1.03, y, f"{val:.2f}", ha='left', va='center',
                fontsize=8, color='#4A4A48', fontfamily='monospace')

    ax.set_xlim(-0.55, 1.15)
    ax.set_ylim(-0.1, 0.95)
    fig.tight_layout(pad=0.2)
    return fig

def make_sigmoid_mpl(value, size=(4.5, 2.2)):
    x = np.linspace(0, 100, 400)
    y = 1 / (1 + np.exp(-0.12*(x-50)))
    y_val = 1 / (1 + np.exp(-0.12*(value-50)))

    fig, ax = plt.subplots(figsize=size, facecolor='white')
    ax.set_facecolor('white')
    ax.plot(x, y, color='#9AA3B2', lw=2.5, zorder=2)
    ax.scatter([value], [y_val], s=120, color='#1E7D54',
               zorder=5, linewidths=2.5, edgecolors='white')
    ax.annotate("You are here", xy=(value, y_val),
                xytext=(value+12, y_val+0.08),
                fontsize=8, color='#1E7D54', fontfamily='sans-serif',
                arrowprops=dict(arrowstyle='->', color='#1E7D54', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='#1E7D54', lw=0.8))
    ax.set_xlabel('Growth Index', fontsize=8, color='#666660')
    ax.set_ylabel('Maturity Momentum', fontsize=8, color='#666660')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=7, colors='#888880')
    for spine in ax.spines.values():
        spine.set_edgecolor('#E8E8E6')
    ax.grid(axis='y', color='#F0F0EE', lw=0.6)
    fig.tight_layout(pad=0.4)
    return fig

def make_q_grid_mpl(row, size=(7.5, 4.0)):
    fig, axes = plt.subplots(4, 5, figsize=size, facecolor='white')
    fig.patch.set_facecolor('white')
    stage_colors = {
        'FDN': '#C2A24C', 'GRW': '#3A8FB5',
        'ACC': '#9B5FCF', 'LEG': '#2E9C6E',
    }
    stage_tags = ['FDN']*5 + ['GRW']*5 + ['ACC']*5 + ['LEG']*5

    for idx in range(20):
        r, c = divmod(idx, 5)
        ax = axes[r][c]
        ax.set_facecolor('#FCFCFB')
        for spine in ax.spines.values():
            spine.set_edgecolor('#E8E8E6')
            spine.set_linewidth(0.8)
        ax.set_xticks([]); ax.set_yticks([])

        q_num = idx + 1
        score = row[f'S{q_num}']
        color = score_to_color(score)
        stag  = stage_tags[idx]

        ax.text(0.5, 0.78, f"Q{q_num} · {stag}", ha='center', va='center',
                fontsize=6, color='#8A8A84', transform=ax.transAxes,
                fontfamily='monospace')
        ax.text(0.5, 0.45, f"{score:.0f}", ha='center', va='center',
                fontsize=16, fontweight='bold', color=color,
                transform=ax.transAxes, fontfamily='serif')
        dot_x, dot_y = 0.5, 0.14
        ax.scatter([dot_x], [dot_y], s=28, color=color,
                   transform=ax.transAxes, zorder=5, clip_on=False)

    fig.subplots_adjust(hspace=0.25, wspace=0.25, left=0.01, right=0.99, top=0.97, bottom=0.03)
    return fig


# ─────────────────────────────────────────────
#  REPORTLAB PDF BUILDER
# ─────────────────────────────────────────────
def build_pdf(row, results, user_id):
    buf = io.BytesIO()
    PAGE_W, PAGE_H = A4
    MARGIN = 18*mm

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14*mm, bottomMargin=14*mm,
        title=f"R-Cube Strategic Report — {user_id}",
    )

    styles = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, parent=styles['Normal'], **kw)

    sTitle   = S('sTitle',   fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#1A1C20'), spaceAfter=2)
    sSubtag  = S('sSubtag',  fontName='Helvetica',      fontSize=7,  textColor=colors.HexColor('#888880'), spaceAfter=4, leading=10)
    sBadge   = S('sBadge',   fontName='Helvetica-Bold', fontSize=8.5,textColor=colors.HexColor('#1E7D54'), spaceAfter=3)
    sSecHead = S('sSecHead', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1A1C20'), spaceAfter=5, spaceBefore=8)
    sFooter  = S('sFooter',  fontName='Helvetica',      fontSize=7,  textColor=colors.HexColor('#AAAAAA'), alignment=TA_CENTER)
    sTblHdr  = S('sTblHdr',  fontName='Helvetica-Bold', fontSize=7,  textColor=colors.HexColor('#1A1C20'), leading=9)
    sTblCell = S('sTblCell', fontName='Helvetica',      fontSize=7.5,textColor=colors.HexColor('#3A3A38'), leading=12)
    sKpiLbl  = S('sKpiLbl',  fontName='Helvetica',      fontSize=6.5,textColor=colors.HexColor('#888880'), leading=9, spaceAfter=2)
    sKpiVal  = S('sKpiVal',  fontName='Helvetica-Bold', fontSize=28, textColor=colors.HexColor('#1A1C20'), leading=30)
    sKpiBand = S('sKpiBand', fontName='Helvetica-Bold', fontSize=7,  textColor=colors.HexColor('#666660'), leading=9)
    sExpHdr  = S('sExpHdr',  fontName='Helvetica-Bold', fontSize=7.5,leading=10, spaceAfter=4)
    sExpBody = S('sExpBody', fontName='Helvetica',      fontSize=7.5,textColor=colors.HexColor('#3A3A38'), leading=12)

    story = []
    W = PAGE_W - 2*MARGIN

    def divider():
        return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#E2E2E0'), spaceAfter=5, spaceBefore=5)

    def sec(num, title):
        return Paragraph(f'<font color="#888880" size="8">{num}&nbsp;&nbsp;</font>{title}', sSecHead)

    def fig_img(fig, width_mm, height_mm=None, dpi=180):
        buf2 = mpl_fig_to_bytes(fig, dpi=dpi)
        w = width_mm * mm
        if height_mm:
            return RLImage(buf2, width=w, height=height_mm*mm)
        return RLImage(buf2, width=w)

    def kpi_box(label, value, band, accent):
        """Returns a Table cell that looks like a KPI card."""
        band_bg = {
            'Fragile':    '#FFF5F5', 'Emerging':   '#FFF9DB',
            'Developing': '#E7F5FF', 'Strong':     '#EBFBEE', 'Benchmark':  '#F8F0FC',
        }.get(band, '#F4F4F2')

        lbl  = Paragraph(label.upper(), S(f'kl{label}', fontName='Helvetica', fontSize=6,
                          textColor=colors.HexColor('#888880'), leading=8))
        val  = Paragraph(f'<font size="30" color="{accent}"><b>{value:.0f}</b></font>',
                         S(f'kv{label}', fontName='Helvetica-Bold', fontSize=30,
                           textColor=colors.HexColor(accent), leading=32))
        bnd  = Paragraph(band, S(f'kb{label}', fontName='Helvetica-Bold', fontSize=6.5,
                          textColor=colors.HexColor(accent), leading=8))

        inner = Table([[lbl], [val], [bnd]], colWidths=[W/4 - 6*mm])
        inner.setStyle(TableStyle([
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
            ('TOPPADDING',    (0,0),(-1,-1), 0),
            ('BOTTOMPADDING', (0,0),(-1,-1), 2),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ]))

        outer = Table([[inner]], colWidths=[W/4 - 4*mm])
        outer.setStyle(TableStyle([
            ('BOX',           (0,0),(-1,-1), 0.5, colors.HexColor('#E8E8E6')),
            ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#FFFFFF')),
            ('LEFTPADDING',   (0,0),(-1,-1), 8),
            ('RIGHTPADDING',  (0,0),(-1,-1), 6),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LINEABOVE',     (0,0),(-1,0),  2.5, colors.HexColor(accent)),
        ]))
        return outer

    # ════════ HEADER ════════
    label, _, desc = get_strategic_profile(row)
    gi = row['Growth_Index']
    band_label, _ = get_band(gi)

    story.append(Paragraph("R-Cube Strategic Intelligence  ·  Individual Strategic Report", sSubtag))
    story.append(Paragraph(f"Individual Strategic Report — {user_id}", sTitle))
    story.append(Paragraph(f"{label}  ·  {desc}", sBadge))
    story.append(divider())
    story.append(Spacer(1, 3*mm))

    # ════════ KPI ROW — 4 cards + sigmoid ════════
    gi_band, _ = get_band(gi)
    rel_band, _ = get_band(row['Relevance'])
    reli_band, _ = get_band(row['Reliability_Adj'])
    repu_band, _ = get_band(row['Reputability_Adj'])

    gi_box   = kpi_box("Growth Index",     gi,                     gi_band,   '#1E7D54')
    rel_box  = kpi_box("Relevance",        row['Relevance'],        rel_band,  '#B08D20')
    reli_box = kpi_box("Reliability (Adj)",row['Reliability_Adj'],  reli_band, '#2A7A9E')
    repu_box = kpi_box("Reputability (Adj)",row['Reputability_Adj'],repu_band, '#7E46B0')

    sig_fig = make_sigmoid_mpl(gi, size=(4.0, 2.0))
    sig_img = fig_img(sig_fig, 85, 46)

    # Left: 4 KPI cards stacked 2x2; Right: sigmoid
    top_kpi = Table([[gi_box, rel_box]], colWidths=[W*0.24, W*0.24])
    top_kpi.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    bot_kpi = Table([[reli_box, repu_box]], colWidths=[W*0.24, W*0.24])
    bot_kpi.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))
    kpi_stack = Table([[top_kpi], [bot_kpi]], colWidths=[W*0.50])
    kpi_stack.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))

    hero_tbl = Table([[kpi_stack, sig_img]], colWidths=[W*0.50, W*0.50])
    hero_tbl.setStyle(TableStyle([
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))
    story.append(hero_tbl)
    story.append(Spacer(1, 4*mm))
    story.append(divider())

    # ════════ SECTION 01: Gauges ════════
    story.append(sec("01", "R-Cube Maturity Gauges"))

    gauge_data = [
        (row['Relevance'],        "RELEVANCE",         PDF_COLORS['gold']),
        (row['Reliability_Adj'],  "RELIABILITY (ADJ)", PDF_COLORS['blue']),
        (row['Reputability_Adj'], "REPUTABILITY (ADJ)",PDF_COLORS['purple']),
    ]
    gauge_imgs = []
    for val, ttl, col in gauge_data:
        gf = make_gauge_mpl(val, ttl, col, size=(2.8, 1.9))
        gauge_imgs.append(fig_img(gf, W/3/mm - 3, 47))

    gauge_tbl = Table([gauge_imgs], colWidths=[W/3]*3)
    gauge_tbl.setStyle(TableStyle([
        ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0),(-1,-1), 2),
        ('RIGHTPADDING', (0,0),(-1,-1), 2),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))
    story.append(gauge_tbl)
    story.append(Spacer(1, 3*mm))
    story.append(divider())

    # ════════ SECTION 02: How Scores Are Calculated (full content) ════════
    story.append(sec("02", "How Your Scores Are Calculated"))

    rel_bullets = [
        "The school meets the immediate needs of parents and students.",
        "The focus is on curriculum alignment, compliance, visibility, and initial trust-building.",
        "The school has a unique value proposition that differentiates it from other schools.",
    ]
    reli_bullets = [
        "Parents and the community trust that the school delivers consistently year after year.",
        "This means strong academic outcomes, defined SOPs, teacher stability, and structured parent engagement.",
        "The school has a system that can be scaled by empowering middle leaders, embedding technology, and maintaining quality across larger student numbers.",
    ]
    repu_bullets = [
        "The school is recognized at state, national, or international levels.",
        "The school engages in legacy-building initiatives such as research, publications, alumni networks, awards, and collaborations.",
        "Parents choose the school because it is seen as a benchmark of excellence.",
    ]

    def exp_cell(title, accent, bullets):
        items = [Paragraph(f'<font color="{accent}"><b>{title}</b></font>',
                            S(f'eh{title}', fontName='Helvetica-Bold', fontSize=7, leading=10, spaceAfter=5))]
        for b in bullets:
            items.append(Paragraph(f'• {b}', sExpBody))
        return items

    exp_rows = [[
        exp_cell("RELEVANCE",    '#B08D20', rel_bullets),
        exp_cell("RELIABILITY",  '#2A7A9E', reli_bullets),
        exp_cell("REPUTABILITY", '#7E46B0', repu_bullets),
    ]]
    exp_tbl = Table(exp_rows, colWidths=[W/3]*3)
    exp_tbl.setStyle(TableStyle([
        ('BOX',          (0,0),(-1,-1), 0.5, colors.HexColor('#E8E8E6')),
        ('INNERGRID',    (0,0),(-1,-1), 0.5, colors.HexColor('#E8E8E6')),
        ('BACKGROUND',   (0,0),(-1,-1), colors.HexColor('#FCFCFB')),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('TOPPADDING',   (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ]))
    story.append(exp_tbl)
    story.append(Spacer(1, 3*mm))
    story.append(divider())

    # ════════ SECTION 03: Stage Profile + Radar ════════
    story.append(sec("03", "Growth Stage Profile"))

    stage_fig = make_stage_bars_mpl(row)
    radar_fig = make_radar_mpl(row)
    stage_img = fig_img(stage_fig, W*0.46/mm, 60)
    radar_img = fig_img(radar_fig, W*0.50/mm, 60)

    stage_tbl = Table([[stage_img, radar_img]], colWidths=[W*0.48, W*0.52])
    stage_tbl.setStyle(TableStyle([
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))
    story.append(stage_tbl)
    story.append(Spacer(1, 3*mm))
    story.append(divider())

    # ════════ SECTION 04: Growth Stages and Focus Table ════════
    story.append(sec("04", "Growth Stages and Focus"))

    focus_header = [
        Paragraph("Stage",        sTblHdr),
        Paragraph("Management",   sTblHdr),
        Paragraph("School Leader",sTblHdr),
        Paragraph("Faculty",      sTblHdr),
    ]
    focus_data = [
        ["Foundation",
         "Focus on capital investment, brand positioning, community outreach, and long-term vision.",
         "Establish operational systems (admissions, timetable, discipline, communication).",
         "Adapt to school culture, set academic benchmarks, and engage parents directly."],
        ["Growth",
         "Shift from firefighting to governance — set clear policies, delegate authority, monitor performance.",
         "Drive academic quality, teacher mentoring, and parent engagement.",
         "Deliver consistent results; adopt professional development and modern pedagogy."],
        ["Acceleration",
         "Provide strategic investments for innovation; build alliances with universities, corporates, and international partners.",
         "Shift to transformational leadership — focusing on culture, innovation, teacher empowerment, and visibility.",
         "Move from teaching to mentoring and innovating; collaborate on curriculum enrichment, research, and competitions."],
        ["Consolidation",
         "Focus on sustainability, diversification, succession planning, and creating a legacy.",
         "Become ambassadors and thought leaders in education forums; groom next-line leaders.",
         "Engage in advanced professional development, research, publications, and innovation in pedagogy."],
    ]
    col_w = [22*mm, (W-22*mm)/3, (W-22*mm)/3, (W-22*mm)/3]
    tbl_data = [focus_header]
    for rd in focus_data:
        tbl_data.append([
            Paragraph(rd[0], S(f'fs{rd[0]}', fontName='Helvetica-Bold', fontSize=7,
                                textColor=colors.HexColor('#1A1C20'), leading=9)),
            Paragraph(rd[1], sTblCell),
            Paragraph(rd[2], sTblCell),
            Paragraph(rd[3], sTblCell),
        ])

    focus_tbl = Table(tbl_data, colWidths=col_w, repeatRows=1)
    focus_tbl.setStyle(TableStyle([
        ('BOX',          (0,0),(-1,-1), 0.5, colors.HexColor('#D9D8D5')),
        ('INNERGRID',    (0,0),(-1,-1), 0.3, colors.HexColor('#E8E8E6')),
        ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor('#F4F2EE')),
        ('BACKGROUND',   (0,1),(0,-1),  colors.HexColor('#FAF9F6')),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('RIGHTPADDING', (0,0),(-1,-1), 5),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ]))
    story.append(focus_tbl)
    story.append(Spacer(1, 5*mm))

    # ════════ FOOTER ════════
    story.append(divider())
    story.append(Paragraph(
        "R-Cube Screening Metric  ·  Edxso Strategic Intelligence  ·  Screening Tool — Not a Full Appraisal",
        sFooter
    ))

    doc.build(story)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem 0;'>
        <div style='font-family: Playfair Display, serif; font-size: 1.5rem; font-weight: 900; color: #1a1c20; line-height: 1.1;'>
            R-Cube<br>Strategic Intelligence
        </div>
        <div style='font-family: DM Mono, monospace; font-size: 0.6rem; letter-spacing: 0.2em; color: #888880; text-transform: uppercase; margin-top: 0.4rem;'>
            Screening Metric v2
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Response CSV", type=["csv"])

    st.markdown("---")
    st.markdown("""
    <div style='font-family: DM Mono, monospace; font-size: 0.6rem; color: #888880; letter-spacing: 0.1em; text-transform: uppercase;'>
    Scoring Model
    </div>
    <div style='font-size: 0.78rem; color: #666660; margin-top: 0.5rem; line-height: 1.6;'>
    <b style='color:#b08d20;'>Relevance</b> — Q1,2,5,11,13,14<br>
    <b style='color:#2a7a9e;'>Reliability</b> — Q3,4,6-10,12,14,15<br>
    <b style='color:#7e46b0;'>Reputability</b> — Q16–20<br><br>
    GI = 0.35·Rel + 0.40·Reli + 0.25·Rep
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if not uploaded_file:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;
                min-height:70vh;text-align:center;padding:2rem;'>
        <div style='font-family:Playfair Display,serif;font-size:3.5rem;font-weight:900;
                    color:#1a1c20;line-height:1.1;max-width:700px;'>
            R-Cube Strategic<br>Command Centre
        </div>
        <div style='font-family:DM Sans,sans-serif;font-size:1rem;color:#666660;
                    margin-top:1rem;max-width:480px;line-height:1.7;'>
            Upload your response CSV to generate per-school strategic profiles,
            maturity-adjusted R-scores, stage diagnostics, and competitive benchmarking.
        </div>
        <div style='margin-top:2.5rem;font-family:DM Mono,monospace;font-size:0.7rem;
                    letter-spacing:0.2em;text-transform:uppercase;color:#888880;
                    border:1px solid #e2e2e0;padding:0.75rem 1.5rem;border-radius:8px;'>
            ← Upload CSV in sidebar to begin
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    raw = pd.read_csv(uploaded_file)
    q_cols = raw.columns[8:28]
    raw = raw.rename(columns={q_cols[i]: f'Q{i+1}' for i in range(len(q_cols))})
    raw.insert(0, 'UserID', [f"User {i+1}" for i in range(len(raw))])
    for i in range(1, 21):
        raw[f'Q{i}'] = raw[f'Q{i}'].map(RESPONSE_MAP).fillna(3)

    results = calculate_metrics(raw)

    with st.sidebar:
        st.markdown("---")
        user_choice = st.selectbox("Select User Report", results['UserID'].tolist())
        avg_gi = results['Growth_Index'].mean()
        rank   = int(results['Growth_Index'].rank(ascending=False)[results['UserID'] == user_choice].values[0])
        st.markdown(f"""
        <div style='margin-top:1rem;'>
            <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#888880;
                        letter-spacing:0.1em;text-transform:uppercase;'>Cohort Size</div>
            <div style='font-family:Playfair Display,serif;font-size:2rem;font-weight:900;color:#1a1c20;'>{len(results)}</div>
            <div style='font-size:0.75rem;color:#666660;'>schools in dataset</div>
        </div>
        <div style='margin-top:1rem;'>
            <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#888880;
                        letter-spacing:0.1em;text-transform:uppercase;'>Cohort Avg GI</div>
            <div style='font-family:Playfair Display,serif;font-size:1.6rem;font-weight:900;color:#1a1c20;'>{avg_gi:.1f}</div>
        </div>
        <div style='margin-top:1rem;'>
            <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#888880;
                        letter-spacing:0.1em;text-transform:uppercase;'>Current Rank</div>
            <div style='font-family:Playfair Display,serif;font-size:1.6rem;font-weight:900;color:#b08d20;'>#{rank} / {len(results)}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        # ── PDF DOWNLOAD BUTTON (sidebar)
        st.markdown("**Export Report**")
        row_for_pdf = results[results['UserID'] == user_choice].iloc[0]
        with st.spinner("Preparing PDF…"):
            pdf_bytes = build_pdf(row_for_pdf, results, user_choice)
        st.download_button(
            label="⬇ Download PDF Report",
            data=pdf_bytes,
            file_name=f"rcube_{user_choice.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    row = results[results['UserID'] == user_choice].iloc[0]
    label, badge_cls, desc = get_strategic_profile(row)

    # ── HEADER
    st.markdown(f"""
    <div style='margin-bottom:0.5rem;'>
        <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#888880;
                    letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>
            Individual Strategic Report
        </div>
        <div style='font-family:Playfair Display,serif;font-size:2.4rem;font-weight:900;
                    color:#1a1c20;line-height:1.1;margin-bottom:0.6rem;'>
            {user_choice}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI + Sigmoid
    k_left, k_right = st.columns([1, 1.45])
    with k_left:
        st.markdown(kpi_card("Growth Index", row['Growth_Index'], "growth", "growth"), unsafe_allow_html=True)
    with k_right:
        st.plotly_chart(sigmoid_position_chart(row['Growth_Index']), use_container_width=True)

    st.markdown(f"""<div class="status-row">
        <span class="status-badge {badge_cls}">{label}</span>
        <span class="badge-desc">{desc}</span>
    </div><br>""", unsafe_allow_html=True)

    # ── Section 01: Gauges
    st.markdown(section_header("01", "R-Cube Maturity Gauges"), unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(gauge_chart(row['Relevance'],        "RELEVANCE",         "#b08d20"), use_container_width=True)
    with g2: st.plotly_chart(gauge_chart(row['Reliability_Adj'],  "RELIABILITY (ADJ)", "#2a7a9e"), use_container_width=True)
    with g3: st.plotly_chart(gauge_chart(row['Reputability_Adj'], "REPUTABILITY (ADJ)","#7e46b0"), use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(score_explanation_html(), unsafe_allow_html=True)

    # ── Section 02: Stage Profile
    st.markdown(section_header("02", "Growth Stage Profile"), unsafe_allow_html=True)
    col_a, col_b = st.columns([1,1])
    with col_a: st.markdown(stage_bar_html(row), unsafe_allow_html=True)
    with col_b: st.plotly_chart(radar_chart(row), use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(growth_stage_focus_html(), unsafe_allow_html=True)
    # ── Download Button
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_bytes = build_pdf(row, results, user_choice)
    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf_bytes,
        file_name=f"rcube_{user_choice.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

    # ── Footer
    st.markdown("""
    <div style='margin-top:2rem;padding-top:1rem;border-top:1px solid #e2e2e0;
                font-family:DM Mono,monospace;font-size:0.6rem;color:#aaaaaa;
                letter-spacing:0.15em;text-transform:uppercase;text-align:center;'>
        R-Cube Screening Metric · Edxso Strategic Intelligence · Screening Tool — Not a Full Appraisal
    </div>
    """, unsafe_allow_html=True)