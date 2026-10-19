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
| **Phase 3** | Prioritized iNaturalist Collection | **Completed** | 1,519 photos across 38 species (40/species), Pune/Maharashtra prioritized (380 local photos), full CC licenses & GPS metadata |
| **Phase 4** | Dataset Validation & Deduplication | **Completed** | 1,654 clean validated images on disk (Pillow verified, 6 duplicates dropped, 0 corrupt files) |
| **Phase 5** | Grouped Splitting (Train/Val/Test) | **Completed** | Strict leak-free split: 1,050 Train / 236 Val / 228 Test (all iNat) + 140 dedicated `test_van_udyan_benchmark/` (pure Excel field data) |
| **Phase 6** | Google Colab Training Notebook | **Completed (Ready for User)** | `Van_Udyan_Plant_Classification_Model_Training.ipynb` with startup hash isolation validation and MobileNetV2 |
| **Phase 7** | Packaging & Run Documentation | **Completed** | `van_udyan_cleaned_dataset.zip` (256.39 MB) and `docs/colab_run_guide.md` |
| **Phase 8** | Website & Deployment | **Ready for Next Stage** | Inference backend & frontend to be built following Colab model run |

---

## 2. Current Findings & Baselines

1. The initial 38-class baseline achieved **11.79% top-1 test accuracy** on 195 test images and **25.64% top-3 accuracy**. This was a preliminary baseline with only ~30 images per species.
2. The focused 8-class experiment achieved **30.30% test accuracy** on only 33 test images. The training log reported an input-ran-out-of-data warning due to mismatched manual step counts. In the updated pipeline, Keras data loaders now use automatic dataset batch progression (`steps_per_epoch=None`) to eliminate this warning.
3. Closed-set limitation: The classifier always chooses among its supported classes, even when an unrepresented plant is presented. The web app and evaluation pipeline include a low-confidence/unknown threshold notice to handle out-of-distribution inputs transparently.
4. Data leakage prevention: Final evaluation avoids same-observation leakage. All photos from the same observation or specimen are grouped atomically into a single partition, and held-out Van Udyan field photos are reported separately.

---

## 3. Next Actions

1. User executes `Van_Udyan_Plant_Classification_Model_Training.ipynb` in Google Colab on T4 GPU using `van_udyan_cleaned_dataset.zip`.
2. Save trained `best_van_udyan_mobilenetv2.keras`, `class_mapping.json`, confusion matrix, and classification report.
3. Record measured test metrics in `docs/experiment_results_template.md` and `docs/academic_report_draft.md`.
4. Proceed to web application development (FastAPI prediction backend + interactive frontend) for the professor demonstration.
