# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:08:47 2026

@author: Ganesh Gajjala
"""

import pandas as pd
import os

def export_hydrogeology_parameters(input_file_path, output_directory):
    """
    Reads the Berlin 3D GeoModell parameter file, groups data by 
    Stratigraphie ID, formats specific permeability columns to scientific 
    notation, and exports individual CSV files safely.
    """
    # Verify if the source file exists before trying to read it
    if not os.path.exists(input_file_path):
        print(f"Error: Source file not found at {input_file_path}")
        return

    # 1. Read the input file using a safe path string
    print(f"Reading data from: {input_file_path}...")
    parameters_df = pd.read_csv(input_file_path, delimiter='\t')

    # Define target stratigraphic horizons in order corresponding to ID 1 to 11
    strat_units = [
        "Q1_Holozean_Neu",
        "Q2_Holozean_Alt",
        "Q3_Holozean_bis_Weichsel",
        "Q4_Weichsel",
        "Q5_Eem",
        "Q6_Saale",
        "Q7_Holstein",
        "Q8_Elster",
        "T1_Miozean",
        "T2_Oberoligozean",
        "T3_Rupel",
    ]

    columns_to_format = ['kf_P10', 'kf_P50', 'kf_P90']
    stratigraphy_id = 1

    print("\nStarting export loop...")
    for strat_unit in strat_units:
        # 2. Filter data for the current Stratigraphie ID
        df = parameters_df[parameters_df["Stratigraphie"] == stratigraphy_id]
        
        # Check if the filtered dataframe contains any records
        if df.empty:
            print(f"  [Warning] No rows found for Stratigraphie ID "
                  f"{stratigraphy_id} ('{strat_unit}'). Skipping file."
                 )

       # Making a copy of dataframe for further arithmetic processing
        export_df = df.copy()

        # 3. Step A: Perform numeric scaling first across all target columns
        for col in columns_to_format:
            rescale_col = f"{col}_rescale"
            if rescale_col in export_df.columns:
                # Reverse Skua raw data multiplication with 1e9
                export_df[col] = export_df[rescale_col] / 1e9

        # Step B: Filter out rows where the physical kf_P90 value is >= 1 m/s
        if "kf_P90" in export_df.columns:
            export_df = export_df[export_df["kf_P90"] < 1].copy()

        # Step C: Format remaining numerical rows into 12 decimal scientific notation
        for col in columns_to_format:
            if col in export_df.columns:
                export_df[col] = export_df[col].map(
                    lambda x: f"{x:.12e}" if pd.notnull(x) else ""
                )

        # Deleting non-required columns safely
        cols_to_drop = ["kf_P10_rescale", "kf_P50_rescale", "kf_P90_rescale"]
        export_df.drop(columns=cols_to_drop, inplace=True, errors="ignore")

        # 4. Generate safe destination path
        output_file_path = os.path.join(output_directory, f"{strat_unit}.csv")
        
        # Save out to CSV
        export_df.to_csv(output_file_path, index=True, index_label='row_id')
        print(f"  [Success] Exported ID {stratigraphy_id} -> {output_file_path} "
              f"({len(export_df)} rows written)")

        # Increment counter after loop cycle completes
        stratigraphy_id += 1

    print("\nPipeline execution complete.")

if __name__ == "__main__":
    # Using universal forward slashes:
    source_file = 'E:/Berlin_3D-GeoModell_ganz_Parameter.dat'
    destination_dir = 'E:/' # Points safely to E:\ drive base layout
    
    export_hydrogeology_parameters(source_file, destination_dir)


