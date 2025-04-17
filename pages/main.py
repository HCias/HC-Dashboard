import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="HC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rename the page in the sidebar from "main" to "Dashboard"
st.sidebar.markdown("# Dashboard")

# Hide the default page name that appears at the top of the sidebar
hide_streamlit_style = """
<style>
    [data-testid="collapsedControl"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    #stDecoration {display:none;}
    span[data-baseweb="tag"] {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load the data
file_path = os.path.join('dataset', 'db_dashboard.csv')
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

# Apply filters
filtered_df = df.copy()

if selected_bulan != "All":
    filtered_df = filtered_df[filtered_df["BULAN"] == selected_bulan]

if 'TAHUN' in df.columns and selected_tahun != "All":
    filtered_df = filtered_df[filtered_df["TAHUN"] == selected_tahun]

# App title and introduction
st.title("HC Dashboard")
st.write("Dashboard Analytics Karyawan")

# Display active filters if any
filter_info = []
if selected_bulan != "All":
    filter_info.append(f"Bulan: {selected_bulan}")
if selected_tahun != "All":
    filter_info.append(f"Tahun: {selected_tahun}")

if filter_info:
    st.write("Filter aktif: " + ", ".join(filter_info))

# Create metrics section
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_employees = len(filtered_df)
unique_direktorat = filtered_df["DIREKTORAT"].nunique()
unique_division = filtered_df["DIVISION"].nunique()

with col1:
    st.metric("Total Karyawan", f"{total_employees:,}")
    
with col2:
    st.metric("Jumlah Direktorat", f"{unique_direktorat}")
    
with col3:
    st.metric("Jumlah Division", f"{unique_division}")
    
with col4:
    if 'TAHUN' in filtered_df.columns and len(filtered_df) > 0:
        st.metric("Tahun Data", f"{filtered_df['TAHUN'].iloc[0]}")
    elif len(filtered_df) > 0:
        st.metric("Bulan Data", f"{filtered_df['BULAN'].iloc[0]}")
    else:
        st.metric("Data", "No data")

# Only show visualizations if there is data
if len(filtered_df) > 0:
    # Gender distribution chart - full width since we removed the direktorat chart
    st.markdown("### Distribusi Gender Karyawan")
    gender_counts = filtered_df["JENIS KELAMIN"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    
    fig_gender = px.pie(
        gender_counts, 
        values="Count", 
        names="Gender", 
        title="Distribusi Gender",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # Create second row of charts
    st.markdown("### Status & Umur Karyawan")
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        status_counts = filtered_df["STATUS KARYAWAN"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig_status = px.pie(
            status_counts, 
            values="Count", 
            names="Status", 
            title="Distribusi Status Karyawan",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with row2_col2:
        # Create age bins for better visualization
        age_bins = [0, 25, 30, 35, 40, 45, 50, 55, 60, 100]
        age_labels = ['<25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '>60']
        
        filtered_df['Age Group'] = pd.cut(filtered_df['UMUR'], bins=age_bins, labels=age_labels, right=False)
        age_counts = filtered_df['Age Group'].value_counts().sort_index().reset_index()
        age_counts.columns = ["Age Group", "Count"]
        
        fig_age = px.bar(
            age_counts, 
            x="Age Group", 
            y="Count", 
            title="Distribusi Umur Karyawan",
            color="Count",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_age, use_container_width=True)
else:
    st.warning("Tidak ada data yang tersedia dengan filter yang dipilih. Silakan ubah filter.")

# Add information about navigating to the employee data page
st.markdown("---")
st.info("👈 Untuk melihat data lengkap karyawan dan menggunakan filter lainnya, silakan kunjungi halaman 'Employee Data' di sidebar.")
