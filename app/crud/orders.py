from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from .carts import CartDAO
from .products import ProductDAO
from core.models import Order, OrderItem
from core.schemas import OrderBase


class OrderDAO(BaseDAO[Order, OrderBase]):
    model = Order

    @classmethod
    async def create_order(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Order:
        cart_items = await CartDAO.get_carts_by_user_id(
            user_id=user_id, session=session
        )
        if not cart_items:
            raise ValueError("Cart items not found")

        total_price = 0

        for item in cart_items:
            product = await ProductDAO.get_by_id(
                model_id=item.product_id,
                session=session,
            )
            if not product or not product.is_available:
                raise ValueError(f"Product {item.product_id} unavailable.")

            total_price += item.quantity * product.price

        order = Order(user_id=user_id, total_price=total_price)
        session.add(order)
        await session.flush()
        await session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            session.add(order_item)
            await CartDAO.delete(model_id=item.id, session=session)

        await session.commit()

        return order
