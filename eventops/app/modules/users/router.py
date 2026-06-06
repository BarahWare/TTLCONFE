from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.modules.auth.models import User

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("")
async def list_users(org_id: int | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(User)
    if org_id:
        query = query.where(User.org_id == org_id)
    query = query.order_by(User.full_name)
    result = await db.execute(query)
    return result.scalars().all()
