from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import requests, time, os
from dotenv import load_dotenv

from services.assemblyai import upload_file as assembly_upload, transcribe
from services.murf import call_murf_generate
from utils.logger import logger

load_dotenv()
ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

router = APIRouter()
FALLBACK_AUDIO_PATH = "/static/fallback.mp3"


@router.post("/transcribe/file")
async def transcribe_audio(file: UploadFile = File(...)):
    """ Transcribe an uploaded audio file """
    try:
        audio_url = assembly_upload(file.file)
        text = transcribe(audio_url, poll_interval=2.0, timeout=180)
        return JSONResponse(status_code=200, content={"transcription": text})
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "murf_audio_url": FALLBACK_AUDIO_PATH})


@router.post("/tts/echo")
async def tts_echo(file: UploadFile = File(...)):
    """ Echo back transcription as Murf TTS """
    try:
        audio_url = assembly_upload(file.file)
        transcription_text = transcribe(audio_url, poll_interval=2.0, timeout=180)
        murf_audio_url = call_murf_generate(transcription_text)

        return JSONResponse(status_code=200, content={
            "transcription": transcription_text,
            "murf_audio_url": murf_audio_url
        })
    except Exception as e:
        logger.error(f"TTS echo error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "murf_audio_url": FALLBACK_AUDIO_PATH})
