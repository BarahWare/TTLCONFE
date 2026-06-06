from datetime import date

from pydantic import BaseModel


class EventCreate(BaseModel):
    org_id: int
    name: str
    description: str | None = None
    start_date: date
    end_date: date
    location: str | None = None


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
    status: str | None = None


class EventResponse(BaseModel):
    id: int
    org_id: int
    name: str
    description: str | None = None
    start_date: date
    end_date: date
    location: str | None = None
    status: str
    created_at: str

    model_config = {"from_attributes": True}
