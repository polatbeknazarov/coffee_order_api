from pydantic import BaseModel

from core.models import UserRole


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    hashed_password: bytes


class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
