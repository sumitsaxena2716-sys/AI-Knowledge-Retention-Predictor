# AI Knowledge Retention Predictor

AI-assisted learning retention and knowledge reinforcement system using Google Gemini, Python, FastAPI, and Streamlit.

## Implemented Features

- Learner name and study concept management
- Last revision date, quiz score, and difficulty tracking
- AI-assisted retention analysis
- Retention risk classification (Low / Medium / High)
- Forgetting-window guidance
- Recommended revision timing
- Personalized study advice
- Concept-wise analysis and concept removal
- Session-state persistence across Streamlit reruns and navigation
- AI-generated 10-question multiple-choice quizzes
- Structured JSON quiz output and validation
- Quiz answer selection, scoring, and question-wise feedback
- Progress indicators, metric cards, risk indicators, and visual analytics
- FastAPI health check and API endpoints
- Environment-variable based Gemini API configuration
- Secure `.env` exclusion through `.gitignore`
- Deployment-oriented dependency and setup documentation

## Project Structure

```text
AI-Knowledge-Retention-Predictor/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   ├── quiz.py
│   ├── retention.py
│   └── ai_client.py
├── frontend/
│   └── app.py
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
- FastAPI
- Uvicorn
- Streamlit
- Internet connection for Gemini API requests

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI-Knowledge-Retention-Predictor
```

Create and activate a virtual environment:

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

Create a `.env` file in the project root using `.env.example` as a guide:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash
BACKEND_API_URL=http://127.0.0.1:8000
```

Keep `.env` private. Never commit or publish the API key.

`GEMINI_MODEL` is configurable so the deployed environment can select an available Gemini model without changing application code.

## Running the Application

### Start Backend

Open a terminal in the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Frontend

Open another terminal in the project root:

```bash
streamlit run frontend/app.py
```

Frontend:

```text
http://localhost:8501
```

## Application Workflow

1. Enter learner information.
2. Add one or more study concepts.
3. Enter the latest quiz score, revision date, and difficulty.
4. Remove a concept when it is no longer needed.
5. Select a concept and run retention analysis.
6. Review the retention dashboard.
7. Generate an AI-powered quiz for the selected/current concept.
8. Answer all quiz questions.
9. Submit the quiz.
10. Review the final score and question-wise feedback.
11. Generate a new quiz when additional practice is required.

## API Endpoints

### GET `/`

Checks whether the backend API is running.

### GET `/health`

Returns a lightweight service-health response for deployment checks.

### POST `/analyze`

Validates learner data and returns:

- Quiz score
- Difficulty
- Retention risk
- Forgetting window
- Recommended revision timing
- Personalized study advice

The primary path uses Gemini for AI-assisted analysis. A deterministic fallback is used if the external AI service is temporarily unavailable.

### POST `/quiz`

Validates the quiz request and generates a topic-specific multiple-choice quiz. The current application requests 10 questions, each with exactly four options (A-D) and one correct answer.

## Testing Checklist

Before deployment, verify:

- Concept addition and validation
- Concept removal
- Concept persistence across reruns/navigation
- Retention analysis
- Retention risk calculation/guidance
- Forgetting window
- Revision timing
- Personalized study advice
- Dashboard metrics and visualizations
- Quiz generation
- Quiz answer selection
- Quiz scoring
- Correct and incorrect feedback
- Backend/frontend communication
- `/health` endpoint
- Invalid API input handling
- Gemini API configuration
- Missing API-key handling

## Security

- Store the Gemini API key only in environment variables.
- Keep `.env` out of version control.
- Do not place API keys directly in Python source files.
- Use deployment-platform secrets/environment variables in staging or production.

## Current Scope vs Future Scope

The current implementation is an AI-assisted retention and quiz application. It does **not** claim to implement a production-scale ML data lake, data warehouse, feature store, model registry, trained classification/sequence/ensemble models, CI/CD pipeline, production monitoring, or automated notification system.

Those advanced components can be added later as the project grows. Possible future enhancements include:

- Persistent learner database and learning history
- Authentication and user profiles
- Historical retention trend analysis
- Trained predictive ML models using longitudinal learner data
- Advanced feature engineering and model evaluation
- Adaptive quiz difficulty based on previous attempts
- Automated revision reminders and notifications
- Cloud deployment with CI/CD
- Monitoring and feedback loops
- Educator/at-risk learner analytics

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Streamlit
- Google Gemini / Google GenAI SDK
- Pydantic
- Plotly
- Requests
- Python-dotenv
