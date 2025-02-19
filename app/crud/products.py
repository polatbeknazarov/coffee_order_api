import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, asc, desc

from .base import BaseDAO
from core.models import Product
from core.schemas import ProductBase, ProductFilter

log = logging.getLogger(__name__)


class ProductDAO(BaseDAO[Product, ProductBase]):
    model = Product

    @classmethod
    async def get_filtered_products(
        cls,
        session: AsyncSession,
        category_id: int | None = None,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        filters: ProductFilter | None = None,
        sort_by: str | None = None,
        sort_order: str = None,
    ):
        try:
            base_query = filters.filter(
                select(cls.model).where(cls.model.is_available.is_(True))
            )

            if search:
                base_query = base_query.where(cls.model.name.ilike(f"%{search}%"))

            if category_id:
                base_query = base_query.where(cls.model.category_id == category_id)

            if sort_by and hasattr(cls.model, sort_by):
                order_by_clause = (
                    asc(getattr(cls.model, sort_by))
                    if sort_order.lower() == "asc"
                    else desc(getattr(cls.model, sort_by))
                )
                base_query = base_query.order_by(order_by_clause)

            total = (
                await session.scalar(
                    select(func.count()).select_from(base_query.alias())
                )
                or 0
            )
            total_pages = (total + limit - 1) // limit

            stmt = base_query.offset((page - 1) * limit).limit(limit)
            result = await session.scalars(stmt)
            products = result.all()

            return {
                "products": products,
                "pagination": {
                    "total": total,
                    "page": page,
                    "page_size": limit,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1,
                },
            }
        except Exception as e:
            log.exception("Database query failed: %s", e)
            return {
                "products": [],
                "pagination": {
                    "total": 0,
                    "page": page,
                    "page_size": limit,
                    "total_pages": 0,
                    "has_next": False,
                    "has_prev": False,
                },
            }

    @classmethod
    async def check_product_is_available(
        cls,
        product_id: int,
        session: AsyncSession,
    ) -> Product | None:
        product = await cls.get_by_id(model_id=product_id, session=session)

        if not product or not product.is_available:
            return None

        return product
