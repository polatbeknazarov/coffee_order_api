from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(default=True)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
