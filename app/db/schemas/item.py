from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    itemName: str
    price: float
    description: Optional[str] = None
    note: Optional[str] = None


class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    itemName: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    note: Optional[str] = None