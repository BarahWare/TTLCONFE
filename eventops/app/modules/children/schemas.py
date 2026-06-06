from datetime import date, datetime

from pydantic import BaseModel


class ClassroomCreate(BaseModel):
    name: str
    capacity: int | None = None
    age_range: str | None = None
    location: str | None = None
    teacher_id: int | None = None


class ClassroomResponse(BaseModel):
    id: int
    event_id: int
    name: str
    capacity: int | None = None
    age_range: str | None = None
    location: str | None = None
    teacher_id: int | None = None

    model_config = {"from_attributes": True}


class ChildRegister(BaseModel):
    child_name: str
    age: int | None = None
    parent_name: str
    parent_phone: str
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    special_notes: str | None = None


class ChildResponse(BaseModel):
    id: int
    classroom_id: int
    child_name: str
    age: int | None = None
    parent_name: str
    parent_phone: str
    special_notes: str | None = None

    model_config = {"from_attributes": True}


class AttendanceRequest(BaseModel):
    event_date: date
    action: str  # checkin | checkout


class AttendanceResponse(BaseModel):
    id: int
    child_id: int
    event_date: date
    checked_in_at: datetime | None = None
    checked_out_at: datetime | None = None

    model_config = {"from_attributes": True}


class MaterialResponse(BaseModel):
    id: int
    classroom_id: int
    title: str
    description: str | None = None
    file_url: str | None = None
    lesson_date: date | None = None

    model_config = {"from_attributes": True}
