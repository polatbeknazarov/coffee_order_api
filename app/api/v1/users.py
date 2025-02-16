from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import UserRead, UserUpdate
from crud.users import UserDAO
from auth.dependencies import get_current_user, http_bearer

users_router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@users_router.get("/me", response_model=UserRead)
async def get_current_auth_user(
    user: UserRead = Depends(get_current_user),
):
    return user


@users_router.patch("/me", response_model=UserRead)
async def update_current_user(
    user_update: UserUpdate,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_user = await UserDAO.update(
        model_id=user.id,
        validated_values=user_update,
        session=session,
    )
    return updated_user


@users_router.delete("/me")
async def delete_current_user(
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await UserDAO.delete(model_id=user.id, session=session)
    return True


@users_router.get("", response_model=List[UserRead])
async def get_all_users(
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource.",
        )

    users = await UserDAO.get_all(session=session)
    return users


@users_router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource.",
        )

    user = await UserDAO.get_by_id(model_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found.",
        )

    return user
