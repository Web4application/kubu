import os
import zipfile
from typing import Generator, Tuple

# Walk project and yield (file_path, content)
def walk_codebase(root: str) -> Generator[Tuple[str, str], None, None]:
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith((".py", ".js", ".ts", ".json", ".html", ".md", ".yaml")):
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        yield fpath, f.read()
                except Exception as e:
                    print(f"Failed to read {fpath}: {e}")

# Write content to file
def write_file(filepath: str, content: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# Save uploaded zip file and extract
async def extract_repo(uploaded_zip) -> str:
    temp_dir = "/tmp/kubu_project"
    os.makedirs(temp_dir, exist_ok=True)

    zip_path = os.path.join(temp_dir, "repo.zip")
    with open(zip_path, "wb") as f:
        f.write(await uploaded_zip.read())

    extract_path = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path
