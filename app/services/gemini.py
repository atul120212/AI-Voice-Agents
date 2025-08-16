import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

FALLBACK_TEXT = "I'm having trouble connecting right now. Please try again later."

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def call_gemini_llm(prompt_text: str) -> str:
    """
    Call Google Gemini LLM to generate a response.
    Returns fallback text if the API fails or key is missing.
    """
    if not GEMINI_API_KEY:
        logger.warning("Gemini API key missing. Returning fallback text.")
        return FALLBACK_TEXT

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt_text)

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return str(response)

    except Exception as e:
        logger.error(f"Gemini call failed: {e}")
        return FALLBACK_TEXT
