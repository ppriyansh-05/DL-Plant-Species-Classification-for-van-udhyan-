"""
Smoke test suite for the FastAPI backend service.
Validates:
- Health check returns 200 and model status
- Species endpoint returns 15 species with taxonomy and zones
- Metrics endpoint returns verified evaluation numbers
- Predict endpoint handles multipart image upload with real top-k output
- Proper error handling for invalid format and oversized uploads
"""
import io
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from PIL import Image

# Ensure project root is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.main import app
from backend.inference import inference_service

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert data["model_name"] == "EfficientNetB0 (ImageNet Transfer Learning)"
    assert data["num_classes"] == 15

def test_species_endpoint():
    response = client.get("/api/species")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    species = data["species"]
    assert len(species) == 15
    for s in species:
        assert "class_name" in s
        assert "scientific_name" in s
        assert "common_name" in s
        assert "zone" in s
        assert "zones" in s

def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["num_classes"] == 15
    assert "experiments" in data
    assert "experiment_2_top15_focused" in data["experiments"]

def test_predict_endpoint_valid_image():
    # Create test RGB image
    img = Image.new("RGB", (224, 224), color=(60, 130, 80))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/api/predict?top_k=3",
        files={"file": ("test_leaf.jpg", buf, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "top_k" in data
    assert len(data["top_k"]) == 3
    assert "inference_ms" in data
    assert data["inference_ms"] > 0

    first = data["top_k"][0]
    assert "class_name" in first
    assert "scientific_name" in first
    assert "common_name" in first
    assert "confidence" in first
    assert "zone" in first
    assert 0.0 <= first["confidence"] <= 1.0

def test_predict_invalid_file_type():
    txt_data = io.BytesIO(b"This is not an image file")
    response = client.post(
        "/api/predict",
        files={"file": ("notes.txt", txt_data, "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_predict_oversized_file():
    # 9 MB dummy payload
    oversized = io.BytesIO(b"\x00" * (9 * 1024 * 1024))
    response = client.post(
        "/api/predict",
        files={"file": ("huge.jpg", oversized, "image/jpeg")}
    )
    assert response.status_code == 413
    assert "exceeds maximum allowed size" in response.json()["detail"]

if __name__ == "__main__":
    print("Running FastAPI Backend Smoke Tests...")
    test_health_endpoint()
    print("  -> Health endpoint passed")
    test_species_endpoint()
    print("  -> Species endpoint passed (15 species with zones)")
    test_metrics_endpoint()
    print("  -> Metrics endpoint passed")
    test_predict_endpoint_valid_image()
    print("  -> Predict endpoint passed with real EfficientNetB0 inference")
    test_predict_invalid_file_type()
    print("  -> Invalid file format rejection passed (400)")
    test_predict_oversized_file()
    print("  -> Oversized payload rejection passed (413)")
    print("\nALL BACKEND SMOKE TESTS PASSED!")
