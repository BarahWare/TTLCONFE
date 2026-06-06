from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.organizations.schemas import OrganizationCreate, OrganizationResponse
from app.modules.organizations.service import OrganizationService
from app.shared.exceptions import Conflict, NotFound

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("", response_model=list[OrganizationResponse])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    service = OrganizationService(db)
    return await service.get_all()


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(body: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    service = OrganizationService(db)
    try:
        org = await service.create(body.model_dump())
    except Conflict as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    return org


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    service = OrganizationService(db)
    try:
        return await service.get_by_id(org_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
