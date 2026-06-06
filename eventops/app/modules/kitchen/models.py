from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class KitchenMenu(Base):
    __tablename__ = "kitchen_menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    menu_date: Mapped[date] = mapped_column(Date, nullable=False)
    meal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_portions: Mapped[int | None] = mapped_column(Integer, nullable=True)


class KitchenSupplier(Base):
    __tablename__ = "kitchen_suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)


class KitchenIngredient(Base):
    __tablename__ = "kitchen_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("kitchen_suppliers.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    quantity_needed: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    quantity_in_stock: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class KitchenPurchaseOrder(Base):
    __tablename__ = "kitchen_purchase_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("kitchen_suppliers.id"), nullable=True)
    order_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expected_delivery: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    total_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class KitchenTask(Base):
    __tablename__ = "kitchen_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    menu_id: Mapped[int | None] = mapped_column(ForeignKey("kitchen_menus.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    scheduled_time: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
