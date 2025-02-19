from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class StaticInfo(Base):
    __tablename__ = "static_info"

    key: Mapped[str] = mapped_column(nullable=False, unique=True)
    value: Mapped[str] = mapped_column(Text(), nullable=False)
