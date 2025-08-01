from enum import Enum
import uuid
import time
from sqlmodel import Integer, SQLModel, Field, func
from typing import Optional
from uuid import UUID
from geoalchemy2 import Geography
from sqlalchemy import Column

class ShopTableEnum(str, Enum):
    SHOP = "SHOP"

class SHOP(SQLModel, table=True):
    __tablename__ = "shop"
    shop_id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    ) 
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
