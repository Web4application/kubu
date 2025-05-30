import os
from app.services.llm import ask_llm
from app.utils.file_handler import walk_codebase

def summarize_repo(repo_path: str) -> str:
    all_content = ""
    for filepath, content in walk_codebase(repo_path):
        all_content += f"\n\n--- {filepath} ---\n{content[:1500]}"  # Limit size

    prompt = (
        "You are a senior developer. Summarize the purpose, structure, and key functionality "
        "of this project based on the following source code:"
        f"\n{all_content}"
    )
    return ask_llm(prompt)
