import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_age_charts(filtered_df):
    """
    Display age distribution charts and statistics.
    
    Parameters:
    -----------
    filtered_df : pandas.DataFrame
        The filtered dataframe containing employee data
    """
    # Create age visualization
    st.subheader("Distribusi Umur Karyawan")

    # Check if 'UMUR' column exists and has valid data
    if 'UMUR' in filtered_df.columns and not filtered_df['UMUR'].isnull().all():
        # Remove rows with missing age values
        age_df = filtered_df.dropna(subset=['UMUR']).copy()
        
        # Convert age to numeric, coercing errors to NaN
        age_df['UMUR'] = pd.to_numeric(age_df['UMUR'], errors='coerce')
        
        # Drop any rows where conversion failed
        age_df = age_df.dropna(subset=['UMUR'])
        
        # Create two columns for side-by-side layout
        col3, col4 = st.columns(2)
        
        with col3:
            # Create a histogram of ages
            fig3, ax3 = plt.subplots(figsize=(5, 3.5))
            
            # Create histogram with IAS colors
            n, bins, patches = ax3.hist(age_df['UMUR'], bins=10, color='#003C71', edgecolor='white', alpha=0.8)
            
            # Add a title and labels
            plt.title('Distribusi Umur Karyawan', fontsize=12)
            plt.xlabel('Umur (Tahun)', fontsize=10)
            plt.ylabel('Jumlah Karyawan', fontsize=10)
            
            # Tighter layout
            plt.tight_layout()
            
            # Display the histogram
            st.pyplot(fig3)
        
        with col4:
            # Create age groups for easier analysis
            bins = [20, 30, 40, 50, 60, 70]
            labels = ['20-29', '30-39', '40-49', '50-59', '60+']
            
            age_df['Age Group'] = pd.cut(age_df['UMUR'], bins=bins, labels=labels, right=False)
            
            # Count by age group
            age_group_counts = age_df['Age Group'].value_counts().reset_index()
            age_group_counts.columns = ['Age Group', 'Count']
            
            # Sort by age group
            age_group_counts = age_group_counts.sort_values('Age Group')
            
            # Create a bar chart
            fig4, ax4 = plt.subplots(figsize=(5, 3.5))
            
            # Create bar chart with IAS colors
            bar_colors = ['#003C71', '#E36F1E', '#003C71', '#E36F1E', '#003C71']
            sns.barplot(x='Age Group', y='Count', data=age_group_counts, palette=bar_colors, ax=ax4)
            
            # Add a title and labels
            plt.title('Karyawan Berdasarkan Kelompok Umur', fontsize=12)
            plt.xlabel('Kelompok Umur', fontsize=10)
            plt.ylabel('Jumlah Karyawan', fontsize=10)
            
            # Add count labels on top of bars
            for i, count in enumerate(age_group_counts['Count']):
                plt.text(i, count + 5, str(count), ha='center', fontsize=10)
            
            # Remove spines
            sns.despine()
            
            # Tighter layout
            plt.tight_layout()
            
            # Display the bar chart
            st.pyplot(fig4)
            
        # Add some statistics about age
        st.markdown("### Statistik Umur Karyawan")
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Rata-rata Umur", f"{age_df['UMUR'].mean():.1f}")
        
        with stats_col2:
            st.metric("Umur Median", f"{age_df['UMUR'].median():.1f}")
        
        with stats_col3:
            st.metric("Umur Minimum", f"{age_df['UMUR'].min():.1f}")
        
        with stats_col4:
            st.metric("Umur Maksimum", f"{age_df['UMUR'].max():.1f}")
            
        # Add section for employees over 50 years old (approaching retirement)
        st.markdown("### Karyawan Mendekati Usia Pensiun (> 50 Tahun)")
        
        # Filter employees over 50 years old
        retirement_df = age_df[age_df['UMUR'] > 50].copy()
        
        # Sort by age descending to show oldest employees first
        retirement_df = retirement_df.sort_values('UMUR', ascending=False)
        
        # Select relevant columns for display
        if 'NAMA KARYAWAN' in retirement_df.columns and 'DIREKTORAT' in retirement_df.columns:
            display_cols = ['NAMA KARYAWAN', 'UMUR', 'DIREKTORAT', 'DIVISION', 'JENIS KELAMIN']
            display_cols = [col for col in display_cols if col in retirement_df.columns]
            
            # Show count
            st.write(f"Jumlah karyawan di atas 50 tahun: **{len(retirement_df)}** orang")
            
            # Display the dataframe with formatting
            st.dataframe(
                retirement_df[display_cols],
                column_config={
                    "NAMA KARYAWAN": st.column_config.TextColumn("Nama Karyawan"),
                    "UMUR": st.column_config.NumberColumn("Umur (Tahun)"),
                    "DIREKTORAT": st.column_config.TextColumn("Direktorat"),
                    "DIVISION": st.column_config.TextColumn("Divisi"),
                    "JENIS KELAMIN": st.column_config.TextColumn("Gender")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Add download button for the retirement list
            csv = retirement_df[display_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Daftar Karyawan > 50 Tahun",
                data=csv,
                file_name="karyawan_mendekati_pensiun.csv",
                mime="text/csv",
            )
        else:
            st.warning("Data karyawan tidak lengkap untuk menampilkan daftar karyawan mendekati pensiun.")
    else:
        st.warning("Data umur tidak tersedia atau semua nilai kosong.")
