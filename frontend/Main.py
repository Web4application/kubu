import os
import shutil
import tempfile
import json
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Make sure to set your OpenAI API key as env variable before running:
# export OPENAI_API_KEY="your_api_key_here"
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="KubuHai AI Repo Analyzer")

class RepoRequest(BaseModel):
    repo_url: str
    max_files: int = 10
    max_file_size_kb: int = 100  # max size per file to include (in KB)

def clone_repo(repo_url: str, dest_path: str):
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, dest_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git clone failed: {e.stderr.decode().strip()}")

def read_files(base_path: str, max_files: int, max_file_size_kb: int):
    files_data = []
    count = 0
    for root, _, files in os.walk(base_path):
        for f in files:
            if count >= max_files:
                break
            full_path = os.path.join(root, f)
            try:
                size_kb = os.path.getsize(full_path) / 1024
                if size_kb > max_file_size_kb:
                    continue
                with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    files_data.append({
                        "filename": os.path.relpath(full_path, base_path),
                        "content": content
                    })
                    count += 1
            except Exception:
                # Skip unreadable files silently
                continue
        if count >= max_files:
            break
    return files_data

def build_prompt(files):
    file_list_str = "\n".join([f"- {file['filename']}" for file in files])
    file_contents_str = "\n\n".join([f"Filename: {file['filename']}\n```\n{file['content']}\n```" for file in files])

    prompt = f"""
You are an expert full-stack developer and software architect with decades of experience in analyzing, improving, and documenting codebases. You understand best practices, code readability, security, and performance.

Given the following codebase files and their content, do the following tasks:

1. Summarize the project in a few sentences:
   - Its purpose
   - Technologies used
   - Main components and their roles

2. Analyze the code quality and highlight potential improvements:
   - Code smells or anti-patterns
   - Opportunities for refactoring or modernization
   - Potential security vulnerabilities

3. Suggest a prioritized list of refactoring or upgrade tasks, each with:
   - A clear description
   - Expected benefits
   - Estimated complexity (low, medium, high)

4. Generate a README.md content draft:
   - Project overview
   - Setup and installation instructions
   - Usage examples
   - Contribution guidelines
   - License information (if provided)

---

Files:

{file_list_str}

Contents:

{file_contents_str}

---

Respond with a JSON object with the following keys:
{{
  "summary": "Project summary here",
  "analysis": "Detailed code quality analysis here",
  "refactor_plan": [
    {{
      "task": "Description",
      "benefit": "What it improves",
      "complexity": "low|medium|high"
    }}
  ],
  "readme": "Full README.md content as markdown text"
}}
"""
    return prompt

@app.post("/analyze-repo")
async def analyze_repo(request: RepoRequest):
    temp_dir = tempfile.mkdtemp()
    try:
        clone_repo(request.repo_url, temp_dir)
        files = read_files(temp_dir, request.max_files, request.max_file_size_kb)
        if not files:
            raise HTTPException(status_code=400, detail="No suitable files found in repo.")

        prompt = build_prompt(files)

        # Call OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        text_response = response.choices[0].message.content.strip()
        try:
            json_response = json.loads(text_response)
        except json.JSONDecodeError:
            json_response = {"raw_response": text_response}

        return {"result": json_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(temp_dir)
