import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Vessel Trajectories", layout="wide")
st.title("🗺️ Interactive Vessel Paths")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")
    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.sort_values(by=['VesselName', 'timestamp'])
    return df

df = load_data()

# User selects vessels
selected = st.multiselect("Choose vessels:", df['VesselName'].unique(), default=df['VesselName'].unique()[:5])

if selected:
    filtered = df[df['VesselName'].isin(selected)]

    fig = px.scatter_mapbox(
        filtered,
        lat="LAT",
        lon="LON",
        color="VesselName",
        hover_name="VesselName",
        hover_data={"timestamp": True},
        line_group="VesselName",
        animation_frame=None,  # Remove animation for legend to work
        zoom=5,
        height=600
    )

    fig.update_traces(mode='lines+markers')  # 👈 This line enables toggling
    fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one vessel to display.")
