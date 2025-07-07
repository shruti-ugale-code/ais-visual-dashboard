import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean the data
@st.cache_data
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")

    # Basic cleanup
    df = df[['VesselName', 'LAT', 'LON', 'timestamp', 'sog', 'heading', 'width', 'length', 'shiptype']]
    df = df.dropna()
    
    # Remove invalid GPS
    df = df[(df['LAT'].between(-90, 90)) & (df['LON'].between(-180, 180))]

    # Focus only on Singapore Strait area to remove land trajectories
    df = df[(df['LAT'].between(1.0, 1.6)) & (df['LON'].between(103.5, 104.5))]

    # Ensure datetime is sorted for proper lines
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['VesselName', 'timestamp'])

    return df

# Load data
df = load_data()

# Streamlit UI
st.title("🧭 Vessel Trajectories (Top 5)")

top5_vessels = df['VesselName'].value_counts().head(5).index.tolist()
filtered = df[df['VesselName'].isin(top5_vessels)]

# Plotting
fig = px.line_mapbox(
    filtered,
    lat="LAT",
    lon="LON",
    color="VesselName",
    line_group="VesselName",
    hover_name="VesselName",
    hover_data={"timestamp": True, "sog": True, "shiptype": True},
    zoom=8,
    height=700
)

fig.update_layout(mapbox_style="carto-positron")  # Clean map look
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Show plot
st.plotly_chart(fig)
