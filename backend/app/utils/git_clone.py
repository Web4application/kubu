import os
import shutil
import subprocess
from tempfile import mkdtemp

def clone_repo(git_url: str) -> str:
    """
    Clone a git repository to a temporary directory.
    Returns the path to the cloned repo.
    """
    temp_dir = mkdtemp(prefix="kubu_clone_")
    try:
        subprocess.run(
            ["git", "clone", git_url, temp_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"Failed to clone repo: {e.stderr.decode().strip()}")
