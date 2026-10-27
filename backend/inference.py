import time
import json
from pathlib import Path
import numpy as np
from PIL import Image

from backend.config import (
    IMG_HEIGHT,
    IMG_WIDTH,
    CLASS_MAPPING_PATH,
    CONFIDENCE_THRESHOLD,
    SPECIES_INFO
)
from backend.model_loader import ensure_model_available

class ModelInferenceService:
    def __init__(self):
        self.model = None
        self.class_mapping = {}
        self.load_error = None
        self.load_class_mapping()

    def load_class_mapping(self):
        paths = [
            CLASS_MAPPING_PATH,
            Path("class_mapping.json"),
            Path("..") / "class_mapping.json",
            Path(__file__).resolve().parent.parent / "class_mapping.json"
        ]
        for p in paths:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.class_mapping = {int(k): v for k, v in data.items()}
                return
        self.class_mapping = {i: name for i, name in enumerate(sorted(SPECIES_INFO.keys()))}

    def load_model(self):
        if self.model is not None:
            return True, "Model already loaded in memory."
        
        ok, msg, resolved_path = ensure_model_available()
        if not ok or resolved_path is None:
            self.load_error = msg
            return False, msg
        
        try:
            import keras
            self.model = keras.models.load_model(str(resolved_path), compile=False)
            self.load_error = None
            return True, "Model loaded successfully."
        except Exception as e:
            self.load_error = f"Failed to instantiate Keras model from {resolved_path.name}: {str(e)}"
            return False, self.load_error

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Converts PIL image to RGB, resizes to 224x224, and formats float32 [0, 255]
        matching the EfficientNetB0 training pipeline.
        """
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.BILINEAR)
        arr = np.array(image, dtype=np.float32)
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict(self, image: Image.Image, top_k_count: int = 3):
        """
        Executes genuine EfficientNetB0 neural network inference.
        Returns top-K predictions with confidence, botanical taxonomy, zones,
        and inference latency in milliseconds.
        """
        if self.model is None:
            ok, msg = self.load_model()
            if not ok or self.model is None:
                raise RuntimeError(f"Model Inference Unavailable: {self.load_error or msg}")

        start_time = time.perf_counter()
        preprocessed = self.preprocess_image(image)
        raw_output = self.model.predict(preprocessed, verbose=0)[0]
        inference_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        preds = np.array(raw_output, dtype=np.float32)

        if len(preds) != len(self.class_mapping):
            raise ValueError(
                f"Model output dimension mismatch: Model produced {len(preds)} outputs, "
                f"expected {len(self.class_mapping)} classes."
            )

        top_indices = np.argsort(preds)[::-1][:top_k_count]
        top_1_score = float(preds[top_indices[0]])
        is_low_confidence = top_1_score < CONFIDENCE_THRESHOLD

        top_k_results = []
        for idx in top_indices:
            cls_name = self.class_mapping.get(idx, "Unknown")
            info = SPECIES_INFO.get(cls_name, {})
            score = float(preds[idx])
            top_k_results.append({
                "class_name": cls_name,
                "scientific_name": cls_name.replace("_", " "),
                "common_name": info.get("common_name", cls_name),
                "marathi_name": info.get("marathi_name", ""),
                "family": info.get("family", ""),
                "zone": info.get("primary_zone", "Zone 1, 2 or 3"),
                "zones": info.get("zones", ["Zone 1", "Zone 2", "Zone 3"]),
                "ecological_role": info.get("ecological_role", ""),
                "foliage": info.get("foliage", ""),
                "blooming_season": info.get("blooming_season", ""),
                "confidence": round(score, 4),
                "confidence_pct": round(score * 100, 2)
            })

        return {
            "top_k": top_k_results,
            "inference_ms": inference_ms,
            "is_low_confidence": is_low_confidence,
            "warning": (
                "Low Confidence Alert: Top prediction is below 40.0%. "
                "The specimen may not be one of the 15 supported Van Udyan species, "
                "or the leaf lighting/angle may be ambiguous."
                if is_low_confidence else None
            ),
            "is_real_model": True
        }

inference_service = ModelInferenceService()
