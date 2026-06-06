from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    slug: str
    logo_url: str | None = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    slug: str
    logo_url: str | None = None
    created_at: str

    model_config = {"from_attributes": True}
