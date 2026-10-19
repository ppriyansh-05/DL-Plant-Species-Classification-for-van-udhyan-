"""
inaturalist_collector.py
Standalone CLI and reproducible module for querying the official iNaturalist v1 API,
collecting licensed photos (CC0, CC-BY, CC-BY-NC, CC-BY-SA, CC-BY-NC-SA),
enforcing strict rate-limiting and taxonomy resolution,
prioritizing observations from Pune, then Maharashtra, then India, and then Global fallback,
and generating an attribution manifest.
"""

import os
import re
import time
import json
import hashlib
from pathlib import Path
from urllib.parse import urlparse
import argparse
import requests
import pandas as pd
from tqdm import tqdm

API_BASE = "https://api.inaturalist.org/v1"
HEADERS = {
    "User-Agent": "VanUdyanPlantClassificationStudentProject/2.0 (academic dataset collection; contact=rswf-pune-academic)"
}

ALLOWED_PHOTO_LICENSES = {
    "cc0", "cc-by", "cc-by-nc", "cc-by-sa", "cc-by-nc-sa"
}

# Standard iNaturalist place identifiers for geographic prioritization
PUNE_PLACE_ID = 32349        # Pune District, MH, IN
MAHARASHTRA_PLACE_ID = 6683  # Maharashtra State, IN
INDIA_PLACE_ID = 6681        # India

