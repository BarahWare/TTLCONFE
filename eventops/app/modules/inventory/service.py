from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryItem, InventoryMovement
from app.modules.inventory.schemas import InventorySummary
from app.shared.exceptions import NotFound


class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, team_id: int, event_id: int, data: dict) -> InventoryItem:
        item = InventoryItem(event_id=event_id, team_id=team_id, quantity_available=data.get("quantity", 0), **data)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def get_by_team(self, team_id: int) -> list[InventoryItem]:
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.team_id == team_id).order_by(InventoryItem.name)
        )
        return list(result.scalars().all())

    async def get_by_id(self, item_id: int) -> InventoryItem:
        result = await self.db.execute(select(InventoryItem).where(InventoryItem.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise NotFound("Inventory item not found")
        return item

    async def update(self, item_id: int, data: dict) -> InventoryItem:
        item = await self.get_by_id(item_id)
        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)
        if "quantity" in data and data["quantity"] is not None:
            item.quantity_available = data["quantity"]
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def add_movement(self, item_id: int, user_id: int, data: dict) -> InventoryMovement:
        item = await self.get_by_id(item_id)
        if data["movement_type"] in ("checkout",):
            item.quantity_available -= data["quantity"]
        elif data["movement_type"] in ("checkin",):
            item.quantity_available += data["quantity"]
        movement = InventoryMovement(item_id=item_id, performed_by=user_id, **data)
        self.db.add(movement)
        await self.db.commit()
        await self.db.refresh(movement)
        return movement

    async def get_movements(self, item_id: int) -> list[InventoryMovement]:
        result = await self.db.execute(
            select(InventoryMovement).where(InventoryMovement.item_id == item_id).order_by(InventoryMovement.moved_at.desc())
        )
        return list(result.scalars().all())

    async def get_summary(self, event_id: int) -> InventorySummary:
        items = await self.get_by_event(event_id)
        total = len(items)
        available = sum(1 for i in items if i.status == "available")
        in_use = sum(1 for i in items if i.status == "in_use")
        maintenance = sum(1 for i in items if i.status == "maintenance")
        rented = sum(1 for i in items if i.is_rented)
        low_stock = [i for i in items if i.quantity > 0 and i.quantity_available <= 0]
        return InventorySummary(
            total_items=total, available=available, in_use=in_use,
            under_maintenance=maintenance, rented=rented,
            low_stock_items=low_stock,
        )

    async def get_by_event(self, event_id: int) -> list[InventoryItem]:
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.event_id == event_id).order_by(InventoryItem.name)
        )
        return list(result.scalars().all())
