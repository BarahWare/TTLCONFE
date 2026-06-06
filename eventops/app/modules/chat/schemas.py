from datetime import datetime

from pydantic import BaseModel


class ChannelCreate(BaseModel):
    team_id: int | None = None
    name: str
    channel_type: str = "team"


class ChannelResponse(BaseModel):
    id: int
    event_id: int
    team_id: int | None = None
    name: str
    channel_type: str

    model_config = {"from_attributes": True}


class MessageSend(BaseModel):
    content: str
    message_type: str = "text"
    file_url: str | None = None
    is_priority: bool = False


class MessageResponse(BaseModel):
    id: int
    channel_id: int
    sender_id: int
    content: str | None = None
    message_type: str
    file_url: str | None = None
    is_pinned: bool
    is_priority: bool
    sent_at: datetime

    model_config = {"from_attributes": True}


class DirectMessageSend(BaseModel):
    content: str
    message_type: str = "text"
    file_url: str | None = None


class DirectMessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str | None = None
    message_type: str
    file_url: str | None = None
    read_at: datetime | None = None
    sent_at: datetime

    model_config = {"from_attributes": True}
