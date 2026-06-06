from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.user_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, channel: str, user_id: int):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)
        self.user_connections[user_id] = websocket

    async def disconnect(self, websocket: WebSocket, channel: str, user_id: int):
        if channel in self.active_connections:
            self.active_connections[channel].remove(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]
        self.user_connections.pop(user_id, None)

    async def broadcast_to_channel(self, channel: str, message: dict):
        if channel not in self.active_connections:
            return
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception:
                pass

    async def send_to_user(self, user_id: int, message: dict):
        connection = self.user_connections.get(user_id)
        if connection:
            try:
                await connection.send_json(message)
            except Exception:
                pass

    async def broadcast_event(self, event_id: int, message: dict):
        channel = f"event_{event_id}"
        await self.broadcast_to_channel(channel, message)


manager = ConnectionManager()
