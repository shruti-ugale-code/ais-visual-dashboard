import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

# Load data
df = pd.read_csv("ship_data_sample.csv")

# Update columns (17 columns as per your CSV)
# This is correct for your file
df.columns = ['MMSI', 'Date', 'Latitude', 'Longitude', 'Speed', 'Course', 'ShipType',
              'VesselName', 'IMO', 'CallSign', 'Length', 'Width', 'Draft',
              'Cargo', 'HazardousCargo', 'Region']


# Drop rows with missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Group by ShipName
grouped = df.groupby("ShipName")

# Create Streamlit app
st.title("Ship Trajectories on Map")

# Create base map
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

# Plot each ship's trajectory
for name, group in grouped:
    points = list(zip(group["Latitude"], group["Longitude"]))
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

    for _, row in group.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=3,
            color="red",
            fill=True,
            fill_color="red",
            popup=f"{name}\n{row['Date']}",
        ).add_to(m)

# Show the map in Streamlit
st_folium(m, width=1200, height=700)
