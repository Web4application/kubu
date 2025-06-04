import os
import uuid
import asyncio
import shutil
import subprocess
from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS — tighten this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "/tmp/kubu_projects"
os.makedirs(BASE_DIR, exist_ok=True)

# --- Models ---
class RepoUrl(BaseModel):
    git_url: str

# --- Helper: Async shell command streaming ---
async def run_cmd_stream(cmd: str, websocket: WebSocket):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        await websocket.send_text(line.decode().strip())
    await process.wait()
    if process.returncode != 0:
        error = (await process.stderr.read()).decode()
        await websocket.send_text(f"ERROR: {error}")
        raise Exception(f"Command failed: {error}")

# --- Clone + Analyze: WebSocket Streaming ---
@app.websocket("/ws/clone")
async def websocket_clone(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        git_url = data.get("git_url")
        if not git_url:
            await websocket.send_text("ERROR: 'git_url' required")
            return

        project_id = str(uuid.uuid4())
        project_path = os.path.join(BASE_DIR, project_id)
        os.makedirs(project_path, exist_ok=True)

        await websocket.send_text(f"Cloning repo {git_url} into {project_path}...\n")
        await run_cmd_stream(f"git clone {git_url} {project_path}", websocket)

        await websocket.send_text("Starting AI analysis...\n")
        for i in range(5):  # Simulate streaming progress
            await asyncio.sleep(1)
            await websocket.send_text(f"Analyzing... step {i+1}/5")

        await websocket.send_text("✅ Analysis complete!")
    except Exception as e:
        await websocket.send_text(f"❌ Exception: {str(e)}")
    finally:
        await websocket.close()

# --- Basic Chat Echo WebSocket ---
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            response = f"Echo: {message}"
            await websocket.send_text(response)
    except Exception:
        await websocket.close()

# --- Synchronous Git Clone ---
def clone_repo(git_url: str, destination: str):
    result = subprocess.run(["git", "clone", git_url, destination],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)

# --- Background AI Task ---
async def analyze_and_upgrade_project(project_path: str):
    await asyncio.sleep(5)
    with open(os.path.join(project_path, "analysis.log"), "w") as f:
        f.write("AI Analysis complete.\n")

# --- Clone + Analyze Background Task Endpoint ---
@app.post("/clone-and-analyze")
async def clone_and_analyze_repo(repo: RepoUrl, background_tasks: BackgroundTasks):
    git_url = repo.git_url
    project_id = str(uuid.uuid4())
    project_path = os.path.join(BASE_DIR, project_id)

    try:
        os.makedirs(project_path, exist_ok=True)
        clone_repo(git_url, project_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    background_tasks.add_task(analyze_and_upgrade_project, project_path)
    return {"message": "✅ Cloned and analysis started", "project_id": project_id}
