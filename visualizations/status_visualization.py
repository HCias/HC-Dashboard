import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_status_charts(filtered_df):
    """
    Display employee status distribution charts.
    
    Parameters:
    -----------
    filtered_df : pandas.DataFrame
        The filtered dataframe containing employee data
    """
    # Create status visualization
    st.subheader("Distribusi Status Karyawan")

    # Count the status distribution (using filtered data)
    status_counts = filtered_df['STATUS KARYAWAN'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Create two columns for side-by-side layout
    col1, col2 = st.columns(2)

    with col1:
        # Create a figure with colors matching IAS corporate identity
        fig, ax = plt.subplots(figsize=(5, 3.5))
        
        # Generate alternating colors
        num_statuses = len(status_counts)
        colors = [('#003C71', '#E36F1E')[i % 2] for i in range(num_statuses)]

        # Create the plot
        bars = sns.barplot(x='Status', y='Count', data=status_counts, palette=colors, ax=ax)

        # Customize plot
        plt.title('Jumlah Karyawan Berdasarkan Status', fontsize=12)
        plt.xlabel('Status Karyawan', fontsize=10)
        plt.ylabel('Jumlah Karyawan', fontsize=10)
        
        # Rotate x-axis labels if there are many status types
        if num_statuses > 3:
            plt.xticks(rotation=45, ha='right')

        # Add count labels on top of bars
        for i, count in enumerate(status_counts['Count']):
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
        
        # Generate colors for pie chart
        pie_colors = ['#003C71', '#E36F1E', '#005A99', '#FF8D3C', '#0078CC'] 
        # Use only as many colors as needed
        pie_colors = pie_colors[:num_statuses]
        
        ax2.pie(status_counts['Count'], labels=status_counts['Status'], autopct='%1.1f%%', 
                colors=pie_colors, startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Persentase Status Karyawan', fontsize=12)
        
        # Tighter layout
        plt.tight_layout()

        # Display the pie chart
        st.pyplot(fig2)
        
    # Add a table with detailed status information
    st.markdown("### Rincian Status Karyawan")
    
    # Add status count with percentage
    status_percentage = pd.DataFrame({
        'Status': status_counts['Status'],
        'Jumlah': status_counts['Count'],
        'Persentase': (status_counts['Count'] / status_counts['Count'].sum() * 100).round(2).astype(str) + '%'
    })
    
    # Display the table
    st.dataframe(
        status_percentage,
        column_config={
            "Status": st.column_config.TextColumn("Status Karyawan"),
            "Jumlah": st.column_config.NumberColumn("Jumlah"),
            "Persentase": st.column_config.TextColumn("Persentase")
        },
        use_container_width=True,
        hide_index=True
    )