TARGET_38_SPECIES = [
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

class INaturalistCollector:
    def __init__(
        self,
        output_dir: str = "data/raw_inaturalist",
        max_images_per_species: int = 50,
        request_delay: float = 1.0,
        timeout: int = 25
    ):
        self.output_dir = Path(output_dir)
        self.image_dir = self.output_dir / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_images_per_species = max_images_per_species
        self.request_delay = request_delay
        self.timeout = timeout
        
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        self.metadata_csv = self.output_dir / "inat_photo_attribution_metadata.csv"
        self.summary_csv = self.output_dir / "collection_summary.csv"
        
        self.metadata_rows = []
        self.summary_rows = []
        self.seen_photo_ids = set()
        
        # Resume from existing manifest if present
        if self.metadata_csv.exists():
            existing_df = pd.read_csv(self.metadata_csv)
            self.metadata_rows = existing_df.to_dict("records")
            self.seen_photo_ids = set(existing_df["photo_id"].dropna().astype(int).tolist()) if "photo_id" in existing_df else set()
            print(f"Resumed from {self.metadata_csv} with {len(self.metadata_rows)} photos already recorded.")

    def api_get(self, endpoint: str, params=None, retries=5):
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                if response.status_code == 429:
                    wait = min(45, 2 ** (attempt + 1))
                    print(f"\n[Rate Limit 429] Backing off {wait}s...")
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                time.sleep(self.request_delay)
                return response.json()
            except requests.RequestException as exc:
                if attempt == retries - 1:
                    print(f"\n[API Error] Request failed for {url}: {exc}")
                    return None
                time.sleep(min(20, 2 ** (attempt + 1)))
        return None

    @staticmethod
    def safe_name(text: str) -> str:
        text = text.strip().replace(" ", "_")
        return re.sub(r"[^A-Za-z0-9_.-]", "", text)

    def resolve_taxon(self, scientific_name: str):
        data = self.api_get("taxa", {"q": scientific_name, "per_page": 10})
        if not data or not data.get("results"):
            return None
        results = data["results"]
        
        # Clean helper to normalize hybrid symbols ('×', 'x', '\u00d7')
        def norm(n):
            return re.sub(r"[\s\u00d7xX]+", " ", (n or "").casefold()).strip()

        target_norm = norm(scientific_name)
        exact = [
            t for t in results
            if norm(t.get("name")) == target_norm or norm(t.get("matched_term")) == target_norm
        ]
        candidates = exact or []
        if not candidates:
            return None
        candidates.sort(key=lambda t: (t.get("rank") not in ("species", "hybrid"), t.get("is_active") is False))
        return candidates[0]

    @staticmethod
    def licence_code(photo: dict) -> str:
        code = photo.get("license_code")
        return str(code).strip().lower() if code else ""

    @staticmethod
    def get_photo_url(photo: dict) -> str:
        url = photo.get("url") or ""
        if not url:
            return ""
        # Upgrade standard square thumbnails to medium resolution for DL quality
        return re.sub(r"/(square|small|thumb)\.", "/medium.", url)

    def download_image(self, url: str, dest: Path):
        try:
            r = self.session.get(url, timeout=self.timeout, stream=True)
            r.raise_for_status()
            content_type = r.headers.get("Content-Type", "").split(";")[0].lower()
            if not content_type.startswith("image/"):
                r.close()
                return False, "not_an_image"
            temp_path = dest.with_suffix(dest.suffix + ".part")
            with open(temp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        f.write(chunk)
            r.close()
            if not temp_path.exists() or temp_path.stat().st_size < 1000:
                temp_path.unlink(missing_ok=True)
                return False, "file_too_small"
            temp_path.replace(dest)
            return True, content_type
        except Exception as exc:
            return False, str(exc)[:200]

    def collect_for_species(self, scientific_name: str, max_images: int = None):
        target_count = max_images or self.max_images_per_species
        
        # Check already downloaded count
        existing_for_species = [
            m for m in self.metadata_rows
            if m.get("scientific_name_requested") == scientific_name
        ]
        if len(existing_for_species) >= target_count:
            return len(existing_for_species)

        taxon = self.resolve_taxon(scientific_name)
        if not taxon:
            print(f"Exact taxon match NOT found for: {scientific_name}")
            self.summary_rows.append({
                "scientific_name": scientific_name,
                "taxon_id": None,
                "downloaded": len(existing_for_species),
                "status": "Exact taxon match not found"
            })
            return len(existing_for_species)

        taxon_id = taxon.get("id")
        species_dir = self.image_dir / self.safe_name(scientific_name)
        species_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = len(existing_for_species)
        examined_observations = 0

        # Tiered geographic prioritization: Pune -> Maharashtra -> India -> Global
        TIERS = [
            ("Pune", PUNE_PLACE_ID),
            ("Maharashtra", MAHARASHTRA_PLACE_ID),
            ("India", INDIA_PLACE_ID),
            ("Global", None)
        ]

        for tier_name, place_id in TIERS:
            if downloaded >= target_count:
                break

            page = 1
            max_pages = 4  # Up to 400 observations per geographic tier
            while downloaded < target_count and page <= max_pages:
                params = {
                    "taxon_id": taxon_id,
                    "photos": "true",
                    "per_page": 100,
                    "page": page,
                    "order_by": "created_at",
                    "order": "desc",
                }
                if place_id:
                    params["place_id"] = place_id

                data = self.api_get("observations", params)
                if not data or not data.get("results"):
                    break
                    
                results = data["results"]
                if not results:
                    break
                    
                for obs in results:
                    if downloaded >= target_count:
                        break

                    examined_observations += 1
                    obs_id = obs.get("id")
                    obs_url = f"https://www.inaturalist.org/observations/{obs_id}" if obs_id else ""
                    taxon_info = obs.get("taxon") or {}
                    observer = obs.get("user") or {}
                    photos = obs.get("photos") or []
                    
                    for photo in photos:
                        if downloaded >= target_count:
                            break
                        photo_id = photo.get("id")
                        lic = self.licence_code(photo)
                        photo_url = self.get_photo_url(photo)
                        
                        if lic not in ALLOWED_PHOTO_LICENSES or not photo_url:
                            continue
                        if photo_id and photo_id in self.seen_photo_ids:
                            continue
                            
                        ext = os.path.splitext(urlparse(photo_url).path)[1].lower()
                        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
                            ext = ".jpg"
                        image_id = photo_id or hashlib.sha1(photo_url.encode("utf-8")).hexdigest()[:12]
                        filename = f"inat_{self.safe_name(scientific_name)}_{image_id}{ext}"
                        dest = species_dir / filename
                        
                        if dest.exists() and dest.stat().st_size >= 1000:
                            success, detail = True, "already_downloaded"
                        else:
                            success, detail = self.download_image(photo_url, dest)
                            
                        if not success:
                            continue
                            
                        if photo_id:
                            self.seen_photo_ids.add(photo_id)
                        downloaded += 1
                        
                        coords = (obs.get("geojson") or {}).get("coordinates", [None, None])
                        
                        self.metadata_rows.append({
                            "image_id": f"INAT_{photo_id}",
                            "local_path": str(dest).replace("\\", "/"),
                            "file_name": filename,
                            "scientific_name_requested": scientific_name,
                            "inat_taxon_id": taxon_id,
                            "inat_taxon_name": taxon_info.get("name"),
                            "observation_id": obs_id,
                            "observation_url": obs_url,
                            "photo_id": photo_id,
                            "photo_url_downloaded": photo_url,
                            "photo_attribution": photo.get("attribution"),
                            "observer_name": observer.get("name"),
                            "observer_login": observer.get("login"),
                            "photo_license_code": lic,
                            "photo_license_url": f"https://creativecommons.org/licenses/{lic}/4.0/" if lic.startswith("cc-") else ("https://creativecommons.org/publicdomain/zero/1.0/" if lic == "cc0" else ""),
                            "observed_on": obs.get("observed_on"),
                            "place_guess": obs.get("place_guess"),
                            "geographic_scope": tier_name,
                            "latitude": coords[1] if len(coords) == 2 else None,
                            "longitude": coords[0] if len(coords) == 2 else None,
                            "source_dataset": "iNaturalist_API",
                            "download_status": detail
                        })
                        
                    if downloaded >= target_count:
                        break
                        
                if len(results) < 100:
                    break
                page += 1
            
        self.summary_rows.append({
            "scientific_name": scientific_name,
            "taxon_id": taxon_id,
            "downloaded": downloaded,
            "observations_examined": examined_observations,
            "status": "OK" if downloaded > 0 else "No images found under licence criteria"
        })
        
        # Checkpoint save
        pd.DataFrame(self.metadata_rows).to_csv(self.metadata_csv, index=False)
        pd.DataFrame(self.summary_rows).to_csv(self.summary_csv, index=False)
        return downloaded

    def run_all(self, species_list=None):
        species_list = species_list or TARGET_38_SPECIES
        print(f"Starting prioritized licensed collection for {len(species_list)} species (target <= {self.max_images_per_species}/species)...")
        for sc in tqdm(species_list, desc="Overall Progress"):
            cnt = self.collect_for_species(sc)
            
        print(f"\nCollection run completed. Total records saved: {len(self.metadata_rows)}")
        print(f"Manifest: {self.metadata_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect licensed iNaturalist photos with Pune/Maharashtra/India prioritization")
    parser.add_argument("--max", type=int, default=50, help="Max images per species")
    parser.add_argument("--pilot", action="store_true", help="Run quick pilot for top 2 species")
    parser.add_argument("--species", type=str, default=None, help="Specific species to collect")
    args = parser.parse_args()
    
    collector = INaturalistCollector(max_images_per_species=args.max)
    if args.species:
        collector.collect_for_species(args.species, max_images=args.max)
    elif args.pilot:
        print("Running pilot on 2 species...")
        collector.run_all(TARGET_38_SPECIES[:2])
    else:
        collector.run_all()
