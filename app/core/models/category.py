from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=True)

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
    )
