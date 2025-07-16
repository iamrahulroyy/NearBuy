from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    USER = "USER"
    OWNER = "OWNER"
    STATE_CONTRIBUTER = "STATE_CONTRIBUTER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    

class UserBase(BaseModel):
    email: EmailStr
    fullName: Optional[str] = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    created_at: Optional[str]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None