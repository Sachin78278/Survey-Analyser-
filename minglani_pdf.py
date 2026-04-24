import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components
 
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
#  CUSTOM CSS – Dark editorial theme
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  CUSTOM CSS – Light editorial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
 
/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #fdfcf9; /* Soft Ivory Background */
    color: #1a1c20;
}
 
/* Sidebar */
[data-testid="stSidebar"] {
    background: #f4f2ee !important;
    border-right: 1px solid #e2e2e0;
}
[data-testid="stSidebar"] * { color: #4a4a48 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1a1c20 !important; }
 
/* Main headings */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1a1c20 !important; }
 
/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
 
/* ── KPI Cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.relevance::before  { background: #d4af37; }
.kpi-card.reliability::before { background: #3a8fb5; }
.kpi-card.reputability::before { background: #9b5fcf; }
.kpi-card.growth::before { background: #2e9c6e; }
 
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #888880;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-value.relevance  { color: #b08d20; }
.kpi-value.reliability { color: #2a7a9e; }
.kpi-value.reputability { color: #7e46b0; }
.kpi-value.growth { color: #1e7d54; }
 
.kpi-band {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-top: 0.25rem;
}
.band-fragile     { background: #fff5f5; color: #e03131; }
.band-emerging    { background: #fff9db; color: #f08c00; }
.band-developing  { background: #ebfbee; color: #2f9e44; }
.band-strong      { background: #e7f5ff; color: #1971c2; }
.band-benchmark   { background: #f8f0fc; color: #9c36b5; }
 
/* ── Stage Bar ── */
.stage-bar-wrap {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    border-radius: 12px;
    padding: 1.5rem;
}
.stage-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
.stage-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666660;
    width: 130px;
}
.stage-track {
    flex: 1;
    height: 8px;
    background: #f0f0ee;
    border-radius: 4px;
}
.stage-fill {
    height: 100%;
    border-radius: 4px;
}
.stage-val {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #4a4a48;
}
 
