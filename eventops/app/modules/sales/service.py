from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.sales.models import (
    SalesProduct,
    SalesReconciliation,
    SalesStand,
    SalesTransaction,
)


class SalesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stand(self, event_id: int, data: dict) -> SalesStand:
        stand = SalesStand(event_id=event_id, **data)
        self.db.add(stand)
        await self.db.commit()
        await self.db.refresh(stand)
        return stand

    async def get_stands(self, event_id: int) -> list[SalesStand]:
        result = await self.db.execute(
            select(SalesStand).where(SalesStand.event_id == event_id)
        )
        return list(result.scalars().all())

    async def create_product(self, stand_id: int, data: dict) -> SalesProduct:
        product = SalesProduct(stand_id=stand_id, **data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_products(self, stand_id: int) -> list[SalesProduct]:
        result = await self.db.execute(
            select(SalesProduct).where(SalesProduct.stand_id == stand_id)
        )
        return list(result.scalars().all())

    async def record_transaction(self, stand_id: int, user_id: int, data: dict) -> SalesTransaction:
        txn = SalesTransaction(stand_id=stand_id, registered_by=user_id, **data)
        self.db.add(txn)
        await self.db.commit()
        await self.db.refresh(txn)
        return txn

    async def get_transactions(self, stand_id: int) -> list[SalesTransaction]:
        result = await self.db.execute(
            select(SalesTransaction).where(SalesTransaction.stand_id == stand_id)
        )
        return list(result.scalars().all())

    async def reconcile(self, stand_id: int, user_id: int, data: dict) -> SalesReconciliation:
        expected = await self.db.execute(
            select(func.coalesce(func.sum(SalesTransaction.amount), 0)).where(
                SalesTransaction.stand_id == stand_id
            )
        )
        expected_total = float(expected.scalar())
        rec = SalesReconciliation(
            stand_id=stand_id, reconciled_by=user_id,
            expected_total=expected_total, **data,
        )
        rec.difference = rec.expected_total - rec.actual_total
        self.db.add(rec)
        await self.db.commit()
        await self.db.refresh(rec)
        return rec

    async def get_reconciliations(self, stand_id: int) -> list[SalesReconciliation]:
        result = await self.db.execute(
            select(SalesReconciliation).where(SalesReconciliation.stand_id == stand_id)
        )
        return list(result.scalars().all())
