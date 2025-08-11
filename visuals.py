import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import glob
import os

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="ship_refresh")

# Title
st.title("Ship Trajectories on Map (Auto Refresh)")

# Get all CSV files in current directory
csv_files = glob.glob("*.csv")

all_dataframes = []
for file in csv_files:
    try:
        df_temp = pd.read_csv(file)
        # Skip empty or irrelevant CSVs
        if df_temp.empty:
            continue

        # Ensure correct column count before renaming
        if len(df_temp.columns) >= 16:
            df_temp = df_temp.iloc[:, :16]  # Keep first 16 cols
            df_temp.columns = [
                'MMSI', 'Date', 'Latitude', 'Longitude', 'Speed', 'Course',
                'ShipType', 'VesselName', 'IMO', 'CallSign', 'Length', 'Width',
                'Draft', 'Cargo', 'HazardousCargo', 'Region'
            ]
            all_dataframes.append(df_temp)
    except Exception as e:
        st.warning(f"Skipping file {file} due to error: {e}")

# Combine all CSV data
if not all_dataframes:
    st.error("No valid ship data found in CSV files.")
    st.stop()

df = pd.concat(all_dataframes, ignore_index=True)

# Keep only valid lat/lon
df = df.dropna(subset=["Latitude", "Longitude"])

# Ensure numeric lat/lon
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
df = df.dropna(subset=["Latitude", "Longitude"])

# Group by vessel
grouped = df.groupby("VesselName")

# Ship type color mapping
ship_colors = {
    "Fishing": "blue",
    "Cargo": "brown",
    "Tanker": "green",
    "Passenger": "purple",
    "Pleasure Craft": "pink"
}

# Create map
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

# Add trajectories
for name, group in grouped:
    ship_type = group["ShipType"].iloc[0] if not group["ShipType"].isna().all() else "Other"
    color = ship_colors.get(ship_type, "gray")  # Default to gray if unknown

    points = list(zip(group["Latitude"], group["Longitude"]))
    folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)

    for _, row in group.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{name} ({ship_type})\n{row['Date']}",
        ).add_to(m)

# Show map
st_folium(m, width=1200, height=700)
