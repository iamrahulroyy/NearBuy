from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    itemName: str
    price: float
    description: Optional[str] = None
    note: Optional[str] = None


class ItemUpdate(BaseModel):
    itemName: str = None
    price: Optional[float] = None
    description: Optional[str] = None
    note: Optional[str] = None