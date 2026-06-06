from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GuestCategory(Base):
    __tablename__ = "guest_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    color_label: Mapped[str | None] = mapped_column(String(20), nullable=True)


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("guest_categories.id"), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    organization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    has_plus_one: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    invitation_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    checked_in: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_in_at: Mapped[datetime | None] = mapped_column(nullable=True)
    assigned_transport: Mapped[str | None] = mapped_column(String(255), nullable=True)
    assigned_hotel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
