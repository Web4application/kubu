# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import databases
import sqlalchemy

DATABASE_URL = "postgresql://user:password@db:5432/kubu_hai_db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app = FastAPI(title="Kubu-hai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/ping")
async def ping():
    return {"message": "kubu-hai backend is alive and kicking"}
