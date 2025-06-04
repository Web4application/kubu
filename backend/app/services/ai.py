import os
from pathlib import Path
import openai
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

async def analyze_project_code(project_path: Path) -> str:
    # Read some key files as context (e.g., README.md, main.py, setup.py)
    context = ""
    for filename in ["README.md", "main.py", "setup.py"]:
        file_path = project_path / filename
        if file_path.exists():
            context += f"\n\n# File: {filename}\n" + file_path.read_text()

    prompt = f"""
    You are a senior AI developer and code analyst. Here is the project context:
    {context}

    Summarize what this project does, its tech stack, and suggest improvements or refactors.
    Be concise but insightful.
    """

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

async def generate_readme_content(project_path: Path) -> str:
    prompt = f"""
    Write a professional, concise README.md for the following project:
    (Files in project: {', '.join(f.name for f in project_path.iterdir() if f.is_file())})
    """
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
