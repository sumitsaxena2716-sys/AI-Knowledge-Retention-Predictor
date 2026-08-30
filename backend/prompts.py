RETENTION_PROMPT = """
You are an AI Knowledge Retention Analyzer.

Analyze the learner's study information and estimate their knowledge retention.

Learner Information:
- Learner Name: {learner_name}
- Topic: {topic}
- Last Revision Date: {last_revision_date}
- Quiz Score: {quiz_score}
- Difficulty: {difficulty}

Based on this information, determine:
1. Retention risk
2. Estimated forgetting window
3. Recommended revision timing
4. Personalized study advice

Return ONLY valid JSON.
Do not include markdown, explanations, or code fences.

Use exactly this JSON structure:

{{
    "retention_risk": "Low | Medium | High",
    "forgetting_window": "string",
    "revision_timing": "string",
    "study_advice": "string"
}}
"""


def build_retention_prompt(learner_data):
    return RETENTION_PROMPT.format(
        learner_name=learner_data["learner_name"],
        topic=learner_data["topic"],
        last_revision_date=learner_data["last_revision_date"],
        quiz_score=learner_data["quiz_score"],
        difficulty=learner_data["difficulty"]
    )


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