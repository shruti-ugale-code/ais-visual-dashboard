import streamlit as st
import pandas as pd
import time
import random

# Title
st.title("🚢 AIS Real-Time Dashboard")
st.caption("Refreshing every 5 seconds to simulate real-time updates.")

# Load data
def load_data():
    df = pd.read_csv("ais_data_sample.csv")
    df['sog'] = pd.to_numeric(df['sog'], errors='coerce')
    df['heading'] = pd.to_numeric(df['heading'], errors='coerce')
    df['width'] = pd.to_numeric(df['width'], errors='coerce')
    df['length'] = pd.to_numeric(df['length'], errors='coerce')
    df = df.dropna(subset=['sog', 'heading', 'width', 'length'])
    return df

df = load_data()

# Sample a subset to simulate changing visuals
subset = df.sample(20)

# Column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Speed Over Ground (SOG)")
    st.line_chart(subset['sog'])

with col2:
    st.subheader("Heading Distribution")
    st.bar_chart(subset['heading'])

# Ship Type Count
st.subheader("🚢 Ship Type Count")
ship_type_count = subset['shiptype'].value_counts()
st.bar_chart(ship_type_count)

# Data table
st.subheader("📊 Latest Sample Data")
st.dataframe(subset)

# Sleep + refresh
time.sleep(5)
st.rerun()
