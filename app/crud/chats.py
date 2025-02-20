from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from .base import BaseDAO
from core.models import Chat
from core.schemas import ChatBase, ChatCreate


class ChatDAO(BaseDAO[Chat, ChatBase]):
    model = Chat

    @classmethod
    async def get_or_create(cls, user_id: int, session: AsyncSession) -> Chat:
        chat = await cls.find_one(where={"user_id": user_id}, session=session)

        if not chat:
            chat_data = ChatCreate(user_id=user_id)
            chat = await cls.create(validated_values=chat_data, session=session)

        return chat

    @classmethod
    async def get_chats_with_messages(
        cls,
        session: AsyncSession,
    ) -> Sequence[Chat]:
        stmt = select(Chat).options(selectinload(Chat.messages))
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    async def get_chat_by_id_with_messages(
        cls,
        chat_id: int,
        session: AsyncSession,
    ) -> Chat | None:
        stmt = (
            select(Chat).filter(Chat.id == chat_id).options(selectinload(Chat.messages))
        )
        result = await session.scalars(stmt)
        return result.one_or_none()
