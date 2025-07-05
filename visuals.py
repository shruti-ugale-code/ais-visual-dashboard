import streamlit as st
import pandas as pd
import time
import random
import plotly.express as px

# Title
st.title("🚢 AIS Real-Time Dashboard")
st.caption("Refreshing every 3 seconds to simulate real-time updates.")

# Load data
def load_data():
    df = pd.read_csv("ais_data_sample_with_trajectories.csv")
    df['sog'] = pd.to_numeric(df['sog'], errors='coerce')
    df['heading'] = pd.to_numeric(df['heading'], errors='coerce')
    df['width'] = pd.to_numeric(df['width'], errors='coerce')
    df['length'] = pd.to_numeric(df['length'], errors='coerce')
    
    required_columns = ['sog', 'heading', 'width', 'length']
    optional_geo = ['LAT', 'LON']
    available_geo = [col for col in optional_geo if col in df.columns]
    df = df.dropna(subset=required_columns + available_geo)

    return df

# Load and prepare data
df = load_data()
subset = df.sample(20)

# Layout: SOG and Heading
col1, col2 = st.columns(2)
with col1:
    st.subheader("Speed Over Ground (SOG)")
    st.line_chart(subset['sog'])

with col2:
    st.subheader("Heading Distribution")
    st.bar_chart(subset['heading'])

# Ship Type Count
st.subheader("🚢 Ship Type Count")
if 'shiptype' in subset.columns:
    st.bar_chart(subset['shiptype'].value_counts())
else:
    st.warning("Column 'shiptype' not found in dataset.")

# Vessel Trajectory Plot (if data is available)
st.subheader("🗺️ Vessel Trajectories (Top 5)")
if all(col in df.columns for col in ['LAT', 'LON', 'VesselName']):
    top_vessels = df['VesselName'].value_counts().head(5).index
    df_traj = df[df['VesselName'].isin(top_vessels)]

    fig = px.line_mapbox(
        df_traj,
        lat='LAT',
        lon='LON',
        color='VesselName',
        line_group='VesselName',
        hover_name='VesselName',
        zoom=3,
        height=500
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig)
else:
    st.warning("LAT/LON/VesselName columns not found – skipping trajectory map.")

# Data table
st.subheader("📊 Latest Sample Data")
st.dataframe(subset)

# Auto-refresh every 3 seconds
time.sleep(3)
st.rerun()
