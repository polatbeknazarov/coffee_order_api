from typing import List
from pydantic import BaseModel

from core.models import OrderStatus


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(BaseModel):
    cart_ids: List[int]


class OrderRead(OrderBase):
    id: int
    total_price: float
    status: OrderStatus


class OrderUpdate(BaseModel):
    status: OrderStatus
