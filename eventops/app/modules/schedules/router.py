from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.schedules.schemas import (
    ConflictResponse,
    ScheduleAssignmentCreate,
    ScheduleAssignmentResponse,
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)
from app.modules.schedules.service import ScheduleService
from app.shared.exceptions import NotFound

router = APIRouter(tags=["schedules"])


@router.get("/api/v1/users/me/schedule", response_model=list[ScheduleResponse])
async def my_schedule(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    return await service.get_user_schedule(user.id)


@router.get("/api/v1/events/{event_id}/schedules", response_model=list[ScheduleResponse])
async def list_schedules(event_id: int, db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    return await service.get_by_event(event_id)


@router.post("/api/v1/events/{event_id}/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    event_id: int,
    body: ScheduleCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ScheduleService(db)
    return await service.create(event_id, user.id, body.model_dump())


@router.patch("/api/v1/schedules/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: int, body: ScheduleUpdate, db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    try:
        return await service.update(schedule_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/api/v1/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    try:
        await service.delete(schedule_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("/api/v1/schedules/{schedule_id}/assignments", response_model=ScheduleAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def assign_schedule(schedule_id: int, body: ScheduleAssignmentCreate, db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    assignment = await service.assign(schedule_id, body.user_id)
    return assignment


@router.get("/api/v1/events/{event_id}/schedule-conflicts", response_model=list[ConflictResponse])
async def get_schedule_conflicts(event_id: int, db: AsyncSession = Depends(get_db)):
    service = ScheduleService(db)
    return await service.detect_conflicts(event_id)
