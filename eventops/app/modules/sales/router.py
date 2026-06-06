from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.sales.schemas import (
    ProductCreate,
    ProductResponse,
    ReconcileRequest,
    ReconciliationResponse,
    StandCreate,
    StandResponse,
    TransactionCreate,
    TransactionResponse,
)
from app.modules.sales.service import SalesService

router = APIRouter(tags=["sales"])


@router.get("/api/v1/events/{event_id}/sales/stands", response_model=list[StandResponse])
async def list_stands(event_id: int, db: AsyncSession = Depends(get_db)):
    service = SalesService(db)
    return await service.get_stands(event_id)


@router.post("/api/v1/events/{event_id}/sales/stands", response_model=StandResponse, status_code=status.HTTP_201_CREATED)
async def create_stand(event_id: int, body: StandCreate, db: AsyncSession = Depends(get_db)):
    service = SalesService(db)
    return await service.create_stand(event_id, body.model_dump())


@router.get("/api/v1/sales/stands/{stand_id}/products", response_model=list[ProductResponse])
async def list_products(stand_id: int, db: AsyncSession = Depends(get_db)):
    service = SalesService(db)
    return await service.get_products(stand_id)


@router.post("/api/v1/sales/stands/{stand_id}/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(stand_id: int, body: ProductCreate, db: AsyncSession = Depends(get_db)):
    service = SalesService(db)
    return await service.create_product(stand_id, body.model_dump())


@router.get("/api/v1/sales/stands/{stand_id}/transactions", response_model=list[TransactionResponse])
async def list_transactions(stand_id: int, db: AsyncSession = Depends(get_db)):
    service = SalesService(db)
    return await service.get_transactions(stand_id)


@router.post("/api/v1/sales/stands/{stand_id}/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def record_transaction(
    stand_id: int, body: TransactionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SalesService(db)
    return await service.record_transaction(stand_id, user.id, body.model_dump())


@router.post("/api/v1/sales/stands/{stand_id}/reconcile", response_model=ReconciliationResponse)
async def reconcile_stand(
    stand_id: int, body: ReconcileRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SalesService(db)
    return await service.reconcile(stand_id, user.id, body.model_dump())
