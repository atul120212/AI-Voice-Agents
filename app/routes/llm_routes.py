from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from services.assemblyai import upload_file as assembly_upload, transcribe
from services.gemini import call_gemini_llm
from services.murf import call_murf_generate
from utils.logger import logger

router = APIRouter()

FALLBACK_AUDIO_PATH = "/static/fallback.mp3"


@router.post("/llm/query")
async def llm_query(
    request: Request,
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Accepts either:
    - text input OR
    - audio file input -> STT -> LLM -> TTS
    """
    try:
        if file:
            try:
                audio_url = assembly_upload(file.file)
                transcription_text = transcribe(audio_url, poll_interval=2.0, timeout=180)
            except Exception as e:
                return JSONResponse(status_code=503, content={
                    "error": "STT failed",
                    "message": str(e),
                    "murf_audio_url": FALLBACK_AUDIO_PATH
                })

            gemini_response_text = call_gemini_llm(transcription_text)
            murf_audio_url = call_murf_generate(gemini_response_text)

            return JSONResponse(status_code=200, content={
                "transcription": transcription_text,
                "llm_text": gemini_response_text,
                "murf_audio_url": murf_audio_url
            })

        # text-only path
        if not text:
            try:
                body = await request.json()
                text = body.get("text")
            except Exception:
                raise HTTPException(status_code=400, detail="No text or file provided")

        gemini_text = call_gemini_llm(text)
        return JSONResponse(status_code=200, content={"response": gemini_text})

    except Exception as e:
        logger.error(f"Unexpected error in /llm/query: {e}")
        return JSONResponse(status_code=500, content={
            "error": "server_error",
            "message": str(e),
            "murf_audio_url": FALLBACK_AUDIO_PATH
        })
