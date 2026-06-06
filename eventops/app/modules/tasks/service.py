from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.tasks.models import Task, TaskAssignment
from app.shared.exceptions import NotFound


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_id: int, user_id: int, data: dict) -> Task:
        task = Task(event_id=event_id, created_by=user_id, **data)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_event(self, event_id: int) -> list[Task]:
        result = await self.db.execute(
            select(Task).where(Task.event_id == event_id).order_by(Task.created_at)
        )
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Task:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFound("Task not found")
        return task

    async def update(self, task_id: int, data: dict) -> Task:
        task = await self.get_by_id(task_id)
        for key, value in data.items():
            if value is not None:
                setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def assign(self, task_id: int, user_id: int) -> TaskAssignment:
        assignment = TaskAssignment(task_id=task_id, user_id=user_id)
        self.db.add(assignment)
        await self.db.commit()
        await self.db.refresh(assignment)
        return assignment

    async def get_assignments(self, task_id: int) -> list[TaskAssignment]:
        result = await self.db.execute(
            select(TaskAssignment).where(TaskAssignment.task_id == task_id)
        )
        return list(result.scalars().all())
