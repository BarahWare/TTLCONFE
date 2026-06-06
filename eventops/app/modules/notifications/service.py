from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notifications.models import Notification, PushToken


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_token(self, user_id: int, token: str, platform: str) -> PushToken:
        result = await self.db.execute(
            select(PushToken).where(PushToken.user_id == user_id, PushToken.token == token)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing
        pt = PushToken(user_id=user_id, token=token, platform=platform)
        self.db.add(pt)
        await self.db.commit()
        await self.db.refresh(pt)
        return pt

    async def get_notifications(self, user_id: int) -> list[Notification]:
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(50)
        )
        return list(result.scalars().all())

    async def mark_read(self, notification_id: int, user_id: int) -> Notification | None:
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        )
        n = result.scalar_one_or_none()
        if n:
            n.is_read = True
            await self.db.commit()
            await self.db.refresh(n)
        return n

    async def create_notification(
        self, user_id: int, event_id: int, title: str, body: str, ntype: str,
        related_entity_type: str | None = None, related_entity_id: int | None = None,
    ) -> Notification:
        n = Notification(
            user_id=user_id, event_id=event_id, title=title, body=body,
            notification_type=ntype, related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
        )
        self.db.add(n)
        await self.db.commit()
        await self.db.refresh(n)
        return n
