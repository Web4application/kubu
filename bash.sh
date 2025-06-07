python main.py --repo ../kubu-hai
pip install -r requirements.txt
python -m http.server 8000
cd kubu/backend
pip install -r requirements.txt
uvicorn main:app --reload
cd kubu
git add .
git commit -m "Add audit script, CI/CD workflow, and FastAPI backend scaffold"
git push origin main
cd kubu/scripts
python3 audit_repo.py

docker pull ghcr.io/web4application/kubu:main
docker pull ghcr.io/web4application/kubu@sha256:<digest>
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
