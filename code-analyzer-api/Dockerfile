FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV OPENAI_API_KEY="AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
