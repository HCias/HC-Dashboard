import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and introduction
st.title("HC Dashboard")
st.write("Visualisasi Data Karyawan")

# Path to the Excel file
file_path = os.path.join('dataset', 'db_dashboard.xlsx')

# Read the Excel file
df = pd.read_excel(file_path)

# Display information about the data
st.subheader("Data Karyawan")
st.write(f"Total data: {len(df)} karyawan")

# Display the DataFrame as a table
st.dataframe(df, use_container_width=True)

# Add a feature to download the data
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data CSV",
    data=csv,
    file_name="employee_data.csv",
    mime="text/csv",
)
