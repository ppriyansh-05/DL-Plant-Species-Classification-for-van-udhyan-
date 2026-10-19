# Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: Creative Commons](https://img.shields.io/badge/License-CC_BY--NC-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Institution: RSWF Pune](https://img.shields.io/badge/Partner-RSWF_Pune-green.svg)](https://www.rswf.org/)

## 1. Project Overview

This repository contains the complete dataset preparation, extraction, quality validation, and deep learning model workflow for **"Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring"**, supporting the **Van Udyan urban biodiversity monitoring initiative** with **Reform Social Welfare Foundation (RSWF), Pune**.

The system is configured to recognize **38 target tree and plant species** across three distinct plantation zones (Zone 1, Zone 2, Zone 3) using transfer learning with **MobileNetV2**.

---

## 2. Directory Structure

```text
├── Zone Wise Plants.xlsx                               # Source Excel workbook with embedded in-situ field photos
├── Van_Udyan_iNaturalist_Licensed_Photo_Collector.ipynb # iNaturalist licensed photo collection Colab notebook
├── Van_Udyan_Plant_Classification_Model_Training.ipynb  # Google Colab transfer learning training notebook
├── requirements.txt                                    # Python dependencies
├── scripts/
│   ├── extract_excel_images.py                         # OpenPyXL extractor & label/quarantine validator
│   ├── inaturalist_collector.py                        # Standalone CC-licensed iNaturalist API collector
│   └── prepare_dataset.py                              # Dataset validation, deduplication & grouped split
├── data/
│   ├── raw_excel/                                      # Extracted Van Udyan field photos & manifest
│   │   ├── images/<species_name>/
│   │   ├── quarantine/                                 # Isolated invalid/corrupt rows (e.g. Row 74 '?')
│   │   └── raw_excel_manifest.csv
│   ├── raw_inaturalist/                                # Supplementary licensed iNaturalist observations
│   │   ├── images/<species_name>/
│   │   ├── inat_photo_attribution_metadata.csv         # Full legal attribution & observation records
│   │   └── collection_summary.csv
│   └── processed/                                      # Cleaned, split dataset ready for training
│       ├── train/
│       ├── val/
│       ├── test/
│       ├── test_van_udyan_benchmark/                   # Dedicated pure Van Udyan field test set
│       ├── master_dataset_manifest.csv
│       └── species_split_summary.csv
└── docs/
    ├── project_tracker.md                              # Progress tracking & phase audit
    ├── dataset_documentation.md                        # Dataset sources, taxonomy & leakage prevention
    ├── data_collection.md                              # API querying, polite throttling & CC licensing
    ├── model_methodology.md                            # MobileNetV2 architecture & training protocol
    ├── experiment_results_template.md                  # Standardized performance tables for Colab
    └── academic_report_draft.md                        # Academic DL paper draft
```

---

## 3. Quick Start & Execution Guide

### Step 1: Environment Setup
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Extract & Validate Excel Field Images
```bash
python scripts/extract_excel_images.py
```
- Extracts 141 embedded images from `Zone Wise Plants.xlsx`.
- Automatically maps each image to its row label (`Scientific Name`) and `Zone`.
- Quarantines Row 74 (`?`, Zone 2) to maintain strict taxonomic integrity.

### Step 3: Run / Supplement iNaturalist Collection
Either run in Google Colab using `Van_Udyan_iNaturalist_Licensed_Photo_Collector.ipynb` or via CLI:
```bash
python scripts/inaturalist_collector.py --max 30
```
- Respects 1.1s API rate limits and exponential backoff on HTTP 429.
- Enforces CC0, CC-BY, CC-BY-NC, CC-BY-SA, CC-BY-NC-SA licences.
- Logs complete photo-level attribution and GPS coordinates.

### Step 4: Validate, Deduplicate, and Generate Grouped Splits
```bash
python scripts/prepare_dataset.py
```
- Performs **grouped splitting** by `observation_id` across the 1,514 validated iNaturalist photos: **1,050 Train**, **236 Val**, and **228 Test** images across all 38 classes.
- Keeps all **140 authentic Van Udyan field photos** strictly and exclusively in `test_van_udyan_benchmark/` to ensure zero cross-partition leakage.

### Step 5: Dedicated Top-15 Species Fast-Track Pipeline
```bash
python scripts/prepare_top15_dataset.py
```
- Filters exclusively for the **15 best-supported Van Udyan species** in NGO records (*Azadirachta indica*, *Mangifera indica*, *Pongamia pinnata*, *Bombax ceiba*, *Syzygium cumini*, *Alstonia scholaris*, *Terminalia bellirica*, *Terminalia catappa*, *Bauhinia variegata*, *Cordia dichotoma*, *Dalbergia latifolia*, *Erythrina variegata*, *Ficus religiosa*, *Tectona grandis*, *Ficus benghalensis*).
- Integrates 69 authentic Van Udyan field photos into the training (54) and validation (15) splits so the model learns real-world in-situ field conditions.
- Preserves a strictly untouched independent benchmark of **30 field photos** (2 per species) in `test_van_udyan_benchmark/`.
- Packaged into `van_udyan_top15_cleaned_dataset.zip` (152.59 MB, 1,008 images total).
- Dedicated Colab Notebook: `Van_Udyan_Top15_Plant_Classification_Model_Training.ipynb` (MobileNetV2 vs. EfficientNetB0 comparison).

### Step 6: Model Training on Google Colab (User Handoff)
1. Upload `data/processed/` (or archive `processed.zip`) to Google Drive or Colab session.
2. Open `Van_Udyan_Plant_Classification_Model_Training.ipynb` in Google Colab.
3. Select GPU Runtime (`Runtime` → `Change runtime type` → `T4 GPU`).
4. Execute cells sequentially to train MobileNetV2, generate confusion matrices, and evaluate test metrics.

---

## 4. Citation and Attribution

- **Field Photography & Ground Truth**: Reform Social Welfare Foundation (RSWF), Pune – Van Udyan Biodiversity Monitoring Team.
- **Supplementary Imagery**: iNaturalist community members under specified Creative Commons licences. Attribution metadata is preserved in `data/raw_inaturalist/inat_photo_attribution_metadata.csv`.
