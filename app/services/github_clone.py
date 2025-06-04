import subprocess
import os

def clone_repo(git_url: str, dest_path: str):
    if os.path.exists(dest_path):
        raise Exception(f"Destination path '{dest_path}' already exists.")
    os.makedirs(dest_path, exist_ok=True)
    try:
        subprocess.run(
            f"git clone {git_url} {dest_path}",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git clone failed: {e.stderr}")
