"""Train a reproducible Random Forest on clearly labelled demonstration data."""
from pathlib import Path
import sys
import joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from backend.ml.feature_engineering import FEATURE_COLUMNS
def main():
    data = pd.read_csv(ROOT / "dataset.csv")
    missing = set(FEATURE_COLUMNS + ["label"]) - set(data.columns)
    if missing: raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    x, y = data[FEATURE_COLUMNS], data["label"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.25, random_state=42, stratify=y)
    pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", RandomForestClassifier(n_estimators=160, min_samples_leaf=2, random_state=42, class_weight="balanced"))])
    pipeline.fit(x_train, y_train); predictions = pipeline.predict(x_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, predictions, average="binary", zero_division=0)
    print("DEMO DATA metrics — not production performance")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}\nPrecision: {precision:.3f}\nRecall: {recall:.3f}\nF1: {f1:.3f}\nConfusion matrix:\n{confusion_matrix(y_test, predictions)}")
    joblib.dump(pipeline, ROOT / "model.pkl")
if __name__ == "__main__": main()
