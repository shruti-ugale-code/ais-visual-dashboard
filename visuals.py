import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st


df = pd.read_csv("ship_data_sample.csv")


df.columns = ['MMSI', 'Date', 'Latitude', 'Longitude', 'Speed', 'Course', 'ShipType',
              'VesselName', 'IMO', 'CallSign', 'Length', 'Width', 'Draft',
              'Cargo', 'HazardousCargo', 'Region']



df = df.dropna(subset=["Latitude", "Longitude"])


grouped = df.groupby("VesselName")


st.title("Ship Trajectories on Map")


m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)


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


st_folium(m, width=1200, height=700)
