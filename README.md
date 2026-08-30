# AI Knowledge Retention Predictor

AI-assisted learning retention and knowledge reinforcement system using Google Gemini, FastAPI, Streamlit, Plotly, SQLite, and an optional machine-learning pipeline.

## Current Application Features

- Learner and study concept management
- Last revision date, quiz score, and difficulty tracking
- Gemini-assisted retention analysis
- Retention risk, forgetting-window, revision timing, and study advice
- Deterministic fallback when Gemini is unavailable
- AI-generated 10-question MCQ quizzes
- Structured JSON output and validation
- Quiz scoring and feedback
- Session-state persistence
- Dashboard metrics, progress indicators, and visual analytics
- SQLite learning-history storage
- At-risk learner analytics endpoint
- In-app retention alerts
- Health and application metrics endpoints
- Secure environment-variable configuration

## Advanced Architecture Support

The project also includes implementation-ready components for the broader architecture:

- CSV ingestion, cleaning, and feature engineering
- Optional Random Forest retention classifier
- Accuracy, precision, recall, F1, and AUC-ROC evaluation when a suitable labeled dataset is supplied
- Local data-lake / warehouse / feature-store directory structure
- Model-registry structure for trained artifacts
- Runtime monitoring metrics
- GitHub Actions CI validation

These advanced ML/data-engineering components are intentionally data-driven. The application does not fabricate training results or claim that a production ML model has been trained without a real labeled dataset.

## Project Structure

```text
AI-Knowledge-Retention-Predictor/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   ├── quiz.py
│   ├── retention.py
│   ├── ai_client.py
│   ├── storage.py
│   ├── data_pipeline.py
│   ├── ml_model.py
│   └── monitoring.py
├── frontend/
│   └── app.py
├── data/
│   ├── lake/raw/
│   ├── warehouse/
│   ├── feature_store/
│   └── retention_dataset_template.csv
├── models/
│   └── registry/
├── .github/workflows/ci.yml
├── config.py
├── test_gemini.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- Google Gemini API key
- Internet connection for Gemini requests

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create `.env` in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
BACKEND_API_URL=http://127.0.0.1:8000
```

Never commit `.env` or expose the API key.

## Running the Application

Backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Frontend, in another terminal:

```bash
streamlit run frontend/app.py
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Streamlit:

```text
http://localhost:8501
```

## API Endpoints

- `GET /` — service status
- `GET /health` — deployment health check
- `GET /metrics` — lightweight runtime request/latency metrics
- `GET /analytics/summary` — learning-history summary
- `GET /analytics/at-risk` — recent medium/high-risk records
- `POST /analyze` — retention analysis
- `POST /quiz` — AI quiz generation
- `POST /quiz/feedback` — store quiz performance feedback

## Data and ML Pipeline

Use `data/retention_dataset_template.csv` as a schema reference. A real labeled dataset should contain:

- learner_name
- topic
- last_revision_date
- quiz_score
- difficulty
- retention_risk

The pipeline cleans missing/invalid records and creates features such as days since revision and difficulty score.

To train the optional retention model:

```python
import pandas as pd
from backend.data_pipeline import clean_data, engineer_features
from backend.ml_model import train_retention_model

df = pd.read_csv("data/your_labeled_dataset.csv")
metrics = train_retention_model(df)
print(metrics)
```

The resulting evaluation includes accuracy, macro precision, macro recall, macro F1, and AUC-ROC when binary-class probabilities permit it.

## Security

- Store API keys only in environment variables.
- Keep `.env` out of version control.
- Do not hard-code secrets.
- Use deployment-platform secrets for staging/production.
- SQLite is suitable for this project/demo; a managed database is recommended for production scale.

## Testing

Check:

- Concept add/remove and persistence
- Retention analysis
- Gemini and fallback paths
- Dashboard visualization
- Quiz generation and validation
- Quiz scoring
- API error handling
- `/health` and `/metrics`
- Analytics storage
- Invalid input validation
- CI syntax/compile checks

## Scope and Future Expansion

The current code implements the core AI learning workflow plus practical storage, analytics, monitoring, and an optional ML pipeline. Large-scale LMS ingestion, managed data lakes/warehouses, distributed feature stores, cloud model registries, external notification providers, and full production observability require deployment infrastructure and real organizational data. They are represented by the project structure and extension points rather than being falsely presented as already deployed.

## Technology Stack

Python, FastAPI, Uvicorn, Streamlit, Google Gemini, Pydantic, Plotly, Requests, Python-dotenv, SQLite, Pandas, Scikit-learn, Joblib, GitHub Actions.
