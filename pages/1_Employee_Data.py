import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="Employee Data",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and introduction
st.title("Data Karyawan")
st.write("Visualisasi dan Filtering Data Karyawan")

# Path to the CSV file (using CSV instead of Excel for better compatibility)
file_path = os.path.join('dataset', 'db_dashboard.csv')

# Read the CSV file
df = pd.read_csv(file_path)

# Add sidebar with filters
st.sidebar.header("Filter Data")

# Month filter
bulan_list = ["All"] + sorted(df["BULAN"].unique().tolist())
selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_list)

# Year filter (if 'TAHUN' column exists)
if 'TAHUN' in df.columns:
    tahun_list = ["All"] + sorted(df["TAHUN"].unique().tolist())
    selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)
else:
    selected_tahun = "All"

# Department filter
direktorat_list = ["All"] + sorted(df["DIREKTORAT"].unique().tolist())
selected_direktorat = st.sidebar.selectbox("Pilih Direktorat", direktorat_list)

# Status filter
status_list = ["All"] + sorted(df["STATUS KARYAWAN"].unique().tolist())
selected_status = st.sidebar.selectbox("Pilih Status Karyawan", status_list)

# Apply filters
filtered_df = df.copy()

if selected_bulan != "All":
    filtered_df = filtered_df[filtered_df["BULAN"] == selected_bulan]

if 'TAHUN' in df.columns and selected_tahun != "All":
    filtered_df = filtered_df[filtered_df["TAHUN"] == selected_tahun]

if selected_direktorat != "All":
    filtered_df = filtered_df[filtered_df["DIREKTORAT"] == selected_direktorat]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["STATUS KARYAWAN"] == selected_status]

# Reset index for display
filtered_df = filtered_df.reset_index(drop=True)

# Display information about the filtered data
st.subheader("Data Karyawan")
st.write(f"Menampilkan {len(filtered_df)} dari {len(df)} karyawan")

# Add filter information
filter_info = []
if selected_bulan != "All":
    filter_info.append(f"Bulan: {selected_bulan}")
if selected_tahun != "All":
    filter_info.append(f"Tahun: {selected_tahun}")
if selected_direktorat != "All":
    filter_info.append(f"Direktorat: {selected_direktorat}")
if selected_status != "All":
    filter_info.append(f"Status: {selected_status}")

if filter_info:
    st.write("Filter aktif: " + ", ".join(filter_info))

# Display the DataFrame as a table
st.dataframe(filtered_df, use_container_width=True)

# Add a feature to download the filtered data
filtered_csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data Filtered CSV",
    data=filtered_csv,
    file_name="filtered_employee_data.csv",
    mime="text/csv",
)
