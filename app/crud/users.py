from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

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

    @classmethod
    async def verify_user(cls, user_id: int, session: AsyncSession) -> User:
        try:
            user = await cls.get_by_id(model_id=user_id, session=session)
            user.is_verified = True
            await session.commit()
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise
