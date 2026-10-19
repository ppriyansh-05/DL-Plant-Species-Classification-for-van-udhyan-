# Experiment Results Template

> **Note**: As per instructions, model training and evaluation are executed by the user on Google Colab. This document serves as the standardized placeholder template to record experimental metrics once Colab execution is completed.

---

## 1. Overall Performance Metrics (Held-out Test Split)

| Model Configuration | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Inference Latency (ms/img) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| MobileNetV2 (Feature Extractor) | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* |
| MobileNetV2 (Fine-Tuned) | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* | *[Colab Result]* |

---

## 2. Dedicated Van Udyan Local Field Benchmark Evaluation

| Target Species (Van Udyan Test Images) | Support (N) | Correct Predictions | Per-Class Recall | Notes / Field Conditions |
| :--- | :---: | :---: | :---: | :--- |
| *Aegle marmelos* | *[N]* | *[ ]* | *[ ]%* | Foliage / bark |
| *Azadirachta indica* | *[N]* | *[ ]* | *[ ]%* | Canopy view |
| *Bombax ceiba* | *[N]* | *[ ]* | *[ ]%* | Trunk / thorn features |
| *Careya arborea* | *[N]* | *[ ]* | *[ ]%* | Single field specimen |
| *Mangifera indica* | *[N]* | *[ ]* | *[ ]%* | Mature tree |
| *Pongamia pinnata* | *[N]* | *[ ]* | *[ ]%* | Dense canopy |
| *(Remaining 32 species...)* | *[N]* | *[ ]* | *[ ]%* | ... |

---

## 3. Confusion Matrix and Error Observations

- **Most Frequent Misclassifications**:
  1. *[Class A]* misclassified as *[Class B]*: *[Reason/visual similarity]*
  2. *[Class C]* misclassified as *[Class D]*: *[Reason/visual similarity]*
- **Key Error Factors**:
  - Distance/scale variation in field photography.
  - Background clutter (soil, fencing, overlapping weed foliage).
  - Lighting conditions (shadows vs. direct midday sunlight).
