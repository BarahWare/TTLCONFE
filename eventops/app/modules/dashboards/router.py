from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.children.models import ChildrenClassroom, ChildrenRegistry
from app.modules.events.service import EventService
from app.modules.guests.models import Guest
from app.modules.inventory.service import InventoryService
from app.modules.kitchen.models import KitchenTask
from app.modules.sales.models import SalesStand, SalesTransaction
from app.modules.schedules.service import ScheduleService
from app.modules.tasks.service import TaskService

router = APIRouter(tags=["dashboards"])


@router.get("/api/v1/events/{event_id}/dashboard")
async def event_dashboard(event_id: int, db: AsyncSession = Depends(get_db)):
    schedule_service = ScheduleService(db)
    task_service = TaskService(db)
    inventory_service = InventoryService(db)
    event_service = EventService(db)

    event = await event_service.get_by_id(event_id)
    schedules = await schedule_service.get_by_event(event_id)
    tasks = await task_service.get_by_event(event_id)
    conflicts = await schedule_service.detect_conflicts(event_id)

    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t.status == "completed")
    pending = sum(1 for t in tasks if t.status == "pending")

    classrooms = await db.execute(
        select(func.count(ChildrenClassroom.id)).where(ChildrenClassroom.event_id == event_id)
    )
    total_children = await db.execute(
        select(func.count(ChildrenRegistry.id)).where(ChildrenRegistry.event_id == event_id)
    )
    kitchen_tasks = await db.execute(
        select(func.count(KitchenTask.id)).where(KitchenTask.event_id == event_id)
    )
    kitchen_done = await db.execute(
        select(func.count(KitchenTask.id)).where(
            KitchenTask.event_id == event_id, KitchenTask.status == "completed"
        )
    )
    stands = await db.execute(
        select(func.count(SalesStand.id)).where(SalesStand.event_id == event_id)
    )
    total_sales = await db.execute(
        select(func.coalesce(func.sum(SalesTransaction.amount), 0)).where(
            SalesTransaction.stand_id.in_(
                select(SalesStand.id).where(SalesStand.event_id == event_id)
            )
        )
    )
    vip_count = await db.execute(
        select(func.count(Guest.id)).where(
            Guest.event_id == event_id, Guest.is_vip == True
        )
    )
    checked_in = await db.execute(
        select(func.count(Guest.id)).where(
            Guest.event_id == event_id, Guest.checked_in == True
        )
    )
    total_guests = await db.execute(
        select(func.count(Guest.id)).where(Guest.event_id == event_id)
    )

    return {
        "event": event.name,
        "event_status": event.status,
        "total_schedules": len(schedules),
        "total_tasks": total_tasks,
        "tasks_completed": completed,
        "tasks_pending": pending,
        "schedule_conflicts": len(conflicts),
        "compliance_pct": round((completed / total_tasks * 100) if total_tasks else 0, 1),
        "children": {
            "classrooms": classrooms.scalar() or 0,
            "registered": total_children.scalar() or 0,
        },
        "kitchen": {
            "tasks": kitchen_tasks.scalar() or 0,
            "completed": kitchen_done.scalar() or 0,
        },
        "sales": {
            "stands": stands.scalar() or 0,
            "total_amount": float(total_sales.scalar() or 0),
        },
        "guests": {
            "total": total_guests.scalar() or 0,
            "vip": vip_count.scalar() or 0,
            "checked_in": checked_in.scalar() or 0,
        },
    }
