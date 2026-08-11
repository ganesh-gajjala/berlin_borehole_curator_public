# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:08:47 2026

@author: Ganesh Gajjala
"""

import pandas as pd
import os

def export_stratigraphy_parameters(input_file_path, output_directory):
    """
    Reads the Berlin 3D GeoModell parameter file, groups data by Stratigraphie ID,
    formats specific permeability columns to fixed decimal notation,
    and exports individual CSV files safely.
    """
    # Verify if the source file exists before trying to read it
    if not os.path.exists(input_file_path):
        print(f"Error: Source file not found at {input_file_path}")
        return

    # 1. Read the input file using a safe path string
    print(f"Reading data from: {input_file_path}...")
    parameters_df = pd.read_csv(input_file_path, delimiter='\t')

    # Define target stratigraphic horizons in order corresponding to ID 1 to 11
    columns = [
        'Q1_Holozean_Neu', 'Q2_Holozean_Alt', 'Q3_Holozean_bis_Weichsel',
        'Q4_Weichsel', 'Q5_Eem', 'Q6_Saale', 'Q7_Holstein', 
        'Q8_Elster', 'T1_Miozean', 'T2_Oberoligozean', 'T3_Rupel'
    ]

    columns_to_format = ['kf_P10', 'kf_P50', 'kf_P90']
    stratigraphy_id = 1

    print("\nStarting export loop...")
    for column in columns:
        # 2. Filter data for the current Stratigraphie ID
        df = parameters_df[parameters_df["Stratigraphie"] == stratigraphy_id]
        
        # Check if the filtered dataframe contains any records
        if df.empty:
            print(f"  [Warning] No rows found for Stratigraphie ID {stratigraphy_id} ('{column}'). Creating empty or skipping file.")
        
        export_df = df.copy()

        # 3. Format targeted float columns to decimal representation safely handling empty/NaN values
        for col in columns_to_format:
            if col in export_df.columns:
                # Using pd.notnull(x) prevents errors if there are empty/NaN cells in the data
                export_df[col] = export_df[col].map(lambda x: f"{x:.6f}" if pd.notnull(x) else "")

        # 4. Generate safe destination path
        output_file_path = os.path.join(output_directory, f"{column}.csv")
        
        # Save out to CSV
        export_df.to_csv(output_file_path, index=True)
        print(f"  [Success] Exported ID {stratigraphy_id} -> {output_file_path} ({len(export_df)} rows written)")

        # Increment counter after loop cycle completes
        stratigraphy_id += 1

    print("\nPipeline execution complete.")

if __name__ == "__main__":
    # Using universal forward slashes:
    source_file = 'E:/Berlin_3D-GeoModell_ganz_Parameter.dat'
    destination_dir = 'E:/' # Points safely to E:\ drive base layout
    
    export_stratigraphy_parameters(source_file, destination_dir)


