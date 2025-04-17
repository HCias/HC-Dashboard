import streamlit as st
import pandas as pd
import os

# Import visualization modules
from visualizations.gender_visualization import display_gender_charts
from visualizations.age_visualization import display_age_charts

# Set page configuration
st.set_page_config(
    page_title="Employee Data",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and introduction
st.title("Dashboard Karyawan")
st.write("Dashboard Karyawan")

# Path to the CSV file (using CSV instead of Excel for better compatibility)
file_path = os.path.join('dataset', 'db_dashboard.csv')

# Read the CSV file
df = pd.read_csv(file_path)

# Add sidebar with filters
st.sidebar.header("Filter Data")

# Month filter
bulan_list = ["All"] + sorted(df["BULAN"].unique().tolist())
selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_list)

# Year filter
if 'TAHUN' in df.columns:
    tahun_list = ["All"] + sorted(df["TAHUN"].unique().tolist())
    selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)
else:
    selected_tahun = "All"

# Apply filters
filtered_df = df.copy()

if selected_bulan != "All":
    filtered_df = filtered_df[filtered_df["BULAN"] == selected_bulan]

if 'TAHUN' in df.columns and selected_tahun != "All":
    filtered_df = filtered_df[filtered_df["TAHUN"] == selected_tahun]

# Display filter information
filter_info = []
if selected_bulan != "All":
    filter_info.append(f"Bulan: {selected_bulan}")
if selected_tahun != "All":
    filter_info.append(f"Tahun: {selected_tahun}")

if filter_info:
    st.write("Filter aktif: " + ", ".join(filter_info))

# Display gender charts
display_gender_charts(filtered_df)

# Display age charts
display_age_charts(filtered_df)
