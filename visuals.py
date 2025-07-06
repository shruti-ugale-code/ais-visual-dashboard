import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Specific Vessel Paths", layout="wide")
st.title("🛳️ Specific Vessel Trajectories")
st.caption("Each vessel path is shown in a different color.")

# Load and clean data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("ais_singapore_strait_animated.csv")
    
    # Convert types
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Drop rows with missing values
    df = df.dropna(subset=['LAT', 'LON', 'VesselName', 'timestamp'])
    
    # Sort for smooth paths
    df = df.sort_values(by=['VesselName', 'timestamp'])
    
    return df

df = load_data()

# Let user choose vessels
available_vessels = df['VesselName'].unique().tolist()
selected_vessels = st.multiselect("Select vessels to show:", available_vessels, default=available_vessels[:3])

# Filter and plot
if selected_vessels:
    filtered_df = df[df['VesselName'].isin(selected_vessels)]
    
    fig = px.line_mapbox(
        filtered_df,
        lat='LAT',
        lon='LON',
        color='VesselName',
        line_group='VesselName',
        hover_name='VesselName',
        hover_data={'timestamp': True},
        zoom=5,
        height=600
    )

    fig.update_layout(mapbox_style='carto-positron', margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧾 Data for Selected Vessels")
    st.dataframe(filtered_df[['VesselName', 'timestamp', 'LAT', 'LON']].tail(20))
else:
    st.warning("Please select at least one vessel.")

