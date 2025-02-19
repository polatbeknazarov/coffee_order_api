from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import CartRead, CartCreate, UserRead
from crud.carts import CartDAO
from auth.dependencies import http_bearer, require_role

carts_router = APIRouter(
    prefix=settings.api.v1.carts,
    tags=["Carts"],
    dependencies=[Depends(http_bearer)],
)


@carts_router.post("", response_model=CartRead)
async def add_product_to_cart(
    cart_request: CartCreate,
    user: UserRead = Depends(require_role(UserRole.USER)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    cart = await CartDAO.add_product(
        cart_request=cart_request,
        user_id=user.id,
        session=session,
    )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return cart


@carts_router.get("", response_model=List[CartRead])
async def get_all_user_carts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(require_role(UserRole.USER)),
):
    carts = await CartDAO.get_carts_by_user_id(user_id=user.id, session=session)
    return carts


@carts_router.get("/{cart_id}", response_model=CartRead)
async def get_user_cart_by_id(
    cart_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(require_role(UserRole.USER)),
):
    cart = await CartDAO.get_user_cart_by_id(
        user_id=user.id,
        cart_id=cart_id,
        session=session,
    )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found.",
        )

    return cart


@carts_router.delete("/{cart_id}")
async def delete_cart_by_id(
    cart_id: int,
    user: UserRead = Depends(require_role(UserRole.USER)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    cart = await CartDAO.get_by_id(model_id=cart_id, session=session)
    if cart.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this cart.",
        )

    await CartDAO.delete(model_id=cart_id, session=session)
    return {"message": "Cart deleted successfully."}
