python main.py --repo ../kubuverse
pip install -r requirements.txt
python -m http.server 8000

cd kubuverse/backend
pip install -r requirements.txt
uvicorn main:app --reload

cd kubuverse/scripts
python3 audit_repo.p

docker pull ghcr.io/web4application/kubu:main
docker pull ghcr.io/web4application/kubu@sha256:<digest>
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
docker build -t ghcr.io/web4application/kubuverse:main .
# Generate key (only once)
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key ghcr.io/web4application/kubu:main
cosign verify --key cosign.pub ghcr.io/web4application/kubu:main

pip install fastapi uvicorn sqlalchemy psycopg2-binary
