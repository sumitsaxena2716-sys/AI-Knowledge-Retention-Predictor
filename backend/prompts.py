QUIZ_PROMPT = """
You are an AI Quiz Generator.

Generate exactly 10 multiple-choice questions based on the learner's topic and retention analysis.

Learner Information:
- Topic: {topic}
- Retention Risk: {retention_risk}
- Difficulty: {difficulty}

Rules:
- Generate exactly 10 questions.
- Each question must have exactly 4 options: A, B, C, D.
- Only one option must be correct.
- Questions must be relevant to the given topic.
- Adjust question difficulty according to the learner's difficulty and retention risk.
- Do not include explanations.
- Do not include markdown or code fences.
- Return ONLY valid JSON.

Use exactly this JSON structure:

{{
    "questions": [
        {{
            "question": "string",
            "options": {{
                "A": "string",
                "B": "string",
                "C": "string",
                "D": "string"
            }},
            "correct_answer": "A"
        }}
    ]
}}
"""


def build_quiz_prompt(quiz_data):
    return QUIZ_PROMPT.format(
        topic=quiz_data["topic"],
        retention_risk=quiz_data["retention_risk"],
        difficulty=quiz_data["difficulty"]
    )