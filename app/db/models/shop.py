import time
from sqlmodel import Integer, SQLModel, Field, func
from typing import Optional
from uuid import UUID
from geoalchemy2 import Geography
from sqlalchemy import Column

class Shop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id")
    fullName: str
    shopName: str
    address: str
    contact: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    is_open: bool = Field(default=True)
    location: Optional[str] = Field(
        sa_column=Column(Geography(geometry_type="POINT", srid=4326))
    )
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
    updated_at: Optional[int] = Field(default=None,sa_column=Column(Integer, onupdate=func.extract("epoch", func.now())),)
    note: Optional[str] = Field(default=None)
