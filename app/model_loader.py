import os
from pathlib import Path
from app.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET,
    SUPABASE_MODEL_PATH,
    LOCAL_MODEL_PATH
)

def ensure_model_available():
    """
    Checks if model exists locally. If not, and Supabase credentials are configured,
    attempts safe server-side download from Supabase Storage.
    Returns (status: bool, message: str)
    """
    if LOCAL_MODEL_PATH.exists():
        return True, f"Found local model at {LOCAL_MODEL_PATH}"
    
    # Check parent directory as fallback
    parent_path = Path("..") / LOCAL_MODEL_PATH
    if parent_path.exists():
        return True, f"Found local model at {parent_path}"

    if not SUPABASE_URL or not SUPABASE_KEY:
        return False, (
            "Model file 'best_van_udyan_top15.keras' not found locally, and Supabase credentials "
            "are not configured. Please place the model in the root directory or set SUPABASE_URL "
            "and SUPABASE_KEY in environment variables."
        )

    try:
        from supabase import create_client
        print(f"Connecting to Supabase Storage at {SUPABASE_URL} to fetch {SUPABASE_MODEL_PATH}...")
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Download from private bucket
        res = client.storage.from_(SUPABASE_BUCKET).download(SUPABASE_MODEL_PATH)
        if res:
            with open(LOCAL_MODEL_PATH, "wb") as f:
                f.write(res)
            return True, f"Successfully downloaded model from Supabase Storage bucket '{SUPABASE_BUCKET}' to {LOCAL_MODEL_PATH}"
        else:
            return False, f"Failed to download model from Supabase bucket '{SUPABASE_BUCKET}'. File may not exist."
    except Exception as e:
        return False, f"Error connecting to Supabase Storage: {str(e)}"
