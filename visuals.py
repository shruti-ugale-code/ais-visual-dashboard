import streamlit as st
import pandas as pd
import folium
from folium import plugins
import streamlit.components.v1 as components

# Page settings
st.set_page_config(layout="wide")
st.title("🚢 AIS Ship Trajectories Map")

# Load AIS data
df = pd.read_csv("ais_cleaned_trajectories.csv")

if df.empty:
    st.warning("The CSV file is empty.")
    st.stop()

# Create Folium map centered around average ship location
m = folium.Map(location=[df["LAT"].mean(), df["LON"].mean()], zoom_start=8)

# Get list of unique vessels
vessels = df["VesselName"].unique()

# Loop through each ship and draw its trajectory
for vessel in vessels:
    ship_data = df[df["VesselName"] == vessel].sort_values("timestamp")
    coords = list(zip(ship_data["LAT"], ship_data["LON"]))

    # Skip ships with fewer than 2 points
    if len(coords) < 2:
        continue

    # Draw trajectory as a blue line
    folium.PolyLine(
        coords,
        color="blue",
        weight=3,
        opacity=0.7
    ).add_to(m)

    # Add red circle markers with timestamps every 5th point
    for i in range(0, len(ship_data), 5):
        folium.CircleMarker(
            location=[ship_data.iloc[i]["LAT"], ship_data.iloc[i]["LON"]],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup=f"{vessel}<br>{ship_data.iloc[i]['timestamp']}"
        ).add_to(m)

# Save map to HTML
m.save("map.html")

# Read HTML and render in Streamlit using iframe
with open("map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

components.html(map_html, height=700, scrolling=False)

components.html(map_html, height=700)
