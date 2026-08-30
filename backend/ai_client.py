from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_content(prompt: str) -> str:
    try:
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt,
        )

        text = getattr(interaction, "output_text", None)

        if not text:
            raise ValueError("Gemini returned an empty response.")

        return text

    except Exception as e:
        raise RuntimeError(f"AI service failed: {e}") from e