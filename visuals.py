# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import os
from datetime import timedelta

st.set_page_config(layout="wide", page_title="Ship Tracks")

# -----------------------------
# Your exact CSV filenames
# -----------------------------
CSV_FILES = [
    "ais_animated_trajectory_sample.csv",
    "ais_cleaned_trajectories.csv",
    "ais_data_sample.csv",
    "ais_data_sample_with_trajectories.csv",
    "ais_singapore_strait_animated.csv",
    "ship_data_sample.csv"
]

st.sidebar.header("Data + Refresh")
autorefresh = st.sidebar.checkbox("Auto refresh (simulate live)", value=True)
refresh_secs = st.sidebar.number_input("Refresh interval (sec)", min_value=2, max_value=300, value=8)

@st.cache_data
def load_and_normalize():
    frames = []
    for file in CSV_FILES:
        if os.path.exists(file):
            df = pd.read_csv(file)
            df["__source_file"] = os.path.basename(file)
            frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["ship_id", "lat", "lon", "timestamp", "__source_file"])
    
    df = pd.concat(frames, ignore_index=True)

    # --- auto-detect columns ---
    def find_col(candidates):
        for c in df.columns:
            if c.lower() in candidates:
                return c
        return None

    id_col = find_col({"mmsi", "imo", "ship_id", "vessel", "id", "callsign"})
    lat_col = find_col({"lat", "latitude"})
    lon_col = find_col({"lon", "lng", "longitude", "long"})
    time_col = find_col({"timestamp", "time", "datetime", "date", "utc_time", "ts"})

    if id_col is None:
        df["ship_id"] = df["__source_file"]
    else:
        df["ship_id"] = df[id_col].astype(str)

    if lat_col and lon_col:
        df["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
        df["lon"] = pd.to_numeric(df[lon_col], errors="coerce")
    else:
        return pd.DataFrame(columns=["ship_id", "lat", "lon", "timestamp", "__source_file"])

    if time_col:
        df["timestamp"] = pd.to_datetime(df[time_col], errors="coerce")
    else:
        df["timestamp"] = pd.NaT

    df = df.dropna(subset=["lat", "lon", "timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df[["ship_id", "lat", "lon", "timestamp", "__source_file"]]

df = load_and_normalize()

if df.empty:
    st.warning("No data loaded from your CSV files.")
    st.stop()

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")
all_ships = sorted(df["ship_id"].unique().tolist())
selected_ships = st.sidebar.multiselect("Select ship(s)", all_ships, default=all_ships[:3])

min_date = df["timestamp"].dt.date.min()
max_date = df["timestamp"].dt.date.max()
start_date, end_date = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

mask = df["ship_id"].isin(selected_ships) & \
       (df["timestamp"] >= pd.to_datetime(start_date)) & \
       (df["timestamp"] <= pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1))

filtered = df.loc[mask]
st.write(f"Showing {len(filtered)} records for {len(selected_ships)} ship(s).")

if autorefresh:
    st_autorefresh(interval=refresh_secs * 1000, limit=None, key="ship_autorefresh")

# -----------------------------
# Map rendering
# -----------------------------
if filtered.empty:
    st.info("No data in selected date range / ships.")
else:
    center = [filtered["lat"].mean(), filtered["lon"].mean()]
    folium_map = folium.Map(location=center, zoom_start=6, tiles="CartoDB positron")

    colors = ["blue", "green", "red", "purple", "orange", "darkblue", "lightgreen", "cadetblue", "darkred", "beige"]

    max_points_per_ship = st.sidebar.slider("Max points per ship", 100, 5000, 1500)

    for i, ship in enumerate(selected_ships):
        sub = filtered[filtered["ship_id"] == ship].sort_values("timestamp")
        if sub.empty:
            continue

        step = max(1, int(len(sub) / max_points_per_ship))
        trace = list(zip(sub["lat"].iloc[::step].tolist(), sub["lon"].iloc[::step].tolist()))

        folium.PolyLine(
            locations=trace,
            color=colors[i % len(colors)],
            weight=3,
            tooltip=f"{ship} — {len(sub)} pts"
        ).add_to(folium_map)

        start = sub.iloc[0]
        end = sub.iloc[-1]

        folium.CircleMarker(
            location=[start["lat"], start["lon"]],
            radius=5, color="green", fill=True,
            popup=f"Start<br>{ship}<br>{start['timestamp']}"
        ).add_to(folium_map)

        folium.CircleMarker(
            location=[end["lat"], end["lon"]],
            radius=5, color="red", fill=True,
            popup=f"End<br>{ship}<br>{end['timestamp']}"
        ).add_to(folium_map)

    st_folium(folium_map, width=1000, height=700)
