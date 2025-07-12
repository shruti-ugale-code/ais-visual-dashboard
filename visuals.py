import pandas as pd
import folium
from folium.plugins import AntPath

# Load your data
df = pd.read_csv("ship_data_sample.csv")

# Optional: convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group by vessel
grouped = df.groupby("VesselName")

# Create a map centered on the average location
avg_lat = df["Latitude"].mean()
avg_lon = df["Longitude"].mean()
ship_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

# Loop through each ship's data
for name, group in grouped:
    group_sorted = group.sort_values("Date")

    # Plot trajectory as a blue AntPath line
    points = list(zip(group_sorted["Latitude"], group_sorted["Longitude"]))
    AntPath(points, color='blue', weight=3).add_to(ship_map)

    # Add red dots and timestamps
    for _, row in group_sorted.iterrows():
        folium.CircleMarker(
            location=(row["Latitude"], row["Longitude"]),
            radius=4,
            color='red',
            fill=True,
            fill_color='red',
        ).add_to(ship_map)
        folium.map.Marker(
            [row["Latitude"], row["Longitude"]],
            icon=folium.DivIcon(html=f"""<div style="font-size: 8pt">{row["Date"].date()}</div>""")
        ).add_to(ship_map)

# Save to HTML
ship_map.save("ship_trajectories_map.html")
