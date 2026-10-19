# Project Tracker: Van Udyan Deep Learning Plant Classification

**Project Title:** Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring  
**Organization:** Reform Social Welfare Foundation (RSWF), Pune – Van Udyan Biodiversity Monitoring  
**Last Updated:** 2026-10-19

---

## 1. Status Overview

| Phase | Description | Status | Output / Artifacts |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Inspect Folder & Missing Inputs | **Completed** | Inventory of `Zone Wise Plants.xlsx` and the iNaturalist collection/training notebooks |
| **Phase 2** | Excel Extraction & Validation | **Completed** | 140 usable Van Udyan images; the unknown `?` label must remain excluded pending identification |
| **Phase 3** | Licensed iNaturalist Collection | **Collected; audit before reuse** | Existing collection reports 1,140 photos across 38 target species. Verify actual local files, licences, labels, and observation grouping before the next run |
| **Phase 4** | Dataset Validation & Split | **Needs review before final experiment** | Existing split reports 876 train / 204 validation / 195 test. Re-run validation and duplicate/observation-group checks after any new collection |
| **Phase 5** | Initial 38-Class Model | **Baseline only — weak performance** | Existing MobileNetV2 run: 195 test images, 38 classes, 11.79% top-1 accuracy and 25.64% top-3 accuracy |
| **Phase 6** | Focused 8-Class Experiment | **Preliminary; do not treat as final** | 218 train / 37 validation / 33 test images; 30.30% test accuracy. Training log emitted an input-ran-out-of-data warning. Rebuild the dataset pipeline and rerun before making claims |
| **Phase 7** | Expanded Pune/Maharashtra Dataset | **Next** | Collect additional correctly labelled, appropriately licensed images for the maximum feasible set of Van Udyan species; preserve attribution and source metadata |
| **Phase 8** | Final Training & Evaluation | **Pending** | Clean grouped splits, fresh MobileNetV2 training, test metrics, macro F1, per-class report, confusion matrix, and separate Van Udyan evaluation |
| **Phase 9** | Web Demo & Deployment | **Pending** | Upload image, predicted scientific/common name, top-3 predictions, calibrated/clearly labelled confidence, supported-class notice, and evaluation page |
| **Phase 10** | Report & GitHub Documentation | **In progress** | Report only measured results and document dataset sources, licence conditions, split protocol, and limitations |

---

## 2. Current Findings

1. The 38-class baseline achieved **11.79% top-1 test accuracy** on 195 test images and **25.64% top-3 accuracy**. This is a weak baseline, not the final result.
2. The focused 8-class experiment achieved **30.30% test accuracy** on only 33 test images (approximately 10 correct). The training log reported that input ran out of data. Treat this as a debugging result, not a final performance claim.
3. A field photo believed to be Kanar/yellow oleander or oleander was predicted as neem with 37.57% model confidence. This demonstrates a closed-set limitation: the classifier always chooses among its known classes, even when the true plant is absent from those classes.
4. The model must include the correct, verified species label (for example, *Thevetia peruviana* / *Cascabela thevetia* or *Nerium oleander*, depending on confirmation) before claiming support for that plant.
5. The earlier training set contains images from multiple sources. Final evaluation must avoid duplicate/near-duplicate and same-observation leakage. Report the ordinary held-out test result separately from performance on held-out Van Udyan field photos.

---

## 3. Next Actions

1. Inspect the current repo and source data in Antigravity; do not overwrite raw data or previous experiment artifacts.
2. Audit the 38 target names against the Van Udyan spreadsheet and confirm ambiguous/common-name mappings.
3. Collect as many useful, correctly identified images as possible for those species from Pune/Maharashtra first, then broader India where needed. Keep source URLs, observation IDs, image licences, attribution, and location metadata.
4. Enforce the relevant licence terms. Do not assume every iNaturalist image is reusable; retain only images whose photo licence is explicitly permitted by the project policy.
5. Validate images, exact-deduplicate, detect near-duplicates, and split by observation/specimen before training. Do not let images of the same observation occur in both training and test.
6. Preserve a dedicated Van Udyan evaluation subset that is not used for model fitting or model selection.
7. Train a fresh model in Google Colab when GPU training is needed; use Antigravity for code, dataset tooling, tests, documentation, API, frontend, and deployment.
8. Save the model and class mapping as one versioned artifact. Record seed, dataset manifest version, class counts, parameters, and measured metrics.
9. Build and test the website locally, then deploy. Add an unknown/low-confidence warning rather than presenting every prediction as certain.
10. Update this tracker and the report only with outputs that have actually been produced and verified.

---

## 4. Working Rules

- **No invented accuracy:** all report numbers must come from the final evaluation run.
- **No data leakage:** split by observation/specimen; deduplicate before splitting.
- **No licence assumptions:** preserve photo-level licence and attribution.
- **No hidden source mixing:** report overall test and local Van Udyan results separately.
- **No false integration claim:** the DL demo is a separate experimental model unless a real integration is implemented and tested.
- **Large training jobs:** run in Google Colab (preferably GPU); keep code and experiment instructions in this repository.
