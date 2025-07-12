from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    USER = "USER"
    OWNER = "OWNER"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    created_at: Optional[str]

    class Config:
        from_attributes = True
