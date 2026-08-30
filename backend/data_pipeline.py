
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "learner_name", "topic", "last_revision_date",
    "quiz_score", "difficulty", "retention_risk"
}


def ingest_csv(csv_path):
    df = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing))}")
    return clean_data(df)


def clean_data(df):
    result = df.copy()
    result["learner_name"] = result["learner_name"].astype(str).str.strip()
    result["topic"] = result["topic"].astype(str).str.strip()
    result["quiz_score"] = pd.to_numeric(result["quiz_score"], errors="coerce")
    result["last_revision_date"] = pd.to_datetime(
        result["last_revision_date"], errors="coerce"
    )
    result["difficulty"] = result["difficulty"].astype(str).str.title()
    result["retention_risk"] = result["retention_risk"].astype(str).str.title()
    result = result.dropna(subset=[
        "learner_name", "topic", "quiz_score",
        "last_revision_date", "difficulty", "retention_risk"
    ])
    result = result[result["quiz_score"].between(0, 100)]
    return result.reset_index(drop=True)


def engineer_features(df):
    result = df.copy()
    today = pd.Timestamp.today().normalize()
    result["days_since_revision"] = (today - result["last_revision_date"]).dt.days.clip(lower=0)
    result["difficulty_score"] = result["difficulty"].map({
        "Easy": 1, "Medium": 2, "Hard": 3
    }).fillna(2)
    return result
