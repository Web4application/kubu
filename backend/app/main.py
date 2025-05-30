import asyncio
import shutil
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock this down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path("/tmp/kubu_projects")

class RepoURL(BaseModel):
    url: str

async def run_cmd_async(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode().strip()}")
    return stdout.decode().strip()

from services.ai import analyze_project_code

@app.post("/analyze-project/{project_id}")
async def analyze_project(project_id: str):
    project_path = BASE_DIR / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        analysis = await analyze_project_code(project_path)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@app.post("/upgrade-project/{project_id}")
async def upgrade_project(project_id: str):
    project_path = BASE_DIR / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    # TODO: AI-powered upgrade/refactor logic
    return {"message": f"Project {project_id} upgraded (placeholder)."}

@app.post("/generate-readme/{project_id}")
async def generate_readme(project_id: str):
    project_path = BASE_DIR / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    readme_path = project_path / "README.md"
    readme_content = "# Auto-generated README\n\nProject description here."
    readme_path.write_text(readme_content)
    return {"message": "README.md generated."}

@app.post("/install-dependencies/{project_id}")
async def install_dependencies(project_id: str, background_tasks: BackgroundTasks):
    project_path = BASE_DIR / project_id
    requirements_path = project_path / "requirements.txt"

    if not requirements_path.exists():
        raise HTTPException(status_code=404, detail="requirements.txt not found")

    async def install_reqs():
        try:
            logging.info(f"Installing dependencies from {requirements_path}")
            await run_cmd_async(f"pip install -r {requirements_path}")
            logging.info("Dependencies installed successfully.")
        except Exception as e:
            logging.error(f"Dependency installation failed: {e}")

    background_tasks.add_task(install_reqs)
    return {"message": "Installing dependencies in background."}

@app.get("/project-files/{project_id}")
async def list_project_files(project_id: str):
    project_path = BASE_DIR / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    files = [str(path.relative_to(project_path)) for path in project_path.rglob("*") if path.is_file()]
    return {"files": files}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
