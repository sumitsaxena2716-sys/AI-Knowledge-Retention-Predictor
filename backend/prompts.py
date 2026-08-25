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