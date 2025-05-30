# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze, upgrade, chat, voice

app = FastAPI(
    title="kubu-hai AI Backend",
    description="A self-improving AI dev agent that analyzes, upgrades, and documents your codebase.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev only – lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(analyze.router, prefix="/analyze")
app.include_router(upgrade.router, prefix="/upgrade")
app.include_router(chat.router, prefix="/chat")
app.include_router(voice.router, prefix="/voice")

@app.get("/")
async def root():
    return {"message": "kubu-hai AI backend is online 🧠"}
