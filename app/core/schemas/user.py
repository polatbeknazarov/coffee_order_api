from pydantic import BaseModel

from core.models import UserRole


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None


class UserRead(UserBase):
    role: UserRole
    is_active: bool
