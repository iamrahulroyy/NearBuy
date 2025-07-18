from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.db.schemas.user import Register_Vendor

# class ShopBase(BaseModel):
#     fullName: str
#     shopName: str
#     address: str
#     contact: Optional[str]
#     is_open: bool

# class ShopCreate(ShopBase):
#     owner_id: UUID
#     latitude: float
#     longitude: float

# class ShopRead(ShopBase):
#     id: int
#     created_at: Optional[str]

#     class Config:
#         from_attributes = True

class ShopCreate(Register_Vendor):
    owner_id: UUID
    latitude: float
    longitude: float

class ShopUpdate(BaseModel):
    fullName: Optional[str]
    shopName: Optional[str]
    contact: Optional[str]
    address: Optional[str]
    is_open: Optional[bool]
    latitude: Optional[float]
    longitude: Optional[float]
    note: str
