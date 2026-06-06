from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.events.models import Event
from app.shared.exceptions import NotFound


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Event:
        event = Event(**data)
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_by_org(self, org_id: int) -> list[Event]:
        result = await self.db.execute(
            select(Event).where(Event.org_id == org_id).order_by(Event.start_date)
        )
        return list(result.scalars().all())

    async def get_by_id(self, event_id: int) -> Event:
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if not event:
            raise NotFound("Event not found")
        return event

    async def update(self, event_id: int, data: dict) -> Event:
        event = await self.get_by_id(event_id)
        for key, value in data.items():
            if value is not None:
                setattr(event, key, value)
        await self.db.commit()
        await self.db.refresh(event)
        return event
