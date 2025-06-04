import os
from app.services.llm import ask_llm
from app.utils.file_handler import write_file

def generate_readme(summary: str, repo_path: str):
    prompt = f"Generate a detailed, clean README.md based on the following project summary:\n{summary}"
    readme = ask_llm(prompt)
    write_file(os.path.join(repo_path, "README.md"), readme)

def generate_requirements(code_text: str, repo_path: str):
    prompt = f"Extract and list all Python package dependencies from this codebase:\n{code_text}"
    deps = ask_llm(prompt)
    write_file(os.path.join(repo_path, "requirements.txt"), deps)
