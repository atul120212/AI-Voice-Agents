from pydantic import BaseModel
from typing import List, Dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    transcription: str
    llm_text: str
    murf_audio_url: str
    history: List[Dict[str, str]]
