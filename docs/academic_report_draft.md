# Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring

**Project Report Draft**  
**Course:** Deep Learning Project (Semester 5)  
**Field Collaboration:** Reform Social Welfare Foundation (RSWF), Pune – Van Udyan Biodiversity Monitoring  
**Authors:** Student Project Team  
**Date:** October 2026  

---

## Abstract

Urban plantation monitoring requires scalable, precise, and continuous taxonomic identification to assess biodiversity recovery, sapling survival, and canopy health. This project develops an automated deep learning framework for classifying **38 plant and tree species** across three distinct planting zones in the Van Udyan urban forest reserve in Pune, Maharashtra. The dataset comprises local in-situ field imagery from field surveillance and supplementary Creative Commons-licensed observations harvested from the iNaturalist platform. 

To address severe class imbalance present in raw field surveys and avoid data leakage across multiple photographs of identical specimens, a **grouped stratified splitting strategy** by observation identifier is established. A **MobileNetV2** deep convolutional neural network architecture with inverted residual bottlenecks and depthwise separable convolutions is utilized via transfer learning, designed for edge computing and mobile field monitoring. The training methodology, evaluation protocol, confusion matrix diagnostics, and baseline results template are formalized for reproducible execution on Google Colab.

**Keywords:** Deep Learning, Plant Species Classification, Urban Forestry, Transfer Learning, MobileNetV2, Data Leakage Prevention, Biodiversity Monitoring.

---

## 1. Introduction

Urban forestry initiatives provide essential ecosystem services, including microclimate stabilization, carbon sequestration, stormwater mitigation, and habitat restoration. The Van Udyan project, spearheaded by the Reform Social Welfare Foundation (RSWF) in Pune, represents an intensive ecological restoration endeavor across multiple designated zones.

Manual botanical auditing in large-scale plantations is labor-intensive, requires expert taxonomic knowledge, and is prone to human transcription errors. Automated image-based plant species identification using deep learning presents an effective solution for automated tree inventorying and continuous ecological surveillance.

Key technical challenges addressed in this work include:
1. **Severe Class Imbalance**: Dominant canopy trees (such as *Azadirachta indica* and *Mangifera indica*) possess numerous observations, whereas rarer native species (such as *Careya arborea* and *Sterculia urens*) possess sparse field samples.
2. **Data Leakage in Field Photography**: Burst captures or multi-angle photos of the same physical tree specimen risk inflating validation metrics if distributed across both training and testing sets.
3. **Field Generalizability**: Reconciling heterogeneous lighting, occlusions, and background clutter characteristic of in-situ field imagery.

---

## 2. Literature Review

Convolutional Neural Networks (CNNs) have revolutionized computer vision in biological classification (LeCun et al., 2015). Early automated botanical classification systems relied on handcrafted morphological descriptors (e.g., leaf vein patterns, leaf margins, and shape contours) classified via Support Vector Machines or Random Forests (Cope et al., 2012). However, such models deteriorate under natural field conditions where foliage is partially occluded, pest-damaged, or photographed against complex soil backgrounds.

Transfer learning from large-scale natural image corpora (ImageNet) has emerged as the standard paradigm for biological vision tasks (Wäldchen & Mäder, 2018). Models such as ResNet (He et al., 2016) and DenseNet (Huang et al., 2017) demonstrate high accuracy but incur substantial computational overhead and parameter counts ($>25\text{M}$ parameters), hindering low-power mobile deployment.

To address computational constraints in field-based ecological monitoring, Sandler et al. (2018) introduced **MobileNetV2**, which utilizes inverted residual blocks with linear bottlenecks and depthwise separable convolutions. MobileNetV2 drastically reduces floating-point operations (FLOPs) and parameter footprint ($\sim 3.4\text{M}$ parameters) while maintaining competitive feature discriminability. This makes it particularly suited for offline field inference on low-cost smartphones deployed by forestry volunteers.

---

## 3. Methodology

### 3.1 Target Species Taxonomy
The classification taxonomy comprises 38 indigenous and planted species identified across Van Udyan Zones 1, 2, and 3, including *Aegle marmelos*, *Bombax ceiba*, *Butea monosperma*, *Careya arborea*, *Dalbergia latifolia*, *Ficus benghalensis*, *Ficus religiosa*, *Madhuca longifolia*, *Pongamia pinnata*, and *Terminalia arjuna*.

### 3.2 Dataset Acquisition and Curation
1. **Van Udyan Ground Truth**: 141 in-situ photos were extracted from the field survey workbook (`Zone Wise Plants.xlsx`) via OpenPyXL drawing anchor extraction. An anomaly detection pass quarantined Row 74 (labeled as `?` in Zone 2) to maintain strict label hygiene.
2. **Supplementary iNaturalist Collection**: An automated, rate-limited query engine harvested high-resolution, peer-verified observations filtered exclusively under permissive Creative Commons licences (`CC0`, `CC-BY`, `CC-BY-NC`, `CC-BY-SA`, `CC-BY-NC-SA`). Images with NoDerivatives (`-ND`) licences or missing attribution were strictly rejected.

