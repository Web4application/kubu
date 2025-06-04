# backend/app/routes/upgrade.py

from fastapi import APIRouter, Body
from app.services.upgrader import upgrade_codebase

router = APIRouter()

@router.post("/")
async def run_upgrade(data: dict = Body(...)):
    repo_path = data.get("path")
    result = upgrade_codebase(repo_path)
    return {"upgraded": result}
