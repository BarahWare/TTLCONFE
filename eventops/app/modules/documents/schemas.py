from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    description: str | None = None
    file_url: str
    file_type: str | None = None
    file_size_bytes: int | None = None
    tags: list[str] | None = None
    category: str | None = None
    is_public_to_event: bool = False


class DocumentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    is_public_to_event: bool | None = None


class DocumentResponse(BaseModel):
    id: int
    event_id: int
    team_id: int
    title: str
    description: str | None = None
    file_url: str
    file_type: str | None = None
    file_size_bytes: int | None = None
    tags: list[str] | None = None
    category: str | None = None
    uploaded_by: int
    version: int
    is_public_to_event: bool

    model_config = {"from_attributes": True}
