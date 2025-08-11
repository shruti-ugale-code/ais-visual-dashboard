import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os

# Auto-refresh every 5 seconds
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

# Standard column mapping (index-based to avoid mismatch errors)
column_mapping = {
    0: 'MMSI',
    1: 'Date',
    2: 'Latitude',
    3: 'Longitude',
    4: 'Speed',
    5: 'Course',
    6: 'ShipType',
    7: 'VesselName',
    8: 'IMO',
    9: 'CallSign',
    10: 'Length',
    11: 'Width',
    12: 'Draft',
    13: 'Cargo',
    14: 'HazardousCargo',
    15: 'Region'
}
import glob

# List of all your CSV files
csv_files = [
    "file1.csv",
    "file2.csv",
    "file3.csv"
    # add all your ship CSV filenames here
]

# Read each CSV into a dataframe and store in a list
all_dataframes = []
for file in csv_files:
    df_temp = pd.read_csv(file)
    all_dataframes.append(df_temp)

# Combine them into one dataframe
df = pd.concat(all_dataframes, ignore_index=True)

# After reading CSVs and merging
df = pd.concat(all_dataframes, ignore_index=True)

# ✅ Paste here
df = df.dropna(subset=["Latitude", "Longitude"])
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
df = df.dropna(subset=["Latitude", "Longitude"])

# Map center calculation will now work
m = folium.Map(
    location=[df["Latitude"].mean(), df["Longitude"].mean()],
    zoom_start=5
)

# Load and merge all CSVs
frames = []
for file in CSV_FILES:
    if os.path.exists(file):
        df_temp = pd.read_csv(file)

        # Rename columns safely (only if index exists in file)
        df_temp.rename(
            columns={
                df_temp.columns[i]: new_name
                for i, new_name in column_mapping.items()
                if i < len(df_temp.columns)
            },
            inplace=True
        )

        frames.append(df_temp)

if not frames:
    st.error("No CSV files found. Please check file paths.")
    st.stop()

df = pd.concat(frames, ignore_index=True)

# Drop rows without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Convert Date to datetime (if exists)
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Define ship type colors
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

# Create map centered on mean location
m = folium.Map(
    location=[df["Latitude"].mean(), df["Longitude"].mean()],
    zoom_start=5
)

# Group and plot
if "VesselName" in df.columns:
    for name, group in df.groupby("VesselName"):
        ship_type = group["ShipType"].iloc[0] if "ShipType" in group.columns and not group["ShipType"].isna().all() else "Other"
        color = ship_colors.get(ship_type, "black")

        # Polyline for ship trajectory
        points = list(zip(group["Latitude"], group["Longitude"]))
        folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)

        # Circle markers
        for _, row in group.iterrows():
            popup_text = f"{name} ({ship_type})"
            if "Date" in row:
                popup_text += f"\n{row['Date']}"
            folium.CircleMarker(
                location=(row["Latitude"], row["Longitude"]),
                radius=3,
                color=color,
                fill=True,
                fill_color=color,
                popup=popup_text,
            ).add_to(m)

# Show map
st_folium(m, width=1200, height=700)


