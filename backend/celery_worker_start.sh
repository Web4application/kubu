#!/bin/bash
celery -A app.worker.celery_app worker --loglevel=info
docker build -t kubu-hai-api .
docker run -p 8000:8000 -e OPENAI_API_KEY="AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10" kubu-hai-api
