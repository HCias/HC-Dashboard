import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

# Create gender visualization
st.subheader("Distribusi Gender Karyawan")

# Count the gender distribution (using filtered data)
gender_counts = filtered_df['JENIS KELAMIN'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

with col1:
    # Create a figure with soft colors using matplotlib and seaborn
    fig, ax = plt.subplots(figsize=(5, 3.5))
    colors = ['#8FB3D9', '#D99AC5']  # Soft blue and soft pink

    # Create the plot
    sns.barplot(x='Gender', y='Count', data=gender_counts, palette=colors, ax=ax)

    # Customize plot
    plt.title('Jumlah Karyawan Berdasarkan Gender', fontsize=12)
    plt.xlabel('Gender', fontsize=10)
    plt.ylabel('Jumlah Karyawan', fontsize=10)

    # Add count labels on top of bars
    for i, count in enumerate(gender_counts['Count']):
        plt.text(i, count + 5, str(count), ha='center', fontsize=10)

    # Remove spines
    sns.despine()
    
    # Tighter layout
    plt.tight_layout()

    # Display the plot
    st.pyplot(fig)

with col2:
    # Create a pie chart as an alternative view
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    ax2.pie(gender_counts['Count'], labels=gender_counts['Gender'], autopct='%1.1f%%', 
            colors=colors, startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Persentase Gender Karyawan', fontsize=12)
    
    # Tighter layout
    plt.tight_layout()

    # Display the pie chart
    st.pyplot(fig2)
