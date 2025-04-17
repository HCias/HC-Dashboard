import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_gender_charts(filtered_df):
    """
    Display gender distribution charts.
    
    Parameters:
    -----------
    filtered_df : pandas.DataFrame
        The filtered dataframe containing employee data
    """
    # Create gender visualization
    st.subheader("Distribusi Gender Karyawan")

    # Count the gender distribution (using filtered data)
    gender_counts = filtered_df['JENIS KELAMIN'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    # Create two columns for side-by-side layout
    col1, col2 = st.columns(2)

    with col1:
        # Create a figure with colors matching IAS corporate identity
        fig, ax = plt.subplots(figsize=(5, 3.5))
        colors = ['#003C71', '#E36F1E']  # Navy blue and orange (IAS corporate colors)

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
