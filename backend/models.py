from datetime import date
from pydantic import BaseModel, Field


class LearnerData(BaseModel):
    learner_name: str = Field(..., min_length=1)
    topic: str = Field(..., min_length=1)
    last_revision_date: date
    quiz_score: float = Field(..., ge=0, le=100)
    difficulty: str = Field(..., min_length=1)

    def to_prompt_data(self):
        return {
            "learner_name": self.learner_name,
            "topic": self.topic,
            "last_revision_date": self.last_revision_date.isoformat(),
            "quiz_score": self.quiz_score,
            "difficulty": self.difficulty,
        }