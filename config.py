import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")
