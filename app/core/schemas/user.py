from pydantic import BaseModel, EmailStr

from core.models import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: bytes


class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool


class UserUpdate(UserBase):
    pass


class UserAdminCreate(UserCreate):
    role: UserRole
    is_active: bool = True
    is_verified: bool = True
