import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Page config
st.set_page_config(page_title="AIS Vessel Dashboard", layout="wide")

st.title("🗺️ Vessel Trajectories (Top 5)")
st.caption("Map updates every 5 seconds to simulate real-time tracking.")

# Load and preprocess data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")

    # Clean data types
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])
    return df

df = load_data()

# Filter top 5 vessel names by appearance
top_vessels = df['VesselName'].value_counts().head(5).index.tolist()
filtered_df = df[df['VesselName'].isin(top_vessels)]

# Plot trajectories
fig = px.line_mapbox(
    filtered_df.sort_values("timestamp"),
    lat="LAT",
    lon="LON",
    color="VesselName",
    line_group="VesselName",
    zoom=5,
    height=600,
    hover_data={"VesselName": True, "timestamp": True}
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(fig, use_container_width=True)

# Show live sample data
st.subheader("📊 Latest Sample Data")
st.dataframe(filtered_df.sample(10))

# Refresh every 5 seconds
time.sleep(5)
st.rerun()
