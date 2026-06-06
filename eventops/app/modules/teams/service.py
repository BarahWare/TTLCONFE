from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.modules.auth.models import User
from app.modules.teams.models import Role, Team, UserTeamAssignment
from app.shared.exceptions import Conflict, NotFound


class TeamService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_id: int, data: dict) -> Team:
        team = Team(event_id=event_id, **data)
        self.db.add(team)
        await self.db.commit()
        await self.db.refresh(team)
        return team

    async def get_by_event(self, event_id: int) -> list[Team]:
        result = await self.db.execute(
            select(Team).where(Team.event_id == event_id).order_by(Team.name)
        )
        return list(result.scalars().all())

    async def get_by_id(self, team_id: int) -> Team:
        result = await self.db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        if not team:
            raise NotFound("Team not found")
        return team

    async def update(self, team_id: int, data: dict) -> Team:
        team = await self.get_by_id(team_id)
        for key, value in data.items():
            if value is not None:
                setattr(team, key, value)
        await self.db.commit()
        await self.db.refresh(team)
        return team

    async def add_member(self, team_id: int, user_id: int, role_id: int, event_id: int) -> UserTeamAssignment:
        result = await self.db.execute(
            select(UserTeamAssignment).where(
                UserTeamAssignment.user_id == user_id,
                UserTeamAssignment.team_id == team_id,
                UserTeamAssignment.event_id == event_id,
            )
        )
        if result.scalar_one_or_none():
            raise Conflict("User already in this team")

        assignment = UserTeamAssignment(
            user_id=user_id, team_id=team_id, role_id=role_id, event_id=event_id
        )
        self.db.add(assignment)
        await self.db.commit()
        await self.db.refresh(assignment)
        return assignment

    async def remove_member(self, team_id: int, user_id: int):
        result = await self.db.execute(
            select(UserTeamAssignment).where(
                UserTeamAssignment.team_id == team_id,
                UserTeamAssignment.user_id == user_id,
            )
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            raise NotFound("Member not found in this team")
        await self.db.delete(assignment)
        await self.db.commit()

    async def get_members(self, team_id: int) -> list[dict]:
        result = await self.db.execute(
            select(UserTeamAssignment, User, Role)
            .join(User, UserTeamAssignment.user_id == User.id)
            .join(Role, UserTeamAssignment.role_id == Role.id)
            .where(UserTeamAssignment.team_id == team_id)
        )
        members = []
        for assignment, user, role in result.all():
            members.append({
                "id": assignment.id,
                "user_id": user.id,
                "team_id": assignment.team_id,
                "role_id": assignment.role_id,
                "is_active": assignment.is_active,
                "user_full_name": user.full_name,
                "user_email": user.email,
                "role_name": role.name,
            })
        return members
