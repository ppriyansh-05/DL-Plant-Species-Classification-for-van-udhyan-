# iNaturalist Data Collection Workflow

## 1. Overview and Ethical Guidelines

This document details the automated photo collection procedure used to gather supplementary plant observations from the official iNaturalist v1 API for the 38 target species in the Van Udyan project.

### Principles:
1. **Respect API Limits**: A forced polite delay of 1.1s is maintained between requests, plus exponential backoff upon encountering HTTP 429 status codes.
2. **Strict Creative Commons Licensing**: Only images explicitly marked as non-commercial, attribution-compatible, and modification-permissive are downloaded.
3. **Exact Taxon Matching**: Species queries are resolved using the iNaturalist `/taxa` endpoint, requiring exact case-insensitive matches against species-level active taxa to prevent taxonomic drift.

---

## 2. API Endpoints Used

- **Taxon Resolution**:
  ```http
  GET https://api.inaturalist.org/v1/taxa?q={scientific_name}&per_page=10
  ```
- **Observation Retrieval**:
  ```http
  GET https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&photos=true&per_page=100&page={page}&order_by=created_at&order=desc
  ```

---

## 3. Allowed vs. Rejected Licences

| Licence Code | Legal Status | Pipeline Decision |
| :--- | :--- | :--- |
| `cc0` | Public Domain Dedication | **Accepted** |
| `cc-by` | Attribution 4.0 International | **Accepted** |
| `cc-by-nc` | Attribution-NonCommercial 4.0 International | **Accepted** |
| `cc-by-sa` | Attribution-ShareAlike 4.0 International | **Accepted** |
| `cc-by-nc-sa` | Attribution-NonCommercial-ShareAlike 4.0 International | **Accepted** |
| `cc-by-nd` | Attribution-NoDerivatives | **Rejected** (pre-processing/resizing violates ND terms) |
| `cc-by-nc-nd`| Attribution-NonCommercial-NoDerivatives | **Rejected** |
| `None` / `all-rights-reserved` | Proprietary Copyright | **Rejected** |

---

## 4. Reproducing Collection

Run the standalone CLI:
```bash
python scripts/inaturalist_collector.py --max 30
```
Outputs:
- Images stored at `data/raw_inaturalist/images/<species_name>/`
- Attribution metadata stored at `data/raw_inaturalist/inat_photo_attribution_metadata.csv`
- Summary progress stored at `data/raw_inaturalist/collection_summary.csv`
