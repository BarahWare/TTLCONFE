from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.schedules.models import Schedule, ScheduleAssignment
from app.shared.exceptions import NotFound


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_id: int, user_id: int, data: dict) -> Schedule:
        schedule = Schedule(event_id=event_id, created_by=user_id, **data)
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def get_by_event(self, event_id: int) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule).where(Schedule.event_id == event_id).order_by(Schedule.start_datetime)
        )
        return list(result.scalars().all())

    async def get_by_id(self, schedule_id: int) -> Schedule:
        result = await self.db.execute(select(Schedule).where(Schedule.id == schedule_id))
        schedule = result.scalar_one_or_none()
        if not schedule:
            raise NotFound("Schedule not found")
        return schedule

    async def update(self, schedule_id: int, data: dict) -> Schedule:
        schedule = await self.get_by_id(schedule_id)
        for key, value in data.items():
            if value is not None:
                setattr(schedule, key, value)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def delete(self, schedule_id: int):
        schedule = await self.get_by_id(schedule_id)
        await self.db.delete(schedule)
        await self.db.commit()

    async def assign(self, schedule_id: int, user_id: int) -> ScheduleAssignment:
        assignment = ScheduleAssignment(schedule_id=schedule_id, user_id=user_id)
        self.db.add(assignment)
        await self.db.commit()
        await self.db.refresh(assignment)
        return assignment

    async def get_user_schedule(self, user_id: int) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule).join(ScheduleAssignment).where(
                ScheduleAssignment.user_id == user_id
            ).order_by(Schedule.start_datetime)
        )
        return list(result.scalars().all())

    async def detect_conflicts(self, event_id: int) -> list[dict]:
        subq = (
            select(
                ScheduleAssignment.user_id,
                ScheduleAssignment.schedule_id,
                Schedule.start_datetime,
                Schedule.end_datetime,
                Schedule.title,
            )
            .join(Schedule, ScheduleAssignment.schedule_id == Schedule.id)
            .where(Schedule.event_id == event_id)
            .subquery()
        )

        result = await self.db.execute(
            select(subq.c.user_id, subq.c.schedule_id, subq.c.title, subq.c.start_datetime, subq.c.end_datetime)
            .select_from(subq)
            .join(
                subq,
                and_(
                    subq.c.user_id == subq.c.user_id,
                    subq.c.schedule_id != subq.c.schedule_id,
                    subq.c.start_datetime < subq.c.end_datetime,
                    subq.c.end_datetime > subq.c.start_datetime,
                ),
            )
            .distinct()
        )
        conflicts = []
        for row in result.all():
            conflicts.append({
                "user_id": row.user_id,
                "schedule_id": row.schedule_id,
                "title": row.title,
                "start_datetime": row.start_datetime.isoformat(),
                "end_datetime": row.end_datetime.isoformat(),
            })
        return conflicts
