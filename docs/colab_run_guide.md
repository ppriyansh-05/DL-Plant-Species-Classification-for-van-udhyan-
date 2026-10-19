# Google Colab Step-by-Step Training Guide

**Notebook Filename:** `Van_Udyan_Plant_Classification_Model_Training.ipynb`  
**Dataset Archive:** `van_udyan_cleaned_dataset.zip` (256.39 MB)  
**Target Architecture:** Transfer Learning with MobileNetV2 (Pretrained on ImageNet-1k)  
**Number of Classes:** 38 Classes  
**Total Images:** 1,654 (1,050 Train / 236 Val / 228 Test + 140 Independent Van Udyan Benchmark)  

---

## Partition Architecture & Zero Data Leakage
- **Train (1,050 images)**: iNaturalist photos across 38 species.
- **Val (236 images)**: iNaturalist photos across 38 species for early stopping and validation loss monitoring.
- **Test (228 images)**: Held-out iNaturalist evaluation split.
- **Dedicated Local Benchmark (140 images)**: Authentic in-situ Van Udyan field photos from `Zone Wise Plants.xlsx`. **Kept completely independent** — zero images in train, val, or regular test. Evaluated strictly post-training to measure real-world field domain adaptation.

---

## Step 1: Open Notebook in Google Colab
1. Navigate to [Google Colab](https://colab.research.google.com/).
2. Select **Upload** and upload `Van_Udyan_Plant_Classification_Model_Training.ipynb` from this project folder.

---

## Step 2: Configure GPU Accelerator
1. In the top navigation menu, go to **Runtime -> Change runtime type**.
2. Under **Hardware accelerator**, select **T4 GPU** (Standard free GPU).
3. Click **Save**.

---

## Step 3: Provide Dataset to Colab
1. On the left sidebar in Colab, click the **Folder icon (`Files`)**.
2. Drag and drop `van_udyan_cleaned_dataset.zip` from your computer into `/content/`:
   `c:\Users\ppriy\OneDrive\Desktop\semester 5\DL PROJECT - SPECIES IDENTIFICATION\van_udyan_cleaned_dataset.zip`

---

## Step 4: Run Training
1. In the top menu, select **Runtime -> Run all** (`Ctrl+F9`).
2. The notebook will automatically:
   - Check GPU and unpack the dataset.
   - Run **Strict Startup Validation**: verifies all 38 class mappings, directory file counts, and executes SHA-256 hash isolation checks to prove 0 cross-partition leakage. (Aborts with a clear error if any mismatch is found).
   - Compute balanced class weights to neutralize class imbalance.
   - Train Stage 1 (Feature extraction with frozen MobileNetV2 backbone, Adam $\text{lr}=10^{-3}$, early stopping).
   - Train Stage 2 (Fine-tuning top residual blocks, Adam $\text{lr}=10^{-5}$).
   - Evaluate held-out test split (Accuracy, Top-3 Accuracy, Macro/Weighted F1).
   - Evaluate dedicated independent in-situ Van Udyan benchmark photos.
   - Generate and display `confusion_matrix.png` and `evaluation_classification_report.txt`.
   - Export `best_van_udyan_mobilenetv2.keras` and `class_mapping.json`.

---

## Step 5: Post-Training Results Update
Once training finishes in Colab:
1. Download `evaluation_classification_report.txt`, `confusion_matrix.png`, and `best_van_udyan_mobilenetv2.keras`.
2. Record the test accuracy and F1 metrics into `docs/experiment_results_template.md`.
3. Use the trained `.keras` model weights for the Van Udyan Plant AI website demo.
