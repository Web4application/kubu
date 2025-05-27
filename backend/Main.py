from fastapi import FastAPI, WebSocket
import psutil
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from collections import deque
import statistics

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
