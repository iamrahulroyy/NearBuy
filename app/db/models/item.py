import time
from sqlmodel import Column, Integer, SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    itemName: str = Field(index=True, unique=True)
    price: float
    description: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)
   