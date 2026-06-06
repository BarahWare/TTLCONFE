from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    team_type: str
    description: str | None = None
    color: str | None = None
    icon: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    color: str | None = None
    icon: str | None = None


class TeamResponse(BaseModel):
    id: int
    event_id: int
    name: str
    team_type: str
    description: str | None = None
    color: str | None = None
    icon: str | None = None
    member_count: int = 0

    model_config = {"from_attributes": True}


class AddMemberRequest(BaseModel):
    user_id: int
    role_id: int


class MemberResponse(BaseModel):
    id: int
    user_id: int
    team_id: int
    role_id: int
    is_active: bool
    user_full_name: str = ""
    user_email: str = ""
    role_name: str = ""

    model_config = {"from_attributes": True}
