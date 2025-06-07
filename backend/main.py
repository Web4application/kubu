from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analyze, chat

app = FastAPI(title="Kubu-Hai AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Kubu-Hai Backend is running"}
