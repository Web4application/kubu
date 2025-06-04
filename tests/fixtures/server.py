from fastapi import FastAPI, Request
import time, random

app = FastAPI()

@app.get("/h2test/echo")
async def echo(req: Request):
    return {"headers": dict(req.headers)}

@app.get("/h2test/delay")
async def delay(ms: int = 500):
    time.sleep(ms / 1000.0)
    return {"delayed": f"{ms}ms"}

@app.get("/h2test/error")
async def error(code: int = 500):
    return {"error": "simulated"}, code
