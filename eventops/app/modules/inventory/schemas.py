from pydantic import BaseModel


class InventoryItemCreate(BaseModel):
    category_id: int | None = None
    name: str
    description: str | None = None
    quantity: int = 0
    unit: str | None = None
    is_rented: bool = False
    rental_supplier: str | None = None
    assigned_location: str | None = None
    responsible_user_id: int | None = None
    photo_url: str | None = None
    serial_number: str | None = None
    notes: str | None = None


class InventoryItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    unit: str | None = None
    status: str | None = None
    assigned_location: str | None = None
    responsible_user_id: int | None = None
    notes: str | None = None


class InventoryItemResponse(BaseModel):
    id: int
    event_id: int
    team_id: int
    category_id: int | None = None
    name: str
    description: str | None = None
    quantity: int
    quantity_available: int
    unit: str | None = None
    status: str
    is_rented: bool
    rental_supplier: str | None = None
    assigned_location: str | None = None
    responsible_user_id: int | None = None
    photo_url: str | None = None
    serial_number: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class MovementCreate(BaseModel):
    movement_type: str
    quantity: int
    from_location: str | None = None
    to_location: str | None = None
    notes: str | None = None


class MovementResponse(BaseModel):
    id: int
    item_id: int
    movement_type: str
    quantity: int
    from_location: str | None = None
    to_location: str | None = None
    performed_by: int
    notes: str | None = None
    moved_at: str

    model_config = {"from_attributes": True}


class InventorySummary(BaseModel):
    total_items: int
    available: int
    in_use: int
    under_maintenance: int
    rented: int
    low_stock_items: list[InventoryItemResponse] = []
