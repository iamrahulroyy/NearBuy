from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum
from typing import Optional

from app.db.models.user import UserRole


class Register_User(BaseModel):
    fullName: str = "test"
    email: EmailStr = "test@example.com"
    password: str = "test1234"
    role: UserRole = UserRole.USER

class Register_Vendor(BaseModel):
    fullName: str = "test vendor"
    shopName: str = "test shop"
    address: str = "test address, sector V"
    contact: Optional[str] = "test contact"
    email: Optional[EmailStr] = "testvendor@example1.com"
    password: str = "test1234"
    role: UserRole = UserRole.VENDOR

class Register_STATE_CONTRIBUTER(BaseModel):
    fullName: str = "test contributor"
    email: EmailStr = "test_contributor@example.com"
    password: str = "test1234"
    role: UserRole = UserRole.STATE_CONTRIBUTER

class Login_User(BaseModel):
    email: Optional[EmailStr] = "test@example.com"
    password: str = "test1234"
    keepLogin: bool = True
