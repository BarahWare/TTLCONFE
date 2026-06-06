from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    level: int
    permissions: dict = {}


class RoleResponse(BaseModel):
    id: int
    org_id: int
    name: str
    level: int
    permissions: dict

    model_config = {"from_attributes": True}
