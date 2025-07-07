import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🛳️ Ship Trajectories Map")

# Load the AIS data (Replace this with your file name)
df = pd.read_csv("ais_singapore_strait_animated.csv")

# Ensure data is clean
df = df.dropna(subset=["VesselName", "LAT", "LON", "timestamp"])
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
df = df.dropna(subset=["LAT", "LON"])
df = df.sort_values(by=["VesselName", "timestamp"])

# Allow user to select vessels
vessel_list = df["VesselName"].unique().tolist()
selected_vessels = st.multiselect("Select vessels to show trajectory:", vessel_list, default=vessel_list[:3])

# Filter data for selected vessels
filtered = df[df["VesselName"].isin(selected_vessels)]

# Create a trajectory map
fig = go.Figure()

for vessel in selected_vessels:
    vessel_df = filtered[filtered["VesselName"] == vessel]
    fig.add_trace(go.Scattermapbox(
        lat=vessel_df["LAT"],
        lon=vessel_df["LON"],
        mode='lines+markers',
        name=vessel,
        marker=dict(size=6),
        line=dict(width=2)
    ))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": filtered["LAT"].mean(), "lon": filtered["LON"].mean()},
    height=600,
    margin={"r":0, "t":0, "l":0, "b":0}
)

st.plotly_chart(fig)
