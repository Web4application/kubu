from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import openai
import asyncio

app = FastAPI()

openai.api_key = "YOUR_OPENAI_API_KEY"  # Secure this for prod!

class AnalysisRequest(BaseModel):
    repo_url: str = None
    files: List[str] = []

@app.post("/analyze")
async def analyze_repo(repo_url: str = Form(None), files: List[UploadFile] = File([])):
    # For brevity, let's pretend we clone and parse the repo or process files here.
    code_samples = []
    for f in files:
        content = await f.read()
        code_samples.append(content.decode())

    # Compose prompt to analyze code samples or repo URL.
    prompt = f"Analyze this repo: {repo_url}\nFiles:\n" + "\n---\n".join(code_samples)

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert AI code analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.3,
    )

    analysis = response.choices[0].message.content
    return {"analysis": analysis}
