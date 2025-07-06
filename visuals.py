import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🌊 Interactive Vessel Trajectories (Connected Paths)")

# Load your actual dataset (replace with your actual file name)
df = pd.read_csv("ais_singapore_strait_animated.csv")

# Drop rows with missing coordinates or vessel name
df.dropna(subset=["LAT", "LON", "timestamp", "VesselName"], inplace=True)

# Convert LAT and LON to numeric if needed
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
df["LON"] = pd.to_numeric(df["LON"], errors="coerce")

# Drop any remaining NaNs
df.dropna(subset=["LAT", "LON"], inplace=True)

# Filter vessel selection
vessels = df["VesselName"].unique().tolist()
selected_vessels = st.multiselect("Select vessels to display:", vessels, default=vessels[:3])

# Filter and sort by timestamp
filtered = df[df["VesselName"].isin(selected_vessels)].sort_values(by=["VesselName", "timestamp"])

# Create figure
fig = go.Figure()

# Plot line for each vessel
for vessel in selected_vessels:
    vessel_data = filtered[filtered["VesselName"] == vessel]
    fig.add_trace(go.Scattermapbox(
        lat=vessel_data["LAT"],
        lon=vessel_data["LON"],
        mode="lines+markers",
        name=vessel,
        marker=dict(size=5),
        line=dict(width=2)
    ))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": filtered["LAT"].mean(), "lon": filtered["LON"].mean()},
    height=600,
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig)
