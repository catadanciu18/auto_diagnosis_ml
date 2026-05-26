import os
import joblib
from app.utils.feature_builder import build_feature_frame
from config import MODEL_PATH, LABEL_ENCODER_PATH, TOP_N_PREDICTIONS


model = None
label_encoder = None


def load_model():
    global model, label_encoder

    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Modelul nu există. Rulează train_model.py mai întâi.")
        model = joblib.load(MODEL_PATH)

    if label_encoder is None:
        if not os.path.exists(LABEL_ENCODER_PATH):
            raise FileNotFoundError("Label encoder lipsește.")
        label_encoder = joblib.load(LABEL_ENCODER_PATH)


def predict_faults(payload: dict, top_n: int = 2):
    load_model()

    X = build_feature_frame(payload)

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0]

        results = []
        for idx, prob in enumerate(proba):
            label = label_encoder.inverse_transform([idx])[0]
            results.append({
                "fault": label,
                "probability": float(prob)
            })


        results.sort(key=lambda x: x["probability"], reverse=True)

        return results[:top_n]


    pred = model.predict(X)[0]
    label = label_encoder.inverse_transform([pred])[0]

    return [{
        "fault": label,
        "probability": 1.0
    }]