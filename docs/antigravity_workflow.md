# Antigravity Workflow — Van Udyan Plant Classification

## Goal
Use Antigravity for the software/data pipeline and website, Google Colab for GPU-heavy training, and GitHub as the source of truth. The model should support as many Van Udyan species as the available verified data permits.

## Repository
`ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-`

## Development rules
- Inspect the existing repository before editing. Reuse existing scripts and notebooks where appropriate; do not duplicate entire pipelines.
- Never commit raw image datasets, private NGO material, credentials, or trained model binaries to GitHub. Keep large data/model files in Drive or appropriate artifact storage; commit manifests, code, docs, and small metrics only.
- Preserve iNaturalist photo attribution, observation URL/ID, licence, source and location fields. Only use photos whose licence permits the intended use.
- Never guess scientific names. Keep uncertain labels quarantined until verified.
- Use deterministic, observation/specimen-grouped train/validation/test splits and deduplicate before splitting. A dedicated Van Udyan evaluation set must remain unseen during model fitting and model selection.
- Keep all species that have useful labelled data; document class counts and flag low-support classes rather than silently dropping them.
- Do not claim a target accuracy. Generate metrics from the actual saved test predictions.
- Treat the existing 38-class 11.79% and 8-class 30.30% results as preliminary baselines only. The 8-class run showed an input-ran-out-of-data warning and only 33 test images.
- The prediction app must show supported classes and top predictions, and warn users that confidence is not calibrated probability. Add an unknown/low-confidence response if technically validated.
- Keep the DL web app separate from the existing service-learning dashboard unless an integration is explicitly implemented and tested.

## Phase A — Audit
1. Inspect all scripts, notebooks, docs, dataset manifests, and current git status.
2. Check that the collector's requested geographic filters actually limit observations to Pune/Maharashtra; if not, implement explicit geographic filtering and source metadata.
3. Verify class names against the spreadsheet and identify ambiguous/missing plant labels.
4. Check the split code for empty validation sets, low per-class support, exact/near duplicates, and observation/specimen leakage.
5. Add automated tests for taxon mapping, licence filtering, image integrity, deduplication, and split isolation.

## Phase B — Data expansion
1. Query licensed iNaturalist observations for every verified target species. Search Pune/Maharashtra first and broaden to India only when needed.
2. Keep a configurable target per species, but collect until a reasonable cap or source/API limit is reached; don't stop at 30 solely because of the old default.
3. Download only explicit, approved licences; retain photo attribution, photo URL, observation URL, taxon ID/name, licence, observation date and locality.
4. Include usable Van Udyan photos with correct labels. Keep uncertain and unlabelled records out of supervised training.
5. Validate images, exact-deduplicate, review near-duplicates, create one master manifest, and make group-aware splits.

## Phase C — Training (Google Colab)
1. Use the generated processed dataset and class mapping.
2. Train a fresh MobileNetV2 transfer-learning model with consistent preprocessing, augmentation only on training data, class weights or sampling if appropriate, callbacks, and reproducible seed.
3. Make sure each epoch has a finite, correct number of steps; no input-ran-out-of-data warnings.
4. Save model, class mapping, training history, test predictions, and metrics to Drive.
5. Report top-1 accuracy, top-3 accuracy, macro/weighted F1, per-class precision/recall, confusion matrix, and support.
6. Evaluate the held-out Van Udyan set separately. Do not use it for tuning.

## Phase D — Website
- Build a clean responsive plant identification UI.
- Backend: FastAPI endpoint accepting a photo, validating file type/size, preprocessing exactly as training, loading the model once, and returning top-3 scientific names/scores and model version.
- Frontend: upload/preview, prediction result, top-3 list, supported-species disclaimer, low-confidence/unknown messaging, project overview and measured evaluation metrics.
- Add tests for valid images, invalid files, class-map consistency, and preprocessing parity.
- Use environment variables for deployment settings; no secrets in source.
- Deploy only after local end-to-end smoke tests. Store large model artifacts outside Git if needed.

## Phase E — GitHub hygiene
- Commit code/docs/tests/metrics with small, focused commits.
- Do not commit raw photos, licensed image copies, credentials, or model binaries.
- Keep README, tracker, dataset docs, model methodology, results, and report synchronized.
- Never put unverified metrics into the report.
