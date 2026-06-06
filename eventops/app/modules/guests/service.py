from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.guests.models import Guest, GuestCategory
from app.shared.exceptions import NotFound


class GuestsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, event_id: int, data: dict) -> GuestCategory:
        cat = GuestCategory(event_id=event_id, **data)
        self.db.add(cat)
        await self.db.commit()
        await self.db.refresh(cat)
        return cat

    async def get_categories(self, event_id: int) -> list[GuestCategory]:
        result = await self.db.execute(
            select(GuestCategory).where(GuestCategory.event_id == event_id).order_by(GuestCategory.priority)
        )
        return list(result.scalars().all())

    async def create_guest(self, event_id: int, user_id: int, data: dict) -> Guest:
        guest = Guest(event_id=event_id, created_by=user_id, **data)
        self.db.add(guest)
        await self.db.commit()
        await self.db.refresh(guest)
        return guest

    async def get_guests(self, event_id: int) -> list[Guest]:
        result = await self.db.execute(
            select(Guest).where(Guest.event_id == event_id).order_by(Guest.is_vip.desc(), Guest.full_name)
        )
        return list(result.scalars().all())

    async def get_guest(self, guest_id: int) -> Guest:
        result = await self.db.execute(select(Guest).where(Guest.id == guest_id))
        guest = result.scalar_one_or_none()
        if not guest:
            raise NotFound("Guest not found")
        return guest

    async def check_in(self, guest_id: int) -> Guest:
        guest = await self.get_guest(guest_id)
        guest.checked_in = True
        guest.checked_in_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(guest)
        return guest

    async def confirm(self, guest_id: int) -> Guest:
        guest = await self.get_guest(guest_id)
        guest.confirmed = True
        guest.confirmed_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(guest)
        return guest

    async def get_vip_guests(self, event_id: int) -> list[Guest]:
        result = await self.db.execute(
            select(Guest).where(Guest.event_id == event_id, Guest.is_vip == True)
        )
        return list(result.scalars().all())
