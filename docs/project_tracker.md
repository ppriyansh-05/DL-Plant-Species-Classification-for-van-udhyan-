# Project Tracker: Van Udyan Deep Learning Plant Classification

**Project Title:** Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring  
**Organization:** Reform Social Welfare Foundation (RSWF), Pune – Van Udyan Biodiversity Monitoring  
**Last Updated:** 2026-10-19  

---

## 1. Status Overview

| Phase | Description | Status | Output / Artifacts |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Inspect Folder & Missing Inputs | **Completed** | Full inventory of `Zone Wise Plants.xlsx` & `Van_Udyan_iNaturalist_Licensed_Photo_Collector.ipynb` |
| **Phase 2** | Excel Extraction & Validation | **Completed** | 140 validated images, 1 quarantined row (`?`), `data/raw_excel/raw_excel_manifest.csv` |
| **Phase 3** | iNaturalist Licensed Photo Collection | **Completed** | 1,140 photos across 38 species (30/species), full CC licensing & GPS attribution metadata |
| **Phase 4** | Dataset Validation & Deduplication | **Completed** | 1,275 verified images (Pillow integrity, 5 duplicates dropped, 0 corrupt files) |
| **Phase 5** | Grouped Splitting (Train/Val/Test) | **Completed** | Grouped split: 876 Train / 204 Val / 195 Test + dedicated `test_van_udyan_benchmark/` (140) |
| **Phase 6** | Google Colab Training Notebook | **Completed (Ready)** | `Van_Udyan_Plant_Classification_Model_Training.ipynb` (MobileNetV2, Non-executed) |
| **Phase 7** | Documentation & Report Draft | **Completed** | Comprehensive README, dataset documentation, methodology, results template, academic draft |
| **Phase 8** | Non-Training Checks & Final Handoff | **Completed** | Packaged `data_processed.zip` (206 MB), Colab execution handoff instructions |

---

## 2. Issues, Anomalies & Mitigations

1. **Row 74 in Excel Workbook**:
   - *Issue*: Scientific name was entered as `?` with zone `Zone 2`.
   - *Action Taken*: Quarantined into `data/raw_excel/quarantine/` with a formal alert in the manifest. Dropped from training/test labels to prevent corrupting taxonomy.
2. **Local Van Udyan Class Imbalance**:
   - *Issue*: Van Udyan spreadsheet has only 1 image for 10 species (e.g. *Careya arborea*, *Dalbergia sissoo*, *Swietenia macrophylla*) and up to 18 images for *Azadirachta indica*.
   - *Action Taken*: Supplementary licensed iNaturalist collection targeting up to 30 images per species under permissive CC licenses (`cc0`, `cc-by`, `cc-by-nc`, `cc-by-sa`, `cc-by-nc-sa`).
3. **Data Leakage Prevention**:
   - *Issue*: Multiple photos taken of the same tree/specimen in an observation must not be split across train and test partitions.
   - *Action Taken*: Grouped splitting by `observation_id` ensures zero observation leakage across splits.
