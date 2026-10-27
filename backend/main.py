import io
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image

from backend.config import (
    ALLOWED_CONTENT_TYPES,
    MAX_FILE_SIZE_BYTES,
    METRICS_PATH,
    CLASS_MAPPING_PATH,
    SPECIES_INFO,
    CORS_ORIGINS,
    BASE_DIR
)
from backend.inference import inference_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the model once into memory
    print("[Backend] Initializing Van Udyan Plant AI FastAPI service...")
    try:
        ok, msg = inference_service.load_model()
        if ok:
            print(f"[Backend] Model loaded successfully: {msg}")
        else:
            print(f"[Backend Warning] Model load deferred or failed: {msg}")
    except Exception as e:
        print(f"[Backend Error] Exception during startup model load: {e}")
    yield
    # Shutdown
    print("[Backend] Shutting down service.")

app = FastAPI(
    title="Van Udyan Plant AI Backend",
    description="High-performance neural inference backend for Van Udyan urban plant species classification.",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [origin.strip() for origin in CORS_ORIGINS if origin.strip()]
if not origins or "*" in origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Service health and model status diagnostic endpoint."""
    model_loaded = inference_service.model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "service": "van-udyan-plant-ai-backend",
        "version": "2.0.0",
        "model_loaded": model_loaded,
        "model_name": "EfficientNetB0 (ImageNet Transfer Learning)",
        "num_classes": len(inference_service.class_mapping),
        "load_error": inference_service.load_error
    }

@app.get("/api/species")
async def get_species():
    """Returns all 15 supported Van Udyan species with botanical metadata and zone details."""
    species_list = []
    # Guarantee consistent order matching class_mapping indices
    for idx in sorted(inference_service.class_mapping.keys()):
        raw_name = inference_service.class_mapping[idx]
        info = SPECIES_INFO.get(raw_name, {})
        species_list.append({
            "id": idx,
            "class_name": raw_name,
            "scientific_name": raw_name.replace("_", " "),
            "common_name": info.get("common_name", raw_name),
            "marathi_name": info.get("marathi_name", ""),
            "family": info.get("family", "Unknown"),
            "zone": info.get("primary_zone", "Zone 1, 2 or 3"),
            "zones": info.get("zones", ["Zone 1", "Zone 2", "Zone 3"]),
            "ecological_role": info.get("ecological_role", ""),
            "foliage": info.get("foliage", ""),
            "blooming_season": info.get("blooming_season", "")
        })
    return {
        "total": len(species_list),
        "species": species_list
    }

@app.get("/api/metrics")
async def get_metrics():
    """Returns official model evaluation and benchmark metrics from evaluation_summary.json."""
    metrics_file = METRICS_PATH
    if not metrics_file.exists():
        fallback = BASE_DIR / "evaluation_summary.json"
        if fallback.exists():
            metrics_file = fallback

    if metrics_file.exists():
        with open(metrics_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="evaluation_summary.json not found."
        )

@app.post("/api/predict")
async def predict_species(
    file: UploadFile = File(...),
    top_k: int = Query(3, ge=1, le=15, description="Number of top candidates to return")
):
    """
    Accepts multipart image upload (JPEG, PNG, WEBP max 8MB).
    Preprocesses to 224x224 RGB and runs genuine EfficientNetB0 neural inference.
    """
    # 1. Validate content type
    content_type = file.content_type or ""
    if content_type.lower() not in ALLOWED_CONTENT_TYPES:
        # Check filename extension fallback
        filename = (file.filename or "").lower()
        if not (filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".webp")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format '{content_type}'. Please upload a JPG, PNG, or WEBP image."
            )

    # 2. Read and validate file size
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read image payload: {str(e)}"
        )

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size ({len(contents) / (1024 * 1024):.2f} MB) exceeds maximum allowed size of 8 MB."
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # 3. Open image with Pillow
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Verify it's an authentic image
        image = Image.open(io.BytesIO(contents))  # Reopen after verify
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupt or unreadable image file: {str(e)}"
        )

    # 4. Perform genuine neural inference
    try:
        prediction_result = inference_service.predict(image, top_k_count=top_k)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )

    return prediction_result

@app.get("/api/samples")
async def list_sample_images():
    """Lists available authentic Van Udyan field benchmark photos for instant one-click testing."""
    bench_dir = BASE_DIR / "data" / "processed_top15" / "test_van_udyan_benchmark"
    samples = []
    if bench_dir.exists():
        for path in sorted(bench_dir.glob("*/*.*"))[:12]:
            species_raw = path.parent.name
            info = SPECIES_INFO.get(species_raw, {})
            samples.append({
                "id": path.stem,
                "filename": path.name,
                "species_name": species_raw.replace("_", " "),
                "common_name": info.get("common_name", species_raw),
                "zone": info.get("primary_zone", "Zone 1, 2 or 3"),
                "relative_path": f"data/processed_top15/test_van_udyan_benchmark/{species_raw}/{path.name}"
            })
    return {"samples": samples}

@app.get("/api/samples/image/{species}/{filename}")
async def get_sample_image(species: str, filename: str):
    """Serves a benchmark sample image for testing."""
    img_path = BASE_DIR / "data" / "processed_top15" / "test_van_udyan_benchmark" / species / filename
    if img_path.exists() and img_path.is_file():
        return FileResponse(img_path)
    raise HTTPException(status_code=404, detail="Sample image not found")
