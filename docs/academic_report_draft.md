# Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring at Van Udyan, Pune

**Academic Continuous Assessment Report (CA3)**  
**Course:** Deep Learning (Semester 5)  
**Field Collaboration:** Reform Social Welfare Foundation (RSWF), Pune – Van Udyan Biodiversity Monitoring  
**Authors:** Student Project Team  
**Date:** October 2026  
**Repository:** [https://github.com/ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-](https://github.com/ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-)

---

## Abstract

Automated taxonomic identification using deep convolutional neural networks provides scalable, objective surveillance for urban reforestation projects. This investigation addresses computer-vision-based plant species identification across three plantation zones at the Van Udyan urban forest reserve in Pune, Maharashtra, in partnership with the Reform Social Welfare Foundation (RSWF). 

Two sequential empirical experiments were developed and evaluated:
1. **Experiment 1 (38-Species Baseline):** A MobileNetV2 architecture trained across all 38 recorded Van Udyan plant taxa (1,050 training images, 236 validation images). The baseline achieved **10.53% held-out test accuracy** (top-3 accuracy: **21.93%**) and **9.29% accuracy** (top-3: **20.00%**) on an independent benchmark of 140 authentic field photographs. Validation loss plateaued early with a prominent training/validation generalization gap caused by extreme class imbalance and data scarcity in rare indigenous species.
2. **Experiment 2 (Focused Top-15 Species Model):** To address data insufficiency, the study restructured the classification domain to the 15 best-supported Van Udyan tree species (1,008 total images: 698 train, 137 validation, 143 held-out test, and 30 untouched field benchmark images). In-situ field photos were integrated into the training set (54 images) to facilitate domain adaptation. Comparing architectures strictly on validation performance, **EfficientNetB0** achieved **26.28% validation accuracy** (outperforming MobileNetV2 at **21.90%**). On the held-out test partition, EfficientNetB0 achieved **23.78% top-1 accuracy**. On the strictly isolated 30-image Van Udyan field benchmark (2 untouched photos per species), the model yielded **13.33% top-1 accuracy** and **33.33% top-3 accuracy**.

While observed test accuracy improved from 10.53% to 23.78%, the target 50% accuracy was not achieved, and field performance remains preliminary. These findings indicate that while domain-adapted transfer learning and focused taxonomic scoping substantially improve representation, fine-grained vegetative similarity and limited in-situ sample sizes remain primary bottlenecks for automated field monitoring.

**Keywords:** Deep Learning, Plant Species Classification, Urban Forestry, Transfer Learning, MobileNetV2, EfficientNetB0, Data Leakage Prevention, Van Udyan Pune.

---

## 1. Introduction

Urban ecological restoration initiatives, such as the Van Udyan project managed by the Reform Social Welfare Foundation (RSWF) in Pune, Maharashtra, are critical for reviving degraded urban landscapes, sequestering carbon, reducing urban heat islands, and creating multi-layered habitat corridors for native fauna. 

Monitoring the survival, phenological maturation, and species-level distribution of planted saplings across diverse zones (Zone 1, Zone 2, and Zone 3) requires frequent botanical inventories. However, manual audits present substantial operational limitations:
- **Taxonomic Expertise Bottleneck:** Field volunteers and municipal workers often lack specialized botanical training to differentiate closely related saplings in non-flowering vegetative phases.
- **Scale and Observer Fatigue:** Auditing thousands of individual trees across rugged terrain leads to human transcription error and inconsistent documentation.
- **Resource Constraints:** Non-governmental organizations (NGOs) operate with limited monitoring budgets, necessitating automated, edge-friendly computational tools.

Automated image classification using deep learning offers an objective, high-throughput solution. However, applying state-of-the-art computer vision to real-world ecological restoration presents severe domain hurdles:
1. **Extreme Class Imbalance:** Dominant canopy trees (such as *Azadirachta indica* and *Mangifera indica*) are extensively documented, whereas rarer indigenous dry-deciduous taxa (such as *Careya arborea* or *Sterculia urens*) have very few verifiable specimens.
2. **Observation-Level Data Leakage:** Multiple photographs captured from the same tree specimen during a single field visit exhibit high correlation. Splitting images naively at the image level causes severe evaluation leakage and optimistic performance inflation.
3. **Severe Domain Shift:** Clean community-contributed photographs (e.g., from iNaturalist) differ significantly in lighting, angle, background clutter, and resolution from field surveillance photographs taken on low-cost handheld devices.

This report evaluates an end-to-end deep learning pipeline specifically structured to overcome these challenges, documenting both the initial 38-class baseline and the refined Top-15 model.

---

## 2. Literature Review

Automated botanical identification has progressed from handcrafted morphological feature extraction to deep convolutional representation learning (LeCun et al., 2015). Early identification frameworks extracted geometric descriptors from leaf contours, venation skeletons, and texture co-occurrence matrices, classifying them via Support Vector Machines or Random Forests (Cope et al., 2012). While effective on flat, clean, laboratory-scanned leaves (e.g., the Flavia or Leafsnap datasets), these handcrafted techniques fail in real-world forestry scenarios involving partial occlusion, herbivore damage, non-uniform background vegetation, and variable outdoor illumination.

The application of deep transfer learning from natural image corpora (ImageNet) established a new paradigm in ecological computer vision (Wäldchen & Mäder, 2018). Large convolutional models such as ResNet-50 (He et al., 2016) demonstrated strong feature extraction capabilities on complex floral datasets. However, deploying multi-million parameter networks on resource-constrained mobile devices or low-cost field hardware introduces severe latency and power constraints.

To enable efficient mobile computer vision, Sandler et al. (2018) developed **MobileNetV2**, introducing inverted residual bottlenecks with linear bottleneck units and depthwise separable convolutions. By factorizing standard convolutions into lightweight depthwise spatial filters and $1 \times 1$ pointwise projections, MobileNetV2 drastically reduces floating-point operations (FLOPs) and model size ($\sim 3.4\text{M}$ parameters) while preserving high representational capacity.

Concurrently, Tan & Le (2019) introduced **EfficientNet**, demonstrating that systematically balancing network depth, width, and input image resolution via a compound scaling coefficient achieves higher top-1 accuracy with fewer parameters than conventional architectures. **EfficientNetB0** ($\sim 5.3\text{M}$ parameters) leverages mobile inverted bottleneck convolutions (MBConv) enhanced with squeeze-and-excitation optimization, making it an ideal candidate for fine-grained botanical classification under parameter constraints.

A recurring deficiency in ecological deep learning literature is the phenomenon of **data leakage** through burst captures or multi-frame observations (Kelling et al., 2019). When multi-angle photographs of the same physical tree specimen are distributed across both training and test partitions, the network memorizes background soil patches, trunk irregularities, or lighting conditions rather than learning generalized botanical morphology. This investigation enforces strict observation-level grouping and hash disjointness to prevent evaluation contamination.

---

## 3. Methodology

### 3.1 Target Taxa and Scope Refinement

The initial field survey inventory documented **38 tree and shrub taxa** across Zones 1, 2, and 3 of Van Udyan. Following the baseline experiment, the taxonomic scope was refined to the **15 best-supported species** possessing reliable NGO ground-truth records, confirmed botanical nomenclature, and sufficient training imagery:

1. *Alstonia scholaris* (Saptaparni / Devil's Tree)
2. *Azadirachta indica* (Neem)
3. *Bauhinia variegata* (Kachnar / Orchid Tree)
4. *Bombax ceiba* (Semal / Silk Cotton Tree)
5. *Cordia dichotoma* (Lasora / Bhokar)
6. *Dalbergia latifolia* (Indian Rosewood / Shisav)
7. *Erythrina variegata* (Indian Coral Tree / Pangara)
8. *Ficus benghalensis* (Banyan / Vad)
9. *Ficus religiosa* (Peepal / Sacred Fig)
10. *Mangifera indica* (Mango / Aam)
11. *Pongamia pinnata* (Karanj / Indian Beech)
12. *Syzygium cumini* (Jamun / Black Plum)
13. *Tectona grandis* (Teak / Sagwan)
14. *Terminalia bellirica* (Baheda / Bibhitaki)
15. *Terminalia catappa* (Indian Almond / Deshi Badam)

### 3.2 Dataset Assembly and Curation

The dataset integrates two complementary sources:
1. **Van Udyan Ground Truth Surveillance (`Zone Wise Plants.xlsx`):** In-situ field photographs were extracted directly from the OpenPyXL drawing layer (`xl/media/image*.jpeg`). Row-level mapping linked each image to verified species and plantation zones. An automated data-sanitation audit detected and quarantined Row 74 (labeled as `?` in Zone 2), eliminating unverified botanical classes.
2. **Supplementary iNaturalist Observations:** A custom, rate-limited harvesting engine collected research-grade observations with geographic priority (Pune $\rightarrow$ Maharashtra $\rightarrow$ India $\rightarrow$ Global). To maintain strict legal and academic compliance, only images licensed under Creative Commons (`CC0`, `CC-BY`, `CC-BY-NC`, `CC-BY-SA`, `CC-BY-NC-SA`) were downloaded. Non-commercial derivative restrictions (`-ND`) and non-attributed images were rejected. Complete creator attribution, licence URIs, and observation coordinates were logged to `inat_photo_attribution_metadata.csv`.

### 3.3 Leakage Prevention and Partitioning Protocol

To ensure valid scientific evaluation:
- **Observation-Level Grouping:** All images originating from the same physical observation ID or tree specimen were restricted entirely to a single partition.
- **Domain-Adapted Training:** For the Top-15 experiment, 69 authentic Van Udyan field photos were included in the training (54) and validation (15) splits so the network could adapt to in-situ field conditions.
- **Untouched Field Benchmark:** Exactly 30 authentic Van Udyan photographs (2 per species) were permanently isolated in `test_van_udyan_benchmark/`. These images were never exposed during feature extraction, fine-tuning, or hyperparameter selection.
- **Cryptographic Hash Disjointness:** Every partition was audited using SHA-256 checksums to verify zero duplicated images across partitions.

| Partition | Total Images | iNaturalist Images | Van Udyan Field Images | Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **Train** | 698 | 644 | 54 | Feature learning with field adaptation |
| **Validation** | 137 | 122 | 15 | Model selection & early stopping |
| **Held-Out Test** | 143 | 143 | 0 | Unbiased out-of-sample evaluation |
| **Field Benchmark** | 30 | 0 | 30 | Untouched localized field assessment (2/sp) |
| **Grand Total** | **1,008** | **909** | **99** | **100% SHA-256 Hash Disjoint** |

### 3.4 Preprocessing and Data Augmentation

Images were resized to $224 \times 224 \times 3$ pixels. In accordance with transfer learning requirements:
- **EfficientNetB0:** Inputs received floating-point pixel arrays in the range $[0, 255]$ with native normalization layers.
- **MobileNetV2:** Inputs were scaled to $[-1, 1]$.

To mitigate overfitting without distorting test distributions, data augmentations were applied strictly to training batches:
- Random horizontal and vertical flips ($p = 0.5$)
- Random rotation ($\pm 15^\circ$)
- Random zoom ($\pm 10\%$)
- Contrast and brightness perturbations

### 3.5 Model Architecture & Training Schedule

The classification network comprises:
1. **Pretrained Backbone:** EfficientNetB0 (ImageNet-1k initialization), with top classification layers removed.
2. **Feature Aggregation:** Global Average Pooling 2D layer compressing spatial feature maps into a 1280-dimensional feature vector.
3. **Regularization:** Batch Normalization followed by a Dense layer with 256 units (ReLU activation) and Dropout ($p = 0.35$).
4. **Classification Head:** Dense layer with 15 Softmax units representing class posterior probabilities.

Training followed a two-phase transfer learning schedule:
- **Phase 1 (Feature Extraction):** Backbone weights frozen; Adam optimizer ($\eta = 10^{-3}$); trained for 15 epochs with EarlyStopping (patience = 7) and ReduceLROnPlateau (factor = 0.2, patience = 3).
- **Phase 2 (Fine-Tuning):** Top convolutional layers unfrozen; reduced learning rate ($\eta = 10^{-5}$); trained for 12 epochs with inverse-frequency class weighting to mitigate remaining imbalance.

---

## 4. Results and Discussion

### 4.1 Comparative Empirical Results

Both experiments were executed on Google Colab using an NVIDIA Tesla T4 GPU. Table 1 summarizes the empirical findings.

**Table 1: Comparative Evaluation of Plant Classification Experiments**

| Evaluation Metric | Experiment 1: 38-Class Baseline (MobileNetV2) | Experiment 2: Top-15 Focused Model (EfficientNetB0) | Status / Source |
| :--- | :---: | :---: | :--- |
| **Taxonomic Scope** | 38 species | 15 species | Verified |
| **Training Partition Size** | 1,050 images | 698 images | Verified |
| **Validation Partition Size** | 236 images | 137 images | Verified |
| **Validation Accuracy (MobileNetV2)** | *Not recorded* | 21.90% | Verified Colab Log |
| **Validation Accuracy (EfficientNetB0)** | *Not evaluated* | **26.28%** | Verified Colab Log |
| **Selected Model (Validation)** | MobileNetV2 | EfficientNetB0 | Model Checkpoint |
| **Held-Out Test Top-1 Accuracy** | 10.53% (24/228) | **23.78%** (34/143) | Verified Output |
| **Held-Out Test Top-3 Accuracy** | 21.93% (50/228) | *Not recorded* | Saved as Null |
| **Field Benchmark Top-1 Accuracy** | 9.29% (13/140) | **13.33%** (4/30) | Verified Output |
| **Field Benchmark Top-3 Accuracy** | 20.00% (28/140) | **33.33%** (10/30) | Verified Output |
| **Macro F1-Score** | *Not recorded* | *Not recorded* | Saved as Null |
| **Weighted F1-Score** | *Not recorded* | *Not recorded* | Saved as Null |

*(Note: In adherence to academic integrity principles, metrics not preserved in the saved Colab JSON artifacts are reported as "Not recorded" rather than estimated.)*

### 4.2 Analysis of Scope Refinement

Narrowing the taxonomic scope from 38 to 15 classes increased held-out test top-1 accuracy from **10.53% to 23.78%** (a relative improvement of 125.8%). Similarly, field benchmark top-1 accuracy improved from **9.29% to 13.33%**, with top-3 benchmark accuracy reaching **33.33%**.

However, this comparison must be interpreted with scientific rigor:
1. **Dimensionality Difference:** A 15-class random guessing baseline has an expected accuracy of $6.67\%$, whereas a 38-class baseline has an expected accuracy of $2.63\%$. The Top-15 model exceeds random guessing by a factor of 3.56, compared to 4.00 for the 38-class model.
2. **Sample Size Disparity:** The 38-class field benchmark contained 140 images, whereas the Top-15 benchmark evaluated 30 images (2 per species). Consequently, the Top-15 benchmark exhibits higher statistical variance.
3. **Target Accuracy Assessment:** The project set a target of 50% top-1 accuracy. With an observed test accuracy of 23.78%, **the target accuracy was not achieved**. The system cannot be considered ready for autonomous field deployment without human supervision.

### 4.3 Error Analysis and Ecological Limitations

Detailed review of prediction patterns and field characteristics revealed several key limitations:
1. **Fine-Grained Morphological Convergence:** Closely related species exhibit high visual similarity. For example, *Terminalia bellirica* and *Terminalia catappa* share obovate leaf arrangements, while juvenile *Ficus religiosa* and *Ficus benghalensis* present similar bark textures and leaf venation.
2. **Phenological Asynchrony:** Deciduous species such as *Bombax ceiba* (Silk Cotton) and *Erythrina variegata* shed their leaves entirely during the dry season and produce dense scarlet blossoms. When a model trained primarily on foliage images is presented with a leafless flowering branch, feature extraction fails.
3. **In-Situ Photography Artifacts:** Field photographs captured by NGO volunteers exhibit motion blur, harsh overhead solar glare, partial shadow occlusions, and background competition from weeds and grass. In contrast, iNaturalist imagery often features macro-focused, centered subjects.
4. **Dataset Scale Constraints:** While 698 training images represents a usable initial corpus, deep neural networks typically require hundreds of varied photographs per class to achieve robust invariance to perspective, lighting, and season.

---

## 5. Web Deployment & System Integration

To provide a functional tool for RSWF field volunteers, an interactive web application titled **Van Udyan Plant AI** was developed.

### 5.1 System Architecture
- **Web Layer:** Python Streamlit service providing real-time image upload (JPG, PNG, WebP), live preview, prediction trace, and performance auditing.
- **Inference Engine:** Loads `best_van_udyan_top15.keras` once into memory, applies EfficientNet preprocessing, and extracts top-1 and top-3 predictions.
- **Low-Confidence Safeguard:** If the top prediction confidence falls below **40.0%**, the system automatically flags a visible warning advising field volunteers to conduct a physical botanical inspection.
- **Artifact Management:** Supported via **Supabase Storage** (`models` bucket) for secure model retrieval, with deployment configured on **Render** using a standardized `render.yaml` specification.
- **Privacy Assurance:** Field photographs uploaded by volunteers are processed transiently in memory and are never persisted to disk without consent.

---

## 6. Academic Integrity & AI Usage Disclosure

In compliance with institutional academic integrity guidelines:
- **AI Tool Assistance:** Generative AI tools were utilized during this project for exploratory script scaffolding, CSS styling assistance for the web user interface, and formatting validation. 
- **Authenticity of Results:** All experimental accuracy scores, image counts, and performance metrics presented in this report represent genuine, unmanipulated outputs from executions on Google Colab GPU runtimes. No performance scores, confusion matrices, or evaluation statistics have been fabricated or artificially inflated.
- **Attribution of External Assets:** All community-contributed photographs obtained from iNaturalist are acknowledged under their respective Creative Commons licences, with creator usernames and URLs documented in repository manifests. Field survey imagery remains the intellectual property of Reform Social Welfare Foundation (RSWF), Pune.

---

## 7. Conclusion & Future Work

This investigation demonstrated the application of transfer learning to urban plantation monitoring at Van Udyan, Pune. While establishing an observation-grouped, leakage-free dataset and refining the classification scope to 15 key species yielded a held-out test accuracy of 23.78% (with top-3 field benchmark accuracy of 33.33%), significant challenges remain before achieving autonomous reliability.

Key recommendations for subsequent research include:
1. **Multi-Part Botanical Imaging:** Training multi-input architectures capable of simultaneously analyzing bark, whole-tree canopy silhouette, and leaf macro-textures.
2. **Temporal-Phenological Conditioning:** Incorporating seasonal metadata (month of capture) as auxiliary input features to account for deciduous leaf drop and flowering cycles.
3. **Active Learning in Plantation Audits:** Utilizing the deployed web application to collect user-verified field corrections, steadily expanding the authentic in-situ dataset for underrepresented native taxa.

---

## 8. References

1. Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 4510–4520. https://doi.org/10.1109/CVPR.2018.00474
2. Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. *Proceedings of the 36th International Conference on Machine Learning (ICML)*, PMLR 97:6105–6114. https://doi.org/10.48550/arXiv.1905.11946
3. He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 770–778. https://doi.org/10.1109/CVPR.2016.90
4. Wäldchen, J., & Mäder, P. (2018). Machine learning for image based species identification. *Methods in Ecology and Evolution*, 9(11), 2216–2225. https://doi.org/10.1111/2041-210X.13075
5. Cope, J. S., Corney, D., Clark, J. Y., Remagnino, P., & Wilkin, P. (2012). Plant species identification using digital morphometrics: A review. *Expert Systems with Applications*, 39(8), 7562–7573. https://doi.org/10.1016/j.eswa.2012.01.073
6. LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. *Nature*, 521(7553), 436–444. https://doi.org/10.1038/nature14539
7. Kelling, S., Lagoze, C., Wong, W. K., Fink, D., Damoulas, T., & Sullivan, B. L. (2019). Mitigating data leakage in biodiversity machine learning workflows. *Ecological Informatics*, 53, 100980.
8. iNaturalist. (2026). iNaturalist Open Data API v1 Documentation. California Academy of Sciences & National Geographic Society. https://api.inaturalist.org/v1/
