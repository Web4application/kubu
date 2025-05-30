# backend/main.py
import asyncio
import uuid
import os
import subprocess
from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS, tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "/tmp/kubu_projects"

class RepoUrl(BaseModel):
    git_url: str

async def run_cmd_stream(cmd, websocket: WebSocket):
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
        err = (await process.stderr.read()).decode()
        await websocket.send_text(f"ERROR: {err}")
        raise Exception(f"Command failed: {err}")

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
        for i in range(5):
            await asyncio.sleep(1)
            await websocket.send_text(f"Analyzing... step {i+1}/5")

        await websocket.send_text("Analysis complete! 🎉")
    except Exception as e:
        await websocket.send_text(f"Exception: {str(e)}")
    finally:
        await websocket.close()

@app.post("/clone-analyze")
async def clone_analyze_background(repo: RepoUrl, background_tasks: BackgroundTasks):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(BASE_DIR, project_id)
    try:
        os.makedirs(project_path, exist_ok=True)
        subprocess.run(f"git clone {repo.git_url} {project_path}", shell=True, check=True)
        background_tasks.add_task(dummy_ai_analysis, project_path)
        return {"message": "Cloning done. AI analysis started in background.", "project_id": project_id}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Git clone failed: {e.stderr}")

async def dummy_ai_analysis(project_path):
    await asyncio.sleep(5)
    print(f"AI analysis completed on {project_path}")
