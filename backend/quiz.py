import json

from backend.ai_client import generate_content
from backend.prompts import build_quiz_prompt


def _clean_json_response(response: str) -> str:
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def generate_quiz(quiz_data):
    prompt = build_quiz_prompt(quiz_data)
    response = generate_content(prompt)

    try:
        result = json.loads(_clean_json_response(response))
    except json.JSONDecodeError as e:
        raise ValueError("Gemini returned invalid JSON") from e

    if not isinstance(result, dict) or "questions" not in result:
        raise ValueError("Missing questions field")

    questions = result["questions"]
    expected_count = quiz_data.get("num_questions", 10)
    if not isinstance(questions, list) or len(questions) != expected_count:
        raise ValueError(f"Quiz must contain exactly {expected_count} questions")

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be an object")
        required_fields = {"question", "options", "correct_answer"}
        if not required_fields.issubset(question):
            raise ValueError("Each question must contain question, options, and correct_answer")
        options = question["options"]
        if not isinstance(options, dict) or set(options.keys()) != {"A", "B", "C", "D"}:
            raise ValueError("Each question must have exactly 4 options: A, B, C, D")
        if question["correct_answer"] not in {"A", "B", "C", "D"}:
            raise ValueError("Invalid correct answer")
        if not all(isinstance(options[k], str) and options[k].strip() for k in options):
            raise ValueError("All quiz options must be non-empty strings")

    return result
