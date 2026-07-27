# Berlin Borehole Curator
### 📈 Executive Summary

* **The Problem:** Subsurface data repositories often consist of multi-gigabyte, fragmented relational datasets with significant spatial reference mismatches, missing values, and structural lithological inconsistencies that cause downstream 3D modeling failures.
* **The Computational Solution:** Engineered an automated data engineering and validation pipeline using Python (Pandas) and `cx_Oracle` to connect directly to relational databanks, programmatic cleaning modules, and spatial harmonization algorithms.
* **The Domain Impact:** Transformed a highly volatile state-wide dataset into a pristine, verified data infrastructure, reducing data prep anomalies for the 2.4 TB 3D-GeoModel Berlin project to zero.

An automated data engineering, harmonization, and validation pipeline written in Python to enforce plausibility controls on the Berlin Borehole Database. 

The pipeline rectifies structural data inconsistencies, refines lithological and petrographic logs, corrects geometric height errors, and exports clean, standardized datasets optimized for developing fictitious grain size distribution curves.

---

## 🛠️ Repository Architecture & Module Map

The database remediation process is divided into two distinct parts:
1. **The Oracle Pipeline:** Connects directly to the live server to clean up simple data fields and typos.
2. **The Pandas Pipeline:** Imports records into dataframes for correcting complexerrors related to structural, layer-depth, and mass-balance calculations

### Functional Support Modules
These files contain core configurations and utility functions used across both processing pipelines:
*   **`config.py`**: Configuration file containing secure credentials (username/password) for Oracle server authentication.
*   **`queries_NK.py`**: Repository of SQL statements and queries executed by the Oracle pipeline scripts.
*   **`transition_functions.py`**: Logic engine housing the data transformation routines for the Pandas pipeline.
*   **`mass_correction_functions.py`**: Mathematical validation helper functions called by the grain-size and mass-balance scripts.

---

## 🚀 Sequence of Execution

To achieve complete data consistency, you must execute the scripts sequentially. Each individual script isolates, flags, and fixes one specific data anomaly.

### Phase 1: Direct Database Corrections (Oracle Server via `cx_Oracle`)
This initial phase resolves text formatting anomalies, invalid placeholders, and structural naming rules directly inside the database.

1.  **`model_clas_change.py`**
    *   Fixes `fX schichten` errors and implements custom SenMVKU alterations to standardize *Geschiebelehm/-Mergel* and *Schluff*.
2.  **`NULL_and_KA_fix_neu.py`**
    *   Finds and replaces invalid `NULL` and `KA` placeholders located within the core petrographic columns.
3.  **`voe_fix.py`**
    *   Parses and cleans occurrences of the qualitative modifier `voe` (*vereinzelt*) inside the petrographic field.
4.  **`special_char_fix.py`**
    *   Strips broken special characters from petrographic fields and repairs malformed grain size boundary text.
5.  **`parenthesis_comma_fix.py`**
    *   Sanitizes syntax by removing or reformatting misplaced commas and parenthetical entries.
6.  **`overlap_grain_fix.py`**
    *   Resolves overlapping classification boundaries for identical grain size fractions in the raw tables.

### Phase 2: Advanced Dataframe Engineering (Pandas Pipeline)
This phase loads the pre-cleaned data into memory to solve complex, dependent data anomalies such as layer geometry, overlapping intervals, and mass fraction calculations.

1.  **`invalid_transit_fix.py`**
    *   Corrects scientifically impossible or logically invalid grain size transition paths.
2.  **`duplicate_symbol_fix.py`**
    *   Finds and prunes repetitive or duplicate petrographic shorthand symbols within single layers.
3.  **`non_petro_fix.py`**
    *   Removes non-geological characters or extraneous data entries logged in petrographic descriptions.
4.  **`modelling_classes.py`**
    *   Assigns final modeling classes to petrographic structures, applies depth corrections to borehole intervals, and re-calculates offset borehole starting coordinates.
5.  **`transit_expand.py`**
    *   Expands continuous transition logs into individual grain fractions and recovers hidden grain size sub-classes.
6.  **`remove_overlaps_transits.py`**
    *   Identifies and strips overlapping intervals from complex transiting grain fraction segments.
7.  **`mass_percentage_and_grain_sizes.py`**
    *   Maps clastic sediment records to a reference dictionary to extract standardized mass percentages and grain scale metrics.
8.  **`mass_error_type.py`**
    *   Evaluates total-mass imbalances across layer segments and assigns categorized troubleshooting error codes.
9.  **`mass_inconsistencies_fix.py`**
    *   Applies algorithmic re-balancing adjustments to completely resolve the flagged total-mass inconsistencies.
10. **`expanding_columns.py`**
    *   The final pipeline step. Flattens mass percentages into separate, distinct feature columns and exports the curated dataset to `corrected_borehole_data.csv`.

### Utilities & Outlier Filtering
*   **`extracting_boreholes_with_false_height.py`**
    *   An isolated data-cleaning utility that removes duplicate borehole profile IDs and drops non-physical boreholes with a log length of `0` meters.

---

## 📦 Requirements & Getting Started

### 1. Prerequisites
Ensure you have a functional connection to your institutional Oracle database server and that your credentials are saved in `config.py`.

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com
cd berlin-borehole-curator

# Install data engineering and connectivity libraries
pip install numpy pandas openpyxl cx_Oracle matplotlib seaborn
```

### 3. Pipeline Output
The successful execution of the final script (`expanding_columns.py`) generates:
*   📁 **`corrected_borehole_data.csv`** — The verified, golden dataset ready to feed downstream grain size distribution curves and numerical geological models.

---

## ⚠️ Internal Notice

🔒 **Confidentiality:** This repository contains proprietary research logic and workflow structures. It is intended strictly for **internal institutional use only**. Do not distribute, publish, or share code or associated data blocks externally without explicit written clearance from the project author or an authorized representative of the Technical University of Munich (TUM).
