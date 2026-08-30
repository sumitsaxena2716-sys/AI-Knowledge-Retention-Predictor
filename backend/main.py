
import time
from fastapi import FastAPI, HTTPException
from backend.models import LearnerData, QuizRequest
from backend.quiz import generate_quiz
from backend.retention import analyze_retention, fallback_retention_analysis
from backend.storage import init_db, save_analysis, save_alert, save_quiz_feedback, get_at_risk_learners, get_summary
from backend.monitoring import track, metrics

app = FastAPI(
    title="AI Knowledge Retention Predictor",
    description="AI-assisted learning retention analysis, adaptive quiz generation, analytics, and learning feedback.",
    version="2.0.0",
)

init_db()


@app.get("/")
def root():
    return {"message": "AI Knowledge Retention Predictor API is running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "AI Knowledge Retention Predictor API"}


@app.get("/metrics")
def application_metrics():
    return {"service": "AI Knowledge Retention Predictor API", "metrics": metrics()}


@app.get("/analytics/summary")
def analytics_summary():
    return get_summary()


@app.get("/analytics/at-risk")
def at_risk_learners():
    return {"learners": get_at_risk_learners()}


@app.post("/analyze")
def analyze_learner(data: LearnerData):
    started = time.perf_counter()
    payload = data.to_prompt_data()
    try:
        try:
            result = analyze_retention(payload)
            source = "gemini"
        except Exception:
            result = fallback_retention_analysis(data)
            source = "fallback"

        record = save_analysis(payload, result)

        if result["retention_risk"] in {"High", "Medium"}:
            save_alert(
                data.learner_name,
                data.topic,
                f"{result['retention_risk']} retention risk. {result['revision_timing']}",
                result["retention_risk"],
            )

        return {
            "message": "Learner data analyzed successfully",
            "topic": data.topic,
            "quiz_score": float(data.quiz_score),
            "difficulty": data.difficulty,
            "analysis_source": source,
            "record_id": record,
            **result,
        }
    finally:
        track("/analyze", time.perf_counter() - started)


@app.post("/quiz")
def create_quiz(quiz_data: QuizRequest):
    started = time.perf_counter()
    try:
        quiz = generate_quiz(quiz_data.model_dump())
        return {"message": "Quiz generated successfully", "quiz": quiz}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {e}") from e
    finally:
        track("/quiz", time.perf_counter() - started)


@app.post("/quiz/feedback")
def quiz_feedback(payload: dict):
    required = {"topic", "score", "total_questions"}
    if not required.issubset(payload):
        raise HTTPException(status_code=400, detail="topic, score and total_questions are required")
    save_quiz_feedback(
        payload.get("learner_name", ""),
        str(payload["topic"]),
        float(payload["score"]),
        int(payload["total_questions"]),
    )
    return {"message": "Quiz feedback recorded successfully"}
