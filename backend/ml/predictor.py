import pandas as pd
from .model_loader import load_model

def predict_probability(features: dict) -> float:
    model = load_model()
    if model is None:
        raise RuntimeError("ML model not trained. Run: python ml/train.py")
    return round(float(model.predict_proba(pd.DataFrame([features]))[0][1]), 4)