/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 1.2rem;
    border-radius: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-benchmark  { background: #f8f0fc; border: 1px solid #9c36b5; color: #9c36b5; }
.badge-fragile    { background: #fff5f5; border: 1px solid #fa5252; color: #fa5252; }
.badge-efficient  { background: #ebfbee; border: 1px solid #2f9e44; color: #2f9e44; }
.badge-default    { background: #f8f9fa; border: 1px solid #dee2e6; color: #495057; }
 
.badge-desc {
    font-size: 0.82rem;
    color: #666660;
}
 
/* ── Section headers ── */
.section-header {
    border-bottom: 1px solid #e2e2e0;
}
.section-number { color: #a0a09a; }
 
/* ── Brutal Truth bars ── */
.bt-row {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
}
.bt-label-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.4rem;
}
.bt-label {
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    color: #4a4a48;
}
.bt-delta { font-weight: 700; }
.delta-neg { color: #c92a2a; }
.delta-pos { color: #2b8a3e; }
.bt-values {
    font-size: 0.82rem;
    color: #666660;
    white-space: nowrap;
}

/* ── Question Cards ── */
.q-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(120px, 1fr));
    gap: 0.75rem;
}
.q-cell {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    border-radius: 12px;
    min-height: 96px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.6rem 0.4rem;
}
.q-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #8a8a84;
    margin-bottom: 0.25rem;
}
.q-score {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 900;
    line-height: 1;
}
.q-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 0.45rem;
}
@media (max-width: 900px) {
    .q-grid { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
}

/* ── Score Explanation ── */
.explain-wrap {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 1rem;
}
.explain-head {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 900;
    color: #1a1c20;
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.explain-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a8399;
    margin-bottom: 0.9rem;
}
.explain-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(180px, 1fr));
    gap: 0.8rem;
}
.explain-card {
    background: #fcfcfb;
    border: 1px solid #ecebe8;
    border-radius: 10px;
    padding: 0.8rem 0.85rem;
}
.explain-card h4 {
    margin: 0 0 0.45rem 0;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    text-transform: uppercase;
}
.exp-rel h4 { color: #b08d20; }
.exp-reli h4 { color: #2a7a9e; }
.exp-repu h4 { color: #7e46b0; }
.explain-card ul {
    margin: 0;
    padding-left: 1rem;
    color: #4a4a48;
    font-size: 0.88rem;
    line-height: 1.5;
}
@media (max-width: 980px) {
    .explain-grid { grid-template-columns: 1fr; }
}

/* ── Growth Stage Focus Table ── */
.focus-wrap {
    background: #ffffff;
    border: 1px solid #e8e8e6;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    overflow-x: auto;
}
.focus-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 900;
    color: #1a1c20;
    margin-bottom: 0.65rem;
}
.focus-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 860px;
}
.focus-table th,
.focus-table td {
    border: 1px solid #d9d8d5;
    padding: 0.58rem 0.55rem;
    vertical-align: top;
    color: #3f403d;
    line-height: 1.35;
}
.focus-table th {
    background: #f4f2ee;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.focus-stage {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    white-space: nowrap;
    background: #faf9f6;
}

/* Divider */
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
    (0, 40):  ("Fragile",          "band-fragile"),
    (40, 60): ("Emerging",         "band-emerging"),
    (60, 75): ("Developing",       "band-developing"),
    (75, 90): ("Strong",           "band-strong"),
    (90, 101):("Benchmark",        "band-benchmark"),
}
 
STAGE_COLORS = {
    "Foundation":    ("#c2a24c", "#3d2c0a"),
    "Growth":        ("#3a8fb5", "#0a1e2d"),
    "Acceleration":  ("#9b5fcf", "#1e0d35"),
    "Legacy":        ("#2e9c6e", "#071a10"),
}
 
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c8c4bc", size=11),
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
    gi = row['Growth_Index']
    rel  = row['Relevance']
    reli = row['Reliability_Adj']
    repu = row['Reputability_Adj']
 
    if gi >= 85:
        return "🏆 Benchmark Institution", "badge-benchmark", \
               "Market leader and legacy institution setting the standard for peers."
    if rel > 70 and reli < 50:
        return "⚡ Fragile Starter", "badge-fragile", \
               "Strong vision and relevance, but operational systems are failing to match ambition."
    if reli > 70 and rel < 50:
        return "⚙️ Efficient Machine", "badge-efficient", \
               "Consistent delivery and strong systems, but at risk of becoming obsolete."
    if reli > 60 and repu > 60:
        return "📜 Legacy Builder", "badge-legacy", \
               "Strong operational systems and actively building long-term market authority."
    if gi < 40:
        return "🛑 Fragile Foundation", "badge-fragile", \
               "Immediate intervention required — core foundations are critically weak."
    return "🌱 Emerging", "badge-default", \
           "Moving out of survival phase and stabilising core operations."
 
 
# ─────────────────────────────────────────────
#  SCORING ENGINE
# ─────────────────────────────────────────────
def calculate_metrics(df):
    df = df.copy()
 
    # 0–100 conversion
    # Reverse-coded: Q1, Q2, Q3, Q4, Q5
    for i in [1, 2, 3, 4, 5]:
        df[f'S{i}'] = (5 - df[f'Q{i}']) * 25
    # Positive: Q6–Q20
    for i in range(6, 21):
        df[f'S{i}'] = (df[f'Q{i}'] - 1) * 25
 
    # R-Scores (per guide)
    # Relevance: R1, R2, R5, P11, P13, P14
    df['Relevance'] = df[['S1', 'S2', 'S5', 'S11', 'S13', 'S14']].mean(axis=1)
 
    # Reliability raw: R3, R4, P6, P7, P8, P9, P10, P12, P14, P15
    df['Rel_Raw'] = df[['S3', 'S4', 'S6', 'S7', 'S8', 'S9', 'S10', 'S12', 'S14', 'S15']].mean(axis=1)
 
    # Reputability raw: P16–P20
    df['Rep_Raw'] = df[['S16', 'S17', 'S18', 'S19', 'S20']].mean(axis=1)
 
    # Maturity-adjusted scores
    df['Reliability_Adj']   = df['Rel_Raw'] * (0.75 + 0.25 * df['Relevance'] / 100)
    min_floor               = df[['Relevance', 'Reliability_Adj']].min(axis=1)
    df['Reputability_Adj']  = df['Rep_Raw'] * (0.60 + 0.40 * min_floor / 100)
 
    # Stage profiles (raw response averages, 1–5 scale)
    df['Foundation']    = df[[f'Q{i}' for i in range(1, 6)]].mean(axis=1)
    df['Growth']        = df[[f'Q{i}' for i in range(6, 11)]].mean(axis=1)
    df['Acceleration']  = df[[f'Q{i}' for i in range(11, 16)]].mean(axis=1)
    df['Legacy']        = df[[f'Q{i}' for i in range(16, 21)]].mean(axis=1)
 
    # Overall Growth Index
    df['Growth_Index'] = (
        0.35 * df['Relevance'] +
        0.40 * df['Reliability_Adj'] +
        0.25 * df['Reputability_Adj']
    )
 
    return df
 
 
# ─────────────────────────────────────────────
#  CHART BUILDERS
# ─────────────────────────────────────────────
def radar_chart(row):
    cats  = ['Foundation', 'Growth', 'Acceleration', 'Legacy']
    vals  = [row[c] for c in cats]
    colors_r = ["#c2a24c", "#3a8fb5", "#9b5fcf", "#2e9c6e"]
    avg_c = "#e8e4dc"
 
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill='toself',
        fillcolor='rgba(60,100,160,0.12)',
        line=dict(color='#3a6eb5', width=2),
        name='Profile',
        hovertemplate='%{theta}: %{r:.2f}<extra></extra>',
    ))
    # Benchmark line at 4 (=good)
    bench = [4, 4, 4, 4]
    fig.add_trace(go.Scatterpolar(
        r=bench + [bench[0]],
        theta=cats + [cats[0]],
        line=dict(color='rgba(255,255,255,0.12)', width=1, dash='dash'),
        mode='lines',
        name='Benchmark ref',
        hoverinfo='skip',
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor='rgba(20,24,32,0.8)',
            radialaxis=dict(
                visible=True, range=[0, 5],
                color='#3a4557', gridcolor='#1e2430',
                tickfont=dict(size=9, color='#4a5568'),
            ),
            angularaxis=dict(color='#7a8399', gridcolor='#1e2430'),
        ),
        showlegend=False,
        height=320,
    )
    return fig
 
 
