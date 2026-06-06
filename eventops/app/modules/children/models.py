from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ChildrenClassroom(Base):
    __tablename__ = "children_classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_range: Mapped[str | None] = mapped_column(String(50), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class ChildrenRegistry(Base):
    __tablename__ = "children_registry"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("children_classrooms.id"), nullable=False)
    child_name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parent_name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    special_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)


class ChildrenAttendance(Base):
    __tablename__ = "children_attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("children_registry.id"), nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    checked_in_at: Mapped[datetime | None] = mapped_column(nullable=True)
    checked_out_at: Mapped[datetime | None] = mapped_column(nullable=True)
    checked_in_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    checked_out_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class ChildrenTeachingMaterial(Base):
    __tablename__ = "children_teaching_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("children_classrooms.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    lesson_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
