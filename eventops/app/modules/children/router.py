from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.children.schemas import (
    AttendanceRequest,
    AttendanceResponse,
    ChildRegister,
    ChildResponse,
    ClassroomCreate,
    ClassroomResponse,
    MaterialResponse,
)
from app.modules.children.service import ChildrenService
from app.shared.exceptions import NotFound

router = APIRouter(tags=["children"])


@router.get("/api/v1/events/{event_id}/children/classrooms", response_model=list[ClassroomResponse])
async def list_classrooms(event_id: int, db: AsyncSession = Depends(get_db)):
    service = ChildrenService(db)
    return await service.get_classrooms(event_id)


@router.post("/api/v1/events/{event_id}/children/classrooms", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
async def create_classroom(event_id: int, body: ClassroomCreate, db: AsyncSession = Depends(get_db)):
    service = ChildrenService(db)
    return await service.create_classroom(event_id, body.model_dump())


@router.get("/api/v1/children/classrooms/{classroom_id}/students", response_model=list[ChildResponse])
async def list_students(classroom_id: int, db: AsyncSession = Depends(get_db)):
    service = ChildrenService(db)
    return await service.get_students(classroom_id)


@router.post("/api/v1/events/{event_id}/children/classrooms/{classroom_id}/students", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def register_student(event_id: int, classroom_id: int, body: ChildRegister, db: AsyncSession = Depends(get_db)):
    service = ChildrenService(db)
    return await service.register_child(classroom_id, event_id, body.model_dump())


@router.post("/api/v1/children/students/{child_id}/attendance", response_model=AttendanceResponse)
async def record_attendance(
    child_id: int,
    body: AttendanceRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChildrenService(db)
    return await service.record_attendance(child_id, user.id, body)


@router.get("/api/v1/children/classrooms/{classroom_id}/materials", response_model=list[MaterialResponse])
async def list_materials(classroom_id: int, db: AsyncSession = Depends(get_db)):
    service = ChildrenService(db)
    return await service.get_materials(classroom_id)
