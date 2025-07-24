import time
from sqlmodel import UUID, Column, Integer, SQLModel, Field, func
from typing import Optional
import uuid
from enum import Enum

class UserTableEnum(str, Enum):
    USER = "USER"
    USER_SESSION = "USER_SESSION"
    USER_META = "USER_META"


class UserRole(str, Enum):
    USER = "USER" # this for all user of the service
    VENDOR = "VENDOR" # this for all vendors of the service
    STATE_CONTRIBUTER = "STATE_CONTRIBUTER" # this for all state contributors of the service
    ADMIN = "ADMIN" # this for all admins of the service
    SUPER_ADMIN = "SUPER_ADMIN" # this for all super admins of the service

class ReasonEnum(str, Enum):
    SIGNUP = "SIGNUP" 
    LOGIN = "LOGIN"
    # UPGRADE = "empupgrade"
    # CHECKEMPLOYEE = "emp_checkemployee"


class USER(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True)
    )
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER)
    fullName: Optional[str] = Field(default=None)
    try_count: Optional[int] = Field(default=0)  # for password retry check
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
    updated_at: Optional[int] = Field(default=None,sa_column=Column(Integer, onupdate=func.extract("epoch", func.now())),)
    note: Optional[str] = Field(default=None)

class USER_SESSION(SQLModel, table=True):
    pk: str = Field(primary_key=True)
    email: str
    role: UserRole = Field(index=True) 
    ip: Optional[str]
    browser: Optional[str]
    os: Optional[str]
    created_at: int = Field(default_factory=lambda: int(time.time()))
    expired_at: int

class USER_META(SQLModel, table=True):
    pk: int = Field(primary_key=True)
    email: str
    reason: ReasonEnum  # signup, login, resetPassword, changePassword, set2fa, remove2fa, change2fa, confirmEmail, resetApikey
    ip: Optional[str]
    role : UserRole
    browser: Optional[str]
    os: Optional[str]
    ts: Optional[int] = Field(default_factory=lambda: int(time.time()))

