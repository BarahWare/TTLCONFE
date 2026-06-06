from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.teams.schemas import AddMemberRequest, MemberResponse, TeamCreate, TeamResponse, TeamUpdate
from app.modules.teams.service import TeamService
from app.shared.exceptions import Conflict, NotFound

router = APIRouter(tags=["teams"])


@router.get("/api/v1/events/{event_id}/teams", response_model=list[TeamResponse])
async def list_teams(event_id: int, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    return await service.get_by_event(event_id)


@router.post("/api/v1/events/{event_id}/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(event_id: int, body: TeamCreate, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    return await service.create(event_id, body.model_dump())


@router.get("/api/v1/teams/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    try:
        return await service.get_by_id(team_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.patch("/api/v1/teams/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, body: TeamUpdate, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    try:
        return await service.update(team_id, body.model_dump(exclude_none=True))
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("/api/v1/teams/{team_id}/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(team_id: int, body: AddMemberRequest, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    team = await service.get_by_id(team_id)
    try:
        assignment = await service.add_member(team_id, body.user_id, body.role_id, team.event_id)
        return MemberResponse(
            id=assignment.id,
            user_id=assignment.user_id,
            team_id=assignment.team_id,
            role_id=assignment.role_id,
            is_active=assignment.is_active,
        )
    except Conflict as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@router.delete("/api/v1/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(team_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    try:
        await service.remove_member(team_id, user_id)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.get("/api/v1/teams/{team_id}/members", response_model=list[MemberResponse])
async def list_members(team_id: int, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    return await service.get_members(team_id)
