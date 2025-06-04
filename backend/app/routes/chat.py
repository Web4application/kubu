# backend/app/routes/chat.py

from fastapi import APIRouter, Body
from app.services.llm import ask_llm

router = APIRouter()

@router.post("/")
async def chat_with_ai(data: dict = Body(...)):
    message = data.get("message")
    response = ask_llm(message)
    return {"response": response}
