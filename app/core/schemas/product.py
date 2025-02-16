from pydantic import BaseModel

from .category import CategoryRead


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    category_id: int


class ProductRead(ProductBase):
    id: int
    category: CategoryRead
    is_available: bool


class ProductUpdate(ProductBase):
    is_available: bool
