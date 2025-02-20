from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import MessageRead, UserRead, MessageUpdate
from crud.chats import ChatDAO
from crud.messages import MessageDAO
from auth.dependencies import http_bearer, get_current_user

messages_router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
    dependencies=[Depends(http_bearer)],
)


@messages_router.get("/{chat_id}", response_model=List[MessageRead])
async def get_chat_messages(
    chat_id: int,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chat = await ChatDAO.get_by_id(model_id=chat_id, session=session)
    if chat.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get this chat.",
        )

    chat_messages = await MessageDAO.find_all(
        where={"chat_id": chat_id},
        session=session,
    )
    return chat_messages


@messages_router.delete("/{message_id}")
async def delete_message_by_id(
    message_id: int,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    message = await MessageDAO.get_by_id(model_id=message_id, session=session)
    if message.sender_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get this chat.",
        )

    result = await MessageDAO.delete(model_id=message_id, session=session)
    return result


@messages_router.patch("/{message_id}", response_model=MessageRead)
async def update_message(
    request: MessageUpdate,
    message_id: int,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    message = await MessageDAO.get_by_id(model_id=message_id, session=session)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    if message.sender_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this message.",
        )

    result = await MessageDAO.update(
        model_id=message_id,
        validated_values=request,
        session=session,
    )
    return result
