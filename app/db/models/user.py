from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    OWNER = "OWNER"

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER)
    created_at: Optional[str] = Field(default=None)
