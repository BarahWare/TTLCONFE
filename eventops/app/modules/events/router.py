from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.events.schemas import EventCreate, EventResponse, EventUpdate
from app.modules.events.service import EventService
from app.shared.exceptions import NotFound

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
async def list_events(org_id: int | None = None, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    if org_id:
        return await service.get_by_org(org_id)
    return []


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    return await service.create(body.model_dump())


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    try:
        return await service.get_by_id(event_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, body: EventUpdate, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    try:
        return await service.update(event_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
