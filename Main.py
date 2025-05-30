import torch
from cpufeature import CPUFeature
from petals.constants import PUBLIC_INITIAL_PEERS
import cronitor
from dataclasses import dataclass
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import os
import subprocess
from typing import List
import asyncio

app = FastAPI()

# Enable CORS for your frontend domain during dev or prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    repo_url: HttpUrl

class AnalysisResponse(BaseModel):
    summary: str
    files: List[str]
    upgrade_status: str

def list_files(start_path):
    files = []
    for root, _, filenames in os.walk(start_path):
        for fname in filenames:
            rel_path = os.path.relpath(os.path.join(root, fname), start_path)
            files.append(rel_path)
    return files

@app.post("/api/start-analysis", response_model=AnalysisResponse)
async def start_analysis(req: AnalysisRequest):
    tmp_dir = tempfile.mkdtemp(prefix="repo_")
    try:
        # Clone the repo (shallow, single branch for speed)
        clone_cmd = ["git", "clone", "--depth", "1", req.repo_url, tmp_dir]
        proc = await asyncio.create_subprocess_exec(*clone_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Git clone failed: {stderr.decode().strip()}")

        files = list_files(tmp_dir)

        # Dummy summary and upgrade_status — replace with your AI/analysis logic
        summary = f"Repository at {req.repo_url} has {len(files)} files."
        upgrade_status = "No upgrades detected (placeholder)."

        return AnalysisResponse(summary=summary, files=files, upgrade_status=upgrade_status)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

# Define the ModelInfo data class
@dataclass
class ModelInfo:
    repo: str
    adapter: Optional[str] = None

# List of models with versioning
MODELS = [
    ModelInfo(repo="meta-llama/Llama-2-70b-chat-hf"),
    ModelInfo(repo="stabilityai/StableBeluga2"),
    ModelInfo(repo="enoch/llama-65b-hf"),
    ModelInfo(repo="enoch/llama-65b-hf", adapter="timdettmers/guanaco-65b"),
    ModelInfo(repo="bigscience/bloomz"),
]
DEFAULT_MODEL_NAME = "web4/AI"

# Initial peers for network connection
INITIAL_PEERS = PUBLIC_INITIAL_PEERS

# Device and data type configuration
DEVICE = "cpu"
if DEVICE == "cuda":
    TORCH_DTYPE = "auto"
elif CPUFeature["AVX512f"] and CPUFeature["OS_AVX512"]:
    TORCH_DTYPE = torch.bfloat16
else:
    TORCH_DTYPE = torch.float32

STEP_TIMEOUT = 5 * 60
MAX_SESSIONS = 50

# Cronitor setup
monitor = cronitor.Monitor('important-background-job')

# Function to perform the background job
async def perform_job():
    try:
        # Notify Cronitor that the job has started
        monitor.ping(state='run')

        print('Running background job with monitoring!')

        # Simulate job processing
        await asyncio.sleep(2)  # Sleep for 2 seconds

        # Notify Cronitor that the job has completed successfully
        monitor.ping(state='complete')
    except Exception as error:
        # Notify Cronitor that the job has failed
        monitor.ping(state='fail')

        # Log the error
        print('Job failed:', error)

# Wrap the job function with Cronitor monitoring
async def main():
    cronitor.wrap('important-background-job', perform_job)
    await perform_job()

# Execute the job
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
