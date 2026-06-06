from datetime import datetime

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    priority: int = 0
    color_label: str | None = None


class CategoryResponse(BaseModel):
    id: int
    event_id: int
    name: str
    priority: int
    color_label: str | None = None

    model_config = {"from_attributes": True}


class GuestCreate(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    organization: str | None = None
    role_title: str | None = None
    is_vip: bool = False
    has_plus_one: bool = False
    category_id: int | None = None
    notes: str | None = None
    assigned_transport: str | None = None
    assigned_hotel: str | None = None


class GuestResponse(BaseModel):
    id: int
    event_id: int
    category_id: int | None = None
    full_name: str
    email: str | None = None
    phone: str | None = None
    organization: str | None = None
    role_title: str | None = None
    is_vip: bool
    has_plus_one: bool
    invitation_sent: bool
    confirmed: bool
    checked_in: bool
    notes: str | None = None

    model_config = {"from_attributes": True}
