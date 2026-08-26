import json

from backend.prompts import build_quiz_prompt
from backend.ai_client import generate_content


def generate_quiz(quiz_data):
    prompt = build_quiz_prompt(quiz_data)

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

    try:
        result = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError("Gemini returned invalid JSON") from e

    # Validate quiz structure
    if "questions" not in result:
        raise ValueError("Missing questions field")

    questions = result["questions"]

    if not isinstance(questions, list):
        raise ValueError("Questions must be a list")

    if len(questions) != 10:
        raise ValueError("Quiz must contain exactly 10 questions")

    for question in questions:
        required_fields = ["question", "options", "correct_answer"]

        for field in required_fields:
            if field not in question:
                raise ValueError(f"Missing field: {field}")

        if not isinstance(question["options"], dict):
            raise ValueError("Options must be an object")

        if set(question["options"].keys()) != {"A", "B", "C", "D"}:
            raise ValueError("Each question must have exactly 4 options: A, B, C, D")

        if question["correct_answer"] not in {"A", "B", "C", "D"}:
            raise ValueError("Invalid correct answer")

    return result