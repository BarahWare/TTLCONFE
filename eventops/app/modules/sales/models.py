from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SalesStand(Base):
    __tablename__ = "sales_stands"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    responsible_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    opening_balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class SalesProduct(Base):
    __tablename__ = "sales_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    stand_id: Mapped[int] = mapped_column(ForeignKey("sales_stands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)


class SalesTransaction(Base):
    __tablename__ = "sales_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    stand_id: Mapped[int] = mapped_column(ForeignKey("sales_stands.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    registered_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class SalesReconciliation(Base):
    __tablename__ = "sales_reconciliation"

    id: Mapped[int] = mapped_column(primary_key=True)
    stand_id: Mapped[int] = mapped_column(ForeignKey("sales_stands.id"), nullable=False)
    expected_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    actual_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    difference: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    reconciled_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reconciled_at: Mapped[datetime] = mapped_column(default=datetime.now)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
