from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.kitchen.models import (
    KitchenIngredient,
    KitchenMenu,
    KitchenPurchaseOrder,
    KitchenTask,
)


class KitchenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_menu(self, event_id: int, data: dict) -> KitchenMenu:
        menu = KitchenMenu(event_id=event_id, **data)
        self.db.add(menu)
        await self.db.commit()
        await self.db.refresh(menu)
        return menu

    async def get_menus(self, event_id: int) -> list[KitchenMenu]:
        result = await self.db.execute(
            select(KitchenMenu).where(KitchenMenu.event_id == event_id).order_by(KitchenMenu.menu_date)
        )
        return list(result.scalars().all())

    async def create_ingredient(self, event_id: int, data: dict) -> KitchenIngredient:
        ing = KitchenIngredient(event_id=event_id, **data)
        self.db.add(ing)
        await self.db.commit()
        await self.db.refresh(ing)
        return ing

    async def get_ingredients(self, event_id: int) -> list[KitchenIngredient]:
        result = await self.db.execute(
            select(KitchenIngredient).where(KitchenIngredient.event_id == event_id)
        )
        return list(result.scalars().all())

    async def create_purchase_order(self, event_id: int, user_id: int, data: dict) -> KitchenPurchaseOrder:
        po = KitchenPurchaseOrder(event_id=event_id, created_by=user_id, **data)
        self.db.add(po)
        await self.db.commit()
        await self.db.refresh(po)
        return po

    async def get_purchase_orders(self, event_id: int) -> list[KitchenPurchaseOrder]:
        result = await self.db.execute(
            select(KitchenPurchaseOrder).where(KitchenPurchaseOrder.event_id == event_id)
        )
        return list(result.scalars().all())

    async def create_task(self, event_id: int, data: dict) -> KitchenTask:
        task = KitchenTask(event_id=event_id, **data)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_tasks(self, event_id: int) -> list[KitchenTask]:
        result = await self.db.execute(
            select(KitchenTask).where(KitchenTask.event_id == event_id)
        )
        return list(result.scalars().all())
