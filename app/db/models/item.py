from enum import Enum
import uuid
from sqlmodel import UUID, Column, SQLModel, Field
from typing import Optional

class ItemTableEnum(str, Enum):
    ITEM = "ITEM"
class ITEM(SQLModel, table=True):
    __tablename__ = "item"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True)
    )
    shop_id: uuid.UUID  = Field(foreign_key="shop.shop_id")
    itemName: str = Field(index=True)
    price: float
    description: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)
   