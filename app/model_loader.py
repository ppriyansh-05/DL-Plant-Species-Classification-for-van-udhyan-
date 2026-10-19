import os
import json
import zipfile
import tempfile
import shutil
from pathlib import Path
from app.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET,
    SUPABASE_MODEL_PATH,
    LOCAL_MODEL_PATH
)

def _sanitize_keras_archive(keras_path: Path) -> Path:
    """
    Keras 3.13+ saves an extra 'quantization_config: null' inside layer configs.
    Keras 3.12 (standard on CPU / Python 3.10) raises TypeError on unexpected kwargs.
    This helper checks config.json and removes quantization_config if present,
    returning a clean path that loads smoothly in all Keras 3 versions.
    """
    try:
        with zipfile.ZipFile(keras_path, 'r') as zin:
            if 'config.json' not in zin.namelist():
                return keras_path
            cfg_bytes = zin.read('config.json')
            if b'quantization_config' not in cfg_bytes:
                return keras_path
            
            cfg = json.loads(cfg_bytes.decode('utf-8'))
            
            def clean_dict(d):
                if isinstance(d, dict):
                    d.pop('quantization_config', None)
                    for k, v in d.items():
                        clean_dict(v)
                elif isinstance(d, list):
                    for item in d:
                        clean_dict(item)

            clean_dict(cfg)
            meta = zin.read('metadata.json')
            weights = zin.read('model.weights.h5')

        # Write sanitized version back in place or to a sanitized file
        sanitized_path = keras_path.parent / f"{keras_path.stem}_compat.keras"
        with zipfile.ZipFile(sanitized_path, 'w') as zout:
            zout.writestr('metadata.json', meta)
            zout.writestr('config.json', json.dumps(cfg).encode('utf-8'))
            zout.writestr('model.weights.h5', weights)
        return sanitized_path
    except Exception as e:
        print(f"[Warning] Failed to inspect/sanitize Keras archive: {e}")
        return keras_path

def ensure_model_available():
    """
    Checks if model exists locally. If not, and Supabase credentials are configured,
    attempts safe server-side download from Supabase Storage.
    Never logs secrets or sensitive credentials.
    Returns (status: bool, message: str, resolved_path: Path or None)
    """
    # 1. Check configured local model path or fallback
    target_path = LOCAL_MODEL_PATH
    if not (target_path.exists() and target_path.is_file()):
        for fallback in [Path("best_van_udyan_top15.keras"), Path("..") / "best_van_udyan_top15.keras"]:
            if fallback.exists() and fallback.is_file() and str(target_path) == str(Path("best_van_udyan_top15.keras")):
                target_path = fallback
                break

    if target_path.exists() and target_path.is_file():
        clean_path = _sanitize_keras_archive(target_path)
        return True, f"Found local model at {target_path.name}", clean_path

    # 2. Check Supabase Storage configuration
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False, (
            "Model file 'best_van_udyan_top15.keras' not found locally on disk, "
            "and Supabase Storage credentials are not configured in environment variables. "
            "Please upload 'best_van_udyan_top15.keras' to the repository root or set "
            "SUPABASE_URL and SUPABASE_KEY in your environment (.env / Render dashboard)."
        ), None

    # Redact URL domain for clean logging without leaking paths or keys
    masked_url = SUPABASE_URL.split("//")[-1].split("/")[0] if "//" in SUPABASE_URL else "configured Supabase host"

    try:
        from supabase import create_client
        print(f"[Storage] Connecting to Supabase Storage at {masked_url} to fetch '{SUPABASE_MODEL_PATH}'...")
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Download from bucket
        res = client.storage.from_(SUPABASE_BUCKET).download(SUPABASE_MODEL_PATH)
        if res:
            with open(LOCAL_MODEL_PATH, "wb") as f:
                f.write(res)
            print(f"[Storage] Successfully downloaded model from bucket '{SUPABASE_BUCKET}'.")
            clean_path = _sanitize_keras_archive(LOCAL_MODEL_PATH)
            return True, f"Successfully downloaded model from Supabase Storage bucket '{SUPABASE_BUCKET}'", clean_path
        else:
            return False, f"Failed to download model from Supabase bucket '{SUPABASE_BUCKET}'. File may not exist or bucket is empty.", None
    except Exception as e:
        # Never print the key or raw headers; report clean exception message
        err_msg = str(e)
        if SUPABASE_KEY and SUPABASE_KEY in err_msg:
            err_msg = err_msg.replace(SUPABASE_KEY, "[REDACTED_KEY]")
        return False, f"Error connecting to Supabase Storage: {err_msg}", None
