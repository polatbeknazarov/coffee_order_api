from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import BaseDAO
from core.models import User
from core.schemas import UserBase


class UserDAO(BaseDAO[User, UserBase]):
    model = User

    @classmethod
    async def get_user_by_email_or_username(
        cls,
        username: str,
        email: str,
        session: AsyncSession,
    ) -> User | None:
        stmt = select(User).filter((User.email == email) | (User.username == username))
        result = await session.scalars(stmt)
        return result.one_or_none()

    @classmethod
    async def get_user_by_email(
        cls,
        email: str,
        session: AsyncSession,
    ) -> User | None:
        stmt = select(User).filter(User.email == email)
        result = await session.scalars(stmt)
        return result.one_or_none()
