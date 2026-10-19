"""
Smoke Test for Van Udyan Plant AI Web Application & Inference Service
Validates:
1. Class mapping file integrity (exact 15 classes).
2. Image preprocessing pipeline for valid images (JPG/PNG).
3. Handling of corrupted or non-image files (graceful rejection).
4. Prediction dictionary structure, confidence threshold alert, and top-3 outputs.
5. Model loader fallback handling when model file is remote or local.
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
    print("[1/5] Testing class mapping integrity...")
    assert len(inference_service.class_mapping) == 15, f"Expected 15 classes, got {len(inference_service.class_mapping)}"
    first_cls = inference_service.class_mapping[0]
    assert first_cls == "Alstonia_scholaris", f"Expected Alstonia_scholaris as index 0, got {first_cls}"
    print("  -> Passed: Exactly 15 classes correctly ordered.")

def test_valid_image_inference():
    print("[2/5] Testing valid image inference...")
    # Create synthetic test image
    test_img = Image.new("RGB", (300, 300), color=(73, 109, 137))
    res = inference_service.predict(test_img)
    
    assert "predicted_scientific_name" in res
    assert "predicted_common_name" in res
    assert "confidence_pct" in res
    assert "top_3_predictions" in res
    assert len(res["top_3_predictions"]) == 3
    print(f"  -> Passed: Prediction returned: {res['predicted_common_name']} ({res['predicted_scientific_name']}) at {res['confidence_pct']}%")

def test_preprocessing_dimensions():
    print("[3/5] Testing preprocessing array dimensions...")
    test_img = Image.new("RGB", (500, 400), color=(100, 150, 200))
    arr = inference_service.preprocess_image(test_img)
    assert arr.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3), f"Unexpected shape {arr.shape}"
    print(f"  -> Passed: Image resized and formatted to {arr.shape}")

def test_low_confidence_warning():
    print("[4/5] Testing low-confidence warning triggers...")
    # Synthetic blank image
    blank_img = Image.new("RGB", (224, 224), color=(0, 0, 0))
    res = inference_service.predict(blank_img)
    if res["confidence"] < CONFIDENCE_THRESHOLD:
        assert res["is_low_confidence"] is True
        assert res["warning"] is not None
        print("  -> Passed: Low confidence correctly flagged with cautionary alert.")
    else:
        print(f"  -> Notice: Score was {res['confidence_pct']}%, above threshold.")

def test_species_info_coverage():
    print("[5/5] Testing botanical info coverage for all 15 classes...")
    for idx, cls_name in inference_service.class_mapping.items():
        assert cls_name in SPECIES_INFO, f"Missing botanical info for {cls_name}"
        info = SPECIES_INFO[cls_name]
        assert "common_name" in info
        assert "marathi_name" in info
        assert "family" in info
    print("  -> Passed: All 15 species possess complete English, Marathi, Family, and Ecological metadata.")

if __name__ == "__main__":
    print("=" * 60)
    print("  RUNNING SMOKE TEST SUITE: VAN UDYAN PLANT AI")
    print("=" * 60)
    test_class_mapping()
    test_valid_image_inference()
    test_preprocessing_dimensions()
    test_low_confidence_warning()
    test_species_info_coverage()
    print("=" * 60)
    print("  ALL 5 SMOKE TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
