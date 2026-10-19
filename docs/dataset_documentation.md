# Dataset Documentation: Van Udyan Plant Species Classification

## 1. Overview and Problem Context

The dataset for **"Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring"** supports automated vegetation health and biodiversity surveillance for the Van Udyan urban plantation project managed by **Reform Social Welfare Foundation (RSWF), Pune**.

The primary objective is to accurately recognize 38 native and planted tree species across different plantation zones (Zone 1, Zone 2, and Zone 3) from field imagery.

---

## 2. Target Species Taxonomy

The dataset encompasses 38 target plant classes:

1. *Aegle marmelos* (Bael)
2. *Alstonia scholaris* (Saptaparni / Devil's Tree)
3. *Azadirachta indica* (Neem)
4. *Bauhinia racemosa* (Apta / Bidi Leaf Tree)
5. *Bauhinia variegata* (Kachnar / Orchid Tree)
6. *Bombax ceiba* (Semal / Red Silk Cotton)
7. *Butea monosperma* (Palash / Flame of the Forest)
8. *Careya arborea* (Kumbhi / Wild Guava)
9. *Citrus aurantiifolia* (Key Lime / Nimbu)
10. *Cordia dichotoma* (Lasora / Indian Cherry)
11. *Cordia sebestena* (Scarlet Cordia / Geiger Tree)
12. *Dalbergia latifolia* (Shisham / Indian Rosewood)
13. *Dalbergia sissoo* (North Indian Rosewood)
14. *Erythrina variegata* (Indian Coral Tree)
15. *Ficus benghalensis* (Banyan Tree)
16. *Ficus religiosa* (Peepal Tree)
17. *Gmelina arborea* (Gamhar / Beechwood)
18. *Grewia tiliifolia* (Dhaman)
19. *Hibiscus rosa-sinensis* (China Rose / Gudhal)
20. *Madhuca longifolia* (Mahua)
21. *Mangifera indica* (Mango)
22. *Melia azedarach* (Bakain / Chinaberry)
23. *Melia dubia* (Malabar Neem)
24. *Mimusops elengi* (Bakul / Spanish Cherry)
25. *Nerium oleander* (Kaner / Oleander)
26. *Plumeria rubra* (Frangipani / Champa)
27. *Pongamia pinnata* (Karanj / Indian Beech)
28. *Psidium guajava* (Guava / Amrood)
29. *Salix tetrasperma* (Indian Willow)
30. *Sterculia urens* (Gum Karaya)
31. *Swietenia macrophylla* (Big-leaf Mahogany)
32. *Syzygium cumini* (Jamun / Black Plum)
33. *Tectona grandis* (Teak / Sagwan)
34. *Terminalia arjuna* (Arjun Tree)
35. *Terminalia bellirica* (Baheda)
36. *Terminalia catappa* (Indian Almond / Desi Badam)
37. *Thespesia populnea* (Portia Tree / Paras Peepal)
38. *Ziziphus mauritiana* (Indian Jujube / Ber)

---

## 3. Data Sources

### A. Local Field Data: Van Udyan (`Zone Wise Plants.xlsx`)
- **Origin**: In-situ photography conducted by RSWF field teams across Plantation Zones 1, 2, and 3.
- **Format**: 141 embedded images inside an Excel workbook drawing layer.
- **Extraction Protocol**: Extracted via OpenPyXL drawing layer anchors into `data/raw_excel/`.
- **Quality Inspection & Quarantining**:
  - Valid images: 140
  - Quarantined: 1 (Excel Row 74 has label `?`, Zone 2. Quarantined to prevent corrupted taxonomic labels).
  - Average resolution: 100 x 160 px (drawing thumbnail dimensions preserved from workbook).
  - Duplicate check: 0 duplicate SHA-256 hashes detected.

### B. Supplementary External Data: iNaturalist API
- **Origin**: Official iNaturalist v1 API (`https://api.inaturalist.org/v1/observations`).
- **Target Size**: Up to 30 photos per species to compensate for local severe class imbalance.
- **Licensing Restrictions**: Exclusively permissive, non-commercial, attribution-preserving Creative Commons licenses:
  - `CC0` (Public Domain)
  - `CC-BY` (Attribution)
  - `CC-BY-NC` (Attribution-NonCommercial)
  - `CC-BY-SA` (Attribution-ShareAlike)
  - `CC-BY-NC-SA` (Attribution-NonCommercial-ShareAlike)
  - *Strict Exclusion*: NoDerivatives (`-ND`) and All Rights Reserved images are rejected at API query level.
- **Metadata Captured**: Observation ID, photo ID, observer username/name, CC license code, attribution URL, observation timestamp, geographic coordinates.

---

## 4. Pipeline Architecture and Data Flow

```mermaid
graph TD
    subgraph Data Sources
        A["Van Udyan Workbook (Zone Wise Plants.xlsx)"]
        B["iNaturalist v1 API (Taxon Query)"]
    end

    subgraph Phase 2: Extraction & Quarantine
        A --> C["scripts/extract_excel_images.py"]
        C --> D["data/raw_excel/images/ (140 Images)"]
        C --> E["data/raw_excel/quarantine/ (Row 74: '?')"]
        C --> F["data/raw_excel/raw_excel_manifest.csv"]
    end

    subgraph Phase 3: Licensed API Collection
        B --> G["scripts/inaturalist_collector.py"]
        G --> H["data/raw_inaturalist/images/"]
        G --> I["data/raw_inaturalist/inat_photo_attribution_metadata.csv"]
    end

    subgraph Phase 4 & 5: Dataset Pipeline & Grouped Split
        D --> J["scripts/prepare_dataset.py"]
        H --> J
        F --> J
        I --> J
        J --> K["Integrity Checks & Pillow Validation"]
        K --> L["Deduplication (SHA-256 Hash Matching)"]
        L --> M["Grouped Stratified Splitting (By Observation ID)"]
        M --> N["data/processed/train/"]
        M --> O["data/processed/val/"]
        M --> P["data/processed/test/"]
        M --> Q["data/processed/test_van_udyan_benchmark/"]
        M --> R["data/processed/master_dataset_manifest.csv"]
    end

    subgraph Phase 6: Training Handoff (Google Colab)
        N -.-> S["Google Colab Runtime (MobileNetV2 Transfer Learning)"]
        O -.-> S
        P -.-> S
        Q -.-> S
    end
```

---

## 5. Data Leakage Prevention Strategy

To ensure genuine generalization in real-world urban plantation deployment:
1. **Observation Grouping**: Multiple photographs taken during a single observation (same plant specimen, identical lighting, different angles) are grouped by `group_id` (`observation_id`).
2. **Atomic Allocation**: An entire observation group is assigned exclusively to either `train`, `val`, or `test`. No observation crosses partition boundaries.
3. **Pure Van Udyan Evaluation Benchmark**: In addition to standard test partitions, all valid Van Udyan field images are tracked in `test_van_udyan_benchmark/` so the model can be evaluated specifically against raw field imagery from Pune.
