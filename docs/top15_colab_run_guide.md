# Google Colab Step-by-Step Training Guide: Top-15 Van Udyan Model

**Notebook Filename:** `Van_Udyan_Top15_Plant_Classification_Model_Training.ipynb`  
**Dataset Archive:** `van_udyan_top15_cleaned_dataset.zip` (152.59 MB)  
**Target Classes:** 15 Best-Supported Van Udyan Species  
**Total Images:** 1,008 Images (698 Train / 137 Val / 143 Test + 30 Independent Untouched Field Benchmark)  

---

## 1. Selected Top-15 Species & Image Counts

| No. | Scientific Name | Common Name | Excel Photos | iNaturalist Photos | Train | Val | Test | Untouched Benchmark | Total |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | *Azadirachta indica* | Neem | 18 | 70 | 66 | 10 | 10 | 2 | **88** |
| 2 | *Mangifera indica* | Mango | 12 | 60 | 47 | 13 | 10 | 2 | **72** |
| 3 | *Pongamia pinnata* | Karanj | 11 | 60 | 46 | 11 | 12 | 2 | **71** |
| 4 | *Bombax ceiba* | Semal / Silk Cotton | 10 | 60 | 47 | 6 | 15 | 2 | **70** |
| 5 | *Syzygium cumini* | Jamun | 6 | 60 | 44 | 10 | 10 | 2 | **66** |
| 6 | *Alstonia scholaris* | Saptaparni | 5 | 60 | 47 | 9 | 7 | 2 | **65** |
| 7 | *Terminalia bellirica* | Baheda | 5 | 60 | 42 | 8 | 13 | 2 | **65** |
| 8 | *Terminalia catappa* | Indian Almond | 5 | 60 | 40 | 16 | 7 | 2 | **65** |
| 9 | *Bauhinia variegata* | Kachnar | 4 | 60 | 46 | 7 | 9 | 2 | **64** |
| 10 | *Cordia dichotoma* | Lasora | 4 | 60 | 48 | 9 | 5 | 2 | **64** |
| 11 | *Dalbergia latifolia* | Shisham | 4 | 60 | 44 | 6 | 12 | 2 | **64** |
| 12 | *Erythrina variegata* | Coral Tree | 4 | 60 | 41 | 11 | 10 | 2 | **64** |
| 13 | *Ficus religiosa* | Peepal | 4 | 60 | 44 | 9 | 8 | 2 | **63** |
| 14 | *Tectona grandis* | Teak | 4 | 60 | 50 | 6 | 6 | 2 | **64** |
| 15 | *Ficus benghalensis* | Banyan | 3 | 60 | 46 | 6 | 9 | 2 | **63** |
| **Total** | **All 15 Species** | — | **99** | **909** | **698** | **137** | **143** | **30** | **1,008** |

---

## 2. Partition Strategy: Real-World Learning & Independent Benchmarking
- **Field Photo Inclusion**: 69 of the 99 Van Udyan Excel field photos are distributed across the training (54) and validation (15) splits so the network learns from actual local lighting, soil backgrounds, and plant stages.
- **Untouched Benchmark**: Exactly 2 authentic Van Udyan field photos per species (30 total) are reserved in `test_van_udyan_benchmark/`. These images are **never seen** during training, hyperparameter tuning, or model selection.
- **Strict Hash Disjointness**: All 4 partition directories have 0 overlapping SHA-256 hashes.

---

## 3. Step-by-Step Google Colab Execution Instructions

1. **Open Colab**: Navigate to [https://colab.research.google.com/](https://colab.research.google.com/) and click **Upload Notebook**.
2. **Select Notebook**: Upload `Van_Udyan_Top15_Plant_Classification_Model_Training.ipynb` from your project folder.
3. **Configure Hardware Accelerator**:
   - Go to **Runtime -> Change runtime type**.
   - Under **Hardware accelerator**, select **T4 GPU** and click **Save**.
4. **Upload Dataset Archive**:
   - Click the **Files (Folder)** icon on Colab's left sidebar.
   - Drag and drop `van_udyan_top15_cleaned_dataset.zip` (152.59 MB) into `/content/`.
5. **Run All Cells**:
   - Click **Runtime -> Run all** (`Ctrl+F9`).
   - The notebook will:
     - Verify GPU and extract the archive.
     - Validate that all 15 classes exist across splits and execute the SHA-256 disjointness test (aborts if any overlap or missing classes are detected).
     - Calculate balanced class weights.
     - Train MobileNetV2 (Stage 1 Feature Extractor + Stage 2 Fine-Tuning).
     - Train EfficientNetB0 for comparison and automatically select the best model based on validation loss.
     - Evaluate the held-out test split and the untouched Van Udyan benchmark.
     - Save `best_van_udyan_top15.keras`, `class_mapping.json`, `confusion_matrix.png`, and `evaluation_summary.json`.
