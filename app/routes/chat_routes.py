from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from services.assemblyai import upload_file as assembly_upload, transcribe
from services.gemini import call_gemini_llm
from services.murf import call_murf_generate
from utils.logger import logger

router = APIRouter()

FALLBACK_AUDIO_PATH = "/static/fallback.mp3"
chat_sessions = {}  # session store


@router.post("/agent/chat/{session_id}")
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    try:
        audio_url = assembly_upload(file.file)
        transcription_text = transcribe(audio_url, poll_interval=2.0, timeout=180)

        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

        chat_sessions[session_id].append({"role": "user", "content": transcription_text})

        # build prompt
        prompt = "\n".join(
            [f"{'User' if msg['role']=='user' else 'Assistant'}: {msg['content']}"
             for msg in chat_sessions[session_id]]
        ) + "\nAssistant:"

        gemini_response_text = call_gemini_llm(prompt)
        chat_sessions[session_id].append({"role": "assistant", "content": gemini_response_text})

        murf_audio_url = call_murf_generate(gemini_response_text)

        return JSONResponse(status_code=200, content={
            "transcription": transcription_text,
            "llm_text": gemini_response_text,
            "murf_audio_url": murf_audio_url,
            "history": chat_sessions[session_id]
        })

    except Exception as e:
        logger.error(f"Unexpected error in /agent/chat: {e}")
        return JSONResponse(status_code=500, content={
            "error": "server_error",
            "message": str(e),
            "murf_audio_url": FALLBACK_AUDIO_PATH
        })
