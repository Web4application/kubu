from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from services.analyzer import analyze_repo

router = APIRouter()

class RepoInput(BaseModel):
    url: HttpUrl

@router.post("/analyze")
async def analyze(input: RepoInput):
    try:
        result = await analyze_repo(input.url)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
