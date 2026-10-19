"""
prepare_top15_dataset.py
Dedicated Top-15 Van Udyan Dataset Preparation Pipeline.

Features:
1. Filters exclusively for the 15 best-supported species in Van Udyan records.
2. Incorporates local Van Udyan photos into training/validation/test so the model learns from field conditions,
   while preserving a dedicated, unseen set of 30 Van Udyan field photographs (2 per species) in 'test_van_udyan_benchmark/'.
3. Observation-grouped splitting on both local field specimens and iNaturalist observations (seed=42).
4. Strict SHA-256 hash deduplication and disjointness across all 4 partitions.
5. Safely cleans previous Top-15 target directories before building to prevent stale artifacts.
"""

import os
import re
import io
import shutil
import hashlib
from pathlib import Path
from collections import Counter
import pandas as pd
from PIL import Image

RANDOM_SEED = 42

TOP_15_SPECIES = [
    "Azadirachta indica",    # Neem (18 Excel photos)
    "Mangifera indica",      # Mango (12 Excel photos)
    "Pongamia pinnata",      # Karanj (11 Excel photos)
    "Bombax ceiba",          # Semal (10 Excel photos)
    "Syzygium cumini",       # Jamun (6 Excel photos)
    "Alstonia scholaris",    # Saptaparni (5 Excel photos)
    "Terminalia bellirica",  # Baheda (5 Excel photos)
    "Terminalia catappa",    # Indian Almond (5 Excel photos)
    "Bauhinia variegata",    # Kachnar (4 Excel photos)
    "Cordia dichotoma",      # Lasora (4 Excel photos)
    "Dalbergia latifolia",   # Shisham (4 Excel photos)
    "Erythrina variegata",   # Coral Tree (4 Excel photos)
    "Ficus religiosa",       # Peepal (4 Excel photos)
    "Tectona grandis",       # Teak (4 Excel photos)
    "Ficus benghalensis"     # Banyan (3 Excel photos)
]

