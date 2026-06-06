from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.roles.schemas import RoleCreate, RoleResponse
from app.modules.roles.service import RoleService
from app.shared.exceptions import Conflict

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("", response_model=list[RoleResponse])
async def list_roles(org_id: int, db: AsyncSession = Depends(get_db)):
    service = RoleService(db)
    return await service.get_by_org(org_id)


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(org_id: int, body: RoleCreate, db: AsyncSession = Depends(get_db)):
    service = RoleService(db)
    try:
        return await service.create(org_id, body.model_dump())
    except Conflict as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
