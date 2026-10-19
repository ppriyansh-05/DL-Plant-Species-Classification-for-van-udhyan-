"""
extract_excel_images.py
Extracts embedded drawing images from 'Zone Wise Plants.xlsx',
maps each image to its respective row (Scientific Name, Zone),
flags and quarantines unlabelled/suspicious rows (e.g. '?'),
and outputs a structured manifest and image dataset under data/raw_excel/.
"""

import os
import re
import io
import hashlib
from pathlib import Path
import pandas as pd
import openpyxl
from PIL import Image

TARGET_38 = [
    "Aegle marmelos", "Alstonia scholaris", "Azadirachta indica", "Bauhinia racemosa",
    "Bauhinia variegata", "Bombax ceiba", "Butea monosperma", "Careya arborea",
    "Citrus aurantiifolia", "Cordia dichotoma", "Cordia sebestena", "Dalbergia latifolia",
    "Dalbergia sissoo", "Erythrina variegata", "Ficus benghalensis", "Ficus religiosa",
    "Gmelina arborea", "Grewia tiliifolia", "Hibiscus rosa-sinensis", "Madhuca longifolia",
    "Mangifera indica", "Melia azedarach", "Melia dubia", "Mimusops elengi",
    "Nerium oleander", "Plumeria rubra", "Pongamia pinnata", "Psidium guajava",
    "Salix tetrasperma", "Sterculia urens", "Swietenia macrophylla", "Syzygium cumini",
    "Tectona grandis", "Terminalia arjuna", "Terminalia bellirica", "Terminalia catappa",
    "Thespesia populnea", "Ziziphus mauritiana"
]

def sanitize_filename(name: str) -> str:
    name = name.strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9_.-]", "", name)

def compute_sha256(byte_data: bytes) -> str:
    return hashlib.sha256(byte_data).hexdigest()

def extract_excel_images(
    excel_path: str = "Zone Wise Plants.xlsx",
    output_dir: str = "data/raw_excel"
):
    base_dir = Path(output_dir)
    images_dir = base_dir / "images"
    quarantine_dir = base_dir / "quarantine"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading workbook: {excel_path} ...")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet = wb.active
    
    # Read row data (1-based row index in openpyxl)
    # Header is at row 1, data starts at row 2
    row_data = {}
    for r_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        if r_idx == 1:
            continue
        sc_name = str(row[0]).strip() if row[0] is not None else ""
        zone = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
        row_data[r_idx] = (sc_name, zone)
        
    print(f"Total data rows in spreadsheet: {len(row_data)}")
    print(f"Total embedded images found: {len(sheet._images)}")
    
    manifest_records = []
    
    for idx, img in enumerate(sheet._images, start=1):
        # Determine anchor row
        anchor = getattr(img, "anchor", None)
        if anchor is None or not hasattr(anchor, "_from"):
            row_idx = idx + 1
        else:
            # openpyxl 0-indexed row offset + 1 = 1-based excel row number
            row_idx = anchor._from.row + 1
            
        sc_name, zone = row_data.get(row_idx, ("UNKNOWN", "UNKNOWN"))
        
        # Extract raw image bytes
        image_bytes = img._data()
        sha256 = compute_sha256(image_bytes)
        
        # Verify image using Pillow
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            width, height = pil_img.size
            img_format = pil_img.format or "JPEG"
            is_valid = True
            error_msg = ""
        except Exception as e:
            width, height = 0, 0
            img_format = "UNKNOWN"
            is_valid = False
            error_msg = str(e)
            
        ext = f".{img_format.lower()}" if img_format and img_format.lower() != "jpeg" else ".jpg"
        
        # Check label status
        is_quarantined = False
        quarantine_reason = ""
        
        if sc_name == "?" or not sc_name or sc_name == "UNKNOWN":
            is_quarantined = True
            quarantine_reason = f"Invalid species label: '{sc_name}'"
        elif sc_name not in TARGET_38:
            is_quarantined = True
            quarantine_reason = f"Species '{sc_name}' not in predefined 38 target classes"
        elif not is_valid:
            is_quarantined = True
            quarantine_reason = f"Image corrupt/unreadable: {error_msg}"
            
        # File naming & destination
        safe_species = sanitize_filename(sc_name if sc_name and sc_name != "?" else "unlabelled")
        safe_zone = sanitize_filename(zone)
        filename = f"van_udyan_row{row_idx:03d}_{safe_species}_{safe_zone}_{sha256[:8]}{ext}"
        
        if is_quarantined:
            dest_folder = quarantine_dir
            relative_dest = dest_folder / filename
        else:
            dest_folder = images_dir / safe_species
            dest_folder.mkdir(parents=True, exist_ok=True)
            relative_dest = dest_folder / filename
            
        # Save image
        with open(relative_dest, "wb") as f:
            f.write(image_bytes)
            
        manifest_records.append({
            "image_id": f"VU_EXCEL_{row_idx:03d}",
            "excel_row": row_idx,
            "scientific_name_raw": sc_name,
            "scientific_name_clean": sc_name if not is_quarantined else None,
            "zone": zone,
            "source_dataset": "Van_Udyan_Excel",
            "file_path": str(relative_dest).replace("\\", "/"),
            "file_name": filename,
            "width": width,
            "height": height,
            "format": img_format,
            "file_size_bytes": len(image_bytes),
            "sha256": sha256,
            "is_quarantined": is_quarantined,
            "quarantine_reason": quarantine_reason
        })

    df = pd.DataFrame(manifest_records)
    manifest_csv = base_dir / "raw_excel_manifest.csv"
    df.to_csv(manifest_csv, index=False)
    
    print("\n--- Extraction Summary ---")
    print(f"Total images processed: {len(df)}")
    print(f"Successfully extracted valid images: {(~df['is_quarantined']).sum()}")
    print(f"Quarantined images: {df['is_quarantined'].sum()}")
    if df['is_quarantined'].sum() > 0:
        quarantined = df[df['is_quarantined']]
        for _, q in quarantined.iterrows():
            print(f"  - Row {q['excel_row']} ({q['scientific_name_raw']}, {q['zone']}): {q['quarantine_reason']}")
    print(f"Manifest written to: {manifest_csv}")
    return df

if __name__ == "__main__":
    extract_excel_images()
