from fastapi import APIRouter, HTTPException, Query
from app.utils.git_clone import clone_repo
from app.services.summarizer import summarize_repo
import shutil

router = APIRouter()

@router.get("/clone-analyze")
async def clone_and_analyze_repo(git_url: str = Query(..., description="GitHub repository URL to clone")):
    try:
        repo_path = clone_repo(git_url)
        summary = summarize_repo(repo_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        # Clean up cloned repo
        if 'repo_path' in locals():
            shutil.rmtree(repo_path, ignore_errors=True)

    return {"summary": summary}
