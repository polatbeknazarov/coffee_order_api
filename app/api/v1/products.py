from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi_filter import FilterDepends

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
    ProductFilter,
    UserRead,
)
from crud.products import ProductDAO
from auth.dependencies import http_bearer, require_role

products_router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
    dependencies=[Depends(http_bearer)],
)


@products_router.get("")
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page."),
    category_id: int | None = Query(None, description="Category ID."),
    search: str | None = Query(None, description="Search query."),
    sort_by: str | None = Query(None, description="Field to sort by."),
    sort_order: str | None = Query(
        None,
        regex="^(asc|desc)$",
        description="Sort order (asc or desc).",
    ),
    filters: ProductFilter = FilterDepends(ProductFilter),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    products = await ProductDAO.get_filtered_products(
        session=session,
        page=page,
        limit=limit,
        category_id=category_id,
        search=search,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return products


@products_router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    product = await ProductDAO.get_by_id(model_id=product_id, session=session)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@products_router.post("", response_model=ProductRead)
async def create_product(
    product_create: ProductCreate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        product = await ProductDAO.create(
            validated_values=product_create, session=session
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id",
        )

    return product


@products_router.patch("/{product_id}", response_model=ProductUpdate)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_product = await ProductDAO.update(
        model_id=product_id, validated_values=product_update, session=session
    )
    return updated_product


@products_router.delete("/{product_id}")
async def delete_product_by_id(
    product_id: int,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await ProductDAO.delete(model_id=product_id, session=session)
    return {"message": "Product deleted successfully."}
