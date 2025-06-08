import tempfile
import subprocess

async def clone_repo(url: str) -> str:
    path = tempfile.mkdtemp()
    subprocess.run(["git", "clone", url, path], check=True)
    return path
