from .base import BaseDAO
from core.models import Category
from core.schemas import CategoryBase


class CategoryDAO(BaseDAO[Category, CategoryBase]):
    model = Category
