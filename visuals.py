import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="AIS Trajectories", layout="wide")

st.title("🌊 Vessel Trajectories (Top 5)")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("ais_animated_trajectory_sample.csv")  # <- your CSV name
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["LAT", "LON", "VesselName", "timestamp"], inplace=True)
    return df

# --- Remove land by bounding box (adjust lat/lon if needed) ---
def remove_land_points(df):
    sea_df = df[
        (df["LAT"] >= 1.0) & (df["LAT"] <= 2.0) &   # Example for Singapore Strait
        (df["LON"] >= 103.0) & (df["LON"] <= 105.0)
    ]
    return sea_df

df = load_data()
df = remove_land_points(df)

# --- Vessel filter ---
top_vessels = df["VesselName"].value_counts().head(5).index.tolist()
selected_vessels = st.multiselect("Select vessels to display:", top_vessels, default=top_vessels)

# --- Filter data ---
filtered = df[df["VesselName"].isin(selected_vessels)]

# --- Plot trajectories ---
if not filtered.empty:
    fig = px.line_mapbox(
        filtered,
        lat="LAT",
        lon="LON",
        color="VesselName",
        line_group="VesselName",
        hover_name="VesselName",
        animation_frame=filtered["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"),
        zoom=7,
        height=600
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected vessels in sea area.")

# --- Data Preview ---
st.subheader("📄 Current Sample Data")
st.dataframe(filtered.head(20))

# --- Auto refresh every 5 seconds ---
time.sleep(5)
st.rerun()
