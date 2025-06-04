import os
from app.services.llm import ask_llm
from app.utils.file_handler import walk_codebase, write_file

def upgrade_codebase(repo_path: str):
    updates = []
    for filepath, content in walk_codebase(repo_path):
        prompt = (
            f"You're a world-class AI engineer. Refactor and optimize the following Python code. "
            f"Add typing, better structure, and inline comments:\n\n{content}"
        )
        improved = ask_llm(prompt)
        write_file(filepath, improved)
        updates.append(filepath)
    return updates
