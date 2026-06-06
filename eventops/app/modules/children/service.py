from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.children.models import (
    ChildrenAttendance,
    ChildrenClassroom,
    ChildrenRegistry,
    ChildrenTeachingMaterial,
)
from app.shared.exceptions import NotFound


class ChildrenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_classroom(self, event_id: int, data: dict) -> ChildrenClassroom:
        room = ChildrenClassroom(event_id=event_id, **data)
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def get_classrooms(self, event_id: int) -> list[ChildrenClassroom]:
        result = await self.db.execute(
            select(ChildrenClassroom).where(ChildrenClassroom.event_id == event_id)
        )
        return list(result.scalars().all())

    async def register_child(self, classroom_id: int, event_id: int, data: dict) -> ChildrenRegistry:
        child = ChildrenRegistry(classroom_id=classroom_id, event_id=event_id, **data)
        self.db.add(child)
        await self.db.commit()
        await self.db.refresh(child)
        return child

    async def get_students(self, classroom_id: int) -> list[ChildrenRegistry]:
        result = await self.db.execute(
            select(ChildrenRegistry).where(ChildrenRegistry.classroom_id == classroom_id)
        )
        return list(result.scalars().all())

    async def record_attendance(self, child_id: int, user_id: int, body) -> ChildrenAttendance:
        result = await self.db.execute(
            select(ChildrenAttendance).where(
                ChildrenAttendance.child_id == child_id,
                ChildrenAttendance.event_date == body.event_date,
            )
        )
        record = result.scalar_one_or_none()
        if not record:
            record = ChildrenAttendance(
                child_id=child_id, event_date=body.event_date,
                checked_in_at=datetime.now(), checked_in_by=user_id,
            )
            self.db.add(record)
        elif body.action == "checkin" and not record.checked_in_at:
            record.checked_in_at = datetime.now()
            record.checked_in_by = user_id
        elif body.action == "checkout" and not record.checked_out_at:
            record.checked_out_at = datetime.now()
            record.checked_out_by = user_id
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_materials(self, classroom_id: int) -> list[ChildrenTeachingMaterial]:
        result = await self.db.execute(
            select(ChildrenTeachingMaterial).where(ChildrenTeachingMaterial.classroom_id == classroom_id)
        )
        return list(result.scalars().all())
