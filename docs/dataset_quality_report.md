# Dataset Quality Report: Van Udyan Plant Species Classification

**Date:** 2026-10-19  
**Total Images Analyzed:** 1,280  
**Validated Clean Images:** 1,275  
**Quarantined / Dropped:** 1 quarantined label (`?`), 5 exact duplicate images dropped  
**Target Classes Represented:** 38 / 38 (100% coverage)  

---

## 1. Source Breakdown and Summary

| Source Stream | Raw Images | Validated Images | Quarantined / Dropped | Attribution & Licences |
| :--- | :---: | :---: | :---: | :--- |
| **Van Udyan Excel (`Zone Wise Plants.xlsx`)** | 141 | 140 | 1 (Row 74: `?` unknown label) | In-situ field photos from RSWF Pune |
| **iNaturalist API (`raw_inaturalist`)** | 1,140 | 1,135 | 5 (SHA-256 exact duplicates) | CC0, CC-BY, CC-BY-NC, CC-BY-SA, CC-BY-NC-SA |
| **Total** | **1,280** | **1,275** | **6** | **Full metadata recorded** |

---

## 2. Partition and Split Distribution (Leakage-Free Grouped Split)

Images were grouped by `group_id` (`observation_id`) to ensure multiple photos from a single plant observation never leak across splits.

| Split Partition | Van Udyan Local Images | iNaturalist Supplementary Images | Total Images | Partition Percentage |
| :--- | :---: | :---: | :---: | :---: |
| **Train** | 93 | 783 | **876** | 68.7% |
| **Validation** | 21 | 183 | **204** | 16.0% |
| **Test (Held-out)** | 26 | 169 | **195** | 15.3% |
| **Total** | **140** | **1,135** | **1,275** | **100.0%** |
| *Dedicated Van Udyan Benchmark* | *140* | *0* | *140* | *Evaluation subset in test_van_udyan_benchmark/* |

---

## 3. Image Integrity & Dimensional Analysis

- **Format**: 100% validated JPEG images (Pillow verified).
- **Width Range**: 90 px (minimum thumbnail preserved from Excel) to 500 px (standard iNaturalist medium resolution).
- **Height Range**: 160 px to 500 px.
- **Corrupt / Unreadable Files**: 0 corrupt files found.
- **Aspect Ratios**: Preserved without forced stretching during data preparation; dynamic aspect-ratio resizing and standard zero-padding or scaling is handled during batch tensor loading in Colab.

---

## 4. Class Balance Summary across 38 Species

All 38 target species have between **30 and 48 total images**:
- **Mean count per species**: $\approx 33.5$ images.
- **Minimum count**: 30 images (*Careya arborea*, *Dalbergia sissoo*, *Gmelina arborea*, *Melia dubia*, *Sterculia urens*, *Swietenia macrophylla*, *Citrus aurantiifolia*).
- **Maximum count**: 48 images (*Azadirachta indica* with 18 local field photos + 30 iNaturalist observations).
- **Imbalance Mitigation**: The addition of iNaturalist observations raised the minimum sample count from 1 image to 30 images per class, resolving severe class imbalance.
