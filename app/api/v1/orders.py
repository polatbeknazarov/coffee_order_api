from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import OrderUpdate, OrderRead, UserRead
from crud.orders import OrderDAO
from auth.dependencies import http_bearer, require_role

orders_router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Orders"],
    dependencies=[Depends(http_bearer)],
)


@orders_router.post("", response_model=OrderRead)
async def create_order(
    user: UserRead = Depends(require_role(UserRole.USER)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        order = await OrderDAO.create_order(
            user_id=user.id,
            session=session,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return order


@orders_router.get("/all", response_model=List[OrderRead])
async def get_all_orders(
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    orders = await OrderDAO.get_all(session=session)
    return orders


@orders_router.get("", response_model=List[OrderRead])
async def get_all_current_user_orders(
    user: UserRead = Depends(require_role(UserRole.USER)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    orders = await OrderDAO.find_all(where={"user_id": user.id}, session=session)
    return orders


@orders_router.delete("/{order_id}")
async def delete_order_by_id(
    order_id: int,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await OrderDAO.delete(model_id=order_id, session=session)
    return result


@orders_router.patch("/{order_id}", response_model=OrderRead)
async def update_order_status(
    order_id: int,
    update_order_request: OrderUpdate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await OrderDAO.update(
        model_id=order_id,
        validated_values=update_order_request,
        session=session,
    )
    return result