def gauge_chart(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(
            font=dict(family="Playfair Display", size=36, color=color),
            suffix="",
            valueformat=".1f",
        ),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=0, tickcolor='rgba(0,0,0,0)', visible=False),
            bar=dict(color=color, thickness=0.65),
            bgcolor='rgba(20,24,32,0)',
            borderwidth=0,
            steps=[
                dict(range=[0, 40],  color='rgba(239,68,68,0.15)'),
                dict(range=[40, 60], color='rgba(245,158,11,0.12)'),
                dict(range=[60, 75], color='rgba(59,130,246,0.12)'),
                dict(range=[75, 90], color='rgba(16,185,129,0.12)'),
                dict(range=[90, 100],color='rgba(167,139,250,0.15)'),
            ],
            threshold=dict(line=dict(color='rgba(255,255,255,0.2)', width=2), thickness=0.8, value=75),
        ),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=200,
        title=dict(text=title, font=dict(size=11, family='DM Mono', color='#7a8399'), x=0.5, y=0.95),
    )
    return fig
 
 
def scatter_chart(results, current_row):
    results = results.copy()
    results['Band'] = results['Growth_Index'].apply(lambda v: get_band(v)[0])
    band_colors = {
        "Fragile": "#ef4444", "Emerging": "#f59e0b",
        "Developing": "#3b82f6", "Strong": "#10b981", "Benchmark": "#a78bfa",
    }
    results['Color'] = results['Band'].map(band_colors)
 
    fig = go.Figure()
 
    for band, grp in results.groupby('Band'):
        fig.add_trace(go.Scatter(
            x=grp['Reliability_Adj'],
            y=grp['Relevance'],
            mode='markers',
            marker=dict(
                size=grp['Reputability_Adj'] / 5 + 8,
                color=band_colors.get(band, "#9ca3af"),
                opacity=0.7,
                line=dict(width=1, color='rgba(255,255,255,0.1)'),
            ),
            name=band,
            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "Reliability: %{x:.1f}<br>"
                "Relevance: %{y:.1f}<br>"
                "<extra></extra>"
            ),
            customdata=grp['UserID'],
        ))
 
    # Highlight current
    fig.add_trace(go.Scatter(
        x=[current_row['Reliability_Adj']],
        y=[current_row['Relevance']],
        mode='markers+text',
        marker=dict(size=22, color='#fff', symbol='star', line=dict(width=2, color='#e8c84a')),
        text=[current_row['UserID']],
        textposition='top center',
        textfont=dict(size=10, color='#e8c84a', family='DM Mono'),
        name='Selected',
        hovertemplate="<b>%{text}</b><br>Reliability: %{x:.1f}<br>Relevance: %{y:.1f}<extra></extra>",
    ))
 
    # Quadrant lines
    fig.add_hline(y=60, line=dict(color='rgba(255,255,255,0.06)', dash='dot', width=1))
    fig.add_vline(x=60, line=dict(color='rgba(255,255,255,0.06)', dash='dot', width=1))
 
    # Quadrant labels
    for txt, x, y in [
        ("Fragile Starter", 75, 85), ("Efficient Machine", 85, 35),
        ("Double Risk", 20, 20), ("Legacy Builder", 75, 75),
    ]:
        fig.add_annotation(
            x=x, y=y, text=txt,
            showarrow=False,
            font=dict(size=8, color='rgba(255,255,255,0.15)', family='DM Mono'),
        )
 
    fig.update_layout(
        **PLOTLY_THEME,
        height=420,
        xaxis=dict(title='Reliability (Adjusted)', gridcolor='#1e2430', zeroline=False, range=[0, 110]),
        yaxis=dict(title='Relevance', gridcolor='#1e2430', zeroline=False, range=[0, 110]),
        legend=dict(font=dict(size=10), bgcolor='rgba(0,0,0,0)', bordercolor='#1e2430', borderwidth=1),
        title=dict(text="Competitive Landscape — Reliability vs Relevance (bubble = Reputation)", font=dict(size=12)),
    )
    return fig
 
 
