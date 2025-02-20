from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .manager import manager
from core.models import db_helper
from core.schemas import MessageCreate, MessageRead
from crud.chats import ChatDAO
from crud.messages import MessageDAO

ws_router = APIRouter()


@ws_router.websocket("/ws/chat/{user_id}")
async def client_ws(
    websocket: WebSocket,
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    chat = await ChatDAO.get_or_create(user_id=user_id, session=session)
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            message_data = MessageCreate(
                chat_id=chat.id,
                sender_id=2,
                message_text=data["message"],
            )
            message = await MessageDAO.create(
                validated_values=message_data, session=session
            )
            message_data = MessageRead(
                id=message.id,
                chat_id=message.chat_id,
                sender_id=message.sender_id,
                message_text=message.message_text,
                created_at=message.created_at,
            )

            await manager.broadcast(user_id, message_data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast(user_id, {"message": f"User {user_id} left the chat"})


@ws_router.websocket("/ws/admin/{chat_id}")
async def admin_chat(
    websocket: WebSocket,
    chat_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    chat = await ChatDAO.get_by_id(model_id=chat_id, session=session)
    if not chat:
        await websocket.close()
        return

    await manager.connect(websocket, chat_id)

    try:
        while True:
            data = await websocket.receive_json()
            message_data = MessageCreate(
                chat_id=chat_id,
                sender_id=2,
                message_text=data["message"],
            )
            message = await MessageDAO.create(
                validated_values=message_data, session=session
            )
            message_data = MessageRead(
                id=message.id,
                chat_id=message.chat_id,
                sender_id=message.sender_id,
                message_text=message.message_text,
                created_at=message.created_at,
            )

            await manager.broadcast(chat_id, message_data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
        await manager.broadcast(chat_id, {"message": "Admin left the chat"})
