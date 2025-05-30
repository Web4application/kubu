import subprocess
import os

def install_requirements(requirements_path: str):
    if not os.path.exists(requirements_path):
        print("No requirements.txt found.")
        return False

    try:
        subprocess.run(
            ["pip", "install", "-r", requirements_path],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")
        return False
