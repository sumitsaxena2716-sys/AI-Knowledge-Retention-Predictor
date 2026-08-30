from fastapi import FastAPI, HTTPException
from backend.models import LearnerData
from backend.quiz import generate_quiz


app = FastAPI(
    title="AI Knowledge Retention Predictor",
    description="Backend API for AI-powered knowledge retention analysis and adaptive quiz generation.",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("AI Knowledge Retention Predictor API started.")


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Retention Predictor API is running"
    }


# =========================================================
# RETENTION ANALYSIS
# =========================================================

@app.post("/analyze")
def analyze_learner(data: LearnerData):

    quiz_score = float(data.quiz_score)
    difficulty = str(data.difficulty).lower()

    # Calculate retention risk
    if quiz_score < 50:

        retention_risk = "High"
        forgetting_window = "1-2 days"
        revision_timing = "Revise today and again within 2 days"

        study_advice = (
            "Focus on weak areas and use active recall with short practice sessions."
        )

    elif quiz_score < 80:

        retention_risk = "Medium"
        forgetting_window = "3-5 days"
        revision_timing = "Revise within 3 days"

        study_advice = (
            "Review the concept regularly and practice with short quizzes."
        )

    else:

        retention_risk = "Low"
        forgetting_window = "7-10 days"
        revision_timing = "Revise within 7 days"

        study_advice = (
            "Your mastery is strong. Use spaced repetition to maintain retention."
        )

    # Adjust risk based on difficulty
    if difficulty == "hard" and quiz_score < 90:

        if retention_risk == "Low":
            retention_risk = "Medium"

    return {
        "message": "Learner data analyzed successfully",
        "topic": data.topic,
        "quiz_score": quiz_score,
        "difficulty": data.difficulty,
        "retention_risk": retention_risk,
        "forgetting_window": forgetting_window,
        "revision_timing": revision_timing,
        "study_advice": study_advice
    }

# =========================================================
# QUIZ GENERATION
# =========================================================

@app.post("/quiz")
def create_quiz(quiz_data: dict):

    try:

        # Add retention information if it is not provided
        if "retention_risk" not in quiz_data:
            quiz_data["retention_risk"] = "Medium"

        if "forgetting_window" not in quiz_data:
            quiz_data["forgetting_window"] = "3-5 days"

        if "revision_timing" not in quiz_data:
            quiz_data["revision_timing"] = "Revise within 3 days"

        if "study_advice" not in quiz_data:
            quiz_data["study_advice"] = (
                "Review the concept regularly and practice with short quizzes."
            )

        quiz = generate_quiz(quiz_data)

        return {
            "message": "Quiz generated successfully",
            "quiz": quiz
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {str(e)}"
        )