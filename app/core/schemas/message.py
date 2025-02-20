from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    chat_id: int


class MessageCreate(MessageBase):
    sender_id: int
    message_text: str


class MessageRead(MessageCreate):
    id: int
    created_at: datetime
