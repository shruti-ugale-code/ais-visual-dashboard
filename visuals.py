import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📍 Vessel Trajectories (Top 5)")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("ais_cleaned_trajectories.csv")
    df = df.dropna(subset=["LAT", "LON", "timestamp", "VesselName"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_data()

# Top 5 Vessels by point count
top_vessels = df['VesselName'].value_counts().head(5).index.tolist()
filtered_df = df[df['VesselName'].isin(top_vessels)]

# Plot line trajectories
fig = px.line_mapbox(
    filtered_df.sort_values("timestamp"),
    lat="LAT",
    lon="LON",
    color="VesselName",
    line_group="VesselName",
    zoom=5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

st.plotly_chart(fig, use_container_width=True)

# Latest data table
st.subheader("📊 Latest Sample Data")
st.dataframe(filtered_df.sample(20))
