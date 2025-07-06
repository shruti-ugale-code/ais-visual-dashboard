import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 Interactive Vessel Trajectories (Clean Paths)")
st.markdown("Select vessels to display on the map:")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])
    return df

df = load_data()

# Select specific vessels
unique_vessels = sorted(df['VesselName'].unique())
selected_vessels = st.multiselect(
    "Choose vessels:",
    options=unique_vessels,
    default=unique_vessels[:5]
)

# Filter data
filtered = df[df['VesselName'].isin(selected_vessels)]

# Sort for connected lines
filtered = filtered.sort_values(by=['VesselName', 'timestamp'])

# Show warning if no data
if filtered.empty:
    st.warning("⚠️ No data found for selected vessels.")
else:
    # Draw line trajectories
    fig = px.line_mapbox(
        filtered,
        lat='LAT',
        lon='LON',
        color='VesselName',
        line_group='VesselName',
        hover_name='VesselName',
        zoom=5,
        height=650
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig, use_container_width=True)

# Show table
st.subheader("📄 Trajectory Data Sample")
st.dataframe(filtered.tail(15))
