import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Edxso Full Dashboard", layout="wide")

# Mapping strings to numeric values
RESPONSE_MAP = {
    "Completely disagree": 1,
    "Disagree": 2,
    "Don’t Know, Can’t Say": 3,
    "don't know ,can't say": 3,
    "Agree": 4,
    "Completely agree": 5,
    "Completely Agree": 5
}

def calculate_metrics(df):
    """Calculates all R-Cube scores and Stage Profile Averages."""
    # 1. Individual Scoring (0-100)
    for i in range(1, 6): df[f'S{i}'] = (5 - df[f'Q{i}']) * 25
    for i in range(6, 21): df[f'S{i}'] = (df[f'Q{i}'] - 1) * 25

    # 2. R-Scores
    df['Relevance'] = df[['S1', 'S2', 'S5', 'S11', 'S13', 'S14']].mean(axis=1)
    df['Rel_Raw'] = df[['S3', 'S4', 'S6', 'S7', 'S8', 'S9', 'S10', 'S12', 'S14', 'S15']].mean(axis=1)
    df['Rep_Raw'] = df[['S16', 'S17', 'S18', 'S19', 'S20']].mean(axis=1)

    # 3. Maturity Adjustments
    df['Reliability_Adj'] = df['Rel_Raw'] * (0.75 + 0.25 * df['Relevance'] / 100)
    min_found = df[['Relevance', 'Reliability_Adj']].min(axis=1)
    df['Reputability_Adj'] = df['Rep_Raw'] * (0.60 + 0.40 * min_found / 100)

    # 4. Stage Profile Averages
    df['Foundation Pressure'] = df[[f'Q{i}' for i in range(1, 6)]].mean(axis=1)
    df['Growth Stability'] = df[[f'Q{i}' for i in range(6, 11)]].mean(axis=1)
    df['Acceleration Readiness'] = df[[f'Q{i}' for i in range(11, 16)]].mean(axis=1)
    df['Legacy Strength'] = df[[f'Q{i}' for i in range(16, 21)]].mean(axis=1)

    # 5. Overall Growth Index
    df['Growth_Index'] = (0.35 * df['Relevance'] + 0.40 * df['Reliability_Adj'] + 0.25 * df['Reputability_Adj'])
    return df

def draw_ring(value, color):
    """Maturity Rings chart."""
    fig = go.Figure(go.Pie(
        values=[value, 100 - value],
        hole=.7,
        marker_colors=[color, "#f0f2f6"],
        textinfo='none',
        sort=False
    ))
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=180,
                      annotations=[dict(text=f"{int(value)}", x=0.5, y=0.5, font_size=20, showarrow=False)])
    return fig

def get_stage_label(score):
    if score < 40: return "FOUNDATION"
    if score < 60: return "GROWTH"
    if score < 80: return "ACCELERATION"
    return "CONSOLIDATION"

def draw_index_pie(value):
    """Overall Index Pie with Stage Label in middle."""
    stage = get_stage_label(value)
    fig = go.Figure(go.Pie(
        values=[value, 100-value],
        hole=.75,
        marker_colors=["#1c3d5a", "#f0f2f6"],
        textinfo='none',
        sort=False
    ))
    fig.update_layout(
        showlegend=False,
        height=350,
        annotations=[dict(text=f"<b>{stage}</b><br>{int(value)}%", x=0.5, y=0.5, font_size=22, showarrow=False)]
    )
    return fig

# --- UI ---
st.title("🏫 Edxso Evolution Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    q_cols = data.columns[8:28]
    data = data.rename(columns={q_cols[i]: f'Q{i+1}' for i in range(len(q_cols))})
    data.insert(0, 'UserID', [f"User {i+1}" for i in range(len(data))])

    for i in range(1, 21):
        data[f'Q{i}'] = data[f'Q{i}'].map(RESPONSE_MAP).fillna(3)

    results = calculate_metrics(data)
    user_choice = st.sidebar.selectbox("Select User Report", results['UserID'])
    row = results[results['UserID'] == user_choice].iloc[0]

    # --- SECTION 1: R-CUBE RINGS ---
    st.header("1. R-Cube Balanced Maturity (%)")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("<center><b>RELEVANCE</b></center>", unsafe_allow_html=True)
        st.plotly_chart(draw_ring(row['Relevance'], "#1c3d5a"), use_container_width=True)
    with r2:
        st.markdown("<center><b>RELIABILITY</b></center>", unsafe_allow_html=True)
        st.plotly_chart(draw_ring(row['Reliability_Adj'], "#2a9d8f"), use_container_width=True)
    with r3:
        st.markdown("<center><b>REPUTABILITY</b></center>", unsafe_allow_html=True)
        st.plotly_chart(draw_ring(row['Reputability_Adj'], "#e76f51"), use_container_width=True)

    st.divider()

    # --- SECTION 2: BAR CHART ---
    st.header("2. Stage Profile Averages (1-5)")
    stages_data = {'Foundation': row['Foundation Pressure'], 'Growth': row['Growth Stability'],
                   'Acceleration': row['Acceleration Readiness'], 'Legacy': row['Legacy Strength']}
    fig_bar = px.bar(x=list(stages_data.keys()), y=list(stages_data.values()), color=list(stages_data.keys()),
                     range_y=[0, 5], labels={'x': 'Phase', 'y': 'Rating'})
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- SECTION 3: NEW GROWTH INDEX PIE ---
    st.header("3. Overall Growth Index & Stage")
    st.plotly_chart(draw_index_pie(row['Growth_Index']), use_container_width=True)

else:
    st.info("CSV upload karo bhai.")