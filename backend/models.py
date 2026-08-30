from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class LearnerData(BaseModel):
    learner_name: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    last_revision_date: date
    quiz_score: float = Field(..., ge=0, le=100)
    difficulty: Literal["Easy", "Medium", "Hard"]

    def to_prompt_data(self):
        return {
            "learner_name": self.learner_name.strip(),
            "topic": self.topic.strip(),
            "last_revision_date": self.last_revision_date.isoformat(),
            "quiz_score": self.quiz_score,
            "difficulty": self.difficulty,
        }


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty: Literal["Easy", "Medium", "Hard"]
    retention_risk: Literal["Low", "Medium", "High"] = "Medium"
    forgetting_window: str = Field(default="3-5 days", max_length=100)
    revision_timing: str = Field(default="Revise within 3 days", max_length=200)
    study_advice: str = Field(
        default="Review the concept regularly and practice with short quizzes.",
        max_length=500,
    )
    num_questions: int = Field(default=10, ge=5, le=10)