def compute_file_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(64 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()

def prepare_top15_dataset(
    excel_manifest_path: str = "data/raw_excel/raw_excel_manifest.csv",
    inat_manifest_path: str = "data/raw_inaturalist/inat_photo_attribution_metadata.csv",
    output_dir: str = "data/processed_top15"
):
    base_out = Path(output_dir)
    train_dir = base_out / "train"
    val_dir = base_out / "val"
    test_dir = base_out / "test"
    bench_dir = base_out / "test_van_udyan_benchmark"
    
    # 0. Cleanly purge previous Top-15 directories
    print("Purging target Top-15 directories to avoid stale files...")
    for d in [train_dir, val_dir, test_dir, bench_dir]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
        
    excel_records = []
    inat_records = []
    
    # 1. Load Excel Van Udyan Manifest (Filtered for Top-15)
    excel_p = Path(excel_manifest_path)
    if excel_p.exists():
        df_excel = pd.read_csv(excel_p)
        for _, r in df_excel.iterrows():
            if r.get("is_quarantined", False):
                continue
            sc_clean = r["scientific_name_clean"]
            if sc_clean not in TOP_15_SPECIES:
                continue
            file_p = Path(r["file_path"])
            if not file_p.exists():
                continue
            excel_records.append({
                "source_dataset": "Van_Udyan_Excel",
                "species": sc_clean,
                "group_id": f"VU_SPECIMEN_{r['excel_row']:03d}",
                "original_path": str(file_p).replace("\\", "/"),
                "file_name": file_p.name,
                "zone": r["zone"],
                "licence": "Proprietary_Van_Udyan_RSWF",
                "attribution": "Reform Social Welfare Foundation (RSWF), Pune - Van Udyan Bio-Monitoring",
                "observation_id": f"VU_ROW_{r['excel_row']}",
            })
            
    # 2. Load iNaturalist Manifest (Filtered for Top-15)
    inat_p = Path(inat_manifest_path)
    if inat_p.exists():
        df_inat = pd.read_csv(inat_p)
        for _, r in df_inat.iterrows():
            sc_req = r.get("scientific_name_requested")
            if sc_req not in TOP_15_SPECIES:
                continue
            file_p = Path(r["local_path"])
            if not file_p.exists():
                continue
            obs_id = str(r.get("observation_id", ""))
            group_key = f"INAT_OBS_{obs_id}" if obs_id and obs_id != "nan" else f"INAT_PHOTO_{r.get('photo_id')}"
            inat_records.append({
                "source_dataset": "iNaturalist_API",
                "species": sc_req,
                "group_id": group_key,
                "original_path": str(file_p).replace("\\", "/"),
                "file_name": file_p.name,
                "zone": "External_iNaturalist",
                "licence": r.get("photo_license_code"),
                "attribution": r.get("photo_attribution"),
                "observation_id": obs_id,
            })

    print(f"Top-15 Records loaded: {len(excel_records)} Excel photos, {len(inat_records)} iNaturalist photos.")

    # 3. Validation & Byte Deduplication
    def validate_records(records, seen_hashes):
        valid = []
        for r in records:
            p = Path(r["original_path"])
            try:
                with Image.open(p) as im:
                    im.verify()
                with Image.open(p) as im:
                    w, h = im.size
                    fmt = im.format
            except Exception:
                continue
            sha = compute_file_sha256(p)
            if sha in seen_hashes:
                continue
            seen_hashes.add(sha)
            
            d = r.copy()
            d["width"] = w
            d["height"] = h
            d["format"] = fmt
            d["sha256"] = sha
            valid.append(d)
        return valid

    global_hashes = set()
    clean_excel = validate_records(excel_records, global_hashes)
    clean_inat = validate_records(inat_records, global_hashes)
    print(f"Clean validated: {len(clean_excel)} Excel photos, {len(clean_inat)} iNaturalist photos.")

    # 4. Strict Partition Allocation
    # Strategy:
    # A. For each Top-15 species, designate 2 Excel photos as the dedicated, UNTOUCHED benchmark (test_van_udyan_benchmark).
    #    Total benchmark size = 15 * 2 = 30 untouched field photos.
    # B. The remaining 64 Excel field photos are incorporated into the general training & validation splits
    #    so the model actively learns field lighting, soil backgrounds, and local morphology.
    # C. iNaturalist photos are split across train / val / test using observation grouping (seed=42).
    
    import random
    random.seed(RANDOM_SEED)

    df_excel_clean = pd.DataFrame(clean_excel)
    df_inat_clean = pd.DataFrame(clean_inat)

    excel_benchmark_rows = []
    excel_trainable_rows = []

    for sp in TOP_15_SPECIES:
        sp_excel = df_excel_clean[df_excel_clean["species"] == sp].to_dict("records")
        random.shuffle(sp_excel)
        # Select 2 for benchmark
        bench_photos = sp_excel[:2]
        trainable_photos = sp_excel[2:]
        for bp in bench_photos:
            bp["split"] = "test_van_udyan_benchmark"
            excel_benchmark_rows.append(bp)
        for tp in trainable_photos:
            # 80% to train, 20% to val
            excel_trainable_rows.append(tp)

    # Split trainable Excel photos
    for ep in excel_trainable_rows:
        ep["split"] = "train" if random.random() < 0.8 else "val"

    # Split iNaturalist photos by observation group
    df_inat_clean["split"] = "unassigned"
    for sp in TOP_15_SPECIES:
        sp_df = df_inat_clean[df_inat_clean["species"] == sp]
        groups = sp_df["group_id"].unique().tolist()
        random.shuffle(groups)
        
        n_total = len(groups)
        n_test = max(1, int(round(0.15 * n_total)))
        n_val = max(1, int(round(0.15 * n_total)))
        
        test_g = set(groups[:n_test])
        val_g = set(groups[n_test:n_test + n_val])
        train_g = set(groups[n_test + n_val:])
        
        for g in train_g:
            df_inat_clean.loc[(df_inat_clean["species"] == sp) & (df_inat_clean["group_id"] == g), "split"] = "train"
        for g in val_g:
            df_inat_clean.loc[(df_inat_clean["species"] == sp) & (df_inat_clean["group_id"] == g), "split"] = "val"
        for g in test_g:
            df_inat_clean.loc[(df_inat_clean["species"] == sp) & (df_inat_clean["group_id"] == g), "split"] = "test"

    df_excel_bench = pd.DataFrame(excel_benchmark_rows)
    df_excel_trainable = pd.DataFrame(excel_trainable_rows)
    
    master_top15 = pd.concat([df_inat_clean, df_excel_trainable, df_excel_bench], ignore_index=True)
    
    # 5. Copy files into partition directories
    partition_hashes = {"train": set(), "val": set(), "test": set(), "test_van_udyan_benchmark": set()}
    for _, row in master_top15.iterrows():
        s = row["split"]
        safe_sp = row["species"].replace(" ", "_")
        dest_folder = base_out / s / safe_sp
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / row["file_name"]
        shutil.copy2(row["original_path"], dest_file)
        partition_hashes[s].add(row["sha256"])

    # 6. Verify Complete Hash Isolation
    print("\n--- Verifying Strict Hash Isolation Across All 4 Top-15 Partitions ---")
    splits = ["train", "val", "test", "test_van_udyan_benchmark"]
    leakage = False
    for i in range(len(splits)):
        for j in range(i+1, len(splits)):
            s1, s2 = splits[i], splits[j]
            overlap = partition_hashes[s1].intersection(partition_hashes[s2])
            if overlap:
                print(f"[ERROR] Hash overlap between {s1} and {s2}: {len(overlap)}")
                leakage = True
            else:
                print(f"[OK] {s1:25s} vs {s2:25s}: 0 overlapping hashes (PASSED)")
                
    if leakage:
        raise ValueError("Data leakage detected in Top-15 partition generation!")

    # 7. Export Manifests
    manifest_path = base_out / "top15_master_manifest.csv"
    master_top15.to_csv(manifest_path, index=False)
    print(f"\nSaved Top-15 master manifest to: {manifest_path}")

    summary_counts = master_top15.groupby(["split", "source_dataset"]).size().unstack(fill_value=0)
    print("\n--- Top-15 Dataset Split Breakdown ---")
    print(summary_counts)
    
    species_summary = master_top15.groupby("species")["split"].value_counts().unstack(fill_value=0)
    summary_csv = base_out / "top15_species_split_summary.csv"
    species_summary.to_csv(summary_csv)
    print(f"\nSaved Top-15 species summary to: {summary_csv}")
    print(species_summary)

    return master_top15

if __name__ == "__main__":
    prepare_top15_dataset()
