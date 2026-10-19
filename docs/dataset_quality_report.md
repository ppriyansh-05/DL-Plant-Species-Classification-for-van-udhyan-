# Dataset Quality & Expanded Readiness Report: Van Udyan Plant Classification

**Date:** 2026-10-19  
**Harvest Version:** Prioritized Multi-Tier Collection (Pune -> Maharashtra -> India -> Global)  
**Total Images Analyzed:** 1,660  
**Validated Clean Images on Disk:** 1,654  
**Quarantined / Dropped:** 1 quarantined label (`?` row), 6 exact byte duplicates dropped  
**Target Classes Represented:** 38 / 38 (100% species coverage, 40 to 58 images/species)  

---

## 1. Source Breakdown and Summary

| Source Stream | Harvested Photos | Validated Photos | Quarantined / Dropped | Attribution & Licences |
| :--- | :---: | :---: | :---: | :--- |
| **Van Udyan Excel (`Zone Wise Plants.xlsx`)** | 141 | 140 | 1 (Row 74: `?` unknown label) | In-situ field photos from RSWF Pune |
| **iNaturalist Prioritized Harvest (`raw_inaturalist`)** | 1,519 | 1,514 | 5 (SHA-256 byte duplicates) | CC0, CC-BY, CC-BY-NC, CC-BY-SA, CC-BY-NC-SA |
| **Total Combined** | **1,660** | **1,654** | **6** | **Full metadata recorded** |

---

## 2. Partition and Split Distribution (Observation-Grouped Split)

Images are grouped by `group_id` (`observation_id` for iNaturalist, `VU_ROW_xxx` for Van Udyan) so multi-angle or burst shots of the same tree specimen never cross partition boundaries.

| Split Partition | Van Udyan Local Images | iNaturalist Supplementary Images | Total Images | Partition Percentage |
| :--- | :---: | :---: | :---: | :---: |
| **Train** | 101 | 1,049 | **1,150** | 69.5% |
| **Validation** | 17 | 247 | **264** | 16.0% |
| **Test (Held-out)** | 22 | 218 | **240** | 14.5% |
| **Total** | **140** | **1,514** | **1,654** | **100.0%** |
| *Dedicated Van Udyan Benchmark* | *140* | *0* | *140* | *Evaluation set in test_van_udyan_benchmark/* |

---

## 3. Geographic Prioritization in Supplementary Harvest

- **Pune District (`place_id=32349`)**: **372 photos** collected with direct geographic tagging in and around Pune, Maharashtra.
- **Maharashtra State (`place_id=6683`)**: **8 photos** added from wider Maharashtra.
- **National & Regional Fallback**: Complementary licensed photos across India to ensure every single species has at least 40 images.
