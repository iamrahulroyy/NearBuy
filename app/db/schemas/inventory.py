from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, conint

from app.db.models.inventory import StockStatus

class InventoryBase(BaseModel):
    shop_id: str
    item_id: str
    quantity: int
    price_at_entry: Optional[float] = None
    min_quantity: Optional[int] = 5
    max_quantity: Optional[int] = 100
    status: Optional[StockStatus] = StockStatus.IN_STOCK
    location: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[int] = None 
    note: Optional[str] = None

# class InventoryCreate(InventoryBase):
#     last_restocked_at: Optional[int] = None  

# class InventoryRead(InventoryBase):
#     last_restocked_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True

class InventoryUpdate(BaseModel):
    inventory_id: Optional[str] = None
    shop_id: Optional[str] = None
    item_id: Optional[str] = None
    quantity: Optional[Annotated[int, conint(ge=0)]] = None
    price_at_entry: Optional[float] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    status: Optional[StockStatus] = None
    location: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[int] = None
    note: Optional[str] = None
    last_restocked_at: Optional[int] = None
    