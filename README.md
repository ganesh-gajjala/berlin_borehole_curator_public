# Berlin Borehole Curator

An automated data engineering and data-cleaning pipeline written in Python to sanitize, harmonize, and validate the Berlin Borehole Database. This project rectifies structural inconsistencies, handles lithological classification errors, corrects geometry calculations, and resolves textual duplications across the dataset.

## 📋 Project Scope & Solved Anomalies

The geological records within the database contain systemic collection and legacy input errors. This suite of scripts automates the resolution of the following anomalies:

*   **Structural Data Remediation:** Detects and corrects missing stratigraphic intervals, invalid null fields, and data-entry gaps.
*   **Elevation & Depth Corrections:** Flags and mathematically recalculates incorrect borehole collar elevations, reference heights, and depth-log calculations.
*   **Lithological Harmonization:** Disentangles mixed clastic and non-clastic borehole sections into distinct, geologically accurate facies intervals.
*   **Textual De-duplication:** Sanitizes lithological logs by identifying and stripping repetitive text or redundant descriptions.

## 🛠️ Repository Architecture & Module Map

The codebase is split into modular scripts targeting specific validation pipelines:

```text
├── data_sanitizer.py          # Master cleaning script for missing logs and null fills
├── height_corrector.py        # Logic engine recalculating collar heights and depth bounds
├── litho_harmonizer.py        # Algorithmic separator for mixed clastic/non-clastic segments
└── text_deduplicator.py       # NLP-based processing to prune repeated layer descriptions
```

## 📦 Requirements & Getting Started

1. Clone your newly created repository:
   ```bash
   git clone https://github.com
   cd berlin-borehole-curator
   ```

2. Install the necessary analytical and processing libraries:
   ```bash
   pip install numpy pandas openpyxl
   ```

## 🚀 Execution Pattern

Each workflow step can be triggered sequentially to pass raw data sheets through the remediation pipeline:

```bash
# Step 1: Fix missing records and structural gaps
python data_sanitizer.py --input raw_data.csv

# Step 2: Validate and shift depth heights
python height_corrector.py --input sanitized_data.csv

# Step 3: Parse and split complex clastic/non-clastic intervals
python litho_harmonizer.py --input heights_corrected.csv
```


## ⚠️ Internal Notice

🔒 **Confidentiality:** This repository is intended strictly for **internal use only**. Do not distribute, publish, or share data/code blocks externally without explicit organizational clearance.
