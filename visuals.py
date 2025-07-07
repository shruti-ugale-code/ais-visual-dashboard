import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("🛰️ Live Ship Trajectories (Auto-Refreshing Every 5s)")

# Auto-refresh every 5 seconds
st.caption("This dashboard refreshes every 5 seconds to simulate live updates.")
time.sleep(5)
st.rerun()

# Load your dataset (update this path if needed)
df = pd.read_csv("ais_singapore_strait_animated.csv")

# Make sure coordinates and timestamp are usable
df = df.dropna(subset=["VesselName", "LAT", "LON", "timestamp"])
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
df = df.dropna(subset=["LAT", "LON"])
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.sort_values(by=["VesselName", "timestamp"])

# Vessel selection
vessel_names = df["VesselName"].unique().tolist()
selected_vessels = st.multiselect("Select ships to show trajectory:", vessel_names, default=vessel_names[:3])

# Filter for selected vessels
filtered_df = df[df["VesselName"].isin(selected_vessels)]

# Plot trajectory lines for each ship
fig = go.Figure()

for vessel in selected_vessels:
    ship_df = filtered_df[filtered_df["VesselName"] == vessel]
    fig.add_trace(go.Scattermapbox(
        lat=ship_df["LAT"],
        lon=ship_df["LON"],
        mode='lines+markers',
        name=vessel,
        line=dict(width=2),
        marker=dict(size=5),
        hoverinfo='text',
        text=ship_df["timestamp"].astype(str)
    ))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": filtered_df["LAT"].mean(), "lon": filtered_df["LON"].mean()},
    height=600,
    margin={"r":0, "t":0, "l":0, "b":0},
    legend_title="VesselName"
)

st.plotly_chart(fig, use_container_width=True)

# Optional: show latest raw data
with st.expander("Show Latest Data Sample"):
    st.dataframe(filtered_df.tail(20))
