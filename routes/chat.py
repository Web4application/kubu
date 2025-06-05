from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_chat import query_llm

router = APIRouter()

class ChatInput(BaseModel):
    message: str

@router.post("/chat")
async def chat(input: ChatInput):
    reply = await query_llm(input.message)
    return {"reply": reply}
