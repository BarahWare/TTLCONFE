from datetime import date, datetime

from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    team_id: int
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime
    location: str | None = None
    is_recurring: bool = False
    recurrence_rule: str | None = None


class ScheduleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    location: str | None = None
    is_recurring: bool | None = None
    recurrence_rule: str | None = None


class ScheduleResponse(BaseModel):
    id: int
    event_id: int
    team_id: int
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime
    location: str | None = None
    is_recurring: bool
    recurrence_rule: str | None = None
    created_by: int

    model_config = {"from_attributes": True}


class ScheduleAssignmentCreate(BaseModel):
    user_id: int


class ScheduleAssignmentResponse(BaseModel):
    id: int
    schedule_id: int
    user_id: int
    status: str
    notes: str | None = None

    model_config = {"from_attributes": True}


class ConflictResponse(BaseModel):
    schedule_id: int
    title: str
    user_id: int
    start_datetime: datetime
    end_datetime: datetime
