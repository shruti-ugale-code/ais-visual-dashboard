import pandas as pd
import folium

# Load AIS data
df = pd.read_csv("ais_cleaned_trajectories.csv")

# Create base map centered around the average location
center_lat = df["LAT"].mean()
center_lon = df["LON"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

# Get unique vessel names
vessels = df["VesselName"].unique()

# Plot each vessel's path
for vessel in vessels:
    ship_data = df[df["VesselName"] == vessel].sort_values("timestamp")
    
    # Get coordinates
    coords = list(zip(ship_data["LAT"], ship_data["LON"]))

    # Draw trajectory as blue line
    folium.PolyLine(coords, color="blue", weight=3, opacity=0.7).add_to(m)
    
    # Place red markers with timestamps every few points
    for i in range(0, len(ship_data), 5):  # every 5th point
        folium.Marker(
            location=[ship_data.iloc[i]["LAT"], ship_data.iloc[i]["LON"]],
            popup=f"{vessel}<br>{ship_data.iloc[i]['timestamp']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Save the interactive map
m.save("ship_trajectories_map.html")
print("✅ Map saved as ship_trajectories_map.html")
