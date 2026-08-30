
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "retention_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

FEATURES = ["quiz_score", "days_since_revision", "difficulty"]
TARGET = "retention_risk"


def train_retention_model(df):
    from backend.data_pipeline import engineer_features
    data = engineer_features(df)
    if len(data) < 20:
        raise ValueError("At least 20 valid labeled records are recommended for model training.")

    X = data[FEATURES]
    y = data[TARGET]
    if y.nunique() < 2:
        raise ValueError("Training data must contain at least two retention-risk classes.")

    pre = ColumnTransformer([
        ("difficulty", OneHotEncoder(handle_unknown="ignore"), ["difficulty"])
    ], remainder="passthrough")

    pipeline = Pipeline([
        ("preprocess", pre),
        ("classifier", RandomForestClassifier(
            n_estimators=150, random_state=42, class_weight="balanced"
        ))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)

    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision_macro": round(precision_score(y_test, pred, average="macro", zero_division=0), 4),
        "recall_macro": round(recall_score(y_test, pred, average="macro", zero_division=0), 4),
        "f1_macro": round(f1_score(y_test, pred, average="macro", zero_division=0), 4),
    }

    try:
        proba = pipeline.predict_proba(X_test)
        classes = list(pipeline.classes_)
        if len(classes) == 2:
            metrics["auc_roc"] = round(
                roc_auc_score((y_test == classes[1]).astype(int), proba[:, 1]), 4
            )
    except Exception:
        pass

    joblib.dump(pipeline, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def predict_retention(quiz_score, days_since_revision, difficulty):
    if not MODEL_PATH.exists():
        return None
    model = joblib.load(MODEL_PATH)
    frame = pd.DataFrame([{
        "quiz_score": float(quiz_score),
        "days_since_revision": int(days_since_revision),
        "difficulty": difficulty
    }])
    return str(model.predict(frame)[0])
