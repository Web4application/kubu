# backend/app/routes/voice.py

from fastapi import APIRouter, UploadFile, File
from app.services.voice import transcribe_audio, synthesize_text

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    text = transcribe_audio(file)
    return {"text": text}

@router.post("/speak")
async def speak(data: dict):
    text = data.get("text", "")
    audio_url = synthesize_text(text)
    return {"audio_url": audio_url}
