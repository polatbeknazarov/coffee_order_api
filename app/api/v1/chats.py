from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import ChatRead, UserRead
from crud.chats import ChatDAO
from auth.dependencies import http_bearer, require_role, get_current_user

chats_router = APIRouter(
    prefix=settings.api.v1.chats,
    tags=["Chats"],
    dependencies=[Depends(http_bearer)],
)


@chats_router.get("", response_model=List[ChatRead])
async def get_all_chats(
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chats = await ChatDAO.get_all(session=session)
    return chats


@chats_router.get("/{chat_id}", response_model=ChatRead)
async def get_chat_by_id(
    chat_id: int,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chat = await ChatDAO.get_by_id(model_id=chat_id, session=session)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    if chat.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get this chat.",
        )

    return chat


@chats_router.delete("/{chat_id}")
async def delete_chat_by_id(
    chat_id: int,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await ChatDAO.delete(model_id=chat_id, session=session)
    return result
