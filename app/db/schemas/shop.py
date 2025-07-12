from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ShopBase(BaseModel):
    name: str
    contact: Optional[str]
    address: Optional[str]
    is_open: bool

class ShopCreate(ShopBase):
    owner_id: UUID
    latitude: float
    longitude: float

class ShopRead(ShopBase):
    id: int
    created_at: Optional[str]

    class Config:
        from_attributes = True

class ShopUpdate(ShopBase):
    pass