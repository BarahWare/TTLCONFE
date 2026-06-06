from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.inventory.schemas import (
    InventoryItemCreate,
    InventoryItemResponse,
    InventoryItemUpdate,
    InventorySummary,
    MovementCreate,
    MovementResponse,
)
from app.modules.inventory.service import InventoryService
from app.shared.exceptions import NotFound

router = APIRouter(tags=["inventory"])


@router.get("/api/v1/teams/{team_id}/inventory", response_model=list[InventoryItemResponse])
async def list_inventory(team_id: int, db: AsyncSession = Depends(get_db)):
    service = InventoryService(db)
    return await service.get_by_team(team_id)


@router.post("/api/v1/teams/{team_id}/inventory", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    team_id: int,
    body: InventoryItemCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)
    return await service.create(team_id, user.id, body.model_dump())


@router.patch("/api/v1/inventory/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(item_id: int, body: InventoryItemUpdate, db: AsyncSession = Depends(get_db)):
    service = InventoryService(db)
    try:
        return await service.update(item_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("/api/v1/inventory/{item_id}/movements", response_model=MovementResponse, status_code=status.HTTP_201_CREATED)
async def add_movement(
    item_id: int,
    body: MovementCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)
    try:
        return await service.add_movement(item_id, user.id, body.model_dump())
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.get("/api/v1/inventory/{item_id}/history", response_model=list[MovementResponse])
async def get_movement_history(item_id: int, db: AsyncSession = Depends(get_db)):
    service = InventoryService(db)
    return await service.get_movements(item_id)


@router.get("/api/v1/events/{event_id}/inventory/summary", response_model=InventorySummary)
async def get_inventory_summary(event_id: int, db: AsyncSession = Depends(get_db)):
    service = InventoryService(db)
    return await service.get_summary(event_id)
