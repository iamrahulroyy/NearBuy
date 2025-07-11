from sqlmodel import SQLModel, Field
from typing import Optional

class Inventory(SQLModel, table=True):
    shop_id: int = Field(foreign_key="shop.id", primary_key=True)
    item_id: int = Field(foreign_key="item.id", primary_key=True)
    quantity: int = Field(default=0)
