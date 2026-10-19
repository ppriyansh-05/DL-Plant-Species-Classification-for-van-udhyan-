# Google Colab Step-by-Step Training Guide

**Notebook Filename:** `Van_Udyan_Plant_Classification_Model_Training.ipynb`  
**Dataset Archive:** `van_udyan_cleaned_dataset.zip` (257.44 MB)  
**Target Architecture:** Transfer Learning with MobileNetV2 (Pretrained on ImageNet-1k)  
**Number of Classes:** 38 Classes  
**Total Images:** 1,654 (1,150 Train / 264 Val / 240 Test + 140 Van Udyan Benchmark)  

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

### Method A: Upload the Cleaned ZIP (Fastest & Simplest)
1. On the left sidebar in Colab, click the **Folder icon** (`Files`).
2. Click the **Upload** icon and select `van_udyan_cleaned_dataset.zip` from your computer:
   `c:\Users\ppriy\OneDrive\Desktop\semester 5\DL PROJECT - SPECIES IDENTIFICATION\van_udyan_cleaned_dataset.zip`
3. In Cell 2 of the notebook, keep `USE_GOOGLE_DRIVE = False`.

### Method B: Using Google Drive (Optional)
If you upload `van_udyan_cleaned_dataset.zip` to your personal Google Drive:
1. Set `USE_GOOGLE_DRIVE = True` in Cell 2.
2. Set `DRIVE_ZIP_PATH = "/content/drive/MyDrive/van_udyan_cleaned_dataset.zip"`.
3. Follow the authentication prompt when Cell 2 mounts Google Drive.

> **Note on NGO Photos Drive Folder**:
> If the NGO Google Drive folder (`https://drive.google.com/drive/folders/1lYT2GITixXzw1rp8lGRkQqc5vyenDH8E`) is private, you can add a shortcut of that folder to your personal Drive (`Add shortcut to Drive`), mount your Drive via Cell 2, and access images directly at `/content/drive/MyDrive/<shortcut_name>`.

---

## Step 4: Run Training
1. In the top menu, select **Runtime -> Run all** (`Ctrl+F9`).
2. The notebook will automatically:
   - Check GPU and unpack the dataset.
   - Verify all 38 classes and show image counts.
   - Compute balanced class weights to neutralize class imbalance.
   - Train Stage 1 (Feature extraction with frozen MobileNetV2 backbone, Adam $\text{lr}=10^{-3}$, callbacks).
   - Train Stage 2 (Fine-tuning top residual blocks, Adam $\text{lr}=10^{-5}$).
   - Evaluate held-out test split (Accuracy, Top-3 Accuracy, Macro/Weighted F1).
   - Evaluate dedicated pure in-situ Van Udyan benchmark photos.
   - Generate and display `confusion_matrix.png` and `evaluation_classification_report.txt`.
   - Export `best_van_udyan_mobilenetv2.keras` and `class_mapping.json`.

---

## Step 5: Post-Training Results Update
Once training finishes in Colab:
1. Download `evaluation_classification_report.txt`, `confusion_matrix.png`, and `best_van_udyan_mobilenetv2.keras`.
2. Record the test accuracy and F1 metrics into `docs/experiment_results_template.md`.
3. Use the trained `.keras` model weights for the Van Udyan Plant AI website demo.
