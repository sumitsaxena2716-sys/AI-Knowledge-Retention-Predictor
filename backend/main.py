from fastapi import FastAPI, HTTPException
from backend.models import LearnerData, QuizRequest
from backend.quiz import generate_quiz
from backend.retention import analyze_retention, fallback_retention_analysis


app = FastAPI(
    title="AI Knowledge Retention Predictor",
    description="Backend API for AI-powered knowledge retention analysis and adaptive quiz generation.",
    version="1.1.0",
)


@app.get("/")
def root():
    return {"message": "AI Knowledge Retention Predictor API is running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "AI Knowledge Retention Predictor API"}


@app.post("/analyze")
def analyze_learner(data: LearnerData):
    payload = data.to_prompt_data()

    try:
        # Gemini provides the personalized analysis requested by the project.
        result = analyze_retention(payload)
    except Exception:
        # Keep the core application usable when the external AI service is
        # temporarily unavailable. The fallback is deterministic and clearly
        # based on the learner's supplied score, difficulty, and revision date.
        result = fallback_retention_analysis(data)

    return {
        "message": "Learner data analyzed successfully",
        "topic": data.topic,
        "quiz_score": float(data.quiz_score),
        "difficulty": data.difficulty,
        **result,
    }


@app.post("/quiz")
def create_quiz(quiz_data: QuizRequest):
    try:
        quiz = generate_quiz(quiz_data.model_dump())
        return {"message": "Quiz generated successfully", "quiz": quiz}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {e}") from e
