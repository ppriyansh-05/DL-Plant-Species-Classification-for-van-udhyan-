# Dataset Quality & Partition Audit: Van Udyan Plant Classification

**Date:** 2026-10-19  
**Total Images Analyzed:** 1,660  
**Validated Clean Images on Disk:** 1,654  
**Quarantined / Dropped:** 1 quarantined label (`?` row in Excel), 6 exact byte duplicates dropped  
**Target Classes Represented:** 38 / 38 (100% species coverage)  

---

## 1. Partition Breakdown and Strict Leakage-Free Design

All 140 usable in-situ Excel field photos are preserved **exclusively** in `test_van_udyan_benchmark/`. They are never included in training, validation, or the regular test split. The 1,514 validated iNaturalist photos are partitioned into regular train/val/test splits using deterministic observation-grouped splitting.

| Partition Directory | Purpose | Photos Included | Unique Hashes | Data Source |
| :--- | :--- | :---: | :---: | :--- |
| `train/` | Model Fitting | **1,050** | 1,050 | iNaturalist (Pune / Maha / India) |
| `val/` | Hyperparameter Tuning & Early Stopping | **236** | 236 | iNaturalist (Pune / Maha / India) |
| `test/` | Held-Out Evaluation | **228** | 228 | iNaturalist (Pune / Maha / India) |
| `test_van_udyan_benchmark/` | Independent Real-World Local Evaluation | **140** | 140 | Van Udyan Excel (`Zone Wise Plants.xlsx`) |
| **Total Images** | — | **1,654** | **1,654** | **100% Hash Disjoint (0 Overlap)** |

---

## 2. Hash Disjointness Verification Results

Cross-partition intersection tests performed on SHA-256 image hashes:
- `train` vs `val`: **0 overlapping hashes (PASSED)**
- `train` vs `test`: **0 overlapping hashes (PASSED)**
- `train` vs `test_van_udyan_benchmark`: **0 overlapping hashes (PASSED)**
- `val` vs `test`: **0 overlapping hashes (PASSED)**
- `val` vs `test_van_udyan_benchmark`: **0 overlapping hashes (PASSED)**
- `test` vs `test_van_udyan_benchmark`: **0 overlapping hashes (PASSED)**

---

## 3. Geographic Prioritization in iNaturalist Harvest

- **Pune District (`place_id=32349`)**: **372 photos** collected with direct geographic tagging in and around Pune, Maharashtra.
- **Maharashtra State (`place_id=6683`)**: **8 photos** added from wider Maharashtra.
- **National & Regional Fallback**: Complementary licensed photos across India to ensure all 38 species have sufficient examples.
