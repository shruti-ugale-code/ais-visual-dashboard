import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import os

st.set_page_config(layout="wide")
st.title("🛰️ Vessel Trajectories (Live Auto-Refreshing)")

# Auto-refresh every 5 seconds
st.caption("This dashboard auto-refreshes every 5 seconds to simulate live ship tracking.")
time.sleep(5)
st.rerun()

# Load CSV
file_path = "ais_singapore_strait_animated.csv"
if not os.path.exists(file_path):
    st.error(f"CSV file not found at: {file_path}")
    st.stop()

# Read dataset
df = pd.read_csv(file_path)

# Clean columns
df = df.dropna(subset=["VesselName", "LAT", "LON", "timestamp"])
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["LAT", "LON", "timestamp"])
df = df.sort_values(by=["VesselName", "timestamp"])

# Vessel selector
vessels = df["VesselName"].unique().tolist()
selected = st.multiselect("Select ships to show on map:", vessels, default=vessels[:3])

# Filter data
df_selected = df[df["VesselName"].isin(selected)]

if df_selected.empty:
    st.warning("No data found for selected vessels.")
    st.stop()

# Create the trajectory lines
fig = go.Figure()

for vessel in selected:
    vessel_df = df_selected[df_selected["VesselName"] == vessel]
    fig.add_trace(go.Scattermapbox(
        lat=vessel_df["LAT"],
        lon=vessel_df["LON"],
        mode='lines+markers',
        name=vessel,
        line=dict(width=2),
        marker=dict(size=6),
        text=vessel_df["timestamp"].astype(str),
        hoverinfo="text+name"
    ))

# Map layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": df_selected["LAT"].mean(), "lon": df_selected["LON"].mean()},
    height=650,
    margin={"r":0, "t":0, "l":0, "b":0}
)

# Show map
st.plotly_chart(fig, use_container_width=True)

# Show recent rows
with st.expander("📊 View Sample Data"):
    st.dataframe(df_selected.tail(10))
