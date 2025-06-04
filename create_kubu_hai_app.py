import os
import argparse
from pathlib import Path
from datetime import datetime

def create_directories(project_name):
    os.makedirs(f"{project_name}/backend/app/api", exist_ok=True)
    os.makedirs(f"{project_name}/backend/app/models", exist_ok=True)
    os.makedirs(f"{project_name}/backend/app/db", exist_ok=True)
    os.makedirs(f"{project_name}/frontend", exist_ok=True)
    os.makedirs(f"{project_name}/nginx", exist_ok=True)
    os.makedirs(f"{project_name}/.github/workflows", exist_ok=True)

def write_backend_files(project_name):
    backend_root = f"{project_name}/backend"
    main_py = f"""\"
FastAPI main entry
\"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{project_name} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {{"status": "KubuHai backend ready"}}
"""
    with open(f"{backend_root}/app/main.py", "w") as f:
        f.write(main_py)

    with open(f"{backend_root}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn[standard]\npsycopg2-binary\nredis\nalembic\npython-dotenv\n")

    with open(f"{backend_root}/alembic.ini", "w") as f:
        f.write("# Alembic config placeholder")

def write_frontend_files(project_name, use_dart=False):
    frontend_root = f"{project_name}/frontend"
    if use_dart:
        Path(f"{frontend_root}/main.dart").write_text("// Dart frontend entry")
    else:
        Path(f"{frontend_root}/index.html").write_text("""
<!DOCTYPE html>
<html>
<head><title>KubuHai Frontend</title></head>
<body>
    <h1>Welcome to KubuHai</h1>
    <script>console.log("Frontend ready")</script>
</body>
</html>
""")

def write_nginx_config(project_name):
    config = f"""
server {{
    listen 80;
    server_name api.kubu-hai.com;

    location / {{
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
"""
    with open(f"{project_name}/nginx/default.conf", "w") as f:
        f.write(config)

def write_docker_compose(project_name):
    compose = f"""
version: "3.9"

services:
  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/code
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: kubuhai_db
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:alpine

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend

volumes:
  pgdata:
"""
    with open(f"{project_name}/docker-compose.yml", "w") as f:
        f.write(compose)

def write_env(project_name):
    env = """
DB_URL=postgresql://user:password@db:5432/kubuhai_db
REDIS_URL=redis://redis:6379
"""
    with open(f"{project_name}/.env", "w") as f:
        f.write(env)

def write_github_actions(project_name):
    ci_yaml = f"""
name: KubuHai CI

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: kubuhai_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Run Lint
      run: |
        cd backend
        python -m flake8 .
"""
    with open(f"{project_name}/.github/workflows/ci.yml", "w") as f:
        f.write(ci_yaml)

def write_readme(project_name):
    readme = f"""# {project_name}

Kubu-Hai production-ready scaffold.

## Stack

- FastAPI backend
- PostgreSQL + Redis
- Docker Compose
- Nginx reverse proxy
- Optional Dart or HTML frontend
- HTTPS-ready (Certbot hookable)
- CI/CD via GitHub Actions
- Alembic migrations
- .env support

## Setup

```bash
docker-compose up --build
