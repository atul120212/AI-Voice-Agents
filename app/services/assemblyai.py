import requests, time, os
from dotenv import load_dotenv

load_dotenv()
ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def upload_file(file_obj) -> str:
    headers = {"authorization": ASSEMBLY_API_KEY}
    resp = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=file_obj)
    resp.raise_for_status()
    return resp.json()["upload_url"]

def transcribe(audio_url: str, poll_interval=2.0, timeout=120) -> str:
    headers = {"authorization": ASSEMBLY_API_KEY}
    transcript_req = {"audio_url": audio_url, "speech_model": "universal"}
    res = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_req, headers=headers)
    res.raise_for_status()
    transcript_id = res.json()["id"]

    polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    elapsed = 0
    while True:
        poll = requests.get(polling_url, headers=headers).json()
        if poll["status"] == "completed":
            return poll["text"]
        if poll["status"] == "error":
            raise RuntimeError(f"Transcription error: {poll['error']}")
        time.sleep(poll_interval)
        elapsed += poll_interval
        if elapsed > timeout:
            raise TimeoutError("Transcription timed out")
