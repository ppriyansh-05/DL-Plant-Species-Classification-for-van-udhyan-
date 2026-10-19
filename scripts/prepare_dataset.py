"""
prepare_dataset.py
Master dataset preparation, validation, deduplication, and split pipeline.

Strict Leakage-Free Design:
1. Keeps all 140 usable Van Udyan Excel field photos EXCLUSIVELY in 'test_van_udyan_benchmark/'.
   They are NEVER assigned to train, validation, or the regular test split.
2. Uses the 1,514 validated iNaturalist photos exclusively for the regular train/val/test splits
   using deterministic observation-grouped splitting (seed=42).
3. Safely clears and rebuilds target output directories upon every run to prevent stale files.
4. Enforces disjoint SHA-256 image hashes across all 4 partition folders.
5. Generates the master manifest, per-species split summaries, and quality reports.
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

def compute_file_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(64 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()

def prepare_dataset(
    excel_manifest_path: str = "data/raw_excel/raw_excel_manifest.csv",
    inat_manifest_path: str = "data/raw_inaturalist/inat_photo_attribution_metadata.csv",
    processed_dir: str = "data/processed",
    target_img_size: int = 224
):
    base_out = Path(processed_dir)
    train_dir = base_out / "train"
    val_dir = base_out / "val"
    test_dir = base_out / "test"
    test_van_udyan_only = base_out / "test_van_udyan_benchmark"
    
    # 0. Cleanly remove stale target directories to ensure clean rebuilding
    print("Clearing target output directories to avoid stale artifacts...")
    for d in [train_dir, val_dir, test_dir, test_van_udyan_only]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
        
    excel_records = []
    inat_records = []
    
    # 1. Load Excel Van Udyan Manifest (Exclusively for independent benchmark)
    excel_p = Path(excel_manifest_path)
    if excel_p.exists():
        df_excel = pd.read_csv(excel_p)
        print(f"Loaded Excel manifest: {len(df_excel)} rows")
        for _, r in df_excel.iterrows():
            if r.get("is_quarantined", False):
                continue
            sc_clean = r["scientific_name_clean"]
            if not sc_clean or pd.isna(sc_clean):
                continue
            file_p = Path(r["file_path"])
            if not file_p.exists():
                continue
            excel_records.append({
                "source_dataset": "Van_Udyan_Excel",
                "species": sc_clean,
                "group_id": f"VU_ROW_{r['excel_row']:03d}",
                "original_path": str(file_p).replace("\\", "/"),
                "file_name": file_p.name,
                "zone": r["zone"],
                "licence": "Proprietary_Van_Udyan_RSWF",
                "attribution": "Reform Social Welfare Foundation (RSWF), Pune - Van Udyan Bio-Monitoring",
                "observation_id": f"VU_ROW_{r['excel_row']}",
                "split": "test_van_udyan_benchmark"
            })
            
    # 2. Load iNaturalist Manifest (Exclusively for train / val / test)
    inat_p = Path(inat_manifest_path)
    if inat_p.exists():
        df_inat = pd.read_csv(inat_p)
        print(f"Loaded iNaturalist manifest: {len(df_inat)} rows")
        for _, r in df_inat.iterrows():
            sc_req = r.get("scientific_name_requested")
            if not sc_req or pd.isna(sc_req):
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
                "split": "unassigned"
            })

    print(f"Raw collected: {len(excel_records)} Excel records, {len(inat_records)} iNaturalist records")
    
    # 3. Validation and Deduplication
    def validate_and_dedup(records, seen_hashes):
        validated = []
        corrupt = 0
        dup = 0
        for row in records:
            img_path = Path(row["original_path"])
            try:
                with Image.open(img_path) as im:
                    im.verify()
                with Image.open(img_path) as im:
                    w, h = im.size
                    fmt = im.format
            except Exception:
                corrupt += 1
                continue
                
            sha256 = compute_file_sha256(img_path)
            if sha256 in seen_hashes:
                dup += 1
                continue
            seen_hashes.add(sha256)
            
            row_dict = row.copy()
            row_dict["width"] = w
            row_dict["height"] = h
            row_dict["format"] = fmt
            row_dict["sha256"] = sha256
            row_dict["aspect_ratio"] = round(w / h, 3) if h > 0 else 0
            validated.append(row_dict)
        return validated, corrupt, dup

    global_seen_hashes = set()
    
    # Validate Van Udyan local benchmark images first
    val_excel, c_e, d_e = validate_and_dedup(excel_records, global_seen_hashes)
    print(f"Van Udyan Benchmark: {len(val_excel)} clean images (dropped {c_e} corrupt, {d_e} duplicates)")
    
    # Validate iNaturalist images (ensuring none match any Van Udyan image hash)
    val_inat, c_i, d_i = validate_and_dedup(inat_records, global_seen_hashes)
    print(f"iNaturalist Dataset: {len(val_inat)} clean images (dropped {c_i} corrupt, {d_i} duplicates)")

    df_inat_val = pd.DataFrame(val_inat)
    
    # 4. Grouped Splitting for iNaturalist Photos (Train / Val / Test)
    import random
    random.seed(RANDOM_SEED)
    
    for species, group_df in df_inat_val.groupby("species"):
        unique_groups = group_df["group_id"].unique().tolist()
        random.shuffle(unique_groups)
        
        n_total = len(unique_groups)
        if n_total == 1:
            train_groups = set(unique_groups)
            val_groups = set()
            test_groups = set()
        elif n_total == 2:
            train_groups = {unique_groups[0]}
            test_groups = {unique_groups[1]}
            val_groups = set()
        elif n_total < 5:
            train_groups = set(unique_groups[:-1])
            test_groups = {unique_groups[-1]}
            val_groups = set()
        else:
            n_test = max(1, int(round(0.15 * n_total)))
            n_val = max(1, int(round(0.15 * n_total)))
            test_groups = set(unique_groups[:n_test])
            val_groups = set(unique_groups[n_test:n_test + n_val])
            train_groups = set(unique_groups[n_test + n_val:])
            
        for g in train_groups:
            df_inat_val.loc[(df_inat_val["species"] == species) & (df_inat_val["group_id"] == g), "split"] = "train"
        for g in val_groups:
            df_inat_val.loc[(df_inat_val["species"] == species) & (df_inat_val["group_id"] == g), "split"] = "val"
        for g in test_groups:
            df_inat_val.loc[(df_inat_val["species"] == species) & (df_inat_val["group_id"] == g), "split"] = "test"

    # Combine into Master Manifest
    df_excel_val = pd.DataFrame(val_excel)
    master_df = pd.concat([df_inat_val, df_excel_val], ignore_index=True)
    
    # 5. Populate Partition Directories on Disk
    partition_hashes = {"train": set(), "val": set(), "test": set(), "test_van_udyan_benchmark": set()}
    
    for _, row in master_df.iterrows():
        split_name = row["split"]
        safe_sp = row["species"].replace(" ", "_")
        dest_folder = base_out / split_name / safe_sp
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / row["file_name"]
        
        shutil.copy2(row["original_path"], dest_file)
        partition_hashes[split_name].add(row["sha256"])

    # 6. Verify Disjoint Hash Isolation Across All Four Partitions
    print("\n--- Verifying Hash Disjointness Across Partitions ---")
    splits_list = ["train", "val", "test", "test_van_udyan_benchmark"]
    leakage_detected = False
    for i in range(len(splits_list)):
        for j in range(i + 1, len(splits_list)):
            s1, s2 = splits_list[i], splits_list[j]
            overlap = partition_hashes[s1].intersection(partition_hashes[s2])
            if len(overlap) > 0:
                print(f"[CRITICAL ERROR] Hash overlap detected between {s1} and {s2}: {len(overlap)} images!")
                leakage_detected = True
            else:
                print(f"[OK] {s1} and {s2} are completely disjoint (0 overlapping hashes).")
                
    if leakage_detected:
        raise ValueError("Data leakage detected across partitions! Aborting.")

    # 7. Export Manifests
    master_manifest_path = base_out / "master_dataset_manifest.csv"
    master_df.to_csv(master_manifest_path, index=False)
    print(f"\nMaster manifest saved to: {master_manifest_path}")
    
    split_counts = master_df.groupby(["split", "source_dataset"]).size().unstack(fill_value=0)
    print("\n--- Final Dataset Split Summary ---")
    print(split_counts)
    
    species_summary = master_df.groupby("species")["split"].value_counts().unstack(fill_value=0)
    summary_path = base_out / "species_split_summary.csv"
    species_summary.to_csv(summary_path)
    print(f"\nSpecies split summary saved to: {summary_path}")
    
    return master_df

if __name__ == "__main__":
    prepare_dataset()
