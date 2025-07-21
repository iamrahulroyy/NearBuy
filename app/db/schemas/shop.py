import uuid
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
    shop_id: str =  None
    fullName: Optional[str] =  None
    shopName: Optional[str]=  None
    contact: Optional[str]=  None
    address: Optional[str]=  None
    is_open: Optional[bool]=  None
    latitude: Optional[float]=  None
    longitude: Optional[float]=  None
    note: Optional[str] =  None
