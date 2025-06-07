import asyncio
from fastapi import WebSocket
from typing import List

class ChatManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def handle_message(self, websocket: WebSocket, message: str):
        # Here: integrate your LLM or chatbot logic
        # For now, just echo
        response = f"Echo: {message}"
        await websocket.send_text(response)

chat_manager = ChatManager()

async def chat_endpoint(websocket: WebSocket):
    await chat_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.handle_message(websocket, data)
    except Exception:
        chat_manager.disconnect(websocket)
