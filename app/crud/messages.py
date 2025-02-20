from .base import BaseDAO
from core.models import Message
from core.schemas import MessageBase


class MessageDAO(BaseDAO[Message, MessageBase]):
    model = Message
