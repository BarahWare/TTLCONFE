from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.tasks.schemas import (
    TaskAssignmentCreate,
    TaskAssignmentResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.modules.tasks.service import TaskService
from app.shared.exceptions import NotFound

router = APIRouter(tags=["tasks"])


@router.get("/api/v1/events/{event_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(event_id: int, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_by_event(event_id)


@router.post("/api/v1/events/{event_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    event_id: int,
    body: TaskCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    return await service.create(event_id, user.id, body.model_dump())


@router.patch("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, body: TaskUpdate, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    try:
        return await service.update(task_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("/api/v1/tasks/{task_id}/assignments", response_model=TaskAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def assign_task(task_id: int, body: TaskAssignmentCreate, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.assign(task_id, body.user_id)
