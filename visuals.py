import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os

# Auto-refresh every 5 seconds (5000 ms)
st_autorefresh(interval=5000, key="map_refresh")

# List of CSV files to load
CSV_FILES = [
    "ais_animated_trajectory_sample.csv",
    "ais_cleaned_trajectories.csv",
    "ais_data_sample.csv",
    "ais_data_sample_with_trajectories.csv",
    "ais_singapore_strait_animated.csv",
    "ship_data_sample.csv"
]

# Load all CSVs into one DataFrame
frames = []
for file in CSV_FILES:
    if os.path.exists(file):
        df_temp = pd.read_csv(file)
        frames.append(df_temp)

if not frames:
    st.error("No CSV files found. Please check file paths.")
    st.stop()

df = pd.concat(frames, ignore_index=True)

# Try to standardize columns — adjust if different in your files
df.columns = [
    'MMSI', 'Date', 'Latitude', 'Longitude', 'Speed', 'Course', 'ShipType',
    'VesselName', 'IMO', 'CallSign', 'Length', 'Width', 'Draft',
    'Cargo', 'HazardousCargo', 'Region'
]

# Drop rows without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Convert Date to datetime if not already
if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Define colors for ship types
ship_colors = {
    "Fishing": "blue",
    "Cargo": "brown",
    "Tanker": "red",
    "Passenger": "green",
    "Pleasure Craft": "purple",
    "Other": "gray"
}

# Title
st.title("Ship Trajectories on Map (Auto-Refreshing, Multi-CSV)")

# Create base map centered on mean coords
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

# Group by vessel and plot
for name, group in df.groupby("VesselName"):
    ship_type = group["ShipType"].iloc[0] if not group["ShipType"].isna().all() else "Other"
    color = ship_colors.get(ship_type, "black")

    # Draw polyline for full trajectory
    points = list(zip(group["Latitude"], group["Longitude"]))
    folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)

    # Add markers for each recorded position
    for _, row in group.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{name} ({ship_type})\n{row['Date']}",
        ).add_to(m)

# Display in Streamlit
st_folium(m, width=1200, height=700)
