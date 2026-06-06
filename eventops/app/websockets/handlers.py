from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.websockets.manager import manager

router = APIRouter()


@router.websocket("/ws/chat/{channel_id}")
async def chat_websocket(websocket: WebSocket, channel_id: int, user: User = Depends(get_current_user)):
    channel = f"chat_{channel_id}"
    await manager.connect(websocket, channel, user.id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast_to_channel(channel, {
                "type": "chat.message",
                "channel_id": channel_id,
                "user_id": user.id,
                "payload": data,
            })
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, user.id)


@router.websocket("/ws/user/{user_id}")
async def user_websocket(websocket: WebSocket, user_id: int, user: User = Depends(get_current_user)):
    channel = f"user_{user_id}"
    await manager.connect(websocket, channel, user.id)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, user.id)


@router.websocket("/ws/event/{event_id}")
async def event_websocket(websocket: WebSocket, event_id: int, user: User = Depends(get_current_user)):
    channel = f"event_{event_id}"
    await manager.connect(websocket, channel, user.id)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, user.id)
