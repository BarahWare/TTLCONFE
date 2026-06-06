from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.organizations.models import Organization
from app.shared.exceptions import Conflict, NotFound


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Organization:
        result = await self.db.execute(select(Organization).where(Organization.slug == data["slug"]))
        if result.scalar_one_or_none():
            raise Conflict("Organization slug already exists")
        org = Organization(**data)
        self.db.add(org)
        await self.db.commit()
        await self.db.refresh(org)
        return org

    async def get_all(self) -> list[Organization]:
        result = await self.db.execute(select(Organization).order_by(Organization.name))
        return list(result.scalars().all())

    async def get_by_id(self, org_id: int) -> Organization:
        result = await self.db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()
        if not org:
            raise NotFound("Organization not found")
        return org
