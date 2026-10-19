"""
Strict Smoke Test for Van Udyan Plant AI Web Application
Validates:
1. Class mapping file integrity (exact 15 classes matching Keras output index).
2. Model loading: Ensures the actual EfficientNetB0 Keras model loads into memory.
3. Strict Inference: Verifies that inference is performed by the real neural network,
   producing a 15-class probability vector that sums to 1.0 (softmax).
   Fails immediately if any fallback or pseudo-prediction is detected.
4. Input Preprocessing: Ensures 224x224 RGB image arrays in float32 are consumed correctly.
5. Real Field Photo Verification: Tests an authentic Van Udyan field benchmark image.
6. Supabase Logging Safety: Confirms no secrets or sensitive keys are exposed in error logs.
"""
import sys
import numpy as np
from PIL import Image
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import (
    CLASS_MAPPING_PATH,
    SPECIES_INFO,
    CONFIDENCE_THRESHOLD,
    IMG_HEIGHT,
    IMG_WIDTH
)
from app.inference import inference_service

def test_class_mapping():
    print("[1/6] Testing class mapping integrity...")
    assert len(inference_service.class_mapping) == 15, f"Expected 15 classes, got {len(inference_service.class_mapping)}"
    first_cls = inference_service.class_mapping[0]
    assert first_cls == "Alstonia_scholaris", f"Expected Alstonia_scholaris as index 0, got {first_cls}"
    print(f"  -> Passed: Exactly 15 classes configured. Index 0: {first_cls}")

def test_model_loaded_strictly():
    print("[2/6] Verifying actual Keras model loading...")
    status, msg = inference_service.load_model()
    assert status is True, f"Model failed to load: {msg}"
    assert inference_service.model is not None, "Model object is None after load_model()"
    print(f"  -> Passed: Actual Keras model loaded successfully ({inference_service.model.name}).")

def test_real_neural_inference():
    print("[3/6] Testing genuine neural network inference (NO fallbacks)...")
    test_img = Image.new("RGB", (300, 300), color=(80, 140, 100))
    res = inference_service.predict(test_img)
    
    # Must flag is_real_model = True
    assert res.get("is_real_model") is True, "FAIL: Prediction was marked as a fallback/fake!"
    assert "top_3_predictions" in res
    assert len(res["top_3_predictions"]) == 3
    
    # Verify raw prediction properties from the underlying model
    preprocessed = inference_service.preprocess_image(test_img)
    raw_preds = inference_service.model.predict(preprocessed, verbose=0)[0]
    assert len(raw_preds) == 15, f"Expected output dimension 15, got {len(raw_preds)}"
    assert np.isclose(np.sum(raw_preds), 1.0, atol=1e-3), f"Probabilities do not sum to 1: {np.sum(raw_preds)}"
    
    print(f"  -> Passed: Real model inference confirmed. Top prediction: {res['predicted_common_name']} ({res['confidence_pct']}%)")

def test_preprocessing_dimensions():
    print("[4/6] Testing preprocessing array dimensions and dtype...")
    test_img = Image.new("RGB", (512, 384), color=(120, 160, 90))
    arr = inference_service.preprocess_image(test_img)
    assert arr.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3), f"Unexpected shape {arr.shape}"
    assert arr.dtype == np.float32, f"Unexpected dtype {arr.dtype}"
    # Verify pixel range is [0, 255] float32 for EfficientNet
    assert arr.max() <= 255.0 and arr.min() >= 0.0, f"Pixel range out of expected bounds: [{arr.min()}, {arr.max()}]"
    print(f"  -> Passed: Dimensions {arr.shape}, dtype float32, valid range [0, 255].")

def test_real_field_sample_evaluation():
    print("[5/6] Testing prediction on an authentic Van Udyan field benchmark photo...")
    bench_dir = Path("data/processed_top15/test_van_udyan_benchmark")
    assert bench_dir.exists(), "Benchmark directory not found!"
    sample_files = list(bench_dir.glob("*/*.*"))
    assert len(sample_files) > 0, "No benchmark images found!"
    
    sample_img = Image.open(sample_files[0])
    res = inference_service.predict(sample_img)
    assert res["predicted_scientific_name"] in [c.replace("_", " ") for c in inference_service.class_mapping.values()]
    print(f"  -> Passed: Authentic sample '{sample_files[0].name}' ({sample_files[0].parent.name}) classified as {res['predicted_scientific_name']} ({res['confidence_pct']}%).")

def test_no_secrets_in_supabase_error_reporting():
    print("[6/6] Verifying secret masking in Supabase Storage error handler...")
    from app.model_loader import ensure_model_available
    import app.model_loader as ml
    
    # Mock invalid secret to verify redaction
    original_key = ml.SUPABASE_KEY
    original_url = ml.SUPABASE_URL
    original_local = ml.LOCAL_MODEL_PATH
    
    try:
        # Point to non-existent local model
        ml.LOCAL_MODEL_PATH = Path("non_existent_model_test_path.keras")
        ml.SUPABASE_URL = "https://mockproject.supabase.co"
        ml.SUPABASE_KEY = "SUPER_SECRET_KEY_12345"
        
        ok, msg, path = ensure_model_available()
        assert ok is False, "Expected failure with mock credentials!"
        assert "SUPER_SECRET_KEY_12345" not in msg, "SECURITY LEAK: Secret key exposed in error message!"
        print("  -> Passed: Secrets are masked properly; credentials never printed to logs.")
    finally:
        ml.SUPABASE_KEY = original_key
        ml.SUPABASE_URL = original_url
        ml.LOCAL_MODEL_PATH = original_local

if __name__ == "__main__":
    print("=" * 65)
    print("  STRICT SMOKE TEST SUITE: VAN UDYAN PLANT AI (NO FALLBACKS)")
    print("=" * 65)
    test_class_mapping()
    test_model_loaded_strictly()
    test_real_neural_inference()
    test_preprocessing_dimensions()
    test_real_field_sample_evaluation()
    test_no_secrets_in_supabase_error_reporting()
    print("=" * 65)
    print("  ALL 6 STRICT SMOKE TESTS PASSED CLEANLY WITH REAL MODEL!")
    print("=" * 65)
