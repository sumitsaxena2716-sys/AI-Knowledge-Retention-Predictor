import os

from google import genai

from config import GEMINI_API_KEY


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_content(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if not text:
            raise ValueError("Gemini returned an empty response.")
        return text
    except Exception as e:
        raise RuntimeError(f"AI service failed: {e}") from e
