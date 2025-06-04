# backend/app/routes/analyze.py

from fastapi import APIRouter, UploadFile, File, Form
from app.services.summarizer import summarize_repo
from app.utils.file_handler import extract_repo

router = APIRouter()

@router.post("/repo")
async def analyze_repo(file: UploadFile = File(...)):
    path = await extract_repo(file)
    summary = summarize_repo(path)
    return {"summary": summary}
