from typing import Annotated
from pydantic import BaseModel, conint

class InventoryBase(BaseModel):
    shop_id: int
    item_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    class Config:
        orm_mode = True

class InventoryUpdate(BaseModel):
    shop_id: int
    item_id: int
    quantity: Annotated[int, conint(ge=0)]
    