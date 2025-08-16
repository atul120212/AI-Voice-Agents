import os
import requests
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

FALLBACK_AUDIO_PATH = "/static/fallback.mp3"  # fallback audio file


def call_murf_generate(text: str, voice_id: str = "en-US-natalie") -> str:
    """
    Call Murf API to convert text into speech.
    Returns an audio URL if successful, otherwise returns a fallback path.
    """
    if not MURF_API_KEY:
        logger.warning("Murf API key missing. Returning fallback audio.")
        return FALLBACK_AUDIO_PATH

    headers = {
        "api-key": MURF_API_KEY,
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voiceId": voice_id
    }

    try:
        response = requests.post(
            "https://api.murf.ai/v1/speech/generate",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Try different keys that Murf might return
        audio_file = (
            data.get("audioFile") or
            data.get("audio_url") or
            data.get("audio") or
            data.get("result")
        )

        if audio_file:
            return audio_file
        else:
            logger.error(f"Murf response missing audio field. Response: {data}")
            return FALLBACK_AUDIO_PATH

    except Exception as e:
        logger.error(f"Murf TTS failed: {e}")
        return FALLBACK_AUDIO_PATH
