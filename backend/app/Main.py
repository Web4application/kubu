from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

app = FastAPI()

# Allow frontend to connect (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class RepoRequest(BaseModel):
    repoUrl: str

@app.post("/api/analyzeRepo")
async def analyze_repo(request: RepoRequest):
    if not request.repoUrl.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    prompt = f"Analyze this GitHub repo for code quality and security issues, and provide recommendations:\n{request.repoUrl}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        summary = response.choices[0].message.content
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
