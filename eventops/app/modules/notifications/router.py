from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.notifications.schemas import NotificationResponse, PushTokenRegister
from app.modules.notifications.service import NotificationService

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.post("/push-token")
async def register_push_token(
    body: PushTokenRegister,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    await service.register_token(user.id, body.token, body.platform)
    return {"message": "Token registered"}


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    return await service.get_notifications(user.id)


@router.patch("/{notification_id}/read")
async def mark_read(
    notification_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    n = await service.mark_read(notification_id, user.id)
    return {"message": "Marked as read"} if n else {"message": "Not found"}
