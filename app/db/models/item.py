from enum import Enum
import uuid
from sqlmodel import UUID, Column, SQLModel, Field
from typing import Optional

class ItemTableEnum(str, Enum):
    ITEM = "ITEM"
class ITEM(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True)
    )
    itemName: str = Field(index=True, unique=True)
    price: float
    description: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)
   