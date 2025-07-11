from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID
from geoalchemy2 import Geography
from sqlalchemy import Column

class Shop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id")
    name: str
    contact: Optional[str]
    address: Optional[str]
    is_open: bool = Field(default=True)
    location: Optional[str] = Field(
        sa_column=Column(Geography(geometry_type="POINT", srid=4326))
    )
    created_at: Optional[str] = Field(default=None)
