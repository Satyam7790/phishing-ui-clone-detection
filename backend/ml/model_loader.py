import joblib
from backend.config import MODEL_PATH

def load_model():
    return joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
