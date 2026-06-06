from datetime import date, datetime

from pydantic import BaseModel


class MenuCreate(BaseModel):
    name: str
    menu_date: date
    meal_type: str
    description: str | None = None
    estimated_portions: int | None = None


class MenuResponse(BaseModel):
    id: int
    event_id: int
    name: str
    menu_date: date
    meal_type: str
    description: str | None = None
    estimated_portions: int | None = None

    model_config = {"from_attributes": True}


class IngredientCreate(BaseModel):
    name: str
    supplier_id: int | None = None
    unit: str | None = None
    quantity_needed: float = 0
    quantity_in_stock: float = 0
    unit_cost: float | None = None
    notes: str | None = None


class IngredientResponse(BaseModel):
    id: int
    name: str
    supplier_id: int | None = None
    unit: str | None = None
    quantity_needed: float
    quantity_in_stock: float
    unit_cost: float | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class PurchaseOrderCreate(BaseModel):
    supplier_id: int | None = None
    notes: str | None = None


class PurchaseOrderResponse(BaseModel):
    id: int
    event_id: int
    supplier_id: int | None = None
    order_date: date | None = None
    expected_delivery: date | None = None
    status: str
    total_amount: float | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class KitchenTaskCreate(BaseModel):
    menu_id: int | None = None
    title: str
    assigned_to: int | None = None
    scheduled_time: datetime | None = None
    notes: str | None = None


class KitchenTaskResponse(BaseModel):
    id: int
    title: str
    assigned_to: int | None = None
    scheduled_time: datetime | None = None
    status: str
    notes: str | None = None

    model_config = {"from_attributes": True}
