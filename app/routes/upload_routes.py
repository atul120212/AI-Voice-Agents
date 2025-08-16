from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_audio_file(file: UploadFile = File(...)):
    """ Upload audio and save locally """
    try:
        contents = await file.read()
        save_path = UPLOAD_DIR / file.filename
        with open(save_path, "wb") as f:
            f.write(contents)

        return JSONResponse(status_code=200, content={
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
