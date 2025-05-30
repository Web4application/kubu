from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

app = FastAPI()

# Enable CORS for local development or adjust for production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ActivityRequest(BaseModel):
    activity: str
    repo_url: str

class ChatRequest(BaseModel):
    message: str

@app.post("/activity")
async def handle_activity(request: ActivityRequest):
    # Basic validation & dummy response for demonstration
    activity = request.activity.lower()
    repo_url = request.repo_url

    # Insert real repo processing logic here — e.g., clone, analyze, summarize, etc.
    # For now, respond with a poetic nod to the future:

    if activity == 'analyze':
        result = f"Analyzing repository at {repo_url}... The AI dives deep, unearthing secrets encoded in bytes."
    elif activity == 'summary':
        result = f"Generating a summary for {repo_url}... Wisdom distilled from digital ink flows."
    elif activity == 'upgrade':
        result = f"Upgrading project {repo_url}... Breathing new life into legacy code, future-proof and strong."
    elif activity == 'readme':
        result = f"Creating README for {repo_url}... Your project's story, told clearly and proudly."
    elif activity == 'dependencies':
        result = f"Installing dependencies for {repo_url}... Ensuring every cog fits perfectly in the machine."
    else:
        result = f"Unknown activity: {activity}. Choose wisely, seeker."

    # Simulate async processing
    await asyncio.sleep(1)
    return {"result": result}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_msg = request.message.strip()
    # In real app, here connect to your LLM backend (OpenAI, local LLM, etc)
    # For now, mock a simple echo response with some AI flair:

    reply = f"You asked: '{user_msg}'. The future is bright and full of promise — let's build it together!"

    # Simulate async delay for LLM response
    await asyncio.sleep(0.5)
    return {"reply": reply}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
