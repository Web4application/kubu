from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess
import os
import shutil
import uuid

app = FastAPI()

BASE_DIR = "/tmp/kubu_projects"  # temp dir for cloning projects

# Helper to run shell commands
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)
    return result.stdout

# Models
class RepoUrl(BaseModel):
    git_url: str

@app.post("/clone-analyze")
async def clone_and_analyze(repo: RepoUrl):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(BASE_DIR, project_id)
    try:
        os.makedirs(project_path, exist_ok=True)
        run_cmd(f"git clone {repo.git_url} {project_path}")
        # TODO: Add your AI analyze logic here to summarize and understand project
        summary = f"Project cloned at {project_path}. (AI analysis placeholder)"
        return {"summary": summary, "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upgrade-project/{project_id}")
async def upgrade_project(project_id: str):
    project_path = os.path.join(BASE_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    # TODO: Add AI-powered refactor/upgrade logic here
    return {"message": f"Project {project_id} upgraded (placeholder)."}

@app.post("/generate-readme/{project_id}")
async def generate_readme(project_id: str):
    project_path = os.path.join(BASE_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    # TODO: AI generate README.md content and write to project folder
    readme_content = "# Auto-generated README\n\nProject description here."
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(readme_content)
    return {"message": "README.md generated."}

@app.post("/install-dependencies/{project_id}")
async def install_dependencies(project_id: str, background_tasks: BackgroundTasks):
    project_path = os.path.join(BASE_DIR, project_id)
    requirements_path = os.path.join(project_path, "requirements.txt")
    if not os.path.exists(requirements_path):
        raise HTTPException(status_code=404, detail="requirements.txt not found")
    
    def install_reqs():
        run_cmd(f"pip install -r {requirements_path}")

    background_tasks.add_task(install_reqs)
    return {"message": "Installing dependencies in background."}

@app.get("/project-files/{project_id}")
async def list_project_files(project_id: str):
    project_path = os.path.join(BASE_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")

    file_list = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            rel_dir = os.path.relpath(root, project_path)
            rel_file = os.path.join(rel_dir, file) if rel_dir != "." else file
            file_list.append(rel_file)
    return {"files": file_list}
