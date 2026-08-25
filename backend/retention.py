import json

from backend.prompts import build_retention_prompt
from backend.ai_client import generate_content


REQUIRED_FIELDS = [
    "retention_risk",
    "forgetting_window",
    "revision_timing",
    "study_advice"
]


def analyze_retention(learner_data):
    prompt = build_retention_prompt(learner_data)

    response = generate_content(prompt)

    # Remove markdown code fences if Gemini adds them
    cleaned_response = response.strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]

    cleaned_response = cleaned_response.strip()

    result = json.loads(cleaned_response)

    # Validate required fields
    for field in REQUIRED_FIELDS:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")

    return result