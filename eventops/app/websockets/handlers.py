from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from jose import JWTError, jwt

from app.config import settings
from app.websockets.manager import manager

router = APIRouter()


async def _get_user_id_from_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None


@router.websocket("/ws/chat/{channel_id}")
async def chat_websocket(websocket: WebSocket, channel_id: int, token: str = Query(...)):
    user_id = await _get_user_id_from_token(token)
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    channel = f"chat_{channel_id}"
    await manager.connect(websocket, channel, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast_to_channel(channel, {
                "type": "chat.message",
                "channel_id": channel_id,
                "user_id": user_id,
                "payload": data,
            })
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, user_id)


@router.websocket("/ws/user/{user_id}")
async def user_websocket(websocket: WebSocket, user_id: int, token: str = Query(...)):
    uid = await _get_user_id_from_token(token)
    if uid is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    channel = f"user_{user_id}"
    await manager.connect(websocket, channel, uid)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, uid)


@router.websocket("/ws/event/{event_id}")
async def event_websocket(websocket: WebSocket, event_id: int, token: str = Query(...)):
    uid = await _get_user_id_from_token(token)
    if uid is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    channel = f"event_{event_id}"
    await manager.connect(websocket, channel, uid)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel, uid)
