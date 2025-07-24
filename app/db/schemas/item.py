from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    shop_id: str
    itemName: str
    price: float
    description: Optional[str] = None
    note: Optional[str] = None


class ItemUpdate(BaseModel):
    shop_id: str = None
    itemName: str = None
    price: Optional[float] = None
    description: Optional[str] = None
    note: Optional[str] = None