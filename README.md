# AI Knowledge Retention Predictor

AI-powered learning retention prediction system using Google Gemini, Python, FastAPI, and Streamlit.

## Features

- Learner concept input and management
- AI-powered knowledge retention analysis
- Retention risk prediction
- Forgetting window estimation
- Personalized study advice
- Concept-wise retention dashboard
- AI-generated adaptive quizzes
- Quiz scoring and question-wise feedback
- Progress bars and visual analytics
- Interactive Streamlit interface

## Project Structure

    AI-Knowledge-Retention-Predictor/
    │
    ├── backend/
    │   ├── main.py
    │   ├── models.py
    │   ├── prompts.py
    │   ├── quiz.py
    │   ├── retention.py
    │   └── ai_client.py
    │
    ├── frontend/
    │   └── app.py
    │
    ├── config.py
    ├── test_gemini.py
    ├── requirements.txt
    ├── .env
    ├── .gitignore
    └── README.md

## Requirements

- Python 3.10+
- Google Gemini API key
- FastAPI
- Uvicorn
- Streamlit

## Installation

Clone the repository:

    git clone <repository-url>
    cd AI-Knowledge-Retention-Predictor

Create a virtual environment:

    python -m venv .venv

Activate the virtual environment on Windows:

    .venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

## Environment Configuration

Create a `.env` file in the project root:

    GEMINI_API_KEY=your_gemini_api_key

Keep the `.env` file private. Never commit or publish the API key.

## Running the Application

### Start Backend

Run the FastAPI backend:

    uvicorn backend.main:app --reload --port 8000

Backend URL:

    http://127.0.0.1:8000

### Start Frontend

Open another terminal and run:

    streamlit run frontend/app.py

Frontend URL:

    http://localhost:8501

## Application Workflow

1. Enter learner information.
2. Add a study concept.
3. Enter the latest quiz score and difficulty.
4. Run retention analysis.
5. Review the retention analysis dashboard.
6. Generate an AI-powered quiz.
7. Answer the quiz questions.
8. Submit the quiz.
9. Review the final score and question-wise feedback.

## API Endpoints

### GET `/`

Checks whether the backend API is running.

### POST `/analyze`

Analyzes learner data and returns:

- Quiz score
- Retention risk
- Forgetting window
- Recommended revision timing
- Personalized study advice

### POST `/quiz`

Generates a 10-question AI-powered multiple-choice quiz based on the selected topic and difficulty.

## Testing

Before deployment, verify:

- Concept input and management
- Concept persistence across navigation and reruns
- Retention analysis
- Retention risk calculation
- Forgetting window
- Personalized study advice
- Dashboard visualizations
- Quiz generation
- Quiz answer selection
- Quiz scoring
- Correct and incorrect answer feedback
- Navigation between application sections
- Backend and frontend communication
- Environment variable configuration

## Security

API keys and environment variables must remain private.

The `.env` file is excluded from version control using `.gitignore`.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Streamlit
- Google Gemini
- Pydantic
- Plotly
- Requests