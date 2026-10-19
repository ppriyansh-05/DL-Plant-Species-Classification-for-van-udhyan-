import json
import numpy as np
from PIL import Image
from pathlib import Path
from app.config import (
    IMG_HEIGHT,
    IMG_WIDTH,
    CLASS_MAPPING_PATH,
    CONFIDENCE_THRESHOLD,
    SPECIES_INFO
)
from app.model_loader import ensure_model_available

class ModelInferenceService:
    def __init__(self):
        self.model = None
        self.class_mapping = {}
        self.load_error = None
        self.load_class_mapping()

    def load_class_mapping(self):
        paths = [CLASS_MAPPING_PATH, Path("class_mapping.json"), Path("..") / "class_mapping.json"]
        for p in paths:
            if p.exists():
                with open(p, "r") as f:
                    data = json.load(f)
                    self.class_mapping = {int(k): v for k, v in data.items()}
                return
        from app.config import SPECIES_INFO
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
            # Load the sanitized/verified model archive
            self.model = keras.models.load_model(str(resolved_path), compile=False)
            self.load_error = None
            return True, "Model loaded successfully."
        except Exception as e:
            self.load_error = f"Failed to instantiate Keras model from {resolved_path.name}: {str(e)}"
            return False, self.load_error

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Converts PIL image to RGB, resizes to 224x224, and formats float32 [0, 255]
        matching EfficientNetB0 training pipeline.
        """
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.BILINEAR)
        arr = np.array(image, dtype=np.float32)
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict(self, image: Image.Image):
        """
        Executes actual neural network inference.
        CRITICAL: Never uses fake or pseudo-random fallbacks. If the model is not loaded,
        raises a RuntimeError with a descriptive message so the caller displays an error.
        """
        if self.model is None:
            ok, msg = self.load_model()
            if not ok or self.model is None:
                raise RuntimeError(
                    f"Model Inference Unavailable: {self.load_error or 'Model weights could not be loaded.'}"
                )

        # Run actual neural network inference
        preprocessed = self.preprocess_image(image)
        raw_output = self.model.predict(preprocessed, verbose=0)[0]
        preds = np.array(raw_output, dtype=np.float32)

        if len(preds) != len(self.class_mapping):
            raise ValueError(
                f"Model output dimension mismatch: Model produced {len(preds)} logits/probabilities, "
                f"but class_mapping.json specifies {len(self.class_mapping)} classes."
            )

        # Rank indices
        top_indices = np.argsort(preds)[::-1][:3]
        top_1_idx = top_indices[0]
        top_1_score = float(preds[top_1_idx])
        top_1_class = self.class_mapping.get(top_1_idx, "Unknown")

        top_3 = []
        for idx in top_indices:
            cls_name = self.class_mapping.get(idx, "Unknown")
            info = SPECIES_INFO.get(cls_name, {})
            top_3.append({
                "scientific_name": cls_name.replace("_", " "),
                "raw_class": cls_name,
                "common_name": info.get("common_name", cls_name),
                "marathi_name": info.get("marathi_name", ""),
                "score": float(preds[idx]),
                "confidence_pct": round(float(preds[idx]) * 100, 2)
            })

        is_low_confidence = top_1_score < CONFIDENCE_THRESHOLD
        top_info = SPECIES_INFO.get(top_1_class, {})

        return {
            "predicted_scientific_name": top_1_class.replace("_", " "),
            "raw_class": top_1_class,
            "predicted_common_name": top_info.get("common_name", top_1_class),
            "marathi_name": top_info.get("marathi_name", ""),
            "family": top_info.get("family", ""),
            "ecological_role": top_info.get("ecological_role", ""),
            "confidence": top_1_score,
            "confidence_pct": round(top_1_score * 100, 2),
            "is_low_confidence": is_low_confidence,
            "warning": (
                "Low Confidence Alert: Model score is below 40.0%. "
                "The specimen may not be one of the 15 supported Van Udyan species, or lighting/angle is ambiguous."
                if is_low_confidence else None
            ),
            "top_3_predictions": top_3,
            "is_real_model": True
        }

# Global service instance
inference_service = ModelInferenceService()
