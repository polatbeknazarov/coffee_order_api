from pydantic import BaseModel

from .product import ProductRead


class CartBase(BaseModel):
    product_id: int


class CartCreate(CartBase):
    quantity: int


class CartRead(BaseModel):
    id: int
    user_id: int
    product: ProductRead
    quantity: int
    total_price: float


class CartUpdate(CartBase):
    quantity: int
