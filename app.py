"""
================================================================================
INTERACTIVE HR ANALYTICS & ATTRITION DASHBOARD (STREAMLIT APP)
================================================================================
Run locally with: streamlit run app.py
================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="HR Attrition Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("HR Data.csv")
    df.columns = [c.strip() for c in df.columns]
    df['Attrition_Value'] = df['Attrition'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)
    return df

df = load_data()

# Header
st.title("📊 HR Analytics & Employee Attrition Intelligence")
st.markdown("**Enterprise Workforce Insights, Demographic Breakdown & Risk Scoring**")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filter Analytics")
dept_filter = st.sidebar.multiselect(
    "Select Department",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)

ot_filter = st.sidebar.multiselect(
    "Overtime Status",
    options=df['Over Time'].unique(),
    default=df['Over Time'].unique()
)

filtered_df = df[
    (df['Department'].isin(dept_filter)) &
    (df['Over Time'].isin(ot_filter))
]

# Key Performance Indicators
col1, col2, col3, col4 = st.columns(4)
total_emp = len(filtered_df)
total_att = filtered_df['Attrition_Value'].sum()
att_rate = (total_att / total_emp * 100) if total_emp > 0 else 0
avg_inc = filtered_df['Monthly Income'].mean() if total_emp > 0 else 0

col1.metric("Total Headcount", f"{total_emp:,}")
col2.metric("Total Attrition", f"{total_att:,}")
col3.metric("Attrition Rate", f"{att_rate:.1f}%")
col4.metric("Avg Monthly Income", f"${avg_inc:,.0f}")

st.markdown("---")

# Visualizations Row 1
r1_col1, r1_col2 = st.columns(2)

with r1_col1:
    st.subheader("Overtime Impact on Attrition")
    ot_df = filtered_df.groupby('Over Time')['Attrition_Value'].agg(['count', 'sum']).reset_index()
    ot_df['Rate'] = (ot_df['sum'] / ot_df['count']) * 100
    fig_ot = px.bar(
        ot_df, 
        x='Over Time', 
        y='Rate', 
        color='Over Time',
        text_auto='.1f',
        labels={'Rate': 'Attrition Rate (%)'},
        color_discrete_map={'Yes': '#ef553b', 'No': '#636efa'}
    )
    st.plotly_chart(fig_ot, use_container_width=True)

with r1_col2:
    st.subheader("Departmental Attrition Breakdown")
    dept_df = filtered_df.groupby('Department')['Attrition_Value'].agg(['count', 'sum']).reset_index()
    dept_df['Rate'] = (dept_df['sum'] / dept_df['count']) * 100
    fig_dept = px.bar(
        dept_df, 
        x='Department', 
        y='Rate', 
        color='Department',
        text_auto='.1f',
        labels={'Rate': 'Attrition Rate (%)'}
    )
    st.plotly_chart(fig_dept, use_container_width=True)

# Visualizations Row 2
r2_col1, r2_col2 = st.columns(2)

with r2_col1:
    st.subheader("Job Satisfaction vs Monthly Income")
    fig_scatter = px.scatter(
        filtered_df,
        x='Monthly Income',
        y='Job Satisfaction',
        color='Attrition',
        hover_data=['Job Role', 'Age'],
        color_discrete_map={'Yes': '#ef553b', 'No': '#00cc96'},
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with r2_col2:
    st.subheader("Years at Company Distribution")
    fig_box = px.box(
        filtered_df,
        x='Attrition',
        y='Years At Company',
        color='Attrition',
        color_discrete_map={'Yes': '#ef553b', 'No': '#00cc96'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.caption("Powered by Streamlit | HR Analytics Intelligence Dashboard")
