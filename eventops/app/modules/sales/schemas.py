from datetime import datetime

from pydantic import BaseModel


class StandCreate(BaseModel):
    name: str
    location: str | None = None
    category: str | None = None
    responsible_id: int | None = None
    opening_balance: float = 0
    notes: str | None = None


class StandResponse(BaseModel):
    id: int
    event_id: int
    name: str
    location: str | None = None
    category: str | None = None
    responsible_id: int | None = None
    opening_balance: float
    notes: str | None = None

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    price: float
    cost: float | None = None
    stock: int = 0
    category: str | None = None


class ProductResponse(BaseModel):
    id: int
    stand_id: int
    name: str
    price: float
    cost: float | None = None
    stock: int
    category: str | None = None

    model_config = {"from_attributes": True}


class TransactionCreate(BaseModel):
    amount: float
    type: str
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    stand_id: int
    amount: float
    type: str
    description: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReconcileRequest(BaseModel):
    actual_total: float
    notes: str | None = None


class ReconciliationResponse(BaseModel):
    id: int
    stand_id: int
    expected_total: float
    actual_total: float
    difference: float
    reconciled_at: datetime

    model_config = {"from_attributes": True}
