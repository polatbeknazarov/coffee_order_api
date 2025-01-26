from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import BaseDAO
from core.models import User
from core.schemas import UserCreate


class UserDAO(BaseDAO[User, UserCreate]):
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
