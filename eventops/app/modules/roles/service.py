from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.teams.models import Role
from app.shared.exceptions import Conflict, NotFound


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, org_id: int, data: dict) -> Role:
        result = await self.db.execute(
            select(Role).where(Role.org_id == org_id, Role.name == data["name"])
        )
        if result.scalar_one_or_none():
            raise Conflict("Role already exists in this organization")
        role = Role(org_id=org_id, **data)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def get_by_org(self, org_id: int) -> list[Role]:
        result = await self.db.execute(
            select(Role).where(Role.org_id == org_id).order_by(Role.level)
        )
        return list(result.scalars().all())
