from datetime import datetime
from typing import List

from pydantic import BaseModel

from .message import MessageRead


class ChatBase(BaseModel):
    user_id: int


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: int
    created_at: datetime
