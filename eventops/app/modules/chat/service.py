from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.models import ChatChannel, ChatMessage, DirectMessage
from app.shared.exceptions import NotFound


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_channel(self, event_id: int, data: dict) -> ChatChannel:
        channel = ChatChannel(event_id=event_id, **data)
        self.db.add(channel)
        await self.db.commit()
        await self.db.refresh(channel)
        return channel

    async def get_channels(self, event_id: int) -> list[ChatChannel]:
        result = await self.db.execute(
            select(ChatChannel).where(ChatChannel.event_id == event_id).order_by(ChatChannel.name)
        )
        return list(result.scalars().all())

    async def send_message(self, channel_id: int, sender_id: int, data: dict) -> ChatMessage:
        msg = ChatMessage(channel_id=channel_id, sender_id=sender_id, **data)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_messages(self, channel_id: int, limit: int = 100) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.channel_id == channel_id)
            .order_by(ChatMessage.sent_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))

    async def send_direct(self, sender_id: int, receiver_id: int, data: dict) -> DirectMessage:
        msg = DirectMessage(sender_id=sender_id, receiver_id=receiver_id, **data)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_direct_messages(self, user_id: int, other_id: int, limit: int = 100) -> list[DirectMessage]:
        result = await self.db.execute(
            select(DirectMessage)
            .where(
                or_(
                    (DirectMessage.sender_id == user_id) & (DirectMessage.receiver_id == other_id),
                    (DirectMessage.sender_id == other_id) & (DirectMessage.receiver_id == user_id),
                )
            )
            .order_by(DirectMessage.sent_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))
