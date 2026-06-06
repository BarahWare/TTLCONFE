from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.kitchen.schemas import (
    IngredientCreate,
    IngredientResponse,
    KitchenTaskCreate,
    KitchenTaskResponse,
    MenuCreate,
    MenuResponse,
    PurchaseOrderCreate,
    PurchaseOrderResponse,
)
from app.modules.kitchen.service import KitchenService

router = APIRouter(tags=["kitchen"])


@router.get("/api/v1/events/{event_id}/kitchen/menus", response_model=list[MenuResponse])
async def list_menus(event_id: int, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.get_menus(event_id)


@router.post("/api/v1/events/{event_id}/kitchen/menus", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(event_id: int, body: MenuCreate, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.create_menu(event_id, body.model_dump())


@router.get("/api/v1/events/{event_id}/kitchen/ingredients", response_model=list[IngredientResponse])
async def list_ingredients(event_id: int, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.get_ingredients(event_id)


@router.post("/api/v1/events/{event_id}/kitchen/ingredients", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
async def create_ingredient(event_id: int, body: IngredientCreate, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.create_ingredient(event_id, body.model_dump())


@router.get("/api/v1/events/{event_id}/kitchen/purchase-orders", response_model=list[PurchaseOrderResponse])
async def list_purchase_orders(event_id: int, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.get_purchase_orders(event_id)


@router.post("/api/v1/events/{event_id}/kitchen/purchase-orders", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    event_id: int,
    body: PurchaseOrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = KitchenService(db)
    return await service.create_purchase_order(event_id, user.id, body.model_dump())


@router.get("/api/v1/events/{event_id}/kitchen/tasks", response_model=list[KitchenTaskResponse])
async def list_kitchen_tasks(event_id: int, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.get_tasks(event_id)


@router.post("/api/v1/events/{event_id}/kitchen/tasks", response_model=KitchenTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_kitchen_task(event_id: int, body: KitchenTaskCreate, db: AsyncSession = Depends(get_db)):
    service = KitchenService(db)
    return await service.create_task(event_id, body.model_dump())
