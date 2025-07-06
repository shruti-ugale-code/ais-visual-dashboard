import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Clean AIS Trajectories", layout="wide")
st.title("🧭 Clean Vessel Trajectories (Top 5 Ships)")
st.caption("Auto-refreshing every 5 seconds.")

# Load and clean data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")

    # Clean column types
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Drop missing or invalid values
    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['VesselName', 'timestamp', 'LAT', 'LON'])

    # Sort by timestamp for proper trajectory
    df = df.sort_values(by=['VesselName', 'timestamp'])

    return df

df = load_data()

# Get top 5 vessels by number of data points
top_vessels = df['VesselName'].value_counts().nlargest(5).index.tolist()
df_top = df[df['VesselName'].isin(top_vessels)]

# Plot clean trajectories
fig = px.line_mapbox(
    df_top,
    lat="LAT",
    lon="LON",
    color="VesselName",
    line_group="VesselName",   # ← very important
    hover_name="VesselName",
    hover_data={"timestamp": True},
    zoom=5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0}
)

st.plotly_chart(fig, use_container_width=True)

# Show a clean live data snapshot
st.subheader("📊 Live Sample (Top Vessels Only)")
st.dataframe(df_top.sample(10))

# Refresh every 5 seconds
time.sleep(5)
st.rerun()
