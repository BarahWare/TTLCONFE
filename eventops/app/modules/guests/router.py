from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.guests.schemas import (
    CategoryCreate,
    CategoryResponse,
    GuestCreate,
    GuestResponse,
)
from app.modules.guests.service import GuestsService

router = APIRouter(tags=["guests"])


@router.get("/api/v1/events/{event_id}/guests/categories", response_model=list[CategoryResponse])
async def list_categories(event_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.get_categories(event_id)


@router.post("/api/v1/events/{event_id}/guests/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(event_id: int, body: CategoryCreate, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.create_category(event_id, body.model_dump())


@router.get("/api/v1/events/{event_id}/guests", response_model=list[GuestResponse])
async def list_guests(event_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.get_guests(event_id)


@router.post("/api/v1/events/{event_id}/guests", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
async def create_guest(
    event_id: int, body: GuestCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GuestsService(db)
    return await service.create_guest(event_id, user.id, body.model_dump())


@router.get("/api/v1/guests/{guest_id}", response_model=GuestResponse)
async def get_guest(guest_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.get_guest(guest_id)


@router.post("/api/v1/guests/{guest_id}/check-in", response_model=GuestResponse)
async def check_in_guest(guest_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.check_in(guest_id)


@router.post("/api/v1/guests/{guest_id}/confirm", response_model=GuestResponse)
async def confirm_guest(guest_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.confirm(guest_id)


@router.get("/api/v1/events/{event_id}/guests/vip", response_model=list[GuestResponse])
async def list_vip(event_id: int, db: AsyncSession = Depends(get_db)):
    service = GuestsService(db)
    return await service.get_vip_guests(event_id)
