from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.chat.schemas import (
    ChannelCreate,
    ChannelResponse,
    DirectMessageResponse,
    DirectMessageSend,
    MessageResponse,
    MessageSend,
)
from app.modules.chat.service import ChatService

router = APIRouter(tags=["chat"])


@router.get("/api/v1/events/{event_id}/channels", response_model=list[ChannelResponse])
async def list_channels(event_id: int, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    return await service.get_channels(event_id)


@router.post("/api/v1/events/{event_id}/channels", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(event_id: int, body: ChannelCreate, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    return await service.create_channel(event_id, body.model_dump())


@router.get("/api/v1/channels/{channel_id}/messages", response_model=list[MessageResponse])
async def get_channel_messages(channel_id: int, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    return await service.get_messages(channel_id)


@router.post("/api/v1/channels/{channel_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_channel_message(
    channel_id: int,
    body: MessageSend,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.send_message(channel_id, user.id, body.model_dump())


@router.get("/api/v1/direct-messages/{user_id}", response_model=list[DirectMessageResponse])
async def get_direct_messages(
    user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.get_direct_messages(user.id, user_id)


@router.post("/api/v1/direct-messages/{user_id}", response_model=DirectMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_direct_message(
    user_id: int,
    body: DirectMessageSend,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.send_direct(user.id, user_id, body.model_dump())
