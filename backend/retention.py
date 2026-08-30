import json
from datetime import date

from backend.ai_client import generate_content
from backend.prompts import build_retention_prompt


REQUIRED_FIELDS = {
    "retention_risk",
    "forgetting_window",
    "revision_timing",
    "study_advice",
}
VALID_RISKS = {"Low", "Medium", "High"}


def _clean_json_response(response: str) -> str:
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def _validate_result(result: dict) -> dict:
    if not isinstance(result, dict):
        raise ValueError("Gemini returned an invalid analysis object")
    missing = REQUIRED_FIELDS - result.keys()
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")
    if result["retention_risk"] not in VALID_RISKS:
        raise ValueError("Invalid retention risk")
    for field in ("forgetting_window", "revision_timing", "study_advice"):
        if not isinstance(result[field], str) or not result[field].strip():
            raise ValueError(f"Invalid {field}")
    return result


def analyze_retention(learner_data):
    response = generate_content(build_retention_prompt(learner_data))
    try:
        result = json.loads(_clean_json_response(response))
    except json.JSONDecodeError as e:
        raise ValueError("Gemini returned invalid JSON for retention analysis") from e
    return _validate_result(result)


def fallback_retention_analysis(data) -> dict:
    """Deterministic fallback so the API remains useful during AI outages."""
    score = float(data.quiz_score)
    days_since_revision = max(0, (date.today() - data.last_revision_date).days)

    if score < 50 or days_since_revision > 14:
        risk = "High"
        window = "1-2 days"
        timing = "Revise today and again within 2 days"
        advice = "Focus on weak areas and use active recall with short practice sessions."
    elif score < 80 or (data.difficulty == "Hard" and score < 90) or days_since_revision > 7:
        risk = "Medium"
        window = "3-5 days"
        timing = "Revise within 3 days"
        advice = "Review the concept regularly and practice with short quizzes."
    else:
        risk = "Low"
        window = "7-10 days"
        timing = "Revise within 7 days"
        advice = "Your mastery is strong. Use spaced repetition to maintain retention."

    return {
        "retention_risk": risk,
        "forgetting_window": window,
        "revision_timing": timing,
        "study_advice": advice,
    }