def distribution_chart(results, metric='Growth_Index'):
    fig = go.Figure()
    colors = [score_to_color(v) for v in results[metric]]
    fig.add_trace(go.Bar(
        x=results['UserID'],
        y=results[metric],
        marker=dict(
            color=colors,
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=280,
        xaxis=dict(gridcolor='#1e2430', tickangle=-45, tickfont=dict(size=8)),
        yaxis=dict(range=[0, 100], gridcolor='#1e2430', zeroline=False),
        bargap=0.25,
        title=dict(text="Growth Index Distribution — All Schools", font=dict(size=12)),
    )
    return fig
 
 
# ─────────────────────────────────────────────
#  HTML COMPONENTS
# ─────────────────────────────────────────────
def kpi_card(label, value, card_cls, val_cls):
    band_label, band_css = get_band(value)
    return f"""
    <div class="kpi-card {card_cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {val_cls}">{value:.0f}</div>
        <span class="kpi-band {band_css}">{band_label}</span>
    </div>
    """
 
 
def section_header(num, title):
    return f"""
    <div class="section-header">
        <span class="section-number">{num}</span>
        <span class="section-title">{title}</span>
    </div>
    """
 
 
def stage_bar_html(row):
    stages = [
        ("Foundation Pressure",   row['Foundation'],   5, "#c2a24c"),
        ("Growth Stability",      row['Growth'],       5, "#3a8fb5"),
        ("Acceleration Readiness",row['Acceleration'], 5, "#9b5fcf"),
        ("Legacy Strength",       row['Legacy'],       5, "#2e9c6e"),
    ]
    bars = ""
    for label, val, max_val, color in stages:
        pct = (val / max_val) * 100
        bars += (
            f'<div class="stage-row">'
            f'<span class="stage-label">{label}</span>'
            f'<div class="stage-track">'
            f'<div class="stage-fill" style="width:{pct:.1f}%; background:{color};"></div>'
            f'</div>'
            f'<span class="stage-val">{val:.2f}</span>'
            f'</div>'
        )
    return f'<div class="stage-bar-wrap">{bars}</div>'
 
 
def alert_html(cls, title, body):
    return f"""
    <div class="alert-box alert-{cls}">
        <div class="alert-title">{title}</div>
        {body}
    </div>
    """
 
 
def question_grid_html(row):
    cells = ""
    for i in range(1, 21):
        score  = row[f'S{i}']
        color  = score_to_color(score)
        cells += (
            f'<div class="q-cell">'
            f'<div class="q-num">Q{i}</div>'
            f'<div class="q-score" style="color:{color};">{score:.0f}</div>'
            f'<div class="q-dot" style="background:{color};"></div>'
            f'</div>'
        )
    return f'<div class="q-grid">{cells}</div>'
 
 



def growth_stage_focus_html():
    return (
        '<div class="focus-wrap">'
        '<div class="focus-title">Growth Stages and Focus</div>'
        '<table class="focus-table">'
        '<thead>'
        '<tr>'
        '<th></th>'
        '<th>Management</th>'
        '<th>School Leader</th>'
        '<th>Faculty</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
        '<tr>'
        '<td class="focus-stage">Foundation</td>'
        '<td>Focus on capital investment, brand positioning, community outreach, and long-term vision.</td>'
        '<td>Establish operational systems (admissions, timetable, discipline, communication).</td>'
        '<td>Adapt to school culture, set academic benchmarks, and engage parents directly.</td>'
        '</tr>'
        '<tr>'
        '<td class="focus-stage">Growth</td>'
        '<td>Shift from firefighting to governance - set clear policies, delegate authority, monitor performance.</td>'
        '<td>Drive academic quality, teacher mentoring, and parent engagement.</td>'
        '<td>Deliver consistent results; adopt professional development and modern pedagogy.</td>'
        '</tr>'
        '<tr>'
        '<td class="focus-stage">Acceleration</td>'
        '<td>Provide strategic investments for innovation; build alliances (universities, corporates, international partners).</td>'
        '<td>Shift to transformational leadership - focusing on culture, innovation, teacher empowerment, and visibility.</td>'
        '<td>Move from "teaching" to "mentoring and innovating"; collaborate on curriculum enrichment, research, and competitions.</td>'
        '</tr>'
        '<tr>'
        '<td class="focus-stage">Consolidation</td>'
        '<td>Focus on sustainability, diversification, succession planning, and creating a legacy.</td>'
        '<td>Become ambassadors and thought leaders in education forums; groom next-line leaders.</td>'
        '<td>Engage in advanced professional development, research, publications, and innovation in pedagogy.</td>'
        '</tr>'
        '</tbody>'
        '</table>'
        '</div>'
    )


def render_pdf_download_widget(filename="individual_strategic_report.pdf"):
    components.html(
        f"""
        <div style="margin-top: 1rem;">
          <button id="download-pdf-btn" style="
              background:#ffffff;
              color:#1a1c20;
              border:1px solid #d9d9d9;
              border-radius:8px;
              padding:10px 14px;
              font-family:'DM Sans',sans-serif;
              font-size:14px;
              cursor:pointer;">
            Download Report as PDF
          </button>
          <div id="pdf-status" style="font-size:12px;color:#666;margin-top:8px;"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
        <script>
          const btn = document.getElementById("download-pdf-btn");
          const statusEl = document.getElementById("pdf-status");
          btn.onclick = async () => {{
            try {{
              statusEl.textContent = "Preparing PDF...";
              const {{ jsPDF }} = window.jspdf;
              const parentDoc = window.parent.document;
              const target = parentDoc.querySelector('[data-testid="stAppViewContainer"]');
              const canvas = await html2canvas(target, {{
                scale: 2,
                useCORS: true,
                backgroundColor: "#ffffff",
                windowWidth: parentDoc.documentElement.scrollWidth,
                windowHeight: parentDoc.documentElement.scrollHeight
              }});

              const imgData = canvas.toDataURL("image/png");
              const pdf = new jsPDF("p", "mm", "a4");
              const pdfWidth = pdf.internal.pageSize.getWidth();
              const pdfHeight = pdf.internal.pageSize.getHeight();
              const imgWidth = pdfWidth;
              const imgHeight = (canvas.height * imgWidth) / canvas.width;

              let heightLeft = imgHeight;
              let position = 0;

              pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
              heightLeft -= pdfHeight;

              while (heightLeft > 0) {{
                position = heightLeft - imgHeight;
                pdf.addPage();
                pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
                heightLeft -= pdfHeight;
              }}

              pdf.save("{filename}");
              statusEl.textContent = "PDF downloaded.";
            }} catch (e) {{
              statusEl.textContent = "Could not generate PDF. Try browser Print (Ctrl/Cmd+P) -> Save as PDF.";
              console.error(e);
            }}
          }};
        </script>
        """,
        height=95,
    )


def question_stage_tag(q_idx):
    if q_idx <= 5:
        return "Foundation"
    if q_idx <= 10:
        return "Growth"
    if q_idx <= 15:
        return "Acceleration"
    return "Consolidation"


def question_sentiment_text(row, q_idx):
    score = row[f'S{q_idx}']
    stage = question_stage_tag(q_idx)

    if score < 40:
        sentiment = "This response signals clear concern."
        implication = (
            f"For the {stage} stage, current sentiment suggests friction, hesitation, or low confidence. "
            "This is an immediate priority area for support and coaching."
        )
    elif score < 60:
        sentiment = "This response shows early but unstable progress."
        implication = (
            f"In the {stage} stage, sentiment is mixed: there is intent, but consistency is still developing. "
            "Focused follow-through can quickly improve this area."
        )
    elif score < 75:
        sentiment = "This response is directionally positive."
        implication = (
            f"For {stage}, the sentiment indicates workable strength with room to mature. "
            "Refining practices and consistency will move this into a strong zone."
        )
    elif score < 90:
        sentiment = "This response reflects strong confidence and healthy practice."
        implication = (
            f"In the {stage} stage, sentiment is stable and performance-oriented. "
            "This can be leveraged as a model for weaker question areas."
        )
    else:
        sentiment = "This response reflects benchmark-level confidence."
        implication = (
            f"For {stage}, sentiment indicates highly mature behavior and clear alignment. "
            "This is a strength to protect and replicate."
        )

    return (
        f"Q{q_idx} ({stage})\n\n"
        f"Score sentiment: {sentiment}\n\n"
        f"What this means: {implication}"
    )
 
 
# ─────────────────────────────────────────────
#  PRIORITY ENGINE
# ─────────────────────────────────────────────
def get_action_alerts(row):
    alerts = []
    gi    = row['Growth_Index']
    rel   = row['Relevance']
    reli  = row['Reliability_Adj']
    repu  = row['Reputability_Adj']
    fdn   = row['Foundation']
    grw   = row['Growth']
    acc   = row['Acceleration']
    leg   = row['Legacy']
 
    # Friction detection
    if fdn > grw:
        alerts.append(("warning",
            "⚠ Friction Detected",
            "Foundation Pressure exceeds Growth Stability. The school is 'running to stand still.' "
            "Stabilise basic SOPs before investing in growth initiatives."))
 
    # Stage skipping
    if acc > grw and grw < 3:
        alerts.append(("warning",
            "⚡ Stage Skip Risk",
            "Acceleration Readiness appears higher than Growth Stability. "
            "Innovation without operational maturity creates fragility. Build systems first."))
 
    # Priority 1 (lowest R)
    mins = {"Relevance": rel, "Reliability": reli, "Reputability": repu}
    lowest_k = min(mins, key=mins.get)
    lowest_v = mins[lowest_k]
    prescriptions = {
        "Relevance":    "Focus on curriculum innovation, competitive differentiation, and future-facing positioning.",
        "Reliability":  "Invest in operational systems, leadership depth, academic consistency, and parent processes.",
        "Reputability": "Activate alumni engagement, third-party recognition, and brand authority programmes.",
    }
    alerts.append(("critical",
        f"🎯 Priority 1 — {lowest_k} ({lowest_v:.0f})",
        prescriptions[lowest_k]))
 
    # Strength callout
    highest_k = max(mins, key=mins.get)
    alerts.append(("success",
        f"✅ Leverage Strength — {highest_k}",
        f"Your {highest_k.lower()} score is your strongest pillar ({mins[highest_k]:.0f}). "
        "Build strategic initiatives that amplify this advantage."))
 
    # Legacy gap
    if leg > grw + 0.8:
        alerts.append(("info",
            "📜 Legacy Disconnect",
            "Legacy aspirations significantly outpace operational Growth Stability. "
            "External reputation is hard to sustain without mature internal systems."))
 
    return alerts
 
 
# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem 0;'>
        <div style='font-family: Playfair Display, serif; font-size: 1.5rem; font-weight: 900; color: #e8e4dc; line-height: 1.1;'>
            R-Cube<br>Strategic Intelligence
        </div>
        <div style='font-family: DM Mono, monospace; font-size: 0.6rem; letter-spacing: 0.2em; color: #4a5568; text-transform: uppercase; margin-top: 0.4rem;'>
            Screening Metric v2
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    uploaded_file = st.file_uploader("Upload Response CSV", type=["csv"])
 
    st.markdown("---")
    st.markdown("""
    <div style='font-family: DM Mono, monospace; font-size: 0.6rem; color: #4a5568; letter-spacing: 0.1em; text-transform: uppercase;'>
    Scoring Model
    </div>
    <div style='font-size: 0.78rem; color: #7a8399; margin-top: 0.5rem; line-height: 1.6;'>
    <b style='color:#e8c84a;'>Relevance</b> — Q1,2,5,11,13,14<br>
    <b style='color:#4ab8e8;'>Reliability</b> — Q3,4,6-10,12,14,15<br>
    <b style='color:#b87ae0;'>Reputability</b> — Q16–20<br><br>
    GI = 0.35·R + 0.40·Rel + 0.25·Rep
    </div>
    """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if not uploaded_file:
    # Landing state
    st.markdown("""
    <div style='
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 70vh; text-align: center; padding: 2rem;
    '>
        <div style='font-family: Playfair Display, serif; font-size: 3.5rem; font-weight: 900; color: #e8e4dc; line-height: 1.1; max-width: 700px;'>
            R-Cube Strategic<br>Command Centre
        </div>
        <div style='font-family: DM Sans, sans-serif; font-size: 1rem; color: #7a8399; margin-top: 1rem; max-width: 480px; line-height: 1.7;'>
            Upload your response CSV to generate per-school strategic profiles,
            maturity-adjusted R-scores, stage diagnostics, and competitive benchmarking.
        </div>
        <div style='
            margin-top: 2.5rem;
            font-family: DM Mono, monospace; font-size: 0.7rem;
            letter-spacing: 0.2em; text-transform: uppercase;
            color: #4a5568; border: 1px solid #1e2430;
            padding: 0.75rem 1.5rem; border-radius: 8px;
        '>
            ← Upload CSV in sidebar to begin
        </div>
    </div>
    """, unsafe_allow_html=True)
 
else:
    # 1. ── DATA LOADING & PROCESSING ──
    # Ye part zaroori hai taaki 'results' aur 'row' variables create hon
    raw = pd.read_csv(uploaded_file)
    q_cols = raw.columns[8:28]
    raw = raw.rename(columns={q_cols[i]: f'Q{i+1}' for i in range(len(q_cols))})
    raw.insert(0, 'UserID', [f"User {i+1}" for i in range(len(raw))])
    
    # Response mapping
    for i in range(1, 21):
        raw[f'Q{i}'] = raw[f'Q{i}'].map(RESPONSE_MAP).fillna(3)
 
    results = calculate_metrics(raw)
 
    # 2. ── SIDEBAR SELECTION ──
    with st.sidebar:
        st.markdown("---")
        user_choice = st.selectbox("Select User Report", results['UserID'].tolist())
        
        # Stats for sidebar
        avg_gi = results['Growth_Index'].mean()
        rank = int(results['Growth_Index'].rank(ascending=False)[results['UserID'] == user_choice].values[0])
        
        st.markdown(f"""
        <div style='margin-top: 1rem; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;'>
            <div style='font-family: DM Mono; font-size: 0.6rem; color: #4a5568; text-transform: uppercase;'>Cohort Avg GI</div>
            <div style='font-family: Playfair Display; font-size: 1.6rem; font-weight: 900; color: #e8e4dc;'>{avg_gi:.1f}</div>
            <div style='margin-top: 10px; font-family: DM Mono; font-size: 0.6rem; color: #4a5568; text-transform: uppercase;'>Current Rank</div>
            <div style='font-family: Playfair Display; font-size: 1.6rem; font-weight: 900; color: #e8c84a;'>#{rank} / {len(results)}</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. ── GET SPECIFIC USER DATA ──
    row = results[results['UserID'] == user_choice].iloc[0]
    label, badge_cls, desc = get_strategic_profile(row)

    # 4. ── HEADER & TOP METRICS (Grid Layout) ──
    st.markdown("""
    <style>
        .report-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: #e8e4dc; line-height: 1; margin: 0; }
        .metric-subtitle { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #718096; letter-spacing: 0.2em; text-transform: uppercase; }
        .badge-container { display: flex; align-items: center; gap: 12px; margin: 15px 0 25px 0; }
        .status-badge { padding: 4px 12px; border-radius: 4px; font-family: 'DM Mono'; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

    col_header, col_curve = st.columns([1.3, 1])

    with col_header:
        st.markdown('<p class="metric-subtitle">Individual Strategic Report</p>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="report-title">{user_choice}</h1>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="badge-container">
                <span class="status-badge {badge_cls}">{label}</span>
                <span style="color: #a0aec0; font-size: 0.85rem; font-style: italic;">{desc}</span>
            </div>
        """, unsafe_allow_html=True)

        # KPI Metrics Row
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(kpi_card("Growth Index", row['Growth_Index'], "growth", "growth"), unsafe_allow_html=True)
        k2.markdown(kpi_card("Relevance", row['Relevance'], "relevance", "relevance"), unsafe_allow_html=True)
        k3.markdown(kpi_card("Reliability", row['Reliability_Adj'], "reliability", "reliability"), unsafe_allow_html=True)
        k4.markdown(kpi_card("Reputation", row['Reputability_Adj'], "reputability", "reputability"), unsafe_allow_html=True)

    with col_curve:
        st.plotly_chart(growth_curve_chart(row['Growth_Index']), use_container_width=True)

    st.divider()

    # 5. ── SECTION 01: MATURITY GAUGES ──
    st.markdown(section_header("01", "R-Cube Maturity Gauges"), unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(gauge_chart(row['Relevance'], "RELEVANCE", "#e8c84a"), use_container_width=True)
    with g2: st.plotly_chart(gauge_chart(row['Reliability_Adj'], "RELIABILITY (ADJ)", "#4ab8e8"), use_container_width=True)
    with g3: st.plotly_chart(gauge_chart(row['Reputability_Adj'], "REPUTABILITY (ADJ)", "#b87ae0"), use_container_width=True)

    # 6. ── SECTION 02: CALCULATION LOGIC (Boxes) ──
    st.markdown(section_header("02", "Strategic Focus Logic"), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; gap: 20px; align-items: stretch; margin-top: 10px;">
        <div style="flex: 1; padding: 20px; background: rgba(232, 200, 74, 0.05); border-top: 3px solid #e8c84a; border-radius: 4px;">
            <p style="font-family: 'DM Mono'; font-size: 0.75rem; color: #e8c84a; font-weight: bold;">RELEVANCE</p>
            <p style="font-size: 0.75rem; color: #cbd5e0; line-height: 1.5;">Curriculum alignment, unique value proposition, and parent/student need fulfillment.</p>
        </div>
        <div style="flex: 1; padding: 20px; background: rgba(74, 184, 232, 0.05); border-top: 3px solid #4ab8e8; border-radius: 4px;">
            <p style="font-family: 'DM Mono'; font-size: 0.75rem; color: #4ab8e8; font-weight: bold;">RELIABILITY</p>
            <p style="font-size: 0.75rem; color: #cbd5e0; line-height: 1.5;">Operational consistency, SOP stability, and scalable middle leadership systems.</p>
        </div>
        <div style="flex: 1; padding: 20px; background: rgba(184, 122, 224, 0.05); border-top: 3px solid #b87ae0; border-radius: 4px;">
            <p style="font-family: 'DM Mono'; font-size: 0.75rem; color: #b87ae0; font-weight: bold;">REPUTABILITY</p>
            <p style="font-size: 0.75rem; color: #cbd5e0; line-height: 1.5;">Brand authority, alumni engagement, and national benchmark recognition.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7. ── SECTION 03: STAGE PROFILE ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("03", "Growth Stage Profile"), unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown(stage_bar_html(row), unsafe_allow_html=True)
    with col_b:
        st.plotly_chart(radar_chart(row), use_container_width=True)

    # 8. ── DOWNLOAD BUTTON & FOOTER ──
    st.markdown("<br>", unsafe_allow_html=True)
    render_pdf_download_widget(filename=f"RCube_Report_{user_choice.replace(' ', '_')}.pdf")
    
    st.markdown(f"""
    <div style='margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #1e2430; text-align: center;'>
        <p style='font-family: DM Mono; font-size: 0.6rem; color: #4a5568; letter-spacing: 0.15em; text-transform: uppercase;'>
            R-Cube Strategic Intelligence · Screening Tool · {pd.Timestamp.now().strftime('%d %b %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)