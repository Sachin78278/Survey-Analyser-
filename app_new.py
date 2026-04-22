import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Edxso Strategic Command Center", layout="wide")

# Mapping
RESPONSE_MAP = {
    "Completely disagree": 1, "Disagree": 2, "Don’t Know, Can’t Say": 3,
    "don't know ,can't say": 3, "Agree": 4, "Completely agree": 5, "Completely Agree": 5
}

def calculate_metrics(df):
    # 0-100 Scoring
    for i in range(1, 6): df[f'S{i}'] = (5 - df[f'Q{i}']) * 25
    for i in range(6, 21): df[f'S{i}'] = (df[f'Q{i}'] - 1) * 25

    # R-Scores (Raw vs Adjusted)
    df['Relevance'] = df[['S1', 'S2', 'S5', 'S11', 'S13', 'S14']].mean(axis=1)
    df['Rel_Raw'] = df[['S3', 'S4', 'S6', 'S7', 'S8', 'S9', 'S10', 'S12', 'S14', 'S15']].mean(axis=1)
    df['Rep_Raw'] = df[['S16', 'S17', 'S18', 'S19', 'S20']].mean(axis=1)

    # Adjustments
    df['Reliability_Adj'] = df['Rel_Raw'] * (0.75 + 0.25 * df['Relevance'] / 100)
    min_found = df[['Relevance', 'Reliability_Adj']].min(axis=1)
    df['Reputability_Adj'] = df['Rep_Raw'] * (0.60 + 0.40 * min_found / 100)

    # Stage Profiles
    df['Foundation'] = df[[f'Q{i}' for i in range(1, 6)]].mean(axis=1)
    df['Growth'] = df[[f'Q{i}' for i in range(6, 11)]].mean(axis=1)
    df['Acceleration'] = df[[f'Q{i}' for i in range(11, 16)]].mean(axis=1)
    df['Legacy'] = df[[f'Q{i}' for i in range(16, 21)]].mean(axis=1)

    df['Growth_Index'] = (0.35 * df['Relevance'] + 0.40 * df['Reliability_Adj'] + 0.25 * df['Reputability_Adj'])
    return df

def get_strategic_label(row):
    score = row['Growth_Index']
    if score >= 85: return "🏆 BENCHMARK", "Success", "Market leader and legacy institution."
    if row['Relevance'] > 70 and row['Reliability_Adj'] < 50: return "⚡ FRAGILE STARTER", "Warning", "High potential but systems are failing."
    if row['Reliability_Adj'] > 70 and row['Relevance'] < 50: return "⚙️ EFFICIENT MACHINE", "Info", "Consistent but risks becoming obsolete."
    if row['Reliability_Adj'] > 60 and row['Reputability_Adj'] > 60: return "📜 LEGACY BUILDER", "Success", "Strong systems and building long-term impact."
    if score < 40: return "🛑 FRAGILE", "Error", "Immediate intervention required in foundations."
    return "🌱 EMERGING", "Info", "Moving out of survival phase."

# --- UI Layout ---
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    q_cols = data.columns[8:28]
    data = data.rename(columns={q_cols[i]: f'Q{i+1}' for i in range(len(q_cols))})
    data.insert(0, 'UserID', [f"User {i+1}" for i in range(len(data))])
    for i in range(1, 21): data[f'Q{i}'] = data[f'Q{i}'].map(RESPONSE_MAP).fillna(3)

    results = calculate_metrics(data)
    user_choice = st.sidebar.selectbox("Select Individual Report", results['UserID'])
    row = results[results['UserID'] == user_choice].iloc[0]

    # --- HEADER: STATUS BADGE & NORTH STAR ---
    label, status_type, desc = get_strategic_label(row)
    st.title(f"Strategic Command Center: {user_choice}")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric("Growth Index", f"{row['Growth_Index']:.1f}")
        getattr(st, status_type.lower())(f"**{label}**\n\n{desc}")
    
    with col_b:
        # 1. Overall Growth Gauge
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number", value=row['Growth_Index'],
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1c3d5a"},
                   'steps': [{'range': [0, 40], 'color': "red"}, {'range': [40, 75], 'color': "orange"}, {'range': [75, 100], 'color': "green"}]}))
        fig_g.update_layout(height=250, margin=dict(t=30, b=0))
        st.plotly_chart(fig_g, use_container_width=True)

    st.divider()

    # --- SECTION 2: THE TRIAD & RADAR ---
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("I. R-Cube Balanced Maturity")
        # Three mini gauges for Rel, Rel, Rep
        for m, val, color in [("Relevance", row['Relevance'], "#1c3d5a"), 
                             ("Reliability (Adj)", row['Reliability_Adj'], "#2a9d8f"), 
                             ("Reputability (Adj)", row['Reputability_Adj'], "#e76f51")]:
            st.write(f"**{m}: {int(val)}%**")
            st.progress(int(val)/100)
            
    with c2:
        st.subheader("II. Institutional Shape (Radar)")
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[row['Foundation'], row['Growth'], row['Acceleration'], row['Legacy']],
            theta=['Foundation', 'Growth', 'Acceleration', 'Legacy'], fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=300, margin=dict(t=30, b=30))
        st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()

    # --- SECTION 3: THE BRUTAL TRUTH (RAW vs ADJ) ---
    st.subheader("III. The 'Brutal Truth' Analysis")
    st.info("Showing how weak foundations 'drag down' higher-level perceptions.")
    
    brutal_data = pd.DataFrame({
        'Metric': ['Reliability', 'Reputability'],
        'Raw Score': [row['Rel_Raw'], row['Rep_Raw']],
        'Adjusted Score': [row['Reliability_Adj'], row['Reputability_Adj']]
    })
    fig_brutal = px.bar(brutal_data, x='Metric', y=['Raw Score', 'Adjusted Score'], barmode='group',
                        color_discrete_sequence=['#ced4da', '#1c3d5a'])
    st.plotly_chart(fig_brutal, use_container_width=True)

    # --- SECTION 4: ACTION ALERTS ---
    st.subheader("IV. Strategic Action Path")
    
    # Friction Detection
    if row['Foundation'] > row['Growth']:
        st.warning("⚠️ **FRICTION ALERT:** Foundation Pressure is higher than Growth Stability. The school is 'running to stand still.' Fix basic SOPs immediately.")
    
    # Gap Analysis
    low_m = min(row['Relevance'], row['Reliability_Adj'], row['Reputability_Adj'])
    if low_m == row['Relevance']:
        st.error("**PRIORITY 1: Relevance.** Focus on Curriculum Innovation & Competitive Positioning.")
    elif low_m == row['Reliability_Adj']:
        st.error("**PRIORITY 1: Reliability.** Focus on Operational Systems & Leadership Depth.")
    else:
        st.error("**PRIORITY 1: Reputability.** Focus on Alumni Engagement & Brand Authority.")

    # --- SECTION 5: BENCHMARKING (SCATTER) ---
    st.divider()
    st.subheader("V. Competitive Benchmarking (All Users)")
    fig_scatter = px.scatter(results, x='Reliability_Adj', y='Relevance', size='Reputability_Adj', 
                             hover_name='UserID', color='Growth_Index',
                             title="Reliability vs Relevance (Bubble Size = Reputation)")
    # Highlight current user
    fig_scatter.add_trace(go.Scatter(x=[row['Reliability_Adj']], y=[row['Relevance']], 
                                     mode='markers', marker=dict(size=25, color='red', symbol='star'), name='Current User'))
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("Upload the CSV to activate the Strategic Command Center.")