import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title
st.title("🌊 Interactive Vessel Trajectories (Clean Paths)")

# Load data
df = pd.read_csv("your_dataset.csv")

# Drop NaNs
df.dropna(subset=["LAT", "LON", "timestamp", "VesselName"], inplace=True)

# Sidebar for selection
vessels = df["VesselName"].unique().tolist()
selected_vessels = st.multiselect("Select vessels to display:", vessels, default=vessels[:3])

# Filter and sort
filtered = df[df["VesselName"].isin(selected_vessels)]
filtered = filtered.sort_values(by=["VesselName", "timestamp"])

# Plot setup
fig = go.Figure()

for vessel in selected_vessels:
    vessel_data = filtered[filtered["VesselName"] == vessel]
    fig.add_trace(go.Scattermapbox(
        lat=vessel_data["LAT"],
        lon=vessel_data["LON"],
        mode='lines+markers',
        name=vessel,
        marker=dict(size=6),
        line=dict(width=2)
    ))

# Layout settings
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=6,
        center=dict(lat=filtered["LAT"].mean(), lon=filtered["LON"].mean())
    ),
    height=600,
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(fig)
