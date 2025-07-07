import streamlit as st
import pandas as pd
import time
import random
import plotly.express as px

# Title
st.title("🚢 AIS Real-Time Dashboard")
st.caption("Refreshing every 3 seconds to simulate real-time updates.")

# Load main dashboard data
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")
    df['sog'] = pd.to_numeric(df['sog'], errors='coerce')
    df['heading'] = pd.to_numeric(df['heading'], errors='coerce')
    df['width'] = pd.to_numeric(df['width'], errors='coerce')
    df['length'] = pd.to_numeric(df['length'], errors='coerce')
    required_columns = ['sog', 'heading', 'width', 'length']
    optional_geo = ['LAT', 'LON']
    available_geo = [col for col in optional_geo if col in df.columns]
    df = df.dropna(subset=required_columns + available_geo)
    return df

# Load animated data separately
def load_animated_data():
    return pd.read_csv("ais_animated_trajectory_sample.csv")

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

# 🌍 Animated Trajectory Map (Ships as points)
st.subheader("🛰️ Live-like Animated Vessel Trajectories")
animated_df = load_animated_data()

if all(col in animated_df.columns for col in ['LAT', 'LON', 'timestamp', 'VesselName']):
    fig = px.scatter_mapbox(
        animated_df,
        lat='LAT',
        lon='LON',
        color='VesselName',
        size='sog',
        hover_name='VesselName',
        animation_frame='timestamp',
        zoom=2,
        height=600
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig)
else:
    st.warning("Animated map data is missing required columns.")

# Data table
st.subheader("📊 Latest Sample Data")
st.dataframe(subset)

# Refresh every 3 seconds
time.sleep(3)
st.rerun()
