from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from i18n import detect_language, get_translator
from pydantic import BaseModel
from typing import Optional
import subprocess
import os
import shutil
import openai

app = FastAPI()

# Configure your OpenAI key or environment variables here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple model for repo info input
class RepoRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"

# Path to temp clone repos (make sure this exists)
CLONE_BASE_DIR = "/tmp/repos"

def run_command(cmd, cwd=None):
    """Run shell command, return output or raise."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def clone_repo(repo_url: str, branch: str) -> str:
    """Clone repo to temp directory, return path."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    target_dir = os.path.join(CLONE_BASE_DIR, repo_name)
    # Clean up previous clone if exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    # Clone repo
    run_command(f"git clone --branch {branch} {repo_url} {target_dir}")
    return target_dir

def analyze_repo(path: str) -> dict:
    """Stub for repo analysis - insert your static analysis here."""
    # Example: count files, count lines of code, check dependencies
    file_count = int(run_command("find . -type f | wc -l", cwd=path))
    return {"file_count": file_count, "repo_path": path}

def call_openai(prompt: str) -> str:
    """Call OpenAI GPT with a prompt, return text completion."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or your preferred model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

@app.post("/analyze")
async def analyze_endpoint(repo: RepoRequest):
    try:
        path = clone_repo(repo.repo_url, repo.branch)
        analysis = analyze_repo(path)
        # Cleanup repo after analysis to save space
        shutil.rmtree(path)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summary")
async def summary_endpoint(repo: RepoRequest):
    try:
        path = clone_repo(repo.repo_url, repo.branch)
        # Simple placeholder prompt - replace with smarter logic!
        prompt = f"Summarize the repository at {repo.repo_url}. Key points: code quality, structure, and functionality."
        summary = call_openai(prompt)
        shutil.rmtree(path)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upgrade")
async def upgrade_endpoint(repo: RepoRequest):
    try:
        path = clone_repo(repo.repo_url, repo.branch)
        prompt = f"Based on the repo at {repo.repo_url}, suggest improvements and upgrades for code quality, dependencies, and features."
        upgrade_suggestions = call_openai(prompt)
        shutil.rmtree(path)
        return {"upgrades": upgrade_suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/advanced")
async def advanced_page(request: Request):
    lang = detect_language(request)
    translator = get_translator(lang)
    _ = translator.gettext
    return {
        "language": lang,
        "message": _(f"Welcome to the advanced Kubuverse page!")
    }
