python -m http.server 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pip install -r requirements.txt
cd kubu/backend
pip install -r requirements.txt
uvicorn main:app --reload
