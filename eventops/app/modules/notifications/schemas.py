from pydantic import BaseModel


class PushTokenRegister(BaseModel):
    token: str
    platform: str


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    title: str
    body: str | None = None
    notification_type: str
    is_read: bool
    related_entity_type: str | None = None
    related_entity_id: int | None = None

    model_config = {"from_attributes": True}
