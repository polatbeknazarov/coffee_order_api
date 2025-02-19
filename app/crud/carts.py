import logging

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from .base import BaseDAO
from core.models import Cart
from core.schemas import CartBase, CartCreate, CartRead, ProductRead
from .products import ProductDAO

log = logging.getLogger(__name__)


class CartDAO(BaseDAO[Cart, CartBase]):
    model = Cart

    @classmethod
    async def get_carts_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Sequence[Cart]:
        stmt = (
            select(Cart)
            .filter(Cart.user_id == user_id)
            .options(selectinload(Cart.product))
        )
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    async def get_user_cart_by_id(
        cls,
        user_id: int,
        cart_id: int,
        session: AsyncSession,
    ) -> Cart | None:
        stmt = (
            select(Cart)
            .filter(Cart.user_id == user_id, Cart.id == cart_id)
            .options(selectinload(Cart.product))
        )
        result = await session.scalars(stmt)
        return result.one_or_none()

    @classmethod
    async def add_product(
        cls,
        cart_request: CartCreate,
        user_id: int,
        session: AsyncSession,
    ) -> CartRead | None:
        product = await ProductDAO.get_by_id(
            model_id=cart_request.product_id,
            session=session,
        )
        if not product:
            return None

        cart_stmt = select(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == cart_request.product_id,
        )
        result = await session.scalars(cart_stmt)
        cart = result.one_or_none()

        if cart:
            cart.quantity += cart_request.quantity
            await session.commit()
        else:
            cart = await cls.create_cart(
                user_id=user_id,
                product_id=cart_request.product_id,
                quantity=cart_request.quantity,
                session=session,
            )

        return CartRead(
            id=cart.id,
            user_id=cart.user_id,
            product=ProductRead(
                id=cart.product.id,
                name=cart.product.name,
                description=cart.product.description,
                category_id=cart.product.category_id,
                price=cart.product.price,
                is_available=cart.product.is_available,
            ),
            quantity=cart.quantity,
            total_price=cart.total_price,
        )

    @classmethod
    async def create_cart(
        cls,
        user_id: int,
        product_id: int,
        quantity: int,
        session: AsyncSession,
    ) -> Cart:
        instance = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(instance)

        try:
            await session.flush()
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            log.error("Error creating cart: %s", e)
            raise

        return instance

    @classmethod
    async def get_user_carts_by_ids(
        cls,
        cart_ids: List[int],
        user_id: int,
        session: AsyncSession,
    ) -> Sequence[CartRead]:
        stmt = select(Cart).filter(Cart.user_id == user_id, Cart.id.in_(cart_ids))
        result = await session.scalars(stmt)
        return result.all()
