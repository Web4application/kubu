python -m http.server 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pip install -r requirements.txt
cd kubu/backend
pip install -r requirements.txt
uvicorn main:app --reload
docker pull ghcr.io/web4application/kubu:sha256-65a937d797bd4a24738624dc6d2e0f7a7e52ee300c0ed459c653674c212fe2d8.sig
brew install ngrok
ngrok config add-authtoken 2y96VwzmhS1YV6vgll2Ua411oGc_755Qcpps22pznftiuGZWr
ngrok http http://localhost:8080
ngrok http --url=above-feasible-lobster.ngrok-free.app 80
