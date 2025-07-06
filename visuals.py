import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🌍 Interactive Vessel Trajectories (Clean Paths)")
st.markdown("**Select vessels to display:**")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['LAT', 'LON', 'timestamp', 'VesselName'])
    return df

df = load_data()

# Sidebar or multiselect dropdown
unique_vessels = sorted(df['VesselName'].unique())
selected_vessels = st.multiselect("Choose vessels:", unique_vessels, default=unique_vessels[:5])

# Filter by selected vessels
filtered = df[df['VesselName'].isin(selected_vessels)]

if filtered.empty:
    st.warning("No data to display for selected vessels.")
else:
    # Sort data for proper line connections
    filtered = filtered.sort_values(by=['VesselName', 'timestamp'])

    # Create scatter_mapbox with lines (grouped by VesselName)
    fig = px.line_mapbox(
        filtered,
        lat='LAT',
        lon='LON',
        color='VesselName',
        hover_name='VesselName',
        line_group='VesselName',
        zoom=6,
        height=650
    )

    fig.update_layout(mapbox_style="carto-positron", margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig, use_container_width=True)

# Show recent data
st.subheader("📄 Data Sample")
st.dataframe(filtered.tail(15))
