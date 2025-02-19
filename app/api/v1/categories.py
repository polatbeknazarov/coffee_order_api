from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import CategoryCreate, CategoryRead, UserRead
from crud.categories import CategoryDAO
from auth.dependencies import http_bearer, require_role

categories_router = APIRouter(
    prefix=settings.api.v1.categories,
    tags=["Categories"],
    dependencies=[Depends(http_bearer)],
)


@categories_router.post("", response_model=CategoryRead)
async def create_category(
    category_create: CategoryCreate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    category = await CategoryDAO.create(
        validated_values=category_create, session=session
    )
    return category


@categories_router.get("", response_model=List[CategoryRead])
async def get_all_categories(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    categories = await CategoryDAO.get_all(session=session)
    return categories


@categories_router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    category = await CategoryDAO.get_by_id(model_id=category_id, session=session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


@categories_router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_update: CategoryCreate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    category = await CategoryDAO.update(
        model_id=category_id,
        validated_values=category_update,
        session=session,
    )
    return category


@categories_router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await CategoryDAO.delete(model_id=category_id, session=session)
    return result
