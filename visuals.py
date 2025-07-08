import pandas as pd
import folium

# Load the cleaned AIS CSV file
df = pd.read_csv("ais_cleaned_trajectories.csv")

# Create base map centered around mean coordinates
m = folium.Map(location=[df["LAT"].mean(), df["LON"].mean()], zoom_start=8)

# Group by each vessel
vessels = df["VesselName"].unique()

for vessel in vessels:
    # Filter and sort each vessel's data by timestamp
    ship_data = df[df["VesselName"] == vessel].sort_values("timestamp")
    coords = list(zip(ship_data["LAT"], ship_data["LON"]))
    
    # Skip if not enough points for a line
    if len(coords) < 2:
        continue

    # Draw the trajectory as a blue line
    folium.PolyLine(
        coords,
        color="blue",
        weight=3,
        opacity=0.7
    ).add_to(m)

    # Add red markers with timestamp popup every 5 steps
    for i in range(0, len(ship_data), 5):
        folium.CircleMarker(
            location=[ship_data.iloc[i]["LAT"], ship_data.iloc[i]["LON"]],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup=f"{vessel}<br>{ship_data.iloc[i]['timestamp']}"
        ).add_to(m)

# Save the map to an HTML file
m.save("ship_trajectories_map.html")
print("✅ Map saved as ship_trajectories_map.html")
