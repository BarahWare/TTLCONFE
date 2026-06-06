from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.events.service import EventService
from app.modules.inventory.service import InventoryService
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
    overdue = sum(
        1 for t in tasks
        if t.due_datetime and t.status not in ("completed", "cancelled")
    )

    return {
        "event": event.name,
        "event_status": event.status,
        "total_schedules": len(schedules),
        "total_tasks": total_tasks,
        "tasks_completed": completed,
        "tasks_pending": pending,
        "tasks_overdue": overdue,
        "schedule_conflicts": len(conflicts),
        "compliance_pct": round((completed / total_tasks * 100) if total_tasks else 0, 1),
    }
