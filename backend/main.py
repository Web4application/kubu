from fastapi import FastAPI, WebSocket
import psutil
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from collections import deque
import statistics
from fastapi import Depends
from auth import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "roles": user["roles"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.websocket("/ws/metrics")
async def metrics_ws(websocket: WebSocket, current_user=Depends(get_current_user)):
    await websocket.accept()
    # rest of your ws code here

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_HISTORY = 50  # number of points to keep for stats

cpu_history = deque(maxlen=MAX_HISTORY)
mem_history = deque(maxlen=MAX_HISTORY)

def is_anomaly(value, history, threshold=2.5):
    if len(history) < 10:
        return False  # Not enough data to judge
    mean = statistics.mean(history)
    stdev = statistics.stdev(history)
    if stdev == 0:
        return False
    z_score = abs((value - mean) / stdev)
    return z_score > threshold

@app.websocket("/ws/metrics")
async def metrics_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent

            # Append current readings
            cpu_history.append(cpu)
            mem_history.append(mem)

            cpu_anomaly = is_anomaly(cpu, list(cpu_history))
            mem_anomaly = is_anomaly(mem, list(mem_history))

            payload = {
                "cpu": cpu,
                "memory": mem,
                "cpu_anomaly": cpu_anomaly,
                "mem_anomaly": mem_anomaly,
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1)
    except Exception:
        await websocket.close()
