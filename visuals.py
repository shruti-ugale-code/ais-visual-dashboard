import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Live Vessel Tracker", layout="wide")
st.title("🗺️ Interactive Vessel Trajectories (Clean Paths)")

# Load & preprocess
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")

    # Drop missing data
    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Sort to preserve trajectory lines
    df = df.sort_values(by=['VesselName', 'timestamp'])

    return df

df = load_data()

# Let user select vessels
vessels = df['VesselName'].unique()
selected_vessels = st.multiselect("Select vessels to display:", vessels, default=vessels[:5])

# Filter for selected vessels
if not selected_vessels:
    st.warning("Please select at least one vessel.")
    st.stop()

filtered = df[df['VesselName'].isin(selected_vessels)]

# Draw trajectory using scatter_mapbox with line_group
fig = px.scatter_mapbox(
    filtered,
    lat="LAT",
    lon="LON",
    color="VesselName",
    hover_name="VesselName",
    hover_data={"timestamp": True, "LAT": False, "LON": False},
    line_group="VesselName",
    zoom=6,
    height=650
)

# Make line paths visible
fig.update_traces(mode="lines+markers")

# Improve layout
fig.update_layout(mapbox_style="carto-positron", margin={"r":0, "t":0, "l":0, "b":0})

# Show chart
st.plotly_chart(fig, use_container_width=True)

# Optional: refresh every 5 seconds
st.caption("Dashboard auto-refreshes every 5 seconds.")
st.experimental_rerun()
