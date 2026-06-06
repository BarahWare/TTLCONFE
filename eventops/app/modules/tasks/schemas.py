from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    team_id: int
    schedule_id: int | None = None
    title: str
    description: str | None = None
    scope: str | None = None
    location: str | None = None
    priority: str = "normal"
    due_datetime: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    scope: str | None = None
    location: str | None = None
    priority: str | None = None
    status: str | None = None
    due_datetime: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    event_id: int
    team_id: int
    schedule_id: int | None = None
    title: str
    description: str | None = None
    scope: str | None = None
    location: str | None = None
    priority: str
    status: str
    due_datetime: datetime | None = None
    created_by: int

    model_config = {"from_attributes": True}


class TaskAssignmentCreate(BaseModel):
    user_id: int


class TaskAssignmentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int

    model_config = {"from_attributes": True}
