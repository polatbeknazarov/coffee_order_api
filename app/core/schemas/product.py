from pydantic import BaseModel
from fastapi_filter.contrib.sqlalchemy import Filter

from .category import CategoryRead
from core.models import Product


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    category_id: int


class ProductRead(ProductBase):
    id: int
    category_id: int
    is_available: bool


class ProductUpdate(ProductBase):
    is_available: bool


class ProductFilter(Filter):
    name__in: list | None = None
    price__gte: float | None = None
    price__lte: float | None = None

    class Constants(Filter.Constants):
        model = Product

    class Config:
        allow_population_by_field_name = True
