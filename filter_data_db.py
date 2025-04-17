import pandas as pd
import os

# Path to the Excel file
file_path = os.path.join('dataset', 'db_karyawan_from_hcs.xlsx')

# Read the Excel file
df = pd.read_excel(file_path)

# Select essential columns for the dashboard
# These are common HR dashboard columns, but you can adjust based on your needs
# Pilih kolom yang diperlukan untuk dashboard
selected_columns = [
    'BULAN',
    'TAHUN',
    'NIK IAS2', 
    'NAMA KARYAWAN',
    'DIREKTORAT',
    'DIVISION',
    'GROUP',
    'KODE POSISI',
    'REGION',
    'BOD-',
    'JENIS KELAMIN',
    'AGAMA',
    'STATUS KARYAWAN',
    'UMUR',
    'MKP'
]

# Filter only the columns that exist in the dataframe
valid_columns = [col for col in selected_columns if col in df.columns]
filtered_df = df[valid_columns]

# Display information about the filtered data
print(f"Original data dimensions: {df.shape}")
print(f"Filtered data dimensions: {filtered_df.shape}")
print("\nFiltered columns:")
for col in filtered_df.columns:
    print(f"- {col}")

# Export the filtered data to CSV format
output_csv_path = os.path.join('dataset', 'db_dashboard.csv')
filtered_df.to_csv(output_csv_path, index=False)

print(f"\nFiltered data exported to CSV: {output_csv_path}")

# Display a sample of the filtered data
print("\nSample of filtered data:")
print(filtered_df.head())
