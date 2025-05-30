import os
import uuid
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import asyncio
import subprocess

# Configure OpenAI API key (set env var OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path("/tmp/kubu_projects")
BASE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoURL(BaseModel):
    url: str

# Helper: run shell commands safely
def run_cmd(cmd: str):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        raise Exception(proc.stderr)
    return proc.stdout

async def analyze_project_code(project_path: Path) -> str:
    # Load up to 3 key files for context
    context = ""
    for fname in ["README.md", "main.py", "setup.py"]:
        f = project_path / fname
        if f.exists():
            context += f"\n\n# {fname}\n" + f.read_text()
    prompt = (
        "You are a senior AI dev. Analyze this project and provide:\n"
        "1) A concise summary\n2) Tech stack\n3) Suggested improvements\n\n"
        + context
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

async def generate_readme(project_path: Path) -> str:
    files = [f.name for f in project_path.iterdir() if f.is_file()]
    prompt = f"Write a professional README.md for a project with these files: {', '.join(files)}"
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

@app.post("/clone-analyze")
async def clone_and_analyze(repo: RepoURL):
    project_id = str(uuid.uuid4())
    project_path = BASE_DIR / project_id
    try:
        project_path.mkdir(parents=True, exist_ok=False)
        # Clone repo
        run_cmd(f"git clone {repo.url} {project_path}")
        # Analyze with AI
        analysis = await analyze_project_code(project_path)
        return {"project_id": project_id, "analysis": analysis}
    except Exception as e:
        if project_path.exists():
            shutil.rmtree(project_path)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-readme/{project_id}")
async def generate_project_readme(project_id: str):
    project_path = BASE_DIR / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        readme_text = await generate_readme(project_path)
        readme_path = project_path / "README.md"
        readme_path.write_text(readme_text)
        return {"message": "README.md generated", "content": readme_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
