import os
import shutil
import tempfile
from git import Repo

async def clone_repo(repo_url: str) -> str:
    tmp_dir = tempfile.mkdtemp(prefix="kubu_repo_")
    Repo.clone_from(repo_url, tmp_dir)
    return tmp_dir