### 3.3 Data Leakage Prevention and Grouped Splitting
To avoid artificial performance inflation, all images originating from the same physical observation or tree specimen share a unique `group_id`. Group-aware partitioning divides the data into:
- **Training Set (70%)**
- **Validation Set (15%)**
- **Held-Out Test Set (15%)**
- **Dedicated Van Udyan Local Benchmark**: An independent test suite comprised exclusively of authentic Van Udyan field photographs to evaluate localized domain adaptation.

### 3.4 Image Preprocessing & Augmentation
All images are verified using Pillow, stripped of corrupted bytes, and resized to $224 \times 224$ pixels. Input pixels are rescaled to the $[-1, 1]$ interval compatible with MobileNetV2. To combat overfitting during training, stochastic data augmentations are applied strictly to the training split:
- Random horizontal and vertical flips
- Random rotation ($\pm 15^\circ$)
- Random zoom ($\pm 10\%$)
- Contrast and brightness jitter

### 3.5 Model Architecture
The network consists of:
1. **Base Backbone**: MobileNetV2 pretrained on ImageNet-1k (feature extractor).
2. **Global Average Pooling**: Compresses spatial feature maps into a 1280-dimensional feature vector.
3. **Regularization**: Batch Normalization followed by a Dense layer with 256 ReLU units and Dropout ($p = 0.40$).
4. **Output Layer**: Dense classification layer with 38 Softmax outputs representing class posterior probabilities.

```text
[Input 224x224x3] -> [Data Augmentation] -> [MobileNetV2 Base (Frozen/Fine-Tuned)]
                  -> [GlobalAveragePooling2D] -> [BatchNorm] -> [Dense 256, ReLU]
                  -> [Dropout 0.4] -> [Dense 38, Softmax]
```

### 3.6 Training Protocol
The model is trained using the **Categorical Crossentropy** loss and **Adam optimizer**:
- **Phase 1 (Feature Extraction)**: Base weights frozen; initial learning rate $\eta = 10^{-3}$; trained for 15 epochs with EarlyStopping (patience = 5) and ReduceLROnPlateau.
- **Phase 2 (Fine-Tuning)**: Top 30 convolutional layers unfrozen; reduced learning rate $\eta = 10^{-5}$; trained for 10 epochs.

---

## 4. Results and Discussion

*(Note: Model training and evaluation are conducted on Google Colab by the user. The tables and sections below outline the evaluation framework and metric definitions.)*

### 4.1 Quantitative Performance Metrics

| Evaluation Set | Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| Overall Test Split (Combined) | *[Colab Output]* | *[Colab Output]* | *[Colab Output]* | *[Colab Output]* |
| Van Udyan Local Field Benchmark | *[Colab Output]* | *[Colab Output]* | *[Colab Output]* | *[Colab Output]* |

### 4.2 Confusion Matrix Diagnostics
The multi-class confusion matrix highlights visual discrimination boundaries among confusable taxa (e.g., distinguishing *Dalbergia sissoo* from *Dalbergia latifolia*, or *Bauhinia racemosa* from *Bauhinia variegata* based on leaf lobing and venation).

### 4.3 Error Analysis and Ecological Limitations
1. **Phenological Variability**: Deciduous species (such as *Bombax ceiba* and *Butea monosperma*) exhibit stark visual divergence between dry flowering phases and vegetative leafing phases.
2. **Resolution Artifacts**: Embedded spreadsheet photos have lower native resolutions ($\sim 100 \times 160$ px) compared to high-resolution iNaturalist observations.

---

## 5. Conclusion

This study establishes a rigorous, leakage-free deep learning classification framework tailored to urban plantation biodiversity monitoring at Van Udyan, Pune. By uniting verified field surveillance data with ethically licensed iNaturalist observations and implementing group-aware partitioning, the pipeline prevents common evaluation pitfalls. The MobileNetV2 architecture balances parameter efficiency with discriminative power, offering a viable blueprint for edge-assisted urban ecological auditing.

---

## 6. References

1. Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 4510-4520.
2. He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 770-778.
3. Wäldchen, J., & Mäder, P. (2018). Machine learning for image based species identification. *Methods in Ecology and Evolution*, 9(11), 2216-2225.
4. Cope, J. S., Corney, D., Clark, J. Y., Remagnino, P., & Wilkin, P. (2012). Plant species identification using digital morphometrics: A review. *Expert Systems with Applications*, 39(8), 7562-7573.
5. LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. *Nature*, 521(7553), 436-444.
6. iNaturalist. (2026). iNaturalist Open Data API Documentation. Available: https://api.inaturalist.org/v1/
